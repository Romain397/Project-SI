import json
import socket

from bib_core import format_game


HOST, PORT = "localhost", 9999


def send_message(payload: dict) -> dict | list[dict]:
    data = json.dumps(payload)
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


if __name__ == "__main__":
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
    while ci.should_continue:
        input_action = input("Action: ").strip().lower()
        handler = actions.get(input_action)
        if handler is None:
            print("Action inconnue.")
            continue
        message = handler()
        if message is not None:
            print_result(send_message(message))
