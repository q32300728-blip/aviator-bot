import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        def handle_websocket(ws):
            print("[+] WebSocket Connected!")
            
            async def on_message(msg):
                if "starting" in msg.lower() or "waiting" in msg.lower() or "pre_round" in msg.lower():
                    print("বিমান ওড়ার আগের ডেটা:", msg)

            ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com/")
        print("Bot is running and listening for live data...")

        # স্ক্রিপ্ট যেন বন্ধ না হয়ে যায়, তাই দীর্ঘ সময় লুপ চালিয়ে রাখা
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_bot())
