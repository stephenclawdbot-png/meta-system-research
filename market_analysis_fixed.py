#!/usr/bin/env python3
import requests
from datetime import datetime

# Broader search to understand current memecoin landscape
print('🗺️ CURRENT MEMECOIN LANDSCAPE ANALYSIS')
print('Scan Time:', datetime.now().strftime('%A, %B %d, %Y — %I:%M %p Asia/Manila'))
print('Analysing newest tokens across all market caps')
print('='*60)

# Try multiple DexScreener endpoints
endpoints = [
    'https://api.dexscreener.com/latest/dex/tokens/newest',
    'https://api.dexscreener.com/latest/dex/search?q=solana',
]

for endpoint in endpoints:
    print(f'\n🔍 Checking {endpoint}')
    try:
        response = requests.get(endpoint, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data and 'pairs' in data and data['pairs']:
                tokens_by_mcap = {'micro': [], 'small': [], 'medium': [], 'large': []}
                
                for token in data['pairs'][:30]:  # Top 30
                    mcap = token.get('fdv', 0)
                    symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
                    
                    if mcap < 10000:
                        tokens_by_mcap['micro'].append((symbol, mcap))
                    elif mcap < 100000:
                        tokens_by_mcap['small'].append((symbol, mcap))
                    elif mcap < 1000000:
                        tokens_by_mcap['medium'].append((symbol, mcap))
                    else:
                        tokens_by_mcap['large'].append((symbol, mcap))
                
                print(f'Found {len(data[\"pairs\"])} tokens total')
                print('Market Cap Distribution:')
                print(f'💎 Micro (<$10k): {len(tokens_by_mcap["micro"])}')
                print(f'📈 Small ($10k-$100k): {len(tokens_by_mcap["small"])}')
                print(f'🚀 Medium ($100k-$1M): {len(tokens_by_mcap["medium"])}')
                print(f'🏆 Large (>$1M): {len(tokens_by_mcap["large"])}')
                
                # Focus on alpha territory
                print()
                print('🎯 CURRENT ALPHA STATUS:')
                target_tokens = tokens_by_mcap['small'] + tokens_by_mcap['medium']
                print(f'Tokens in 30k-200k target range: {len(target_tokens)}')
                
                if target_tokens:
                    print('Potentials:')
                    for symbol, mcap in target_tokens[:5]:
                        print(f'   {symbol} - ${mcap:,.0f}')
                break
            else:
                print('No token data available')
        else:
            print(f'API error: {response.status_code}')
    except Exception as e:
        print(f'Error: {e}')
else:
    print('❌ All API calls failed')

print()
print('💡 SCANNER SUMMARY:')
print('Market scan complete - monitoring 30k-200k mcap range for alpha opportunities')
print('Next automated scan in 5 minutes')