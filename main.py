import asyncio
import json
import logging
import threading
from flask import Flask, jsonify, render_template

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

WS_URL = "wss://channel.local2j111.link/"

class GameStateCache:
    def __init__(self):
        self.state = "WAITING"
        self.multiplier = 1.00
        self.history = []

    def update_state(self, new_state, multiplier=1.00):
        self.state = new_state
        self.multiplier = multiplier
        if new_state == "CRASHED":
            self.history.append(multiplier)
        logging.info(f"[Updated] State: {self.state} | Multiplier: {self.multiplier}x")

cache = GameStateCache()

async def crash_bot_listener():
    from websockets.client import connect
    from websockets.exceptions import ConnectionClosed
    
    while True:
        try:
            logging.info(f"[WebSocket] Connecting to target server...")
            async with connect(WS_URL, ping_interval=10, ping_timeout=5) as websocket:
                logging.info("[WebSocket] Connected successfully.")
                
                # সার্ভারে সাবস্ক্রিপশন বা ইউজার আইডি পাঠানো
                init_payload = json.dumps({"id": "63204229452", "type": "subscribe"})
                await websocket.send(init_payload)
                logging.info("[WebSocket] Sent initial payload.")
                
                async for message in websocket:
                    if isinstance(message, bytes):
                        try:
                            decoded_message = message.decode('utf-8', errors='ignore')
                        except Exception:
                            decoded_message = message.hex()
                    else:
                        decoded_message = message

                    logging.info(f"[Raw Stream]: {decoded_message}")
                    
                    try:
                        data = json.loads(decoded_message)
                        if isinstance(data, dict):
                            mult = data.get("multiplier") or data.get("f") or 1.00
                            status = data.get("status") or "RUNNING"
                            cache.update_state(status, float(mult))
                    except json.JSONDecodeError:
                        pass

        except ConnectionClosed as cc:
            logging.warning(f"[WebSocket] Connection closed: {cc}. Reconnecting...")
            await asyncio.sleep(2)
        except Exception as ex:
            logging.error(f"[WebSocket] Error: {ex}. Retrying...")
            await asyncio.sleep(3)

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(crash_bot_listener())

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-live-data")
def get_live_data():
    return jsonify({
        "status": cache.state,
        "multiplier": f"{cache.multiplier:.2f}x",
        "history": cache.history[-5:]
    })

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে অ্যাসিনক্রোনাস ওয়েবসকেট লুপ চালু করার জন্য আলাদা ইভেন্ট লুপ থ্রেড
    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_background_loop, args=(new_loop,), daemon=True)
    t.start()

    # মূল থ্রেডে ফ্লস্ক সার্ভার রান করা যাতে রেন্ডার অ্যাপ বন্ধ না হয়ে যায়
    app.run(host="0.0.0.0", port=8080)
