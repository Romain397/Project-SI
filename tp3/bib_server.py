import json
import socket
import socketserver
import threading
from dataclasses import dataclass

from bib_core import InMemoryRepository, LibraryService, NotFoundError


SERVICE = LibraryService(InMemoryRepository())


@dataclass(frozen=True, slots=True)
class Subscriber:
    client_id: str
    name: str
    host: str
    port: int


class NotificationHub:
    def __init__(self) -> None:
        self._subscribers: dict[str, Subscriber] = {}
        self._lock = threading.Lock()

    def subscribe(self, client_id: str, name: str, host: str, port: int) -> dict:
        subscriber = Subscriber(client_id=client_id, name=name, host=host, port=port)
        with self._lock:
            self._subscribers[client_id] = subscriber
            count = len(self._subscribers)
        return {"status": "OK", "client_id": client_id, "subscribers": count}

    def unsubscribe(self, client_id: str) -> dict:
        with self._lock:
            removed = self._subscribers.pop(client_id, None)
            count = len(self._subscribers)
        return {"status": "OK", "removed": removed is not None, "subscribers": count}

    def broadcast(self, event: dict, exclude_client_id: str | None = None) -> None:
        with self._lock:
            subscribers = list(self._subscribers.values())
        for subscriber in subscribers:
            if subscriber.client_id == exclude_client_id:
                continue
            try:
                self._notify_subscriber(subscriber, event)
            except OSError:
                # Keep notifications best-effort for classroom use.
                continue

    @staticmethod
    def _notify_subscriber(subscriber: Subscriber, event: dict) -> None:
        with socket.create_connection((subscriber.host, subscriber.port), timeout=1.5) as sock:
            sock.sendall(json.dumps(event, ensure_ascii=False).encode("utf-8"))
            sock.sendall(b"\n")


HUB = NotificationHub()


def build_event(action: str, result: dict, origin_name: str | None) -> dict:
    event_name = {
        "c": "created",
        "u": "updated",
        "d": "deleted",
    }[action]
    return {
        "type": "notification",
        "event": event_name,
        "origin": origin_name or "client inconnu",
        "game": result,
    }


def dispatch_message(message: dict) -> tuple[dict | list[dict], int]:
    action = message.get("action")
    client_id = message.get("client_id")
    client_name = message.get("client_name")

    try:
        if action == "subscribe":
            notify_host = str(message.get("notify_host", "127.0.0.1"))
            notify_port = int(message["notify_port"])
            if not client_id:
                raise ValueError("client_id requis pour l'abonnement")
            if not client_name:
                raise ValueError("client_name requis pour l'abonnement")
            return HUB.subscribe(client_id, client_name, notify_host, notify_port), 200

        if action == "unsubscribe":
            if not client_id:
                raise ValueError("client_id requis pour le desabonnement")
            return HUB.unsubscribe(client_id), 200

        if action == "c":
            result = SERVICE.create_game(message)
            HUB.broadcast(build_event("c", result, client_name), exclude_client_id=client_id)
            return result, 200
        if action == "u":
            result = SERVICE.update_game(message)
            HUB.broadcast(build_event("u", result, client_name), exclude_client_id=client_id)
            return result, 200
        if action == "g":
            return SERVICE.get_game(message), 200
        if action == "l":
            return SERVICE.list_games(), 200
        if action == "d":
            result = SERVICE.delete_game(message)
            HUB.broadcast(build_event("d", result, client_name), exclude_client_id=client_id)
            return result, 200
        return {"error": f"Action inconnue: {action}"}, 400
    except ValueError as error:
        return {"error": str(error)}, 400
    except NotFoundError as error:
        return {"error": str(error)}, 404


class BibHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        pieces = [b""]
        total = 0
        while b"\n" not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2048))
            total += len(pieces[-1])
        data = b"".join(pieces).strip()
        if not data:
            self.request.sendall(json.dumps({"error": "Message vide"}).encode("utf-8"))
            return

        print(f"Received from {self.client_address[0]}: {data.decode('utf-8')}")
        try:
            message = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            response = {"error": "JSON invalide"}
        else:
            if "notify_host" not in message:
                message["notify_host"] = self.client_address[0]
            response, _ = dispatch_message(message)

        self.request.sendall(json.dumps(response, ensure_ascii=False).encode("utf-8"))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with ThreadedTCPServer((HOST, PORT), BibHandler) as server:
        print(f"Serveur TCP en ecoute sur {HOST}:{PORT}")
        server.serve_forever()
