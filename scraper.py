import asyncio
from playwright.async_api import async_playwright

async def get_live_websocket_url():
    """রিয়েল-টাইম ব্রাউজার অটোমেশন দিয়ে গেমের আসল WebSocket URL ক্যাপচার করা"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        target_ws_url = None

        def handle_ws(ws):
            nonlocal target_ws_url
            if "ossjj1.com" in ws.url or "ws" in ws.url:
                if "theengagelab" not in ws.url:
                    target_ws_url = ws.url
                    print(f"[+] ডাইনামিক WebSocket URL পাওয়া গেছে: {target_ws_url}")

        page.on("websocket", handle_ws)
        
        print("🔄 J188 পেজ লোড হচ্ছে এবং টোকেন ক্যাপচার করা হচ্ছে...")
        try:
            await page.goto("https://j188.com/", wait_until="domcontentloaded", timeout=60000)
            # গেমের WebSocket ট্রিগার হওয়ার জন্য পর্যাপ্ত সময় অপেক্ষা
            for _ in range(20):
                if target_ws_url:
                    break
                await asyncio.sleep(1)
        except Exception as e:
            print(f"⚠️ ব্রাউজার লোডিং ওয়ার্নিং: {e}")
            
        await browser.close()
        return target_ws_url
