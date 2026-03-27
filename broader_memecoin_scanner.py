#!/usr/bin/env python3
"""
Broader Memecoin Scanner - Wider market cap ranges
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_tokens():
    """Fetch tokens from DexScreener"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'pairs' in data:
                return data['pairs']
            else:
                print("No 'pairs' found in response")
                return []
        else:
            print(f"API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []


def filter_memecoin_opportunities_by_ranges(tokens):
    """Filter tokens by different market cap ranges"""
    ranges = [
        (5000, 30000, "MICRO"),
        (30000, 200000, "TARGET"),
        (200000, 1000000, "SMALL"),
        (1000000, 5000000, "MID")
    ]
    
    results = {}
    
    if not tokens:
        return results
        
    for token in tokens:
        try:
            market_cap = token.get('marketCap', 0)
            base_token = token.get('baseToken', {})
            symbol = base_token.get('symbol', 'Unknown')
            
            # Skip main SOL pairs
            if symbol == 'SOL' or 'solana' in base_token.get('name', '').lower():
                continue
            
            for min_mcap, max_mcap, category in ranges:
                if min_mcap <= market_cap <= max_mcap:
                    volume_24h = token.get('volume', {}).get('h24', 0)
                    price_change_24h = token.get('priceChange', {}).get('h24', 0)
                    liquidity = token.get('liquidity', {}).get('usd', 0)
                    
                    txns = token.get('txns', {}).get('h24', {})
                    buys = txns.get('buys', 0)
                    sells = txns.get('sells', 0)
                    total_txns = buys + sells
                    buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
                    
                    vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
                    alpha_score = min(100, vol_mcap_ratio * 1.5)
                    
                    opportunity = {
                        'symbol': symbol,
                        'name': base_token.get('name', 'Unknown'),
                        'market_cap': market_cap,
                        'volume_24h': volume_24h,
                        'price_change_24h': price_change_24h,
                        'liquidity': liquidity,
                        'buy_ratio': buy_ratio,
                        'vol_mcap_ratio': vol_mcap_ratio,
                        'alpha_score': alpha_score,
                        'url': token.get('url', '')
                    }
                    
                    if category not in results:
                        results[category] = []
                    results[category].append(opportunity)
                    break
                    
        except Exception as e:
            continue
    
    # Sort each category by alpha score
    for category in results:
        results[category].sort(key=lambda x: x['alpha_score'], reverse=True)
    
    return results

def main():
    print("🎯 BROADER MEMECOIN SCANNER")
    print("=" * 60)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print()
    
    print("Fetching DexScreener data...")
    tokens = fetch_dexscreener_tokens()
    
    if not tokens:
        print("❌ No tokens found from DexScreener API")
        return
        
    print(f"✅ Found {len(tokens)} total tokens")
    
    # Filter by different ranges
    results = filter_memecoin_opportunities_by_ranges(tokens)
    
    print(f"\n📊 MARKET CAP SCAN RESULTS")
    print("=" * 30)
    
    # Define ranges and their labels
    ranges = [
        ("MICRO", "$5K-$30K"),
        ("TARGET", "$30K-$200K"),
        ("SMALL", "$200K-$1M"),
        ("MID", "$1M-$5M")
    ]
    
    total_opportunities = 0
    for category, label in ranges:
        count = len(results.get(category, []))
        total_opportunities += count
        print(f"{category}: {count} tokens {label}")
    
    print(f"Total Opportunities: {total_opportunities}")
    
    # Show detailed results for each category
    for category, label in ranges:
        opportunities = results.get(category, [])
        if opportunities:
            print(f"\n🔥 {label} ALPHA OPPORTUNITIES")
            print("-" * 40)
            
            for i, opp in enumerate(opportunities[:5], 1):  # Top 5 per category
                print(f"{i}. {opp['symbol']} - Alpha: {opp['alpha_score']:.1f}")
                print(f"   Market Cap: ${opp['market_cap']:,}")
                print(f"   Vol/MCap: {opp['vol_mcap_ratio']:.2f}%")
                print(f"   24h Change: {opp['price_change_24h']:.2f}%")
                print(f"   Buy Ratio: {opp['buy_ratio']:.1f}%")
                print(f"   URL: {opp['url']}")
    
    if total_opportunities == 0:
        print("\n⚠️ No memecoins detected in any range. Market appears quiet.")
    else:
        print(f"\n🎯 Focus on TARGET range ($30K-$200K) opportunities:")
        target_opps = results.get("TARGET", [])
        if target_opps:
            for opp in target_opps:
                print(f"• {opp['symbol']} - MCap: ${opp['market_cap']:,} - Alpha: {opp['alpha_score']:.1f}")
        else:
            print("No TARGET range opportunities - expanding search to other ranges")
            for category, label in ranges:
                if category != "TARGET" and results.get(category):
                    opps = results[category]
                    print(f"\n{label} alternatives:")
                    for opp in opps[:3]:
                        print(f"• {opp['symbol']} - MCap: ${opp['market_cap']:,} - Alpha: {opp['alpha_score']:.1f}")
    
    print("\n⚠️ HIGH RISK - RESEARCH REQUIRED")

if __name__ == "__main__":
    main()