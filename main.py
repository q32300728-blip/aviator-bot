from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Aviator Bot is Running!"

# ব্রাউজার থেকে লাইভ ডাটা রিসিভ করার রুট
@app.route('/receive-data', methods=['POST'])
def receive_data():
    req_data = request.get_json()
    timestamp = req_data.get('timestamp')
    game_data = req_data.get('data')
    
    # রেন্ডার কনসোলে এই প্রিন্ট করা ডাটা দেখতে পাবেন
    print(f"Received Live Data: {game_data}")
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
