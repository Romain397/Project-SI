import json
import os
import socket
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from bib_core import InMemoryRepository, LibraryService, NotFoundError


HOST = os.getenv("BIB_HTTP_HOST", "127.0.0.1")
PORT = int(os.getenv("BIB_HTTP_PORT", "8000"))
BACKEND_MODE = os.getenv("BIB_HTTP_BACKEND", "memory").lower()
TCP_BACKEND_HOST = os.getenv("BIB_TCP_BACKEND_HOST", "127.0.0.1")
TCP_BACKEND_PORT = int(os.getenv("BIB_TCP_BACKEND_PORT", "9998"))
SERVICE = LibraryService(InMemoryRepository())


def call_tcp_backend(message: dict) -> tuple[dict | list[dict], int]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((TCP_BACKEND_HOST, TCP_BACKEND_PORT))
        sock.sendall(json.dumps(message).encode("utf-8"))
        sock.sendall(b"\n")
        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    payload = json.loads(b"".join(chunks).decode("utf-8"))
    status = 200 if "error" not in payload else 400
    if isinstance(payload, dict) and "introuvable" in payload.get("error", "").lower():
        status = 404
    return payload, status


def dispatch_locally(action: str, payload: dict | None) -> tuple[dict | list[dict], int]:
    message = payload or {}
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


def dispatch(action: str, payload: dict | None) -> tuple[dict | list[dict], int]:
    message = dict(payload or {})
    message["action"] = action
    if BACKEND_MODE == "tcp":
        return call_tcp_backend(message)
    return dispatch_locally(action, message)


class BibHttpHandler(BaseHTTPRequestHandler):
    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw_body = self.rfile.read(length)
        if not raw_body:
            return {}
        return json.loads(raw_body.decode("utf-8"))

    def _send_json(self, payload: dict | list[dict], status: int) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _extract_id(path: str) -> int | None:
        normalized = path.strip("/")
        if normalized == "games":
            return None
        prefix = "games/"
        if normalized.startswith(prefix):
            return int(normalized[len(prefix):])
        raise ValueError("Route inconnue")

    def do_GET(self) -> None:
        try:
            game_id = self._extract_id(self.path)
            if game_id is None:
                payload, status = dispatch("l", {})
            else:
                payload, status = dispatch("g", {"id": game_id})
        except ValueError as error:
            payload, status = {"error": str(error)}, HTTPStatus.BAD_REQUEST
        self._send_json(payload, int(status))

    def do_POST(self) -> None:
        try:
            if self.path.rstrip("/") != "/games":
                raise ValueError("Route inconnue")
            payload, status = dispatch("c", self._read_json_body())
        except json.JSONDecodeError:
            payload, status = {"error": "JSON invalide"}, HTTPStatus.BAD_REQUEST
        except ValueError as error:
            payload, status = {"error": str(error)}, HTTPStatus.BAD_REQUEST
        self._send_json(payload, int(status))

    def do_PUT(self) -> None:
        try:
            game_id = self._extract_id(self.path)
            if game_id is None:
                raise ValueError("Un identifiant est requis")
            body = self._read_json_body()
            body["id"] = game_id
            payload, status = dispatch("u", body)
        except json.JSONDecodeError:
            payload, status = {"error": "JSON invalide"}, HTTPStatus.BAD_REQUEST
        except ValueError as error:
            payload, status = {"error": str(error)}, HTTPStatus.BAD_REQUEST
        self._send_json(payload, int(status))

    def do_DELETE(self) -> None:
        try:
            game_id = self._extract_id(self.path)
            if game_id is None:
                raise ValueError("Un identifiant est requis")
            payload, status = dispatch("d", {"id": game_id})
        except ValueError as error:
            payload, status = {"error": str(error)}, HTTPStatus.BAD_REQUEST
        self._send_json(payload, int(status))

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def run(server_class=HTTPServer, handler_class=BibHttpHandler) -> None:
    httpd = server_class((HOST, PORT), handler_class)
    print(f"Serveur HTTP en ecoute sur http://{HOST}:{PORT} (backend={BACKEND_MODE})")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
