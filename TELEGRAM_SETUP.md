# Telegram Bot Setup Instructions

To enable automatic Telegram alerts, you need to configure a Telegram bot:

## Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to create a new bot
3. Choose a name for your bot (e.g., "Memecoin Alpha Scanner")
4. Choose a username ending with "bot" (e.g., "memecoinalphascanner_bot")
5. Save the bot token that BotFather provides

## Step 2: Add Bot to Group

1. Add the bot to your Telegram group
2. Make sure the bot has permission to send messages

## Step 3: Configure Scanner

Update `telegram_config.py` with your bot token:

```python
# Replace YOUR_BOT_TOKEN_HERE with your actual token
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

The chat ID (`-1002328055394`) is already set for your group.

## Step 4: Test the Bot

Run a test to verify the bot works:

```bash
python3 -c "from telegram_config import send_telegram_message; send_telegram_message('Test message from memecoin scanner')"
```

## Security Notes

- Never share your bot token publicly
- Keep `telegram_config.py` secure
- The bot only sends messages, cannot read messages
- Alerts will only be sent for genuine opportunities meeting strict criteria

## Current Configuration

- **Chat ID:** `-1002328055394` (your Telegram group)
- **Criteria:** 30k-100k market cap, >$1k volume, <24h age, buy ratio >60%
- **Frequency:** Alerts sent immediately when criteria met
- **Duplicates:** Same token alerts blocked for 24 hours