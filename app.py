import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম ট্রেডিং টার্মিনাল স্টাইল কনফিগারেশন
st.set_page_config(page_title="Pro Elite OTC AI Trading Terminal", layout="wide", page_icon="📈")

# কাস্টম CSS দিয়ে বড় ডিসপ্লে সিগন্যাল এবং প্রিমিয়াম লুক
st.markdown("""
    <style>
    .main { background-color: #07090e; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #00ffa3, #00b09b); color: #07090e; font-weight: bold; border-radius: 8px; height: 3.8em; font-size: 18px; border: none; }
    .stButton>button:hover { background: linear-gradient(135deg, #00cc82, #008f7a); color: #ffffff; }
    
    .signal-up { background: linear-gradient(135deg, #00b09b, #96c93d); color: white; padding: 35px; border-radius: 15px; text-align: center; font-size: 50px; font-weight: bold; box-shadow: 0px 6px 30px rgba(0, 176, 155, 0.6); margin-bottom: 25px; text-transform: uppercase; letter-spacing: 3px; border: 2px solid #ffffff33; }
    .signal-down { background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; padding: 35px; border-radius: 15px; text-align: center; font-size: 50px; font-weight: bold; box-shadow: 0px 6px 30px rgba(255, 65, 108, 0.6); margin-bottom: 25px; text-transform: uppercase; letter-spacing: 3px; border: 2px solid #ffffff33; }
    
    .analysis-card { background-color: #121824; padding: 25px; border-radius: 12px; border: 1px solid #1f2a3d; margin-top: 15px; font-size: 16px; line-height: 1.7; color: #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# রেন্ডার এনভায়রনমেন্ট থেকে API Key লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not found in Render Dashboard.")
else:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚡ Pro Elite OTC AI Trading Terminal")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ সেটিংস")
    market_name = st.selectbox("OTC মার্কেট সিলেক্ট করুন:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "Crypto IDX (OTC)", "AUD/CAD (OTC)"])
    st.markdown("---")
    st.info("💡 ১-মিনিটের পরিষ্কার চার্ট আপলোড করে নিচের বাটনে ক্লিক করুন।")

uploaded_file = st.file_uploader(f"📷 {market_name} এর স্ক্রিনশট আপলোড করুন", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Live Chart: {market_name}', use_container_width=True)
    
    with col2:
        st.subheader("📊 এআই সিগন্যাল প্যানেল")
        
        system_prompt = f"""
        Act as an elite OTC Market Algorithmic Trader and Price Action Master. Analyze this 1-minute OTC chart for {market_name}.
        Provide your response strictly in Bengali under these headings:
        1. **চূড়ান্ত সিগন্যাল (Final Signal):** Write "UP (CALL)" or "DOWN (PUT)" right at the top.
        2. **মারকেট কাদের আয়ত্তে আছে (Market Dominance):** Buyers vs Sellers strength.
        3. **ওটিসি ট্র্যাপ ও ফেকআউট (OTC Trap):** Trap or liquidity grab status.
        4. **প্রাইস পয়েন্ট (Price Points & HH/LL):** Key levels.
        5. **সাপোর্ট ও রেজিস্টেন্স (Support & Resistance):** Zones.
        6. **ক্যান্ডেল প্রেডিকশন (Candle Prediction & Strategy):** Direction and entry advice.
        """
        
        if st.button("🚀 এনালাইসিস শুরু করুন"):
            with st.spinner("🔍 এআই চার্ট স্ক্যান করছে, একটু অপেক্ষা করুন..."):
                try:
                    response = model.generate_content([system_prompt, image])
                    result_text = response.text
                    
                    if "DOWN" in result_text.upper() or "PUT" in result_text.upper():
                        st.markdown('<div class="signal-down">🔴 DOWN / PUT SIGNAL</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="signal-up">🟢 UP / CALL SIGNAL</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="analysis-card">
                        {result_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"⚠️ ত্রুটি ঘটেছে: {e}")
