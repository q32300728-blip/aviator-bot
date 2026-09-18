import asyncio
import json
import logging
import websockets
from flask import Flask, render_template, jsonify

# ১. লো-লেটেসি ও লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# ৪. স্টেট মেশিন ও ক্যাশিং (গেমের বর্তমান অবস্থা ধরে রাখার জন্য)
game_state = {
    "status": "Connecting...",
    "multiplier": "1.00x",
    "history": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    return jsonify(game_state)

async def run_game_bot():
    ws_url = "wss://channel.local2j111.link/"
    
    # ৩. সকেট হ্যান্ডশেক ও হার্টবিট সিমুলেশন (ব্রাউজার হেডার সহ)
    extra_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://local2j111.link"
    }

    while True:
        try:
            async with websockets.connect(ws_url, extra_headers=extra_headers) as ws:
                game_state["status"] = "Live Connected"
                logging.info("Successfully Connected to Real WebSocket Server!")

                async for message in ws:
                    # ২. বাইনারি প্রোটোকল ও ডাটা পার্সিং লজিক
                    try:
                        if isinstance(message, bytes):
                            # বাইনারি ডাটা হলে ডিকোড করা
                            parsed_data = message.decode('utf-8', errors='ignore')
                        else:
                            parsed_data = message

                        # জেসন বা টেক্সট পার্স করে স্টেট আপডেট করা
                        if parsed_data.startswith("{") or parsed_data.startswith("["):
                            data = json.loads(parsed_data)
                            # গেম ডাটা আপডেট লজিক
                            if "multiplier" in data:
                                game_state["multiplier"] = str(data["multiplier"])
                        
                        logging.info(f"Received Data: {parsed_data}")

                    except json.JSONDecodeError:
                        # বাইনারি বা র ম্যাসেজ হ্যান্ডেল করার জন্য
                        pass
                    except Exception as e:
                        logging.error(f"Parsing error: {e}")

        except Exception as e:
            game_state["status"] = "Reconnecting..."
            logging.warning(f"Connection lost: {e}. Retrying in 3 seconds...")
            await asyncio.sleep(3)

# ২ & ৩. অ্যাসিঙ্ক্রোনাস ইভেন্ট লুপ ব্যাকগ্রাউন্ডে রান করা
def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_game_bot())

if __name__ == '__main__':
    import threading
    loop = asyncio.new_event_loop()
    threading.Thread(target=start_background_loop, args=(loop,), daemon=True).start()
    
    # ফ্লাস্ক সার্ভার রান করা
    app.run(host='0.0.0.0', port=5000)
