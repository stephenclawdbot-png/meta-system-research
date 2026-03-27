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
    """Analyze trending pairs for alpha gems with broader criteria"""
    alpha_gems = []
    
    if not data or 'pairs' not in data or not data['pairs']:
        return alpha_gems
    
    for pair in data['pairs']:
        try:
            # Broader market cap filtering (10k-500k range)
            mcap = pair.get('fdv', 0)
            if not (10000 <= mcap <= 500000):
                continue
            
            # Lower volume threshold ($500 minimum)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            if volume_24h < 500:
                continue
                
            # Get basic info
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            price_change = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            dex_url = pair.get('url', '')
            
            # Get transaction data
            tx_24h = pair.get('txns', {}).get('h24', {})
            buys_24h = tx_24h.get('buys', 0)
            sells_24h = tx_24h.get('sells', 0)
            total_tx = buys_24h + sells_24h
            buy_ratio = buys_24h / total_tx if total_tx > 0 else 0
            
            # Calculate alpha score (enhanced)
            alpha_score = 0
            
            # Volume/mcap ratio (weighted 40 points max)
            vol_mcap_ratio = volume_24h / mcap if mcap > 0 else 0
            if vol_mcap_ratio > 2.0:
                alpha_score += 40
            elif vol_mcap_ratio > 1.0:
                alpha_score += 30
            elif vol_mcap_ratio > 0.5:
                alpha_score += 25
            elif vol_mcap_ratio > 0.2:
                alpha_score += 15
            elif vol_mcap_ratio > 0.1:
                alpha_score += 10
                
            # Price momentum (weighted 20 points max)
            if price_change > 0:
                if price_change > 100:
                    alpha_score += 20
                elif price_change > 50:
                    alpha_score += 15
                elif price_change > 20:
                    alpha_score += 10
                elif price_change > 5:
                    alpha_score += 5
                    
            # Buy ratio (weighted 20 points max)
            if buy_ratio > 0:
                if buy_ratio > 0.8:
                    alpha_score += 20
                elif buy_ratio > 0.7:
                    alpha_score += 15
                elif buy_ratio > 0.6:
                    alpha_score += 10
                elif buy_ratio > 0.55:
                    alpha_score += 5
                    
            # Liquidity bonus (weighted 10 points max)
            if liquidity > 20000:
                alpha_score += 10
            elif liquidity > 10000:
                alpha_score += 7
            elif liquidity > 5000:
                alpha_score += 5
            elif liquidity > 1000:
                alpha_score += 3
                
            # Transaction volume bonus (weighted 10 points max)
            if total_tx > 1000:
                alpha_score += 10
            elif total_tx > 500:
                alpha_score += 7
            elif total_tx > 200:
                alpha_score += 5
            elif total_tx > 50:
                alpha_score += 3
                
            alpha_gems.append({
                'symbol': symbol,
                'name': name,
                'mcap': mcap,
                'volume_24h': volume_24h,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_ratio': buy_ratio * 100,
                'total_tx': total_tx,
                'buys': buys_24h,
                'sells': sells_24h,
                'dex_url': dex_url,
                'chain': dex_url.split('/')[3] if dex_url else 'unknown'
            })
            
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    print("🎯 MEMECOIN ALPHA SCANNER - BROAD SCAN")
    print("=" * 60)
    print(f"Scan Time: {timestamp}")
    print("Market Cap Range: $10,000 - $500,000")
    print("Min Volume: $500")
    print("Alpha Detection Criteria: Enhanced multi-factor scoring")
    print()
    
    data = fetch_dexscreener_trending()
    alpha_gems = analyze_trending_pairs(data)
    
    if not alpha_gems:
        print("❌ No alpha gems found even with broader criteria")
        print("   Market appears to be exceptionally quiet")
        print("   This could indicate after-hours consolidation or technical issues")
        return
    
    print(f"💎 TOP ALPHA GEMS FOUND: {len(alpha_gems)}")
    print("=" * 60)
    
    for i, gem in enumerate(alpha_gems[:10], 1):
        print(f"\n🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100")
        print(f"   📈 24h Stats: ${gem['volume_24h']:,} vol • ${gem['mcap']:,} mcap • {gem['volume_24h']/gem['mcap']:.1%} ratio")
        print(f"   📊 Sentiment: {gem['price_change']:.1f}% price • {gem['buy_ratio']:.1f}% buy ratio")
        print(f"   🔄 Activity: {gem['total_tx']} txns ({gem['buys']} buys/{gem['sells']} sells)")
        print(f"   💧 Liquidity: ${gem['liquidity']:,}")
        print(f"   🌐 Chain: {gem['chain']}")
        print(f"   🔗 {gem['dex_url']}")
    
    if len(alpha_gems) > 0:
        avg_score = sum(g['alpha_score'] for g in alpha_gems) / len(alpha_gems)
        avg_mcap = sum(g['mcap'] for g in alpha_gems) / len(alpha_gems)
        avg_vol_ratio = sum(g['volume_24h']/g['mcap'] for g in alpha_gems) / len(alpha_gems)
        
        print(f"\n📊 MARKET SUMMARY FOR {len(alpha_gems)} GEMS")
        print("=" * 60)
        print(f"• Average Alpha Score: {avg_score:.1f}/100")
        print(f"• Average Market Cap: ${avg_mcap:,.0f}")
        print(f"• Average Volume/MCap Ratio: {avg_vol_ratio:.1f}%")
        print(f"• Top Performer: {alpha_gems[0]['symbol']} ({alpha_gems[0]['alpha_score']}/100)")
        
        print(f"\n💡 Key Alpha Signals:")
        print("- Volume/Mcap ratio > 25% indicates strong interest")
        print("- Buy ratio > 60% suggests accumulation phase")
        print("- High transaction volume = active community")
    
    print(f"\n⚠️ DISCLAIMER: High risk assets - DYOR required")

if __name__ == "__main__":
    main()