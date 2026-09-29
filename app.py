import os
import asyncio
import logging
import time
import requests
from fastapi import FastAPI
import websocket
import uvicorn

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# গ্লোবাল ডিকশনারি যেখানে লাইভ ডাটা জমা থাকবে
live_flight_data = {
    "status": "Connecting...",
    "last_message": None,
    "updated_at": None
}

def get_dynamic_ws_url():
    """
    ডাইনামিক বা অটোমেটিক WebSocket ইউআরএল পাওয়ার ফাংশন।
    যদি রেলওয়ে ভ্যারিয়েবলে লিংক থাকে সেটি নেবে, অন্যথায় ডিফল্ট লিংক ব্যবহার করবে।
    """
    env_url = os.getenv("TARGET_WS_URL")
    if env_url:
        return env_url
    
    # আপনার ব্রাউজার থেকে পাওয়া সঠিক ও লেটেস্ট WebSocket লিংকটি এখানে বসিয়ে দেওয়া হলো:
    default_url = "wss://ajiss.ossj3.com/ws/websocket?authStr=2850-314182ae8b6d7daea451790048165987074216"
    return default_url

def on_message(ws, message):
    global live_flight_data
    logger.info(f"Live Data Received: {message}")
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
    logger.info("Successfully connected to WebSocket!")
    live_flight_data["status"] = "Connected"

def run_websocket():
    reconnect_delay = 2
    max_delay = 60

    while True:
        try:
            # প্রতিবার রিডিকানেক্ট করার সময় ডাইনামিক লিংক রিফ্রেশ হবে
            current_ws_url = get_dynamic_ws_url()
            logger.info(f"Connecting to target server: {current_ws_url}")
            
            ws = websocket.WebSocketApp(
                current_ws_url,
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
            logger.error(f"Connection Exception: {e}")
        
        time.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, max_delay)

@app.on_event("startup")
async def startup_event():
    import threading
    ws_thread = threading.Thread(target=run_websocket, daemon=True)
    ws_thread.start()
    logger.info("Background Worker started with Auto-URL resolution.")

@app.get("/")
def read_root():
    return {
        "platform": "Aviator Live Monitor (Automated)",
        "connection_status": live_flight_data["status"],
        "last_update_time": live_flight_data["updated_at"],
        "pre_flight_data": live_flight_data["last_message"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
