import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # WebSocket কানেকশন ট্র্যাক করার ফাংশন
        def handle_websocket(ws):
            print(f"🔥 Connected to WebSocket: {ws.url}")
            
            # সার্ভার থেকে আসা প্রতিটি মেসেজ শোনার জন্য লিসেনার
            ws.on("framereceived", lambda payload: print(f"📥 Received Data: {payload}"))
            
            # বট থেকে কোনো ডেটা পাঠানো হলে তা দেখার জন্য
            ws.on("framesent", lambda payload: print(f"📤 Sent Data: {payload}"))

        page.on("websocket", handle_websocket)

        print("Opening game page...")
        await page.goto("https://j188.com")

        print("Bot is running and listening for live data...")
        await asyncio.sleep(300)  # ৫ মিনিট চলবে

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
