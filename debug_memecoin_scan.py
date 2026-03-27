#!/usr/bin/env python3
"""Debug scanner to see all tokens"""

import requests
import json
from datetime import datetime

def fetch_all_tokens():
    """Fetch all Solana tokens"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            print(f"Total pairs: {len(pairs)}")
            print("-" * 50)
            
            for i, pair in enumerate(pairs, 1):
                mcap = pair.get('marketCap', 0)
                base_token = pair.get('baseToken', {})
                symbol = base_token.get('symbol', 'Unknown')
                name = base_token.get('name', 'Unknown')
                
                volume_24h = pair.get('volume', {}).get('h24', 0)
                price_change = pair.get('priceChange', {}).get('h24', 0)
                liquidity = pair.get('liquidity', {}).get('usd', 0)
                
                print(f"{i}. {symbol} (MCap: ${mcap:,})")
                print(f"   Name: {name}")
                print(f"   Volume: ${volume_24h:,.2f}")
                print(f"   Change: {price_change:.2f}%")
                print(f"   Liquidity: ${liquidity:,}")
                print()
                 
        else:
            print(f"API error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("🔍 DEBUG MEMECOIN SCANNER")
    print("=" * 60)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')}")
    print()
    
    fetch_all_tokens()

if __name__ == "__main__":
    main()