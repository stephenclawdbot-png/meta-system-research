#!/usr/bin/env python3
"""
Telegram Bot Configuration
You need to create a bot and get these credentials
"""

# Telegram Bot Configuration - REAL CRYPTO ORACLE
# Configure this with your actual bot token from @BotFather
TELEGRAM_BOT_TOKEN = "7768896203:AAFqmGSrNfN0xdhVLdV800AzdQt8zpzYHSM"  # Replace with YOUR token

# Telegram Chat ID - Your crypto alerts group
TELEGRAM_CHAT_ID = "-1002328055394"

def send_telegram_message(message):
    """Send message via Telegram bot"""
    if TELEGRAM_BOT_TOKEN == "7768896203:AAFqmGSrNfN0xdhVLdV800AzdQt8zpzYHSM" or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ Telegram bot not configured. Alert logged locally.")
        return False
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram message sent successfully")
            return True
        else:
            print(f"❌ Telegram API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False