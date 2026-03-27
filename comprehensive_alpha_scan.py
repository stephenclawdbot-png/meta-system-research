#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def search_memecoins(keyword=""):
    """Search DexScreener for memecoins"""
    if keyword:
        url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
    else:
        url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        filtered_tokens = []
        
        if not data or 'pairs' not in data:
            return filtered_tokens
        
        # List of wrapped tokens and major blockchain names to exclude
        wrapped_tokens = ['wbtc', 'weth', 'wsol', 'wmatic', 'wbnb', 'wftm', 'wavax']
        blockchain_names = ['solana', 'ethereum', 'bitcoin', 'cardano', 'polkadot', 'avalanche', 
                          'polygon', 'binance', 'bnb', 'arbitrum', 'optimism', 'base']
        
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            name = token.get('baseToken', {}).get('name', '').lower()
            symbol = token.get('baseToken', {}).get('symbol', '').lower()
            
            # Filter: 30k-200k mcap range
            if 30000 <= mcap <= 200000:
                # Exclude wrapped tokens and blockchain names
                if any(wrapped in name for wrapped in wrapped_tokens):
                    continue
                if any(chain in name for chain in blockchain_names):
                    continue
                if any(chain in symbol for chain in blockchain_names):
                    continue
                    
                # Additional filtering for actual memecoins
                if 'coin' in name or 'token' in name:
                    continue  # Skip generic names
                    
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
                    'pair_created_at': token.get('pairCreatedAt', 0)
                }
                filtered_tokens.append(token_info)
        
        return filtered_tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data for '{keyword}': {e}")
        return []

def calculate_alpha_score(token):
    """Calculate alpha score based on metrics"""
    # Base score components
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Boost score for newer tokens (based on creation timestamp)
    age_score = 0
    if 'pair_created_at' in token and token['pair_created_at']:
        # Estimate token age (very rough - DexScreener timestamps are weird)
        if token['pair_created_at'] > 1e12:  # Likely milliseconds
            age_score = min(15, max(0, 15 - ((1700000000000 - token['pair_created_at']) / 10000000000)))
    
    # Higher volume/mcap ratio indicates more alpha
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.6) +  # Volume/MCap ratio (most important)
        (momentum * 0.3) +         # Price momentum
        (min(20, token['volume_24h'] / 5000) * 0.1) +  # Absolute volume
        age_score                 # Age factor
    )
    
    return round(alpha_score, 1)

def main():
    print("🧠 COMPREHENSIVE MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Filters: Excludes wrapped tokens & blockchain names")
    print()
    
    # Search multiple memecoin-related keywords
    keywords = [
        "",  # Generic Solana search
        "memecoin", 
        "pepe", 
        "doge", 
        "shiba",
        "bonk",
        "cat",
        "dog",
        "meme",
        "elon",
        "trump"
    ]
    
    all_tokens = []
    seen_symbols = set()
    
    for keyword in keywords:
        tokens = search_memecoins(keyword)
        print(f"🔍 Searching '{keyword if keyword else 'solana general'}': Found {len(tokens)} tokens")
        
        for token in tokens:
            if token['symbol'] not in seen_symbols:
                seen_symbols.add(token['symbol'])
                all_tokens.append(token)
    
    if not all_tokens:
        print("\n❌ No memecoins found in 30k-200k range")
        print("Tried searches:", ", ".join(keywords))
        print("Market may be quiet or API returning limited results")
        return
    
    # Sort by alpha score
    for token in all_tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    all_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"\n🔥 TOP ALPHA MEMECOINS DETECTED ({len(all_tokens)} total):")
    print("-" * 50)
    
    for i, token in enumerate(all_tokens[:10], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(all_tokens)} tokens")
    print(f"Top Alpha Scores Range: {all_tokens[0]['alpha_score']}/100 - {all_tokens[-1]['alpha_score'] if len(all_tokens)>1 else 'N/A'}/100")
    if all_tokens:
        print(f"🥇 Highest Alpha: {all_tokens[0]['symbol']} ({all_tokens[0]['alpha_score']}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in all_tokens)/len(all_tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in all_tokens)/len(all_tokens):,.0f}")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - Do your own research!")

if __name__ == "__main__":
    main()