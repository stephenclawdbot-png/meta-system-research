#!/usr/bin/env python3
"""
Alpha Scanner - Updated version with requests library
"""

import json
import requests
from datetime import datetime

def fetch_dexscreener_data():
    """Fetch data from DexScreener API with proper headers"""
    url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://dexscreener.com/',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
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
        
        # Filter criteria: 30k-200k mcap, min $1k volume
        if (mcap and 30000 <= mcap <= 200000 and 
            volume_24h and volume_24h >= 1000):
            
            # Get transaction data
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            # Enhanced alpha scoring
            alpha_score = 0
            
            # Volume efficiency (max 25)
            if vol_mcap_ratio >= 50:
                alpha_score += 25
            elif vol_mcap_ratio >= 30:
                alpha_score += 20
            elif vol_mcap_ratio >= 20:
                alpha_score += 15
            elif vol_mcap_ratio >= 10:
                alpha_score += 10
            elif vol_mcap_ratio >= 5:
                alpha_score += 5
            
            # Buy pressure (max 25)
            if buy_ratio >= 0.8:
                alpha_score += 25
            elif buy_ratio >= 0.7:
                alpha_score += 20
            elif buy_ratio >= 0.6:
                alpha_score += 15
            elif buy_ratio >= 0.55:
                alpha_score += 10
            elif buy_ratio >= 0.5:
                alpha_score += 5
            
            # Volume strength (max 20)
            if volume_24h >= 20000:
                alpha_score += 20
            elif volume_24h >= 10000:
                alpha_score += 15
            elif volume_24h >= 5000:
                alpha_score += 10
            elif volume_24h >= 2000:
                alpha_score += 5
            
            # Price momentum (max 15)
            if price_change >= 100:
                alpha_score += 15
            elif price_change >= 50:
                alpha_score += 10
            elif price_change >= 25:
                alpha_score += 7
            elif price_change >= 10:
                alpha_score += 3
            elif price_change > 0:
                alpha_score += 1
            
            # Transaction activity (max 15)
            if buys >= 1000:
                alpha_score += 15
            elif buys >= 500:
                alpha_score += 12
            elif buys >= 200:
                alpha_score += 8
            elif buys >= 100:
                alpha_score += 5
            elif buys >= 50:
                alpha_score += 2
            
            # Cap score adjustment (higher scores for smaller caps)
            if mcap < 50000:
                alpha_score += 5
            elif mcap < 100000:
                alpha_score += 3
            elif mcap < 150000:
                alpha_score += 1
            
            pair['alpha_score'] = min(alpha_score, 100)  # Cap at 100
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
    
    if not memecoins:
        report += "No tokens found matching criteria\n\n"
    else:
        analysis_data = {
            'total_candidates': len(memecoins),
            'avg_alpha_score': sum(c['alpha_score'] for c in memecoins) / len(memecoins),
            'avg_vol_mcap_ratio': sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins),
            'avg_buy_ratio': sum(c['buy_ratio'] for c in memecoins) / len(memecoins),
            'avg_mcap': sum(c['marketCap'] for c in memecoins) / len(memecoins)
        }
        
        for i, coin in enumerate(memecoins[:7], 1):
            symbol = coin['baseToken']['symbol']
            name = coin['baseToken']['name']
            mcap = coin['marketCap']
            volume = coin['volume']['h24']
            price_change = coin.get('priceChange', {}).get('h24', 0)
            buy_sell = coin.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            dex_url = coin.get('url', '#')
            
            # Check for boosts/labels
            boost_info = ""
            boosts = coin.get('boosts', {})
            if boosts and boosts.get('active', 0) > 0:
                boost_info = f"🚀 Boost: {boosts['active']}x"
            
            # Generate risk assessment
            risk_level = "High Risk"
            if coin['alpha_score'] >= 70:
                risk_level = "Medium-High Risk"
            if coin['alpha_score'] >= 85:
                risk_level = "Monitor Closely"
            
            report += f"""{i}. {symbol} ({name}) - Alpha Score: {coin['alpha_score']}/100
   💰 MCap: ${mcap:,}
   📈 Volume 24h: ${volume:,}
   🔥 Vol/MCap Ratio: {coin['vol_mcap_ratio']:.1f}%
   📊 Price Change: {price_change:+.1f}%
   🔄 Buy/Sell: {buy_sell.get('buys', 0)}/{buy_sell.get('sells', 0)} ({coin['buy_ratio']:.1%} buys)
   🔗 Chain: {coin.get('chainId', 'Unknown')}
   {risk_level} | DexScreener: {dex_url}
   {boost_info}

"""
        
        # Find highest momentum and volume efficiency
        best_momentum = max(memecoins, key=lambda x: x.get('priceChange', {}).get('h24', 0))
        best_volume_eff = max(memecoins, key=lambda x: x['vol_mcap_ratio'])
        highest_buys = max(memecoins, key=lambda x: x.get('txns', {}).get('h24', {}).get('buys', 0))
        
        report += f"""📊 MARKET ANALYSIS:
• Total candidates found: {analysis_data['total_candidates']} tokens meeting criteria
• Average Alpha Score: {analysis_data['avg_alpha_score']:.1f}/100
• Average Vol/MCap Ratio: {analysis_data['avg_vol_mcap_ratio']:.1f}%
• Average Buy Ratio: {analysis_data['avg_buy_ratio']:.1%}
• Average Market Cap: ${analysis_data['avg_mcap']:,.0f}
• Highest Momentum: {best_momentum['baseToken']['symbol']} (+{best_momentum.get('priceChange', {}).get('h24', 0):.1f}%)
• Most Efficient Volume: {best_volume_eff['baseToken']['symbol']} ({best_volume_eff['vol_mcap_ratio']:.1f}% vol/mcap)
• Highest Buy Pressure: {highest_buys['baseToken']['symbol']} ({highest_buys.get('txns', {}).get('h24', {}).get('buys', 0)} buys)

💡 KEY ALPHA INSIGHTS:
• Focus on tokens with high vol/mcap ratio and strong buy pressure
• Monitor volume trends for continued momentum
• Consider token age and community engagement

🚨 HIGH ALPHA ALERT:
"""
        
        # Highlight tokens with exceptional scores
        high_alpha_tokens = [coin for coin in memecoins if coin['alpha_score'] >= 70]
        if high_alpha_tokens:
            for token in high_alpha_tokens[:3]:
                report += f"• {token['baseToken']['symbol']} - Score {token['alpha_score']}/100 (High vol/mcap: {token['vol_mcap_ratio']:.1f}%, Buy ratio: {token['buy_ratio']:.1%})\n"
        else:
            report += "• No tokens currently showing exceptional alpha characteristics\n"
    
    report += """
⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE
• Always conduct your own research before investing
• Memecoins are extremely volatile
• Only risk what you can afford to lose
• Monitor volume and buy/sell ratios closely
"""
    
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
    filename = f"memecoin_alpha_scan_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved as: {filename}")

if __name__ == "__main__":
    main()