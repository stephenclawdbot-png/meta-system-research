#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

# Modified scanner with broader coverage
searches = ['elon', 'pepe', 'bonk', 'floki', 'shib', 'squid', 'doge', 'sol', 'meme', 'cat', 'dog', 'ape', 'game', 'ai', 'nft']

all_pairs = []
for search_term in searches:
    try:
        cmd = f'curl -s "https://api.dexscreener.com/latest/dex/search?q={search_term}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('pairs'):
                all_pairs.extend(data['pairs'])
    except:
        pass

# Analyze with 30k-200k mcap and minimal volume
candidates = []
for p in all_pairs:
    try:
        mcap = p.get('fdv', 0)
        vol = p.get('volume', {}).get('h24', 0)
        liq = p.get('liquidity', {}).get('usd', 0)
        
        if mcap >= 30000 and mcap <= 200000 and vol > 0:
            ticker = p.get('baseToken', {}).get('symbol', 'UNKNOWN')
            name = p.get('baseToken', {}).get('name', 'Unknown')
            price_chg = p.get('priceChange', {}).get('h24', 0)
            
            txns = p.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            buy_ratio = buys/(buys+sells) if buys+sells > 0 else 0
            
            candidates.append({
                'symbol': ticker,
                'name': name,
                'mcap': mcap,
                'volume': vol,
                'liquidity': liq,
                'price_chg': price_chg,
                'buy_ratio': buy_ratio,
                'txns': f'{buys}/{sells}'
            })
    except:
        continue

# Show top candidates by volume
candidates.sort(key=lambda x: x['volume'], reverse=True)

print(f'SCAN RESULTS - Total pairs scanned: {len(all_pairs)}')
print(f'Candidates in 30k-200k mcap range: {len(candidates)}')
print()

if candidates:
    print('TOP MEMECOINS IN TARGET RANGE:')
    for i, cand in enumerate(candidates[:10], 1):
        print(f"{i}. {cand['symbol']} - MCap: ${cand['mcap']:,} Vol: ${cand['volume']:.0f} Liq: ${cand['liquidity']:.0f} B/S: {cand['txns']}")
else:
    print('No tokens found in 30k-200k mcap range with trading activity')

print(f"\nTimestamp: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")