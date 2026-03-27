#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins_by_keywords():
    """Fetch memecoins using various search terms"""
    search_terms = [
        'dog', 'cat', 'pepe', 'floki', 'bonk', 'shib', 'doge', 'elon', 'moon', 
        'mars', 'wif', 'frog', 'ape', 'degens', 'rocket', 'based', 'chad'
    ]
    
    all_tokens = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                for token in data.get('pairs', []):
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
                            'createdAt': token.get('createdAt', '')
                        }
                        
                        # Avoid duplicates
                        if token_info not in all_tokens:
                            all_tokens.append(token_info)
            
        except Exception as e:
            print(f"Error fetching {term}: {e}")
            continue
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on metrics"""
    volume = max(token['volume_24h'], 0)
    mcap = max(token['mcap'], 1)  # Avoid division by zero
    vol_mcap_ratio = (volume / mcap) * 100
    momentum = max(token['price_change_24h'], 0) if token['price_change_24h'] else 0
    
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.6) + 
        (momentum * 0.3) + 
        (min(100, volume / 1000) * 0.1)
    )
    
    return round(max(alpha_score, 0), 1)

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - 30K-200K MCAP FOCUS")
    print("=" * 70)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Alpha Criteria: High volume/mcap ratio + positive momentum")
    print()
    
    # Fetch tokens
    tokens = fetch_memecoins_by_keywords()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Remove duplicates based on name+symbol+mcap
    unique_tokens = []
    seen = set()
    for token in tokens:
        key = f"{token['name']}-{token['symbol']}-{token['mcap']}"
        if key not in seen:
            seen.add(key)
            unique_tokens.append(token)
    
    tokens = unique_tokens
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Filter for alpha potential: minimum 1% vol/mcap ratio
    alpha_tokens = [t for t in tokens if (t['volume_24h'] / max(t['mcap'], 1)) * 100 >= 1]
    
    if not alpha_tokens:
        print("❌ No tokens with sufficient volume/mcap ratio found")
        return
    
    # Sort by alpha score (highest first)
    alpha_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 70)
    
    for i, token in enumerate(alpha_tokens[:15], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - {token['name']}")
        print(f"   💎 Alpha Score: {token['alpha_score']}/100")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol 24h: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Memecoins Found: {len(tokens)}")
    print(f"Alpha Candidates (Vol/MCap > 1%): {len(alpha_tokens)}")
    print(f"Top Alpha Score: {alpha_tokens[0]['alpha_score']}/100")
    
    if len(alpha_tokens) > 1:
        avg_score = sum(t['alpha_score'] for t in alpha_tokens[:5]) / min(5, len(alpha_tokens))
        print(f"Avg Top 5 Score: {avg_score:.1f}/100")
    
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - DYOR/NFA")

if __name__ == "__main__":
    main()