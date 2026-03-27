#!/usr/bin/env python3
"""
Final Alpha Scan - Focused analysis
"""

import json
import subprocess
from datetime import datetime

def fetch_top_memecoins():
    """Fetch top trending memecoins"""
    keywords = ['wif', 'bonk', 'pepe', 'bome', 'dog', 'cat', 'fart', 'rock', 'motor', 'game']
    all_pairs = []
    
    for keyword in keywords:
        try:
            result = subprocess.run(
                [f'curl', '-s', f'https://api.dexscreener.com/latest/dex/search/?q={keyword}&limit=30'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                pairs = data.get('pairs', [])
                all_pairs.extend(pairs)
                print(f"Found {len(pairs)} pairs for '{keyword}'")
        except Exception as e:
            print(f"Error fetching '{keyword}': {e}")
    
    # Remove duplicates
    unique_pairs = {}
    for pair in all_pairs:
        address = pair.get('pairAddress')
        if address:
            unique_pairs[address] = pair
    
    return list(unique_pairs.values())

def advanced_filtering(pairs):
    """Advanced filtering with multiple criteria"""
    memecoins = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        
        # Expanded criteria: 20k-250k mcap, min $100 volume
        if (mcap and 20000 <= mcap <= 250000 and 
            volume_24h and volume_24h >= 100):
            
            # Transaction data
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            # Enhanced alpha scoring
            alpha_score = 0
            
            # Volume Efficiency (max 40)
            if vol_mcap_ratio >= 100:
                alpha_score += 40
            elif vol_mcap_ratio >= 50:
                alpha_score += 30
            elif vol_mcap_ratio >= 30:
                alpha_score += 20
            elif vol_mcap_ratio >= 15:
                alpha_score += 10
            elif vol_mcap_ratio >= 5:
                alpha_score += 5
            
            # Buy Pressure (max 25)
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
            
            # Price Momentum (max 15)
            if price_change >= 500:
                alpha_score += 15
            elif price_change >= 200:
                alpha_score += 12
            elif price_change >= 100:
                alpha_score += 9
            elif price_change >= 50:
                alpha_score += 6
            elif price_change >= 25:
                alpha_score += 3
            elif price_change > 0:
                alpha_score += 1
            
            # Liquidity Quality (max 10)
            if liquidity >= 10000:
                alpha_score += 10
            elif liquidity >= 5000:
                alpha_score += 8
            elif liquidity >= 2000:
                alpha_score += 6
            elif liquidity >= 1000:
                alpha_score += 4
            elif liquidity >= 500:
                alpha_score += 2
            
            # Transaction Velocity (max 10)
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

def generate_final_report(memecoins):
    """Generate detailed alpha report"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER - FINAL REPORT
===================================================
Scan Time: {current_time}
Market Focus: Sub 30k-200k MCap Gems (Expanded to 20k-250k)
Scan Scope: Top 10 trending memecoin categories

🔥 ALPHA GEMS DISCOVERED
--------------------------
"""
    
    if not memecoins:
        report += "No premium alpha detected in current market\n"
    else:
        # Categorize by quality
        premium_alpha = [c for c in memecoins if c['alpha_score'] >= 75]
        strong_alpha = [c for c in memecoins if 50 <= c['alpha_score'] < 75]
        moderate_alpha = [c for c in memecoins if 30 <= c['alpha_score'] < 50]
        
        if premium_alpha:
            report += "💎💎 PREMIUM ALPHA (Score ≥75) 💎💎\n"
            for i, coin in enumerate(premium_alpha, 1):
                symbol = coin['baseToken']['symbol']
                name = coin['baseToken']['name']
                mcap = coin['marketCap']
                volume = coin['volume']['h24']
                price_change = coin.get('priceChange', {}).get('h24', 0)
                buy_sell = coin.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
                dex_url = coin.get('url', '#')
                chain = coin.get('chainId', 'Unknown')
                liquidity = coin.get('liquidity', {}).get('usd', 0)
                
                report += f"""{i}. {symbol} ({name})
   ⭐ Alpha Score: {coin['alpha_score']}/100
   💰 MCap: ${mcap:,}
   📈 Volume 24h: ${volume:,}
   🔥 Vol/MCap: {coin['vol_mcap_ratio']:.1f}%
   📊 Price Chg: {price_change:+.1f}%
   🔄 Buy/Sell: {buy_sell.get('buys', 0)}/{buy_sell.get('sells', 0)} ({coin['buy_ratio']:.1%})
   💧 Liquidity: ${liquidity:,}
   🔗 Chain: {chain}
   📱 DexScreener: {dex_url}

"""
        
        if strong_alpha:
            report += "✨ STRONG ALPHA (Score 50-74) ✨\n"
            for coin in strong_alpha:
                symbol = coin['baseToken']['symbol']
                mcap = coin['marketCap']
                vol_ratio = coin['vol_mcap_ratio']
                price_change = coin.get('priceChange', {}).get('h24', 0)
                report += f"• {symbol} (Score: {coin['alpha_score']}, MCap: ${mcap:,}, Vol/MCap: {vol_ratio:.1f}%, Price: {price_change:+.1f}%)\n"
            report += "\n"
        
        if moderate_alpha:
            report += "🔍 MODERATE POTENTIAL (Score 30-49)\n"
            for coin in moderate_alpha[:3]:
                symbol = coin['baseToken']['symbol']
                report += f"• {symbol} (Score: {coin['alpha_score']}, Vol/MCap: {coin['vol_mcap_ratio']:.1f}%, Buy: {coin['buy_ratio']:.1%})\n"
            if len(moderate_alpha) > 3:
                report += f"• ...and {len(moderate_alpha)-3} more\n"
            report += "\n"
        
        # Market insights
        report += "📊 MARKET INSIGHTS:\n"
        totals = {
            'total': len(memecoins),
            'premium': len(premium_alpha),
            'strong': len(strong_alpha),
            'moderate': len(moderate_alpha)
        }
        
        report += f"• Total qualifying tokens: {totals['total']}\n"
        report += f"• Premium alpha gems: {totals['premium']}\n"
        report += f"• Strong candidates: {totals['strong']}\n"
        report += f"• Moderate potential: {totals['moderate']}\n"
        
        avg_score = sum(c['alpha_score'] for c in memecoins) / len(memecoins)
        avg_mcap = sum(c['marketCap'] for c in memecoins) / len(memecoins)
        
        report += f"• Average Alpha Score: {avg_score:.1f}/100\n"
        report += f"• Average Market Cap: ${avg_mcap:,.0f}\n"
        
        # Top performers
        if memecoins:
            top_vol = max(memecoins, key=lambda x: x['vol_mcap_ratio'])
            top_momentum = max(memecoins, key=lambda x: x.get('priceChange', {}).get('h24', 0))
            top_buys = max(memecoins, key=lambda x: x.get('txns', {}).get('h24', {}).get('buys', 0))
            
            report += f"• Highest Volume Efficiency: {top_vol['baseToken']['symbol']} ({top_vol['vol_mcap_ratio']:.1f}%)\n"
            report += f"• Strongest Momentum: {top_momentum['baseToken']['symbol']} (+{top_momentum.get('priceChange', {}).get('h24', 0):.1f}%)\n"
            report += f"• Most Buy Activity: {top_buys['baseToken']['symbol']} ({top_buys.get('txns', {}).get('h24', {}).get('buys', 0)} buys)\n"
    
    report += """
⚠️ ALERT: HIGHEST PRIORITY RECOMMENDATIONS
• Focus on tokens with Vol/MCap ratio > 50% and positive momentum
• Monitor buy ratio for sustained accumulation
• Verify liquidity before entering positions

� DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE
• Memecoin investments carry extreme volatility
• Only use capital you can afford to lose completely
• Always DYOR (Do Your Own Research)
• Diversify across multiple opportunities

🎯 NEXT CRON SCAN: 9:07 PM Manila Time"""
    
    return report

def main():
    print("🔍 Running final alpha scan for high-potential memecoins...")
    
    pairs = fetch_top_memecoins()
    print(f"Total unique pairs collected: {len(pairs)}")
    
    memecoins = advanced_filtering(pairs)
    print(f"Final filtered candidates: {len(memecoins)}")
    
    report = generate_final_report(memecoins)
    print(report)
    
    # Save for cron delivery
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"final_alpha_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved as: {filename}")
    
    return report

if __name__ == "__main__":
    main()