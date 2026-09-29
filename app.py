import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
import websocket

app = FastAPI()

# এনভায়রনমেন্ট থেকে WebSocket URL রিড করা (ফলব্যাক সহ)
WS_URL = os.getenv(
    "TARGET_WS_URL",
    "wss://a3jissau.ossjs3.com/ws/websocket?socketauthstr=2850-314182e8b6dd7daea451790048165987074216",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_message(ws, message):
  logger.info(f"Received message: {message}")


def on_error(ws, error):
  logger.error(f"WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
  logger.info("WebSocket connection closed")


def on_open(ws):
  logger.info("WebSocket connection opened successfully")


def run_websocket():
  # persistent connection বজায় রাখার জন্য লুপ
  while True:
    try:
      logger.info(f"Connecting to WebSocket: {WS_URL}")
      ws = websocket.WebSocketApp(
          WS_URL,
          on_message=on_message,
          on_error=on_error,
          on_close=on_close,
          on_open=on_open,
      )
      ws.run_forever()
    except Exception as e:
      logger.error(f"WebSocket connection failed: {e}")
    import time

    time.sleep(5)  # রিট্রোই করার আগে ৫ সেকেন্ড অপেক্ষা


@app.on_event("startup")
async def startup_event():
  # ব্যাকগ্রাউন্ডে WebSocket কানেকশন রান করার জন্য থ্রেড শুরু করা
  import threading

  ws_thread = threading.Thread(target=run_websocket, daemon=True)
  ws_thread.start()


@app.get("/")
def read_root():
  return {
      "status": "online",
      "message": "Aviator bot is running smoothly via WebSocket!",
  }
