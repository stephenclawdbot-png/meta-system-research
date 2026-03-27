#!/usr/bin/env python3
"""
Main runner for continuous memecoin alpha scanner with Telegram broadcasting
"""

import asyncio
import os
import logging
from memecoin_scanner import MemecoinScanner
from telegram_broadcaster import TelegramBroadcaster, broadcast_alpha_alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler()
    ]
)

class AlphaScannerRunner:
    def __init__(self):
        self.scanner = MemecoinScanner()
        self.broadcaster = None
        self.setup_telegram()
        
    def setup_telegram(self):
        """Setup Telegram broadcaster if token is available"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            self.broadcaster = TelegramBroadcaster(token, '-1002328055394')
            logging.info("Telegram broadcaster configured")
        else:
            logging.warning("TELEGRAM_BOT_TOKEN not set - alerts will be logged locally only")
    
    async def process_token(self, token_data):
        """Process and broadcast token alert"""
        token, message = token_data
        
        logging.info(f"\n🎯 ALPHA FOUND:")
        logging.info(f"Token: {token.get('baseToken', {}).get('symbol', 'Unknown')}")
        logging.info(f"Market Cap: ${token.get('marketCap', 0):,.0f}")
        logging.info(f"Volume: ${token.get('volume', {}).get('h24', 0):,.0f}")
        logging.info(f"Buy Ratio: {token.get('buyRatio', 0):.1f}%")
        
        # Broadcast to Telegram
        if self.broadcaster:
            success = await broadcast_alpha_alert(self.broadcaster, message)
            if success:
                logging.info("✅ Alert broadcasted to Telegram")
            else:
                logging.error("❌ Failed to broadcast alert")
    
    async def run_continuous(self):
        """Run scanner continuously"""
        logging.info("🚀 Starting continuous alpha scanner with Telegram broadcasting")
        logging.info("Scanner criteria:")
        logging.info("- Market Cap: $30K - $100K")
        logging.info("- Minimum Volume: $1K")
        logging.info("- Maximum Age: 24h")
        logging.info("- Buy Ratio: >60%")
        logging.info("- Organic Growth Pattern")
        
        try:
            for token_data in self.scanner.run_continuous_scan():
                await self.process_token(token_data)
        except KeyboardInterrupt:
            logging.info("Scanner stopped by user")
        except Exception as e:
            logging.error(f"Scanner error: {e}")

async def main():
    runner = AlphaScannerRunner()
    await runner.run_continuous()

if __name__ == "__main__":
    # Install dependencies if needed
    try:
        import requests
        import telegram
    except ImportError:
        logging.info("Installing dependencies...")
        import subprocess
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        logging.info("Dependencies installed")
    
    # Run the scanner
    asyncio.run(main())