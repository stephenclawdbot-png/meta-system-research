#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_trending():
    """Fetch trending/new pairs from DexScreener"""
    try:
        # Try multiple approaches to find memecoins
        # Search for trending/new tokens
        url = "https://api.dexscreener.com/latest/dex/tokens/new?limit=100"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        tokens = []
        
        if not data or 'pairs' not in data:
            return tokens
        
        # Filter criteria
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            
            # Focus on 30k-200k market cap range
            if 30000 <= mcap <= 200000:
                # Calculate transaction momentum
                txn_data = token.get('txns', {})
                h24_buys = txn_data.get('h24', {}).get('buys', 0)
                h24_sells = txn_data.get('h24', {}).get('sells', 0)
                
                # Only include tokens with meaningful activity
                if h24_buys + h24_sells < 10:
                    continue
                    
                token_info = {
                    'name': token.get('baseToken', {}).get('name', 'Unknown'),
                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': token.get('volume', {}).get('h24', 0),
                    'price': token.get('priceUsd', 0),
                    'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                    'url': token.get('url', ''),
                    'dex': token.get('dexId', ''),
                    'chain': token.get('chainId', ''),
                    'pairAddress': token.get('pairAddress', ''),
                    'created_at': token.get('pairCreatedAt', None),
                    'h24_buys': h24_buys,
                    'h24_sells': h24_sells,
                    'buy_ratio': h24_buys / (h24_buys + h24_sells) if (h24_buys + h24_sells) > 0 else 0
                }
                tokens.append(token_info)
        
        return tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def calculate_alpha_score(token):
    """Calculate alpha score based on multiple metrics"""
    # Volume/MCap ratio (most important - shows high trading relative to size)
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    # Buy pressure (more buys than sells = accumulation)
    buy_pressure = max(0, (token['buy_ratio'] - 0.5) * 100)  # Bonus for >50% buys
    
    # Price momentum
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Age score (newer tokens are higher alpha)
    age_score = 0
    if token.get('created_at'):
        # If created timestamp is available, newer tokens get higher score
        age_seconds = datetime.now().timestamp() - (token['created_at'] / 1000)
        if age_seconds < 86400:  # Less than 24 hours old
            age_score = min(20, 100 * (86400 - age_seconds) / 86400)
    
    # Transaction velocity
    txn_velocity = min(20, token['h24_buys'] / 10) + min(20, token['h24_sells'] / 10)
    
    # Composite alpha score
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.3) +      # Volume/MCap ratio
        (buy_pressure * 0.25) +        # Buy pressure
        (momentum * 0.15) +            # Price momentum
        (age_score * 0.15) +            # Newness bonus
        (txn_velocity * 0.15)          # Transaction activity
    )
    
    return round(alpha_score, 1)

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP FOCUS")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Metrics: Volume/MCap Ratio, Buy Pressure, Momentum, Age")
    print()
    
    # Fetch tokens
    tokens = fetch_dexscreener_trending()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        
        # Try alternative approach
        print("🔄 Trying alternative memecoin search...")
        url = "https://api.dexscreener.com/latest/dex/search?q=PEPE"  # Popular memecoin
        try:
            response = requests.get(url)
            data = response.json()
            if data and 'pairs' in data:
                print(f"✅ API working, found {len(data['pairs'])} pairs total")
            else:
                print("❌ API issue: no pairs returned")
        except Exception as e:
            print(f"❌ API error: {e}")
        return
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Filter for minimum quality
    tokens = [t for t in tokens if t['alpha_score'] >= 20]
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"✅ Found {len(tokens)} potential alpha memecoins")
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 60)
    
    for i, token in enumerate(tokens[:10], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,} | Vol: ${token['volume_24h']:,}")
        print(f"   📈 24h Change: {token['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🟢 Buy Ratio: {token['buy_ratio']:.1%}")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(tokens)} tokens")
    if tokens:
        top_token = tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in tokens)/len(tokens):,.0f}")
        print(f"🚀 Avg Vol/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - DYOR NFA")

if __name__ == "__main__":
    main()