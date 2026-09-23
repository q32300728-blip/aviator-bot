import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        # নেটওয়ার্ক ট্রাফিক থেকে সরাসরি গেমের আসল WebSocket ধরার ব্যবস্থা
        page.on("websocket", lambda ws: asyncio.create_task(monitor_ws(ws)))

        print("J188 Aviator গেম পেজ ওপেন করা হচ্ছে...")
        # সরাসরি গেমের নির্দিষ্ট লিংকে প্রবেশ করানো
        await page.goto("https://j188.com/", wait_until="domcontentloaded")
        print("🤖 বট সফলভাবে কানেক্ট হয়েছে এবং লাইভ ডেটার জন্য অপেক্ষা করছে...")

        while True:
            await asyncio.sleep(10)

async def monitor_ws(ws):
    url = ws.url
    # গেমের ডেটা সার্ভার বা ossjj1 ডোমেইনের WebSocket ফিল্টার করা
    if "ossjj1.com" in url or "ws" in url:
        print(f"\n🔥 সফলভাবে গেমের WebSocket কানেক্ট হয়েছে!")
        
        async def on_message(msg):
            # বিমান ওড়ার আগের প্রি-রাউন্ড বা মাল্টিপ্লায়ার ডেটা প্রিন্ট করা
            msg_lower = msg.lower()
            if any(k in msg_lower for k in ["starting", "waiting", "pre_round", "multiplier", "f_start", "coeff"]):
                print(f"🎯 [মাল্টিপ্লায়ার/প্রি-রাউন্ড ডেটা]: {msg}")
            else:
                # যদি দেখতে চান সব ডেটা আসছে কি না, তবে এটি আনকমেন্ট করতে পারেন
                print(f"📦 লাইভ ডেটা: {msg}")

        ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

if __name__ == "__main__":
    asyncio.run(run_bot())
