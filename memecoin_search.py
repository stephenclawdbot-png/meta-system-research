#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Search for actual memecoins using specific keywords
MEMECOIN_KEYWORDS = [
    "memecoin", "meme", "wojak", "pepe", "doge", "shib", "bonk", "wif", 
    "trump", "elon", "musk", "crypto", "coin", "token"
]

def search_memecoins():
    """Search DexScreener for memecoin-related tokens"""
    all_results = []
    
    for keyword in MEMECOIN_KEYWORDS:
        print(f"🔍 Searching: '{keyword}'...")
        
        url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}&limit=20"
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                for pair in pairs:
                    # Filter for reasonable market caps and exclude major tokens
                    mcap = pair.get('fdv', pair.get('marketCap', 0))
                    symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                    
                    # Skip major tokens
                    if symbol in ['SOL', 'ETH', 'BTC', 'USDC', 'USDT']:
                        continue
                    
                    # Ensure reasonable MCap
                    if mcap < 1000:  # Too small
                        continue
                        
                    all_results.append(pair)
                    
                print(f"   Found {len(pairs)} pairs")
            else:
                print(f"   Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # Remove duplicates
    unique_results = []
    seen = set()
    for pair in all_results:
        pair_id = pair.get('pairAddress')
        if pair_id not in seen:
            seen.add(pair_id)
            unique_results.append(pair)
    
    return unique_results

def analyze_memecoins(pairs):
    """Analyze memecoins in the target mcap range"""
    filtered = []
    
    for pair in pairs:
        mcap = pair.get('fdv', pair.get('marketCap', 0))
        volume = pair.get('volume', {}).get('h24', 0)
        symbol = pair.get('baseToken', {}).get('symbol', '').upper()
        
        # Target range filter
        if not (30000 <= mcap <= 200000):
            continue
        
        # Volume filter
        if volume < 1000:
            continue
        
        # Calculate age
        age_hours = 0
        created_at = pair.get('pairCreatedAt')
        if created_at:
            created_dt = datetime.fromtimestamp(created_at / 1000)
            now = datetime.now()
            age_hours = (now - created_dt).total_seconds() / 3600
        
        # Calculate simple alpha score
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
        score = min(100, vol_mcap_ratio * 0.8)
        
        # Bonus for newer coins
        if age_hours < 24:
            score += min(20, (24 - age_hours) / 24 * 20)
        
        price_change = pair.get('priceChange', {}).get('h24', 0)
        if price_change > 0:
            score += min(10, price_change * 0.1)
        
        filtered.append({
            'symbol': symbol,
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'mcap': mcap,
            'volume': volume,
            'vol_mcap_ratio': vol_mcap_ratio,
            'price_change': price_change,
            'age_hours': age_hours,
            'liquidity': pair.get('liquidity', {}).get('usd', 0),
            'url': pair.get('url', ''),
            'decor': pair.get('dexId', ''),
            'alpha_score': score
        })
    
    return filtered

if __name__ == "__main__":
    print("🎯 MEMECOIN ALPHA SEARCH")
    print("="*50)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print("Target: Sub-200K MCap memecoins\n")
    
    pairs = search_memecoins()
    print(f"\n📊 Found {len(pairs)} total pairs across searches")
    
    filtered = analyze_memecoins(pairs)
    
    # Sort by alpha score
    filtered.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    if filtered:
        print(f"🔥 ALPHA GEMS (Top 10):\n")
        
        for i, token in enumerate(filtered[:10], 1):
            print(f"#{i} {token['symbol']} - Alpha Score: {token['alpha_score']:.1f}/100")
            print(f"   Name: {token['name']}")
            print(f"   MCap: ${token['mcap']:,}")
            print(f"   Volume: ${token['volume']:,}")
            print(f"   Vol/MCap: {token['vol_mcap_ratio']:.1f}%")
            print(f"   Price Δ: {token['price_change']:+.1f}%")
            print(f"   Liquidity: ${token['liquidity']:,}")
            print(f"   Age: {token['age_hours']:.1f}h")
            print(f"   Dex: {token['decor']}")
            print(f"   URL: {token['url']}")
            print()
    else:
        print("📭 No memecoin alpha gems found")
    
    print("⚠️  DISCLAIMER: High risk memecoins - NFA")