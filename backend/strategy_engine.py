import random
import asyncio
import websockets
import json

DERIV_SYMBOL_MAP = {
    "Boom 1000": "BOOM1000",
    "Boom 500": "BOOM500",
    "Crash 1000": "CRASH1000",
    "Crash 500": "CRASH500",
    "Volatility 75 Index": "R_75",
    "Volatility 25 Index": "R_25",
    "Volatility 10 Index": "R_10",
    "Volatility 100 Index": "R_100"
}

async def fetch_price(symbol: str) -> float:
    mapped_symbol = DERIV_SYMBOL_MAP.get(symbol, "R_75")
    uri = "wss://ws.derivws.com/websockets/v3?app_id=1089"

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({
                "ticks": mapped_symbol,
                "subscribe": 0
            }))
            response = await websocket.recv()
            data = json.loads(response)
            price = float(data["tick"]["quote"])
            print(f"✅ Live price for {symbol}: {price}")
            return price
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return 0.0

def get_live_price(symbol: str) -> float:
    return asyncio.run(fetch_price(symbol))

def generate_signal(symbol: str, price: float) -> dict:
    direction = random.choice(["buy", "sell"])
    order_type = random.choice(["market", "buy_limit", "sell_limit", "buy_stop", "sell_stop"])
    entry = round(price + random.uniform(-5, 5), 2)

    if direction == "sell":
        sl = round(entry + random.uniform(5, 10), 2)
        tp = round(entry - random.uniform(5, 10), 2)
    else:
        sl = round(entry - random.uniform(5, 10), 2)
        tp = round(entry + random.uniform(5, 10), 2)

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
