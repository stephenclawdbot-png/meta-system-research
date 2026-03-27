#!/usr/bin/env python3
import requests

# Get Solana pairs
url = "https://api.dexscreener.com/latest/dex/tokens/solana"
response = requests.get(url)
data = response.json()
pairs = data.get('pairs', [])

runners = []
for pair in pairs:
    mcap = pair.get('marketCap', 0) or 0
    volume = pair.get('volume', {}).get('h24', 0) or 0
    price_change = pair.get('priceChange', {}).get('h24', 0) or 0
    liquidity = pair.get('liquidity', {}).get('usd', 0) or 0
    address = pair.get('baseToken', {}).get('address', '')
    
    # Only tokens with momentum
    if mcap > 10000 and mcap < 10000000:  # 10k-10m range
        if volume > 100000:  # Minimum 100k volume
            buys = pair.get('txns', {}).get('h24', {}).get('buys', 0)
            sells = pair.get('txns', {}).get('h24', {}).get('sells', 0)
            total_txns = buys + sells
            
            runners.append({
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'mcap': mcap,
                'volume': volume,
                'change': price_change,
                'address': address,
                'liquidity': liquidity,
                'txns': total_txns,
                'buys': buys,
                'sells': sells
            })

# Sort by volume
runners.sort(key=lambda x: x['volume'], reverse=True)

print('🔥 HIGH VOLUME PUMP PLAYS')
print('=' * 70)

for i, r in enumerate(runners[:15], 1):
    buy_ratio = (r['buys'] / r['txns'] * 100) if r['txns'] > 0 else 50
    
    print(f"\n{i}. {r['symbol']}")
    print(f"   MCap: ${r['mcap']:,.0f}")
    print(f"   Volume: ${r['volume']:,.0f}")
    print(f"   Change: {r['change']:+.1f}%")
    print(f"   TXNs: {r['txns']:,} | Buy %: {buy_ratio:.0f}%")
    print(f"   Liq: ${r['liquidity']:,.0f}")
    print(f"   {r['address']}")
