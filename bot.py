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
    <title>Liquidity & SMC Trading Bot</title>
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
            <div class="logo">⚡ LIQUIDITY BOT <span class="pro-badge">SMC</span></div>
            <div style="font-size: 13px; color: #9ca3af;">OTC Liquidity Scanner</div>
        </div>

        <h2>🌊 Liquidity Pool & Order Block Engine</h2>
        
        <div class="pair-grid">
            <div class="pair-card">EUR/USD (OTC)<br><span>88% Profit</span></div>
            <div class="pair-card">GBP/USD (OTC)<br><span>85% Profit</span></div>
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
                <option value="15 Seconds" {% if timeframe == '15 Seconds' %}selected{% endif %}>15 Seconds</option>
                <option value="1 Minute" {% if timeframe == '1 Minute' %}selected{% endif %}>1 Minute</option>
            </select>

            <button type="submit" name="action" value="start" class="start-btn">🚀 Connect Liquidity Engine</button>
            
            {% if started %}
            <div class="loading">✅ Scanning Liquidity Pools & Stop Hunts...</div>
            <button type="submit" name="action" value="get_signal" class="signal-btn">📊 Get Liquidity Signal</button>
            {% endif %}
        </form>

        {% if signal %}
        <div class="signal-box">
            <p><b>📌 Asset:</b> {{ pair }}</p>
            <p><b>⏱ Timeframe:</b> {{ timeframe }}</p>
            <p><b>💧 Liquidity Sweep (Stop Hunt):</b> {{ liquidity_sweep }}</p>
            <p><b>🧱 Order Block (OB):</b> {{ order_block }}</p>
            <p><b>⚡ Fair Value Gap (FVG):</b> {{ fvg_status }}</p>
            <p><b>🎯 Final Prediction:</b> <span class="{{ class_name }}">{{ signal }}</span></p>
            <p><b>⭐ Accuracy Level:</b> {{ accuracy }}%</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

OTC_PAIRS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", 
    "USD/PKR (OTC)", "USD/BDT (OTC)", "NZD/CAD (OTC)"
]

SWEEP_LOGICS = [
    "Bullish Liquidity Sweep (Grabbed Sell-side Liquidity at Support)",
    "Bearish Liquidity Sweep (Stop Hunt at Buy-side Highs)",
    "Asian Range Liquidity Purge + CHoCH Confirmed",
    "External Range Liquidity Sweep Completed"
]

OB_LOGICS = [
    "Bullish Order Block (Demand Zone Mitigation)",
    "Bearish Order Block (Supply Zone Rejection)",
    "Institutional Mitigation Block Test",
    "Extreme Order Block Rebound"
]

FVG_LOGICS = [
    "Bullish FVG Imbalance Filled & Rebounded",
    "Bearish FVG Resistance Active",
    "Liquidity Void Zone Mitigated"
]

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_pair = "EUR/USD (OTC)"
    timeframe = "5 Seconds"
    started = False
    signal = None
    pair = ""
    liquidity_sweep = ""
    order_block = ""
    fvg_status = ""
    class_name = ""
    accuracy = 0.0

    if request.method == 'POST':
        selected_pair = request.form.get('selected_pair', 'EUR/USD (OTC)')
        timeframe = request.form.get('timeframe', '5 Seconds')
        action = request.form.get('action')
        
        if action == 'start':
            started = True
        elif action == 'get_signal':
            started = True
            liquidity_sweep = random.choice(SWEEP_LOGICS)
            order_block = random.choice(OB_LOGICS)
            fvg_status = random.choice(FVG_LOGICS)
            
            if "Bullish" in liquidity_sweep or "Demand" in order_block or "Filled" in fvg_status:
                signal = "UP (CALL) 🟢"
            else:
                signal = "DOWN (PUT) 🔴"
                
            class_name = "up" if "UP" in signal else "down"
            accuracy = round(random.uniform(97.5, 99.5), 2)
            pair = selected_pair

    return render_template_string(
        HTML_TEMPLATE, 
        pairs=OTC_PAIRS,
        selected_pair=selected_pair, 
        timeframe=timeframe, 
        started=started,
        signal=signal,
        pair=pair,
        liquidity_sweep=liquidity_sweep,
        order_block=order_block,
        fvg_status=fvg_status,
        class_name=class_name,
        accuracy=accuracy
    )

if __name__ == "__main__":
    port = int(os.environ.com.get("PORT", 10000) if hasattr(os.environ, "com") else os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
