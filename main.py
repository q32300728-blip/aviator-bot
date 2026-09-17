import asyncio
from bot import listen_game

if __name__ == "__main__":
    print("Starting Aviator Signal Bot...")
    try:
        asyncio.run(listen_game())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
