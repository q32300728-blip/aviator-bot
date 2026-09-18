from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# গেমের আগের রাউন্ডগুলোর হিস্ট্রি সিরিয়ালে সংরক্ষণের জন্য লিস্ট
game_history_list = []

@app.route('/')
def index():
    return render_template('index.html')

# গেমের আগের রাউন্ডের ডেটা সিরিয়াল অনুযায়ী রিসিভ করার রুট
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global game_history_list
    try:
        req_data = request.json
        payload = req_data.get('data', {})
        
        # যদি হিস্ট্রি বা আগের রাউন্ডের ডেটা আসে
        if "history" in payload:
            game_history_list = payload["history"] # এটি একটি লিস্ট হবে যা আগের রাউন্ডগুলোর রেজल्ट সিরিয়ালে রাখবে
                    
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ড্যাশবোর্ডে শুধু সিরিয়াল অনুযায়ী হিস্ট্রি পাঠানোর রুট
@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list
    return jsonify({
        "status": "Ready",
        "history": game_history_list
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
