#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Search for newly listed tokens on various chains
search_urls = [
    "https://api.dexscreener.com/latest/dex/search?q=solana&limit=50",
    "https://api.dexscreener.com/latest/dex/search?q=ethereum&limit=30",
    "https://api.dexscreener.com/latest/dex/search?q=base&limit=30",
    "https://api.dexscreener.com/latest/dex/search?q=polygon&limit=20",
    "https://api.dexscreener.com/latest/dex/search?q=arbitrum&limit=20"
]

print(f'Scanning for tokens in $30k-$200k range at {datetime.now()}')
print('='*60)

count = 0
found_tokens = []

for url in search_urls:
    try:
        response = requests.get(url)
        data = response.json()
        
        if data and isinstance(data, dict) and 'pairs' in data and isinstance(data['pairs'], list):
            for token in data['pairs']:
                mcap = token.get('marketCap', 0)
                if mcap and 30000 <= mcap <= 200000:
                    symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
                    # Skip duplicates
                    if symbol not in found_tokens:
                        count += 1
                        found_tokens.append(symbol)
                        
                        volume = token.get('volume', {}).get('h24', 0)
                        price_change = token.get('priceChange', {}).get('h24', 0)
                        liquidity = token.get('liquidity', {}).get('usd', 0)
                        chain = token.get('chainId', 'Unknown')
                        
                        print(f'{count}. {symbol} ({chain})')
                        print(f'   MCap: ${mcap:,.0f}')
                        print(f'   24h Vol: ${volume:,.0f}')
                        print(f'   Price Change: {price_change:.1f}%')
                        print(f'   Liquidity: ${liquidity:,.0f}')
                        print(f'   URL: {token.get(\"url\", \"\")}')
                        
                        txns = token.get('txns', {}).get('h24', {})
                        buys = txns.get('buys', 0)
                        sells = txns.get('sells', 0)
                        if buys > 0 or sells > 0:
                            buy_ratio = buys / (buys + sells) * 100
                            print(f'   Buy Ratio: {buy_ratio:.1f}% ({buys}/{sells})')
                        
                        print('---')
    except Exception as e:
        print(f'Error processing {url}: {e}')

print(f'\nTotal tokens found: {count}')