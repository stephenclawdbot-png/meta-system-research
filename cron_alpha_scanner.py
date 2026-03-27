#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Fetch memecoins from DexScreener search API"""
    # Search for popular memecoin terms across chains
    searches = ["dog", "cat", "meme", "ai", "pepe", "wif", "bonk", "elon", "doge", "sol", "eth", "btc", "satoshi", "pump", "fun", "alpha", "gem", "nft", "degen", "ape"]
    all_tokens = []
    
    for search_term in searches:
        url = f"https://api.dexscreener.com/latest/dex/search?q={search_term}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        
            filtered_tokens = []
            
            if not data or 'pairs' not in data:
                continue
            
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                name = token.get('baseToken', {}).get('name', '').lower()
                symbol = token.get('baseToken', {}).get('symbol', '').lower()
                
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
                        'chain': token.get('chainId', '')
                    }
                    filtered_tokens.append(token_info)
            
            all_tokens.extend(filtered_tokens)
            
        except Exception as e:
            print(f"Error searching for '{search_term}': {e}")
            continue
    
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
    print("🧠 MEMECOIN ALPHA SCANNER - 30K-200K MCAP FOCUS")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target Range: $30k - $200k Market Cap")
    print()
    
    # Fetch tokens
    tokens = fetch_memecoins()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Sort by volume/mcap ratio to find alpha
    tokens.sort(key=lambda x: x['volume_24h'] / x['mcap'], reverse=True)
    
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:10], 1):
        alpha_score = calculate_alpha_score(token)
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {alpha_score}/100")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(tokens)} tokens")
    if tokens:
        top_token = tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({calculate_alpha_score(top_token)}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in tokens)/len(tokens):,.0f}")
        print(f"🚀 Avg Vol/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - NFA")

if __name__ == "__main__":
    main()