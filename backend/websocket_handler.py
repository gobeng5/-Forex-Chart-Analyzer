import asyncio
import websockets
import json

DERIV_WS = "wss://ws.deriv.com/websockets/v3"

async def get_price(symbol):
    async with websockets.connect(DERIV_WS) as ws:
        await ws.send(json.dumps({"ticks": symbol}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "tick" in data:
                print(f"{symbol} price: {data['tick']['quote']}")
                return data['tick']['quote']
