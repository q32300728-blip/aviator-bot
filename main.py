import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # অ্যান্টি-বট ডিটেকশন এড়ানোর জন্য ব্রাউজারের বিভিন্ন ফ্ল্যাগ এবং আর্গুমেন্ট যুক্ত করা হয়েছে
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage"
            ]
        )
        
        # ইউজার এজেন্ট রিয়েল ব্রাউজারের মতো সেট করা যাতে সাইট ব্লক না করে
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = await context.new_page()

        # WebSocket ট্রাফিক ক্যাপচার করার ফাংশন
        def handle_websocket(ws):
            # নোটিফিকেশন বা আবলুস WebSocket বাদ দিয়ে শুধুমাত্র গেমের সার্ভার ফিল্টার করা
            if "ossjj1.com" in ws.url or "ws" in ws.url:
                if "theengagelab" not in ws.url:
                    print(f"\n[+] গেমের আসল WebSocket কানেক্ট হয়েছে: {ws.url}")
                    
                    async def on_message(msg):
                        # বিমান ওড়ার আগের প্রি-রাউন্ড বা মাল্টিপ্লায়ার ডেটা ফিল্টার করে প্রিন্ট করা
                        msg_lower = msg.lower()
                        if any(k in msg_lower for k in ["starting", "waiting", "pre_round", "multiplier", "f_start", "coeff", "f_end"]):
                            print(f"🎯 [মাল্টিপ্লায়ার/প্রি-রাউন্ড ডেটা]: {msg}")
                        else:
                            print(f"📦 লাইভ ডেটা: {msg}")

                    ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("J188 Aviator গেম পেজ লোড করা হচ্ছে...")
        try:
            # পেজ যেন সম্পূর্ণ লোড হওয়ার সুযোগ পায়
            await page.goto("https://j188.com/", wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"লোডিং ওয়ার্নিং (চালিয়ে যাওয়া হচ্ছে): {e}")

        print("🤖 বট সফলভাবে সচল রয়েছে এবং গেমের ডেটার জন্য অপেক্ষা করছে...")

        # স্ক্রিপ্ট যেন বন্ধ না হয়ে চিরকাল চালু থাকে
        while True:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_bot())
