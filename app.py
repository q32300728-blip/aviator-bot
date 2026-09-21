import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# পৃষ্ঠার লেআউট এবং প্রিমিয়াম স্টাইল কনফিগারেশন
st.set_page_config(page_title="Pro Elite OTC AI Trading Terminal", layout="wide", page_icon="📈")

# কাস্টম CSS দিয়ে প্রিমিয়াম লুক
st.markdown("""
<style>
.main { background-color: #07090e; color: #ffffff; }
.stButton>button { width: 100%; background: linear-gradient(135deg, #00b09b, #96c93d); color: white; padding: 12px; border-radius: 12px; border: none; font-weight: bold; font-size: 16px; }
.stButton>button:hover { background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; }

.signal-up { background: linear-gradient(135deg, #00b09b, #96c93d); padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 20px; font-weight: bold; }
.signal-down { background-color: #ff416c; padding: 15px; border-radius: 12px; color: white; text-align: center; font-size: 20px; font-weight: bold; }

.analysis-card { background-color: #121824; padding: 25px; border-radius: 16px; border: 1px solid #1f293d; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
</style>
""", unsafe_allow_html=True)

# রেন্ডার ড্যাশবোর্ড থেকে এপিআই কী লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY environment variable not found in Render Dashboard.")
else:
    genai.configure(api_key=api_key)

# এরর মেসেজ অনুযায়ী লেটেস্ট মডেল সেট করা হলো
model = genai.GenerativeModel('gemini-3.6-flash')

st.title("প্রো এলিট ওটিসি এআই ট্রেডিং টার্মিনাল")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ সেটিংস")
    market_name = st.selectbox("OTC মার্কেট সিলেক্ট করুন:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "USD/JPY (OTC)", "EUR/JPY (OTC)"])
    st.markdown("---")
    st.info("💡 ১-মিনিটের চার্ট আপলোড করে নিচের বাটন ক্লিক করুন:")

uploaded_file = st.file_uploader(f"মার্কেট {market_name} এর চার্ট আপলোড করুন:", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns([1, 4])

with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Live Chart: " + market_name, use_container_width=True)

with col2:
    st.subheader("📊 এআই সিগন্যাল প্যানেল")
    
    system_prompt = """
    Act as an elite OTC Market Algorithmic Trader and Price Action Master. Analyze this 1-minute OTC chart and provide your response strictly in Bengali under these headings:
    1. **মুহূর্তের ফাইনাল (Final Signal):** Write "UP (CALL)" or "DOWN (PUT)" right at the top.
    2. **মার্কেট বারের আয়ত্তে আছে (Market Dominance):** Buyers vs Sellers strength.
    3. **ওটিসি ট্র্যাপ ও ফ্লোটেলিটি (OTC Trap):** Trap or liquidity grab status.
    4. **প্রাইস পয়েন্ট ও লেভেল (Price Points & HM/LL):** Key levels.
    5. **সাপোর্ট ও রেজিস্ট্যান্স (Support & Resistance):** Zones.
    6. **ক্যান্ডেল প্রডিকশন (Candle Prediction & Strategy):** Direction and entry advice.
    """

    if st.button("🚀 এনালাইসিস শুরু করুন"):
        if uploaded_file is not None:
            with st.spinner("এআই চার্ট বিশ্লেষণ করছে, একটু অপেক্ষা করুন..."):
                response = model.generate_content([system_prompt, image])
                result_text = response.text

                if "DOWN" in result_text.upper() or "PUT" in result_text.upper():
                    st.markdown(f'<div class="signal-down">🔻 DOWN / PUT SIGNAL</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="signal-up">🚀 UP / CALL SIGNAL</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="analysis-card">
                    {result_text}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ প্রথমে অনুগ্রহ করে একটি চার্ট আপলোড করুন!")
