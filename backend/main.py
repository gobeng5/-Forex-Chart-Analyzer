from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy_engine import generate_signal, get_live_price
from telegram_bot import send_telegram_signal

app = FastAPI()

# ✅ Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class SignalRequest(BaseModel):
    symbol: str

# ✅ Main signal endpoint
@app.post("/generate-signal/")
async def generate_signal_with_live_price(data: SignalRequest):
    try:
        live_price = get_live_price(data.symbol)
        if live_price == 0.0:
            return {"error": "Failed to fetch live price from Deriv."}

        signal = generate_signal(data.symbol, live_price)
        print(f"📈 Signal generated: {signal}")
        send_telegram_signal(signal)

        return {"signal": signal}

    except Exception as e:
        print(f"❌ ERROR in /generate-signal/: {e}")
        return {"error": str(e)}
