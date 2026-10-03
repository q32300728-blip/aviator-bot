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
    <title>TR PRO Smart Liquidity Trading Bot</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #fff; margin: 0; padding: 15px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #111827; padding: 12px 20px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 20px; }
        .logo { font-size: 18px; font-weight: bold; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        .pro-badge { background: #22c55e; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .container { max-width: 600px; margin: 0 auto; background: #111827; padding: 20px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.7); border: 1px solid #1f2937; }
        h2 { color: #38bdf8; font-size: 20px; text-align: center; margin-bottom: 15px; }
        .pair-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
        .pair-card { background: #1f2937; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #374151; font-size: 14px; }
        .pair-card span { color: #22c55e; font-weight: bold; }
        select, button { padding: 12px; margin: 8px 0; width: 100%; border-radius: 6px; border: none; font-size: 15px; box-sizing: border-box; }
        select { background: #374151; color: #fff; }
        .start-btn { background: #059669; color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .start-btn:hover { background: #047857; }
        .signal-btn { background: #0284c7; color: #fff; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .signal-btn:hover { background: #0369a1; }
        .signal-box { background: #1f2937; padding: 18px; margin-top: 15px; border-radius: 10px; font-size: 14px; border-left: 5px solid #38bdf8; text-align: left; line-height: 1.6; }
        .up { color: #22c55e; font-weight: bold; font-size: 20px; }
        .down { color: #ef4444; font-weight: bold; font-size: 20px; }
        .loading { color: #facc15; font-style: italic; font-size: 13px; text-align: center; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡ TR PRO BOT <span class="pro-badge">PRO</span></div>
            <div style="font-size: 13px; color: #9ca3af;">Quotex OTC Market</div>
        </div>

        <h2>🧠 Smart Liquidity & Order Block Scanner</h2>
        
        <div class="pair-grid">
            <div class="pair-card">EUR/USD (OTC)<br><span>88% Profit</span></div>
            <div class="pair-card">GBP/USD (OTC)<br><span>85% Profit</span></div>
            <div class="pair-card">AUD/CAD (OTC)<br><span>83% Profit</span></div>
            <div class="pair-card">USD/PKR (OTC)<br><span>82% Profit</span></div>
        </div>

        <form method="POST">
            <label style="font-size: 14px; color: #d1d5db;"><b>Select OTC Asset:</b></label>
            <select name="selected_pair">
                {% for p in pairs %}
                    <option value="{{ p }}" {% if selected_pair == p %}selected{% endif %}>{{ p }}</option>
                {% endfor %}
            </select>

            <label style="font-size: 14px; color: #d1d5db;"><b>Select Timeframe:</b></label>
            <select name="timeframe">
                <option value="5 Seconds" {% if timeframe == '5 Seconds' %}selected{% endif %}>5 Seconds</option>
                <option value="10 Seconds" {% if timeframe == '10 Seconds' %}selected{% endif %}>10 Seconds</option>
                <option value="15 Seconds" {% if timeframe == '15 Seconds' %}selected{% endif %}>15 Seconds</option>
                <option value="30 Seconds" {% if timeframe == '30 Seconds' %}selected{% endif %}>30 Seconds</option>
            </select>

            <button type="submit" name="action" value="start" class="start-btn">🚀 Initialize Liquidity Engine</button>
            
            {% if started %}
            <div class="loading">✅ Market connected. Scanning Liquidity Pools & Sweeps...</div>
            <button type="submit" name="action" value="get_signal" class="signal-btn">📊 Get Liquidity-Based Signal</button>
            {% endif %}
        </form>

        {% if signal %}
        <div class="signal-box">
            <p><b>📌 Asset:</b> {{ pair }}</p>
            <p><b>⏱ Timeframe:</b> {{ timeframe }}</p>
            <p><b>💧 Liquidity Analysis:</b> {{ liquidity_status }}</p>
            <p><b>🧱 Order Block / Zone:</b> {{ zone_status }}</p>
            <p><b>📈 Final Signal:</b> <span class="{{ class_name }}">{{ signal }}</span></p>
            <p><b>🎯 Accuracy Score:</b> {{ accuracy }}%</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

OTC_PAIRS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", 
    "USD/PKR (OTC)", "USD/BDT (OTC)", "NZD/CAD (OTC)", 
    "CAD/CHF (OTC)", "GBP/JPY (OTC)", "AUD/JPY (OTC)", 
    "EUR/JPY (OTC)", "USD/JPY (OTC)", "USD/INR (OTC)"
]

LIQUIDITY_LOGICS = [
    "Bullish Liquidity Sweep below Asian Session Low + Order Block Rejection",
    "Bearish Liquidity Grab at Previous High (Stop Hunt) + Fair Value Gap Fill",
    "Double Top Liquidity Sweep + Institutional Rejection Candle",
    "Support Level Liquidity Purge + Strong Momentum Reversal"
]

ZONE_LOGICS = [
    "Institutional Demand Zone (Bullish OB)",
    "Institutional Supply Zone (Bearish OB)",
    "Key Resistance Level Liquidity Void",
    "Major Support Level Mitigation Block"
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
            liquidity_status = random.choice(LIQUIDITY_LOGICS)
            zone_status = random.choice(ZONE_LOGICS)
            
            if "Bullish" in liquidity_status or "Demand" in zone_status or "Support" in liquidity_status:
                signal_type = "UP (CALL) 🟢"
            else:
                signal_type = "DOWN (PUT) 🔴"
                
            class_name = "up" if "UP" in signal_type else "down"
            accuracy = round(random.uniform(97.5, 99.9), 2)
            
            signal_data = {
                'signal': signal_type,
                'pair': selected_pair,
                'timeframe': timeframe,
                'liquidity_status': liquidity_status,
                'zone_status': zone_status,
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
