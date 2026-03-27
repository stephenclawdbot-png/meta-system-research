#!/usr/bin/env python3
"""
Advanced Memecoin Scanner
More comprehensive search for memecoin patterns
"""

import json
import subprocess
import time
from datetime import datetime

def fetch_multiple_sources():
    """Fetch data from multiple DexScreener sources"""
    
    pairs = []
    
    # Try different search queries
    searches = [
        'dog', 'cat', 'meme', 'pepe', 'shib', 'floki', 'inu', 'baby', 'elon',
        'wojak', 'frog', '🐶', '🐱', '🧸', '🐸', '👑', '🚀', '🌕'
    ]
    
    for search_term in searches:
        try:
            cmd = f"curl -s 'https://api.dexscreener.com/latest/dex/search?q={search_term}&limit=50'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('pairs'):
                    pairs.extend(data['pairs'])
            
            time.sleep(0.2)  # Rate limiting
        except Exception as e:
            print(f"Error searching {search_term}: {e}")
    
    return pairs

def analyze_memecoins(pairs):
    """Analyze pairs for memecoin alpha gems"""
    
    memecoin_indicators = [
        'dog', 'cat', 'meme', 'pepe', 'shib', 'floki', 'elon', 'baby', 'inu', 
        'toshi', 'wojak', 'frog', '🐶', '🐱', '🧸', '🐸', '👑', '🚀', '🌕'
    ]
    
    alpha_gems = []
    processed_addrs = set()
    
    for pair in pairs:
        try:
            pair_addr = pair.get('pairAddress')
            if pair_addr in processed_addrs:
                continue
            processed_addrs.add(pair_addr)
            
            # Get basic metrics
            symbol = pair.get('baseToken', {}).get('symbol', '').upper()
            name = pair.get('baseToken', {}).get('name', '').lower()
            mcap = pair.get('marketCap', 0) or pair.get('fdv', 0)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            
            # Skip if not in range
            if not (30000 <= mcap <= 200000):
                continue
            
            if volume_24h < 1000:
                continue
            
            # Check if it's a memecoin
            is_memecoin = False
            for indicator in memecoin_indicators:
                if (indicator in symbol.lower() or 
                    indicator in name or 
                    indicator in pair.get('baseToken', {}).get('name', '').lower()):
                    is_memecoin = True
                    break
            
            if not is_memecoin:
                continue
            
            # Get detailed metrics
            price = pair.get('priceUsd', 0)
            price_change_24h = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            dex_url = pair.get('url', '')
            
            # Transaction data
            txns_24h = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Calculate alpha score
            alpha_score = 0
            
            # Volume/mcap ratio (30 pts)
            if mcap > 0:
                vol_ratio = volume_24h / mcap
                if vol_ratio > 2.0: alpha_score += 30
                elif vol_ratio > 1.0: alpha_score += 25
                elif vol_ratio > 0.5: alpha_score += 20
                elif vol_ratio > 0.2: alpha_score += 15
                elif vol_ratio > 0.1: alpha_score += 10
            
            # Buy pressure (25 pts)
            if buy_ratio > 80: alpha_score += 25
            elif buy_ratio > 65: alpha_score += 20
            elif buy_ratio > 55: alpha_score += 15
            elif buy_ratio > 50: alpha_score += 10
            
            # Price momentum (20 pts)
            if price_change_24h > 100: alpha_score += 20
            elif price_change_24h > 50: alpha_score += 15
            elif price_change_24h > 25: alpha_score += 10
            elif price_change_24h > 10: alpha_score += 5
            
            # Liquidity/health (15 pts)
            if liquidity > 20000: alpha_score += 15
            elif liquidity > 10000: alpha_score += 12
            elif liquidity > 5000: alpha_score += 10
            elif liquidity > 2500: alpha_score += 8
            elif liquidity > 1000: alpha_score += 5
            
            # Transaction count (10 pts)
            if total_txns > 1000: alpha_score += 10
            elif total_txns > 500: alpha_score += 8
            elif total_txns > 200: alpha_score += 6
            elif total_txns > 100: alpha_score += 4
            elif total_txns > 50: alpha_score += 2
            
            alpha_gems.append({
                'symbol': symbol,
                'name': name,
                'mcap': mcap,
                'price': price,
                'volume_24h': volume_24h,
                'volume_mcap_ratio': volume_24h / mcap if mcap > 0 else 0,
                'price_change_24h': price_change_24h,
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'liquidity': liquidity,
                'total_txns': total_txns,
                'alpha_score': alpha_score,
                'dex_url': dex_url
            })
            
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    print("🎯 ADVANCED MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print(f"Scan Time: {datetime.now().strftime('%A, March 2, 2026 — %I:%M %p (Asia/Manila)')}")
    print()
    
    print("🔍 Searching DexScreener for memecoin patterns...")
    pairs = fetch_multiple_sources()
    
    print(f"📊 Found {len(pairs)} total pairs")
    
    if not pairs:
        print("❌ No data returned")
        return
    
    alpha_gems = analyze_memecoins(pairs)
    
    print(f"💎 Memecoin alpha candidates: {len(alpha_gems)}")
    print()
    
    if not alpha_gems:
        print("❌ No alpha gems found in 30k-200k mcap range")
        print("\n📊 Market Analysis:")
        print("- Current DexScreener trending dominated by major tokens")
        print("- Monday morning market activity may be reduced")
        print("- Pump.fun might have more memecoin activity")
        return
    
    print(f"🥇 TOP 5 ALPHA MEMECOINS:")
    print("=" * 60)
    
    for i, gem in enumerate(alpha_gems[:5], 1):
        print(f"\n{i}. {gem['symbol']} | Alpha Score: {gem['alpha_score']}/100")
        print(f"   Name: {gem['name']}")
        print(f"   MCap: ${gem['mcap']:,} | Volume: ${gem['volume_24h']:,}")
        print(f"   Volume/MCap: {gem['volume_mcap_ratio']:.1%}")
        print(f"   Price: ${float(gem['price']):.6f} | Change: {gem['price_change_24h']:.1f}%")
        print(f"   Buy Ratio: {gem['buy_ratio']:.1f}% ({gem['buys']}/{gem['sells']})")
        print(f"   Liquidity: ${gem['liquidity']:,}")
        print(f"   Total Txns: {gem['total_txns']}")
        print(f"   DexScreener: {gem['dex_url']}")
    
    print(f"\n📈 MARKET OVERVIEW:")
    print("=" * 60)
    
    # Analyze market conditions
    avg_mcap = sum(gem['mcap'] for gem in alpha_gems) / len(alpha_gems) if alpha_gems else 0
    avg_volume = sum(gem['volume_24h'] for gem in alpha_gems) / len(alpha_gems) if alpha_gems else 0
    avg_buy_ratio = sum(gem['buy_ratio'] for gem in alpha_gems) / len(alpha_gems) if alpha_gems else 0
    
    print(f"Average MCap in range: ${avg_mcap:,.0f}")
    print(f"Average Volume: ${avg_volume:,.0f}")
    print(f"Average Buy Ratio: {avg_buy_ratio:.1f}%")
    print(f"Total candidates: {len(alpha_gems)}")
    print(f"Maximum Alpha Score: {alpha_gems[0]['alpha_score'] if alpha_gems else 0}/100")
    print("\n⚠️  Early Monday morning scan - market activity typically lower")

if __name__ == "__main__":
    main()