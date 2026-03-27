#!/usr/bin/env python3
"""
Quick Alpha Scanner for Cron Job - March 4, 2026
Scans DexScreener for memecoins with $30k-$200k market cap
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_memecoins():
    """Fetch memecoins from DexScreener API"""
    tokens = []
    
    # Common memecoin keywords to search
    searches = ["MEME", "DOG", "AI", "CAT", "PEPE", "ELON", "SHIB", "FLOKI", "BONK"]
    
    for keyword in searches:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('pairs'):
                    for pair in data['pairs']:
                        mcap = pair.get('marketCap', 0)
                        if 30000 <= mcap <= 200000:
                            tokens.append(pair)
            print(f"✓ Found {len([t for t in tokens if keyword in t.get('baseToken', {}).get('symbol', '')])} {keyword} tokens")
            
        except Exception as e:
            print(f"❌ Error fetching {keyword}: {e}")
    
    return tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on multiple factors"""
    score = 0
    
    # Market cap score (lower = better for growth)
    mcap = token.get('marketCap', 0)
    if mcap < 50000:
        score += 30
    elif mcap < 100000:
        score += 25
    else:
        score += 20
    
    # Volume/24h
    volume_24h = token.get('volume', {}).get('h24', 0)
    vol_mcap_ratio = volume_24h / mcap if mcap > 0 else 0
    
    if vol_mcap_ratio > 1.0:
        score += 40
    elif vol_mcap_ratio > 0.5:
        score += 30
    elif vol_mcap_ratio > 0.2:
        score += 20
    elif vol_mcap_ratio > 0.1:
        score += 10
    
    # Recent price movement
    price_change = token.get('priceChange', {}).get('h24', 0)
    if price_change > 50:
        score += 15
    elif price_change > 20:
        score += 10
    elif price_change > 10:
        score += 5
    
    # Transaction activity
    txns = token.get('txns', {}).get('h24', {})
    total_txns = txns.get('buys', 0) + txns.get('sells', 0)
    if total_txns > 1000:
        score += 10
    elif total_txns > 500:
        score += 7
    elif total_txns > 100:
        score += 3
    
    # Buy/sell ratio
    if total_txns > 0:
        buy_ratio = txns.get('buys', 0) / total_txns
        if buy_ratio > 0.6:
            score += 5
    
    return min(score, 100)

def main():
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    print("🎯 MEMECOIN ALPHA SCANNER - CRON REPORT")
    print("=" * 60)
    print(f"Scan Time: {timestamp}")
    print("Market Cap Range: $30,000 - $200,000")
    print("Alpha Detection Criteria: Volume/MCap Ratio + Activity")
    print()
    
    tokens = fetch_dexscreener_memecoins()
    
    if not tokens:
        print("❌ No memecoins found matching criteria")
        return
    
    # Calculate alpha scores
    alpha_tokens = []
    for token in tokens:
        score = calculate_alpha_score(token)
        if score >= 0:  # Include all for now, we'll filter later
            base_token = token.get('baseToken', {})
            alpha_tokens.append({
                'symbol': base_token.get('symbol', 'Unknown'),
                'name': base_token.get('name', 'Unknown'),
                'mcap': token.get('marketCap', 0),
                'volume_24h': token.get('volume', {}).get('h24', 0),
                'price_change': token.get('priceChange', {}).get('h24', 0),
                'alpha_score': score,
                'dex_url': token.get('url', ''),
                'chain': token.get('chainId', '')
            })
    
    # Sort by alpha score
    alpha_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"\n💎 TOP ALPHA GEMS FOUND: {len(alpha_tokens)}")
    print("=" * 60)
    
    for i, gem in enumerate(alpha_tokens[:10], 1):
        vol_percent = (gem['volume_24h'] / gem['mcap']) * 100 if gem['mcap'] > 0 else 0
        print(f"\n#{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        print(f"   💰 MCap: ${gem['mcap']:,} | Vol: ${gem['volume_24h']:,}")
        print(f"   📈 24h Change: {gem['price_change']:+.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_percent:.1f}%")
        print(f"   🌐 Dex: {gem['chain']}")
        print(f"   🔗 {gem['dex_url']}")
    
    # Summary
    avg_mcap = sum(gem['mcap'] for gem in alpha_tokens) / len(alpha_tokens)
    avg_vol = sum(gem['volume_24h'] for gem in alpha_tokens) / len(alpha_tokens)
    avg_ratio = avg_vol / avg_mcap * 100 if avg_mcap > 0 else 0
    
    print(f"\n📊 SCAN SUMMARY:")
    print("=" * 60)
    print(f"Total Gems Found: {len(alpha_tokens)} tokens")
    print(f"🥇 Highest Alpha: {alpha_tokens[0]['symbol'] if alpha_tokens else 'None'} ({alpha_tokens[0]['alpha_score'] if alpha_tokens else 0}/100)")
    print(f"💰 Avg MCap: ${avg_mcap:,.0f}")
    print(f"📈 Avg Volume: ${avg_vol:,.0f}")
    print(f"🚀 Avg Vol/MCap Ratio: {avg_ratio:.1f}%")
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - NFA")

if __name__ == "__main__":
    main()