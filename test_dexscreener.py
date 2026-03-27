#!/usr/bin/env python3
import requests
import json

# Test DexScreener API endpoints
test_urls = [
    'https://api.dexscreener.com/latest/dex/tokens/trending',
    'https://api.dexscreener.com/latest/dex/tokens/new',
    'https://api.dexscreener.com/latest/dex/search?q=solana', 
    'https://api.dexscreener.com/latest/dex/search?q=ethereum'
]

for url in test_urls:
    print(f"\nTesting: {url}")
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                if 'pairs' in data:
                    pairs = data['pairs']
                    if pairs:
                        print(f"Found {len(pairs)} pairs")
                        # Show first 2 pairs
                        for i, pair in enumerate(pairs[:2], 1):
                            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                            mcap = pair.get('marketCap', 0)
                            print(f"  {i}. {symbol} - MCap: ${mcap:,}")
                    else:
                        print("No pairs found")
                else:
                    print("No 'pairs' key in response")
                    print("Keys:", list(data.keys()))
            else:
                print(f"Response type: {type(data)}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")