from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from strategy_engine import generate_signal
from telegram_bot import send_telegram_signal

app = FastAPI()

# ✅ Allow cross-origin requests from Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify: ["https://your-vercel-site.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PriceData(BaseModel):
    symbol: str
    price: float

@app.post("/generate-signal/")
async def get_signal(data: PriceData):
    signal = generate_signal(data.symbol, data.price)
    print("DEBUG - Signal:", signal)
    if signal:
        send_telegram_signal(signal)
    return {"signal": signal}
