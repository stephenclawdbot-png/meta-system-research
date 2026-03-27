#!/usr/bin/env python3
"""Quick DexScreener Alpha Scanner - March 3rd"""

import requests
import json
from datetime import datetime
from urllib.request import Request

def fetch_dexscreener_data():
    """Fetch data from DexScreener with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        # Try trending endpoint first
        req = Request('https://api.dexscreener.com/latest/dex/tokens/trending', headers=headers)
        response = requests.get('https://api.dexscreener.com/latest/dex/tokens/trending', headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'pairs' in data:
                return data['pairs']
    except Exception as e:
        print(f"Trending API error: {e}")
    
    try:
        # Fallback to search endpoints
        chains = ['solana', 'base', 'arbitrum', 'polygon', 'ethereum']
        pairs = []
        
        for chain in chains:
            try:
                response = requests.get(f'https://api.dexscreener.com/latest/dex/search?q={chain}', headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'pairs' in data:
                        pairs.extend(data['pairs'][:30])  # Limit to first 30
            except Exception as e:
                print(f"Search API error for {chain}: {e}")
        
        return pairs
    except Exception as e:
        print(f"Fallback error: {e}")
        return []

def generate_report():
    """Generate the alpha scanner report"""
    print("🔍 Scanning DexScreener for memecoin gems...")
    
    pairs = fetch_dexscreener_data()
    if not pairs:
        return "❌ API unavailable - cannot fetch DexScreener data at this time"
    
    print(f"Retrieved {len(pairs)} total pairs")
    
    # Filter for 30k-200k mcap memecoins
    filtered = []
    for pair in pairs:
        mcap = pair.get('fdv', 0)
        volume = pair.get('volume', {}).get('h24', 0)
        
        if mcap and 30000 <= mcap <= 200000 and volume >= 1000:
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Calculate alpha score
            alpha_score = 0
            if buy_ratio > 0.5: alpha_score += 30
            if volume > 5000: alpha_score += 25
            if mcap < 100000: alpha_score += 20
            if buy_ratio > 0.6: alpha_score += 15
            if volume > 10000: alpha_score += 10
            
            filtered.append({
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume': volume,
                'price_change': pair.get('priceChange', {}).get('h24', 0),
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'alpha_score': alpha_score,
                'chain': pair.get('chainId', 'Unknown'),
                'pair_address': pair.get('pairAddress', 'Unknown'),
                'url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}"
            })
    
    filtered.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    if not filtered:
        report = f"""🚨 MEMECOIN ALPHA SCANNER - MARKET QUIET
==================================================
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000

🔍 No memecoin gems detected in target range.
Market appears quiet at this time - check back later.

Next scan at 8:23 AM."""
    else:
        report = f"""🎯 MEMECOIN ALPHA SCANNER - LIVE UPDATE
==================================================
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000
Focus: Early alpha detection before mainstream

🔥 TOP {min(len(filtered), 6)} ALPHA GEMS (30k-200k MCap)
"""
        
        for i, gem in enumerate(filtered[:6], 1):
            report += f"""
🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100
   📈 24h Stats: ${gem['volume']:,.2f} vol • ${gem['mcap']:,.0f} mcap
   📊 Buy Ratio: {gem['buy_ratio']:.1%} • Price Change: {gem['price_change']:.1f}%
   🔄 Activity: {gem['buys']} buys / {gem['sells']} sells
   🌐 Chain: {gem['chain']}
   🔗 {gem['url']}
"""
        
        if len(filtered) > 6:
            report += f"\n📊 Total Candidates Found: {len(filtered)}"
        
        avg_score = sum(g['alpha_score'] for g in filtered) / len(filtered)
        avg_mcap = sum(g['mcap'] for g in filtered) / len(filtered)
        
        report += f"""

💡 ALPHA SIGNALS:
• Buy ratio >50% = accumulation phase
• Volume/MCap ratio >25% = strong interest
• Multiple chains increase discovery chances

⚠️ HIGH RISK ASSETS - DYOR REQUIRED
Next scan in 5 minutes."""
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(report)