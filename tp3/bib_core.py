from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class BoardGame:
    id: int
    title: str
    author: str
    content: str

    def to_dict(self) -> dict:
        return asdict(self)


class NotFoundError(Exception):
    pass


class BaseRepository:
    def create(self, title: str, author: str, content: str) -> BoardGame:
        raise NotImplementedError

    def update(self, game_id: int, title: str, author: str, content: str) -> BoardGame:
        raise NotImplementedError

    def get(self, game_id: int) -> BoardGame:
        raise NotImplementedError

    def list(self) -> list[BoardGame]:
        raise NotImplementedError

    def delete(self, game_id: int) -> bool:
        raise NotImplementedError


class InMemoryRepository(BaseRepository):
    def __init__(self) -> None:
        self._games: dict[int, BoardGame] = {}
        self._next_id = 1

    def create(self, title: str, author: str, content: str) -> BoardGame:
        game = BoardGame(id=self._next_id, title=title, author=author, content=content)
        self._games[game.id] = game
        self._next_id += 1
        return game

    def update(self, game_id: int, title: str, author: str, content: str) -> BoardGame:
        game = self.get(game_id)
        game.title = title
        game.author = author
        game.content = content
        return game

    def get(self, game_id: int) -> BoardGame:
        game = self._games.get(game_id)
        if game is None:
            raise NotFoundError(f"Jeu {game_id} introuvable")
        return game

    def list(self) -> list[BoardGame]:
        return [self._games[key] for key in sorted(self._games)]

    def delete(self, game_id: int) -> bool:
        if game_id not in self._games:
            raise NotFoundError(f"Jeu {game_id} introuvable")
        del self._games[game_id]
        return True


class JsonFileRepository(BaseRepository):
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._save({"next_id": 1, "games": []})

    def _load(self) -> dict:
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save(self, payload: dict) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    def _game_from_dict(self, payload: dict) -> BoardGame:
        return BoardGame(**payload)

    def create(self, title: str, author: str, content: str) -> BoardGame:
        payload = self._load()
        game = BoardGame(id=payload["next_id"], title=title, author=author, content=content)
        payload["games"].append(game.to_dict())
        payload["next_id"] += 1
        self._save(payload)
        return game

    def update(self, game_id: int, title: str, author: str, content: str) -> BoardGame:
        payload = self._load()
        for item in payload["games"]:
            if item["id"] == game_id:
                item["title"] = title
                item["author"] = author
                item["content"] = content
                self._save(payload)
                return self._game_from_dict(item)
        raise NotFoundError(f"Jeu {game_id} introuvable")

    def get(self, game_id: int) -> BoardGame:
        payload = self._load()
        for item in payload["games"]:
            if item["id"] == game_id:
                return self._game_from_dict(item)
        raise NotFoundError(f"Jeu {game_id} introuvable")

    def list(self) -> list[BoardGame]:
        payload = self._load()
        return [self._game_from_dict(item) for item in payload["games"]]

    def delete(self, game_id: int) -> bool:
        payload = self._load()
        remaining_games = [item for item in payload["games"] if item["id"] != game_id]
        if len(remaining_games) == len(payload["games"]):
            raise NotFoundError(f"Jeu {game_id} introuvable")
        payload["games"] = remaining_games
        self._save(payload)
        return True


class SqliteRepository(BaseRepository):
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS board_games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )

    def _row_to_game(self, row: sqlite3.Row | None) -> BoardGame:
        if row is None:
            raise NotFoundError("Jeu introuvable")
        return BoardGame(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            content=row["content"],
        )

    def create(self, title: str, author: str, content: str) -> BoardGame:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO board_games(title, author, content) VALUES (?, ?, ?)",
                (title, author, content),
            )
            game_id = int(cursor.lastrowid)
        return self.get(game_id)

    def update(self, game_id: int, title: str, author: str, content: str) -> BoardGame:
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE board_games SET title = ?, author = ?, content = ? WHERE id = ?",
                (title, author, content, game_id),
            )
            if cursor.rowcount == 0:
                raise NotFoundError(f"Jeu {game_id} introuvable")
        return self.get(game_id)

    def get(self, game_id: int) -> BoardGame:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, title, author, content FROM board_games WHERE id = ?",
                (game_id,),
            ).fetchone()
        if row is None:
            raise NotFoundError(f"Jeu {game_id} introuvable")
        return self._row_to_game(row)

    def list(self) -> list[BoardGame]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT id, title, author, content FROM board_games ORDER BY id"
            ).fetchall()
        return [self._row_to_game(row) for row in rows]

    def delete(self, game_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM board_games WHERE id = ?", (game_id,))
            if cursor.rowcount == 0:
                raise NotFoundError(f"Jeu {game_id} introuvable")
        return True


class LibraryService:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    def create_game(self, payload: dict) -> dict:
        self._validate_game_payload(payload)
        game = self.repository.create(
            title=payload["title"].strip(),
            author=payload["author"].strip(),
            content=payload["content"].strip(),
        )
        return game.to_dict()

    def update_game(self, payload: dict) -> dict:
        game_id = self._extract_id(payload)
        self._validate_game_payload(payload)
        game = self.repository.update(
            game_id=game_id,
            title=payload["title"].strip(),
            author=payload["author"].strip(),
            content=payload["content"].strip(),
        )
        return game.to_dict()

    def get_game(self, payload: dict) -> dict:
        game_id = self._extract_id(payload)
        return self.repository.get(game_id).to_dict()

    def list_games(self) -> list[dict]:
        return [game.to_dict() for game in self.repository.list()]

    def delete_game(self, payload: dict) -> dict:
        game_id = self._extract_id(payload)
        self.repository.delete(game_id)
        return {"status": "OK", "deleted_id": game_id}

    @staticmethod
    def _extract_id(payload: dict) -> int:
        raw_id = payload.get("id")
        if raw_id is None:
            raw_id = payload.get("game_id")
        if raw_id is None:
            raw_id = payload.get("id_to_delete")
        if raw_id is None:
            raise ValueError("Un identifiant est requis")
        return int(raw_id)

    @staticmethod
    def _validate_game_payload(payload: dict) -> None:
        missing = [field for field in ("title", "author", "content") if not str(payload.get(field, "")).strip()]
        if missing:
            raise ValueError(f"Champs requis manquants: {', '.join(missing)}")


def format_game(game: dict) -> str:
    return (
        f"[{game['id']}] {game['title']}\n"
        f"  Auteur : {game['author']}\n"
        f"  Contenu: {game['content']}"
    )
