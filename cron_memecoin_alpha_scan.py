#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_tokens(search_queries):
    """Fetch tokens from DexScreener for multiple search queries"""
    all_tokens = []
    
    for query in search_queries:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data and data['pairs']:
                # Filter by market cap range
                for token in data['pairs']:
                    mcap = token.get('fdv', 0)
                    
                    # Focus on 30k-200k market cap range
                    if 30000 <= mcap <= 200000:
                        # Extract transaction data
                        txn_data = token.get('txns', {})
                        h24_buys = txn_data.get('h24', {}).get('buys', 0)
                        h24_sells = txn_data.get('h24', {}).get('sells', 0)
                        
                        # Only include tokens with meaningful activity
                        if h24_buys + h24_sells < 5:
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
                            'buy_ratio': h24_buys / (h24_buys + h24_sells) if (h24_buys + h24_sells) > 0 else 0,
                            'search_term': query
                        }
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching for query '{query}': {e}")
            continue
    
    return all_tokens

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
    txn_velocity = min(15, (token['h24_buys'] + token['h24_sells']) / 10)
    
    # Composite alpha score
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.3) +      # Volume/MCap ratio
        (buy_pressure * 0.25) +        # Buy pressure
        (momentum * 0.2) +             # Price momentum
        (age_score * 0.15) +            # Newness bonus
        (txn_velocity * 0.1)            # Transaction activity
    )
    
    return round(alpha_score, 1)

def remove_duplicates(tokens):
    """Remove duplicate tokens by pair address"""
    seen = set()
    unique_tokens = []
    for token in tokens:
        if token['pairAddress'] not in seen:
            seen.add(token['pairAddress'])
            unique_tokens.append(token)
    return unique_tokens

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP FOCUS")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Metrics: Volume/MCap Ratio, Buy Pressure, Momentum, Age")
    print()
    
    # Search queries for memecoins
    search_queries = [
        "PEPE", "DOGE", "SHIB", "BONK", "FLOKI", "WIF", "BOME", "MEME",
        "GUAC", "PUDGY", "POPCAT", "MOOK", "HARAMBE", "HODL", "HONEY",
        "CAT", "FROG", "DOG", "SAFE", "RUG", "SOL", "ETH", "BTC"
    ]
    
    print(f"🔍 Searching {len(search_queries)} popular memecoin terms...")
    
    # Fetch tokens
    tokens = fetch_dexscreener_tokens(search_queries)
    tokens = remove_duplicates(tokens)
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Filter for minimum quality
    tokens = [t for t in tokens if t['alpha_score'] >= 25]
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"✅ Found {len(tokens)} potential alpha memecoins")
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 60)
    
    for i, token in enumerate(tokens[:15], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,} | Vol: ${token['volume_24h']:,}")
        print(f"   📈 24h Change: {token['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🟢 Buy Ratio: {token['buy_ratio']:.1%}")
        print(f"   🔍 Search: '{token['search_term']}'")
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