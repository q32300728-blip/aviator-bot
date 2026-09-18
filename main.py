from flask import Flask, render_template, jsonify
import threading
import time
import random

app = Flask(__name__)

# লাইভ ডাটা স্টোরেজ
current_game_state = {
    "status": "Waiting...",
    "multiplier": "1.00x",
    "history": ["1.50x", "2.20x", "1.15x"]
}

# ব্যাকগ্রাউন্ডে লাইভ ডাটা আপডেট বা ট্র্যাক করার ফাংশন
def live_data_fetcher():
    while True:
        # এখানে আসল এপিআই বা গেম সোর্স থেকে ডাটা কানেক্ট করতে হবে
        time.sleep(3) # প্রতি ৩ সেকেন্ড পর পর ডাটা চেক করবে
        simulated_multiplier = round(random.uniform(1.01, 4.50), 2)
        
        current_game_state["multiplier"] = f"{simulated_multiplier}x"
        current_game_state["status"] = "Running"
        
        # হিস্টরিতে নতুন ডাটা যোগ করা
        current_game_state["history"].insert(0, f"{simulated_multiplier}x")
        if len(current_game_state["history"]) > 10:
            current_game_state["history"].pop()

# ব্যাকগ্রাউন্ড থ্রেড স্টার্ট করা
threading.Thread(target=live_data_fetcher, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data')
def get_live_data():
    return jsonify(current_game_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
