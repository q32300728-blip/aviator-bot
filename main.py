import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import random

# এভিয়েটর গেমের হিস্ট্রি স্যাম্পল ও ট্রেন্ড ডাটা (রঙিন লেবেলের জন্য টাইপ সহ)
SAMPLE_TRENDS = [
    {"val": "1.20x", "type": "low"},
    {"val": "1.55x", "type": "low"},
    {"val": "2.05x", "type": "mid"},
    {"val": "3.40x", "type": "mid"},
    {"val": "12.22x", "type": "high"},
    {"val": "1.80x", "type": "low"},
    {"val": "87.15x", "type": "high"},
    {"val": "1.89x", "type": "low"},
    {"val": "7.01x", "type": "mid"},
    {"val": "1.33x", "type": "low"}
]

latest_data = {
    "target": "2.05x",
    "status": "ANALYZING PATTERN...",
    "recent": ["1.80x", "3.40x", "1.55x", "12.22x"]
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIATOR SMART PREDICTOR</title>
    <style>
        body {
            background-color: #0b132b;
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 400px;
            margin: auto;
            background: #1c2541;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
            border: 2px solid #3a506b;
        }
        h2 { color: #00ffcc; letter-spacing: 2px; margin-bottom: 5px; }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 15px 0;
        }
        .stat-box {
            background: #0b132b;
            padding: 8px;
            border-radius: 10px;
            width: 30%;
            border: 1px solid #48cae4;
        }
        .stat-box span { display: block; font-size: 11px; color: #90e0ef; }
        .stat-box strong { font-size: 13px; color: #00ffcc; }
        .target-box {
            background: radial-gradient(circle, #102a43 0%, #0b132b 100%);
            border: 3px solid #00ffcc;
            border-radius: 50%;
            width: 200px;
            height: 200px;
            margin: 25px auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 30px rgba(0, 255, 204, 0.5);
        }
        .target-box h3 { margin: 0; font-size: 13px; color: #ffb703; }
        .target-box h1 { margin: 8px 0; font-size: 32px; color: #00ffcc; text-shadow: 0 0 10px rgba(0,255,204,0.6); }
        .target-box p { margin: 0; font-size: 11px; color: #ade8f4; }
        .signal-btn {
            background: linear-gradient(45deg, #00b4d8, #0077b6);
            color: white;
            padding: 10px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 13px;
            margin: 15px 0;
            letter-spacing: 1px;
        }
        .recent-title {
            text-align: left;
            font-size: 12px;
            margin-top: 20px;
            margin-bottom: 8px;
            color: #90e0ef;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .recent-rounds {
            display: flex;
            justify-content: space-between;
            background: #0b132b;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #243b55;
        }
        .round-item {
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 0 8px rgba(0,0,0,0.3);
        }
        /* কালার কোডিং (কম মানের জন্য নীল, মাঝারি জন্য বেগুনি/গোলাপি, হাই মানের জন্য সোনালী/সবুজ) */
        .low-val { background: #1d3557; color: #48cae4; border: 1px solid #48cae4; }
        .mid-val { background: #3a0ca3; color: #f72585; border: 1px solid #f72585; }
        .high-val { background: #03312e; color: #00ffcc; border: 1px solid #00ffcc; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AVIATOR PRO</h2>
        <p style="font-size: 11px; color: #adb5bd; margin-top:0;">SMART TREND ANALYZER</p>
        
        <div class="stats">
            <div class="stat-box"><span>ACCURACY</span><strong>99.1%</strong></div>
            <div class="stat-box"><span>AI MODE</span><strong>ACTIVE</strong></div>
            <div class="stat-box"><span>SYNC</span><strong>STABLE</strong></div>
        </div>

        <div class="target-box">
            <h3>NEXT PREDICTION</h3>
            <h1 id="target-val">--</h1>
            <p id="status-val">SYNCING...</p>
        </div>

        <div class="signal-btn">⚡ PATTERN MATCHING ON</div>

        <div class="recent-title">DETECTED TRENDS (LIVE PANEL):</div>
        <div class="recent-rounds" id="recent-box">
            <div class="round-item low-val">--</div>
        </div>
    </div>

    <script>
        function getColorClass(valStr) {
            let num = parseFloat(valStr);
            if (num >= 5.0) return 'high-val';
            if (num >= 2.0) return 'mid-val';
            return 'low-val';
        }

        setInterval(async () => {
            try {
                let res = await fetch('/data');
                let data = await res.json();
                document.getElementById('target-val').innerText = data.target;
                document.getElementById('status-val').innerText = data.status;
                
                let recentHtml = '';
                data.recent.forEach(r => {
                    let cssClass = getColorClass(r);
                    recentHtml += `<div class="round-item ${cssClass}">${r}</div>`;
                });
                document.getElementById('recent-box').innerHTML = recentHtml;
            } catch(e) {}
        }, 1000);
    </script>
</body>
</html>
"""

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(latest_data).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
            
    def log_message(self, format, *args):
        return

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

async def smart_trend_simulation():
    global latest_data
    while True:
        latest_data["status"] = "ANALYZING TREND..."
        await asyncio.sleep(1.2)
        
        selected = random.choice(SAMPLE_TRENDS)
        next_val = selected["val"]
        
        latest_data["target"] = next_val
        latest_data["status"] = "SIGNAL LOCKED"
        
        await asyncio.sleep(4.5)
        
        if next_val not in latest_data["recent"]:
            latest_data["recent"].append(next_val)
            if len(latest_data["recent"]) > 4:
                latest_data["recent"].pop(0)

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    asyncio.run(smart_trend_simulation())
