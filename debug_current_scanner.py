#!/usr/bin/env python3
"""Quick debug to see what the scanner is doing"""

import os
import json

def check_scanner_status():
    print("Checking scanner status...")
    
    # Check if scanner.log exists
    if os.path.exists('scanner.log'):
        with open('scanner.log', 'r') as f:
            lines = f.readlines()
            print(f"Log file has {len(lines)} lines")
            if len(lines) > 5:
                print("Last 5 lines:")
                for line in lines[-5:]:
                    print(line.strip())
    else:
        print("No scanner.log file")
    
    # Check if any alert files exist
    alert_files = [f for f in os.listdir('.') if 'alert' in f.lower()]
    print(f"\nAlert files found: {alert_files}")
    
    # Check if crypto_alerts.json exists
    if os.path.exists('crypto_alerts.json'):
        with open('crypto_alerts.json', 'r') as f:
            try:
                data = json.load(f)
                print(f"\nAlert data: {json.dumps(data, indent=2)[:500]}...")
            except:
                print("Error reading crypto_alerts.json")

if __name__ == "__main__":
    check_scanner_status()