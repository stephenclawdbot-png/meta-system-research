#!/usr/bin/env python3
import requests
import json
from datetime import datetime

url = 'https://api.dexscreener.com/latest/dex/tokens/new?limit=50'
response = requests.get(url)
data = response.json()

print(f'Scanning for tokens in $30k-$200k range at {datetime.now()}')
print('='*60)

count = 0

if data and isinstance(data, dict):
    pairs = data.get('pairs', [])
    for token in pairs:
        mcap = token.get('marketCap', 0)
        if mcap and 30000 <= mcap <= 200000:
            count += 1
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
            volume = token.get('volume', {}).get('h24', 0)
            price_change = token.get('priceChange', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            print(f'{count}. {symbol}')
            print(f'   MCap: ${mcap:,.0f}')
            print(f'   24h Vol: ${volume:,.0f}')
            print(f'   Price Change: {price_change:.1f}%')
            print(f'   Liquidity: ${liquidity:,.0f}')
            print(f'   URL: {token.get("url", "")}')
            
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            if buys > 0 or sells > 0:
                buy_ratio = buys / (buys + sells) * 100
                print(f'   Buy Ratio: {buy_ratio:.1f}% ({buys}/{sells})')
            
            print('---')

print(f'\nTotal tokens found: {count}')