#!/usr/bin/env python3

import requests
import json
from datetime import datetime

# Broad list of recent popular memecoin symbols
memecoin_symbols = [
    'bonk', 'wif', 'boden', 'wen', 'popcat', 'myro', 'slerf', 'toshi', 'worm',
    'doge', 'shib', 'pepe', 'floki', 'baby doge', 'sats', 'ordi', 'rats', 'lgb',
    'turbo', 'troll', 'dogeai', 'degen', 'mich', 'inu', 'wojak', 'elon', 'trump',
    'maga', 'cat', 'kitty', 'pussy', 'pusy', 'based', 'silly', 'harrypotter',
    'ponder', 'agent', 'dre', 'virl', 'ptr', 'bgpt', 'ntt', 'sodb', 'bnb',
    'eth', 'sol', 'ltc', 'xrp', 'ada', 'matic', 'arb', 'opt', 'pyth', 'jito',
    'ray', 'msol', 'jup', 'w', 'zetx', 'hiv', 'meme', 'buzz', 'buzzda', 'poo'
]

all_pairs = []

print("🔍 Scanning DexScreener for memecoins across multiple chains...")

for symbol in memecoin_symbols:
    url = f'https://api.dexscreener.com/latest/dex/search/?q={symbol}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            all_pairs.extend(pairs)
            print(f'{symbol}: {len(pairs)} pairs')
        else:
            print(f'{symbol}: API error {response.status_code}')
    except Exception as e:
        print(f'Error fetching {symbol}: {e}')

print(f'\nTotal pairs collected: {len(all_pairs)}')

# Remove duplicates
unique_pairs = {}
for pair in all_pairs:
    pair_address = pair.get('pairAddress', '')
    if pair_address and pair_address not in unique_pairs:
        unique_pairs[pair_address] = pair

all_pairs = list(unique_pairs.values())
print(f'Total unique pairs: {len(all_pairs)}')

# Filter for memecoins in the 30k-200k mcap range
memecoins = []
for pair in all_pairs:
    try:
        mcap = pair.get('marketCap', 0)
        volume = pair.get('volume', {}).get('h24', 0)
        
        # Apply filters
        if mcap and 30000 <= mcap <= 200000 and volume >= 1000:
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            price_change = pair.get('priceChange', {}).get('h24', 0)
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            
            # Calculate alpha metrics
            vol_mcap_ratio = (volume / mcap) * 100 if mcap > 0 else 0
            buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0
            
            # Enhanced alpha scoring algorithm
            alpha_score = 0
            
            # Trading activity components (max 50)
            if vol_mcap_ratio >= 100: alpha_score += 30
            elif vol_mcap_ratio >= 50: alpha_score += 20
            elif vol_mcap_ratio >= 20: alpha_score += 10
            elif vol_mcap_ratio >= 10: alpha_score += 5
            
            if buys >= 500: alpha_score += 15
            elif buys >= 100: alpha_score += 10
            elif buys >= 50: alpha_score += 5
            elif buys >= 10: alpha_score += 2
            
            # Sentiment components (max 30)
            if buy_ratio >= 0.8: alpha_score += 20
            elif buy_ratio >= 0.6: alpha_score += 15
            elif buy_ratio >= 0.5: alpha_score += 10
            elif buy_ratio >= 0.4: alpha_score += 5
            
            # Market strength components (max 20)
            if volume >= 100000: alpha_score += 15
            elif volume >= 50000: alpha_score += 10
            elif volume >= 10000: alpha_score += 5
            
            if price_change > 0:
                if price_change >= 100: alpha_score += 10
                elif price_change >= 50: alpha_score += 8
                elif price_change >= 20: alpha_score += 5
                elif price_change >= 10: alpha_score += 3
            
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
                'pairAddress': pair.get('pairAddress', ''),
                'chain': pair.get('chainId', 'Unknown')
            })
    except Exception as e:
        continue

print(f'Memecoins in target range: {len(memecoins)}')

# Sort by alpha score
memecoins.sort(key=lambda x: x['alpha_score'], reverse=True)

current_time = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')

print(f'\n🎯 MEMECOIN ALPHA SCANNER REPORT')
print('='*60)
print(f'Scan Time: {current_time}')
print(f'Market Cap Range: $30,000 - $200,000')
print('Focus: Early alpha detection before mainstream attention')
print()

if not memecoins:
    print('❌ No alpha gems found matching criteria')
    print('   Market may be quiet for small-cap opportunities currently')
    exit()

print('🔥 TOP ALPHA MEMECOINS DETECTED')
print('-' * 60)

for i, coin in enumerate(memecoins[:15], 1):
    symbol_color = "🟢" if coin['alpha_score'] >= 60 else "🟡" if coin['alpha_score'] >= 40 else "🔴"
    print(f'{symbol_color} #{i} {coin["symbol"]} - Alpha Score: {coin["alpha_score"]}/100')
    print(f'   💰 Market Cap: ${coin["mcap"]:,.0f}')
    print(f'   📈 24h Volume: ${coin["volume"]:,.0f}')
    print(f'   🔥 Vol/MCap Ratio: {coin["vol_mcap_ratio"]:.1f}%')
    print(f'   📊 24h Price Change: {coin["price_change"]:+.1f}%')
    print(f'   🔄 Buy/Sell Ratio: {coin["buy_ratio"]:.1%} ({coin["buys"]} buys/{coin["sells"]} sells)')
    print(f'   💧 Liquidity: ${coin["liquidity"]:,.0f}')
    print(f'   🔗 Chain: {coin["chain"]}')
    if coin.get('url'):
        print(f'   🔗 DexScreener: {coin["url"]}')
    print()

# Market analysis
print('📊 MARKET ANALYSIS')
print('-' * 20)
if memecoins:
    avg_alpha = sum(c['alpha_score'] for c in memecoins) / len(memecoins)
    avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins)
    avg_buy_ratio = sum(c['buy_ratio'] for c in memecoins) / len(memecoins)
    avg_mcap = sum(c['mcap'] for c in memecoins) / len(memecoins)
    
    high_alpha = [c for c in memecoins if c['alpha_score'] >= 60]
    strong_buy_ratio = [c for c in memecoins if c['buy_ratio'] >= 0.7]
    high_volume_ratio = [c for c in memecoins if c['vol_mcap_ratio'] >= 50]
    
    print(f'• Total Alpha Candidates: {len(memecoins)} tokens')
    print(f'• Average Alpha Score: {avg_alpha:.1f}/100')
    print(f'• Highest Alpha Score: {max(c["alpha_score"] for c in memecoins)}/100')
    print(f'• Average Market Cap: ${avg_mcap:,.0f}')
    print(f'• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%')
    print(f'• Average Buy Ratio: {avg_buy_ratio:.1%}')
    print(f'• High Alpha Candidates (≥60): {len(high_alpha)}')
    print(f'• Strong Buy Pressure (≥70% buys): {len(strong_buy_ratio)}')
    print(f'• High Volume Activity (≥50% ratio): {len(high_volume_ratio)}')
    
    # Chain distribution
    chains = {}
    for c in memecoins:
        chain = c['chain']
        chains[chain] = chains.get(chain, 0) + 1
    
    if chains:
        print(f'• Chain Distribution: {dict(sorted(chains.items(), key=lambda x: x[1], reverse=True))}')

print()
print('⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE')
print('• Always conduct your own research before investing')
print('• Memecoins are extremely volatile')
print('• Only risk what you can afford to lose')
print('• Early alpha detection ≠ guaranteed profit')
print('• Market conditions can change rapidly')