#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import time

def scan_solana_memecoins():
    """Scan Solana blockchain for memecoins"""
    memecoins = []
    total_scanned = 0
    
    # Known memecoin terms on Solana
    search_terms = ['bonk', 'wif', 'toshi', 'myro', 'wifhat', 'slerf', 'michi', 'wen']
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={term}"
            response = requests.get(url)
            data = response.json()
            
            pairs = data.get('pairs', [])
            total_scanned += len(pairs)
            
            for pair in pairs:
                try:
                    chain = pair.get('chainId', '').lower()
                    symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                    name = pair.get('baseToken', {}).get('name', '').upper()
                    
                    # Only Solana chain
                    if chain != 'solana':
                        continue
                    
                    mcap = float(pair.get('marketCap', 0))
                    volume_24h = float(pair.get('volume', {}).get('h24', 0))
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
                    
                    # Market cap range: 30k - 200k
                    if mcap >= 30000 and mcap <= 200000:
                        if volume_24h > 5000 and liquidity > 1000:
                            score = (volume_24h / mcap) * 100 if mcap > 0 else 0
                            
                            memecoins.append({
                                'symbol': pair.get('baseToken', {}).get('symbol', ''),
                                'name': pair.get('baseToken', {}).get('name', ''),
                                'market_cap': int(mcap),
                                '24h_volume': int(volume_24h),
                                'liquidity': int(liquidity),
                                'price': float(pair.get('priceUsd', 0)),
                                'score': round(score, 2),
                                'url': pair.get('url', ''),
                                'chain': chain
                            })
                except (ValueError, TypeError):
                    continue
            
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Error searching '{term}': {e}")
            continue
    
    return memecoins, total_scanned

print("🐸 Solana Memecoin Alpha Scanner")
print("=" * 50)
print(f"📊 Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("📍 Target: $30K-$200K MCap, >$5K Daily Volume")
print("")

memecoins, total_scanned = scan_solana_memecoins()

if memecoins:
    # Sort by volume/mcap ratio
    memecoins.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"🎯 Found {len(memecoins)} Solana memecoins in target range:")
    print("=" * 50)
    
    for i, coin in enumerate(memecoins[:10], 1):
        print(f"\n{i}. {coin['symbol']}")
        print(f"   Name: {coin['name']}")
        print(f"   MCap: ${coin['market_cap']:,}")
        print(f"   24h Volume: ${coin['24h_volume']:,}")
        print(f"   Liquidity: ${coin['liquidity']:,}")
        print(f"   Alpha Score: {coin['score']}")
        print(f"   Price: ${coin['price']:.8f}")
        print(f"   DexScreener: {coin['url']}")
    
    # Check broader market
    print("\n" + "=" * 50)
    print(f"🔍 Market Snapshot:")
    print(f"   Total pairs scanned: {total_scanned}")
    print(f"   Memecoins found: {len(memecoins)}")
    
    if len(memecoins) == 0:
        print("💡 Insight: Market appears quiet - few memecoins in this range")
    
else:
    print("❌ No Solana memecoins found in target range")
    print(f"📊 Scanned {total_scanned} total pairs")
    print("💡 Try adjusting criteria or check during peak trading hours")

print("\n✅ Scan complete")