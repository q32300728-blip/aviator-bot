import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম স্টাইল কনফিগারেশন
st.set_page_config(page_title="Pro Elite OTC AI Trading Terminal", layout="wide", page_icon="📈")

# ডিসপ্লের ওপরে বড় ও আকর্ষণীয় সিগন্যাল এবং প্রিমিয়াম লুকের জন্য কাস্টম CSS
st.markdown("""
<style>
.main { background-color: #07090e; color: #ffffff; }
.stButton>button { width: 100%; background: linear-gradient(135deg, #00b09b, #96c93d); color: white; padding: 14px; border-radius: 12px; border: none; font-weight: bold; font-size: 18px; }
.stButton>button:hover { background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; }

/* ডিসপ্লের উপরে বড় করে সিগন্যাল দেখানোর জন্য প্রিমিয়াম ডিজাইন */
.big-signal-up { 
    background: linear-gradient(135deg, #00b09b, #96c93d); 
    padding: 25px; 
    border-radius: 16px; 
    color: white; 
    text-align: center; 
    font-size: 36px; 
    font-weight: 900; 
    box-shadow: 0 6px 25px rgba(0,176,155,0.6); 
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
    box-shadow: 0 6px 25px rgba(255,65,108,0.6); 
    margin-bottom: 20px;
    letter-spacing: 1px;
}

.analysis-card { background-color: #121824; padding: 25px; border-radius: 16px; border: 1px solid #1f293d; box-shadow: 0 4px 20px rgba(0,0,0,0.6); font-size: 16px; line-height: 1.7; color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ড্যাশবোর্ড বা সিক্রেট থেকে এপিআই কী লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not found in Dashboard secrets.")
else:
    genai.configure(api_key=api_key)

# দ্রুততম ও নিখুঁত রেসপন্সের জন্য জেমিনির লেটেস্ট মডেল সেট করা হলো
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🚀 প্রো এলিট ওটিসি এআই ট্রেডিং টার্মিনাল")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ ট্রেডিং সেটিংস")
    market_name = st.selectbox("যেকোনো ওটিসি মার্কেট সিলেক্ট করুন:", [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "USD/JPY (OTC)", 
        "EUR/JPY (OTC)", "USD/BDT (OTC)", "Crypto Index (OTC)", "Other OTC Market"
    ])
    st.markdown("---")
    st.info("💡 ১-মিনিটের ওটিসি চার্টের পরিষ্কার স্ক্রিনশট আপলোড করে এনালাইসিস শুরু করুন।")

uploaded_file = st.file_uploader(f"মার্কেট [{market_name}] এর ১-মিনিটের চার্ট আপলোড করুন:", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns([1, 2.2])

with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Live Chart: " + market_name, use_container_width=True)

with col2:
    st.subheader("📊 অ্যাডভান্সড এআই সিগন্যাল ও মার্কেট অ্যানালাইসিস")
    
    # ফেক সিগন্যাল ফিল্টার করার এবং সমস্ত ইন্ডিকেটর/স্ট্র্যাটেজি অনুসরণের জন্য শক্তিশালী প্রম্পট
    system_prompt = """
    Act as an elite OTC Market Algorithmic Trader, Price Action Master, and Binary Options Expert. 
    Analyze this 1-minute OTC chart snapshot instantly. Strictly filter out fake or weak signals, and provide a high-probability professional technical response in Bengali under the following exact headings:
    
    1. **ফাইনাল ট্রেডিং সিগন্যাল (Final Signal):** Write clearly "UP (CALL)" or "DOWN (PUT)" right at the top based on strong confirmation.
    2. **মার্কেট কন্ট্রোল ও অ্যাক্টিভিটি (Market Control & Active Buyers/Sellers):** Are buyers or sellers currently active and dominating the market momentum?
    3. **মার্কেট প্রাইস পয়েন্ট ও অ্যালগরিদম (Price Points & OTC Algorithm):** Which OTC manipulation, trap, or algorithmic strategy is currently playing out?
    4. **হায়ার হাই ও লোয়ার লো স্ট্রাকচার (Higher High & Lower Low - HH/LL):** Trend structure and swing analysis.
    5. **ক্যান্ডেল রিজেকশন ও উইক স্টাডি (Candle Rejection & Wicks):** Rejection analysis and pressure from wicks.
    6. **সাপোর্ট ও রেজিস্ট্যান্স লেভেল (Support & Resistance Zones):** Key psychological or active technical levels.
    7. **১-মিনিট এন্ট্রি গাইডলাইন (1-Minute Entry Advice):** Precise entry instructions for the next candle.
    """

    if st.button("⚡ ফাস্ট এনালাইসিস শুরু করুন (২০ সেকেন্ড)"):
        if uploaded_file is not None:
            with st.spinner("এআই অ্যালগরিদম চার্ট স্ক্যান করছে, ২০ সেকেন্ডের মধ্যে ফলাফল আসছে..."):
                response = model.generate_content([system_prompt, image])
                result_text = response.text

                # ডিসপ্লের উপরে বড় করে সিগন্যাল দেখানোর লজিক
                if "DOWN" in result_text.upper() or "PUT" in result_text.upper():
                    st.markdown(f'<div class="big-signal-down">🔻 DOWN / PUT SIGNAL (SELL)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="big-signal-up">🚀 UP / CALL SIGNAL (BUY)</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="analysis-card">
                    {result_text}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ ট্রেড করার আগে অনুগ্রহ করে ১-মিনিটের ওটিসি চার্টের একটি স্ক্রিনশট আপলোড করুন!")
