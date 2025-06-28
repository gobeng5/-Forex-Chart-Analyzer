from random import randint

# Simulated candle data (mocked conditions)
CANDLE_DATA = {
    "1H": {"trend": "bearish", "structure": "lower-high"},
    "15m": {"confirmation": "bearish-engulfing"}
}

def simulate_multi_timeframe(symbol: str):
    """
    Simulate HTF and LTF confluence.
    In production, you'd build candles from tick data.
    """
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
        if randint(0, 1):
            return "buy_limit", price - 10
        else:
            return "buy_stop", price + 5
    else:
        if randint(0, 1):
            return "sell_limit", price + 10
        else:
            return "sell_stop", price - 5

def generate_signal(symbol: str, price: float) -> dict:
    result = simulate_multi_timeframe(symbol)

    # ✅ Always return a fallback signal if no confluence
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
