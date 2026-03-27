import requests
import json

def scan_dexscreener_trending():
    url = 'https://api.dexscreener.com/latest/dex/tokens/trending'
    response = requests.get(url, timeout=10)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    if not data:
        return []
    
    alpha_gems = []
    for pair in data:
        mcap = pair.get('fdv', 0)
        if 30000 <= mcap <= 200000:
            gem = {
                'symbol': pair.get('baseToken', {}).get('symbol', ''),
                'mcap': mcap,
                'volume_24h': pair.get('volume', {}).get('h24', 0),
                'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                'chain': pair.get('chainId', ''),
                'url': pair.get('url', ''),
                'liquidity': pair.get('liquidity', {}).get('usd', 0) if pair.get('liquidity') else 0
            }
            alpha_gems.append(gem)
    
    return alpha_gems

trending = scan_dexscreener_trending()
print('TRENDING SUB-200K MEMECOINS')
print('=' * 30)
for gem in trending:
    vol_ratio = (gem['volume_24h'] / gem['mcap']) * 100 if gem['mcap'] > 0 else 0
    print(f"{gem['symbol']} - MCap: ${int(gem['mcap']):,} | Vol: ${int(gem['volume_24h']):,}")
    print(f"  24h: {gem['price_change_24h']:+}% | Vol/MCap: {vol_ratio:.1f}%")
    print(f"  Chain: {gem['chain']} | Liquidity: ${int(gem['liquidity']):,}")
    print(f"  {gem['url']}")
    print()