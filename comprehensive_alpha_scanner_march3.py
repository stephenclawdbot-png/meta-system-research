#!/usr/bin/env python3
"""Comprehensive Alpha Scanner for 30k-200k MCap Memecoins"""

import requests
import json
from datetime import datetime
import time

def fetch_dexscreener_comprehensive():
    """Fetch data from multiple DexScreener endpoints"""
    
    endpoints = [
        "https://api.dexscreener.com/latest/dex/search?q=sol+satoshi+dog+cat+shib",
        "https://api.dexscreener.com/latest/dex/search?q=base+memecoin",
        "https://api.dexscreener.com/latest/dex/search?q=ethereum+meme",
        "https://api.dexscreener.com/latest/dex/search?q=polygon",
        "https://api.dexscreener.com/latest/dex/search?q=bsc+memecoin"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    all_pairs = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                print(f"✓ Fetched {len(pairs)} pairs from {endpoint}")
                all_pairs.extend(pairs)
            else:
                print(f"✗ Failed: {endpoint} - Status {response.status_code}")
        except Exception as e:
            print(f"✗ Error with {endpoint}: {e}")
    
    return all_pairs

def calculate_alpha_score(token_data):
    """Calculate sophisticated alpha score out of 100"""
    
    score = 0
    
    # Volume/MCap Ratio (Max 30 points)
    vol_mcap_ratio = (token_data['volume_24h'] / token_data['mcap']) * 100 if token_data['mcap'] > 0 else 0
    if vol_mcap_ratio > 10: score += 10
    if vol_mcap_ratio > 25: score += 10
    if vol_mcap_ratio > 50: score += 10
    
    # Buy Pressure (Max 25 points)
    if token_data['buy_ratio'] > 0.5: score += 10
    if token_data['buy_ratio'] > 0.6: score += 10
    if token_data['buy_ratio'] > 0.75: score += 5
    
    # Transaction Volume (Max 20 points)
    total_txns = token_data['total_txns']
    if total_txns > 50: score += 5
    if total_txns > 100: score += 5
    if total_txns > 200: score += 5
    if total_txns > 500: score += 5
    
    # Price Momentum (Max 15 points)
    if token_data['price_change_24h'] > 10: score += 5
    if token_data['price_change_24h'] > 25: score += 5
    if token_data['price_change_24h'] > 50: score += 5
    
    # Liquidity Health (Max 10 points)
    if token_data['liquidity'] > token_data['mcap'] * 0.05: score += 5
    if token_data['liquidity'] > token_data['mcap'] * 0.1: score += 5
    
    return min(100, score)  # Cap at 100

def filter_and_score_gems(pairs):
    """Filter for 30k-200k gems and calculate alpha scores"""
    
    filtered_gems = []
    seen_urls = set()
    
    for pair in pairs:
        mcap = pair.get('fdv', pair.get('marketCap', 0))
        volume_24h = pair.get('volume', {}).get('h24', 0)
        url = pair.get('url', '')
        
        # Skip duplicates and check target range
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        # Target range: 30k-200k with minimum volume
        if mcap and 30000 <= mcap <= 200000 and volume_24h >= 100:
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            token_data = {
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume_24h': volume_24h,
                'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'total_txns': total_txns,
                'liquidity': pair.get('liquidity', {}).get('usd', 0),
                'chain': pair.get('chainId', 'Unknown'),
                'url': url
            }
            
            # Calculate alpha score
            token_data['alpha_score'] = calculate_alpha_score(token_data)
            filtered_gems.append(token_data)
    
    return sorted(filtered_gems, key=lambda x: x['alpha_score'], reverse=True)

def generate_cron_report(gems):
    """Generate professional cron report"""
    
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER - CRON REPORT
==================================================
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000
Focus: Early alpha detection before mainstream attention

"""
    
    if not gems:
        report += "🔍 No alpha gems detected in target range\nMarket currently quiet - try again later \n"
    else:
        # Sort by alpha score and get top performers
        gems.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        report += f"🔥 TOP {len(gems)} ALPHA GEMS (Sorted by Alpha Score)\n"
        report += "-" * 60 + "\n\n"
        
        for i, gem in enumerate(gems[:8], 1):
            vol_mcap_ratio = (gem['volume_24h'] / gem['mcap']) * 100 if gem['mcap'] > 0 else 0
            
            report += f"""🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100
   📈 24h Stats: ${gem['volume_24h']:,.0f} vol • ${gem['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio
   📊 Sentiment: {gem['price_change_24h']:.1f}% price • {gem['buy_ratio']:.1%} buy ratio
   🔄 Activity: {gem['total_txns']} txns ({gem['buys']} buys/{gem['sells']} sells)
   💧 Liquidity: ${gem['liquidity']:,.0f}
   🌐 Chain: {gem['chain']}
   🔗 {gem['url']}

"""
    
    # Market summary
    if gems:
        avg_score = sum(g['alpha_score'] for g in gems) / len(gems)
        avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
        avg_vol_ratio = sum((g['volume_24h'] / g['mcap']) * 100 for g in gems if g['mcap'] > 0) / len(gems)
        
        report += f"""📊 MARKET SUMMARY FOR {len(gems)} GEMS
• Average Alpha Score: {avg_score:.1f}/100
• Average Market Cap: ${avg_mcap:,.0f}
• Average Volume/MCap Ratio: {avg_vol_ratio:.1f}%
• Top Performer: {gems[0]['symbol']} ({gems[0]['alpha_score']}/100)

💡 Key Alpha Signals:
- Volume/Mcap ratio > 25% indicates strong interest
- Buy ratio > 60% suggests accumulation phase
- High transaction volume = active community

⚠️ DISCLAIMER: High risk assets - DYOR required
Next scan in 5 minutes"""
    
    return report

def main():
    print("🔍 Starting comprehensive alpha scanner...\n")
    
    # Fetch data from Dexscreener
    pairs = fetch_dexscreener_comprehensive()
    print(f"\n✓ Total pairs collected: {len(pairs)}")
    
    # Filter and score gems
    gems = filter_and_score_gems(pairs)
    print(f"✓ Filtered memecoins in target range: {len(gems)}")
    
    # Generate report
    report = generate_cron_report(gems)
    
    print("\n" + "="*70)
    print(report)
    print("="*70)
    
    # Save report for cron delivery
    with open("cron_memecoin_alpha_report_current.txt", "w") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    result = main()