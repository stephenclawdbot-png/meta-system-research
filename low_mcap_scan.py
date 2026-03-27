#!/usr/bin/env python3
"""Scan for low market cap gems (15k-30k)"""

import requests

def scan_low_mcap():
    url = 'https://api.dexscreener.com/latest/dex/search?q=trending'
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        data = response.json()
        low_mcap_gems = []
        
        for pair in data.get('pairs', [])[:50]:
            mcap = pair.get('marketCap', 0)
            if 15000 <= mcap <= 30000:  # Lower range
                base_token = pair.get('baseToken', {})
                symbol = base_token.get('symbol', '')
                if symbol:  # Skip empty symbols
                    volume_24h = pair.get('volume', {}).get('h24', 0)
                    price_change = pair.get('priceChange', {}).get('h24', 0)
                    liquidity = pair.get('liquidity', {}).get('usd', 0)
                    
                    txns_h24 = pair.get('txns', {}).get('h24', {})
                    buys = txns_h24.get('buys', 0)
                    sells = txns_h24.get('sells', 0)
                    total_txns = buys + sells
                    buy_ratio = buys / total_txns if total_txns > 0 else 0
                    
                    # Enhanced alpha calculation
                    vol_score = min(30, volume_24h / 500 * 3)
                    vol_mcap_ratio = (volume_24h / mcap * 100) if mcap > 0 else 0
                    vol_mcap_score = min(20, vol_mcap_ratio * 0.2)
                    price_score = min(25, max(0, price_change) * 0.5)
                    liq_score = min(15, liquidity / 1000 * 0.3)
                    activity_score = min(10, total_txns * 0.2)
                    buy_score = min(10, buy_ratio * 10)
                    
                    alpha_score = vol_score + vol_mcap_score + price_score + liq_score + activity_score + buy_score
                    
                    if alpha_score > 20:
                        gem = {
                            'symbol': symbol,
                            'name': base_token.get('name', ''),
                            'mcap': mcap,
                            'volume_24h': volume_24h,
                            'price_change': price_change,
                            'liquidity': liquidity,
                            'transactions': total_txns,
                            'buy_ratio': buy_ratio,
                            'alpha_score': alpha_score,
                            'dex_url': pair.get('url', '')
                        }
                        low_mcap_gems.append(gem)
        
        return low_mcap_gems
    return []

results = scan_low_mcap()
if results:
    print('🔥 LOW MCAP ALPHA GEMS (15k-30k):')
    for gem in sorted(results, key=lambda x: x['alpha_score'], reverse=True)[:5]:
        vol_mcap_ratio = gem['volume_24h'] / gem['mcap'] * 100 if gem['mcap'] > 0 else 0
        print(f"🎯 {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}")
        print(f"   MCap: ${gem['mcap']:,} | Volume: ${gem['volume_24h']:.0f}")
        print(f"   Price Change: {gem['price_change']:.1f}% | Vol/MCap: {vol_mcap_ratio:.1f}%")
        print(f"   Txs: {gem['transactions']} | Buy Ratio: {gem['buy_ratio']:.1%}")
        print(f"   DexScreener: {gem['dex_url']}")
        print()
else:
    print('📭 No low mcap gems found in 15k-30k range')