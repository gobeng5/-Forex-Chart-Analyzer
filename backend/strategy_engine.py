import os
import json
import asyncio
import websockets

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
    api_token = os.getenv("DERIV_API_TOKEN")

    if not api_token:
        print("❌ DERIV_API_TOKEN is missing in environment variables.")
        return 0.0

    try:
        print(f"🔌 Connecting to Deriv WebSocket for {selected}")
        async with websockets.connect(ws_url, ping_interval=None) as ws:
            print("🔐 Sending authorization request...")
            await ws.send(json.dumps({ "authorize": api_token }))

            auth_response = await ws.recv()
            print("🔑 Auth response from Deriv:", auth_response)

            await ws.send(json.dumps({
                "ticks": selected,
                "subscribe": 1
            }))
            print(f"📡 Subscribed to ticks for: {selected}")

            for attempt in range(10):
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=5)
                    print(f"🛰️ Tick message received: {message}")
                    data = json.loads(message)

                    if "tick" in data and "quote" in data["tick"]:
                        price = float(data["tick"]["quote"])
                        print(f"✅ Price found: {price}")
                        return price
                except asyncio.TimeoutError:
                    print(f"⚠️ Timeout waiting for tick... retry {attempt+1}/10")

    except Exception as e:
        print(f"❌ WebSocket error: {e}")

    print("❌ Final failure: No live price received.")
    return 0.0
