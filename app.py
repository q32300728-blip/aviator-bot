import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম স্টাইল কনফিগারেশন
st.set_page_config(page_title="প্রো এলিট ওটিসি এআই ট্রেডিং টার্মিনাল", layout="wide")

st.markdown("""
<style>
    /* মূল ব্যাকগ্রাউন্ড কালার */
    .stApp {
        background-color: #0b0b9b;
        color: #ffffff;
    }
    
    /* হেডার ও অ্যাকসেন্ট স্টাইল */
    h1, h2, h3 {
        color: #ff416c !important;
        font-family: 'Inter', sans-serif;
    }
    
    .big-signal-up {
        background: linear-gradient(135deg, #00b09b, #96c93d);
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        font-size: 36px;
        font-weight: 900;
        box-shadow: 0 10px 25px rgba(0,176,155,0.4);
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    .big-signal-down {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        font-size: 36px;
        font-weight: 900;
        box-shadow: 0 10px 25px rgba(255,65,108,0.4);
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    .analysis-card {
        background-color: #121824;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1f293d;
        color: #e2e8f0;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ড্যাশবোর্ড বা সিক্রেট থেকে এপিআই কী লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable is missing. Please configure it in Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)

# সঠিক মডেল নেম প্রিফিক্স সহ সেট করা হলো যাতে NotFound এরর না আসে
model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("🚀 প্রো এলিট ওটিসি এআই ট্রেডিং টার্মিনাল")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ ট্রেডিং সেটিংস")
    market_name = st.selectbox("যেকোনো ওটিসি মার্কেট সিলেক্ট করুন:", [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", 
        "EUR/JPY (OTC)", "USD/BDT (OTC)", "Crypto IDX (OTC)"
    ])
    st.markdown("---")
    st.info("💡 ১-মিনিটের ওটিসি চার্টের পরিষ্কার স্ক্রিনশট আপলোড করুন।")

uploaded_file = st.file_uploader(f"মার্কেট [{market_name}] এর ১-মিনিটের চার্ট আপলোড করুন:", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns([1, 2.2])

with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Live Chart", use_container_width=True)

with col2:
    st.subheader("📊 অ্যাডভান্সড এআই সিগন্যাল ও মার্কেট অ্যানালাইসিস")
    
    system_prompt = """
    Act like an Elite OTC Market Algorithmic Trader, Price Action Master, and Binary Options Expert. 
    Analyze this 1-minute OTC chart snapshot strictly. Filter out fake or weak signals, and provide:
    
    1. **চূড়ান্ত ট্রেডিং সিগন্যাল (Final Signal):** Write clearly "UP (CALL)" or "DOWN (PUT)" at the very top.
    2. **মার্কেট কারেন্ট ও অ্যালগরিদম (Market Condition & Active Buyers/Sellers):** Are buyers or sellers in control?
    3. **প্রাইস অ্যাকশন পয়েন্ট ও ওটিসি অ্যালগরিদম (Price Action & OTC Algorithm):** Which OTC manipulation, trap, or area is active?
    4. **সাপ্লাই জোন বা লোয়ার লো (Higher / Lower Low - HH/LL):** Trend structure and swing analysis.
    5. **ক্যান্ডেল রিজেকশন ও স্টিকনেস (Candle Rejection & Wicks):** Rejection analysis and pressure from wicks.
    6. **সাপোর্ট ও রেজিস্ট্যান্স লেভেল (Support & Resistance Zones):** Key psychological or active technical levels.
    7. **১-মিনিট এন্ট্রি গাইডলাইন (1-Minute Entry Advice):** Precise entry instructions for the next candle.
    """
    
    if st.button("⚡ ফাস্ট অ্যানালাইসিস শুরু করুন (২০ সেকেন্ড)"):
        if uploaded_file is not None:
            with st.spinner("এআই ওটিসি চার্ট স্ক্যান করছে, ২০ সেকেন্ডের মধ্যে ফলাফল আসছে..."):
                response = model.generate_content([system_prompt, image])
                result_text = response.text

            # সিগন্যালের ওপর বড় করে সিগন্যাল শো করার ভিজুয়াল লজিক
            if "DOWN" in result_text.upper() or "PUT" in result_text.upper():
                st.markdown('<div class="big-signal-down">🔻 DOWN / PUT SIGNAL (SELL)</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="big-signal-up">🚀 UP / CALL SIGNAL (BUY)</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="analysis-card">
                {result_text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ দয়া করে ১-মিনিটের ওটিসি চার্টের একটি স্ক্রিনশট আপলোড করুন!")
