import os
import time
from quotexapi.stable_api import Quotex

# রেন্ডারের এনভায়রনমেন্ট থেকে ইমেইল ও পাসওয়ার্ড নেবে (কোডে লিখতে হবে না)
EMAIL = os.getenv("QUOTEX_EMAIL", "")
PASSWORD = os.getenv("QUOTEX_PASSWORD", "")

def run_quotex_bot():
    print("Connecting to Quotex...")
    client = Quotex(email=EMAIL, password=PASSWORD)
    check, message = client.connect()

    if check:
        print("Connected Successfully!")
        client.change_balance("PRACTICE")
        
        asset = "EURUSD"
        amount = 1
        dir = "call"          # "call" (UP) অথবা "put" (DOWN)
        duration = 60         # সময় সেকেন্ডে
        
        status, buy_info = client.buy(asset, amount, dir, duration)
        print("Trade Status:", status, buy_info)
        
        client.close()
    else:
        print("Connection Failed:", message)

if __name__ == "__main__":
    run_quotex_bot()
