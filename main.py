import asyncio
import json
import logging
import threading
from flask import Flask, jsonify, render_template

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
        logging.info(f"[Binary/Ping Detected] State: {self.state} | Multiplier: {self.multiplier}x")

cache = GameStateCache()

async def crash_bot_listener():
    from websockets.client import connect
    from websockets.exceptions import ConnectionClosed
    
    while True:
        try:
            logging.info(f"[WebSocket] Connecting with Ping-Pong enabled...")
            # ping_interval এবং ping_timeout সার্ভারের সাথে কানেকশন লাইভ রাখতে কাজ করবে
            async with connect(WS_URL, ping_interval=10, ping_timeout=5) as websocket:
                logging.info("[WebSocket] Connected successfully.")
                
                async for message in websocket:
                    # বাইনারি ডেটা হলে সেটি ডিকোড বা হ্যান্ডেল করা
                    if isinstance(message, bytes):
                        try:
                            # প্রথমে UTF-8 টেক্সট হিসেবে ডিকোড করার চেষ্টা
                            decoded_message = message.decode('utf-8', errors='ignore')
                        except Exception:
                            decoded_message = message.hex() # বাইনারি হেক্স ফরম্যাট
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
                        # বাইনারি বা পং ফ্রেমের ক্ষেত্রে এখানে কন্ডিশন দেওয়া যেতে পারে
                        pass

        except ConnectionClosed as cc:
            logging.warning(f"[WebSocket] Connection closed: {cc}. Reconnecting...")
            await asyncio.sleep(2)
        except Exception as ex:
            logging.error(f"[WebSocket] Error: {ex}. Retrying...")
            await asyncio.sleep(3)

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

def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    try:
        asyncio.run(crash_bot_listener())
    except KeyboardInterrupt:
        logging.info("[Bot] Stopped.")
