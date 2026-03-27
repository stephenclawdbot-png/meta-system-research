#!/usr/bin/env python3
"""
NBA Automation System - Automated scheduling for NBA updates
Handles morning briefings, live updates, and evening recaps
"""

import schedule
import time
import subprocess
import smtplib
from datetime import datetime
from nba_oracle import NBAOracle

def send_message(message, channel=None):
    """Send message via appropriate channel"""
    print(f"\n📨 Sending message:\n{message}")
    
    # For now, just print to console
    # In production, this would send to Telegram, Discord, etc.
    with open("nba_logs.txt", "a") as f:
        f.write(f"\n=== {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
        f.write(message)
        f.write("\n" + "="*50 + "\n")
    
    return True

def morning_briefing_job():
    """Morning briefing at 7:00 AM"""
    oracle = NBAOracle()
    briefing = oracle.generate_morning_briefing()
    return send_message(briefing)

def live_updates_job():
    """Live updates at 13:00, 15:00, 17:00"""
    oracle = NBAOracle()
    updates = oracle.generate_live_updates()
    return send_message(updates)

def evening_recap_job():
    """Evening recap at 21:00"""
    oracle = NBAOracle()
    recap = oracle.generate_evening_recap()
    return send_message(recap)

def setup_schedule():
    """Set up the automated schedule"""
    # Morning briefing at 7:00 AM daily
    schedule.every().day.at("07:00").do(morning_briefing_job)
    
    # Live updates during game hours
    schedule.every().day.at("13:00").do(live_updates_job)  # 1:00 PM
    schedule.every().day.at("15:00").do(live_updates_job)  # 3:00 PM
    schedule.every().day.at("17:00").do(live_updates_job)  # 5:00 PM
    
    # Evening recap at 9:00 PM
    schedule.every().day.at("21:00").do(evening_recap_job)
    
    print("NBA Automation Schedule Configuration:")
    print("📅 Morning Briefings: 7:00 AM daily")
    print("📊 Live Updates: 1:00 PM, 3:00 PM, 5:00 PM daily")
    print("📝 Evening Recaps: 9:00 PM daily")
    print("\nAutomation system ready!")

def manual_test():
    """Test all functions manually"""
    print("🧪 Manual Testing NBA Automation\n")
    
    print("1. Testing Morning Briefing:")
    morning_briefing_job()
    
    print("\n2. Testing Live Updates:")
    live_updates_job()
    
    print("\n3. Testing Evening Recap:")
    evening_recap_job()
    
    print("\n✅ All manual tests completed successfully!")

def run_scheduler():
    """Run the scheduler continuously"""
    setup_schedule()
    
    print("\n🔄 Starting NBA Automation Scheduler...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            manual_test()
        elif sys.argv[1] == "run":
            run_scheduler()
        elif sys.argv[1] == "briefing":
            morning_briefing_job()
        elif sys.argv[1] == "updates":
            live_updates_job()
        elif sys.argv[1] == "recap":
            evening_recap_job()
        else:
            print("Usage: python3 nba_automation.py [test|run|briefing|updates|recap]")
    else:
        manual_test()