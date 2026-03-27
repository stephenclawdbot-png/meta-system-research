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
    # Use broader search terms to avoid ratelimiting
    urls = [
        "https://api.dexscreener.com/latest/dex/search/?q=solana",
        "https://api.dexscreener.com/latest/dex/search/?q=bonk",
        "https://api.dexscreener.com/latest/dex/search/?q=dog",
        "https://api.dexscreener.com/latest/dex/search/?q=cat"
    ]
    
    all_pairs = []
    
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                data = json.load(response)
                pairs = data.get('pairs', [])
                all_pairs.extend(pairs)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    # Remove duplicates based on pair address
    seen_addresses = set()
    unique_pairs = []
    for pair in all_pairs:
        if pair.get('pairAddress') not in seen_addresses:
            seen_addresses.add(pair.get('pairAddress'))
            unique_pairs.append(pair)
    
    return unique_pairs

def filter_memecoins(pairs):
    """Filter for memecoins in 30k-200k mcap range"""
    memecoins = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter criteria - target 30k-200k mcap
        if (mcap and 30000 <= mcap <= 200000 and 
            volume_24h and volume_24h >= 1000):
            
            # Calculate alpha score
            buy_sell = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = buy_sell.get('buys', 0)
            sells = buy_sell.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
            
            # Alpha scoring formula
            alpha_score = 0
            
            # Volume momentum (higher volume relative to mcap = better)
            if vol_mcap_ratio >= 50:
                alpha_score += 30
            elif vol_mcap_ratio >= 20:
                alpha_score += 20
            elif vol_mcap_ratio >= 10:
                alpha_score += 10
            
            # Buy pressure
            if buy_ratio >= 0.7:
                alpha_score += 25
            elif buy_ratio >= 0.6:
                alpha_score += 15
            elif buy_ratio >= 0.55:
                alpha_score += 10
            
            # Volume absolute threshold
            if volume_24h >= 10000:
                alpha_score += 15
            elif volume_24h >= 5000:
                alpha_score += 10
            
            # Transaction activity
            if buys >= 200:
                alpha_score += 10
            elif buys >= 100:
                alpha_score += 5
            
            pair['alpha_score'] = alpha_score
            pair['buy_ratio'] = buy_ratio
            pair['vol_mcap_ratio'] = vol_mcap_ratio
            memecoins.append(pair)
    
    return sorted(memecoins, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(memecoins):
    """Generate formatted report"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER CRON REPORT
===================================================
Scan Time: {current_time}
Market Cap Target: $30,000 - $200,000
Scanner: DexScreener API (Solana ecosystem)

🔥 EXECUTIVE SUMMARY:
"""
    
    analysis_data = {
        'total_candidates': len(memecoins),
        'avg_alpha_score': 0,
        'avg_vol_mcap_ratio': 0,
        'avg_buy_ratio': 0,
        'avg_mcap': 0,
        'top_score': 0
    }
    
    if memecoins:
        analysis_data['avg_alpha_score'] = sum(c['alpha_score'] for c in memecoins) / len(memecoins)
        analysis_data['avg_vol_mcap_ratio'] = sum(c['vol_mcap_ratio'] for c in memecoins) / len(memecoins)
        analysis_data['avg_buy_ratio'] = sum(c['buy_ratio'] for c in memecoins) / len(memecoins)
        analysis_data['avg_mcap'] = sum(c['marketCap'] for c in memecoins) / len(memecoins)
        analysis_data['top_score'] = memecoins[0]['alpha_score'] if memecoins else 0
        
        if analysis_data['total_candidates']:
            report += f"• Found {analysis_data['total_candidates']} alpha gems within target range\n"
            if analysis_data['top_score'] >= 60:
                report += "• Strong alpha detected with high-confidence candidates\n"
            elif analysis_data['top_score'] >= 40:
                report += "• Moderate alpha signals detected\n"
            else:
                report += "• Weak alpha signals - market cooling\n"
    else:
        report += "• No alpha gems detected in target range\n"
    
    report += "\n🏆 TOP ALPHA GEMS DISCOVERED:\n"
    
    for i, coin in enumerate(memecoins[:8], 1):
        symbol = coin['baseToken']['symbol']
        name = coin['baseToken']['name'][:30] + "..." if len(coin['baseToken']['name']) > 30 else coin['baseToken']['name']
        mcap = coin['marketCap']
        volume = coin['volume']['h24']
        price_change = coin.get('priceChange', {}).get('h24', 0)
        buy_sell = coin.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
        chain = coin.get('chainId', 'SOLANA')
        
        # Determine confidence level
        if coin['alpha_score'] >= 60:
            confidence = "CRYSTAL CLEAR ALPHA"
        elif coin['alpha_score'] >= 40:
            confidence = "SOLID ALPHA"
        elif coin['alpha_score'] >= 20:
            confidence = "MEDIUM ALPHA"
        else:
            confidence = "LOW ALPHA"
        
        report += f"\n{i}. {symbol} - {confidence} - Score: {coin['alpha_score']:.1f}/80\n"
        report += f"   • Buy Pressure: {coin['buy_ratio']:.1%} buys ({buy_sell.get('buys', 0)}/{buy_sell.get('sells', 0)})\n"
        report += f"   • Price Change: {price_change:+.1f}%\n"
        report += f"   • Volume: ${volume:,} 24h\n"
        report += f"   • Vol/MCap Ratio: {coin['vol_mcap_ratio']:.1f}%\n"
        report += f"   • MCap: ${mcap:,}\n"
        report += f"   • Chain: {chain.upper()}\n"
        report += f"   • Link: {coin.get('url', 'N/A')}\n"
    
    report += f"\n📊 MARKET DYNAMICS:\n"
    report += f"• Total Alpha Candidates: {analysis_data['total_candidates']}\n"
    report += f"• Avg Market Cap: ${analysis_data['avg_mcap']:,.0f}\n"
    report += f"• Avg Buy Ratio: {analysis_data['avg_buy_ratio']:.1%}\n"
    report += f"• Avg Vol/MCap Ratio: {analysis_data['avg_vol_mcap_ratio']:.1f}%\n"
    
    report += "\n💡 KEY INSIGHTS:\n"
    if memecoins:
        strongest_coin = memecoins[0]
        if strongest_coin['buy_ratio'] >= 0.7:
            report += "• High buy pressure indicates accumulation phase\n"
        if strongest_coin['vol_mcap_ratio'] >= 50:
            report += "• Extreme volume efficiency suggests momentum\n"
        report += "• Solana ecosystem continues to dominate memecoin space\n"
    else:
        report += "• Market appears quiet - wait for better opportunities\n"
    
    report += "\n⚠️ RISK ASSESSMENT:\n"
    if memecoins:
        if analysis_data['top_score'] >= 60:
            report += "• HIGH RISK/HIGH REWARD: Strong alpha signals detected\n"
        elif analysis_data['top_score'] >= 40:
            report += "• MEDIUM RISK: Moderate alpha potential\n"
        else:
            report += "• HIGH RISK: Weak momentum requires caution\n"
    else:
        report += "• LOW RISK: No actionable signals present\n"
    
    report += "\n🧠 ALPHA STRATEGY:\n"
    if memecoins:
        if len(memecoins) >= 3:
            report += "• Monitor top 3 candidates closely for momentum shifts\n"
        report += "• Track volume acceleration for breakout confirmation\n"
        report += "• Exercise extreme caution - high volatility expected\n"
    else:
        report += "• Wait for better market conditions\n"
    
    report += "\nEND OF REPORT\n🔍 Scanned: DexScreener Multi-Term Search"
    
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
    filename = f"cron_memecoin_alpha_report_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    # Update current report
    with open("cron_memecoin_alpha_report_current.txt", "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved as: {filename}")
    print("📋 Current report updated: cron_memecoin_alpha_report_current.txt")

if __name__ == "__main__":
    main()