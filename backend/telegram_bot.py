import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_signal(signal: dict):
    if not signal:
        return

    message = f"""
🚨 *New Trade Signal Alert*

📉 *Symbol*: `{signal['symbol']}`
🕒 *HTF*: `{signal['timeframe_htf']}` | *LTF*: `{signal['timeframe_ltf']}`

📊 *Direction*: *{signal['direction'].upper()}*
📥 *Order Type*: `{signal['order_type']}`

🎯 *Entry*: `{signal['entry']}`
⛔ *Stop Loss*: `{signal['sl']}`
✅ *Take Profit*: `{signal['tp']}`

📈 *Confidence Score*: *{signal['confidence']}%*

#Forex #SignalBot #{signal['direction']} #MTF
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = httpx.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
