from flask import Flask, render_template, jsonify
import asyncio
import threading
import websockets
import json

app = Flask(__name__)

# গেম হিস্ট্রি এবং স্ট্যাটাস সংরক্ষণের গ্লোবাল ভেরিয়েবল
game_history_list = ["1.50x", "2.20x"]
current_status = "Connecting to Live WebSocket..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list, current_status
    # সর্বশেষ মানটি মাল্টিপ্লায়ার হিসেবে সেট করা
    latest_multiplier = game_history_list[0] if game_history_list else "1.00x"
    return jsonify({
        "status": current_status,
        "multiplier": latest_multiplier,
        "history": game_history_list
    })

# WebSocket কানেক্ট করে লাইভ ডাটা রিসিভ করার ফাংশন
async def listen_websocket():
    global game_history_list, current_status
    uri = "wss://channel.local2j111.link/"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                current_status = "Live Connected"
                print("Connected to live WebSocket successfully!")
                
                async for message in websocket:
                    try:
                        if isinstance(message, str):
                            data = json.loads(message)
                            if "multiplier" in data:
                                val = str(data["multiplier"]) + "x"
                                game_history_list.insert(0, val)
                                if len(game_history_list) > 10:
                                    game_history_list.pop()
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            current_status = "Reconnecting..."
            print("WebSocket connection lost, reconnecting...", e)
            await asyncio.sleep(3)

def run_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_websocket())

threading.Thread(target=run_background_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
