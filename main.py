import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
RENDER_URL = os.environ.get("RENDER_URL")
SECRET = os.environ.get("SECRET", "00000000000000000000000000000000")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Proxy and Keep-Alive are running!")

def run_http_server():
    httpd = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f"HTTP Server listening on port {PORT}")
    httpd.serve_forever()

def keep_alive_pinger():
    if not RENDER_URL:
        print("RENDER_URL environment variable is not set. Pinger disabled.")
        return
    
    while True:
        try:
            time.sleep(600) 
            response = requests.get(RENDER_URL)
            print(f"Pinged self: {response.status_code}")
        except Exception as e:
            print(f"Ping failed: {e}")

def run_proxy():
    proxy_port = 443 
    print(f"Starting MTProto proxy on port {proxy_port}")
    os.system(f"python -m mtprotoproxy -p {proxy_port} -s {SECRET}")

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    
    threading.Thread(target=keep_alive_pinger, daemon=True).start()
    
    run_proxy()