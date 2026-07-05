import os
from dotenv import load_dotenv

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
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=user_text
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"خطا: {e}")

# ----------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot is running...")
    app.run_polling()

# ----------------
if __name__ == "__main__":
    main()