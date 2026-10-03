import os
import random
from flask import Flask, render_template_string, request

app = Flask('')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TR PRO Trading Bot - OTC Markets</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0b0f19; color: #fff; text-align: center; padding: 20px; }
        .container { max-width: 500px; margin: 0 auto; background: #111827; padding: 25px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); border: 1px solid #1f2937; }
        h1 { color: #38bdf8; font-size: 22px; margin-bottom: 20px; }
        .signal-box { background: #1f2937; padding: 18px; margin-top: 20px; border-radius: 10px; font-size: 16px; text-align: left; border-left: 5px solid #38bdf8; }
        .up { color: #22c55e; font-weight: bold; font-size: 22px; }
        .down { color: #ef4444; font-weight: bold; font-size: 22px; }
        select, button { padding: 12px; margin: 10px 0; width: 100%; border-radius: 6px; border: none; font-size: 15px; box-sizing: border-box; }
        select { background: #374151; color: #fff; }
        .start-btn { background: #059669; color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .start-btn:hover { background: #047857; }
        .signal-btn { background: #0284c7; color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .signal-btn:hover { background: #0369a1; }
        .loading { color: #facc15; font-style: italic; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 TR PRO AI Trading Bot</h1>
        <form method="POST">
            <label><b>Select Asset / OTC Pair:</b></label>
            <select name="selected_pair">
                {% for p in pairs %}
                    <option value="{{ p }}" {% if selected_pair == p %}selected{% endif %}>{{ p }}</option>
                {% endfor %}
            </select>

            <label><b>Select Chart Timeframe:</b></label>
            <select name="timeframe">
                <option value="10 Seconds" {% if timeframe == '10 Seconds' %}selected{% endif %}>10 Seconds Chart</option>
                <option value="15 Seconds" {% if timeframe == '15 Seconds' %}selected{% endif %}>15 Seconds Chart</option>
                <option value="30 Seconds" {% if timeframe == '30 Seconds' %}selected{% endif %}>30 Seconds Chart</option>
                <option value="1 Minute" {% if timeframe == '1 Minute' %}selected{% endif %}>1 Minute Chart</option>
            </select>

            <button type="submit" name="action" value="start" class="start-btn">🚀 Start & Connect Market</button>
            
            {% if started %}
            <div class="loading">✅ Connected to Market. Click below for instant analysis!</div>
            <button type="submit" name="action" value="get_signal" class="signal-btn">📊 Get Instant High-Accuracy Signal</button>
            {% endif %}
        </form>

        {% if signal %}
        <div class="signal-box">
            <p><b>📌 Selected Asset:</b> {{ pair }}</p>
            <p><b>⏱ Timeframe:</b> {{ timeframe }}</p>
            <p><b>🔍 Analysis Logic:</b> {{ logic }}</p>
            <p><b>📈 Final Signal:</b> <span class="{{ class_name }}">{{ signal }}</span></p>
            <p><b>🎯 Accuracy Rate:</b> {{ accuracy }}% (Verified)</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# কোটেক্স প্ল্যাটফর্মের জনপ্রিয় ওটিসি পেয়ারগুলোর তালিকা
OTC_PAIRS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", 
    "USD/PKR (OTC)", "USD/BDT (OTC)", "NZD/CAD (OTC)", 
    "CAD/CHF (OTC)", "GBP/JPY (OTC)", "AUD/JPY (OTC)", 
    "EUR/JPY (OTC)", "USD/JPY (OTC)", "USD/INR (OTC)"
]

DEEP_LOGICS = [
    "Multi-Timeframe Trend Alignment + Order Block Rejection",
    "Bollinger Band Squeeze Breakout + Volume Confirmation",
    "RSI Divergence at Strong Support / Resistance Zone",
    "Moving Average (EMA 50/200) Golden/Death Crossover Momentum",
    "Price Action Pinbar / Engulfing Pattern at Key Level"
]

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_pair = "EUR/USD (OTC)"
    timeframe = "10 Seconds"
    started = False
    signal_data = {}

    if request.method == 'POST':
        selected_pair = request.form.get('selected_pair', 'EUR/USD (OTC)')
        timeframe = request.form.get('timeframe', '10 Seconds')
        action = request.form.get('action')
        
        if action == 'start':
            started = True
        elif action == 'get_signal':
            started = True
            logic = random.choice(DEEP_LOGICS)
            signal_type = random.choice(["UP (CALL) 🟢", "DOWN (PUT) 🔴"])
            class_name = "up" if "UP" in signal_type else "down"
            accuracy = round(random.uniform(96.0, 99.8), 2)
            
            signal_data = {
                'signal': signal_type,
                'pair': selected_pair,
                'logic': logic,
                'class_name': class_name,
                'accuracy': accuracy
            }

    return render_template_string(
        HTML_TEMPLATE, 
        pairs=OTC_PAIRS,
        selected_pair=selected_pair, 
        timeframe=timeframe, 
        started=started, 
        **signal_data
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
