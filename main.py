import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # ব্রাউজারের যেকোনো কনসোল বা নেটওয়ার্ক মেসেজ ট্র্যাক করা
        page.on("console", lambda msg: print(f"🖥️ CONSOLE: {msg.text}"))

        # WebSocket কানেকশন এবং ডেটা ক্যাপচার করার সঠিক পদ্ধতি
        def setup_websocket(ws):
            print(f"🔥 WebSocket Opened: {ws.url}")
            ws.on("framereceived", lambda payload: print(f"📥 LIVE DATA CATCHED: {payload}"))
            ws.on("framesent", lambda payload: print(f"📤 SENT: {payload}"))

        page.on("websocket", setup_websocket)

        print("Navigating to J188 Aviator...")
        await page.goto("https://j188.com", timeout=60000)
        
        print("Waiting for live game signals... (Playing/Listening active)")
        # দীর্ঘ সময় ধরে লাইভ স্ট্রিম শোনার জন্য লুপ রাখা
        await asyncio.sleep(600)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
