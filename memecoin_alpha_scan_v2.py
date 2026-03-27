#!/usr/bin/env python3
"""
Targeted Memecoin Scanner for 30k-200k market cap
Search for actual memecoins using popular keywords
"""

import requests
import json
from datetime import datetime

DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"

# Popular memecoin search terms
MEMECOIN_KEYWORDS = [
    "meme", "doge", "shib", "bonk", "pepe", "floki", "sats", "cat", "dog",
    "frog", "gm", "gn", "elon", "wojak", "chad", "kek", "moon", "pump",
    "based", "degen", "autism", "retard", "woof", "meow", "giga", "chad",
    "harambe", "tate", "tucker", "rogan", "trump", "biden", "news", "trending",
    "new", "fresh", "just", "launched", "birdeye", "trading", "solana", "base"
]

def scan_with_keywords():
    """Scan using various memecoin keywords"""
    all_tokens = []
    
    for keyword in MEMECOIN_KEYWORDS[:8]:  # Limit to avoid rate limits
        try:
            response = requests.get(f"{DEXSCREENER_API}/search?q={keyword}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                tokens = data.get('pairs', [])
                all_tokens.extend(tokens)
                print(f"✓ Found {len(tokens)} tokens with '{keyword}'")
            else:
                print(f"✗ Failed for '{keyword}': {response.status_code}")
        except Exception as e:
            print(f"✗ Error with '{keyword}': {e}")
    
    # Remove duplicates
    unique_tokens = {}
    for token in all_tokens:
        addr = token.get('pairAddress', '')
        if addr:
            unique_tokens[addr] = token
    
    return list(unique_tokens.values())

def filter_tokens(tokens):
    """Filter tokens for our criteria"""
    filtered = []
    
    for token in tokens:
        try:
            mcap = token.get('marketCap', token.get('fdv', 0))
            if not (30000 <= mcap <= 200000):
                continue
                
            volume = token.get('volume', {}).get('h24', 0)
            if volume < 100:  # Minimum volume threshold
                continue
                
            filtered.append(token)
        except:
            continue
    
    return filtered

def calculate_alpha_score(token):
    """Calculate comprehensive alpha score"""
    mcap = token.get('marketCap', token.get('fdv', 0))
    volume = token.get('volume', {}).get('h24', 0)
    price_change = token.get('priceChange', {}).get('h24', 0)
    liquidity = token.get('liquidity', {}).get('usd', 0)
    
    txns = token.get('txns', {}).get('h24', {})
    buys = txns.get('buys', 0)
    sells = txns.get('sells', 0)
    total_txns = buys + sells
    buy_ratio = buys / total_txns if total_txns > 0 else 0
    
    # Age calculation
    age_hours = 999
    if 'pairCreatedAt' in token:
        try:
            created_at = datetime.fromtimestamp(token['pairCreatedAt'] / 1000)
            age_hours = (datetime.now() - created_at).total_seconds() / 3600
        except:
            pass
    
    # Score components
    volume_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    price_momentum = max(0, price_change)
    liquidity_factor = min(1, liquidity / 50000)  # Max score at $50k liquidity
    age_freshness = max(0, (48 - age_hours) / 48)  # Bonus for <48h old
    buy_pressure = buy_ratio
    
    # Weighted score (0-100)
    alpha_score = min(100, (
        min(30, volume_mcap_ratio * 0.3) +  # Volume/MCap (most important)
        min(20, price_momentum * 0.2) +      # Price momentum
        min(15, liquidity_factor * 15) +      # Liquidity depth
        min(15, age_freshness * 15) +        # Freshness bonus
        min(20, buy_pressure * 20)           # Buy pressure
    ))
    
    return alpha_score

def generate_report(tokens):
    """Generate formatted report"""
    timestamp = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')
    
    report_lines = [
        "🧠 MEMECOIN ALPHA SCANNER REPORT",
        "=" * 50,
        f"Scan Time: {timestamp}",
        f"Market Cap Range: $30k - $200k",
        f"Scan Method: Keyword-based search",
        ""
    ]
    
    if not tokens:
        report_lines.append("❌ No qualifying memecoins found")
        report_lines.append("The market may be quiet or alpha is elsewhere.")
        return "\n".join(report_lines)
    
    # Sort by alpha score
    tokens_with_scores = []
    for token in tokens:
        alpha_score = calculate_alpha_score(token)
        tokens_with_scores.append((token, alpha_score))
    
    tokens_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    report_lines.append(f"🔥 TOP ALPHA MEMECOINS ({len(tokens)} found):")
    report_lines.append("-" * 40)
    
    for i, (token, alpha_score) in enumerate(tokens_with_scores[:10], 1):
        symbol = token.get('baseToken', {}).get('symbol', 'Unknown').upper()
        name = token.get('baseToken', {}).get('name', 'Unknown')
        mcap = token.get('marketCap', token.get('fdv', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price = token.get('priceUsd', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        liquidity = token.get('liquidity', {}).get('usd', 0)
        
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        buy_ratio = buys / (buys + sells) * 100 if (buys + sells) > 0 else 0
        
        # Age
        age_hours = "Unknown"
        if 'pairCreatedAt' in token:
            try:
                created_at = datetime.fromtimestamp(token['pairCreatedAt'] / 1000)
                age_hours = round((datetime.now() - created_at).total_seconds() / 3600, 1)
            except:
                pass
        
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
        chain = token.get('chainId', 'Unknown')
        url = token.get('url', '')
        
        # Convert price to float safely
        price_float = 0.0
        price_str = str(price)
        try:
            price_float = float(price) if price else 0.0
        except:
            price_float = 0.0
        
        report_lines.extend([
            f"🎯 #{i} {symbol} ({name})",
            f"   💎 Alpha Score: {alpha_score:.0f}/100",
            f"   💰 MCap: ${mcap:,.0f} | 📊 Vol: ${volume:,.0f}",
            f"   📈 Price: ${price_float:.8f} ({price_change:+.1f}%)",
            f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}%",
            f"   🛒 Buy Ratio: {buy_ratio:.1f}%",
            f"   💧 Liquidity: ${liquidity:,.0f}",
            f"   ⏳ Age: {age_hours} hours",
            f"   🌐 Chain: {chain}",
            f"   🔗 {url}",
            ""
        ])
    
    # Summary
    avg_alpha = sum(score for _, score in tokens_with_scores) / len(tokens_with_scores)
    avg_mcap = sum(t.get('marketCap', t.get('fdv', 0)) for t, _ in tokens_with_scores) / len(tokens_with_scores)
    avg_volume = sum(t.get('volume', {}).get('h24', 0) for t, _ in tokens_with_scores) / len(tokens_with_scores)
    
    chains = set()
    for token, _ in tokens_with_scores:
        chains.add(token.get('chainId', 'Unknown'))
    
    report_lines.extend([
        "📊 SCAN SUMMARY",
        "-" * 20,
        f"• Qualified Tokens: {len(tokens)}",
        f"• Average Alpha Score: {avg_alpha:.1f}/100",
        f"• Average MCap: ${avg_mcap:,.0f}",
        f"• Average Volume: ${avg_volume:,.0f}",
        f"• Chain Distribution: {', '.join(chains)}",
        "",
        "💡 KEY SIGNALS TO WATCH:",
        "• Alpha Score > 60: Strong potential",
        "• Vol/MCap > 25%: High demand",
        "• Buy Ratio > 60%: Accumulation",
        "• Age < 24h: Fresh opportunity",
        "• Liquidity > $10k: Lower risk",
        "",
        "⚠️ DISCLAIMER: High-risk assets - Conduct your own research"
    ])
    
    return "\n".join(report_lines)

def main():
    print("🧠 Starting targeted memecoin scan...")
    print("Searching using popular memecoin keywords...")
    
    tokens = scan_with_keywords()
    print(f"\n📊 Found {len(tokens)} total tokens across searches")
    
    filtered_tokens = filter_tokens(tokens)
    print(f"✅ {len(filtered_tokens)} tokens qualify for 30k-200k range")
    
    report = generate_report(filtered_tokens)
    print("\n" + report)

if __name__ == "__main__":
    main()