def generate_signal(symbol: str, price: float) -> dict:
    if price % 2 == 0:
        return {
            "symbol": symbol,
            "direction": "buy",
            "entry": price,
            "sl": price - 10,
            "tp": price + 20,
            "confidence": 75
        }
    else:
        return {
            "symbol": symbol,
            "direction": "sell",
            "entry": price,
            "sl": price + 10,
            "tp": price - 20,
            "confidence": 68
        }
