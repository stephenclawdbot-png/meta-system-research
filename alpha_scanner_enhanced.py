#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins_by_keywords(keywords):
    """Fetch memecoins from DexScreener using multiple keyword searches"""
    all_tokens = []
    
    for keyword in keywords:
        url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'pairs' not in data:
                continue
            
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                
                # Filter: 30k-200k mcap range
                if 30000 <= mcap <= 200000:
                    # Deduplicate by address
                    token_address = token.get('pairAddress', '')
                    if not any(t.get('pairAddress') == token_address for t in all_tokens):
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                            'pairAddress': token_address,
                            'mcap': mcap,
                            'volume_24h': token.get('volume', {}).get('h24', 0),
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'url': token.get('url', ''),
                            'dex': token.get('dexId', ''),
                            'chain': token.get('chainId', ''),
                            'created_at': token.get('pairCreatedAt', 0),
                            'search_term': keyword
                        }
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching data for keyword '{keyword}': {e}")
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on multiple metrics"""
    
    # Get token age in hours
    if token.get('created_at'):
        import time
        age_hours = max(1, (time.time() * 1000 - token['created_at']) / (1000 * 60 * 60))
    else:
        age_hours = 24  # Default age
    
    # Base score components
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Age-based multiplier - newer tokens get bonus
    age_multiplier = max(0.5, min(2.0, 48 / age_hours))  # 2x for 24h old, less for older
    
    # Weight different factors
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.5 * age_multiplier) +  # Volume/MCap ratio (age-weighted)
        (momentum * 0.3) +                        # Price momentum
        (min(100, token['volume_24h'] / 1000) * 0.2)  # Absolute volume (scaled)
    )
    
    return round(alpha_score, 1)

def filter_quality_tokens(tokens):
    """Filter tokens to remove low-quality ones"""
    filtered = []
    
    for token in tokens:
        # Skip tokens with absurd symbols or names
        skip_patterns = [
            'wrapped', 'weth', 'usdc', 'usdt', 'dai', 'stable', 'eth', 'btc',
            'ethereum', 'bitcoin', 'matic', 'solana'
        ]
        
        symbol = token['symbol'].lower()
        name = token['name'].lower()
        
        should_skip = any(pattern in symbol or pattern in name for pattern in skip_patterns)
        
        # Skip if it's just a wrapped version of major coins
        if not should_skip:
            filtered.append(token)
    
    return filtered

def main():
    # Memecoin-related search terms
    keywords = [
        'meme', 'memecoin', 'pepe', 'doge', 'shiba', 'wojak', 'bonk', 'wif',
        'cat', 'dog', 'elon', 'trump', 'alpha', 'pump', 'gem', 'moon', 'to',
        '100x', '1000x', 'based', 'degen', 'giga', 'chad', 'frog', 'penguin',
        'ai', 'artificial', 'intelligence', 'web3', 'nft', 'degods', 'pudgy'
    ]
    
    print("🎯 ENHANCED MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print(f"Searching: {len(keywords)} categories")
    print()
    
    # Fetch tokens
    tokens = fetch_memecoins_by_keywords(keywords)
    tokens = filter_quality_tokens(tokens)
    
    if not tokens:
        print("❌ No quality memecoins found in 30k-200k range")
        return
    
    print(f"📊 Found {len(tokens)} unique tokens")
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Sort by alpha score (highest first)
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("\n🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:15], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        # Calculate age if available
        age_text = ""
        if token.get('created_at'):
            import time
            age_hours = max(1, (time.time() * 1000 - token['created_at']) / (1000 * 60 * 60))
            if age_hours < 24:
                age_text = f" | Age: {age_hours:.1f}h"
        
        print(f"\n🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   📈 Market Cap: ${token['mcap']:,.0f} | Volume: ${token['volume_24h']:,.0f}")
        print(f"   📊 24h Change: {token['price_change_24h']:.1f}% | Vol/MCap: {vol_mcap_ratio:.1f}%{age_text}")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔍 Found via: '{token['search_term']}'")
        print(f"   🔗 {token['url']}")
    
    # Summary statistics
    print("\n📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Quality Gems: {len(tokens)}")
    if tokens:
        top_token = tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']}/100)")
        print(f"💰 Avg MCap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"📈 Avg Volume: ${sum(t['volume_24h'] for t in tokens)/len(tokens):,.0f}")
        print(f"🚀 Avg Vol/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
        print(f"🎯 Avg Alpha Score: {sum(t['alpha_score'] for t in tokens)/len(tokens):.1f}/100")
    
    print("\n💡 Alpha Signals:")
    print("• Vol/MCap ratio > 20% = high interest")
    print("• Age < 24h = fresh opportunity")
    print("• Alpha Score > 50 = strong potential")
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - DYOR required")

if __name__ == "__main__":
    main()