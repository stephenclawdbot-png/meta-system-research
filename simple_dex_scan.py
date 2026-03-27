#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_popular():
    """Try alternative DexScreener endpoints"""
    endpoints = [
        "https://api.dexscreener.com/latest/dex/tokens/newest",
        "https://api.dexscreener.com/latest/dex/tokens",
        "https://api.dexscreener.com/latest/dex"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Trying endpoint: {endpoint}")
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data}")
                return data
                
        except Exception as e:
            print(f"Error with {endpoint}: {e}")
    
    return {}

def main():
    print("🧠 DEXSCREENER ALPHA SCAN")
    print("=" * 40)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print()
    
    data = fetch_dexscreener_popular()
    
    if data:
        print("✅ API Response received")
        print(json.dumps(data, indent=2)[:500] + "...")
    else:
        print("❌ Unable to fetch DexScreener data")
        print("Trying alternative approach...")
        
        # Try direct browser approach
        print("\n💡 Note: DexScreener API appears to be unstable")
        print("Consider using web scraping or browser automation")

if __name__ == "__main__":
    main()