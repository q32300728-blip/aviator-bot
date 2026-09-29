import os
import asyncio
import logging
import time
from fastapi import FastAPI
import websocket
import uvicorn

app = FastAPI()

# সরাসরি j188 সার্ভারের WebSocket URL বা রেলওয়ের ভ্যারিয়েবল থেকে রিড করা
WS_URL = os.getenv("TARGET_WS_URL", "wss://j188.com/ws/websocket")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# গ্লোবাল ডিকশনারি যেখানে বিমান ওড়ার আগের লাইভ ডাটা জমা থাকবে
live_flight_data = {
    "status": "Connecting to j188...",
    "last_message": None,
    "updated_at": None
}

def on_message(ws, message):
    global live_flight_data
    logger.info(f"j188 Live Data: {message}")
    live_flight_data["status"] = "Active & Receiving from j188"
    live_flight_data["last_message"] = message
    live_flight_data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

def on_error(ws, error):
    logger.error(f"j188 WebSocket Error: {error}")
    live_flight_data["status"] = f"Error: {error}"

def on_close(ws, close_status_code, close_msg):
    logger.warning(f"j188 Connection Lost. Code: {close_status_code}, Reason: {close_msg}")
    live_flight_data["status"] = "Disconnected (Reconnecting to j188...)"

def on_open(ws):
    logger.info("Successfully connected to j188 WebSocket!")
    live_flight_data["status"] = "Connected to j188"

def run_websocket():
    reconnect_delay = 2
    max_delay = 60

    while True:
        try:
            logger.info(f"Connecting to target j188 server: {WS_URL}")
            
            # বড় ডেভেলপারদের মতো রিয়েল-টাইম হেডারের স্ট্যান্ডার্ড হ্যান্ডশেক
            ws = websocket.WebSocketApp(
                WS_URL,
                header={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Origin": "https://j188.com"
                },
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            ws.run_forever(ping_interval=20, ping_timeout=10)
        except Exception as e:
            logger.error(f"j188 Connection Exception: {e}")
        
        time.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, max_delay)

@app.on_event("startup")
async def startup_event():
    import threading
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    logger.info("j188 Background Worker started.")

@app.get("/")
def read_root():
    return {
        "platform": "j188 Aviator Live Monitor",
        "connection_status": live_flight_data["status"],
        "last_update_time": live_flight_data["updated_at"],
        "pre_flight_data": live_flight_data["last_message"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
