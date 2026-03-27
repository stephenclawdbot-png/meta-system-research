#!/usr/bin/env python3
import requests
import json

# Get trending Solana pairs
url = "https://api.dexscreener.com/latest/dex/search?q=solana"
response = requests.get(url)
data = response.json()
pairs = data.get('pairs', [])

runners = []
for pair in pairs:
    mcap = pair.get('marketCap', 0) or 0
    volume = pair.get('volume', {}).get('h24', 0) or 0
    price_change = pair.get('priceChange', {}).get('h24', 0) or 0
    liquidity = pair.get('liquidity', {}).get('usd', 0) or 0
    
    # Runner criteria
    if mcap > 50000 and mcap < 5000000:  # 50k-5m range
        if volume > mcap * 0.2:  # Decent volume
            buys = pair.get('txns', {}).get('h24', {}).get('buys', 0)
            sells = pair.get('txns', {}).get('h24', {}).get('sells', 0)
            total_txns = buys + sells
            
            runners.append({
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'mcap': mcap,
                'volume': volume,
                'change': price_change,
                'address': pair.get('baseToken', {}).get('address', ''),
                'liquidity': liquidity,
                'txns': total_txns,
                'buys': buys,
                'sells': sells
            })

# Sort by volume/mcap ratio
runners.sort(key=lambda x: x['volume']/x['mcap'] if x['mcap'] > 0 else 0, reverse=True)

print('🏃 ACTUAL RUNNERS - Volume/Momentum Analysis')
print('=' * 70)

for i, r in enumerate(runners[:12], 1):
    ratio = (r['volume'] / r['mcap'] * 100) if r['mcap'] > 0 else 0
    buy_ratio = (r['buys'] / r['txns'] * 100) if r['txns'] > 0 else 50
    
    print(f"\n{i}. {r['symbol']}")
    print(f"   MCap: ${r['mcap']:,.0f} | Vol: ${r['volume']:,.0f}")
    print(f"   Vol/MCap: {ratio:.1f}% | Change: {r['change']:+.1f}%")
    print(f"   TXNs: {r['txns']:,} (Buy: {buy_ratio:.0f}%) | Liq: ${r['liquidity']:,.0f}")
    print(f"   CA: {r['address']}")
