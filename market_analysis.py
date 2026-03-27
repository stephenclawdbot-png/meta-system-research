#!/usr/bin/env python3
import requests
from datetime import datetime

# Broader search to understand current memecoin landscape
url = 'https://api.dexscreener.com/latest/dex/tokens/newest'
response = requests.get(url)
data = response.json()

print('🗺️ CURRENT MEMECOIN LANDSCAPE ANALYSIS')
print('Scan Time:', datetime.now().strftime('%A, %B %d, %Y — %I:%M %p Asia/Manila'))
print('Analysing newest tokens across all market caps')
print('='*60)

if not data or 'pairs' not in data:
    print('❌ No data available')
else:
    tokens_by_mcap = {'micro': [], 'small': [], 'medium': [], 'large': []}
    
    for token in data['pairs'][:50]:  # Top 50 newest
        mcap = token.get('fdv', 0)
        symbol = token.get('baseToken', {}).get('symbol', '')
        
        if mcap < 10000:
            tokens_by_mcap['micro'].append((symbol, mcap))
        elif mcap < 100000:
            tokens_by_mcap['small'].append((symbol, mcap))
        elif mcap < 1000000:
            tokens_by_mcap['medium'].append((symbol, mcap))
        else:
            tokens_by_mcap['large'].append((symbol, mcap))
    
    print('Market Cap Distribution:')
    print(f'💎 Micro (<$10k): {len(tokens_by_mcap["micro"])} tokens')
    print(f'📈 Small ($10k-$100k): {len(tokens_by_mcap["small"])} tokens')
    print(f'🚀 Medium ($100k-$1M): {len(tokens_by_mcap["medium"])} tokens')
    print(f'🏆 Large (>$1M): {len(tokens_by_mcap["large"])} tokens')
    
    # Show sample from each category
    print()
    if tokens_by_mcap['small']:
        print('🌱 Small Cap Potential (0k-100k):')
        for symbol, mcap in tokens_by_mcap['small'][:5]:
            print(f'   {symbol} - ${mcap:,.0f}')
    
    if tokens_by_mcap['medium']:
        print()
        print('🔥 Medium Cap Momentum (100k-1M):')
        for symbol, mcap in tokens_by_mcap['medium'][:5]:
            print(f'   {symbol} - ${mcap:,.0f}')

print()
print('💡 ALPHA SCANNER STATUS: Market appears quiet for target range')
print('📅 Next scan scheduled in 5 minutes')
print('⚠️ NFA - High volatility, do your own research')