#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_new_tokens():
    """Fetch new tokens from DexScreener"""
    try:
        # Try to get recently added tokens
        url = "https://api.dexscreener.com/latest/dex/tokens/new"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        tokens = []
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            volume = token.get('volume', {}).get('h24', 0)
            
            # Filter for 30k-200k range with some volume
            if 30000 <= mcap <= 200000 and volume > 1000:
                tokens.append(token)
        
        return tokens
    except Exception as e:
        print(f"Error fetching new tokens: {e}")
        return []

def fetch_popular_memecoins():
    """Fetch popular memecoins"""
    search_terms = ["PEPE", "DOGE", "SHIB", "BONK", "WIF", "FLOKI", "BOME", "MEME"]
    tokens = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                
                if 30000 <= mcap <= 200000:
                    tokens.append(token)
        except Exception as e:
            print(f"Error fetching {term}: {e}")
            continue
    
    return tokens

def analyze_token(token):
    """Analyze token metrics"""
    mcap = token.get('fdv', 0)
    volume = token.get('volume', {}).get('h24', 0)
    price_change = token.get('priceChange', {}).get('h24', 0)
    txn_data = token.get('txns', {})
    buys = txn_data.get('h24', {}).get('buys', 0)
    sells = txn_data.get('h24', {}).get('sells', 0)
    
    # Calculate alpha score
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0
    
    # Simple scoring
    score = min(100, vol_mcap_ratio * 0.5 + buy_ratio * 50 + max(0, price_change) * 0.5)
    
    return {
        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
        'name': token.get('baseToken', {}).get('name', 'Unknown'),
        'mcap': mcap,
        'volume': volume,
        'price_change': price_change,
        'vol_mcap_ratio': vol_mcap_ratio,
        'buy_ratio': buy_ratio,
        'score': round(score, 1),
        'url': token.get('url', ''),
        'dex': token.get('dexId', ''),
        'chain': token.get('chainId', '')
    }

def main():
    print("⚡ QUICK DEXSCREENER SCAN - 30k-200k MCap Range")
    print("=" * 50)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p"))
    print("Target: Sub-200k MCap Memecoins with Alpha Potential")
    print()
    
    # Fetch data
    print("🔍 Fetching new tokens...")
    new_tokens = fetch_new_tokens()
    
    print("🔍 Fetching popular memecoins...")
    memecoins = fetch_popular_memecoins()
    
    all_tokens = new_tokens + memecoins
    
    if not all_tokens:
        print("❌ No tokens found in 30k-200k range")
        return
    
    # Remove duplicates
    unique_tokens = []
    seen = set()
    for token in all_tokens:
        addr = token.get('pairAddress')
        if addr not in seen:
            seen.add(addr)
            unique_tokens.append(token)
    
    print(f"✅ Found {len(unique_tokens)} tokens")
    
    # Analyze tokens
    analyzed = []
    for token in unique_tokens:
        analyzed.append(analyze_token(token))
    
    # Sort by score
    analyzed.sort(key=lambda x: x['score'], reverse=True)
    
    # Keep only tokens with score > 10
    analyzed = [t for t in analyzed if t['score'] > 10]
    
    if not analyzed:
        print("❌ No alpha tokens detected (score > 10)")
        return
    
    print(f"🔥 Found {len(analyzed)} alpha tokens")
    print()
    
    # Display top tokens
    for i, token in enumerate(analyzed[:10], 1):
        print(f"🎯 #{i} {token['symbol']}")
        print(f"   Score: {token['score']}/100")
        print(f"   MCap: ${token['mcap']:,}")
        print(f"   Volume: ${token['volume']:,}")
        print(f"   24h Change: {token['price_change']:.1f}%")
        print(f"   Vol/MCap Ratio: {token['vol_mcap_ratio']:.1f}%")
        print(f"   Buy Ratio: {token['buy_ratio']:.1%}")
        print(f"   Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    print("⚠️ DISCLAIMER: High risk memecoin scanning - DYOR NFA")

if __name__ == "__main__":
    main()