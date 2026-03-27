#!/usr/bin/env python3
import schedule
import time
from datetime import datetime
import subprocess
import sys

def run_memecoin_scan():
    """Run the memecoin scanner and handle output"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔍 Automated Scan Started at {timestamp}")
        
        # Run the advanced scanner
        result = subprocess.run([sys.executable, 'advanced_memecoin_scanner.py'], 
                               capture_output=True, text=True)
        
        # Log the results
        log_entry = f"\n=== MEMECOIN SCAN ===\nTime: {timestamp}\n"
        log_entry += f"Return Code: {result.returncode}\n"
        log_entry += f"Output:\n{result.stdout}\n"
        
        if result.stderr:
            log_entry += f"Errors:\n{result.stderr}\n"
        
        # Append to daily log
        with open(f'memory/{datetime.now().strftime("%Y-%m-%d")}_memecoin.log', 'a') as f:
            f.write(log_entry)
            
        print(f"✅ Scan completed at {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Scan failed: {e}")

def setup_schedule():
    """Set up the scanning schedule"""
    # Scan every 30 minutes during active trading hours
    schedule.every(30).minutes.do(run_memecoin_scan)
    
    # More frequent scans during peak hours (9 AM - 11 PM GMT+8)
    schedule.every(15).minutes.between("09:00", "23:00").do(run_memecoin_scan)
    
    print("🎯 Automated Memecoin Monitor Started")
    print("📅 Schedule:")
    print("   • Every 30 minutes (standard)")
    print("   • Every 15 minutes during 9 AM - 11 PM GMT+8")
    print("🚀 Ready to broadcast hot memecoin alerts!")
    
def main():
    """Main monitoring loop"""
    setup_schedule()
    
    # Run initial scan
    run_memecoin_scan()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Memecoin monitor stopped by user")
    except Exception as e:
        print(f"\n💥 Monitor crashed: {e}")
        print("Restarting in 10 seconds...")
        time.sleep(10)
        main()