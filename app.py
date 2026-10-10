import os
import time
from quotexpy import Quotex

# রেন্ডারের এনভায়রনমেন্ট থেকে ইমেইল ও পাসওয়ার্ড নেবে (কোডে লিখতে হবে না)
EMAIL = os.getenv("QUOTEX_EMAIL", "")
PASSWORD = os.getenv("QUOTEX_PASSWORD", "")

def run_quotex_bot():
    print("Connecting to Quotex...")
    client = Quotex(email=EMAIL, password=PASSWORD)
    
    # quotexpy এর কানেকশন পদ্ধতি
    check = client.connect()

    if check:
        print("Connected Successfully!")
        
        # 0 মানে হলো রিয়েল অ্যাকাউন্ট (Real Account)
        client.change_balance(0)
        print("Switched to Real Account.")
        
        asset = "EURUSD"
        amount = 1
        action = "call"       # "call" (UP) অথবা "put" (DOWN)
        duration = 60         # সময় সেকেন্ডে
        
        status, buy_info = client.buy(asset, amount, action, duration)
        print("Trade Status:", status, buy_info)
        
        client.close()
    else:
        print("Connection Failed")

if __name__ == "__main__":
    run_quotex_bot()
