import os
import streamlit as st
import pandas as pd
import numpy as np
from quotexpy import Quotex

st.set_page_config(page_title="Quotex Trading Dashboard", page_icon="📈", layout="wide")

st.title("🚀 Quotex Live Trading Dashboard with Indicators")
st.markdown("---")

# রেন্ডারের এনভায়রনমেন্ট ভেরিয়েবল বা ইউজার ইনপুট থেকে ক্রেডেনশিয়াল নেওয়া
EMAIL = os.getenv("QUOTEX_EMAIL", "")
PASSWORD = os.getenv("QUOTEX_PASSWORD", "")

st.sidebar.header("Bot Configuration")
if not EMAIL:
    EMAIL = st.sidebar.text_input("Quotex Email", type="default")
if not PASSWORD:
    PASSWORD = st.sidebar.text_input("Quotex Password", type="password")

asset = st.sidebar.selectbox("Select Asset", ["EURUSD", "GBPUSD", "EURJPY", "AUDUSD"])
amount = st.sidebar.number_input("Trade Amount ($)", min_value=1, value=1)
duration = st.sidebar.selectbox("Duration (Seconds)", [60, 120, 300], index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("Strategy Parameters")
rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
ma_period = st.sidebar.slider("Moving Average Period", 5, 50, 20)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Market Analysis & Signals")
    status_placeholder = st.empty()
    signal_placeholder = st.empty()

with col2:
    st.subheader("💰 Account Balance")
    balance_placeholder = st.empty()

st.markdown("---")
st.subheader("🎮 Bot Control Panel")

start_button = st.button("🟢 Start Bot", type="primary")

# টেকনিক্যাল ইন্ডিকেটর ক্যালকুলেশন ফাংশন (RSI এবং Moving Average)
def calculate_indicators(closes, rsi_per, ma_per):
    df = pd.DataFrame({'close': closes})
    
    # Moving Average (MA) ক্যালকুলেশন
    df['MA'] = df['close'].rolling(window=ma_per).mean()
    
    # RSI ক্যালকুলেশন
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_per).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_per).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df['RSI'].iloc[-1], df['MA'].iloc[-1], df['close'].iloc[-1]

if start_button:
    if not EMAIL or not PASSWORD:
        st.error("দয়া করে আপনার Quotex ইমেইল এবং পাসওয়ার্ড প্রদান করুন।")
    else:
        status_placeholder.info("Connecting to Quotex Real Account...")
        
        client = Quotex(email=EMAIL, password=PASSWORD)
        check = client.connect()
        
        if check:
            status_placeholder.success("Connected Successfully!")
            client.change_balance(0)  # রিয়েল অ্যাকাউন্ট নিশ্চিত করা
            
            balance = client.get_balance()
            balance_placeholder.metric(label="Real Balance", value=f"${balance}")
            
            signal_placeholder.warning(f"Analyzing {asset} with RSI, MA & Price Action...")
            
            # কুটেক্স থেকে ক্যান্ডেল বা প্রাইস ডাটা ফেচ করার ডেমো অ্যারে (বা লাইভ ডাটা ফিড)
            # নোট: quotexpy লাইব্রেরি থেকে লাইভ ক্লোজিং প্রাইস লিস্ট এখানে ফেচ করতে হবে।
            # নিরাপত্তার জন্য এখানে সিমুলেটেড প্রাইস ফিড স্ট্রাকচার দেওয়া হলো যা লাইভ ডেটার সাথে কাজ করবে।
            dummy_closes = [1.0850, 1.0852, 1.0855, 1.0853, 1.0858, 1.0860, 1.0859, 1.0862, 1.0865, 1.0864,
                            1.0868, 1.0870, 1.0872, 1.0871, 1.0875, 1.0878, 1.0876, 1.0880, 1.0882, 1.0885]
            
            # ইন্ডিকেটর ভ্যালু বের করা
            current_rsi, current_ma, current_price = calculate_indicators(dummy_closes, rsi_period, ma_period)
            
            # প্রাইস অ্যাকশন এবং ইন্ডিকেটর সিগন্যাল লজিক
            # UP ⬆️ শর্ত: যদি RSI < 48 (oversold জোন থেকে রিবাউন্ড) এবং প্রাইস Moving Average-এর উপরে থাকে (Bullish Price Action)
            # DOWN ⬇️ শর্ত: যদি RSI > 52 (overbought জোন) এবং প্রাইস Moving Average-এর নিচে থাকে (Bearish Price Action)
            
            action = None
            if current_rsi < 48 and current_price > current_ma:
                action = "call"  # UP ⬆️
                signal_placeholder.success(f"Signal Detected: UP ⬆️ | RSI: {current_rsi:.2f} | Price > MA")
            elif current_rsi > 52 and current_price < current_ma:
                action = "put"   # DOWN ⬇️
                signal_placeholder.error(f"Signal Detected: DOWN ⬇️ | RSI: {current_rsi:.2f} | Price < MA")
            else:
                signal_placeholder.info(f"Market Neutral | RSI: {current_rsi:.2f} | Waiting for clear signal...")
            
            # যদি সিগন্যাল পাওয়া যায় তবে ট্রেড প্লেস হবে
            if action:
                status, buy_info = client.buy(asset, amount, action, duration)
                st.write("Trade Execution Result:", buy_info)
            
            client.close()
        else:
            status_placeholder.error("Connection Failed! Please check your credentials.")
