import random
import requests

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

def get_live_price(symbol: str) -> float:
    mapped_symbol = DERIV_SYMBOL_MAP.get(symbol, "R_75")
    url = f"https://api.deriv.com/api/tick?symbol={mapped_symbol}"

    try:
        print(f"🌐 Fetching live price from Deriv REST API: {url}")
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            price = float(data["tick"]["quote"])
            print(f"✅ Live price for {symbol}: {price}")
            return price
        else:
            print(f"❌ Deriv API error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Exception fetching live price: {e}")

    print("❌ Failed to fetch live price.")
    return 0.0

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
