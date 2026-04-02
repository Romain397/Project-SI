import json
import socketserver
from pathlib import Path

from bib_core import LibraryService, NotFoundError, SqliteRepository


DATABASE_PATH = Path(__file__).with_name("bib.sqlite3")
SERVICE = LibraryService(SqliteRepository(DATABASE_PATH))


def dispatch_message(message: dict) -> tuple[dict | list[dict], int]:
    action = message.get("action")
    try:
        if action == "c":
            return SERVICE.create_game(message), 200
        if action == "u":
            return SERVICE.update_game(message), 200
        if action == "g":
            return SERVICE.get_game(message), 200
        if action == "l":
            return SERVICE.list_games(), 200
        if action == "d":
            return SERVICE.delete_game(message), 200
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

        print(f"Tier 2 received from {self.client_address[0]}: {data.decode('utf-8')}")
        try:
            message = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            response = {"error": "JSON invalide"}
        else:
            response, _ = dispatch_message(message)
        self.request.sendall(json.dumps(response, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    with socketserver.TCPServer((HOST, PORT), BibHandler) as server:
        print(f"Serveur tier 2 TCP/SQLite en ecoute sur {HOST}:{PORT}")
        server.serve_forever()
