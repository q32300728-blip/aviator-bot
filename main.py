from flask import Flask, render_template, jsonify
import asyncio
import threading
import websockets

app = Flask(__name__)

# গেমের হিস্ট্রি সংরক্ষণের গ্লোবাল লিস্ট
game_history_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list
    return jsonify({
        "status": "Running (WebSocket Connected)",
        "history": game_history_list
    })

# সরাসরি WebSocket কানেক্ট করে ডেটা শোনার ফাংশন
async def listen_websocket():
    global game_history_list
    uri = "wss://channel.local2j111.link/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Game WebSocket Successfully!")
                async for message in websocket:
                    # যদি মেসেজ বাইনারি বা টেক্সট হয়, সে অনুযায়ী প্রসেস করা
                    # এখানে রিসিভ হওয়া ডেটা থেকে মাল্টিপ্লায়ার বা হিস্ট্রি বের করে লিস্টে যোগ করতে হবে
                    if isinstance(message, bytes):
                        # বাইনারি ডেটা হ্যান্ডেল করার লজিক (প্রয়োজনে ডিকোড করা)
                        pass
                    else:
                        # টেক্সট মেসেজ হলে
                        pass
                    
                    # উদাহরণস্বরূপ ডেমো ডাটা বা পার্স করা ডাটা এভাবে পুশ করা যায়:
                    # game_history_list.insert(0, extracted_value)
                    
        except Exception as e:
            print("WebSocket Connection Error, reconnecting in 5s...", e)
            await asyncio.sleep(5)

def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_websocket())

# ব্যাকগ্রাউন্ডে থ্রেড চালু করা
if __name__ == '__main__':
    t = threading.Thread(target=run_async_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)
