async def listen_websocket():
    global game_history_list
    uri = "wss://channel.local2j111.link/"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to Live WebSocket successfully!")
                async for message in websocket:
                    # র ডেটা কনসোলে প্রিন্ট করে দেখার জন্য
                    print("Received raw message:", message)
                    try:
                        if isinstance(message, str):
                            data = json.loads(message)
                            # আপাতত সব জেসন ডেটা থেকে হিস্ট্রি দেখানোর জন্য
                            game_history_list.insert(0, str(data))
                            if len(game_history_list) > 10:  
                                game_history_list.pop()
                    except Exception as e:
                        print("Parsing error:", e)
        except Exception as e:
            print("WebSocket connection lost, reconnecting...", e)
            await asyncio.sleep(3)
