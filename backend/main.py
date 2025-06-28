from fastapi import FastAPI
from strategy_engine import generate_signal
from pydantic import BaseModel

app = FastAPI()

class PriceData(BaseModel):
    symbol: str
    price: float

@app.post("/generate-signal/")
async def get_signal(data: PriceData):
    signal = generate_signal(data.symbol, data.price)
    return {"signal": signal}
