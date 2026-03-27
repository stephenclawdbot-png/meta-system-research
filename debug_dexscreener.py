#!/usr/bin/env python3
import requests

def fetch_raw_dexscreener():
    """Fetch raw DexScreener data to see what's available"""
    url = "https://api.dexscreener.com/latest/dex/search?q=solana&limit=50"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            print("🔍 RAW DEXSCREENER DATA:")
            print(f"Found {len(data.get('pairs', []))} pairs\n")
            
            for i, pair in enumerate(data.get('pairs', [])[:10]):
                base_token = pair.get('baseToken', {})
                print(f"#{i+1}:")
                print(f"  Symbol: {base_token.get('symbol', 'Unknown')}")
                print(f"  Name: {base_token.get('name', 'Unknown')}")
                print(f"  MCap: ${pair.get('fdv', pair.get('marketCap', 0)):,}")
                print(f"  Volume: ${pair.get('volume', {}).get('h24', 0):,}")
                print(f"  DEX: {pair.get('dexId', 'Unknown')}")
                print(f"  URL: {pair.get('url', 'Unknown')}")
                print()
            
            # Show MCap distribution
            mcaps = [p.get('fdv', p.get('marketCap', 0)) for p in data.get('pairs', [])]
            valid_mcaps = [m for m in mcaps if m > 0]
            
            print(f"\n📊 MCAP DISTRIBUTION:")
            print(f"Total pairs: {len(mcaps)}")
            print(f"Valid MCaps: {len(valid_mcaps)}")
            print(f"Min MCap: ${min(valid_mcaps):,}" if valid_mcaps else "No valid MCaps")
            print(f"Max MCap: ${max(valid_mcaps):,}" if valid_mcaps else "No valid MCaps")
            print(f"Average MCap: ${sum(valid_mcaps)/len(valid_mcaps):,}" if valid_mcaps else "No avg")
            
            # Count in our target range
            target_range = [m for m in valid_mcaps if 30000 <= m <= 200000]
            print(f"Target Range (30K-200K): {len(target_range)} tokens")
            
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_raw_dexscreener()