from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse("""
    <html>
        <head>
            <title>Raw Data Monitor</title>
            <style>
                body { background-color: #0e1117; color: #fff; font-family: monospace; padding: 20px; }
                #logs { background: #161b22; padding: 15px; border-radius: 5px; height: 400px; overflow-y: scroll; border: 1px #30363d solid; }
            </style>
        </head>
        <body>
            <h2>Live Raw Data Stream Monitor</h2>
            <div id="logs">Connecting to stream...</div>
            <script>
                const ws = new WebSocket("wss://" + window.location.host + "/ws");
                const logs = document.getElementById('logs');
                
                ws.onopen = function() {
                    logs.innerHTML += "<p style='color: #2ea043;'>[Connected] WebSocket connection established.</p>";
                };
                
                ws.onmessage = function(event) {
                    logs.innerHTML += "<p>Received -> " + event.data + "</p>";
                    logs.scrollTop = logs.scrollHeight;
                };
                
                ws.onclose = function() {
                    logs.innerHTML += "<p style='color: #f85149;'>[Disconnected] Connection closed.</p>";
                };
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo/Raw: {data}")
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
