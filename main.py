from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import logging

# ✅ Bot Token
BOT_TOKEN = "7880080432:AAHlXu-zaLY7NiTot91kpxtLdh2FkRWMpP4"

# ✅ Logs
logging.basicConfig(level=logging.INFO)

# ✅ Custom Buttons
def get_buttons():
    buttons = [
        [
            InlineKeyboardButton("🔁 Try another", callback_data="try_another"),
            InlineKeyboardButton("🔗 Visit Site", url="https://t.me/+6EuBTq2acxk1MjI1")
        ],
        [
            InlineKeyboardButton("📞 Contact Admin", url="https://t.me/AjayMore_Official")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# ✅ /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to Ajay Downloader Bot!*\n\n"
        "📥 Send me any link from:\n"
        "📸 Instagram, 📘 Facebook, 🐦 Twitter (X), 📌 Pinterest, 🧵 Threads\n\n"
        "🔗 Just paste the URL and I'll do the rest! 🚀",
        parse_mode="Markdown",
        reply_markup=get_buttons()
    )

# ✅ Handle Media Download
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("⚠️ Please send a valid URL starting with http or https.", reply_markup=get_buttons())
        return

    await update.message.reply_text("🔄 *Processing your link...*\nPlease wait ⏳", parse_mode="Markdown")

    try:
        api_url = f"https://api.vevioz.com/api/button/download?url={url}"
        res = requests.get(api_url)

        if res.status_code == 200 and (".mp4" in res.text or ".jpg" in res.text):
            links = [line for line in res.text.split('"') if line.startswith("http") and (".mp4" in line or ".jpg" in line)]
            if links:
                if ".mp4" in links[0]:
                    await update.message.reply_video(links[0], caption="🎬 Here's your video!", reply_markup=get_buttons())
                else:
                    await update.message.reply_photo(links[0], caption="🖼️ Here's your image!", reply_markup=get_buttons())
                return

        await update.message.reply_text("❌ *Failed to fetch media from the link.*\nTry another URL 🔁", parse_mode="Markdown", reply_markup=get_buttons())

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("🚫 *Oops! An error occurred while processing the link.*\nPlease try again later 🙏", parse_mode="Markdown", reply_markup=get_buttons())

# ✅ Start Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()
