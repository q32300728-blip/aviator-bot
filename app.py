import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# পৃষ্ঠার লেআউট কনফিগারেশন
st.set_page_config(page_title="AI OTC Trading Analysis Tool", layout="wide")

# রেন্ডার বা লোকাল এনভায়রনমেন্ট থেকে API Key লোড করা
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY environment variable not found. Please set it in your Render dashboard under Environment Variables.")
else:
    genai.configure(api_key=api_key)

# জেমিনি মডেল ইনিশিয়ালাইز করা (ফাস্ট রেসপন্সের জন্য flash মডেল)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 AI-Powered OTC Trading Analysis Tool (1-Min Auto-Analysis)")
st.write("আপনার ওটিসি ট্রেডিং চার্ট আপলোড করুন। সিস্টেম প্রতি ১ মিনিট পর পর ক্যান্ডেল ক্লোজ হওয়ার আগে বা ঠিক সময়ে নতুন এনালাইসিস আপডেট করবে।")

# ফাইল আপলোড অপশন
uploaded_file = st.file_uploader("ট্রেডিং চার্ট বা স্ক্রিনশট আপলোড করুন (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='আপলোডকৃত ট্রেডিং চার্ট', use_column_width=True)
    
    prompt = st.text_input("এআই-এর জন্য আপনার কোনো নির্দিষ্ট প্রশ্ন বা নির্দেশনা আছে কি?", "এই ১ মিনিটের ক্যান্ডেল চার্ট বিশ্লেষণ করে পরবর্তী মুভমেন্ট (Call/Put বা Up/Down) সম্পর্কে দ্রুত সিগন্যাল দিন:")
    
    # অটো-রিফ্রেশ বা প্রতি ১ মিনিটে এনালাইসিস করার জন্য চেক বক্স
    auto_refresh = st.checkbox("🔄 প্রতি ১ মিনিট পর পর অটোমেটিক রিকল/এনালাইসিস চালু করুন")
    
    if st.button("অ্যানালাইসিস শুরু করুন") or auto_refresh:
        placeholder = st.empty()
        
        while True:
            with placeholder.container():
                with st.spinner("১ মিনিটের ক্যান্ডেল এনালাইসিস করা হচ্ছে..."):
                    try:
                        # জেমিনি মডেলের মাধ্যমে ছবি ও প্রম্পট প্রসেস করা
                        response = model.generate_content([prompt, image])
                        st.success("সর্বশেষ ১ মিনিটের আপডেট:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"ত্রুটি ঘটেছে: {e}")
            
            # যদি অটো-রিফ্রেশ টিক দেওয়া না থাকে, তবে লুপ একবারে শেষ হয়ে যাবে
            if not auto_refresh:
                break
                
            # ১ মিনিট (৬০ সেকেন্ড) অপেক্ষা করার কাউন্টডাউন
            with st.status("পরবর্তী ১ মিনিটের ক্যান্ডেলের জন্য অপেক্ষা করা হচ্ছে...", expanded=False) as status:
                for remaining in range(60, 0, -1):
                    status.update(label=f"পরবর্তী আপডেট হতে বাকি: {remaining} সেকেন্ড...")
                    time.sleep(1)
                status.update(label="নতুন ক্যান্ডেল ডেটা প্রসেস হচ্ছে!", state="complete")
