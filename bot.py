import os
import threading
from dotenv import load_dotenv
from flask import Flask

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from google import genai

# ----------------
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ----------------
client = genai.Client(api_key=GEMINI_API_KEY)

# ----------------
# Flask (برای Render)
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Telegram Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

# ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=user_text
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"خطا: {e}")

# ----------------
def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Telegram Bot is running...")
    app.run_polling()

# ----------------
if __name__ == "__main__":
    # اجرای وب‌سرور در یک Thread
    threading.Thread(target=run_web).start()

    # اجرای ربات
    run_bot()
