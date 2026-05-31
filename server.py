#!/usr/bin/env python3
"""
Simple HTTP server for the Raindrop Random Bookmark UI.
Serves index.html and a /api/random endpoint.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from random_bookmark import RaindropRandomizer, get_api_token


class Handler(BaseHTTPRequestHandler):
    randomizer: RaindropRandomizer = None

    def log_message(self, format, *args):
        pass  # suppress default access log noise

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/random":
            self._handle_api(parse_qs(parsed.query))
        elif parsed.path in ("/", "/index.html"):
            self._serve_file("index.html", "text/html")
        else:
            self.send_error(404)

    def _handle_api(self, qs):
        try:
            count = max(1, min(20, int(qs.get("count", ["1"])[0])))
        except ValueError:
            count = 1

        results = []
        for _ in range(count):
            bookmark = self.randomizer.get_random_bookmark()
            if bookmark:
                results.append({
                    "title": bookmark.get("title", "Untitled"),
                    "link": bookmark.get("link", ""),
                    "excerpt": bookmark.get("excerpt", ""),
                    "tags": bookmark.get("tags", []),
                    "created": bookmark.get("created", "")[:10],
                    "cover": bookmark.get("cover", ""),
                })

        body = json.dumps(results).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, filename, content_type):
        path = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(path, "rb") as f:
                body = f.read()
        except FileNotFoundError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


def main():
    token = get_api_token()
    if not token:
        print("No API token. Exiting.")
        sys.exit(1)

    Handler.randomizer = RaindropRandomizer(token)

    port = int(os.getenv("PORT", 8787))
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Raindrop UI running at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
