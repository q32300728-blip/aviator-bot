import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # ব্রাউজার কনফিগারেশন যাতে কোনো অ্যান্টি-বট ব্লক করতে না পারে
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()

        # WebSocket ট্রাফিক ট্র্যাক করার ফাংশন
        def handle_websocket(ws):
            url = ws.url
            # নোটিফিকেশন WebSocket বাদ দিয়ে শুধু গেমের WebSocket ফিল্টার করা
            if "theengagelab" not in url:
                print(f"\n🔥 WebSocket কানেক্ট হয়েছে: {url}")
                
                async def on_message(msg):
                    # বিমান ওড়ার আগের প্রি-রাউন্ড বা মাল্টিপ্লায়ার ডেটা ফিল্টার করা
                    print(f"📦 রিসিভড ডেটা: {msg}")
                    msg_lower = msg.lower()
                    if any(k in msg_lower for k in ["starting", "waiting", "pre_round", "multiplier", "f_start", "coeff", "result"]):
                        print(f"🎯 [কাঙ্ক্ষিত ডেটা/মাল্টিপ্লায়ার]: {msg}")

                ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("J188 গেম পেজ ওপেন হচ্ছে...")
        try:
            # প্রথমে মূল সাইটে প্রবেশ করা
            await page.goto("https://j188.com/", wait_until="domcontentloaded", timeout=60000)
            print("⏳ পেজ লোড হয়েছে, গেমের WebSocket ট্রিগার করার জন্য অপেক্ষা করা হচ্ছে...")
            
            # গেমের পেজে ইউজারকে অনুকরণ করে কিছুক্ষণ অপেক্ষা করা যাতে WebSocket কানেক্ট হতে পারে
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"লোড ওয়ার্নিং: {e}")

        print("🤖 বট সফলভাবে লাইভ ডেটা শোনার জন্য ব্যাকগ্রাউন্ডে সচল রয়েছে...")

        # স্ক্রিপ্ট যেন চিরকাল সচল থাকে এবং বন্ধ না হয়
        while True:
            await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(run_bot())
