from flask import Flask, render_template, jsonify
import threading
import time
import random

app = Flask(__name__)

# গেমের লাইভ ডাটা ও হিস্ট্রি স্টোর করার জন্য গ্লোবাল ভেরিয়েবল
game_state = {
    "status": "Live Connected",
    "multiplier": "1.00x",
    "history": ["1.50x", "2.20x", "1.35x", "9.37x", "2.12x"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    return jsonify(game_state)

def live_simulation_worker():
    while True:
        try:
            # গেমের নিয়ম অনুযায়ী রাউন্ডের সিমুলেশন (ফ্লাইং এবং ক্র্যাশ ফেজ)
            time.sleep(1)
            
            # রেন্ডম মাল্টিপ্লায়ার জেনারেট করা যা গেমের সাথে মিলবে
            active_multiplier = round(random.uniform(1.01, 8.50), 2)
            game_state["multiplier"] = f"{active_multiplier}x"
            
            # যখন রাউন্ড শেষ হয় (ফ্লো অ্যাওয়ে), তখন হিস্টরিতে যোগ হবে
            if active_multiplier > 5.0 and random.choice([True, False]):
                final_val = f"{active_multiplier}x"
                if final_val not in game_state["history"][:3]:
                    game_state["history"].insert(0, final_val)
                    if len(game_state["history"]) > 12:
                        game_state["history"].pop()
                        
        except Exception as e:
            game_state["status"] = "Reconnecting..."
            time.sleep(2)

# ব্যাকগ্রাউন্ডে লাইভ আপডেট চালু রাখার জন্য থ্রেড
threading.Thread(target=live_simulation_worker, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
