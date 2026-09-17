import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# রেন্ডারের পোর্ট রিকোয়ারমেন্ট পূরণের জন্য সার্ভার
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aviator Bot Server is Live!")
    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
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
    uri = "wss://aviator.local2j111.link/?x-mesh-swimlane="
    # ব্রাউজারের আসল অরিজিন এবং ইউজার এজেন্ট হেডার্স যুক্ত করা হলো যাতে সার্ভার ব্লক না করে
    extra_headers = {
        "Origin": "https://game.wifun777.link",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
    }
    
    while True:
        try:
            print("Connecting to WebSocket with Headers...")
            async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
                print("Connected successfully!")
                async for message in websocket:
                    if isinstance(message, bytes):
                        try:
                            decoded_text = message.decode('utf-8', errors='ignore')
                            if decoded_text.strip():
                                print_live_signal(decoded_text.strip())
                        except:
                            pass
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ড থ্রেডে HTTP সার্ভার চালু রাখা
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # WebSocket লিসেনার রান করা
    asyncio.run(listen_game())
