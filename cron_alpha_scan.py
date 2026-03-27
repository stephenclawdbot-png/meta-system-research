#!/usr/bin/env python3
"""
Cron Alpha Scanner - Multiple API endpoints for memecoin detection
"""

import requests
import json
from datetime import datetime
import urllib.request

def try_api_dexscreener():
    """Try multiple DexScreener API endpoints"""
    endpoints = [
        "https://api.dexscreener.com/latest/dex/tokens/new",
        "https://api.dexscreener.com/latest/dex/tokens/trending",
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=base",
        "https://api.dexscreener.com/latest/dex/search?q=ethereum"
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

def filter_memecoins(pairs):
    """Filter for 30k-200k mcap memecoins"""
    filtered = []
    
    for pair in pairs:
        # Try multiple mcap fields
        mcap = pair.get('fdv', pair.get('marketCap', 0))
        volume = pair.get('volume', {}).get('h24', 0)
        
        if mcap and 30000 <= mcap <= 200000 and volume >= 1000:
            # Calculate alpha score
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Simple scoring
            alpha_score = 0
            if buy_ratio > 0.5: alpha_score += 30
            if volume > 5000: alpha_score += 25
            if mcap < 100000: alpha_score += 20
            if buy_ratio > 0.6: alpha_score += 15
            if volume > 10000: alpha_score += 10
            
            filtered.append({
                'symbol': pair.get('baseToken', {}).get('symbol', 'N/A'),
                'name': pair.get('baseToken', {}).get('name', 'N/A'),
                'mcap': mcap,
                'volume': volume,
                'price_change': pair.get('priceChange', {}).get('h24', 0),
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'alpha_score': alpha_score,
                'chain': pair.get('chainId', 'N/A'),
                'pair_address': pair.get('pairAddress', 'N/A'),
                'url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}"
            })
    
    return sorted(filtered, key=lambda x: x['alpha_score'], reverse=True)

def generate_cron_report(memecoins):
    """Generate report for cron delivery"""
    timestamp = datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER CRON REPORT
==================================================
Scanning DexScreener for sub 30k-200k MCap gems
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000

"""
    
    if not memecoins:
        report += "🔍 No alpha gems detected in target range\nMarket may be quiet or API limitations encountered\n"
    else:
        report += f"🔥 TOP {min(len(memecoins), 5)} ALPHA GEMS\n------------------------------\n"
        
        for i, gem in enumerate(memecoins[:5], 1):
            report += f"""{i}. {gem['symbol']}: ${gem['mcap']:,} MCap • {gem['alpha_score']}/100 Alpha Score
   📊 Volume: ${gem['volume']:,} • Buy Ratio: {gem['buy_ratio']:.1%}
   🔄 Txns: {gem['buys']} buys / {gem['sells']} sells
   🌐 Chain: {gem['chain']} • {gem['url']}

"""
    
    # Add market summary
    if memecoins:
        total_gems = len(memecoins)
        avg_score = sum(g['alpha_score'] for g in memecoins) / len(memecoins)
        avg_mcap = sum(g['mcap'] for g in memecoins) / len(memecoins)
        
        report += f"""📊 MARKET SUMMARY
• Total Candidates: {total_gems}
• Average Alpha Score: {avg_score:.1f}/100
• Average Market Cap: ${avg_mcap:,.0f}

💡 Alpha gems detected before mainstream attention.
Buy ratio &gt; 50% suggests accumulation phase.
DYOR - High risk volatile assets.

Next scan in 5 minutes."""
    
    return report

def main():
    print("🔍 Starting comprehensive alpha scan...")
    
    # Try multiple API endpoints
    pairs = try_api_dexscreener()
    print(f"Total pairs collected: {len(pairs)}")
    
    # Filter for memecoins
    memecoins = filter_memecoins(pairs)
    print(f"Filtered memecoins: {len(memecoins)}")
    
    # Generate report
    report = generate_cron_report(memecoins)
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save for cron delivery
    with open("cron_alpha_report.txt", "w") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    result = main()
    print("\n📄 Cron report saved")
    print(result)