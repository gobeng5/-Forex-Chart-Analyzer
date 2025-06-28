import httpx
import os

# Replace with your actual token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_signal(signal: dict):
    message = f"""
🚨 *New Trade Signal*

📉 *Symbol*: {signal['symbol']}
📊 *Direction*: {signal['direction'].upper()}
📈 *Entry*: {signal['entry']}
⛔ *SL*: {signal['sl']}
🎯 *TP*: {signal['tp']}
📊 *Confidence*: {signal['confidence']}%

#Forex #SignalBot
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
