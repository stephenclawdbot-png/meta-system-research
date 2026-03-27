#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

def simple_scan():
    """Simple scan for memecoins in 30k-200k range"""
    print(f"📊 MEMECOIN SCAN - {datetime.now().strftime('%I:%M %p')}")
    print("Filter: $30k-$200k Market Cap\n")
    
    # Search popular meme terms
    terms = ["doge", "pepe", "meme", "coin", "shib", "bonk", "floki", "elon", "musk", "moon"]
    results = []
    
    for term in terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data:
                    for token in data['pairs']:
                        mcap = token.get('marketCap', 0)
                        if 30000 <= mcap <= 200000:
                            volume_24h = token.get('volume', {}).get('h24', 0)
                            if volume_24h > 1000:  # Minimum volume threshold
                                results.append({
                                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                                    'name': token.get('baseToken', {}).get('name', 'Unknown'),
                                    'mcap': mcap,
                                    'volume': volume_24h,
                                    'chain': token.get('chainId', 'Unknown'),
                                    'url': token.get('url')
                                })
            
            time.sleep(0.2)
        except:
            continue
    
    # Sort by volume/mcap ratio
    for token in results:
        token['vol_ratio'] = token['volume'] / token['mcap'] if token['mcap'] > 0 else 0
    
    results.sort(key=lambda x: x['vol_ratio'], reverse=True)
    
    if results:
        print(f"🎯 Found {len(results)} candidate tokens")
        print("-" * 50)
        
        for i, token in enumerate(results[:20]):  # Show top 20
            print(f"\n️ {i+1}. {token['symbol']}")
            print(f"   📛 {token['name']}")
            print(f"   💰 MCap: ${token['mcap']:,}")
            print(f"   📈 24h Volume: ${token['volume']:,}")
            print(f"   🔥 Ratio: {token['vol_ratio']:.2f}x")
            print(f"   ⛓️  Chain: {token['chain']}")
            print(f"   🔗 {token['url']}")
    else:
        print("❌ No tokens found in this range")
        print("💡 The market might be quiet or filters too strict")

if __name__ == "__main__":
    simple_scan()