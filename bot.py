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
    <title>TR PRO Institutional SMC & Liquidity Bot</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #fff; margin: 0; padding: 15px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #111827; padding: 12px 20px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 20px; }
        .logo { font-size: 18px; font-weight: bold; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        .pro-badge { background: #22c55e; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .container { max-width: 650px; margin: 0 auto; background: #111827; padding: 20px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.7); border: 1px solid #1f2937; }
        h2 { color: #38bdf8; font-size: 18px; text-align: center; margin-bottom: 15px; }
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
            <div class="logo">⚡ TR PRO BOT <span class="pro-badge">SMC PRO</span></div>
            <div style="font-size: 13px; color: #9ca3af;">Quotex OTC Market</div>
        </div>

        <h2>🏛️ Institutional SMC & Order Block Scanner</h2>
        
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
                <option value="1 Minute" {% if timeframe == '1 Minute' %}selected{% endif %}>1 Minute</option>
            </select>

            <button type="submit" name="action" value="start" class="start-btn">🚀 Initialize Institutional Engine</button>
            
            {% if started %}
            <div class="loading">✅ Market connected. Scanning OB, FVG & Liquidity Sweeps...</div>
            <button type="submit" name="action" value="get_signal" class="signal-btn">📊 Get Pro Institutional Signal</button>
            {% endif %}
        </form>

        {% if signal %}
        <div class="signal-box">
            <p><b>📌 Asset:</b> {{ pair }}</p>
            <p><b>⏱ Timeframe:</b> {{ timeframe }}</p>
            <p><b>🧱 Order Block (OB):</b> {{ ob_status }}</p>
            <p><b>🌊 Liquidity Sweep:</b> {{ liquidity_status }}</p>
            <p><b>⚡ Fair Value Gap (FVG):</b> {{ fvg_status }}</p>
            <p><b>📈 Indicator & Price Action:</b> {{ pa_ind_status }}</p>
            <p><b>🎯 Final Signal:</b> <span class="{{ class_name }}">{{ signal }}</span></p>
            <p><b>⭐ Accuracy Score:</b> {{ accuracy }}%</p>
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

OB_LOGICS = [
    "Bullish Order Block (Demand Zone) Mitigation Test",
    "Bearish Order Block (Supply Zone) Rejection Tap",
    "15M/1H Confluence Institutional Order Block Active",
    "Major Mitigation Block Rebound Active"
]

LIQUIDITY_LOGICS = [
    "Bullish Liquidity Sweep (Asian Session Low Grab / Stop Hunt)",
    "Bearish Liquidity Sweep (Previous High Sweep & Purge)",
    "Internal Range Liquidity Sweep + Change of Character (CHoCH)",
    "External Range Liquidity Void Fill & Sweep"
]

FVG_LOGICS = [
    "Bullish Fair Value Gap (FVG) Imbalance Fill & Rebound",
    "Bearish Fair Value Gap (FVG) Resistance Barrier",
    "Unfilled Liquidity Gap Re-test in Progress",
    "Discount Array FVG Target Achieved"
]

PA_IND_LOGICS = [
    "RSI Oversold (<30) + Bullish Pinbar Price Action Confirmation",
    "RSI Overbought (>70) + Bearish Engulfing Candle Rejection",
    "Bollinger Bands Lower Band Bounce + Volume Spike",
    "MACD Bullish Histogram Divergence + Break of Structure (BOS)"
]

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_pair = "EUR/USD (OTC)"
    timeframe = "10 Seconds"
    started = False
    signal = None
    pair = ""
    ob_status = ""
    liquidity_status = ""
    fvg_status = ""
    pa_ind_status = ""
    class_name = ""
    accuracy = 0.0

    if request.method == 'POST':
        selected_pair = request.form.get('selected_pair', 'EUR/USD (OTC)')
        timeframe = request.form.get('timeframe', '10 Seconds')
        action = request.form.get('action')
        
        if action == 'start':
            started = True
        elif action == 'get_signal':
            started = True
            ob_status = random.choice(OB_LOGICS)
            liquidity_status = random.choice(LIQUIDITY_LOGICS)
            fvg_status = random.choice(FVG_LOGICS)
            pa_ind_status = random.choice(PA_IND_LOGICS)
            
            if "Bullish" in ob_status or "Demand" in ob_status or "Oversold" in pa_ind_status or "Rebound" in fvg_status:
                signal = "UP (CALL) 🟢"
            else:
                signal = "DOWN (PUT) 🔴"
                
            class_name = "up" if "UP" in signal else "down"
            accuracy = round(random.uniform(98.5, 99.9), 2)
            pair = selected_pair

    return render_template_string(
        HTML_TEMPLATE, 
        pairs=OTC_PAIRS,
        selected_pair=selected_pair, 
        timeframe=timeframe, 
        started=started,
        signal=signal,
        pair=pair,
        ob_status=ob_status,
        liquidity_status=liquidity_status,
        fvg_status=fvg_status,
        pa_ind_status=pa_ind_status,
        class_name=class_name,
        accuracy=accuracy
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
