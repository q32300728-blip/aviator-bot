from flask import Flask, render_template, jsonify
import asyncio
import threading
import websockets
import json

app = Flask(__name__)

game_history_list = ["1.50x", "2.20x"]
current_status = "Connecting to Live WebSocket..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list, current_status
    latest_multiplier = game_history_list[0] if game_history_list else "1.00x"
    return jsonify({
        "status": current_status,
        "multiplier": latest_multiplier,
        "history": game_history_list
    })

async def listen_websocket():
    global game_history_list, current_status
    # আপনার নেটওয়ার্ক ট্যাব থেকে প্রাপ্ত সঠিক ওয়েবসোকেট ইউআরআই
    uri = "wss://channel.local2j111.link/?mesh-swimlane="
    
    extra_headers = {
        "Origin": "https://game.wifun777.link",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
    }
    
    while True:
        try:
            async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
                current_status = "Live Connected"
                print("Connected to live WebSocket successfully!")
                
                async for message in websocket:
                    try:
                        # বাইনারি ডেটা (bytes) বা টেক্সট হ্যান্ডেল করার লজিক
                        if isinstance(message, bytes):
                            try:
                                decoded_message = message.decode('utf-8')
                            except UnicodeDecodeError:
                                # বাইনারি ডেটা সরাসরি রিড করতে না পারলে স্কিপ করবে বা প্রসেস করবে
                                continue
                        else:
                            decoded_message = message
                        
                        if decoded_message and decoded_message.strip():
                            # যদি ডাটা JSON ফরম্যাটে থাকে
                            try:
                                data = json.loads(decoded_message)
                                if "multiplier" in data:
                                    val = str(data["multiplier"]) + "x"
                                    game_history_list.insert(0, val)
                                    if len(game_history_list) > 10:
                                        game_history_list.pop()
                            except json.JSONDecodeError:
                                # সাধারণ টেক্সট বা অন্য ফরম্যাট হলে এখানে হ্যান্ডেল হবে
                                pass
                                
                    except Exception as err:
                        print("Parsing error:", err)
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
