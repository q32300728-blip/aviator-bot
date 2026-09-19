import asyncio
import json
import logging
import threading
from flask import Flask, jsonify

# 1. Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Target WebSocket Endpoint
WS_URL = "wss://channel.local2j111.link/"

# 2. State Machine & Data Tracking Cache
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
        logging.info(f"[Data Detected] State: {self.state} | Multiplier: {self.multiplier}x")

cache = GameStateCache()

# 3. Precise Message Parser & Identifier
def parse_incoming_message(message):
    try:
        if isinstance(message, bytes):
            decoded_data = message.decode('utf-8', errors='ignore')
        else:
            decoded_data = message

        data = json.loads(decoded_data)
        return data
    except Exception as e:
        # যদি ডাটা সরাসরি JSON ফরম্যাটে না হয়ে অন্য কোনো স্ট্রিং হয়, তবে তা এখানে হ্যান্ডেল হবে
        return None

# 4. WebSocket Live Listener
async def crash_bot_listener():
    from websockets.client import connect
    from websockets.exceptions import ConnectionClosed
    
    while True:
        try:
            logging.info(f"[WebSocket] Connecting to target server...")
            async with connect(WS_URL, ping_interval=20, ping_timeout=10) as websocket:
                logging.info("[WebSocket] Successfully connected & monitoring live data.")
                
                async for message in websocket:
                    parsed_data = parse_incoming_message(message)
                    if not parsed_data:
                        continue

                    # সার্ভার থেকে আসা ইভেন্ট এবং মাল্টিপ্লায়ার শনাক্ত করা
                    event_type = parsed_data.get("type", "unknown")
                    multiplier = parsed_data.get("multiplier", 1.00)

                    if event_type == "started":
                        cache.update_state("STARTED", multiplier)
                    elif event_type == "crashed":
                        cache.update_state("CRASHED", multiplier)
                    elif event_type == "waiting":
                        cache.update_state("WAITING", 1.00)

        except ConnectionClosed as cc:
            logging.warning(f"[WebSocket] Connection dropped: {cc}. Reconnecting...")
            await asyncio.sleep(3)
        except Exception as ex:
            logging.error(f"[WebSocket] Error: {ex}. Retrying...")
            await asyncio.sleep(5)

# Flask Server for UI Dashboard
app = Flask(__name__)

@app.route("/data")
def get_data():
    return jsonify({
        "state": cache.state,
        "multiplier": f"{cache.multiplier:.2f}x",
        "history": cache.history[-5:]
    })

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Data Monitor</title>
        <style>
            body {
                background-color: #050b14;
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 400px;
                margin: auto;
                background: #0b192c;
                border: 2px solid #1e3e62;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 195, 255, 0.2);
            }
            .header {
                font-size: 14px;
                color: #00c3ff;
                letter-spacing: 2px;
                margin-bottom: 20px;
                font-weight: bold;
            }
            .circle-box {
                width: 220px;
                height: 220px;
                border: 4px solid #00c3ff;
                border-radius: 50%;
                margin: 30px auto;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 30px rgba(0, 195, 255, 0.4);
                background: radial-gradient(circle, #102035 0%, #060e18 100%);
            }
            .multiplier {
                font-size: 42px;
                font-weight: bold;
                color: #00ffcc;
            }
            .status-label {
                font-size: 12px;
                color: #8a99ad;
                margin-top: 5px;
            }
            .badge {
                background: #1e3e62;
                color: #00c3ff;
                padding: 10px 20px;
                border-radius: 30px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
                display: inline-block;
                border: 1px solid #00c3ff;
            }
            .history {
                margin-top: 25px;
                font-size: 13px;
                color: #a0aec0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">DATA MONITORING BOT</div>
            <div class="circle-box">
                <div class="status-label" id="state-text">WAITING</div>
                <div class="multiplier" id="mult-text">1.00x</div>
                <div class="status-label">LIVE STATUS</div>
            </div>
            <div class="badge">🟢 DETECTING LIVE</div>
            <div class="history">History: <span id="history-text">[]</span></div>
        </div>

        <script>
            setInterval(async () => {
                try {
                    let response = await fetch('/data');
                    let data = await response.json();
                    document.getElementById('state-text').innerText = data.state;
                    document.getElementById('mult-text').innerText = data.multiplier;
                    document.getElementById('history-text').innerText = JSON.stringify(data.history);
                } catch (e) {
                    console.log("Fetch error", e);
                }
            }, 500);
        </script>
    </body>
    </html>
    """

def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    try:
        asyncio.run(crash_bot_listener())
    except KeyboardInterrupt:
        logging.info("[Bot] Stopped.")
