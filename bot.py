import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ডামি HTTP সার্ভার যাতে রেন্ডার পোর্ট বাইন্ড নিয়ে কোনো এরর না দেয়
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aviator Bot is Running!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

def print_live_signal(target_multiplier):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("====================================")
    print("      AVIATOR LIVE MONITOR          ")
    print("====================================")
    print(f"\n   TARGET NEXT: {target_multiplier}\n")
    print("====================================")
    sys.stdout.flush()

async def listen_game():
    uri = "wss://channel.local2j111.link/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Live WebSocket...")
                async for message in websocket:
                    if isinstance(message, bytes):
                        try:
                            decoded_text = message.decode('utf-8', errors='ignore')
                            if decoded_text.strip():
                                print_live_signal(decoded_text.strip())
                        except:
                            pass
        except Exception as e:
            print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    # HTTP সার্ভার আলাদা একটি থ্রেডে রান করানো হলো
    t = threading.Thread(target=run_http_server, daemon=True)
    t.start()
    
    # WebSocket লিসেনার রান করানো হলো
    asyncio.run(listen_game())
