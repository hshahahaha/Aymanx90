import os
import telebot
import requests
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل ملف بطاقات بصيغة:\n`4111111111111111|12|2026|123`", parse_mode="Markdown")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    lines = downloaded_file.decode("utf-8").splitlines()

    bot.reply_to(message, f"📦 Total cards: {len(lines)}\n⏳ Starting check...")

    for i, card in enumerate(lines, 1):
        try:
            res = requests.post(API_URL, json={
                "api_key": API_KEY,
                "card": card
            }, timeout=10)
            data = res.json()
            status = data.get("result") or data.get("message") or "No result"
        except Exception as e:
            status = f"❌ Error: {str(e)}"

        bot.send_message(message.chat.id, f"[{i}] {card} → {status}")
        time.sleep(2)

print("✅ Bot is running...")
bot.infinity_polling()