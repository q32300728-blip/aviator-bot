import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        def handle_websocket(ws):
            print("[+] WebSocket Connected!")
            
            async def on_message(msg):
                # বিমান ওড়ার আগের নির্দিষ্ট ডেটা ফিল্টার করার শর্ত
                if "starting" in msg.lower() or "waiting" in msg.lower() or "pre_round" in msg.lower():
                    print("বিমান ওড়ার আগের ডেটা:", msg)

            ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        # সরাসরি গেমের মূল পেজে প্রবেশ করা
        print("Opening game page...")
        await page.goto("https://j188.com/")

        # স্ক্রিপ্ট সচল রাখার জন্য সময়
        await asyncio.sleep(3600)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
