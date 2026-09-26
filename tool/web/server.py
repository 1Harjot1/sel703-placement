"""
tool/web/server.py
==================
Lightweight zero-dependency local web server for the Cognitive-Access Inspector Demo.
Uses Python's standard library http.server.
Endpoints:
  GET /             -> Serves tool/web/index.html
  POST /api/inspect -> Executes TestRunner against submitted transcript JSON
Usage:
  python -m tool.web.server [--port 8080]
"""

import http.server
import socketserver
import json
import os
import sys
import webbrowser
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from tool.runner import TestRunner

PORT = 8000
if "--port" in sys.argv:
    p_idx = sys.argv.index("--port")
    if p_idx + 1 < len(sys.argv):
        PORT = int(sys.argv[p_idx + 1])

runner = TestRunner(mode="all")

class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html_path = os.path.join(BASE_DIR, "index.html")
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/inspect":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            
            try:
                data = json.loads(post_data)
                transcript = data.get("transcript", "")
                
                # Write to temp file for runner
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as tf:
                    tf.write(transcript)
                    tmp_name = tf.name

                try:
                    report = runner.run_tests(tmp_name)
                finally:
                    if os.path.exists(tmp_name):
                        os.remove(tmp_name)

                response_bytes = json.dumps(report, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)

            except Exception as e:
                err_resp = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_resp)))
                self.end_headers()
                self.wfile.write(err_resp)
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=PORT):
    server = socketserver.TCPServer(("", port), DemoHandler)
    url = f"http://localhost:{port}"
    print("=" * 80)
    print("[SERVER] COGNITIVE-ACCESS INSPECTOR -- LIVE DEMO SERVER")
    print("=" * 80)
    print(f"Local Server URL:   {url}")
    print("Engine Mode:        Hybrid (Deterministic AST/Regex + Gemini Fallback)")
    print("Press Ctrl+C to stop the server.")
    print("=" * 80)
    
    # Open browser automatically
    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping demo server...")
        server.shutdown()

if __name__ == "__main__":
    run_server()
