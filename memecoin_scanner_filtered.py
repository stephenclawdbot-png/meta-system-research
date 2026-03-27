#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Fetch memecoins from DexScreener with better filtering"""
    url = "https://api.dexscreener.com/latest/dex/search?q=meme%20doge%20pepe%20bonk%20shiba"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        filtered_tokens = []
        
        if not data or 'pairs' not in data:
            return filtered_tokens
        
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            name = token.get('baseToken', {}).get('name', '').lower()
            symbol = token.get('baseToken', {}).get('symbol', '').lower()
            
            # Enhanced filtering for genuine memecoins
            skip_patterns = [
                'wrapped', 'weth', 'usdc', 'usdt', 'dai', 'stable', 'eth', 'btc',
                'ethereum', 'bitcoin', 'matic', 'solana', 'dot', 'bnb', 'avax',
                'near', 'arbitrum', 'optimism', 'base', 'polygon'
            ]
            
            should_skip = any(pattern in name or pattern in symbol for pattern in skip_patterns)
            
            # Filter: 30k-200k mcap range and skip wrapper coins
            if 30000 <= mcap <= 200000 and not should_skip:
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
        
        return filtered_tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
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
        (min(100, token['volume_24h'] / 1000) * 0.1)  # Absolute volume (scaled)
    )
    
    return round(alpha_score, 1)

def main():
    print("🎯 FILTERED MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Focus: Filtered memecoins only (no wrapped coins)")
    print()
    
    # Fetch tokens
    tokens = fetch_memecoins()
    
    if not tokens:
        print("❌ No genuine memecoins found in 30k-200k range")
        print("This could mean:")
        print("• Market is quiet at this time")
        print("• No memecoins in our range are gaining traction")
        print("• Try scanning again in 15-30 minutes")
        return
    
    # Sort by volume/mcap ratio to find alpha
    tokens.sort(key=lambda x: x['volume_24h'] / x['mcap'], reverse=True)
    
    print(f"📊 Found {len(tokens)} genuine memecoins")
    print("\n🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:10], 1):
        alpha_score = calculate_alpha_score(token)
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        # More detailed analysis
        print(f"\n🎯 #{i} {token['symbol']} ({token['name']})")
        print(f"   📊 Alpha Score: {alpha_score}/100")
        print(f"   💰 Market Cap: ${token['mcap']:,.0f}")
        print(f"   📈 24h Volume: ${token['volume_24h']:,.0f}")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   📈 Price Change: {token['price_change_24h']:.1f}%")
        print(f"   🌐 Dex: {token['dex']} | Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
    
    # Summary statistics
    print("\n📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(tokens)}")
    if tokens:
        top_token = tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} "
              f"({calculate_alpha_score(top_token)}/100 score)")
        print(f"💰 Average Market Cap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"📈 Average Volume: ${sum(t['volume_24h'] for t in tokens)/len(tokens):,.0f}")
        print(f"🚀 Average Vol/MCap Ratio: "
              f"{sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    
    print("\n💡 Alpha Signals:")
    print("• Vol/MCap ratio > 25% = strong momentum")
    print("• Positive price change = bullish sentiment")
    print("• High Alpha Score = multiple positive factors")
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - NFA")

if __name__ == "__main__":
    main()