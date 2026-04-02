from pathlib import Path

from bib_core import JsonFileRepository, LibraryService, NotFoundError, format_game


DATA_FILE = Path(__file__).with_name("bib_data.json")


class ConsoleApp:
    def __init__(self) -> None:
        self.service = LibraryService(JsonFileRepository(DATA_FILE))
        self.should_continue = True

    def help(self) -> None:
        print("Actions disponibles :")
        print("  c : creer un jeu")
        print("  u : mettre a jour un jeu")
        print("  g : consulter un jeu")
        print("  l : lister tous les jeux")
        print("  d : supprimer un jeu")
        print("  h : afficher l'aide")
        print("  q : quitter")

    def create_game(self) -> None:
        payload = self._read_game_payload()
        print(format_game(self.service.create_game(payload)))

    def update_game(self) -> None:
        game_id = int(input("Id du jeu a modifier: "))
        payload = self._read_game_payload()
        payload["id"] = game_id
        print(format_game(self.service.update_game(payload)))

    def get_game(self) -> None:
        game_id = int(input("Id du jeu a consulter: "))
        print(format_game(self.service.get_game({"id": game_id})))

    def list_games(self) -> None:
        games = self.service.list_games()
        if not games:
            print("Aucun jeu enregistre.")
            return
        for game in games:
            print(format_game(game))

    def delete_game(self) -> None:
        game_id = int(input("Id du jeu a supprimer: "))
        result = self.service.delete_game({"id": game_id})
        print(f"Jeu {result['deleted_id']} supprime.")

    def quit(self) -> None:
        self.should_continue = False

    @staticmethod
    def _read_game_payload() -> dict:
        return {
            "title": input("Titre: ").strip(),
            "author": input("Auteur: ").strip(),
            "content": input("Contenu: ").strip(),
        }


if __name__ == "__main__":
    app = ConsoleApp()
    actions = {
        "h": app.help,
        "c": app.create_game,
        "u": app.update_game,
        "g": app.get_game,
        "l": app.list_games,
        "d": app.delete_game,
        "q": app.quit,
    }

    app.help()
    while app.should_continue:
        action = input("Action: ").strip().lower()
        handler = actions.get(action)
        if handler is None:
            print("Action inconnue. Tapez h pour l'aide.")
            continue
        try:
            handler()
        except ValueError as error:
            print(f"Erreur de saisie: {error}")
        except NotFoundError as error:
            print(error)
