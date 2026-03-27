#!/usr/bin/env python3
import json
import requests
from datetime import datetime

def fetch_trending_memecoins():
    """Fetch trending memecoins from DexScreener with broader criteria"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching trending tokens: {e}")
        return None

def filter_alpha_candidates(data, max_mcap=1000000):
    """Filter for promising memecoins with loose criteria"""
    candidates = []
    
    if not data or 'pairs' not in data:
        return candidates
    
    for pair in data['pairs'][:50]:  # Check first 50 trending pairs
        # Skip obvious non-memecoins
        symbol = pair.get('baseToken', {}).get('symbol', '').upper()
        name = pair.get('baseToken', {}).get('name', '').lower()
        
        # Skip major tokens and obvious non-memecoins
        skip_keywords = ['USDC', 'USDT', 'BTC', 'ETH', 'SOL', 'BNB', 'MATIC', 'AVAX']
        blacklist = ['wrapped', 'stablecoin', 'liquid staking']
        
        if any(skip in symbol for skip in skip_keywords) or any(bl in name for bl in blacklist):
            continue
            
        market_cap = pair.get('marketCap', 0)
        
        # Broader range since market seems quiet
        if market_cap <= max_mcap:
            volume_24h = pair.get('volume', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            # Basic alpha score calculation
            alpha_score = 0
            if volume_24h > 1000:
                alpha_score += 20
            if liquidity > 5000:
                alpha_score += 15
            if price_change > 0:
                alpha_score += 10
            if volume_24h > 10000:
                alpha_score += 15
            if market_cap < 500000:  # Smaller caps higher potential
                alpha_score += 15
            
            candidate = {
                'symbol': symbol,
                'name': pair.get('baseToken', {}).get('name', ''),
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'price': pair.get('priceUsd', 0),
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'url': pair.get('url', ''),
                'chain': pair.get('chainId', '')
            }
            
            if alpha_score >= 30:  # Only include decent candidates
                candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def main():
    print("💎 MEMECOIN ALPHA SCANNER - BROAD RANGE")
    print("=" * 60)
    print("Scan Time: " + datetime.now().strftime('%A, March 2nd, 2026 — %I:%M %p'))
    print()
    
    print("Fetching trending DexScreener data...")
    data = fetch_trending_memecoins()
    
    if not data:
        print("❌ Failed to fetch data")
        return
    
    candidates = filter_alpha_candidates(data)
    
    print(f"\n✅ Found {len(candidates)} Alpha Candidates")
    print("-" * 50)
    
    if not candidates:
        print("No promising memecoins detected in current market.")
        print("Market conditions may be quiet or major selloff impacting prices.")
        return
    
    # Display results
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. 🎯 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']}/60")
        print(f"   💰 Market Cap: ${candidate['market_cap']:,}")
        print(f"   📈 24h Volume: ${candidate['volume_24h']:,}")
        print(f"   📊 Price: ${candidate['price']} ({candidate['price_change']:.2f}%)")
        print(f"   💧 Liquidity: ${candidate['liquidity']:,}")
        print(f"   🌐 Chain: {candidate['chain']}")
        print(f"   🔗 DexScreener: {candidate['url'][:80]}...")
    
    print("\n📊 MARKET SUMMARY")
    print("-" * 25)
    print(f"Total candidates: {len(candidates)}")
    print(f"Highest Alpha Score: {max(c['alpha_score'] for c in candidates) if candidates else 0}")
    print(f"Total market cap scanned: ${sum(c['market_cap'] for c in candidates):,}")
    
    print("\n⚠️ RISK DISCLAIMER: MEMECOINS = HIGH VOLATILITY")
    print("Always DYOR before investing. This is not financial advice.")

if __name__ == "__main__":
    main()