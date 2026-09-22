import asyncio
import json
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        def handle_websocket(ws):
            print(f"🔥 Connected to WebSocket: {ws.url}")
            
            def process_message(payload):
                try:
                    data = json.loads(payload)
                    
                    # ডেটার ভেতরে মাল্টিপ্লায়ার বা নির্দিষ্ট কোনো কি-ওয়ার্ড আছে কিনা চেক করা
                    payload_str = str(data)
                    if "multiplier" in payload_str.lower() or "coef" in payload_str.lower() or "f" in payload_str.lower():
                        print(💥 f"\n[!!!] TARGET DATA / MULTIPLIER FOUND: {data}\n")
                    else:
                        # সাধারণ লাইভ মেসেজগুলো ছোট করে দেখাতে পারেন
                        pass
                except:
                    # যদি টেক্সট ফরম্যাটে মাল্টিপ্লায়ার থাকে
                    if "x" in payload.lower() or "multiplier" in payload.lower():
                        print(🚀 f"\n[live] M-DATA: {payload}\n")

            ws.on("framereceived", process_message)

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com")

        print("Bot is tracking multipliers...")
        await asyncio.sleep(300)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
