import asyncio
import websockets
import json
from scraper import get_live_websocket_url

async def process_game_data(message):
    """গেমের রিয়েল-টাইম ডেটা এবং মাল্টিপ্লায়ার ফিল্টার করার ফাংশন"""
    try:
        if isinstance(message, bytes):
            msg_str = message.decode('utf-8', errors='ignore')
        else:
            msg_str = message

        # পিং-পং বা হার্টবিট মেসেজ ইগ্নোর করা
        if "ping" in msg_str.lower() or "pong" in msg_str.lower():
            return

        # প্রি-রাউন্ড, ওয়েটিং বা মাল্টিপ্লায়ার ডেটা ফিল্টার করা
        msg_lower = msg_str.lower()
        if any(k in msg_lower for k in ["multiplier", "coeff", "starting", "waiting", "crash", "fly", "f_start"]):
            print(f"🎯 [টার্গেট গেম ডেটা]: {msg_str}")
        else:
            print(f"📦 লাইভ স্ট্রিম: {msg_str}")
            
    except Exception as e:
        print(f"❌ ডেটা প্রসেসিং ত্রুটি: {e}")

async def main():
    print("🤖 প্রফেশনাল Aviator পার্মানেন্ট মনিটরিং বট চালু হয়েছে...")
    
    while True:
        websocket = None
        try:
            # ১. ডাইনামিক সেশন ও WebSocket URL ফেচ করা
            ws_url = await get_live_websocket_url()
            
            if not ws_url:
                print("⚠️ WebSocket URL পাওয়া যায়নি। ১০ সেকেন্ড পর আবার চেষ্টা করা হচ্ছে...")
                await asyncio.sleep(10)
                continue
                
            print(f"🔥 গেম সার্ভারে স্থায়ী কানেকশন স্থাপন করা হচ্ছে...")
            
            # ২. পার্মানেন্ট WebSocket কানেকশন ওপেন রাখা
            async with websockets.connect(ws_url, ping_interval=20, ping_timeout=20) as websocket:
                print("✅ সফলভাবে কানেক্টেড! Stomp হ্যান্ডশেক পাঠানো হচ্ছে...")
                
                # সার্ভার হ্যান্ডশেকের জন্য Stomp কানেক্ট ফ্রেম পাঠানো
                connect_frame = "CONNECT\naccept-version:1.1,1.0\nheart-beat:10000,10000\n\n\x00"
                await websocket.send(connect_frame)
                
                # গেমের আপডেট চ্যানেলে সাবস্ক্রাইব করা
                sub_frame = "SUBSCRIBE\nid:sub-0\ndestination:/user/queue/game.update\n\n\x00"
                await websocket.send(sub_frame)
                
                print("🚀 সার্ভার থেকে লাইভ ডেটা শোনা শুরু হয়েছে...")
                
                # ৩. নিরবচ্ছিন্নভাবে লাইভ ডেটা রিড করার লুপ
                async for message in websocket:
                    await process_game_data(message)
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"⚠️ কানেকশন ড্রপ করেছে ({e})। ৫ সেকেন্ডের মধ্যে স্বয়ংক্রিয়ভাবে রি-কানেক্ট করা হচ্ছে...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ অপ্রত্যাশিত ত্রুটি: {e}. ৫ সেকেন্ড পর আবার চেষ্টা করা হচ্ছে...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 বট ম্যানুয়ালি বন্ধ করা হয়েছে।")
