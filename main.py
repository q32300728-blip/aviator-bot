from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

latest_game_data = {
    "multiplier": "Waiting...",
    "status": "Connecting...",
    "history": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive-data', methods=['POST'])
def receive_data():
    global latest_game_data
    try:
        req_data = request.json
        payload = req_data.get('data')
        
        if payload:
            # গেমের WebSocket ডাটা থেকে গুণক ফিল্টার করার চেষ্টা
            latest_game_data["multiplier"] = "Live Connected!"
            latest_game_data["status"] = "Active"
            
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global latest_game_data
    return jsonify(latest_game_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
