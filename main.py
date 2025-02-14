from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your new Telegram bot.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How can I help you?')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.run_polling()

if __name__ == '__main__':
    main()
