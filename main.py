import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        # ক্লাউড এনভায়রনমেন্টের জন্য headless=True রাখতে হবে
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # WebSocket বা নেটওয়ার্ক ট্রাফিক ট্র্যাক করার জন্য ইভেন্ট লিসেনার
        page.on("websocket", lambda ws: print(f"🔥 Connected to WebSocket: {ws.url}"))

        print("Opening game page...")
        await page.goto("https://j188.com")

        print("Bot is running and listening for live data...")
        await asyncio.sleep(120)  # ২ মিনিট রান করবে

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
