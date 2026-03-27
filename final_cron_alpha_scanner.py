#!/usr/bin/env python3
"""
Final Cron Alpha Scanner - Robust DexScreener scanning for 30k-200k mcap memecoins
"""

import json
import urllib.request
from datetime import datetime
import time

def safe_fetch(url):
    """Safe API fetch with error handling"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.load(response)
    except Exception as e:
        return {'pairs': []}

def fetch_broad_data():
    """Fetch broad memecoin data from DexScreener"""
    # Broader search terms that might work
    search_terms = [
        "meme", "bonk", "solana meme", "sol meme",
        "pump", "token", "coin", "crypto"
    ]
    
    all_pairs = []
    
    for term in search_terms:
        url = f"https://api.dexscreener.com/latest/dex/search/?q={term}"
        data = safe_fetch(url)
        pairs = data.get('pairs', [])
        all_pairs.extend(pairs)
        print(f"Fetched {len(pairs)} for '{term}'")
        time.sleep(0.3)  # Rate limit
    
    # Remove duplicates
    seen_addresses = set()
    unique_pairs = []
    for pair in all_pairs:
        address = pair.get('pairAddress')
        if address and address not in seen_addresses:
            seen_addresses.add(address)
            unique_pairs.append(pair)
    
    return unique_pairs

def is_memecoin(pair):
    """Determine if a token is likely a memecoin"""
    base_token = pair.get('baseToken', {})
    name = base_token.get('name', '').lower()
    symbol = base_token.get('symbol', '').lower()
    
    # Keywords that indicate memecoin status
    meme_indicators = [
        'meme', 'bonk', 'wif', 'toshi', 'dog', 'cat', 'pepe', 'floki', 
        'shib', 'shiba', 'inu', 'dogecoin', 'doge', 'wojak', 'chad', 
        'sigma', 'granny', 'gramy', 'puppy', 'kitty', 'frog', 'monke',
        'monkey', 'elon', 'musk', 'crypto', 'token', 'coin', 'purr', 'meow'
    ]
    
    # Check name and symbol for memecoin indicators
    return any(indicator in name or indicator in symbol for indicator in meme_indicators)

def calculate_alpha_score(pair):
    """Calculate alpha score for a potential gem"""
    mcap = pair.get('marketCap', 0) or pair.get('fdv', 0)
    volume = pair.get('volume', {}).get('h24', 0)
    
    if mcap == 0 or volume == 0:
        return 0
    
    # Transaction data
    txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
    buys = txns.get('buys', 0)
    sells = txns.get('sells', 0)
    total_txns = buys + sells
    buy_ratio = buys / total_txns if total_txns > 0 else 0
    
    # Price momentum
    price_change = pair.get('priceChange', {}).get('h24', 0)
    
    # Volume to market cap ratio
    vol_mcap_ratio = (volume / mcap) * 100
    
    # Alpha score calculation (max 100)
    score = 0
    
    # Volume momentum (max 35)
    if vol_mcap_ratio >= 100:
        score += 35
    elif vol_mcap_ratio >= 50:
        score += 25
    elif vol_mcap_ratio >= 20:
        score += 15
    elif vol_mcap_ratio >= 10:
        score += 10
    elif vol_mcap_ratio >= 5:
        score += 5
    
    # Buy pressure (max 25)
    if buy_ratio >= 0.7:
        score += 25
    elif buy_ratio >= 0.6:
        score += 15
    elif buy_ratio >= 0.55:
        score += 10
    elif buy_ratio >= 0.5:
        score += 5
    
    # Absolute volume scale (max 20)
    if volume >= 50000:
        score += 20
    elif volume >= 20000:
        score += 15
    elif volume >= 10000:
        score += 10
    elif volume >= 5000:
        score += 5
    elif volume >= 1000:
        score += 3
    
    # Positive price momentum (max 15)
    if price_change > 10:
        score += 15
    elif price_change > 5:
        score += 10
    elif price_change > 0:
        score += 5
    
    # Transaction activity (max 5)
    if total_txns >= 1000:
        score += 5
    elif total_txns >= 500:
        score += 3
    elif total_txns >= 100:
        score += 2
    
    return min(100, score)

def analyze_alpha_gems():
    """Main analysis function"""
    print("Starting broad DexScreener scan...")
    pairs = fetch_broad_data()
    
    gems = []
    for pair in pairs:
        mcap = pair.get('marketCap', 0) or pair.get('fdv', 0)
        
        # Filter: 30k-200k mcap, minimum volume
        if 30000 <= mcap <= 200000:
            if pair.get('volume', {}).get('h24', 0) >= 100:
                if is_memecoin(pair):
                    alpha_score = calculate_alpha_score(pair)
                    
                    gem = {
                        'symbol': pair['baseToken']['symbol'],
                        'name': pair['baseToken']['name'],
                        'mcap': mcap,
                        'volume': pair['volume']['h24'],
                        'price_change': pair.get('priceChange', {}).get('h24', 0),
                        'chain': pair.get('chainId', 'unknown'),
                        'alpha_score': alpha_score,
                        'url': pair.get('url', '')
                    }
                    
                    if alpha_score > 0:  # Only include gems with some alpha score
                        gems.append(gem)
    
    return sorted(gems, key=lambda x: x['alpha_score'], reverse=True)

def generate_cron_report(gems):
    """Generate final report for cron delivery"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER CRON REPORT
