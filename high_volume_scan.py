#!/usr/bin/env python3
import requests
import json
from datetime import datetime

print('🔍 HIGH-VOLUME MEMECOIN SCAN (30K-200K MCAP)')
print('='*50)
print()

# Fetch trending memecoins with higher volume focus
response = requests.get('https://api.dexscreener.com/latest/dex/tokens/trending')
try:
    if response.status_code == 200:
        tokens = response.json()
        if 'pairs' in tokens:
            filtered = []
            for token in tokens['pairs']:
                mcap = token.get('marketCap', 0)
                volume = token.get('volume', {}).get('h24', 0)
                if 30000 <= mcap <= 200000 and volume > 5000:  # Higher volume requirement
                    filtered.append({
                        'symbol': token['baseToken']['symbol'],
                        'name': token['baseToken']['name'],
                        'mcap': mcap,
                        'volume': volume,
                        'price': token['priceUsd'],
                        'url': token['url'],
                        'chain': token.get('chainId', 'Unknown')
                    })
            
            print(f'🔥 HIGH-VOLUME ALPHA GEMS (Volume > $5K)')
            print('-' * 40)
            if filtered:
                for i, gem in enumerate(filtered[:5], 1):
                    print(f'{i}. 💎 {gem[\"symbol\"]} - {gem[\"name\"]}')
                    print(f'   📊 MCap: ${gem[\"mcap\"]:,}')
                    print(f'   📈 24h Volume: ${gem[\"volume\"]:,}')
                    print(f'   🔗 {gem[\"url\"]}')
                    print()
            else:
                print('📉 No high-volume gems found in target range')
            print()
    else:
        print('❌ Failed to fetch trending tokens')
except Exception as e:
    print(f'Error: {e}')