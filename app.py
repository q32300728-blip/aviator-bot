from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse

app = FastAPI()

# CORS পলিসি এলাউ করার জন্য এটি যুক্ত করা হয়েছে
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_game_data = "Waiting for data from browser..."

@app.get("/")
async def get():
    return HTMLResponse(f"""
    <html>
        <head>
            <title>Aviator Data Bridge</title>
            <style>
                body {{ background-color: #0e1117; color: #fff; font-family: monospace; padding: 20px; }}
                #logs {{ background: #161b22; padding: 15px; border-radius: 5px; height: 400px; overflow-y: scroll; border: 1px #30363d solid; color: #2ea043; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h2>Live Aviator Stream Data</h2>
            <div id="logs">{latest_game_data}</div>
            <script>
                async function fetchData() {{
                    try {{
                        const response = await fetch('/get-data');
                        const data = await response.text();
                        document.getElementById('logs').innerText = data;
                    }} catch (err) {{
                        console.error("Fetch error:", err);
                    }}
                }}
                setInterval(fetchData, 1000);
            </script>
        </body>
    </html>
    """)

@app.post("/push-data")
async def push_data(payload: dict):
    global latest_game_data
    latest_game_data = str(payload.get("data"))
    return {"status": "success"}

@app.get("/get-data", response_class=PlainTextResponse)
async def get_data():
    return latest_game_data
