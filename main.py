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
            async with connect(WS_URL, ping_interval=20, ping_timeout=10) as websocket:
                logging.info("[WebSocket] Connected successfully.")
                
                async for message in websocket:
                    # সার্ভার থেকে যা আসছে তা কনসোলে প্রিন্ট করে দেখা
                    logging.info(f"[Raw Data Received]: {message}")
                    
                    try:
                        data = json.loads(message)
                        # সার্ভারের ডেটা স্ট্রাকচার অনুযায়ী এখানে কী বা ফিল্টার বসবে তা নির্ধারণ করা হবে
                        if isinstance(data, dict):
                            # উদাহরণস্বরূপ যদি মাল্টিপ্লায়ার বা স্টেট থাকে
                            mult = data.get("multiplier") or data.get("f") or 1.00
                            status = data.get("status") or "RUNNING"
                            cache.update_state(status, float(mult))
                    except json.JSONDecodeError:
                        # যদি ডাটা সরাসরি JSON না হয়ে টেক্সট ফরম্যাটে হয়
                        pass

        except ConnectionClosed as cc:
            logging.warning(f"[WebSocket] Connection closed: {cc}. Reconnecting...")
            await asyncio.sleep(3)
        except Exception as ex:
            logging.error(f"[WebSocket] Error: {ex}. Retrying...")
            await asyncio.sleep(5)

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
