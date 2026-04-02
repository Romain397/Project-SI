import json

import requests

from bib_core import format_game


HOST, PORT = "localhost", 8000
BASE_URL = f"http://{HOST}:{PORT}"


def send_request(method: str, path: str = "/games", payload: dict | None = None) -> dict | list[dict]:
    response = requests.request(method=method, url=f"{BASE_URL}{path}", json=payload, timeout=5)
    print("Sent:    ", payload)
    print("Received:", response.text)
    response.raise_for_status()
    return response.json()


class ConsoleInput:
    def __init__(self) -> None:
        self.should_continue = True

    def help(self) -> None:
        print("Actions disponibles : c u g l d h q")

    def create_game(self) -> tuple[str, str, dict]:
        return "POST", "/games", self._read_game_payload()

    def update_game(self) -> tuple[str, str, dict]:
        game_id = int(input("Id du jeu a modifier: "))
        return "PUT", f"/games/{game_id}", self._read_game_payload()

    def get_game(self) -> tuple[str, str, None]:
        game_id = int(input("Id du jeu a consulter: "))
        return "GET", f"/games/{game_id}", None

    def delete_game(self) -> tuple[str, str, None]:
        game_id = int(input("Id du jeu a supprimer: "))
        return "DELETE", f"/games/{game_id}", None

    @staticmethod
    def list_games() -> tuple[str, str, None]:
        return "GET", "/games", None

    def quit(self) -> tuple[None, None, None]:
        self.should_continue = False
        return None, None, None

    @staticmethod
    def _read_game_payload() -> dict:
        return {
            "title": input("Titre: ").strip(),
            "author": input("Auteur: ").strip(),
            "content": input("Contenu: ").strip(),
        }


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
        "l": ci.list_games,
        "d": ci.delete_game,
        "q": ci.quit,
    }
    ci.help()
    while ci.should_continue:
        input_action = input("Action: ").strip().lower()
        handler = actions.get(input_action)
        if handler is None:
            print("Action inconnue.")
            continue
        method, path, payload = handler()
        if method is None:
            continue
        try:
            print_result(send_request(method, path, payload))
        except requests.HTTPError as error:
            print(f"Erreur HTTP: {error.response.status_code} - {error.response.text}")
        except requests.RequestException as error:
            print(f"Erreur reseau: {error}")
        except json.JSONDecodeError:
            print("La reponse du serveur n'est pas un JSON valide.")
