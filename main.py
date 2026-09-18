from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    # সাময়িকভাবে টেস্ট করার জন্য ডেমো ডেটা পাঠানো হচ্ছে
    return jsonify({
        "status": "Connected",
        "history": ["1.50x", "2.20x", "1.15x", "5.40x", "2.00x"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
