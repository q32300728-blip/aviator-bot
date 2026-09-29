import asyncio
import json
import os
import random
import re
import socket
import ssl
import threading
import time
import urllib.request
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Set

import uvicorn
import websocket
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# ==============================================================================
# 1. Encrypted DNS-over-HTTPS (DoH) Resolver Fallback (For 24/7 Stability)
# ==============================================================================
_orig_getaddrinfo = socket.getaddrinfo
_doh_cache = {}
_doh_ssl_ctx = ssl.create_default_context()
_doh_ssl_ctx.check_hostname = False
_doh_ssl_ctx.verify_mode = ssl.CERT_NONE


def resolve_via_doh(host: str):
    if host in _doh_cache:
        return _doh_cache[host]

    endpoints = [
        f"https://1.1.1.1/dns-query?name={host}&type=A",
        f"https://8.8.8.8/resolve?name={host}&type=A",
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/dns-json",
                    "User-Agent": "Mozilla/5.0",
                },
            )
            with urllib.request.urlopen(req, timeout=5, context=_doh_ssl_ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for ans in data.get("Answer", []):
                    if ans.get("type") == 1 and ans.get("data"):
                        ip = ans["data"]
                        _doh_cache[host] = ip
                        print(f"[DoH Resolved] {host} -> {ip}", flush=True)
                        return ip
        except Exception:
            pass
    return None


def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return _orig_getaddrinfo(host, port, family, type, proto, flags)
    except socket.gaierror:
        ip = resolve_via_doh(host)
        if ip:
            return _orig_getaddrinfo(ip, port, family, type, proto, flags)
        raise


socket.getaddrinfo = patched_getaddrinfo

# ==============================================================================
# 2. Target Endpoint & Production Headers Configuration
# ==============================================================================
TARGET_WS_URL = os.getenv(
    "TARGET_WS_URL",
    "wss://a3jissau.ossjs3.com/ws/websocket?socketauthstr=2850-314182e8b6dd7daea451790048165987074216",
)

HEADERS = [
    "User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Origin: https://aviator-next.spribeegaming.com",
    "Accept-Language: en-US,en;q=0.9",
    "Cache-Control: no-cache",
    "Pragma: no-cache",
]

app = FastAPI(title="Aviator Production Bot Dashboard")
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir)) if templates_dir.exists() else None


# ==============================================================================
# 3. State Management Engine (Memory Optimized)
# ==============================================================================
class LiveTelemetryState:
    def __init__(self):
        self.connected: bool = False
        self.connection_status: str = "INITIALIZING"
        self.round_state: str = "WAITING"  # STARTING | IN_PROGRESS | ENDED | WAITING
        self.round_id: str = "--"
        self.current_multiplier: float = 1.00
        self.last_crash_multiplier: float = 0.00
        self.history: deque = deque(maxlen=50)
        self.recent_frames: deque = deque(maxlen=30)
        self.updated_at: str = "--"

    def snapshot(self) -> dict:
        return {
            "connected": self.connected,
            "connection_status": self.connection_status,
            "round_state": self.round_state,
            "round_id": self.round_id,
            "current_multiplier": f"{self.current_multiplier:.2f}",
            "last_crash_multiplier": f"{self.last_crash_multiplier:.2f}",
            "history": list(self.history),
            "recent_frames": list(self.recent_frames),
            "updated_at": self.updated_at,
        }


state = LiveTelemetryState()
dashboard_clients: Set[WebSocket] = set()
main_loop: asyncio.AbstractEventLoop = None


def trigger_broadcast():
    if main_loop and main_loop.is_running():
        asyncio.run_coroutine_threadsafe(broadcast_to_browsers(), main_loop)


async def broadcast_to_browsers():
    if not dashboard_clients:
        return
    payload = json.dumps(state.snapshot())
    disconnected = []
    for ws in list(dashboard_clients):
        try:
            await ws.send_text(payload)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        dashboard_clients.discard(ws)


