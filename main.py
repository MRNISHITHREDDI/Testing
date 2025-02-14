from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import os
import threading
import asyncio

# Flask app for health checks
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

# Telegram bot code
TOKEN = os.getenv('TOKEN')  # Read token from environment variable

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your new Telegram bot.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('How can I help you?')

def run_bot():
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Build and run the bot
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help))
    bot_app.run_polling()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Start the Flask app for health checks
    app.run(host='0.0.0.0', port=8000)
