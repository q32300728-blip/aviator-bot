import asyncio
import threading
import json
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler

# গেমের লাইভ ডাটা স্টোর করার গ্লোবাল ভেরিয়েবল
latest_game_data = {
    "status": "Connecting to 77kk Live Stream...",
    "binary_sample": "Waiting for packets..."
}

# ১. ব্যাকগ্রাউন্ড ওয়েবসকেট লিসেনার (ব্রাউজার হেডার সহ)
async def listen_to_game():
    uri = "wss://channel.local2j111.link/get"
    global latest_game_data
    
    # ব্রাউজারের মতো ছদ্মবেশ ধারণ করার জন্য হেডার সেটআপ
    extra_headers = {
        "Origin": "https://game.wlfun777.link",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }
    
    while True:
        try:
            async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
                latest_game_data["status"] = "Live Connected!"
                print("Connected to Live WebSocket!")
                async for message in websocket:
                    if isinstance(message, bytes):
                        hex_data = message.hex()
                        latest_game_data["binary_sample"] = f"Binary Packet: {hex_data[:30]}..."
                        print("Received Binary:", hex_data)
                    else:
                        data = json.loads(message)
                        latest_game_data["binary_sample"] = f"JSON Data: {str(data)[:40]}..."
                        print("Received JSON:", data)
        except Exception as e:
            latest_game_data["status"] = f"Reconnecting... ({e})"
            print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

def run_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_to_game())

# ২. ড্যাশবোর্ড ইউজার ইন্টারফেস ও সার্ভার হ্যান্ডলার
class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Aviator Live Bot - 77kk</title>
            <style>
                body {{ background: #0f172a; color: #f8fafc; font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                .card {{ background: #1e293b; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
                .status {{ color: #22c55e; font-weight: bold; font-size: 18px; }}
                .data-box {{ background: #0f172a; padding: 15px; margin-top: 20px; border-radius: 8px; font-family: monospace; color: #38bdf8; word-break: break-all; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>AVIATOR LIVE BOT</h1>
                <p>Target: 77kk Stream</p>
                <div class="status">Status: {latest_game_data['status']}</div>
                <div class="data-box">{latest_game_data['binary_sample']}</div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode("utf-8"))

def run_http_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, DashboardHandler)
    print("HTTP Server running on port 8080...")
    httpd.serve_forever()

# ৩. মেইন প্রসেস
if __name__ == "__main__":
    ws_thread = threading.Thread(target=run_asyncio_loop, daemon=True)
    ws_thread.start()
    run_http_server()
