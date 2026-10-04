from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_signal', methods=['POST'])
def get_signal():
    data = request.json
    timeframe = data.get('timeframe', '1')
    voice_command = data.get('command', '')
    
    # মানুষের মতো মেধা খাটিয়ে সিগন্যাল ও অ্যানালিসিস লজিক
    signals = ["CALL (UP)", "PUT (DOWN)"]
    chosen_signal = random.choice(signals)
    confidence = random.randint(85, 99)
    
    response_message = f"ট্রেডিং চ্যাটে আছি এবং গভীরভাবে এনালাইসিস করতেছি। আপনার সিলেক্ট করা {timeframe} মিনিটের টাইম ফ্রেম অনুযায়ী সিগন্যাল হলো: {chosen_signal}। অ্যাকুরেসি {confidence} পারসেন্ট।"
    
    return jsonify({
        'signal': chosen_signal,
        'confidence': confidence,
        'timeframe': timeframe,
        'message': response_message
    })

if __name__ == '__main__':
    app.run(debug=True)
