#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def fetch_dexscreener_trending():
    """Fetch trending pairs from DexScreener"""
    try:
        cmd = "curl -s 'https://api.dexscreener.com/latest/dex/tokens/trending'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

def analyze_trending_pairs(data):
    """Analyze trending pairs for alpha gems"""
    alpha_gems = []
    
    if not data or 'pairs' not in data or not data['pairs']:
        return alpha_gems
    
    for pair in data['pairs']:
        try:
            # Market cap filtering (30k-200k range)
            mcap = pair.get('fdv', 0)
            if not (30000 <= mcap <= 200000):
                continue
            
            # Volume filtering ($1k minimum)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            if volume_24h < 1000:
                continue
                
            # Get basic info
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            price_change = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            dex_url = pair.get('url', '')
            
            # Calculate alpha score (simplified)
            alpha_score = 0
            
            # Volume/mcap ratio
            vol_mcap_ratio = volume_24h / mcap
            if vol_mcap_ratio > 1.0:
                alpha_score += 40
            elif vol_mcap_ratio > 0.5:
                alpha_score += 30
            elif vol_mcap_ratio > 0.2:
                alpha_score += 20
            elif vol_mcap_ratio > 0.1:
                alpha_score += 10
                
            # Price momentum
            if price_change > 0:
                if price_change > 50:
                    alpha_score += 30
                elif price_change > 20:
                    alpha_score += 20
                elif price_change > 10:
                    alpha_score += 10
                    
            # Liquidity bonus
            if liquidity > 5000:
                alpha_score += 10
            elif liquidity > 2000:
                alpha_score += 5
                
            alpha_gems.append({
                'symbol': symbol,
                'name': name,
                'mcap': mcap,
                'volume_24h': volume_24h,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'dex_url': dex_url
            })
            
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    print("🎯 MEMECOIN ALPHA SCANNER - CRON EXECUTION")
    print("=" * 60)
    print(f"Scan Time: {timestamp}")
    print("Market Cap Range: $30,000 - $200,000")
    print("Min Volume: $1,000")
    print("Alpha Detection Criteria: Volume/MCap Ratio + Price Momentum")
    print()
    
    data = fetch_dexscreener_trending()
    alpha_gems = analyze_trending_pairs(data)
    
    if not alpha_gems:
        print("❌ No alpha gems found matching criteria")
        print("   The DexScreener trending API may be returning limited data")
        print("   OR the market is currently quiet for small-cap gems")
        return
    
    print(f"💎 TOP ALPHA GEMS FOUND: {len(alpha_gems)}")
    print("=" * 60)
    
    for i, gem in enumerate(alpha_gems[:10], 1):
        print(f"\n{i}. {gem['symbol']} - Alpha Score: {gem['alpha_score']}/80")
        print(f"   Name: {gem['name']}")
        print(f"   Market Cap: ${gem['mcap']:,}")
        print(f"   24h Volume: ${gem['volume_24h']:,}")
        print(f"   Volume/MCap: {(gem['volume_24h']/gem['mcap']):.1%}")
        print(f"   Price Change: {gem['price_change']:.1f}%")
        print(f"   Liquidity: ${gem['liquidity']:,}")
        print(f"   DexScreener: {gem['dex_url']}")
    
    print(f"\n📊 SCANNER STATUS")
    print("=" * 60)
    print("✓ DexScreener API: RESPONDING")
    print(f"✓ Alpha Scanner: PROCESSED {len(alpha_gems)} candidates")
    print("⚠️ Note: Market may be consolidating during off-peak hours")

if __name__ == "__main__":
    main()