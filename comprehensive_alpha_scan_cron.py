#!/usr/bin/env python3
"""
Comprehensive Alpha Scanner - Multiple keyword search
"""

import json
import subprocess
from datetime import datetime

def fetch_memecoins(keywords, limit=50):
    """Fetch memecoins using multiple keyword searches"""
    all_pairs = []
    
    for keyword in keywords:
        try:
            result = subprocess.run(
                [f'curl', '-s', f'https://api.dexscreener.com/latest/dex/search/?q={keyword}&limit={limit}'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                pairs = data.get('pairs', [])
                all_pairs.extend(pairs)
                print(f"Found {len(pairs)} pairs for '{keyword}'")
            else:
                print(f"Error fetching '{keyword}': {result.stderr}")
        except Exception as e:
            print(f"Error processing '{keyword}': {e}")
    
    # Remove duplicates based on pair address
    unique_pairs = {}
    for pair in all_pairs:
        address = pair.get('pairAddress')
        if address:
            unique_pairs[address] = pair
    
    return list(unique_pairs.values())

def filter_memecoins(pairs):
    """Filter for memecoins in 30k-200k mcap range with alpha characteristics"""
    memecoins = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter criteria: 30k-200k mcap, min $500 volume
        if (mcap and 30000 <= mcap <= 200000 and 
            volume_24h and volume_24h >= 500):
            
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
            
            # Volume efficiency (max 35)
            if vol_mcap_ratio >= 100:
                alpha_score += 35
            elif vol_mcap_ratio >= 50:
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
            if buy_ratio >= 0.9:
                alpha_score += 25
            elif buy_ratio >= 0.8:
                alpha_score += 20
            elif buy_ratio >= 0.7:
                alpha_score += 15
            elif buy_ratio >= 0.6:
                alpha_score += 10
            elif buy_ratio >= 0.55:
                alpha_score += 8
            elif buy_ratio >= 0.5:
                alpha_score += 5
            
            # Volume strength (max 15)
            if volume_24h >= 20000:
                alpha_score += 15
            elif volume_24h >= 10000:
                alpha_score += 12
            elif volume_24h >= 5000:
                alpha_score += 9
            elif volume_24h >= 2000:
                alpha_score += 6
            elif volume_24h >= 1000:
                alpha_score += 3
            
            # Price momentum (max 15)
            if price_change >= 200:
                alpha_score += 15
            elif price_change >= 100:
                alpha_score += 12
            elif price_change >= 50:
                alpha_score += 8
            elif price_change >= 25:
                alpha_score += 5
            elif price_change >= 10:
                alpha_score += 3
            elif price_change > 0:
                alpha_score += 1
            
            # Transaction activity (max 10)
            if buys >= 1000:
                alpha_score += 10
            elif buys >= 500:
                alpha_score += 8
            elif buys >= 200:
                alpha_score += 6
            elif buys >= 100:
                alpha_score += 4
            elif buys >= 50:
                alpha_score += 2
            
            pair['alpha_score'] = min(alpha_score, 100)
            pair['buy_ratio'] = buy_ratio
            pair['vol_mcap_ratio'] = vol_mcap_ratio
            memecoins.append(pair)
    
    return sorted(memecoins, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(memecoins):
    """Generate comprehensive report"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 COMPREHENSIVE MEMECOIN ALPHA SCANNER REPORT
========================================================
Scanning multiple keywords for sub 30k-200k MCap gems
Scan Time: {current_time}
Market Cap Range: $30,000 - $200,000
Filter Criteria: Minimum $500 volume, positive buy pressure

🔥 TOP ALPHA GEMS DETECTED
------------------------------
"""
    
    if not memecoins:
        report += """No tokens found matching criteria ☹️
- Try expanding search criteria
- Current memecoin market may be quiet
- Check back in 1-2 hours
"""
    else:
        # Filter for high quality tokens (score >= 40)
        high_quality = [c for c in memecoins if c['alpha_score'] >= 40]
        moderate_quality = [c for c in memecoins if 20 <= c['alpha_score'] < 40]
        
        if high_quality:
            report += "💎 HIGH QUALITY ALPHA (Score ≥40)\n"
            for i, coin in enumerate(high_quality[:8], 1):
                symbol = coin['baseToken']['symbol']
                name = coin['baseToken']['name']
                mcap = coin['marketCap']
                volume = coin['volume']['h24']
                price_change = coin.get('priceChange', {}).get('h24', 0)
                buy_sell = coin.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
                dex_url = coin.get('url', '#')
                chain = coin.get('chainId', 'Unknown')
                liquidity = coin.get('liquidity', {}).get('usd', 0)
                
                report += f"""{i}. {symbol} ({name}) - Alpha Score: {coin['alpha_score']}/100
   💰 MCap: ${mcap:,}
   📈 Volume 24h: ${volume:,}
   🔥 Vol/MCap Ratio: {coin['vol_mcap_ratio']:.1f}%
   📊 Price Change: {price_change:+.1f}%
   🔄 Buy/Sell: {buy_sell.get('buys', 0)}/{buy_sell.get('sells', 0)} ({coin['buy_ratio']:.1%} buys)
   💧 Liquidity: ${liquidity:,}
   🔗 Chain: {chain}
   DexScreener: {dex_url}

"""
        
        if moderate_quality:
            report += "🔍 MODERATE POTENTIAL (Score 20-39)\n"
            for coin in moderate_quality[:5]:
                symbol = coin['baseToken']['symbol']
                vol_ratio = coin['vol_mcap_ratio']
                buy_ratio = coin['buy_ratio']
                price_change = coin.get('priceChange', {}).get('h24', 0)
                report += f"• {symbol} (Score: {coin['alpha_score']}, Vol/MCap: {vol_ratio:.1f}%, Buy: {buy_ratio:.1%}, Price: {price_change:+.1f}%)\n"
            report += "\n"
        
        # Market analysis
        analysis_data = {
            'total_candidates': len(memecoins),
            'high_quality': len(high_quality),
            'avg_alpha_score': sum(c['alpha_score'] for c in memecoins) / len(memecoins),
            'avg_vol_mcap_ratio': sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins),
            'avg_buy_ratio': sum(c['buy_ratio'] for c in memecoins) / len(memecoins),
            'avg_mcap': sum(c['marketCap'] for c in memecoins) / len(memecoins)
        }
        
        report += f"""📊 MARKET ANALYSIS:
• Total candidates: {analysis_data['total_candidates']} tokens
• High quality (≥40): {analysis_data['high_quality']} tokens
• Average Alpha Score: {analysis_data['avg_alpha_score']:.1f}/100
• Average Vol/MCap Ratio: {analysis_data['avg_vol_mcap_ratio']:.1f}%
• Average Buy Ratio: {analysis_data['avg_buy_ratio']:.1%}
• Average Market Cap: ${analysis_data['avg_mcap']:,.0f}
"""
        
        # Find exceptional characteristics
        if memecoins:
            best_momentum = max(memecoins, key=lambda x: x.get('priceChange', {}).get('h24', 0))
            best_volume_eff = max(memecoins, key=lambda x: x['vol_mcap_ratio'])
            highest_buys = max(memecoins, key=lambda x: x.get('txns', {}).get('h24', {}).get('buys', 0))
            
            report += f"""• Highest Momentum: {best_momentum['baseToken']['symbol']} (+{best_momentum.get('priceChange', {}).get('h24', 0):.1f}%)
• Most Efficient Volume: {best_volume_eff['baseToken']['symbol']} ({best_volume_eff['vol_mcap_ratio']:.1f}% vol/mcap)
• Highest Buy Pressure: {highest_buys['baseToken']['symbol']} ({highest_buys.get('txns', {}).get('h24', {}).get('buys', 0)} buys)
"""
    
    report += """
⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE
• Always conduct your own research before investing
• Memecoins are extremely volatile
• Only risk what you can afford to lose
• Monitor volume and buy/sell ratios closely

📈 NEXT SCAN: Scheduled for next hour"""
    
    return report

def main():
    # Popular memecoin keywords to search
    keywords = ['solana', 'bonk', 'pepe', 'dog', 'cat', 'meme', 'bonk', 'wif', 'bome', 'wif']
    
    print(f"🔍 Scanning DexScreener for {len(keywords)} keywords...")
    
    pairs = fetch_memecoins(keywords, limit=50)
    print(f"Total unique pairs found: {len(pairs)}")
    
    memecoins = filter_memecoins(pairs)
    print(f"Filtered memecoins meeting criteria: {len(memecoins)}")
    
    report = generate_report(memecoins)
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"alpha_scan_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved as: {filename}")
    
    return report

if __name__ == "__main__":
    main()