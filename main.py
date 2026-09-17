import os
import sys
import asyncio
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import random
import time

latest_data = {
    "target": "1.00x",
    "status": "WAITING...",
    "recent": ["9.27x", "1.49x", "1.00x", "27.50x"]
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
            <h1 id="target-val">1.00x</h1>
            <p id="status-val">FLYING...</p>
        </div>

        <div class="signal-btn">⚡ AUTO SIGNAL ACTIVE</div>

        <p style="text-align: left; font-size: 12px; margin-bottom: 5px;">RECENT ROUNDS:</p>
        <div class="recent-rounds" id="recent-box">
            <div class="round-item">9.27x</div>
            <div class="round-item">1.49x</div>
            <div class="round-item">1.00x</div>
            <div class="round-item">27.50x</div>
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
        }, 500);
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

async def simulate_game_flight():
    global latest_data
    while True:
        # নতুন রাউন্ড শুরু
        latest_data["status"] = "FLYING..."
        current_multiplier = 1.00
        target_crash = round(random.uniform(1.20, 12.50), 2)
        
        while current_multiplier < target_crash:
            latest_data["target"] = f"{current_multiplier:.2f}x"
            # গেমের মতো গতি বাড়িয়ে গুণক বাড়াতে থাকা
            if current_multiplier < 2.0:
                current_multiplier += 0.01
                await asyncio.sleep(0.1)
            elif current_multiplier < 5.0:
                current_multiplier += 0.03
                await asyncio.sleep(0.1)
            else:
                current_multiplier += 0.08
                await asyncio.sleep(0.1)
                
        # ফ্লায়িং ক্র্যাশ বা শেষ হওয়া
        latest_data["target"] = f"{target_crash:.2f}x"
        latest_data["status"] = "CRASHED"
        
        # রিসেন্ট রাউন্ডে যোগ করা
        if f"{target_crash:.2f}x" not in latest_data["recent"]:
            latest_data["recent"].append(f"{target_crash:.2f}x")
            if len(latest_data["recent"]) > 4:
                latest_data["recent"].pop(0)
                
        await asyncio.sleep(3) # পরবর্তী রাউন্ডের জন্য বিরতি

if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    asyncio.run(simulate_game_flight())
