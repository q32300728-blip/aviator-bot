import os
import random
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# গেমের গ্লোবাল স্টেট (ভিডিওর স্টাইলের সাথে সামঞ্জস্যপূর্ণ)
game_state = {
    "balance": 100.0,
    "multiplier": "1.30",
    "message": "Enter your bet amount to generate signal."
}

def generate_crash_point():
    r = random.random()
    if r < 0.05:
        return 1.0
    return round(1 / (1 - random.uniform(0.0, 0.97)), 2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "game": game_state})

@app.post("/play", response_class=HTMLResponse)
async def play_round(request: Request, bet: float = Form(...)):
    global game_state
    
    if bet <= 0 or bet > game_state["balance"]:
        game_state["message"] = "Invalid bet amount!"
        return templates.TemplateResponse("index.html", {"request": request, "game": game_state})
    
    game_state["balance"] -= bet
    crash = generate_crash_point()
    
    # ভিডিওর মতো একটি রিয়েলিস্টিক টার্গেট মাল্টিপ্লায়ার জেনারেট করা
    simulated_target = round(random.uniform(1.2, min(crash, 9.0)), 2)
    game_state["multiplier"] = f"{simulated_target:.2f}"
    
    if simulated_target < crash:
        winnings = round(bet * simulated_target, 2)
        game_state["balance"] += winnings
        game_state["message"] = f"Success! Signal Hit: {simulated_target}X | Won: ${winnings}"
    else:
        game_state["message"] = f"Crashed early at {crash}X! Lost ${bet}"
        
    game_state["balance"] = round(game_state["balance"], 2)

    return templates.TemplateResponse("index.html", {"request": request, "game": game_state})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
