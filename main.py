async def listen_to_game():
    uri = "wss://channel.local2j111.link/get"
    global latest_game_data
    while True:
        try:
            # হেডার ছাড়া সরাসরি কানেকশন স্টাবলিশ করা
            async with websockets.connect(uri) as websocket:
                latest_game_data["status"] = "Live Connected!"
                print("Connected to Live WebSocket!")
                async for message in websocket:
                    if isinstance(message, bytes):
                        hex_data = message.hex()
                        latest_game_data["binary_sample"] = f"Binary Packet: {hex_data[:30]}..."
                        print("Received Binary:", hex_data)
                    else:
                        data = json.loads(message)
                        latest_game_data["binary_sample"] = f"JSON Data: {str(data)[:40]}..."
                        print("Received JSON:", data)
        except Exception as e:
            latest_game_data["status"] = f"Reconnecting... ({e})"
            print(f"Connection lost: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
