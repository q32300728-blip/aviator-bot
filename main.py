async def crash_bot_listener():
    from websockets.client import connect
    from websockets.exceptions import ConnectionClosed
    
    while True:
        try:
            logging.info(f"[WebSocket] Connecting to target server...")
            async with connect(WS_URL, ping_interval=10, ping_timeout=5) as websocket:
                logging.info("[WebSocket] Connected successfully.")
                
                # সার্ভারে সাবস্ক্রিপশন বা ইউজার আইডি পাঠানো
                init_payload = json.dumps({"id": "63204229452", "type": "subscribe"})
                await websocket.send(init_payload)
                logging.info("[WebSocket] Sent initial payload.")
                
                async for message in websocket:
                    if isinstance(message, bytes):
                        try:
                            decoded_message = message.decode('utf-8', errors='ignore')
                        except Exception:
                            decoded_message = message.hex()
                    else:
                        decoded_message = message

                    logging.info(f"[Raw Stream]: {decoded_message}")
                    
                    try:
                        data = json.loads(decoded_message)
                        if isinstance(data, dict):
                            mult = data.get("multiplier") or data.get("f") or 1.00
                            status = data.get("status") or "RUNNING"
                            cache.update_state(status, float(mult))
                    except json.JSONDecodeError:
                        pass

        except ConnectionClosed as cc:
            logging.warning(f"[WebSocket] Connection closed: {cc}. Reconnecting...")
            await asyncio.sleep(2)
        except Exception as ex:
            logging.error(f"[WebSocket] Error: {ex}. Retrying...")
            await asyncio.sleep(3)
