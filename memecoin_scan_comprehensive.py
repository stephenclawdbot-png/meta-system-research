#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import time

# Major tokens to exclude
MAJOR_TOKENS = {'SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'DAI', 'BONK', 'WIF', 'JUP', 'RAY', 'ORCA'}

def is_memecoin_like(symbol, name):
    """Heuristic to identify memecoin-like tokens"""
    symbol = symbol.upper()
    name = name.upper()
    
    # Exclude major tokens
    if symbol in MAJOR_TOKENS:
        return False
    
    # Memecoin indicators
    memecoin_patterns = [
        len(symbol) <= 6,  # Short tickers
        'MEME' in name or 'DOG' in name or 'CAT' in name or 'MOON' in name,
        '$' in symbol,
        symbol.isalpha() and len(symbol) >= 2 and len(symbol) <= 5,
        any(word in name for word in ['Meme', 'Dog', 'Cat', 'Moon', 'Rocket', 'Pepe', 'Shiba', 'Floki']),
    ]
    
    return any(memecoin_patterns)

def fetch_memecoins_all_chains():
    """Search across multiple chains for memecoins"""
    memecoins = []
    total_scanned = 0
    
    # Search terms likely to yield memecoins
    search_terms = ['bonk', 'wif', 'pepe', 'shib', 'floki', 'doge', 'meme', 'cat', 'dog']
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={term}"
            response = requests.get(url)
            data = response.json()
            
            for pair in data.get('pairs', []):
                try:
                    symbol = pair.get('baseToken', {}).get('symbol', '')
                    name = pair.get('baseToken', {}).get('name', '')
                    
                    # Filter criteria
                    mcap = float(pair.get('marketCap', 0))
                    volume_24h = float(pair.get('volume', {}).get('h24', 0))
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
                    
                    total_scanned += 1
                    
                    # Market cap range: 30k - 200k
                    if mcap >= 30000 and mcap <= 200000 and volume_24h > 5000:
                        # Only include memecoin-like tokens
                        if is_memecoin_like(symbol, name):
                            # Calculate score (higher volume relative to market cap = more potential)
                            score = (volume_24h / mcap) * 100 if mcap > 0 else 0
                            
                            memecoins.append({
                                'symbol': symbol,
                                'name': name,
                                'address': pair.get('baseToken', {}).get('address'),
                                'market_cap': int(mcap),
                                '24h_volume': int(volume_24h),
                                'liquidity': int(liquidity),
                                'price': float(pair.get('priceUsd', 0)),
                                'score': round(score, 2),
                                'url': pair.get('url', ''),
                                'chain': pair.get('chainId', '')
                            })
                except (ValueError, TypeError):
                    continue
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"⚠️ Error fetching {term}: {e}")
            continue
    
    return memecoins, total_scanned

# Run the scan
print("🔍 Scanning DexScreener for memecoins...")
memecoins, total_scanned = fetch_memecoins_all_chains()

# Sort by score (volume/mcap ratio)
memecoins.sort(key=lambda x: x['score'], reverse=True)

# Generate report
if memecoins:
    print("\n🔥 MEMECOIN ALPHA SCAN REPORT")
    print(f"📊 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📍 Filters: MCap $30K-$200K | Volume > $5K | Memecoin-filtered")
    print(f"🔍 Scanned {total_scanned} pairs, found {len(memecoins)} candidates")
    print("=" * 60)
    
    for i, coin in enumerate(memecoins[:15], 1):
        print(f"\n{i}. {coin['symbol']} ({coin['name']}) [{coin['chain']}]")
        print(f"   Market Cap: ${coin['market_cap']:,}")
        print(f"   24h Volume: ${coin['24h_volume']:,}")
        print(f"   Alpha Score: {coin['score']}")
        print(f"   Liquidity: ${coin['liquidity']:,}")
        print(f"   Price: ${coin['price']:.6f}")
        print(f"   URL: {coin['url']}")
else:
    print(f"❌ No memecoins found matching criteria")
    print(f"🔍 Scanned {total_scanned} pairs total")