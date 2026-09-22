import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # headless=False করা হলো যাতে ব্রাউজার ব্যাকগ্রাউন্ডে সঠিকভাবে প্রসেস করতে পারে
        browser = await p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = await browser.new_page()

        def handle_websocket(ws):
            print(f"[+] WebSocket Connected: {ws.url}")
            
            async def on_message(msg):
                # প্রাপ্ত মেসেজ প্রিন্ট করা এবং ফিল্টার করা
                print("ম্যাসেজ এসেছে:", msg)
                if "starting" in msg.lower() or "waiting" in msg.lower() or "pre_round" in msg.lower():
                    print("🎯 বিমান ওড়ার আগের ডেটা:", msg)

            ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com/")
        print("Bot is running and listening for live data...")

        # স্ক্রিপ্ট চালু রাখার জন্য ইনফিনিট লুপ
        while True:
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_bot())
