#!/usr/bin/env python3
import requests
from datetime import datetime

# Enhanced alpha scanning with memecoin-specific filters
url = 'https://api.dexscreener.com/latest/dex/search?q=solana'
response = requests.get(url)
data = response.json()

filtered_tokens = []

for token in data.get('pairs', []):
    mcap = token.get('fdv', 0)
    symbol = token.get('baseToken', {}).get('symbol', '').lower()
    
    # Focus on actual memecoins (not SOL, ETH, etc.)
    if mcap < 30000 or mcap > 200000:
        continue
    
    # Skip major tokens that aren't memecoins
    if symbol in ['sol', 'solana', 'eth', 'ethereum', 'btc', 'bitcoin']:
        continue
    
    token_info = {
        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
        'name': token.get('baseToken', {}).get('name', 'Unknown'),
        'mcap': mcap,
        'volume_24h': token.get('volume', {}).get('h24', 0),
        'price': token.get('priceUsd', 0),
        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
        'url': token.get('url', ''),
        'dex': token.get('dexId', ''),
        'trades_24h': token.get('txns', {}).get('h24', {}).get('buys', 0) + token.get('txns', {}).get('h24', {}).get('sells', 0)
    }
    filtered_tokens.append(token_info)

print('🚀 MEMECOIN ALPHA DETECTION REPORT')
print('Scan Time:', datetime.now().strftime('%A, %B %d, %Y — %I:%M %p Asia/Manila'))
print('Target: Sub-$200k mcap gems before mainstream attention')
print('='*60)

if not filtered_tokens:
    print('⚠️ No pure memecoins found in 30k-200k range (filtered out major tokens)')
else:
    # Sort by volume momentum
    filtered_tokens.sort(key=lambda x: x['volume_24h'] / max(1, x['mcap']), reverse=True)
    
    print(f'🎯 Found {len(filtered_tokens)} potential alpha memecoins:')
    
    for i, token in enumerate(filtered_tokens[:10], 1):
        vol_mcap_ratio = token['volume_24h'] / token['mcap'] * 100 if token['mcap'] > 0 else 0
        
        print(f'{i}. {token["symbol"]} ({token["name"]})')
        print(f'   MCap: ${token["mcap"]:,.0f} | Vol24h: ${token["volume_24h"]:,.0f}')
        print(f'   Vol/MCap: {vol_mcap_ratio:.1f}% | Change: {token["price_change_24h"]}%')
        print(f'   Dex: {token["dex"]} | Trades24h: {token["trades_24h"]}')
        print(f'   Link: {token["url"]}')
        print()

# Market insights
print('📊 MARKET INSIGHTS:')
print('-' * 20)
print('Low market cap phase (<$200k) is prime alpha territory')
print('Look for tokens with high volume/interest relative to mcap')
print('Watch for social momentum indicators next')
print('⚠️ High risk - significant capital can be lost quickly')