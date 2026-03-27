#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import re

def is_memecoin_like(name, symbol):
    """Check if token name/symbol looks like a memecoin"""
    memecoin_patterns = [
        r'(meme|dog|cat|pepe|wojak|frog|elon|musk|moon|rocket|coin|token|inu)$',
        r'^(pepe|doge|shiba|floki|elon|moon|rocket|bonk|monkey)',
        r'.*(dog|cat|frog|meme|moon|rocket|elon).*'
    ]
    
    name_lower = name.lower()
    symbol_lower = symbol.lower()
    
    for pattern in memecoin_patterns:
        if re.search(pattern, name_lower) or re.search(pattern, symbol_lower):
            return True
    
    # Also check for popular memecoin themes
    if len(name) <= 5 or len(symbol) <= 5:  # Short names often memecoins
        return True
    
    return False

def fetch_memecoins():
    """Fetch memecoins from DexScreener search API"""
    # Search for popular memecoin related queries
    queries = ['meme', 'dog', 'cat', 'pepe', 'elon', 'moon', 'doge', 'shiba']
    
    all_tokens = []
    
    for query in queries:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'pairs' not in data:
                continue
                
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                name = token.get('baseToken', {}).get('name', '')
                symbol = token.get('baseToken', {}).get('symbol', '')
                
                # Stronger filtering for memecoins
                if (30000 <= mcap <= 200000 and 
                    is_memecoin_like(name, symbol) and
                    token.get('volume', {}).get('h24', 0) > 1000):
                    
                    token_info = {
                        'name': name,
                        'symbol': symbol,
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', ''),
                        'pairCreatedAt': token.get('pairCreatedAt', ''),
                        'txns_24h': token.get('txns', {}).get('h24', {}).get('buys', 0) + token.get('txns', {}).get('h24', {}).get('sells', 0)
                    }
                    
                    # Avoid duplicates
                    if token_info not in all_tokens:
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching {query}: {e}")
            continue
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on memecoin metrics"""
    # Base score components
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    # Age benefit - newer tokens have advantage
    age_factor = 1.0
    if token.get('pairCreatedAt'):
        try:
            from datetime import datetime
            created = datetime.fromtimestamp(token['pairCreatedAt'] / 1000)
            age_hours = (datetime.now() - created).total_seconds() / 3600
            age_factor = max(0.5, min(2.0, 48 / max(1, age_hours)))  # Exponential decay
        except:
            age_factor = 1.0
    
    # Weight different factors heavily toward volume/mcap ratio
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.5) +  # Volume/MCap ratio (most important)
        (max(0, token['price_change_24h']) * 0.2) +  # Price momentum
        (min(50, token['txns_24h'] / 10) * 0.2) +  # Transaction activity
        (age_factor * 0.1 * 100)  # Age advantage
    )
    
    return round(alpha_score, 1)

def main():
    print("🎯 MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Market Cap Range: $30k - $200k")
    print("Focus: Early alpha detection before mainstream attention")
    print()
    
    # Fetch memecoins
    tokens = fetch_memecoins()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("🔥 TOP ALPHA MEMECOINS DETECTED")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:8], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} ({token['name']}) - Alpha Score: {token['alpha_score']}/100")
        print(f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio")
        print(f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token['txns_24h']} total txns")
        print(f"   🌐 Chain: {token['chain']} • Dex: {token['dex']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary statistics
    print("📊 MARKET SUMMARY")
    print("-" * 20)
    print(f"• Total Gems Found: {len(tokens)} memecoins")
    if tokens:
        best_gem = tokens[0]
        print(f"• Best Alpha: {best_gem['symbol']} ({best_gem['alpha_score']}/100)")
        print(f"• Average Alpha Score: {sum(t['alpha_score'] for t in tokens)/len(tokens):.1f}/100")
        print(f"• Average Market Cap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"• Average Volume/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    
    print()
    print("💡 Key Alpha Signals:")
    print("- Volume/Mcap ratio > 25% indicates strong interest")
    print("- High transaction volume = active community") 
    print("- Recent token age benefits from freshness bonus")
    print()
    print("⚠️ DISCLAIMER: High risk memecoins - DYOR required")

if __name__ == "__main__":
    main()