import asyncio
import json
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # headless=False করার কারণে ব্রাউজার স্ক্রিনে ওপেন হবে এবং WebSocket সঠিকভাবে কানেক্ট হবে
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        def handle_websocket(ws):
            print(f"\n🔥 WebSocket Connected: {ws.url}")
            
            def process_message(payload):
                try:
                    data = json.loads(payload)
                    payload_str = str(data)
                    # গেমের ডেটা বা মাল্টিপ্লায়ার ফিল্টার করা
                    if any(k in payload_str.lower() for k in ["multiplier", "coef", "f", "progress", "state"]):
                        print(f"💥 MULTIPLIER/DATA: {data}")
                except:
                    if any(k in payload.lower() for k in ["x", "multiplier", "fly"]):
                        print(f"🚀 LIVE DATA: {payload}")

            ws.on("framereceived", process_message)

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com")

        print("Bot is listening to live data...")
        await asyncio.sleep(300)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
