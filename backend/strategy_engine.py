from random import randint

# Simulated multi-timeframe condition (replace with real logic later)
CANDLE_DATA = {
    "1H": {"trend": "bearish"},
    "15m": {"confirmation": "bearish-engulfing"}
}

def simulate_multi_timeframe(symbol: str):
    htf = "1H"
    ltf = "15m"
    htf_trend = CANDLE_DATA[htf]["trend"]
    ltf_pattern = CANDLE_DATA[ltf]["confirmation"]

    if htf_trend.startswith("bear") and "bearish" in ltf_pattern:
        direction = "sell"
    elif htf_trend.startswith("bull") and "bullish" in ltf_pattern:
        direction = "buy"
    else:
        return None
    return direction, htf, ltf

def choose_order_type(price: float, direction: str):
    if direction == "buy":
        return ("buy_limit", price - 10) if randint(0, 1) else ("buy_stop", price + 5)
    else:
        return ("sell_limit", price + 10) if randint(0, 1) else ("sell_stop", price - 5)

def generate_signal(symbol: str, price: float) -> dict:
    result = simulate_multi_timeframe(symbol)

    # Always generate fallback signal if no result
    if not result:
        direction, htf, ltf = "buy", "1H", "15m"
    else:
        direction, htf, ltf = result

    order_type, entry = choose_order_type(price, direction)
    sl = entry - 15 if direction == "buy" else entry + 15
    tp = entry + 30 if direction == "buy" else entry - 30
    confidence = randint(75, 92)

    return {
        "symbol": symbol,
        "timeframe_htf": htf,
        "timeframe_ltf": ltf,
        "direction": direction,
        "order_type": order_type,
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp": round(tp, 2),
        "confidence": confidence
    }
