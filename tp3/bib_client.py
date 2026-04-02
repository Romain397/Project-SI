import json
import os
import socket
import socketserver
import threading
import uuid

from bib_core import format_game


HOST, PORT = "localhost", 9999
CLIENT_NAME = os.getenv("BIB_CLIENT_NAME", f"client-{uuid.uuid4().hex[:6]}")
CLIENT_NOTIFY_HOST = os.getenv("BIB_CLIENT_HOST", "127.0.0.1")
CLIENT_NOTIFY_PORT = int(os.getenv("BIB_CLIENT_PORT", "10001"))
CLIENT_ID = f"{CLIENT_NAME}@{CLIENT_NOTIFY_HOST}:{CLIENT_NOTIFY_PORT}"


def send_message(payload: dict) -> dict | list[dict]:
    enriched_payload = dict(payload)
    enriched_payload.setdefault("client_id", CLIENT_ID)
    enriched_payload.setdefault("client_name", CLIENT_NAME)
    data = json.dumps(enriched_payload)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(data.encode("utf-8"))
        sock.sendall(b"\n")

        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

    response_text = b"".join(chunks).decode("utf-8")
    print("Sent:    ", data)
    print("Received:", response_text)
    return json.loads(response_text)


class NotificationHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        pieces = [b""]
        total = 0
        while b"\n" not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2048))
            total += len(pieces[-1])
        data = b"".join(pieces).strip()
        if not data:
            return
        try:
            notification = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("\n[notification] message invalide recu")
            return

        if notification.get("type") != "notification":
            print(f"\n[notification] {notification}")
            return

        print("\n=== Notification ===")
        print(f"Evenement : {notification.get('event')}")
        print(f"Origine   : {notification.get('origin')}")
        game = notification.get("game")
        if isinstance(game, dict):
            print(format_game(game))
        print("====================")


class ThreadedNotificationServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


class ClientNotificationServer:
    def __init__(self, host: str, port: int) -> None:
        self.server = ThreadedNotificationServer((host, port), NotificationHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self) -> None:
        self.thread.start()
        print(f"Serveur local de notifications en ecoute sur {CLIENT_NOTIFY_HOST}:{CLIENT_NOTIFY_PORT}")

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


class ConsoleInput:
    def __init__(self) -> None:
        self.should_continue = True

    def help(self) -> None:
        print("Actions disponibles : c u g l d h q")

    def create_game(self) -> dict:
        return {
            "action": "c",
            "title": input("Titre: ").strip(),
            "author": input("Auteur: ").strip(),
            "content": input("Contenu: ").strip(),
        }

    def update_game(self) -> dict:
        return {
            "action": "u",
            "id": int(input("Id du jeu a modifier: ")),
            "title": input("Titre: ").strip(),
            "author": input("Auteur: ").strip(),
            "content": input("Contenu: ").strip(),
        }

    def get_game(self) -> dict:
        return {
            "action": "g",
            "id": int(input("Id du jeu a consulter: ")),
        }

    def delete_game(self) -> dict:
        return {
            "action": "d",
            "id": int(input("Id du jeu a supprimer: ")),
        }

    @staticmethod
    def list_games() -> dict:
        return {"action": "l"}

    def quit(self) -> None:
        self.should_continue = False
        return None


def print_result(result: dict | list[dict]) -> None:
    if isinstance(result, list):
        if not result:
            print("Aucun jeu enregistre.")
            return
        for game in result:
            print(format_game(game))
        return
    if {"id", "title", "author", "content"}.issubset(result):
        print(format_game(result))
        return
    print(result)


def subscribe() -> None:
    result = send_message(
        {
            "action": "subscribe",
            "notify_host": CLIENT_NOTIFY_HOST,
            "notify_port": CLIENT_NOTIFY_PORT,
        }
    )
    print(f"Abonnement aux notifications actif pour {CLIENT_ID}: {result}")


def unsubscribe() -> None:
    result = send_message({"action": "unsubscribe"})
    print(f"Desabonnement effectue pour {CLIENT_ID}: {result}")


if __name__ == "__main__":
    notification_server = ClientNotificationServer(CLIENT_NOTIFY_HOST, CLIENT_NOTIFY_PORT)
    notification_server.start()

    try:
        subscribe()
    except OSError as error:
        notification_server.stop()
        raise SystemExit(f"Impossible de s'abonner au serveur principal: {error}") from error

    ci = ConsoleInput()
    actions = {
        "h": ci.help,
        "c": ci.create_game,
        "u": ci.update_game,
        "g": ci.get_game,
        "d": ci.delete_game,
        "l": ci.list_games,
        "q": ci.quit,
    }
    ci.help()
    try:
        while ci.should_continue:
            input_action = input("Action: ").strip().lower()
            handler = actions.get(input_action)
            if handler is None:
                print("Action inconnue.")
                continue
            message = handler()
            if message is not None:
                print_result(send_message(message))
    finally:
        try:
            unsubscribe()
        except OSError:
            pass
        notification_server.stop()
