#!/usr/bin/env python3
"""
Start Crypto Oracle Monitor
This script sets up continuous BTC/ETH/SOL monitoring
with real-time alerts to Telegram group -1002328055394
"""

import subprocess
import sys
import os

def check_setup():
    """Check if system is ready"""
    print("🔧 Checking setup...")
    
    # Check if required files exist
    required_files = ['crypto_oracle_monitor.py', 'telegram_config.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Test API connection
    try:
        import requests
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        if response.status_code == 200:
            print("✅ CoinGecko API accessible")
        else:
            print("❌ CoinGecko API failed")
            return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    return True

def configure_telegram():
    """Help user configure Telegram"""
    print("\n📝 Telegram Configuration")
    print("-" * 40)
    
    # Check current Telegram config
    try:
        from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
        
        if TELEGRAM_BOT_TOKEN.startswith("7768896203:") or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️ Telegram bot token needs configuration")
            print("1. Talk to @BotFather on Telegram")
            print("2. Create new bot with /newbot")
            print("3. Copy the bot token")
            print("4. Update TELEGRAM_BOT_TOKEN in telegram_config.py")
            print("5. Add the bot to your group: -1002328055394")
        else:
            print("✅ Telegram bot token configured")
            print(f"✅ Telegram channel: {TELEGRAM_CHAT_ID}")
            
    except Exception as e:
        print(f"❌ Telegram config error: {e}")

def start_monitor():
    """Start the crypto monitor"""
    print("\n🚀 Starting Crypto Oracle Monitor")
    print("-" * 40)
    
    try:
        # Run one-time scan first
        print("📊 Running initial market scan...")
        result = subprocess.run([sys.executable, "test_scan.py"], capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0:
            print(f"❌ Initial scan failed: {result.stderr}")
            return
        
        # Start continuous monitoring
        print("\n🔄 Starting continuous monitoring...")
        print("⚠️ Press Ctrl+C to stop")
        
        # Run main monitor
        subprocess.run([sys.executable, "crypto_oracle_monitor.py"])
        
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")
    except Exception as e:
        print(f"\n💥 Error starting monitor: {e}")

def main():
    """Main setup routine"""
    print("⚡ CRYPTO ORACLE MONITOR SETUP")
    print("=" * 50)
    print("Real-time BTC/ETH/SOL monitoring with Telegram alerts")
    print("Telegram group: -1002328055394")
    print("Timezone: GMT+8 (Asia/Manila)")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup checks failed")
        return
    
    # Configure Telegram
    configure_telegram()
    
    # Offer to start monitoring
    print("\n🎯 Ready to start monitoring")
    response = input("Start continuous monitoring now? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        start_monitor()
    else:
        print("\n📋 Available commands:")
        print("python3 test_scan.py     - One-time market scan")
        print("python3 crypto_oracle_monitor.py - Continuous monitoring")
        print("\n🚀 To start later: python3 start_monitor.py")

if __name__ == "__main__":
    main()