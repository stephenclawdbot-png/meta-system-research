#!/usr/bin/env python3
import requests
import json
from datetime import datetime

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
        'MEME' in name or 'DOG' in name or 'CAT' in name,
        '$' in symbol,
        symbol.isalpha() and len(symbol) >= 3 and len(symbol) <= 5,
    ]
    
    return any(memecoin_patterns)

# DexScreener API
url = "https://api.dexscreener.com/latest/dex/search/?q=solana"

try:
    response = requests.get(url)
    data = response.json()
    
    memecoins = []
    valid_pairs = 0
    
    for pair in data.get('pairs', []):
        try:
            # Get token info
            symbol = pair.get('baseToken', {}).get('symbol', '')
            name = pair.get('baseToken', {}).get('name', '')
            
            # Filter criteria
            mcap = float(pair.get('marketCap', 0))
            volume_24h = float(pair.get('volume', {}).get('h24', 0))
            liquidity = float(pair.get('liquidity', {}).get('usd', 0))
            
            valid_pairs += 1
            
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
                        'url': pair.get('url', '')
                    })
        except (ValueError, TypeError) as e:
            continue
    
    # Sort by score (volume/mcap ratio)
    memecoins.sort(key=lambda x: x['score'], reverse=True)
    
    # Generate report
    if memecoins:
        print("🔥 MEMECOIN ALPHA SCAN REPORT")
        print(f"📊 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"📍 Filters: MCap $30K-$200K | Volume > $5K | Memecoin-filtered")
        print(f"🔍 Scanned {valid_pairs} pairs, found {len(memecoins)} candidates")
        print("=" * 60)
        
        for i, coin in enumerate(memecoins[:15], 1):
            print(f"\n{i}. {coin['symbol']} ({coin['name']})")
            print(f"   Market Cap: ${coin['market_cap']:,}")
            print(f"   24h Volume: ${coin['24h_volume']:,}")
            print(f"   Alpha Score: {coin['score']}")
            print(f"   Liquidity: ${coin['liquidity']:,}")
            print(f"   Price: ${coin['price']:.6f}")
            print(f"   URL: {coin['url']}")
    else:
        print("❌ No memecoins found matching criteria")
        print(f"🔍 Scanned {valid_pairs} pairs total")
        
except Exception as e:
    print(f"⚠️ Error fetching data: {e}")