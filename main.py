from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# গেম শুরুর আগের ডেটা বা হিস্ট্রি সংরক্ষণের জন্য
game_prediction_data = {
    "next_multiplier": "Waiting for prediction...",
    "history": [],
    "status": "Waiting for game..."
}

@app.route('/')
def index():
    return render_template('index.html')

# গেম শুরু হওয়ার আগের ডেটা রিসিভ করার রুট
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global game_prediction_data
    try:
        req_data = request.json
        payload = req_data.get('data', {})
        
        # গেমের আগের ডেটা বা সিগন্যাল এখানে আপডেট হবে
        if "next_multiplier" in payload:
            game_prediction_data["next_multiplier"] = payload["next_multiplier"]
        if "history" in payload:
            game_prediction_data["history"] = payload["history"]
            
        game_prediction_data["status"] = "Ready for Next Round"
                    
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ড্যাশবোর্ডে শুধু গেম শুরুর আগের ডেটা পাঠানোর রুট
@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_prediction_data
    return jsonify(game_prediction_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
