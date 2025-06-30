from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy_engine import generate_signal, get_live_price
from telegram_bot import send_telegram_signal

app = FastAPI(
    title="AI Forex Signal Generator",
    description="Generates trading signals using live Deriv prices and sends to Telegram.",
    version="1.0.0"
)

# ✅ CORS setup — restrict in production to your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body model
class SignalRequest(BaseModel):
    symbol: str

# ✅ Health check route
@app.get("/")
def root():
    return {"message": "Forex Signal API is running."}

# ✅ Main endpoint: generate signal using live Deriv price
@app.post("/generate-signal/")
async def generate_signal_with_live_price(data: SignalRequest):
    try:
        price = get_live_price(data.symbol)

        if price == 0.0:
            return {"error": f"Could not retrieve live price for symbol: {data.symbol}"}

        signal = generate_signal(data.symbol, price)
        print(f"📈 Signal generated: {signal}")

        # Send to Telegram bot
        send_telegram_signal(signal)

        return {"signal": signal}

    except Exception as e:
        print(f"❌ ERROR in /generate-signal/: {e}")
        return {"error": str(e)}
