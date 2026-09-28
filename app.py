<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Live Multiplier & Round Telemetry</title>
  <style>
    :root {
      --bg: #0b101e;
      --card: #131b2e;
      --border: #253354;
      --cyan: #00e5ff;
      --emerald: #00e676;
      --amber: #ffb300;
      --coral: #ff5252;
      --text: #eaf2ff;
      --muted: #94a3b8;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      padding: 20px;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      display: grid;
      gap: 20px;
    }
    .topbar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px 22px;
      gap: 12px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--amber);
      box-shadow: 0 0 12px var(--amber);
    }
    .dot.online {
      background: var(--emerald);
      box-shadow: 0 0 12px var(--emerald);
    }
    .status-pill {
      font-family: monospace;
      font-size: 0.85rem;
      padding: 6px 12px;
      border-radius: 999px;
      background: rgba(0, 229, 255, 0.12);
      color: var(--cyan);
      border: 1px solid rgba(0, 229, 255, 0.35);
    }
    .hero-stage {
      background: radial-gradient(circle at center, #182442 0%, #101729 100%);
      border: 2px solid var(--border);
      border-radius: 24px;
      padding: 48px 24px;
      text-align: center;
      position: relative;
      overflow: hidden;
      transition: border-color 0.25s ease;
    }
    .hero-stage.state-STARTING {
      border-color: var(--amber);
    }
    .hero-stage.state-IN_PROGRESS {
      border-color: var(--emerald);
    }
    .hero-stage.state-ENDED {
      border-color: var(--coral);
    }
    .round-badge {
      display: inline-block;
      font-family: monospace;
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 8px 18px;
      border-radius: 999px;
      margin-bottom: 16px;
      background: rgba(255, 255, 255, 0.07);
    }
    .multiplier-display {
      font-size: clamp(4.5rem, 14vw, 9rem);
      font-weight: 900;
      line-height: 1;
      letter-spacing: -0.03em;
      font-variant-numeric: tabular-nums;
      color: var(--cyan);
      text-shadow: 0 0 40px rgba(0, 229, 255, 0.35);
      margin: 12px 0;
    }
    .state-IN_PROGRESS .multiplier-display {
      color: var(--emerald);
      text-shadow: 0 0 45px rgba(0, 230, 118, 0.45);
    }
    .state-ENDED .multiplier-display {
      color: var(--coral);
      text-shadow: 0 0 45px rgba(255, 82, 82, 0.45);
    }
    .sub-metrics {
      display: flex;
      justify-content: center;
      gap: 28px;
      margin-top: 18px;
      color: var(--muted);
      font-family: monospace;
      font-size: 0.95rem;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }
    .panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
    }
    .panel h3 {
      font-size: 1rem;
      margin-bottom: 14px;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .history-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .chip {
      font-family: monospace;
      font-weight: 700;
      font-size: 0.9rem;
      padding: 6px 12px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
    }
    .frame-log {
      font-family: monospace;
      font-size: 0.78rem;
      max-height: 240px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .frame-item {
      padding: 6px 10px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 8px;
      word-break: break-all;
      color: #cbd5e1;
    }
    .frame-time {
      color: var(--cyan);
      margin-right: 8px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="topbar">
      <div class="brand">
        <div id="connDot" class="dot"></div>
        <div>
          <h2 style="font-size: 1.15rem;">Live WebSocket Telemetry</h2>
          <p id="updatedAt" style="font-size: 0.8rem; color: var(--muted);">Waiting for stream...</p>
        </div>
      </div>
      <div id="connStatus" class="status-pill">INITIALIZING</div>
    </div>

    <div id="heroStage" class="hero-stage state-WAITING">
      <div id="roundStateBadge" class="round-badge">WAITING FOR NEXT ROUND</div>
      <div id="multiplierValue" class="multiplier-display">1.00x</div>
      <div class="sub-metrics">
        <span>ROUND ID: <strong id="roundId" style="color: var(--text);">--</strong></span>
        <span>LAST CRASH: <strong id="lastCrash" style="color: var(--coral);">0.00x</strong></span>
      </div>
    </div>

    <div class="grid-2">
      <div class="panel">
        <h3>Recent Round Multipliers</h3>
        <div id="historyList" class="history-chips">
          <span style="color: var(--muted); font-size: 0.9rem;">No completed rounds recorded yet.</span>
        </div>
      </div>

      <div class="panel">
        <h3>Incoming WebSocket Frames</h3>
        <div id="frameLog" class="frame-log"></div>
      </div>
    </div>
  </div>

  <script>
    const connDot = document.getElementById("connDot");
    const connStatus = document.getElementById("connStatus");
    const updatedAt = document.getElementById("updatedAt");
    const heroStage = document.getElementById("heroStage");
    const roundStateBadge = document.getElementById("roundStateBadge");
    const multiplierValue = document.getElementById("multiplierValue");
    const roundId = document.getElementById("roundId");
    const lastCrash = document.getElementById("lastCrash");
    const historyList = document.getElementById("historyList");
    const frameLog = document.getElementById("frameLog");

    function renderState(data) {
      connDot.className = data.connected ? "dot online" : "dot";
      connStatus.textContent = data.connection_status;
      updatedAt.textContent = "Last packet UTC: " + data.updated_at;

      heroStage.className = "hero-stage state-" + data.round_state;
      roundStateBadge.textContent = "ROUND STATE: " + data.round_state;
      multiplierValue.textContent = data.current_multiplier + "x";
      roundId.textContent = data.round_id;
      lastCrash.textContent = data.last_crash_multiplier + "x";

      if (data.history && data.history.length > 0) {
        historyList.innerHTML = data.history
          .map(item => `<span class="chip" title="Round ${item.round} at ${item.time}">${item.multiplier}</span>`)
          .join("");
      }

      if (data.recent_frames && data.recent_frames.length > 0) {
        frameLog.innerHTML = data.recent_frames
          .map(f => `<div class="frame-item"><span class="frame-time">[${f.time}]</span>${f.frame}</div>`)
          .join("");
      }
    }

    function connectDashboardWs() {
      const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
      const ws = new WebSocket(`${proto}//${window.location.host}/ws/live`);

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          renderState(data);
        } catch (e) {}
      };

      ws.onclose = () => {
        connStatus.textContent = "DASHBOARD RECONNECTING...";
        setTimeout(connectDashboardWs, 2000);
      };
    }

    connectDashboardWs();
  </script>
</body>
</html>
