#!/usr/bin/env python3
import requests
from datetime import datetime

# Memecoin keywords to search
KEYWORDS = ["meme", "pepe", "doge", "bonk", "shiba", "dog", "cat", "kitty", "puppy", "frog", "elon", "musk"]

def fetch_tokens(keyword):
    """Fetch tokens for a specific keyword"""
    try:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/search?q={keyword}", timeout=10)
        data = response.json()
        return data.get('pairs', [])
    except:
        return []

def calculate_alpha_score(token):
    """Calculate alpha score 0-100 for a token"""
    mcap = token.get('marketCap', 0)
    volume = token.get('volume', {}).get('h24', 0)
    price_change = token.get('priceChange', {}).get('h24', 0) or 0
    liquidity = token.get('liquidity', {}).get('usd', 0)
    
    # Volume/MCap ratio (most important)
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    vol_score = min(40, vol_mcap_ratio * 0.4)
    
    # Price momentum
    momentum_score = max(0, min(20, price_change * 0.5))
    
    # Liquidity score
    liquidity_score = min(20, liquidity / 10000)
    
    # Buy ratio bonus
    txns = token.get('txns', {}).get('h24', {})
    buys = txns.get('buys', 0)
    sells = txns.get('sells', 0)
    buy_ratio = (buys / (buys + sells) * 100) if (buys + sells) > 0 else 50
    buy_score = min(20, buy_ratio * 0.2)
    
    return vol_score + momentum_score + liquidity_score + buy_score

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - CRON REPORT")
    print("=" * 70)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print(f"Market Cap Range: $30,000 - $200,000")
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print()
    
    all_tokens = []
    
    # Fetch tokens for each keyword
    for keyword in KEYWORDS:
        tokens = fetch_tokens(keyword)
        filtered_tokens = [
            token for token in tokens 
            if token.get('marketCap', 0) and 30000 <= token['marketCap'] <= 200000
        ]
        all_tokens.extend(filtered_tokens)
    
    # Remove duplicates by pair address
    unique_tokens = {}
    for token in all_tokens:
        addr = token.get('pairAddress')
        if addr:
            unique_tokens[addr] = token
    
    # Calculate scores and filter
    scored_tokens = []
    for token in unique_tokens.values():
        score = calculate_alpha_score(token)
        if score >= 20:  # Minimum threshold
            token['alpha_score'] = score
            scored_tokens.append(token)
    
    # Sort by alpha score
    scored_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Reporting
    print(f"📊 MARKET OVERVIEW:")
    print(f"• Total tokens scanned: {len(all_tokens)}")
    print(f"• Unique tokens in range: {len(unique_tokens)}")
    print(f"• Tokens with alpha score ≥20: {len(scored_tokens)}")
    print()
    
    if scored_tokens:
        print("🔥 TOP ALPHA GEMS:")
        print("-" * 70)
        
        for i, token in enumerate(scored_tokens[:10], 1):
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
            name = token.get('baseToken', {}).get('name', 'Unknown')
            mcap = token.get('marketCap', 0)
            volume = token.get('volume', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            price_change = token.get('priceChange', {}).get('h24', 0)
            chain = token.get('chainId', 'Unknown')
            
            print(f"🎯 #{i} {symbol} ({chain}) - Alpha Score: {token['alpha_score']:.1f}/100")
            print(f"   📛 {name}")
            print(f"   💰 MCap: ${mcap:,} | Vol: ${volume:,.0f}")
            print(f"   📈 24h Change: {price_change or 0:.1f}%")
            print(f"   💧 Liquidity: ${liquidity:,.0f}")
            
            # Transaction data
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            if buys > 0 or sells > 0:
                buy_ratio = (buys / (buys + sells) * 100) if buys + sells > 0 else 0
                print(f"   🔄 Buy Ratio: {buy_ratio:.1f}% ({buys}/{sells})")
            
            print(f"   🔗 {token.get('url', '')}")
            print()
        
        # Market metrics
        avg_score = sum(t['alpha_score'] for t in scored_tokens) / len(scored_tokens)
        avg_mcap = sum(t['marketCap'] for t in scored_tokens) / len(scored_tokens)
        avg_volume = sum(t.get('volume', {}).get('h24', 0) for t in scored_tokens) / len(scored_tokens)
        
        print("📈 MARKET METRICS:")
        print(f"• Avg Alpha Score: {avg_score:.1f}/100")
        print(f"• Avg Market Cap: ${avg_mcap:,.0f}")
        print(f"• Avg Volume: ${avg_volume:,.0f}")
        print(f"• Top Alpha Score: {scored_tokens[0]['alpha_score']:.1f}/100")
    else:
        print("❌ No alpha gems found in the target range")
        
        # Show some tokens for context
        if unique_tokens:
            sample = list(unique_tokens.values())[:3]
            print("\nSample tokens found (scored below alpha threshold):")
            for token in sample:
                symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
                mcap = token.get('marketCap', 0)
                volume = token.get('volume', {}).get('h24', 0)
                print(f"• {symbol}: MCap ${mcap:,}, Volume ${volume:,}")
    
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - Not financial advice")
    print("• These are high-risk, speculative assets")
    print("• Always perform your own research")
    print("• Only invest what you can afford to lose")

if __name__ == "__main__":
    main()