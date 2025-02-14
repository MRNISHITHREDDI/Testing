import requests
import asyncio
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Replace with your bot token and channel ID
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
TELEGRAM_CHANNEL_ID = '@your_channel_username'  # Or use the channel ID (e.g., -1001234567890)

# API endpoints
ISSUE_API_URL = 'https://imgametransit.com/api/webapi/GetGameIssue'
RESULT_API_URL = 'https://imgametransit.com/api/webapi/GetNoaverageEmerdList'

# Payload for the API requests
PAYLOAD = {
    "typeId": 1,
    "language": 0,
    "random": "f1af2f5123204df1beb5106afbbe237f",
    "signature": "38412CA604FE512BD418DE6E21448BA3",
    "timestamp": 1739526471
}

HEADERS = {
    'Content-Type': 'application/json'
}

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def fetch_data():
    try:
        # Fetch the latest issue data
        issue_response = requests.post(ISSUE_API_URL, json=PAYLOAD, headers=HEADERS)
        issue_data = issue_response.json()

        # Fetch the latest result data
        result_response = requests.post(RESULT_API_URL, json=PAYLOAD, headers=HEADERS)
        result_data = result_response.json()

        # Extract period number and result
        period_number = issue_data['data']['issueNumber']
        latest_result = result_data['data']['list'][0]  # Get the latest result

        # Predict red/green based on the latest result
        result_number = int(latest_result['number'])
        prediction = 'Red' if result_number in [1, 2, 3, 4, 6, 7] else 'Green'

        # Prepare the prediction message
        prediction_message = (
            f"🎰 **TC LOTTERY 1 MINUTE WINGO** 🎰\n\n"
            f"PERIOD ID: {period_number}\n"
            f"PREDICTION: {prediction}\n"
            f"MAINTAIN FUND UPTO LEVEL 8\n"
        )

        # Prepare the result message
        result_message = (
            f"🎉 **RESULT UPDATE** 🎉\n\n"
            f"PERIOD ID: {latest_result['issueNumber']}\n"
            f"RESULT: {latest_result['number']} ({latest_result['colour']})\n"
            f"STATUS: WIN 🎉🎉🎉\n"
        )

        # Send the prediction message to the Telegram channel
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=prediction_message, parse_mode='Markdown')

        # Send the result message to the Telegram channel
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=result_message, parse_mode='Markdown')

        print("Messages sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Schedule the fetch_data function to run every minute
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_data, 'interval', minutes=1)
    scheduler.start()

    # Keep the script running
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
