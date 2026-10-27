"""
Lightweight Python Backend & Web Server for Demand-Supply Matching Prototype.
Serves static frontend (HTML/CSS/JS) and provides JSON API endpoints
connecting the UI to the actual Python DSA modules via api_service.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.api_service import dispatch_api_request

WEB_DIR = os.path.join(PROJECT_ROOT, "web")


class DSAApiHandler(SimpleHTTPRequestHandler):
    """Custom request handler serving static files and delegating /api requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path.startswith("/api/"):
            query_params = urllib.parse.parse_qs(parsed_path.query)
            status_code, data = dispatch_api_request(parsed_path.path, query_params)
            self._send_json(data, status=status_code)
        else:
            # Fallback to static file serving from WEB_DIR
            super().do_GET()

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_json(self, data: dict, status: int = 200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)


def run_server(host: str = "", port: int = 8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, DSAApiHandler)
    display_host = host if host else "localhost"
    print("=" * 80)
    print(f" Demand-Supply Matching Web Server Running at: http://{display_host}:{port}/")
    print(" Press Ctrl+C to stop the server.")
    print("=" * 80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    host = os.environ.get("HOST", "")
    port = int(os.environ.get("PORT", 8000))
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(host=host, port=port)
