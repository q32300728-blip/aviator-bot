import os
import sys
import asyncio
import websockets

def print_live_signal(target_multiplier):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("====================================")
    print("      AVIATOR LIVE MONITOR          ")
    print("====================================")
    print(f"\n   TARGET NEXT: {target_multiplier}\n")
    print("====================================")
    sys.stdout.flush()

async def listen_game():
    uri = "wss://your-websocket-url-here"
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

if __name__ == "__main__":
    asyncio.run(listen_game())
