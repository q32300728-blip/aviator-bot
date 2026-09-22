import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        def handle_websocket(ws):
            # শুধুমাত্র গেম বা নির্দিষ্ট সার্ভারের WebSocket ট্র্যাক করার জন্য শর্ত
            if "ossjj1.com" in ws.url or "ws" in ws.url:
                print(f"\n[+] গেমের WebSocket কানেক্ট হয়েছে: {ws.url}")
                
                async def on_message(msg):
                    print("রিসিভড ডেটা:", msg)
                    if "starting" in msg.lower() or "waiting" in msg.lower() or "pre_round" in msg.lower():
                        print("🎯 বিমান ওড়ার আগের ডেটা:", msg)

                ws.on("framereceived", lambda payload: asyncio.create_task(on_message(payload)))

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com/")
        print("Bot is running and listening for live data...")

        # স্ক্রিপ্ট সচল রাখার জন্য ইনফিনিট লুপ
        while True:
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_bot())
