from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy_engine import generate_signal, get_live_price
from telegram_bot import send_telegram_signal

app = FastAPI()

# ✅ CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input model for /generate-signal/
class SignalRequest(BaseModel):
    symbol: str

# ✅ Main route to generate signal using live Deriv price
@app.post("/generate-signal/")
async def generate_signal_with_live_price(data: SignalRequest):
    try:
        price = get_live_price(data.symbol)  # ✅ No 'await' needed here
        if price == 0.0:
            return {"error": "Failed to fetch live price from Deriv."}

        signal = generate_signal(data.symbol, price)
        print(f"📈 Signal generated: {signal}")
        send_telegram_signal(signal)

        return {"signal": signal}

    except Exception as e:
        print(f"❌ ERROR in /generate-signal/: {e}")
        return {"error": str(e)}
