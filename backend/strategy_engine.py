import random
import asyncio
import websockets
import json

# ✅ Deriv WebSocket Price Fetcher
async def get_live_price(symbol: str) -> float:
    deriv_symbol_map = {
        "Boom 1000": "BOOM1000",
        "Boom 500": "BOOM500",
        "Crash 1000": "CRASH1000",
        "Crash 500": "CRASH500",
        "Volatility 75 Index": "R_75",
        "Volatility 25 Index": "R_25",
        "Volatility 10 Index": "R_10",
        "Volatility 100 Index": "R_100"
    }

    ws_url = "wss://ws.derivws.com/websockets/v3"
    selected = deriv_symbol_map.get(symbol, "R_75")

    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            "ticks": selected,
            "subscribe": 1
        }))

        while True:
            message = await ws.recv()
            data = json.loads(message)
            if "tick" in data and "quote" in data["tick"]:
                return data["tick"]["quote"]

# ✅ Your existing signal logic (mocked AI logic)
def generate_signal(symbol: str, price: float) -> dict:
    direction = random.choice(["buy", "sell"])
    order_type = random.choice(["market", "buy_limit", "sell_limit", "buy_stop", "sell_stop"])
    entry = round(price + random.uniform(-5, 5), 2)
    sl = round(entry + random.uniform(-10, -5) if direction == "sell" else entry + random.uniform(5, 10), 2)
    tp = round(entry + random.uniform(5, 10) if direction == "sell" else entry + random.uniform(-10, -5), 2)
    confidence = random.randint(70, 95)

    return {
        "symbol": symbol,
        "timeframe_htf": "1H",
        "timeframe_ltf": "15m",
        "direction": direction,
        "order_type": order_type,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "confidence": confidence
    }
