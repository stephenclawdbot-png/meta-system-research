#!/usr/bin/env python3
"""
NBA Monitoring System - Complete integration with Telegram
Combines oracle, automation, picks, and broadcasting
"""

import asyncio
import aiohttp
import schedule
import time
from datetime import datetime
from nba_oracle import NBAOracle
from nba_picks import NBAPicks
import subprocess

class NBAMonitor:
    def __init__(self, telegram_bot_token=None, telegram_chat_id=None):
        self.oracle = NBAOracle()
        self.picks = NBAPicks()
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
    
    async def send_telegram_message(self, message):
        """Send message to Telegram channel"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            print(f"📢 Message (Telegram not configured):\n{message}")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload) as response:
                    if response.status == 200:
                        print("✅ Message sent to Telegram")
                        return True
                    else:
                        print(f"❌ Failed to send Telegram message: {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False
    
    def send_message(self, message, use_telegram=False):
        """Send message via appropriate channel"""
        print(f"\n📢 Broadcasting:\n{message}")
        
        # Log to file
        with open("nba_broadcast_log.txt", "a") as f:
            f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
            f.write(message)
            f.write("\n" + "="*50 + "\n")
        
        # Send to Telegram if configured
        if use_telegram and self.telegram_bot_token and self.telegram_chat_id:
            asyncio.run(self.send_telegram_message(message))
        
        return True
    
    def morning_briefing(self):
        """Generate and send morning briefing"""
        briefing = self.oracle.generate_morning_briefing()
        picks = self.picks.generate_gambling_picks()
        
        full_message = f"{briefing}\n\n{picks}"
        return self.send_message(full_message)
    
    def live_updates(self):
        """Generate and send live updates"""
        updates = self.oracle.generate_live_updates()
        return self.send_message(updates)
    
    def evening_recap(self):
        """Generate and send evening recap"""
        recap = self.oracle.generate_evening_recap()
        picks_recap = "🏆 Today's Results Recap 🏆\n\n"
        picks_recap += f"📊 Generated: {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}\n"
        picks_recap += "Analysis of today's picks performance\n"
        
        full_message = f"{recap}\n\n{picks_recap}"
        return self.send_message(full_message)
    
    def setup_schedule(self, use_telegram=False):
        """Set up automated schedule"""
        # Morning briefing at 7:00 AM
        schedule.every().day.at("07:00").do(
            lambda: self.morning_briefing()
        )
        
        # Live updates during peak game hours
        schedule.every().day.at("13:00").do(
            lambda: self.live_updates()
        )
        schedule.every().day.at("15:00").do(
            lambda: self.live_updates()
        )
        schedule.every().day.at("17:00").do(
            lambda: self.live_updates()
        )
        
        # Evening recap at 9:00 PM
        schedule.every().day.at("21:00").do(
            lambda: self.evening_recap()
        )
        
        print("🏀 NBA Monitoring System Schedule:")
        print("⏰ Morning Briefings: 7:00 AM daily")
        print("📊 Live Updates: 1:00 PM, 3:00 PM, 5:00 PM daily") 
        print("📝 Evening Recaps: 9:00 PM daily")
        print(f"📱 Telegram Integration: {'✅ Enabled' if use_telegram else '❌ Disabled'}")
        print("\n🔄 Automation system ready!")
    
    def run_scheduler(self):
        """Run the scheduler continuously"""
        print("🏀 Starting NBA Monitoring System...")
        print("Press Ctrl+C to stop\n")
        
        # Run initial briefing
        self.morning_briefing()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def test_system():
    """Test the complete NBA monitoring system"""
    print("🧪 Testing NBA Monitoring System...\n")
    
    monitor = NBAMonitor()
    
    print("1. Testing Morning Briefing:")
    monitor.morning_briefing()
    
    print("\n2. Testing Live Updates:")
    monitor.live_updates()
    
    print("\n3. Testing Evening Recap:")
    monitor.evening_recap()
    
    print("\n✅ NBA Monitoring System Test Complete!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_system()
        elif sys.argv[1] == "run":
            monitor = NBAMonitor()
            monitor.setup_schedule()
            monitor.run_scheduler()
        elif sys.argv[1] == "briefing":
            monitor = NBAMonitor()
            monitor.morning_briefing()
        elif sys.argv[1] == "updates":
            monitor = NBAMonitor()
            monitor.live_updates()
        elif sys.argv[1] == "recap":
            monitor = NBAMonitor()
            monitor.evening_recap()
        else:
            print("Usage: python3 nba_monitor.py [test|run|briefing|updates|recap]")
    else:
        test_system()