import os
import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Try another", callback_data="try_another")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/AjayMore_Official")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to Ajay Downloader Bot!*\n\n"
        "📥 Send me any link from:\n"
        "📸 Instagram, 📘 Facebook, 🐦 Twitter, 📌 Pinterest, 🧵 Threads\n\n"
        "🔗 Just paste the URL and I'll do the rest! 🚀",
        parse_mode="Markdown",
        reply_markup=get_buttons()
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("⚠️ Please send a valid URL starting with http or https.")
        return

    await update.message.reply_text("🔄 Downloading... Please wait ⏳")

    try:
        api_url = f"https://api.vevioz.com/api/button/download?url={url}"
        response = requests.get(api_url)

        if ".mp4" in response.text:
            link = response.text.split('"')[1]
            await update.message.reply_video(link, caption="🎬 Here is your video!", reply_markup=get_buttons())
        elif ".jpg" in response.text:
            link = response.text.split('"')[1]
            await update.message.reply_photo(link, caption="🖼️ Here is your image!", reply_markup=get_buttons())
        else:
            await update.message.reply_text("❌ Couldn't find downloadable media in this link.")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ An error occurred while processing the link.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()
