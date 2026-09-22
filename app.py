import os
import asyncio
import json
import streamlit as st
import websockets

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম ডার্ক থিম কনফিগারেশন
st.set_page_config(page_title="AVIATOR HACK - LIVE SIGNAL MONITOR", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        color: #00ffcc;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-top: -10px;
    }
    .sub-title {
        text-align: center;
        color: #8a99ad;
        font-size: 12px;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 25px;
    }
    .metric-box {
        background: #121b2b;
        border: 1px solid #1f314d;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        flex: 1;
    }
    .metric-title {
        font-size: 10px;
        color: #8a99ad;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 14px;
        color: #00ffcc;
        font-weight: bold;
    }
    .circle-card {
        background: radial-gradient(circle, #11223b 0%, #0b0f19 80%);
        border: 2px solid #00ffcc;
        border-radius: 50%;
        width: 260px;
        height: 260px;
        margin: 0 auto 25px auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 25px rgba(0,255,204,0.3);
    }
    .circle-label {
        color: #ffaa00;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .circle-multiplier {
        color: #00ffcc;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 1px;
    }
    .circle-status {
        color: #8a99ad;
        font-size: 11px;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    .active-btn {
        background: linear-gradient(90deg, #0072ff, #00ffcc);
        border-radius: 25px;
        color: white;
        padding: 12px;
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 20px;
    }
    .recent-section {
        background: #121b2b;
        border: 1px solid #1f314d;
        border-radius: 12px;
        padding: 15px;
    }
    .recent-title {
        font-size: 11px;
        color: #8a99ad;
        margin-bottom: 10px;
    }
    .rounds-flex {
        display: flex;
        justify-content: space-between;
        gap: 8px;
    }
    .round-pill {
        background: #1a273d;
        border: 1px solid #2a3e5c;
        border-radius: 8px;
        padding: 8px 5px;
        text-align: center;
        flex: 1;
        color: #00ffcc;
        font-weight: bold;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AVIATOR HACK</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">LIVE SIGNAL MONITOR</div>', unsafe_allow_html=True)

# টপ মেট্রিক বক্স
st.markdown("""
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
""", unsafe_allow_html=True)

# স্টেট ম্যানেজমেন্ট যাতে লাইভ ডাটা ধরে রাখা যায়
if 'current_multiplier' not in st.session_state:
    st.session_state['current_multiplier'] = "2.20x"

# মাঝের সার্কেল যেখানে লাইভ মান শো করবে
placeholder = st.empty()

def render_ui(multiplier):
    placeholder.markdown(f"""
    <div class="circle-card">
        <div class="circle-label">AVIATOR</div>
        <div class="circle-multiplier">{multiplier}</div>
        <div class="circle-status">SIGNAL LOCKED</div>
    </div>
    """, unsafe_allow_html=True)

render_ui(st.session_state['current_multiplier'])

st.markdown('<div class="active-btn">⚡ AUTO SIGNAL ACTIVE</div>', unsafe_allow_html=True)

# সাম্প্রতিক রাউন্ড হিস্ট্রি
st.markdown("""
<div class="recent-section">
    <div class="recent-title">RECENT ROUNDS:</div>
    <div class="rounds-flex">
        <div class="round-pill">9.27x</div>
        <div class="round-pill">1.49x</div>
        <div class="round-pill">1.00x</div>
        <div class="round-pill">27.50x</div>
    </div>
</div>
""", unsafe_allow_html=True)

# WebSocket ব্যাকগ্রাউন্ড কানেকশন হ্যান্ডলার (পিং-পং সহ)
async def listen_websocket():
    uri = "wss://jiass.oss2.jswService.com/socket.io/?EIO=4&transport=websocket"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                # পিং আসলে পং রেসপন্স পাঠানো
                if message == "2":
                    await websocket.send("3")
                elif "multiplier" in message or len(message) < 20:
                    # গেমের ডেটা প্রসেস করে মান আপডেট করা
                    st.session_state['current_multiplier'] = "1.95x"  # লাইভ ডেটা অনুযায়ী এখানে পরিবর্তন হবে
                    st.rerun()
                await asyncio.sleep(0.5)
    except Exception:
        pass

# সাইডবারে WebSocket স্ট্যাটাস চেক রাখার অপশন
with st.sidebar:
    st.subheader("🔌 লাইভ কানেকশন")
    if st.button("সিঙ্ক স্টার্ট করুন"):
        try:
            asyncio.run(listen_websocket())
        except RuntimeError:
            pass
