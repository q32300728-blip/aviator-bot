import os
import asyncio
import logging
import time
from fastapi import FastAPI
import websocket
import uvicorn

app = FastAPI()

# রেলওয়ের Variables থেকে WebSocket URL রিড করা
WS_URL = os.getenv("TARGET_WS_URL", "")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# গ্লোবাল ডিকশনারি যেখানে রিয়েল-টাইম লাইভ ডাটা জমা থাকবে
live_flight_data = {
    "status": "Connecting...",
    "last_message": None,
    "updated_at": None
}

def on_message(ws, message):
    global live_flight_data
    logger.info(f"Live Data Stream: {message}")
    # ওয়েবসকেট থেকে আসা ডাটা এখানে সেভ হচ্ছে, যা আপনি ব্রাউজারে দেখতে পাবেন
    live_flight_data["status"] = "Active & Receiving"
    live_flight_data["last_message"] = message
    live_flight_data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

def on_error(ws, error):
    logger.error(f"WebSocket Error: {error}")
    live_flight_data["status"] = f"Error: {error}"

def on_close(ws, close_status_code, close_msg):
    logger.warning(f"Connection Lost. Code: {close_status_code}, Reason: {close_msg}")
    live_flight_data["status"] = "Disconnected (Reconnecting...)"

def on_open(ws):
    logger.info("WebSocket Connection Successfully Established!")
    live_flight_data["status"] = "Connected"

def run_websocket():
    if not WS_URL:
        logger.error("CRITICAL: TARGET_WS_URL environment variable is missing!")
        return
        
    reconnect_delay = 2
    max_delay = 60

    while True:
        try:
            logger.info("Initiating secure WebSocket handshake...")
            ws = websocket.WebSocketApp(
                WS_URL,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            ws.run_forever(ping_interval=20, ping_timeout=10)
        except Exception as e:
            logger.error(f"Network or Socket Exception: {e}")
        
        time.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, max_delay)

@app.on_event("startup")
async def startup_event():
    import threading
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    logger.info("Background WebSocket worker spawned successfully.")

# ব্রাউজারে লাইভ ডাটা দেখার জন্য রুট (এখানেই বিমান ওড়ার আগের ডাটা দেখা যাবে)
@app.get("/")
def read_root():
    return {
        "bot_name": "Aviator Live Data Monitor",
        "connection_status": live_flight_data["status"],
        "last_update_time": live_flight_data["updated_at"],
        "live_data": live_flight_data["last_message"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
