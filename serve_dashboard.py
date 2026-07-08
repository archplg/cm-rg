"""
Phase 2L · Dashboard launcher.

Starts a tiny HTTP server in the archipelago_cross_model directory and
opens the monitor dashboard in your default browser.

Why this exists: when you open monitor_dashboard.html by double-clicking,
the browser uses file:// protocol which blocks fetch() to local files.
This launcher serves files over http://localhost so fetch works.

Cost: $0. Just a local server.
Usage: python serve_dashboard.py
       Then leave this window open while watching the dashboard.
       Press Ctrl+C to stop.
"""
from __future__ import annotations

import http.server
import socketserver
import webbrowser
import sys
from pathlib import Path


PORT = 8765  # uncommon port - avoid conflicts
DASHBOARD = "monitor_dashboard.html"


def main() -> int:
    # Ensure we're in the right directory
    here = Path(__file__).parent.resolve()
    dashboard_path = here / DASHBOARD
    if not dashboard_path.exists():
        print(f"ERROR: {DASHBOARD} not found in {here}")
        return 2

    # Change to archipelago_cross_model directory so server serves from here
    import os
    os.chdir(here)

    # Disable cache so browser always sees fresh state.json
    class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()

        def log_message(self, format, *args):
            # Quiet - don't spam every request
            pass

    url = f"http://localhost:{PORT}/{DASHBOARD}"

    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
            print(f"\n  Phase 2L Dashboard server\n")
            print(f"  Serving: {here}")
            print(f"  Open in browser: {url}")
            print(f"\n  Opening browser now...")
            print(f"  Press Ctrl+C to stop server.\n")
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        if "10048" in str(e) or "already in use" in str(e):
            print(f"\n  Port {PORT} already in use. Maybe server is already running.")
            print(f"  Just open this URL in your browser: {url}")
            return 1
        raise
    except KeyboardInterrupt:
        print("\n  Server stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
