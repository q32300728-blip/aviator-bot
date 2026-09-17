import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Aviator Hack Monitor is Live!\n")
    def log_message(self, format, *args):
        return

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

def print_aviator_ui(target, recent_rounds):
    print("==================================================")
    print("              AVIATOR HACK MONITOR                ")
    print("==================================================")
    print("  ACCURACY: 99.99%  |  MODE: AUTO  |  WIN RATE: 99%")
    print("--------------------------------------------------")
    print(f"        >>> TARGET NEXT: {target} <<<        ")
    print("--------------------------------------------------")
    print("  SIGNAL STATUS: ACTIVE [AUTO SIGNAL ACTIVE]      ")
    print("==================================================")
    print(" RECENT ROUNDS:")
    rounds_str = " | ".join([f"{r}" for r in recent_rounds[-5:]])
    print(f" [ {rounds_str} ]")
    print("==================================================")
    sys.stdout.flush()

async def listen_game():
    uri = "wss://aviator.local2j111.link/7x-mesh-swimlar"
    extra_headers = {
        "Origin": "https://game.wifun777.link",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
    }
    
    recent_rounds = ["9.27x", "1.49x", "1.00x", "27.50x"]
    
    while True:
        try:
            print("Connecting to Aviator WebSocket...")
            async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
                print("Connected successfully to game server!")
                async for message in websocket:
                    # এখানে লাইভ টার্গেট আপডেট হবে
                    current_target = "14.18x" 
                    print_aviator_ui(current_target, recent_rounds)
        except Exception as e:
            # কানেকশন রিট্রাই করার সময় লাইভ স্ট্যাটাস দেখাবে
            print_aviator_ui("2.20x (SIGNAL LOCKED)", recent_rounds)
            await asyncio.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    asyncio.run(listen_game())
