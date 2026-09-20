from google import genai
from PIL import Image
import streamlit as st

# রেন্ডারে সিক্রেট হিসেবে এপিআই কি সেট করতে পারেন বা সরাসরি দিতে পারেন
# তবে সিকিউরিটির জন্য st.secrets ব্যবহার করা ভালো
client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY"))

st.set_page_config(
    page_title="OTC AI Chart Analyst", page_icon="📈", layout="centered"
)

st.title("🤖 OTC Market AI Analyst Software")
st.write(
    "ওটিসি মার্কেটের চার্টের স্ক্রিনশট আপলোড করুন। এআই প্যাটার্ন, ইন্ডিকেটর এবং"
    " প্লাস পয়েন্ট এনালাইসিস করে সিগন্যাল দেবে।"
)

# ইউজারের জন্য ইমেজ আপলোড অপশন
uploaded_file = st.file_uploader(
    "চার্টের স্ক্রিনশট এখানে আপলোড করুন...", type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(
      image,
      caption="Uploaded OTC Chart",
      use_column_width=True,
  )

  if st.button("🚀 এনালাইসিস শুরু করুন"):
    with st.spinner("এআই চার্ট এবং মার্কেট লজিক যাচাই করছে..."):
      try:
        prompt = """
                Act as an expert Binary Options OTC trading AI analyst. 
                Analyze this chart screenshot and provide your decision based on:
                1. Candlestick Patterns (Pin bar, Engulfing, Doji, etc.)
                2. Support & Resistance levels / Price Action
                3. Plus points / Confluence (Multiple confirmations)
                4. OTC Market micro-trends and risk factors
                
                Give your output clearly with:
                - Pattern Identified
                - Plus Points Matched
                - Market Condition (Safe/Risky)
                - Final Signal (UP / DOWN / NO TRADE) with confidence %.
                """

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[image, prompt]
        )

        st.success("এনালাইসিস সম্পন্ন হয়েছে!")
        st.markdown("### 📊 AI Report:")
        st.write(response.text)

      except Exception as e:
        st.error(f"একটি সমস্যা হয়েছে: {e}")
