from flask import Flask, render_template, jsonify
import threading
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# গেমের হিস্ট্রি সংরক্ষণের গ্লোবাল লিস্ট
game_history_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    global game_history_list
    return jsonify({
        "status": "Running (Server-Side Scraping)",
        "history": game_history_list
    })

# ব্যাকগ্রাউন্ডে ব্রাউজার চালিয়ে গেম থেকে ডাটা সংগ্রহ করার ফাংশন
def background_scraper():
    global game_history_list
    with sync_playwright() as p:
        # হেッドレス মোডে ব্রাউজার ওপেন করা
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Opening game page...")
            page.goto("https://game.wifun777.link/web/")
            
            while True:
                page.wait_for_timeout(3000) # প্রতি ৩ সেকেন্ড পর পর ডেটা চেক করবে
                
                # গেমের পেজ থেকে হিস্ট্রি বা আগের রাউন্ডের মাল্টিপ্লায়ার রিড করা
                history = page.evaluate('''() => {
                    const elements = document.querySelectorAll('.payout-string, [class*="multiplier"]');
                    let results = [];
                    elements.forEach(el => results.push(el.innerText));
                    return results;
                }''')
                
                if history and len(history) > 0:
                    game_history_list = history
                    
        except Exception as e:
            print("Scraping Error:", e)
        finally:
        titles = browser.close()

# ব্যাকগ্রাউন্ডে স্ক্র্যাপার রান করার জন্য থ্রেড চালু করা
scraper_thread = threading.Thread(target=background_scraper, daemon=True)
scraper_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
