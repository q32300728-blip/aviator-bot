from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# গেম হিস্ট্রি সংরক্ষণের স্টোরেজ
game_history_list = ["1.50x", "2.20x", "1.15x"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    return jsonify({
        "status": "Production Ready",
        "history": game_history_list
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
