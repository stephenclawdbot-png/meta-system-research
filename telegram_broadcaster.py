#!/usr/bin/env python3
"""
Telegram broadcaster for memecoin alpha alerts
Sends formatted messages to specified Telegram group
"""

import asyncio
from telegram import Bot
from telegram.error import TelegramError
import logging

class TelegramBroadcaster:
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        
    async def send_message(self, text: str) -> bool:
        """Send message to Telegram group"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logging.info(f"Message sent to Telegram group {self.chat_id}")
            return True
        except TelegramError as e:
            logging.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False

async def broadcast_alpha_alert(broadcaster: TelegramBroadcaster, message: str):
    """Broadcast alpha alert to Telegram"""
    return await broadcaster.send_message(message)

if __name__ == "__main__":
    # Example usage
    # You need to set TELEGRAM_BOT_TOKEN environment variable
    import os
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = '-1002328055394'  # Your group ID
    
    if token:
        broadcaster = TelegramBroadcaster(token, chat_id)
        test_message = "🧪 Test message from memecoin alpha scanner"
        asyncio.run(broadcaster.send_message(test_message))
    else:
        print("Please set TELEGRAM_BOT_TOKEN environment variable")