import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from bingo import BingoGame, validate_board


ROOT = Path(__file__).parent
game = None


class BingoHandler(BaseHTTPRequestHandler):
  def send_json(self, status, data):
    body = json.dumps(data).encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def do_GET(self):
    if urlparse(self.path).path == "/api/state":
      if game is None:
        self.send_json(200, {"game_started": False})
      else:
        self.send_json(200, game.state())
      return

    file_name = "index.html" if self.path == "/" else self.path.lstrip("/")
    file_path = (ROOT / file_name).resolve()
    if ROOT not in file_path.parents or not file_path.is_file():
      self.send_error(404)
      return
    content_type = {".html": "text/html", ".css": "text/css", ".js": "text/javascript"}.get(file_path.suffix, "application/octet-stream")
    body = file_path.read_bytes()
    self.send_response(200)
    self.send_header("Content-Type", content_type)
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def do_POST(self):
    global game
    length = int(self.headers.get("Content-Length", 0))
    try:
      data = json.loads(self.rfile.read(length))
      if self.path == "/api/start":
        board = [int(number) for number in data["board"]]
        validate_board(board)
        game = BingoGame(board)
        self.send_json(200, game.state())
      elif self.path == "/api/call" and game is not None:
        latest = game.call_number()
        self.send_json(200, game.state(latest))
      else:
        self.send_json(400, {"error": "Start a game first."})
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
      self.send_json(400, {"error": str(error)})


if __name__ == "__main__":
  print("Bingo is running at http://localhost:8000")
  ThreadingHTTPServer(("localhost", 8000), BingoHandler).serve_forever()