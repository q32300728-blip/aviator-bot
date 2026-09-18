from flask import Flask, render_template, jsonify
import asyncio
import threading
import websockets
import json

app = Flask(__name__)

# রিয়েল-টাইম গেম হিস্ট্রি সংরক্ষণের জন্য গ্লোবাল লিস্ট
game_history_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list
    return jsonify({
        "status": "Running (Live WebSocket)",
        "history": game_history_list
    })

# WebSocket কানেক্ট করে লাইভ ডেটা রিসিভ করার লজিক
async def listen_websocket():
    global game_history_list
    uri = "wss://channel.local2j111.link/"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Live WebSocket successfully!")
                async for message in websocket:
                    try:
                        # যদি ডাটা টেক্সট বা জেসন ফরম্যাটে আসে
                        if isinstance(message, str):
                            data = json.loads(message)
                            # গেমের মাল্টিপ্লায়ার বা হিস্ট্রি ডেটা এখানে প্রসেস হবে
                            # আপনার গেমের ডাটা স্ট্রাকচার অনুযায়ী এখানে ভ্যালু পুশ করতে হবে
                            # উদাহরনস্বরূপ:
                            if "multiplier" in data:
                                game_history_list.insert(0, str(data["multiplier"]) + "x")
                                if len(game_history_list) > 10:  
                                    game_history_list.pop()
                        elif isinstance(message, bytes):
                            # বাইনারি মেসেজ হ্যান্ডেল করার ক্ষেত্রে
                            pass
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print("WebSocket connection lost, reconnecting...", e)
            await asyncio.sleep(3)

def run_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_websocket())

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে WebSocket লিসেনার থ্রেড চালু করা
    t = threading.Thread(target=run_background_loop, daemon=True)
    t.start()
    
    # ফ্লাস্ক অ্যাপ রান করা
    app.run(host='0.0.0.0', port=5000)
