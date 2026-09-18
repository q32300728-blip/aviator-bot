import websocket
import json
import threading
from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# লাইভ ডাটা স্টোর করার ডিকশনারি
game_data = {
    "status": "Live Connected",
    "multiplier": "1.00x",
    "history": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    return jsonify(game_data)

def on_message(ws, message):
    try:
        # সার্ভার থেকে আসা বাইনারি বা টেক্সট মেসেজ প্রসেস করা
        # যদি মেসেজটি জেসন ফরম্যাটে হয় তবে এভাবে আপডেট করতে হবে:
        # data = json.loads(message)
        # game_data["multiplier"] = data.get("multiplier", "1.00x")
        
        # সাময়িকভাবে কনসোলে প্রিন্ট করে দেখার জন্য:
        print("Live Data Received:", message)
    except Exception as e:
        print("Parsing error:", e)

def on_error(ws, error):
    print("WebSocket Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed, Reconnecting...")

def on_open(ws):
    print("Successfully Connected to Real WebSocket Server!")

def start_websocket_stream():
    while True:
        try:
            ws_url = "wss://channel.local2j111.link/"
            ws = websocket.WebSocketApp(ws_url,
                                      on_open=on_open,
                                      on_message=on_message,
                                      on_error=on_error,
                                      on_close=on_close)
            ws.run_forever()
        except Exception as e:
            print("Connection failed, retrying in 3 seconds...", e)
            time.sleep(3)

# ব্যাকগ্রাউন্ডে রিয়েল-টাইম ওয়েবসকেট কানেকশন চালু রাখার থ্রেড
threading.Thread(target=start_websocket_stream, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
