from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# গেমের রিয়েল ডাটা স্টোর করার গ্লোবাল ভেরিয়েবল
latest_game_data = {
    "multiplier": "Waiting...",
    "status": "Connecting...",
    "history": []
}

@app.route('/')
def index():
    return render_template('index.html')

# বুকমার্কলেট থেকে লাইভ ডাটা রিসিভ করার এন্ডপয়েন্ট
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global latest_game_data
    try:
        req_data = request.json
        payload = req_data.get('data')
        
        if payload:
            print("Captured Real Data:", payload)
            latest_game_data["multiplier"] = "Live Data Received"
            latest_game_data["status"] = "Active"
            
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ফ্রন্টএন্ডে রিয়েল-টাইম ডাটা পাঠানোর এন্ডপয়েন্ট
@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global latest_game_data
    return jsonify(latest_game_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
