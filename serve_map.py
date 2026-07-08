"""
Phase 2L · Map launcher.

Запускает HTTP сервер для archpelago map и автоматически открывает в браузере.
Решает проблему file:// security restrictions (Chrome блокирует некоторые JS операции
для local files).

Usage:
    python serve_map.py

Сервер будет работать пока не нажать Ctrl+C.
"""
from __future__ import annotations

import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

PORT = 8766  # отличается от dashboard порта
MAP_FILE = "results_phase2l/archplg_phase2l_map.html"


def main() -> int:
    here = Path(__file__).parent.resolve()
    map_path = here / MAP_FILE
    if not map_path.exists():
        print(f"ERROR: {MAP_FILE} not found in {here}")
        print(f"Сначала запусти: python generate_archipelago_map.py")
        return 2

    os.chdir(here)

    class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            super().end_headers()

        def log_message(self, fmt, *args):
            pass

    url = f"http://localhost:{PORT}/{MAP_FILE}"
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
            print(f"\n  Archipelago Map server")
            print(f"  URL: {url}")
            print(f"  Press Ctrl+C to stop.\n")
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        if "10048" in str(e) or "already in use" in str(e):
            print(f"\n  Port {PORT} занят. Открой в браузере: {url}")
            return 1
        raise
    except KeyboardInterrupt:
        print("\n  Server stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
