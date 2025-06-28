from random import randint

# Timeframe simulation settings (mocked for now)
CANDLE_DATA = {
    "1H": {"trend": "bearish", "structure": "lower-high"},
    "15m": {"confirmation": "bearish-engulfing"}
}

def simulate_multi_timeframe(symbol: str):
    """
    Simulate HTF and LTF confirmation for simplicity.
    In production, you'd build OHLC candles from tick data.
    """
    htf = "1H"
    ltf = "15m"

    # Placeholder logic
    htf_trend = CANDLE_DATA[htf]["trend"]
    ltf_pattern = CANDLE_DATA[ltf]["confirmation"]

    if htf_trend.startswith("bear") and "bearish" in ltf_pattern:
        direction = "sell"
    elif htf_trend.startswith("bull") and "bullish" in ltf_pattern:
        direction = "buy"
    else:
        return None  # No alignment → no signal

    return direction, htf, ltf

def choose_order_type(price: float, direction: str):
    """
    Decide order type based on mock price positioning.
    You can expand this using S/R zones or structure.
    """
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
    if not result:
        return None  # No valid confluence

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
