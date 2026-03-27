#!/usr/bin/env python3
import json
import requests
from datetime import datetime

def fetch_dexscreener_trending():
    """Fetch trending pairs from DexScreener with better error handling"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching trending tokens: {e}")
        return None

def fetch_popular_memecoins():
    """Search for popular memecoin patterns"""
    memecoin_keywords = ['PEPE', 'BONK', 'WIF', 'MEME', 'DOGE', 'SHIB', 'FLOKI']
    all_results = []
    
    for keyword in memecoin_keywords:
        url = f"https://api.dexscreener.com/latest/dex/search/?q={keyword}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('pairs'):
                    all_results.extend(data['pairs'])
        except Exception as e:
            print(f"Error searching for {keyword}: {e}")
    
    return all_results

def filter_alpha_candidates_30k_200k(pairs):
    """Filter for memecoins in the 30k-200k market cap range"""
    candidates = []
    seen_symbols = set()
    
    for pair in pairs:
        if not pair:
            continue
            
        symbol = pair.get('baseToken', {}).get('symbol', '').upper()
        
        # Skip duplicates and obvious non-memecoins
        if symbol in seen_symbols:
            continue
        seen_symbols.add(symbol)
        
        # Skip major tokens
        skip_keywords = ['USDC', 'USDT', 'BTC', 'ETH', 'SOL', 'BNB', 'MATIC', 'AVAX', 'W']
        if any(skip in symbol for skip in skip_keywords):
            continue
        
        market_cap = pair.get('fdv', 0) or pair.get('marketCap', 0)
        
        # Target range: $30k - $200k
        if 30000 <= market_cap <= 200000:
            volume_24h = pair.get('volume', {}).get('h24', 0)
            price = pair.get('priceUsd', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            
            # Transaction data
            txns_h24 = pair.get('txns', {}).get('h24', {})
            buys = txns_h24.get('buys', 0)
            sells = txns_h24.get('sells', 0)
            txns_total = buys + sells
            buy_ratio = buys / txns_total if txns_total > 0 else 0
            
            # Calculate alpha score
            alpha_score = 0
            
            # Volume/MCap ratio (0-40 points)
            if market_cap > 0:
                vol_mcap_ratio = volume_24h / market_cap
                alpha_score += min(40, vol_mcap_ratio * 100)
            
            # Buy pressure (0-25 points)
            alpha_score += min(25, buy_ratio * 25)
            
            # Momentum (0-20 points)
            if price_change and price_change > 0:
                alpha_score += min(20, price_change * 2)
            
            # Liquidity (0-15 points)
            if liquidity > market_cap * 0.1:
                alpha_score += 15
            
            candidate = {
                'symbol': symbol,
                'name': pair.get('baseToken', {}).get('name', ''),
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'price': price,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buys': buys,
                'sells': sells,
                'buy_ratio': buy_ratio,
                'url': pair.get('url', ''),
                'chain': pair.get('chainId', '')
            }
            
            candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def main():
    print("💎 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP FOCUS")
    print("=" * 60)
    print("Scan Time: " + datetime.now().strftime('%A, %B %d, %Y — %I:%M %p'))
    print("Target Range: $30,000 - $200,000 Market Cap")
    print()
    
    print("🔍 Fetching DexScreener data...")
    
    # Try trending endpoint first
    trending_data = fetch_dexscreener_trending()
    all_pairs = []
    
    if trending_data and 'pairs' in trending_data and trending_data['pairs']:
        print("✅ Got trending data")
        all_pairs.extend(trending_data['pairs'])
    else:
        print("❌ Trending endpoint unavailable")
    
    # Try search endpoint for memecoins
    print("🔍 Searching popular memecoins...")
    search_results = fetch_popular_memecoins()
    all_pairs.extend(search_results)
    
    if not all_pairs:
        print("❌ No data retrieved from DexScreener")
        return
    
    print(f"📊 Processing {len(all_pairs)} pairs...")
    candidates = filter_alpha_candidates_30k_200k(all_pairs)
    
    print(f"\n✅ Found {len(candidates)} Tokens in 30k-200k Range")
    print("-" * 60)
    
    if not candidates:
        print("No memecoins found in the target market cap range.")
        print("Market conditions may be quiet or the range is too narrow.")
        return
    
    # Display top 10 candidates
    for i, candidate in enumerate(candidates[:10], 1):
        print(f"\n{i}. 🎯 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        print(f"   📛 {candidate['name']}")
        print(f"   💰 MCap: ${candidate['market_cap']:,}")
        print(f"   📈 Vol/24h: ${candidate['volume_24h']:,}")
        print(f"   💵 Price: ${candidate['price']}")
        print(f"   📊 24h Change: {candidate['price_change'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {(candidate['volume_24h']/candidate['market_cap']*100) if candidate['market_cap'] > 0 else 0:.1f}%")
        print(f"   🟢 Buy Ratio: {candidate['buy_ratio']:.1%}")
        print(f"   💧 Liquidity: ${candidate['liquidity']:,}")
        print(f"   🌐 Chain: {candidate['chain']}")
        print(f"   🔗 {candidate['url']}")
    
    # Summary
    print(f"\n📊 MARKET ANALYSIS")
    print("-" * 25)
    if candidates:
        avg_mcap = sum(c['market_cap'] for c in candidates) / len(candidates)
        avg_volume = sum(c['volume_24h'] for c in candidates) / len(candidates)
        avg_vol_mcap = sum((c['volume_24h']/c['market_cap']*100) for c in candidates if c['market_cap'] > 0) / len(candidates)
        
        print(f"Total Gems: {len(candidates)}")
        print(f"Avg MCap: ${avg_mcap:,.0f}")
        print(f"Avg Volume: ${avg_volume:,.0f}")
        print(f"Avg Vol/MCap Ratio: {avg_vol_mcap:.1f}%")
        print(f"Top Alpha: {candidates[0]['symbol']} ({candidates[0]['alpha_score']:.1f})")
    
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - DYOR NFA")

if __name__ == "__main__":
    main()