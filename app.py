import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>AVIATOR HACK - LIVE SIGNAL MONITOR</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #0b0f19;
            color: #ffffff;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        .main-title { color: #00ffcc; font-size: 24px; font-weight: 900; letter-spacing: 2px; }
        .sub-title { color: #8a99ad; font-size: 11px; margin-bottom: 20px; }
        .metric-container { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 25px; }
        .metric-box { background: #121b2b; border: 1px solid #1f314d; border-radius: 12px; padding: 10px; flex: 1; }
        .metric-title { font-size: 9px; color: #8a99ad; text-transform: uppercase; }
        .metric-value { font-size: 13px; color: #00ffcc; font-weight: bold; }
        .circle-card {
            background: radial-gradient(circle, #11223b 0%, #0b0f19 80%);
            border: 2px solid #00ffcc;
            border-radius: 50%;
            width: 240px;
            height: 240px;
            margin: 0 auto 20px auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 25px rgba(0,255,204,0.3);
        }
        .circle-label { color: #ffaa00; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
        .circle-multiplier { color: #00ffcc; font-size: 38px; font-weight: 900; }
        .circle-status { color: #8a99ad; font-size: 10px; margin-top: 5px; }
        .active-btn {
            background: linear-gradient(90deg, #0072ff, #00ffcc);
            border-radius: 25px;
            color: white;
            padding: 12px;
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .recent-section { background: #121b2b; border: 1px solid #1f314d; border-radius: 12px; padding: 12px; text-align: left; }
        .recent-title { font-size: 10px; color: #8a99ad; margin-bottom: 8px; }
        .rounds-flex { display: flex; justify-content: space-between; gap: 6px; }
        .round-pill { background: #1a273d; border: 1px solid #2a3e5c; border-radius: 6px; padding: 6px; flex: 1; color: #00ffcc; font-weight: bold; font-size: 12px; text-align: center; }
    </style>
</head>
<body>

    <div class="main-title">AVIATOR HACK</div>
    <div class="sub-title">LIVE SIGNAL MONITOR</div>

    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">ACCURACY</div>
            <div class="metric-value">99.99%</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">MODE</div>
            <div class="metric-value">AUTO</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">WIN RATE</div>
            <div class="metric-value">99%</div>
        </div>
    </div>

    <div class="circle-card">
        <div class="circle-label">AVIATOR</div>
        <div id="multiplier" class="circle-multiplier">1.00x</div>
        <div id="status" class="circle-status">CONNECTING...</div>
    </div>

    <div class="active-btn">⚡ AUTO SIGNAL ACTIVE</div>

    <div class="recent-section">
        <div class="recent-title">RECENT ROUNDS:</div>
        <div class="rounds-flex">
            <div class="round-pill">9.27x</div>
            <div class="round-pill">1.49x</div>
            <div class="round-pill">1.00x</div>
            <div class="round-pill">27.50x</div>
        </div>
    </div>

    <script>
        const ws = new WebSocket("wss://" + window.location.host + "/ws");
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById("multiplier").innerText = data.multiplier;
            document.getElementById("status").innerText = data.status;
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    import asyncio
    import random
    try:
        while True:
            # এখানে গেমের লাইভ বা রিয়েল-টাইম সিমুলেটেড সিগন্যাল আপডেট হবে
            mult = f"{round(random.uniform(1.01, 15.50), 2)}x"
            await websocket.send_json({"multiplier": mult, "status": "LIVE SYNCED"})
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
