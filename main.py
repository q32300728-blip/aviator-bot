from flask import Flask, render_template, jsonify
import random
import threading
import time

app = Flask(__name__)

# গেমের লাইভ ডাটা রাখার স্টেট
game_data = {
    "status": "Running smoothly",
    "multiplier": "1.00x",
    "history": ["1.50x", "2.20x", "1.35x"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    return jsonify(game_data)

def update_simulation():
    while True:
        time.sleep(1.5)
        # রেন্ডম মাল্টিপ্লায়ার জেনারেট করে লাইভ দেখাবে
        val = round(random.uniform(1.01, 6.50), 2)
        game_data["multiplier"] = f"{val}x"
        
        # মাঝে মাঝে হিস্ট্রি আপডেট হবে
        if val > 4.0:
            game_data["history"].insert(0, f"{val}x")
            if len(game_data["history"]) > 10:
                game_data["history"].pop()

# ব্যাকগ্রাউন্ডে ডাটা আপডেট চালু রাখা
threading.Thread(target=update_simulation, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
