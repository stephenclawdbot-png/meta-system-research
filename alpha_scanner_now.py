#!/usr/bin/env python3

import requests
import json
from datetime import datetime

# Try searching for more popular memecoins
queries = ['bonk', 'wif', 'boden', 'wen', 'popcat', 'myro', 'slerf', 'toshi', 'worm']

all_pairs = []

for query in queries:
    url = f'https://api.dexscreener.com/latest/dex/search/?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        pairs = data.get('pairs', [])
        all_pairs.extend(pairs)
        print(f'{query}: {len(pairs)} pairs')
    except Exception as e:
        print(f'Error fetching {query}: {e}')

print(f'\nTotal unique pairs: {len(all_pairs)}')

memecoins = []
for pair in all_pairs:
    mcap = pair.get('marketCap', 0)
    volume = pair.get('volume', {}).get('h24', 0)
    
    if mcap and 30000 <= mcap <= 200000 and volume >= 1000:
        symbol = pair['baseToken']['symbol']
        name = pair['baseToken']['name']
        price_change = pair.get('priceChange', {}).get('h24', 0)
        txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        
        # Calculate alpha metrics
        vol_mcap_ratio = (volume / mcap) * 100 if mcap > 0 else 0
        buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0
        
        # Alpha scoring algorithm
        alpha_score = 0
        if vol_mcap_ratio >= 100: alpha_score += 30
        elif vol_mcap_ratio >= 50: alpha_score += 20
        elif vol_mcap_ratio >= 20: alpha_score += 10
        
        if buy_ratio >= 0.6: alpha_score += 25
        elif buy_ratio >= 0.55: alpha_score += 15
        elif buy_ratio >= 0.5: alpha_score += 5
        
        if volume >= 100000: alpha_score += 20
        elif volume >= 50000: alpha_score += 15
        elif volume >= 10000: alpha_score += 10
        
        if buys >= 500: alpha_score += 15
        elif buys >= 100: alpha_score += 10
        elif buys >= 50: alpha_score += 5
        
        if liquidity >= mcap * 0.3: alpha_score += 10

        memecoins.append({
            'symbol': symbol,
            'name': name,
            'mcap': mcap,
            'volume': volume,
            'price_change': price_change,
            'vol_mcap_ratio': vol_mcap_ratio,
            'buy_ratio': buy_ratio,
            'buys': buys,
            'sells': sells,
            'liquidity': liquidity,
            'alpha_score': alpha_score,
            'url': pair.get('url', ''),
            'pairAddress': pair.get('pairAddress', '')
        })

print(f'Memecoins in target range: {len(memecoins)}')

# Sort by alpha score
memecoins.sort(key=lambda x: x['alpha_score'], reverse=True)

current_time = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')

print(f'\n🎯 MEMECOIN ALPHA SCANNER REPORT')
print('='*50)
print(f'Scan Time: {current_time}')
print(f'Market Cap Range: $30,000 - $200,000')
print('Focus: Early alpha detection before mainstream attention')
print()
print('🔥 TOP ALPHA MEMECOINS DETECTED')
print('-' * 50)

for i, coin in enumerate(memecoins[:10], 1):
    print(f'🎯 #{i} {coin["symbol"]} - Alpha Score: {coin["alpha_score"]}/100')
    print(f'   💰 MCap: ${coin["mcap"]:,.0f}')
    print(f'   📈 24h Volume: ${coin["volume"]:,.0f}')
    print(f'   🔥 Vol/MCap Ratio: {coin["vol_mcap_ratio"]:.1f}%')
    print(f'   📊 24h Price Change: {coin["price_change"]:.1f}%')
    print(f'   🔄 Buy/Sell Ratio: {coin["buy_ratio"]:.1%} ({coin["buys"]} buys/{coin["sells"]} sells)')
    print(f'   💧 Liquidity: ${coin["liquidity"]:,.0f}')
    if coin.get('url'):
        print(f'   🔗 DexScreener: {coin["url"]}')
    print()

if memecoins:
    avg_alpha = sum(c['alpha_score'] for c in memecoins) / len(memecoins)
    avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins)
    avg_buy_ratio = sum(c['buy_ratio'] for c in memecoins) / len(memecoins)
    
    print('📊 MARKET SUMMARY')
    print('-' * 20)
    print(f'• Total Alpha Candidates: {len(memecoins)} tokens')
    print(f'• Highest Alpha Score: {max(c["alpha_score"] for c in memecoins)}/100')
    print(f'• Average Alpha Score: {avg_alpha:.1f}/100')
    print(f'• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%')
    print(f'• Average Buy Ratio: {avg_buy_ratio:.1%}')
else:
    print('No memecoins found matching criteria')

print()
print('⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE')
print('• Always conduct your own research before investing')
print('• Memecoins are extremely volatile')
print('• Only risk what you can afford to lose')