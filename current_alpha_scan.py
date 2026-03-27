#!/usr/bin/env python3
"""
Quick DexScreener Alpha Scanner
Focus on 30k-200k mcap memecoins
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_new_pairs():
    """Fetch new pairs from DexScreener"""
    url = "https://api.dexscreener.com/latest/dex/search?q=new"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching DexScreener: {e}")
    return None

def assess_alpha_gems():
    """Assess alpha gems in 30k-200k mcap range"""
    data = fetch_dexscreener_new_pairs()
    alpha_gems = []
    
    if data and 'pairs' in data:
        for pair in data['pairs']:
            mcap = pair.get('fdv', 0)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            
            # Filter for 30k-200k mcap
            if 30000 <= mcap <= 200000:
                # Calculate alpha score
                score = 0
                
                # Volume scoring
                if volume_24h > 10000:
                    score += 30
                elif volume_24h > 5000:
                    score += 20
                elif volume_24h > 1000:
                    score += 10
                
                # Volume/MCap ratio scoring
                vol_ratio = (volume_24h / mcap * 100) if mcap > 0 else 0
                if vol_ratio > 100:
                    score += 25
                elif vol_ratio > 50:
                    score += 15
                elif vol_ratio > 20:
                    score += 10
                
                # Price momentum
                price_change = pair.get('priceChange', {}).get('h24', 0)
                if price_change > 50:
                    score += 20
                elif price_change > 20:
                    score += 10
                elif price_change > 0:
                    score += 5
                
                # Transaction activity
                txns = pair.get('txns', {}).get('h24', {})
                buyers = txns.get('buys', 0)
                sellers = txns.get('sells', 0)
                total_txns = buyers + sellers
                
                if total_txns > 200:
                    score += 15
                elif total_txns > 100:
                    score += 10
                elif total_txns > 50:
                    score += 5
                
                # Buy pressure
                buy_ratio = buyers / (buyers + sellers) if (buyers + sellers) > 0 else 0
                if buy_ratio > 0.7:
                    score += 10
                elif buy_ratio > 0.6:
                    score += 7
                elif buy_ratio > 0.5:
                    score += 5
                
                alpha_gems.append({
                    'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                    'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price_change': price_change,
                    'vol_mcap_ratio': vol_ratio,
                    'buyers': buyers,
                    'sellers': sellers,
                    'total_txns': total_txns,
                    'buy_ratio': buy_ratio,
                    'alpha_score': score,
                    'url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                    'chain': pair.get('chainId', '')
                })
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems[:10]  # Return top 10

def generate_report():
    """Generate alpha scanner report"""
    gems = assess_alpha_gems()
    timestamp = datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')
    
    print(f"🚀 MEMECOIN ALPHA SCANNER UPDATE")
    print("=" * 60)
    print(f"Scan Time: {timestamp}")
    print(f"Focus: Sub-200k MCap Gems (30k-200k range)")
    print("=" * 60)
    print()
    
    if gems:
        print(f"💎 Found {len(gems)} Promising Alpha Gems")
        print("-" * 60)
        print()
        
        for i, gem in enumerate(gems, 1):
            print(f"🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/80")
            print(f"   📈 Market Cap: ${gem['mcap']:,}")
            print(f"   💰 24h Volume: ${gem['volume_24h']:,}")
            print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
            print(f"   📊 Price Change: {gem['price_change']:.2f}%")
            print(f"   🔄 Transactions: {gem['total_txns']} (buys: {gem['buyers']}, sells: {gem['sellers']})")
            print(f"   📈 Buy Ratio: {gem['buy_ratio']:.1%}")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 Dex: {gem['url']}")
            print()
    else:
        print("⚠️ No alpha gems found in the 30k-200k range")
        print("Market conditions may be quiet")
        print()
    
    # Summary
    if gems:
        avg_score = sum(g['alpha_score'] for g in gems) / len(gems)
        avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
        avg_vol = sum(g['volume_24h'] for g in gems) / len(gems)
        
        print("📊 QUICK ANALYSIS:")
        print("-" * 30)
        print(f"• Average Alpha Score: {avg_score:.1f}/80")
        print(f"• Avg Market Cap: ${avg_mcap:,.0f}")
        print(f"• Avg Volume: ${avg_vol:,.0f}")
        print(f"• Total Candidates: {len(gems)}")
        print()
    
    print("💡 KEY ALPHA SIGNALS TO WATCH:")
    print("-" * 35)
    print("• Volume/Mcap > 25% = Strong interest")
    print("• Buy ratio > 60% = Accumulation phase")
    print("• High transaction volume = Active community")
    print("• Positive price momentum = Upside potential")
    print()
    print("⚠️ DISCLAIMER: High risk micro-cap space - DYOR required")

if __name__ == "__main__":
    generate_report()