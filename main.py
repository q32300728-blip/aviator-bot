import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # সার্ভার থেকে রিয়েল-টাইম WebSocket ফ্রেম আসার সাথে সাথে তা প্রিন্ট করবে
        page.on("websocket", lambda ws: ws.on("framereceived", lambda payload: print("📡 LIVE SERVER DATA:", payload)))

        print("Connecting to J188 server...")
        await page.goto("https://j188.com")
        
        # লাইভ ডেটা দেখার জন্য সময় নির্ধারণ
        await asyncio.sleep(300)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
