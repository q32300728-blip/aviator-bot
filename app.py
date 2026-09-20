import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# পৃষ্ঠার লেআউট এবং স্টাইলিং কনফিগারেশন
st.set_page_config(page_title="Pro OTC AI Trading Terminal", layout="wide", page_icon="📈")

# কাস্টম CSS দিয়ে বড় ডিসপ্লে সিগন্যাল এবং প্রিমিয়াম লুক তৈরি করা হলো
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #00ffa3; color: #0b0f19; font-weight: bold; border-radius: 8px; height: 3.5em; font-size: 16px; }
    .stButton>button:hover { background-color: #00cc82; color: #ffffff; }
    
    /* বড় সিগন্যাল ডিসপ্লে স্টাইল */
    .signal-up { background: linear-gradient(135deg, #00b09b, #96c93d); color: white; padding: 30px; border-radius: 15px; text-align: center; font-size: 45px; font-weight: bold; box-shadow: 0px 4px 25px rgba(0, 176, 155, 0.5); margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
    .signal-down { background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; padding: 30px; border-radius: 15px; text-align: center; font-size: 45px; font-weight: bold; box-shadow: 0px 4px 25px rgba(255, 65, 108, 0.5); margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
    
    .analysis-card { background-color: #151a28; padding: 25px; border-radius: 12px; border: 1px solid #262d40; margin-top: 15px; font-size: 16px; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# আপনার এপিআই কি এখানে বসান
genai.configure(api_key="YOUR_API_KEY")

# দ্রুত রেসপন্সের জন্য ফ্লাশ মডেল ব্যবহার (২০ সেকেন্ডে আউটপুটের জন্য সেরা)
model = genai.GenerativeModel('gemini-1.5-flash')

# হেডার সেকশন
st.title("⚡ Pro OTC AI Trading Terminal & Signal Generator")
st.markdown("---")

# সাইডবার কন্ট্রোলস
with st.sidebar:
    st.header("⚙️ টার্মিনাল সেটিংস")
    market_name = st.selectbox("OTC মার্কেট সিলেক্ট করুন:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "Crypto IDX (OTC)", "অন্যান্য OTC Market"])
    auto_refresh = st.checkbox("🔄 অটো-অ্যানালাইসিস লুপ চালু করুন (প্রতি ২০ সেকেন্ড)")
    st.markdown("---")
    st.info("💡 টিপস: ওটিসি মার্কেটের ১-মিনিটের পরিষ্কার ক্যান্ডেলস্টিক চার্ট স্ক্রিনশট আপলোড করুন।")

# ফাইল আপলোড অপশন
uploaded_file = st.file_uploader(f"📷 {market_name} এর চার্ট বা স্ক্রিনশট আপলোড করুন (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Live Chart: {market_name}', use_column_width=True)
    
    with col2:
        st.subheader("📊 রিয়েল-টাইম এআই সিগন্যাল প্যানেল")
        
        # অ্যাডভান্সড ওটিসি অ্যালগরিদম প্রম্পট
        system_prompt = f"""
        Act as an elite, professional OTC Market Algorithmic Trader and Price Action Expert. Analyze this 1-minute OTC chart for {market_name} with extreme precision, considering all complex candle patterns, fakeouts, and algorithm behaviors.
        
        You must strictly evaluate and provide your response in Bengali, structured under these headings:
        1. **চূড়ান্ত সিগন্যাল (Final Signal):** Clearly write "UP (CALL)" or "DOWN (PUT)" right at the top.
        2. **মারকেট কাদের আয়ত্তে আছে (Market Dominance):** Analyze whether Buyers (Bulls) or Sellers (Bears) have more control and strength percentage.
        3. **প্রাইস পয়েন্ট ও লেভেল (Price Points & HH/LL):** Mention current price points, Higher Highs (HH), and Lower Lows (LL).
        4. **সাপোর্ট ও রেজিস্টেন্স (Support & Resistance):** Immediate key support and resistance zones.
        5. **ইন্ডিকেটর ও ভলিউম অ্যানালাইসিস (Indicator & Volume):** Volume behaviour and momentum.
        6. **ক্যান্ডেল প্রেডিকশন ও স্ট্র্যাটেজি (Candle Prediction & Strategy):** Predict the upcoming candle movement and provide exact entry advice.
        """
        
        if st.button("🚀 ২০ সেকেন্ডে ফাস্ট অ্যানালাইসিস শুরু করুন") or auto_refresh:
            placeholder = st.empty()
            
            while True:
                with placeholder.container():
                    with st.spinner("⚡ ২০ সেকেন্ডের মধ্যে ওটিসি অ্যালগরিদম ও ক্যান্ডেল স্ক্যান করা হচ্ছে..."):
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
                            
                            st.caption(f"⏱️ অ্যানালাইসিস সফল! সময় লেগেছে: {speed_taken} সেকেন্ড | মার্কেট: {market_name}")
                            
                            # বিস্তারিত অ্যানালাইসিস কার্ড
                            st.markdown(f"""
                            <div class="analysis-card">
                                {result_text}
                            </div>
                            """, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"⚠️ ত্রুটি ঘটেছে: {e}")
                
                if not auto_refresh:
                    break
                
                # ২০ সেকেন্ডের কাউন্টডাউন লুপ
                with st.status("⏳ পরবর্তী ২০ সেকেন্ডের স্ক্যানের জন্য অপেক্ষা করা হচ্ছে...", expanded=False) as status:
                    for remaining in range(20, 0, -1):
                        status.update(label=f"পরবর্তী আপডেট হতে বাকি: {remaining} সেকেন্ড...")
                        time.sleep(1)
                    status.update(label="নতুন ক্যান্ডেল স্ক্যান হচ্ছে!", state="complete")
