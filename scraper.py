import asyncio
from playwright.async_api import async_playwright

async def get_live_websocket_url():
    """Playwright ব্যবহার করে গেম পেজ থেকে লাইভ WebSocket URL ক্যাপচার করার ফাংশন"""
    ws_url = None
    
    async with async_playwright() as p:
        # ব্রাউজার হেডলেস মোডে চালু করা
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # নেটওয়ার্ক ট্রাফিক ট্র্যাক করে WebSocket URL খুঁজে বের করা
        def handle_websocket(ws):
            nonlocal ws_url
            if "springgaming.com" in ws.url or "ws" in ws.url:
                ws_url = ws.url
                print(ws_url)

        page.on("websocket", handle_websocket)
        
        try:
            # আপনার দেওয়া লিংকটি এখানে বসানো হলো
            await page.goto("https://j188.com/", timeout=60000)
            await asyncio.sleep(10) # গেম লোড হওয়া এবং WebSocket কানেক্ট হওয়ার জন্য সময় দেওয়া
        except Exception as e:
            print(f"⚠️ পেজ লোড করতে সমস্যা হয়েছে: {e}")
            
        await browser.close()
        
    return ws_url
