import os
import requests

# ✅ Use Render environment variable for token and chat ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # could be a user ID or channel ID

def send_telegram_signal(signal: dict):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram bot token or chat ID not set in environment.")
        return

    message = (
        f"📊 *New Signal: {signal['symbol']} ({signal['timeframe_ltf']} / {signal['timeframe_htf']})*\n"
        f"{'🔻 SELL' if signal['direction'] == 'sell' else '🔺 BUY'} *{signal['order_type'].upper()}*\n\n"
        f"📥 Entry: `{signal['entry']}`\n"
        f"🛑 SL: `{signal['sl']}`\n"
        f"🎯 TP: `{signal['tp']}`\n"
        f"📊 Confidence: `{signal['confidence']}%`\n"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print("✅ Signal sent to Telegram.")
        else:
            print(f"❌ Telegram error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
