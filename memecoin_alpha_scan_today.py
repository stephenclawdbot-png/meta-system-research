#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Fetch memecoins from DexScreener search API"""
    # Search for memecoin-related terms
    memecoin_terms = ["meme", "pepe", "doge", "cat", "wif", "bonk", "frog", "eye", "hat", "cap", "bird", "leash"]
    all_tokens = []
    
    for term in memecoin_terms:
        url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                for token in data['pairs']:
                    mcap = token.get('fdv', 0)
                    # Filter for our target range: $30k-$200k
                    if 30000 <= mcap <= 200000:
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                            'mcap': mcap,
                            'volume24h': token.get('volume', {}).get('h24', 0),
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'url': token.get('url', ''),
                            'dex': token.get('dexId', ''),
                            'chain': token.get('chainId', ''),
                            'search_term': term
                        }
                        all_tokens.append(token_info)
        except Exception as e:
            print(f"Error fetching for term '{term}': {e}")
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on memecoin metrics"""
    # Higher volume/mcap ratio indicates serious interest
    vol_mcap_ratio = (token['volume24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Memecoin-specific scoring weights
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.7) +  # Heavy weight on volume/mcap (most important for memecoins)
        (momentum * 0.2) +        # Positive price momentum
        (min(100, token['volume24h'] / 1000) * 0.1)  # Absolute volume bonus
    )
    
    return round(alpha_score, 1)

def main():
    print("🦤 MEMECOIN ALPHA SCANNER - SUB-200K MCAP GEMS")
    print("=" * 70)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print()
    
    # Fetch tokens
    tokens = fetch_memecoins()
    
    # Remove duplicates by contract address using URL as proxy
    unique_tokens = {}
    for token in tokens:
        unique_tokens[token['url']] = token
    tokens = list(unique_tokens.values())
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Sort by alpha score (volume/mcap ratio)
    tokens.sort(key=lambda x: (x['volume24h'] / x['mcap']) if x['mcap'] > 0 else 0, reverse=True)
    
    print(f"🎯 ALPHA MEMECOINS DETECTED ({len(tokens)} tokens):")
    print("-" * 60)
    
    for i, token in enumerate(tokens[:20], 1):
        alpha_score = calculate_alpha_score(token)
        vol_mcap_ratio = (token['volume24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🏆 #{i} {token['symbol']} - Alpha Score: {alpha_score}/100")
        print(f"   📛 Name: {token['name'][:30]}")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔍 Source: '{token['search_term']}' search")
        print(f"   🔗 {token['url'][:80]}...")
        print()
    
    # Summary statistics
    if tokens:
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_volume = sum(t['volume24h'] for t in tokens) / len(tokens)
        avg_vol_mcap_ratio = sum((t['volume24h']/t['mcap']*100 if t['mcap'] > 0 else 0) for t in tokens) / len(tokens)
        
        print("📊 SCAN SUMMARY:")
        print("-" * 20)
        print(f"Total Gems Found: {len(tokens)}")
        print(f"Average MCap: ${avg_mcap:,.0f}")
        print(f"Average Volume: ${avg_volume:,.0f}")
        print(f"Avg Vol/MCap Ratio: {avg_vol_mcap_ratio:.1f}%")
        
        # Show top memecoin categories by search term
        term_counts = {}
        for token in tokens:
            term = token['search_term']
            term_counts[term] = term_counts.get(term, 0) + 1
        
        print(f"\n🔍 Popular Themes: {', '.join(f'{k}({v})' for k, v in term_counts.items())}")
    
    print("\n⚠️  DISCLAIMER: High-risk memecoin alpha detection - NFA (DYOR)")

if __name__ == "__main__":
    main()