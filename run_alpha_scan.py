#!/usr/bin/env python3
"""
Alpha Scanner - Query DexScreener for memecoins in 30k-200k mcap range
"""

import json
import urllib.request
from datetime import datetime
import time

def fetch_dexscreener_data():
    """Fetch data from DexScreener API"""
    url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        return data.get('pairs', [])
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def filter_memecoins(pairs):
    """Filter for memecoins in 30k-200k mcap range"""
    memecoins = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter criteria
        if (mcap and 30000 <= mcap <= 200000 and 
            volume_24h and volume_24h >= 1000):
            
            # Calculate alpha score (simplified version)
            buy_sell = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = buy_sell.get('buys', 0)
            sells = buy_sell.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
            
            # Simple alpha scoring
            alpha_score = 0
            if buy_ratio >= 0.55:
                alpha_score += 30
            if vol_mcap_ratio >= 20:
                alpha_score += 25
            if volume_24h >= 10000:
                alpha_score += 20
            if buys >= 100:
                alpha_score += 15
            if vol_mcap_ratio >= 50:
                alpha_score += 10
            
            pair['alpha_score'] = alpha_score
            pair['buy_ratio'] = buy_ratio
            pair['vol_mcap_ratio'] = vol_mcap_ratio
            memecoins.append(pair)
    
    return sorted(memecoins, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(memecoins):
    """Generate formatted report"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER REPORT
==================================================
Scanning DexScreener for sub 30k-200k MCap gems
Scan Time: {current_time}
Market Cap Range: $30,000 - $200,000

🔥 TOP ALPHA GEMS DETECTED
------------------------------
"""
    
    analysis_data = {
        'total_candidates': len(memecoins),
        'avg_alpha_score': 0,
        'avg_vol_mcap_ratio': 0,
        'avg_buy_ratio': 0,
        'avg_mcap': 0
    }
    
    if memecoins:
        analysis_data['avg_alpha_score'] = sum(c['alpha_score'] for c in memecoins) / len(memecoins)
        analysis_data['avg_vol_mcap_ratio'] = sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins)
        analysis_data['avg_buy_ratio'] = sum(c['buy_ratio'] for c in memecoins) / len(memecoins)
        analysis_data['avg_mcap'] = sum(c['marketCap'] for c in memecoins) / len(memecoins)
    
    for i, coin in enumerate(memecoins[:5], 1):
        symbol = coin['baseToken']['symbol']
        name = coin['baseToken']['name']
        mcap = coin['marketCap']
        volume = coin['volume']['h24']
        price_change = coin.get('priceChange', {}).get('h24', 0)
        buy_sell = coin.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
        
        report += f"""{i}. {symbol} ({name}) - Alpha Score: {coin['alpha_score']}/80
   💰 MCap: ${mcap:,}
   📈 Volume 24h: ${volume:,}
   🔥 Vol/MCap Ratio: {coin['vol_mcap_ratio']:.1f}%
   📊 Price Change: {price_change:.1f}%
   🔄 Buy/Sell: {buy_sell.get('buys', 0)}/{buy_sell.get('sells', 0)} ({coin['buy_ratio']:.1%} buys)
   🔗 Chain: Solana

"""
    
    report += f"""📊 MARKET ANALYSIS:
• Total candidates found: {analysis_data['total_candidates']} tokens meeting criteria
• Average Alpha Score: {analysis_data['avg_alpha_score']:.1f}/80
• Average Vol/MCap Ratio: {analysis_data['avg_vol_mcap_ratio']:.1f}%
• Average Buy Ratio: {analysis_data['avg_buy_ratio']:.1%}
• Average Market Cap: ${analysis_data['avg_mcap']:,.0f}

💡 KEY ALPHA INSIGHTS:
• Potential alpha gems identified based on volume efficiency and buy pressure
• Higher alpha scores indicate stronger momentum and volume activity

⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE
• Always conduct your own research before investing
• Memecoins are extremely volatile
• Only risk what you can afford to lose
• Monitor volume and buy/sell ratios closely"""
    
    return report

def main():
    print("🔍 Scanning DexScreener for 30k-200k mcap memecoins...")
    
    pairs = fetch_dexscreener_data()
    print(f"Total pairs fetched: {len(pairs)}")
    
    memecoins = filter_memecoins(pairs)
    print(f"Filtered memecoins: {len(memecoins)}")
    
    report = generate_report(memecoins)
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"alpha_scan_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved as: {filename}")

if __name__ == "__main__":
    main()