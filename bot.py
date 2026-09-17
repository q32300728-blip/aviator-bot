import os
import sys
import asyncio
import websockets
from aiohttp import web

# ১. রেন্ডারের পোর্ট রিকোয়ারমেন্ট পূরণের জন্য aiohttp ভিত্তিক এথিক্যাল ওয়েব হ্যান্ডলার
async def handle_ping(request):
    return web.Response(text="Aviator Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # রেন্ডার কর্তৃক প্রদত্ত পোর্ট ধরে রাখা
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"HTTP Server started on port {port}")

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
    extra_headers = {
        "Origin": "https://game.wifun777.link",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
    }
    
    while True:
        try:
            print("Connecting to WebSocket...")
            async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
                print("Connected successfully to game WebSocket!")
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

async def main():
    # একসাথে ওয়েব সার্ভার এবং গেম লিসেনার দুটিই অ্যাসিনক্রোনাসভাবে রান করা
    await start_web_server()
    await listen_game()

if __name__ == "__main__":
    asyncio.run(main())
