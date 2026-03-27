#!/usr/bin/env python3
import time
import subprocess
import sys
from datetime import datetime

def run_scan():
    """Run one scan cycle"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    print(f"\n🎯 MEMECOIN SCAN CYCLE - {timestamp}")
    print("=" * 50)
    
    try:
        # Run the scanner
        result = subprocess.run([sys.executable, 'advanced_memecoin_scanner.py'], 
                               capture_output=True, text=True)
        
        print("Scan completed successfully!")
        return True
        
    except Exception as e:
        print(f"Scan failed: {e}")
        return False

def main():
    """Main monitoring loop"""
    print("🚀 AUTO MEMECOIN MONITOR STARTED")
    print("📊 Scanning for promising memecoins every 30 minutes")
    print("📤 Broadcasting alerts to Telegram group: -1002328055394")
    print("⏰ Timezone: GMT+8 (Asia/Manila)")
    print("💡 Press Ctrl+C to stop")
    print("-" * 60)
    
    scan_count = 0
    
    while True:
        scan_count += 1
        print(f"\n🔄 Scan #{scan_count} starting...")
        
        success = run_scan()
        
        if success:
            print(f"✅ Scan #{scan_count} completed")
        else:
            print(f"❌ Scan #{scan_count} failed")
        
        # Wait 30 minutes before next scan
        print("⏳ Waiting 30 minutes for next scan...")
        time.sleep(1800)  # 30 minutes in seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Memecoin monitor stopped")
        print("Thanks for using the memecoin alpha scanner!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Restarting in 10 seconds...")
        time.sleep(10)
        main()