#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def scan_query(query):
    url = f'https://api.dexscreener.com/latest/dex/search/?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return {'pairs': []}
    
    return {'pairs': []}

queries = ['doge', 'pepe', 'floki', 'shib', 'elon', 'cat', 'dog', 'based', 'degen', 'ape', 'wagmi']
all_gems = []

for query in queries:
    print(f'Scanning: {query}')
    data = scan_query(query)
    
    for pair in data.get('pairs', [])[:20]:
        mcap = pair.get('marketCap', 0)
        symbol = pair.get('baseToken', {}).get('symbol', '').upper()
        
        # Skip major tokens
        if symbol in ['SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'WETH', 'WBTC', 'BNB', 'AVAX']:
            continue
            
        if 30000 <= mcap <= 200000:
            volume = pair.get('volume', {}).get('h24', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buy_ratio = (txns.get('buys', 0) / max(txns.get('buys', 0) + txns.get('sells', 0), 1)) * 100
            
            # Only keep tokens with meaningful activity
            if volume > 50 and buy_ratio > 40:
                gem = {
                    'symbol': symbol,
                    'mcap': mcap,
                    'volume': volume,
                    'price_change': price_change,
                    'buy_ratio': buy_ratio,
                    'url': pair.get('url', ''),
                    'chain': pair.get('chainId', 'Unknown'),
                    'age': pair.get('pairCreatedAt', '')
                }
                
                # Check if already in list
                if not any(g['url'] == gem['url'] for g in all_gems):
                    all_gems.append(gem)

# Sort by volume
all_gems.sort(key=lambda x: x['volume'], reverse=True)

print(f'\\nSCAN RESULTS - {datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")}')
print(f'Total tokens found: {len(all_gems)}')
print()

if all_gems:
    for i, gem in enumerate(all_gems[:10], 1):
        print(f'{i}. {gem["symbol"]}')
        print(f'   MCap: ${gem["mcap"]:,} | Volume: ${gem["volume"]:,.0f}')
        print(f'   24h: {gem["price_change"]:+.1f}% | Buy Ratio: {gem["buy_ratio"]:.1f}%')
        print(f'   Chain: {gem["chain"]}')
        print(f'   Dex: {gem["url"]}')
        if i < len(all_gems[:10]):
            print()
else:
    print('No alpha gems found in target range')

print('\\n⚠️ Current market appears quiet for sub 30k-200k mcap memecoins')
print('Suggest waiting for US trading hours or trying broader criteria')