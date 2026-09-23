import asyncio
import websockets
from scraper import get_live_websocket_url

async def process_game_data(message):
    """গেমের ডেটা ফিল্টার ও প্রসেস করার ফাংশন"""
    try:
        msg_lower = message.lower()
        # বিমান ওড়ার আগের প্রি-রাউন্ড, ওয়েটিং বা মাল্টিপ্লায়ার ডেটা ফিল্টার করা
        if any(k in msg_lower for k in ["starting", "waiting", "pre_round", "multiplier", "coeff", "f_start"]):
            print(f"🎯 [টার্গেট মাল্টিপ্লায়ার/প্রি-রাউন্ড ডেটা]: {message}")
        else:
            print(f"📦 লাইভ ডেটা: {message}")
    except Exception as e:
        print(f"❌ ডেটা প্রসেসিং ত্রুটি: {e}")

async def main():
    print("🤖 প্রফেশনাল Aviator মনিটরিং বট চালু হয়েছে...")
    
    while True:
        try:
            # ১. প্রথমে ডাইনামিক WebSocket ইউআরএল সংগ্রহ করা
            ws_url = await get_live_websocket_url()
            
            if not ws_url:
                print("⚠️ WebSocket URL পাওয়া যায়নি। ১০ সেকেন্ড পর আবার চেষ্টা করা হচ্ছে...")
                await asyncio.sleep(10)
                continue
                
            print(f"🔥 WebSocket সার্ভারে কানেক্ট করা হচ্ছে...")
            
            # ২. শক্তিশালী websockets লাইব্রেরি দিয়ে কানেকশন স্থাপন এবং লাইভ ডেটা শোনা
            async with websockets.connect(ws_url) as websocket:
                print("✅ সফলভাবে গেম সার্ভারের সাথে কানেক্টেড! লাইভ ডেটা মনিটর করা হচ্ছে...")
                
                async for message in websocket:
                    await process_game_data(message)
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"⚠️ কানেকশন ডিসকানেক্ট হয়ে গেছে: {e}. ৫ সেকেন্ড পর রি-কানেক্ট করা হচ্ছে...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ অপ্রত্যাশিত ত্রুটি দেখা দিয়েছে: {e}. ৫ সেকেন্ড পর আবার চেষ্টা করা হচ্ছে...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 বট ম্যানুয়ালি বন্ধ করা হয়েছে।")
