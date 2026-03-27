#!/usr/bin/env python3
"""
Immediate Alpha Scanner - 30k-200k MCap Focus
Scan DexScreener for high-potential memecoins before mainstream attention
"""

import json
import requests
import time
from datetime import datetime

def get_dexscreener_trending():
    """Fetch trending tokens from DexScreener API - try multiple endpoints"""
    endpoints = [
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=ethereum", 
        "https://api.dexscreener.com/latest/dex/search?q=bsc",
        "https://api.dexscreener.com/latest/dex/search?q=base"
    ]
    
    all_pairs = []
    
    for url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            print(f"Fetched from {url.split('q=')[1]}: {len(data.get('pairs', []))} pairs")
            
            if 'pairs' in data and data['pairs']:
                all_pairs.extend(data['pairs'])
                
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    
    print(f"Total pairs found: {len(all_pairs)}")
    return all_pairs

def calculate_alpha_score(pair):
    """Calculate alpha score based on multiple factors"""
    volume_usd = float(pair.get('volume', {}).get('h24', 0))
    mcap = float(pair.get('fdv', 0))
    
    # Skip if mcap is outside our target range
    if mcap < 30000 or mcap > 200000:
        return 0
    
    price_change = float(pair.get('priceChange', {}).get('h24', 0))
    liquidity = float(pair.get('liquidity', {}).get('usd', 0))
    
    # Score components
    volume_score = min(30, volume_usd / 1000)  # Base 30 points for volume
    vol_mcap_ratio = volume_usd / mcap if mcap > 0 else 0
    vol_mcap_score = min(20, vol_mcap_ratio * 100)  # Up to 20 points
    
    price_momentum = min(25, max(0, price_change) * 2)  # Up to 25 points for positive momentum
    liquidity_score = min(15, liquidity / 1000)  # Up to 15 points for liquidity
    
    # Base activity score (higher tx count = better)
    tx_count = int(pair.get('txns', {}).get('h24', {}).get('buys', 0)) + int(pair.get('txns', {}).get('h24', {}).get('sells', 0))
    activity_score = min(10, tx_count / 10)  # Up to 10 points
    
    total_score = volume_score + vol_mcap_score + price_momentum + liquidity_score + activity_score
    return min(100, total_score)  # Cap at 100

def scan_alpha_gems():
    """Main scanning function"""
    data = get_dexscreener_trending()
    
    # Check structure and extract pairs
    pairs = []
    if isinstance(data, dict) and 'pairs' in data:
        pairs = data['pairs']
    elif isinstance(data, list):
        pairs = data
    
    print(f"Found {len(pairs)} total pairs")
    
    # Filter and score tokens
    alpha_gems = []
    for pair in pairs:
        mcap = float(pair.get('fdv', 0))
        if 30000 <= mcap <= 200000:
            score = calculate_alpha_score(pair)
            if score > 10:  # Minimum threshold
                alpha_gems.append({
                    'pair': pair,
                    'alpha_score': score
                })
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems[:15]  # Top 15

def format_report(gems):
    """Format the results into a readable report"""
    timestamp = datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""💰 DEXSCREENER ALPHA SCANNER - SUB 30K-200K MCAP
======================================================================
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000
======================================================================

"""
    
    if not gems:
        report += "❌ No alpha gems found in target range\n"
        return report
    
    report += f"💎 Found {len(gems)} Alpha Gems\n"
    report += "----------------------------------------------------------------------\n\n"
    
    for i, gem in enumerate(gems[:10], 1):  # Top 10 only
        pair = gem['pair']
        score = gem['alpha_score']
        
        base_token = pair.get('baseToken', {})
        quote_token = pair.get('quoteToken', {})
        
        symbol = base_token.get('symbol', 'Unknown')
        name = base_token.get('name', symbol)
        mcap = float(pair.get('fdv', 0))
        volume = float(pair.get('volume', {}).get('h24', 0))
        price_change = float(pair.get('priceChange', {}).get('h24', 0))
        liquidity = float(pair.get('liquidity', {}).get('usd', 0))
        
        buys = int(pair.get('txns', {}).get('h24', {}).get('buys', 0))
        sells = int(pair.get('txns', {}).get('h24', {}).get('sells', 0))
        total_tx = buys + sells
        buy_ratio = (buys / total_tx * 100) if total_tx > 0 else 0
        
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
        dex_url = pair.get('url', '#')
        chain = pair.get('chainId', 'unknown')
        
        report += f"🎯 {symbol} ({name})\n"
        report += f"   ⚡ Alpha Score: {score:.1f}/100\n"
        report += f"   💰 Market Cap: ${mcap:,.0f}\n"
        report += f"   📈 24h Volume: ${volume:,.2f}\n"
        report += f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%\n"
        report += f"   📊 Price Change: {price_change:.2f}%\n"
        report += f"   💧 Liquidity: ${liquidity:,.2f}\n"
        report += f"   🔄 Transactions: {total_tx}/24h ({buys} buys, {sells} sells)\n"
        report += f"   📈 Buy/Sell Ratio: {buy_ratio:.1f}%\n"
        report += f"   🌐 Chain: {chain}\n"
        report += f"   🔗 DexScreener: {dex_url}\n\n"
    
    # Summary statistics
    avg_score = sum(g['alpha_score'] for g in gems[:10]) / len(gems[:10]) if gems else 0
    avg_mcap = sum(float(g['pair'].get('fdv', 0)) for g in gems[:10]) / len(gems[:10]) if gems else 0
    avg_volume = sum(float(g['pair'].get('volume', {}).get('h24', 0)) for g in gems[:10]) / len(gems[:10]) if gems else 0
    
    report += f"""📊 SUMMARY STATISTICS:
------------------------------
• Average Alpha Score: {avg_score:.1f}/100
• Average Market Cap: ${avg_mcap:,.0f}
• Average Volume: ${avg_volume:,.0f}
• Total Gems Found: {len(gems)}

🧠 ALPHA SCORE EXPLANATION:
------------------------------
• Volume (30 pts): Higher = more trader interest
• Vol/MCap Ratio (20 pts): Low mcap + high volume = undervalued
• Price Momentum (25 pts): Positive momentum = upside potential
• Liquidity (15 pts): Healthy pool = easier trading
• Activity (10 pts): Higher txns = more community
• Buy Pressure (Combined): Buy ratio > 50% = accumulation

⚠️ Disclaimer: Alpha scanner results only. DYOR before investing.
Market conditions change rapidly. High risk micro-cap space.
"""
    
    return report

if __name__ == "__main__":
    print("🔍 Scanning DexScreener for alpha gems (30k-200k mcap)...")
    gems = scan_alpha_gems()
    report = format_report(gems)
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"alpha_scan_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"📄 Report saved to: {filename}")