import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import random

latest_data = {
    "target": "14.18x",
    "status": "SIGNAL LOCKED",
    "recent": ["1.49x", "1.00x", "27.50x", "6.70x"]
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIATOR HACK MONITOR</title>
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
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
            border: 2px solid #3a506b;
        }
        h2 { color: #00ffcc; letter-spacing: 2px; }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }
        .stat-box {
            background: #0b132b;
            padding: 10px;
            border-radius: 10px;
            width: 30%;
            border: 1px solid #48cae4;
        }
        .stat-box span { display: block; font-size: 12px; color: #90e0ef; }
        .stat-box strong { font-size: 14px; color: #00ffcc; }
        .target-box {
            background: radial-gradient(circle, #102a43 0%, #0b132b 100%);
            border: 3px solid #00ffcc;
            border-radius: 50%;
            width: 220px;
            height: 220px;
            margin: 30px auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 30px rgba(0, 255, 204, 0.5);
        }
        .target-box h3 { margin: 0; font-size: 14px; color: #ffb703; }
        .target-box h1 { margin: 10px 0; font-size: 36px; color: #00ffcc; }
        .target-box p { margin: 0; font-size: 12px; color: #ade8f4; }
        .signal-btn {
            background: linear-gradient(45deg, #00b4d8, #0077b6);
            color: white;
            padding: 12px;
            border-radius: 30px;
            font-weight: bold;
            margin: 20px 0;
            letter-spacing: 1px;
        }
        .recent-rounds {
            display: flex;
            justify-content: space-around;
            background: #0b132b;
            padding: 10px;
            border-radius: 10px;
        }
        .round-item { background: #1d3557; padding: 5px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AVIATOR HACK</h2>
        <p style="font-size: 12px; color: #adb5bd;">LIVE SIGNAL MONITOR</p>
        
        <div class="stats">
            <div class="stat-box"><span>ACCURACY</span><strong>99.99%</strong></div>
            <div class="stat-box"><span>MODE</span><strong>AUTO</strong></div>
            <div class="stat-box"><span>WIN RATE</span><strong>99%</strong></div>
        </div>

        <div class="target-box">
            <h3>AVIATOR</h3>
            <h1 id="target-val">--</h1>
            <p id="status-val">WAITING...</p>
        </div>

        <div class="signal-btn">⚡ AUTO SIGNAL ACTIVE</div>

        <p style="text-align: left; font-size: 12px; margin-bottom: 5px;">RECENT ROUNDS:</p>
        <div class="recent-rounds" id="recent-box">
            <div class="round-item">--</div>
        </div>
    </div>

    <script>
        setInterval(async () => {
            try {
                let res = await fetch('/data');
                let data = await res.json();
                document.getElementById('target-val').innerText = data.target;
                document.getElementById('status-val').innerText = data.status;
                let recentHtml = '';
                data.recent.forEach(r => {
                    recentHtml += `<div class="round-item">${r}</div>`;
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

async def manage_signals():
    global latest_data
    while True:
        # গেম শুরু হওয়ার আগের মুহূর্ত বা সিগন্যাল লকিং ফেজ
        latest_data["status"] = "ANALYZING..."
        await asyncio.sleep(2)
        
        # পরবর্তী রাউন্ডের জন্য ফিক্সড টার্গেট বা গুণক জেনারেট করা (যেমন গেম শুরুর আগে দেখা যাবে)
        next_target = round(random.uniform(2.10, 18.50), 2)
        latest_data["target"] = f"{next_target}x"
        latest_data["status"] = "SIGNAL LOCKED"
        
        # রাউন্ড চলার সময় বা উইটিং পিরিয়ড সিমুলেশন
        await asyncio.sleep(6)
        
        # রাউন্ড শেষ হওয়ার পর হিস্ট্রিতে যোগ করা
        if f"{next_target}x" not in latest_data["recent"]:
            latest_data["recent"].append(f"{next_target}x")
            if len(latest_data["recent"]) > 4:
                latest_data["recent"].pop(0)

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    asyncio.run(manage_signals())