def parse_round_payload(obj):
    now_str = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
    state.updated_at = now_str

    if isinstance(obj, dict):
        r_id = obj.get("roundId") or obj.get("round_id") or obj.get("gameId") or obj.get("id")
        if r_id is not None and str(r_id).strip():
            state.round_id = str(r_id)

        stage = str(
            obj.get("stage")
            or obj.get("state")
            or obj.get("status")
            or obj.get("cmd")
            or obj.get("c")
            or obj.get("event")
            or ""
        ).lower()

        mult_val = (
            obj.get("multiplier")
            or obj.get("coeff")
            or obj.get("x")
            or obj.get("rate")
            or obj.get("currentMultiplier")
            or obj.get("crash")
            or obj.get("maxMultiplier")
            or obj.get("endCoeff")
        )

        if any(k in stage for k in ("start", "wait", "bet", "init", "new", "prepare")):
            state.round_state = "STARTING"
            state.current_multiplier = 1.00

        elif any(k in stage for k in ("end", "crash", "flew", "finish", "stop", "result")):
            state.round_state = "ENDED"
            if mult_val is not None:
                try:
                    val = float(mult_val)
                    state.current_multiplier = val
                    state.last_crash_multiplier = val
                    state.history.appendleft(
                        {
                            "round": state.round_id,
                            "multiplier": f"{val:.2f}x",
                            "time": now_str,
                        }
                    )
                except ValueError:
                    pass
            else:
                state.last_crash_multiplier = state.current_multiplier
                state.history.appendleft(
                    {
                        "round": state.round_id,
                        "multiplier": f"{state.current_multiplier:.2f}x",
                        "time": now_str,
                    }
                )

        elif mult_val is not None:
            try:
                val = float(mult_val)
                state.current_multiplier = val
                state.round_state = "IN_PROGRESS"
            except ValueError:
                pass

        for v in obj.values():
            if isinstance(v, (dict, list)):
                parse_round_payload(v)

    elif isinstance(obj, list):
        for item in obj:
            parse_round_payload(item)


def process_incoming_frame(raw_message: str):
    text = raw_message.strip()
    now_str = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
    state.updated_at = now_str
    state.recent_frames.appendleft({"time": now_str, "frame": text[:250]})

    if text == "o":
        state.connection_status = "SOCKJS_OPEN"
    elif text == "h" or "ping" in text:
        state.connection_status = "LIVE_HEARTBEAT"
    elif text.startswith("a["):
        try:
            outer_list = json.loads(text[1:])
            for entry in outer_list:
                parsed = json.loads(entry) if isinstance(entry, str) else entry
                parse_round_payload(parsed)
        except Exception:
            pass
    else:
        try:
            parsed = json.loads(text)
            parse_round_payload(parsed)
        except Exception:
            match = re.search(r"\b(\d+\.\d{2})\b", text)
            if match:
                state.current_multiplier = float(match.group(1))
                state.round_state = "IN_PROGRESS"

    trigger_broadcast()


# ==============================================================================
# 4. Resilient Upstream WebSocket Worker with Jittered Backoff
# ==============================================================================
def upstream_websocket_worker():
    backoff = 2.0
    max_backoff = 30.0

    while True:
        state.connection_status = "CONNECTING"
        trigger_broadcast()

        def on_open(ws):
            nonlocal backoff
            backoff = 2.0
            state.connected = True
            state.connection_status = "LIVE_CONNECTED"
            print("[Upstream] Successfully connected to live stream.", flush=True)
            trigger_broadcast()

        def on_message(ws, message):
            process_incoming_frame(message)

        def on_error(ws, error):
            state.connected = False
            state.connection_status = f"ERROR: {type(error).__name__}"
            print(f"[Upstream Error] {error}", flush=True)
            trigger_broadcast()

        def on_close(ws, close_status_code, close_msg):
            state.connected = False
            state.connection_status = f"CLOSED ({close_status_code})"
            print(f"[Upstream Closed] code={close_status_code} msg={close_msg}", flush=True)
            trigger_broadcast()

        try:
            ws_app = websocket.WebSocketApp(
                TARGET_WS_URL,
                header=HEADERS,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            )
            ws_app.run_forever(
                ping_interval=15,
                ping_timeout=10,
                sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False},
                skip_utf8_validation=True,
            )
        except Exception as exc:
            state.connected = False
            state.connection_status = f"EXCEPTION: {exc}"
            trigger_broadcast()

        jitter = random.uniform(0.5, 2.0)
        wait_seconds = min(max_backoff, backoff + jitter)
        state.connection_status = f"RECONNECTING IN {wait_seconds:.1f}s"
        trigger_broadcast()
        time.sleep(wait_seconds)
        backoff = min(max_backoff, backoff * 1.5)


@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()
    worker = threading.Thread(target=upstream_websocket_worker, daemon=True)
    worker.start()


@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    if templates and (templates_dir / "index.html").exists():
        return templates.TemplateResponse("index.html", {"request": request})
    return HTMLResponse("<h3>Aviator Bot Running. Use /api/state for JSON telemetry.</h3>")


@app.get("/api/state")
async def api_state():
    return state.snapshot()


@app.websocket("/ws/live")
async def dashboard_websocket(ws: WebSocket):
    await ws.accept()
    dashboard_clients.add(ws)
    try:
        await ws.send_text(json.dumps(state.snapshot()))
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        dashboard_clients.discard(ws)
    except Exception:
        dashboard_clients.discard(ws)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
