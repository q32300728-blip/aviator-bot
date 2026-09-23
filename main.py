import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # ব্রাউজার ব্যাকগ্রাউন্ডে স্টেবলভাবে রান করার জন্য কনফিগারেশন
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        def handle_websocket(ws):
            # গেমের WebSocket কানেকশন ট্র্যাক করা
            print(f"\n[+] নতুন WebSocket কানেক্ট হয়েছে: {ws.url}")
            
            async def on_message(msg):
                # প্রি-রাউন্ড, ওয়েটিং বা মাল্টিপ্লায়ার সম্পর্কিত কিওয়ার্ড ফিল্টার করা
                keywords = ["starting", "waiting", "pre_round", "f_start", "multiplier", "coeff", "status"]
                if any(kw in msg.lower() for kw in keywords):
                    print("🎯 Aviator গেম ডেটা (মাল্টিপ্লায়ার/প্রি-রাউন্ড):", msg)

            ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("J188 গেম পেজ ওপেন হচ্ছে...")
        await page.goto("https://j188.com/", wait_until="networkidle")
        print("🤖 বট সফলভাবে লাইভ ডেটা শোনার জন্য প্রস্তুত এবং সচল রয়েছে...")

        # স্ক্রিপ্ট যেন বন্ধ না হয়ে চিরকাল ব্যাকগ্রাউন্ডে চলতে থাকে
        while True:
            await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(run_bot())
