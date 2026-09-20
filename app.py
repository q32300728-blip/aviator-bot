import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম ট্রেডিং টার্মিনাল স্টাইল কনফিগারেশন
st.set_page_config(page_title="Pro Elite OTC AI Trading Terminal", layout="wide", page_icon="📈")

# কাস্টম CSS দিয়ে বড় ডিসপ্লে সিগন্যাল, ডার্ক মোড এবং আকর্ষণীয় লুক তৈরি করা হলো
st.markdown("""
    <style>
    .main { background-color: #07090e; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #00ffa3, #00b09b); color: #07090e; font-weight: bold; border-radius: 8px; height: 3.8em; font-size: 18px; border: none; }
    .stButton>button:hover { background: linear-gradient(135deg, #00cc82, #008f7a); color: #ffffff; }
    
    /* বড় ডিসপ্লে সিগন্যাল স্টাইল */
    .signal-up { background: linear-gradient(135deg, #00b09b, #96c93d); color: white; padding: 35px; border-radius: 15px; text-align: center; font-size: 50px; font-weight: bold; box-shadow: 0px 6px 30px rgba(0, 176, 155, 0.6); margin-bottom: 25px; text-transform: uppercase; letter-spacing: 3px; border: 2px solid #ffffff33; }
    .signal-down { background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; padding: 35px; border-radius: 15px; text-align: center; font-size: 50px; font-weight: bold; box-shadow: 0px 6px 30px rgba(255, 65, 108, 0.6); margin-bottom: 25px; text-transform: uppercase; letter-spacing: 3px; border: 2px solid #ffffff33; }
    
    .analysis-card { background-color: #121824; padding: 25px; border-radius: 12px; border: 1px solid #1f2a3d; margin-top: 15px; font-size: 16px; line-height: 1.7; color: #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# রেন্ডার এনভায়রনমেন্ট থেকে নিরাপদে API Key লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not found. Please set it in your Render dashboard under Environment Variables.")
else:
    genai.configure(api_key=api_key)

# দ্রুত রেসপন্সের জন্য ফ্ল্যাশ মডেল ব্যবহার
model = genai.GenerativeModel('gemini-1.5-flash')

# হেডার সেকশন
st.title("⚡ Pro Elite OTC AI Trading Terminal & Smart Trap Detector")
st.markdown("---")

# সাইডবার কন্ট্রোলস
with st.sidebar:
    st.header("⚙️ প্রফেশনাল সেটিংস")
    market_name = st.selectbox("OTC মার্কেট সিলেক্ট করুন:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "Crypto IDX (OTC)", "AUD/CAD (OTC)", "অন্যান্য OTC Market"])
    st.markdown("---")
    st.info("💡 টিপস: ওটিসি মার্কেটের ১-মিনিটের ক্যান্ডেলস্টিক চার্টের পরিষ্কার স্ক্রিনশট আপলোড করে নিচের বাটনে ক্লিক করুন।")

# ফাইল আপলোড অপশন
uploaded_file = st.file_uploader(f"📷 {market_name} এর লাইভ চার্ট বা স্ক্রিনশট আপলোড করুন (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Live Chart: {market_name}', use_container_width=True)
    
    with col2:
        st.subheader("📊 প্রো-ট্রেডার এআই ডিশন প্যানেল")
        
        system_prompt = f"""
        Act as an elite, world-class OTC Market Algorithmic Trader, Price Action Master, and Smart Money Concepts (SMC) Expert. Analyze this 1-minute OTC chart for {market_name} with extreme precision like a professional high-level trader. 
        
        Consider OTC specific algorithms, fakeouts, trap candles, liquidity sweeps, and broker manipulation patterns.
        
        You must strictly evaluate and provide your expert response in Bengali, structured precisely under these headings:
        1. **চূড়ান্ত সিগন্যাল (Final Signal):** Clearly write "UP (CALL)" or "DOWN (PUT)" right at the top in big text.
        2. **মারকেট কাদের আয়ত্তে আছে (Market Dominance):** Analyze whether Buyers (Bulls) or Sellers (Bears) have the ultimate control and strength percentage right now.
        3. **ওটিসি ট্র্যাপ ও ফেকআউট ডিটেকশন (OTC Trap & Fakeout Detection):** Identify if there are any trap candles, liquidity grabs, or broker manipulation zones currently active.
        4. **প্রাইস পয়েন্ট ও লেভেল (Price Points & HH/LL):** Mention exact key price points, Higher Highs (HH), and Lower Lows (LL).
        5. **সাপোর্ট ও রেজিস্টেন্স (Support & Resistance):** Immediate strong micro and macro support/resistance zones.
        6. **ইন্ডিকেটর ও ভলিউম বিহেভিয়ার (Indicator & Volume Behavior):** Momentum and volume assessment.
        7. **ক্যান্ডেল প্রেডিকশন ও মাস্টার স্ট্র্যাটেজি (Candle Prediction & Master Strategy):** Predict the exact direction of the upcoming candle with precise entry strategy and risk management.
        """
        
        if st.button("🚀 তাৎক্ষণিক প্রো-লেভেল অ্যানালাইসিস শুরু করুন"):
            with st.spinner("⚡ ওটিসি অ্যালগরিদম, ট্র্যাপ ও ক্যান্ডেল প্যাটার্ন স্ক্যান করা হচ্ছে..."):
                try:
                    start_time = time.time()
                    response = model.generate_content([system_prompt, image])
                    end_time = time.time()
                    speed_taken = round(end_time - start_time, 2)
                    
                    result_text = response.text
                    
                    # এআই রেসপন্স চেক করে বড় ডিসপ্লে সিগন্যাল রেন্ডার করা
                    if "DOWN" in result_text.upper() or "PUT" in result_text.upper():
                        st.markdown('<div class="signal-down">🔴 DOWN / PUT SIGNAL</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="signal-up">🟢 UP / CALL SIGNAL</div>', unsafe_allow_html=True)
                    
                    st.caption(f"⏱️ এনালাইসিস সফল! সময় লেগেছে: {speed_taken} সেকেন্ড | মার্কেট: {market_name}")
                    
                    # বিস্তারিত প্রফেশনাল অ্যানালাইসিস কার্ড
                    st.markdown(f"""
                    <div class="analysis-card">
                        {result_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"⚠️ ত্রুটি ঘটেছে: {e}")