=================================================
Scan Time: {current_time}
Target: $30K-$200K MCap Alpha Memecoins
Source: DexScreener API

"""
    
    if not gems:
        report += "❌ NO ALPHA SIGNALS DETECTED\n\n"
        report += "Market Conditions:\n"
        report += "• No high-alpha memecoins in target range\n"
        report += "• Market appears quiet or API filtering\n"
        report += "• Next scan in 6 hours\n"
        return report
    
    # Executive Summary
    total_gems = len(gems)
    avg_score = sum(g['alpha_score'] for g in gems) / total_gems
    
    report += f"🔥 ALPHA DETECTED: {total_gems} potential gems\n"
    
    if avg_score >= 60:
        report += "• STRONG ALPHA SIGNALS PRESENT\n"
    elif avg_score >= 40:
        report += "• MODERATE ALPHA POTENTIAL\n"
    else:
        report += "• WEAK ALPHA SIGNALS\n"
    
    report += f"\n🏆 TOP ALPHA GEMS:\n"
    
    for i, gem in enumerate(gems[:5], 1):
        sentiment = "🟢" if gem['price_change'] > 0 else "🔴"
        confidence = "HIGH" if gem['alpha_score'] >= 60 else "MEDIUM" if gem['alpha_score'] >= 40 else "LOW"
        
        report += f"\n{i}. {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100 ({confidence})\n"
        report += f"   📛 Name: {gem['name']}\n"
        report += f"   💰 Market Cap: ${gem['mcap']:,}\n"
        report += f"   📈 24h Volume: ${gem['volume']:,}\n"
        report += f"   {sentiment} 24h Price: {gem['price_change']:.1f}%\n"
        report += f"   🌐 Chain: {gem['chain']}\n"
        report += f"   🔗 DexScreener: {gem['url']}\n"
    
    # Market Statistics
    report += f"\n📊 MARKET OVERVIEW:\n"
    report += f"• Total Alpha Gems: {total_gems}\n"
    report += f"• Average Alpha Score: {avg_score:.1f}/100\n"
    report += f"• Average MCap: ${sum(g['mcap'] for g in gems)/total_gems:,.0f}\n"
    report += f"• Average Volume: ${sum(g['volume'] for g in gems)/total_gems:,.0f}\n"
    
    # Strategy Insights
    if gems:
        top_gem = gems[0]
        report += f"\n💡 STRATEGY INSIGHT:\n"
        if top_gem['alpha_score'] >= 70:
            report += f"• Strong alpha on {top_gem['symbol']} - monitor closely\n"
        elif top_gem['alpha_score'] >= 50:
            report += f"• Moderate alpha potential on {top_gem['symbol']}\n"
        else:
            report += "• Weak signals - trade with caution\n"
    
    report += "\n⚠️ HIGH RISK ASSET - DO YOUR OWN RESEARCH"
    return report

def main():
    print("🚀 Starting Cron Alpha Scanner...")
    gems = analyze_alpha_gems()
    
    report = generate_cron_report(gems)
    
    # Print for cron delivery (this will be captured)
    print(report)
    
    # Save report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"alpha_cron_report_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    result = main()
    # The cron system captures the output