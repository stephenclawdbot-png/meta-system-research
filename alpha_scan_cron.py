#!/usr/bin/env python3
"""
Alpha Scanner for Cron Job - Single Run
Scans DexScreener for tokens with:
- Market cap: $30k-$200k
- Minimum volume: $1k
- Good buy pressure
- Trending status
"""

import requests
import json
from datetime import datetime

def fetch_trending_tokens(min_mcap=30000, max_mcap=200000, min_volume=1000):
    """Fetch trending tokens from DexScreener with filtering"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        alpha_gems = []
        
        for pair in data:
            try:
                mcap = pair.get('marketCap', 0)
                volume_24h = pair.get('volume', {}).get('h24', 0)
                
                # Apply filters
                if not (min_mcap <= mcap <= max_mcap):
                    continue
                    
                if volume_24h < min_volume:
                    continue
                
                # Get additional metrics
                symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                name = pair.get('baseToken', {}).get('name', 'Unknown')
                price = pair.get('priceUsd', 0)
                price_change_24h = pair.get('priceChange', {}).get('h24', 0)
                dex_url = pair.get('url', '#')
                chain = pair.get('chainId', 'Unknown')
                
                # Calculate transaction metrics
                txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
                buys = txns.get('buys', 0)
                sells = txns.get('sells', 0)
                total_txns = buys + sells
                buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
                
                # Calculate alpha score (simplified)
                # Volume/Mcap ratio + buy ratio + trending factor
                vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
                alpha_score = min(100, vol_mcap_ratio + buy_ratio)
                
                gem_data = {
                    'symbol': symbol,
                    'name': name,
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price': price,
                    'price_change_24h': price_change_24h,
                    'buy_ratio': buy_ratio,
                    'total_txns': total_txns,
                    'alpha_score': alpha_score,
                    'chain': chain,
                    'dex_url': dex_url,
                    'vol_mcap_ratio': vol_mcap_ratio
                }
                
                alpha_gems.append(gem_data)
                
            except Exception as e:
                continue
                
        # Sort by volume/mcap ratio (high volume relative to mcap is good)
        alpha_gems.sort(key=lambda x: x['vol_mcap_ratio'], reverse=True)
        return alpha_gems
        
    except Exception as e:
        print(f"Error fetching trending tokens: {e}")
        return []

def main():
    print("💎 ALPHA SCANNER - DexScreener Trending Analysis")
    print("=" * 60)
    print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Filters: MCap $30k-$200k | Volume > $1k")
    print()
    
    gems = fetch_trending_tokens()
    
    if not gems:
        print("❌ No alpha gems found matching criteria")
        return
    
    print(f"🔥 {len(gems)} ALPHA GEMS DETECTED:")
    print("-" * 60)
    print()
    
    for i, gem in enumerate(gems[:10], 1):  # Top 10 gems
        # Format numbers
        mcap_str = f"${gem['mcap']:,.0f}"
        volume_str = f"${gem['volume_24h']:,.0f}"
        price_str = f"${gem['price']:.6f}" if gem['price'] < 0.01 else f"${gem['price']:.4f}"
        
        print(f"{i}. 🎯 {gem['symbol']} ({gem['name']})")
        print(f"   💰 MCap: {mcap_str}")
        print(f"   📈 24h Vol: {volume_str}")
        print(f"   💸 Price: {price_str}")
        print(f"   📊 24h Change: {gem['price_change_24h']:.1f}%")
        print(f"   🛒 Buy Ratio: {gem['buy_ratio']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
        print(f"   ⚡ Alpha Score: {min(100, gem['alpha_score']):.0f}/100")
        print(f"   🌐 Chain: {gem['chain'].upper()}")
        print(f"   🔗 DexScreener: {gem['dex_url']}")
        print()
    
    # Summary
    top_gem = gems[0] if gems else None
    if top_gem:
        print("📊 SUMMARY:")
        print(f"   • Best Alpha: {top_gem['symbol']} ({top_gem['alpha_score']:.0f}/100)")
        print(f"   • Highest Vol/Mcap: {top_gem['symbol']} ({top_gem['vol_mcap_ratio']:.1f}%)")
        print(f"   • Total Promising Tokens: {len(gems)}")
    
    print()
    print("ℹ️ DYOR - High risk, high potential")

if __name__ == "__main__":
    main()