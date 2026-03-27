#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def search_dexscreener(query):
    """Search DexScreener for tokens matching query"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        filtered_tokens = []
        
        if not data or 'pairs' not in data:
            return filtered_tokens
        
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            # Filter: 30k-200k mcap range
            if 30000 <= mcap <= 200000:
                token_info = {
                    'query': query,
                    'name': token.get('baseToken', {}).get('name', 'Unknown'),
                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': token.get('volume', {}).get('h24', 0),
                    'price': token.get('priceUsd', 0),
                    'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                    'url': token.get('url', ''),
                    'dex': token.get('dexId', ''),
                    'chain': token.get('chainId', '')
                }
                filtered_tokens.append(token_info)
        
        return filtered_tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data for {query}: {e}")
        return []

def calculate_alpha_score(token):
    """Calculate alpha score based on metrics"""
    # Base score components
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Weight different factors
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.6) +  # Volume/MCap ratio (most important)
        (momentum * 0.3) +        # Price momentum
        (min(100, token['volume_24h'] / 100) * 0.1)  # Absolute volume (scaled)
    )
    
    return round(alpha_score, 1)

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - 30K-200K MCAP FOCUS")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Focus: Early alpha detection before mainstream attention")
    print()
    
    # Search queries for different memecoin types
    queries = ["cat", "dog", "meme", "pepe", "doge", "shiba", "floki", "wojak", "elon", "based"]
    
    all_tokens = []
    
    for query in queries:
        tokens = search_dexscreener(query)
        all_tokens.extend(tokens)
    
    if not all_tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Remove duplicates based on URL
    unique_tokens = {}
    for token in all_tokens:
        unique_tokens[token['url']] = token
    all_tokens = list(unique_tokens.values())
    
    # Calculate alpha scores
    for token in all_tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Sort by alpha score
    all_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(all_tokens[:15], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(all_tokens)} tokens")
    if all_tokens:
        top_token = all_tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in all_tokens)/len(all_tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in all_tokens)/len(all_tokens):,.0f}")
        print(f"🚀 Avg Vol/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in all_tokens)/len(all_tokens):.1f}%")
        print(f"📋 Avg Alpha Score: {sum(t['alpha_score'] for t in all_tokens)/len(all_tokens):.1f}/100")
    print()
    print("💡 Key Alpha Signals:")
    print("- Volume/Mcap ratio > 25% indicates strong interest")
    print("- Positive price momentum = growing demand")
    print("- High transaction volume = active community")
    print()
    print("⚠️ DISCLAIMER: High risk assets - DYOR required")
    print("Next scan in 5 minutes")

if __name__ == "__main__":
    main()