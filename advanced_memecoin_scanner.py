#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_meme_tokens():
    """Search for various meme tokens across different chains"""
    queries = ["meme", "dog", "cat", "pepe", "shib", "elon", "wojak", "doge", "bonk"]
    
    all_tokens = []
    
    for query in queries:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                for token in data['pairs']:
                    mcap = token.get('fdv', 0)
                    
                    # Filter: 30k-200k mcap range
                    if 30000 <= mcap <= 200000:
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
                            'search_query': query
                        }
                        all_tokens.append(token_info)
            
            # Small delay to be polite to the API
            import time
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error searching for {query}: {e}")
    
    return all_tokens

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
        (min(100, token['volume_24h'] / 1000) * 0.1)  # Absolute volume (scaled)
    )
    
    return round(alpha_score, 1)

def main():
    print("🧠 ADVANCED MEMECOIN ALPHA SCANNER")
    print("=" * 50)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target Range: $30k - $200k Market Cap")
    print()
    
    # Fetch meme tokens
    print("🔍 Searching for meme tokens...")
    tokens = fetch_meme_tokens()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Remove duplicates based on symbol
    unique_tokens = []
    seen_symbols = set()
    for token in tokens:
        if token['symbol'] not in seen_symbols:
            seen_symbols.add(token['symbol'])
            unique_tokens.append(token)
    
    # Sort by volume/mcap ratio to find alpha
    unique_tokens.sort(key=lambda x: x['volume_24h'] / x['mcap'], reverse=True)
    
    print(f"🔥 TOP ALPHA MEMECOINS DETECTED ({len(unique_tokens)} total):")
    print("-" * 60)
    
    for i, token in enumerate(unique_tokens[:15], 1):
        alpha_score = calculate_alpha_score(token)
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {alpha_score}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Unique Gems: {len(unique_tokens)} tokens")
    if unique_tokens:
        top_token = unique_tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({calculate_alpha_score(top_token)}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in unique_tokens)/len(unique_tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in unique_tokens)/len(unique_tokens):,.0f}")
        print(f"🚀 Top Vol/MCap Ratio: {max((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in unique_tokens):.1f}%")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - NFA")

if __name__ == "__main__":
    main()