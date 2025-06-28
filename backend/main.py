from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy_engine import generate_signal, get_live_price
from telegram_bot import send_telegram_signal

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://your-vercel-site.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input schema
class SignalRequest(BaseModel):
    symbol: str

# ✅ POST endpoint: uses backend to get live price
@app.post("/generate-signal/")
async def generate_signal_with_live_price(data: SignalRequest):
    live_price = await get_live_price(data.symbol)
    print(f"💰 Live price for {data.symbol}: {live_price}")

    signal = generate_signal(data.symbol, live_price)
    if signal:
        send_telegram_signal(signal)
    return {"signal": signal}
