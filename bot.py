import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# রেন্ডারের দেওয়া পোর্ট সঠিকভাবে ক্যাচ করে HTTP সার্ভার চালু রাখা
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active")
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
    uri = "wss://channel.local2j111.link/"
    while True:
        try:
            print("Attempting to connect to WebSocket...")
            async with websockets.connect(uri) as websocket:
                print("Connected to Live WebSocket successfully!")
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
    # HTTP সার্ভার ব্যাকগ্রাউন্ড থ্রেডে চালু করা হলো যাতে রেন্ডারের পোর্ট টাইমআউট না হয়
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # মূল অ্যাসিনক্রোনাস লুপ রান করা
    asyncio.run(listen_game())
