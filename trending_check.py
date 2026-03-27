#!/usr/bin/env python3
import json
import subprocess

# Fetch trending data
result = subprocess.run(['curl', '-s', 'https://api.dexscreener.com/latest/dex/search?q=trending'], capture_output=True, text=True)
data = json.loads(result.stdout)

print('🔥 TRENDING MEMECOINS IN 30K-200K RANGE:')
print('=' * 50)

count = 0
for pair in data.get('pairs', []):
    mcap = pair.get('fdv', 0)
    if 30000 <= mcap <= 200000:
        symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
        name = pair.get('baseToken', {}).get('name', 'Unknown') 
        vol = pair.get('volume', {}).get('h24', 0)
        change = pair.get('priceChange', {}).get('h24', 0)
        buys = pair.get('txns', {}).get('h24', {}).get('buys', 0)
        sells = pair.get('txns', {}).get('h24', {}).get('sells', 0)
        
        print(f'{symbol} ({name}):')
        print(f'  Market Cap: ${mcap:,}')
        print(f'  24h Volume: ${vol:,}')
        print(f'  Price Change: {change:.2f}%')
        print(f'  Transactions: {buys} buys / {sells} sells')
        print()
        count += 1

if count == 0:
    print('No trending tokens in 30k-200k range')