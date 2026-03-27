#!/usr/bin/env python3
"""
Quick Alpha Scanner for Cron - Scan DexScreener for 30k-200k mcap memecoins
"""

import json
import urllib.request
from datetime import datetime
import time

def fetch_memecoins():
    """Fetch memecoins from DexScreener with targeted searches"""
    # Memecoin related search terms
    search_terms = ["bonk", "spx", "wif", "toshi", "popcat", "myro", "dog", "cat", "bonk2"]
    
    all_pairs = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={term}"
            with urllib.request.urlopen(url) as response:
                data = json.load(response)
                pairs = data.get('pairs', [])
                all_pairs.extend(pairs)
                print(f"✅ Found {len(pairs)} pairs for '{term}'")
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"❌ Error fetching '{term}': {e}")
    
    # Remove duplicates based on pair address
    seen_addresses = set()
    unique_pairs = []
    for pair in all_pairs:
        address = pair.get('pairAddress')
        if address and address not in seen_addresses:
            seen_addresses.add(address)
            unique_pairs.append(pair)
    
    return unique_pairs

def filter_alpha_candidates(pairs):
    """Filter for 30k-200k mcap memecoins"""
    candidates = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0) or pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter criteria
        if 30000 <= mcap <= 200000 and volume_24h >= 100:
            token_name = pair.get('baseToken', {}).get('name', '').lower()
            token_symbol = pair.get('baseToken', {}).get('symbol', '').lower()
            
            # Basic memecoin filter (non-professional sounding names)
            is_memecoin_related = (
                any(word in token_name or word in token_symbol 
                    for word in ['dog', 'cat', 'bonk', 'wif', 'toshi', 'popcat', 
                               'pepe', 'floki', 'shib', 'elon', 'meme', 'shiba',
                               'inu', 'kitty', 'puppy', 'chad', 'sigma', 'alpha',
                               'granny', 'gramy', 'doge', 'wojak'])
            ) or (
                len(token_name) <= 20 and 
                sum(c.isalpha() for c in token_name) >= 4
            )
            
            if is_memecoin_related:
                # Calculate alpha metrics
                txns_24h = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
                buys = txns_24h.get('buys', 0)
                sells = txns_24h.get('sells', 0)
                total_txns = buys + sells
                buy_ratio = buys / total_txns if total_txns > 0 else 0
                
                price_change = pair.get('priceChange', {}).get('h24', 0)
                vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
                
                # Alpha score calculation
                score = min(100, (
                    min(30, vol_mcap_ratio * 0.5) +           # Volume momentum (up to 30)
                    min(25, buy_ratio * 25) +                 # Buy pressure (up to 25)
                    min(20, volume_24h / 1000) +              # Volume scale (up to 20)
                    min(15, total_txns / 10) +                 # Transaction activity (up to 15)
                    min(10, max(0, price_change) * 0.5)       # Positive momentum (up to 10)
                ))
                
                candidate = {
                    'symbol': pair['baseToken']['symbol'],
                    'name': pair['baseToken']['name'],
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price_change': price_change,
                    'buy_ratio': buy_ratio,
                    'total_txns': total_txns,
                    'buys': buys,
                    'sells': sells,
                    'vol_mcap_ratio': vol_mcap_ratio,
                    'alpha_score': score,
                    'url': pair.get('url', ''),
                    'chain': pair.get('chainId', 'unknown')
                }
                candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_summary_report(candidates):
    """Generate concise summary report for cron delivery"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🚀 MEMECOIN ALPHA SCANNER CRON REPORT
=================================================
Scan Time: {current_time}
Target: $30K-$200K MCap Alpha Memecoins

"""
    
    if not candidates:
        report += "❌ NO ALPHA DETECTED\n\nMarket Summary:\n"
        report += "• No memecoins found in target range\n"
        report += "• API filtering or market quiet\n"
        report += "• Next scan scheduled in 6 hours\n"
        return report
    
    # Executive summary
    total_candidates = len(candidates)
    avg_score = sum(c['alpha_score'] for c in candidates) / total_candidates
    avg_vol_mcap = sum(c['vol_mcap_ratio'] for c in candidates) / total_candidates
    avg_buy_ratio = sum(c['buy_ratio'] for c in candidates) / total_candidates
    
    report += f"🔥 ALPHA DETECTED: {total_candidates} gems\n"
    
    if avg_score >= 60:
        report += "• STRONG ALPHA SIGNALS PRESENT\n"
    elif avg_score >= 40:
        report += "• MODERATE ALPHA POTENTIAL\n"
    else:
        report += "• WEAK ALPHA SIGNALS\n"
    
    report += f"\n🏆 TOP 3 ALPHA GEMS:\n"
    
    for i, gem in enumerate(candidates[:3], 1):
        sentiment = "🟢" if gem['price_change'] > 0 else "🔴"
        confidence = "HIGH" if gem['alpha_score'] >= 60 else "MEDIUM" if gem['alpha_score'] >= 40 else "LOW"
        
        report += f"\n{i}. {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100 ({confidence})\n"
        report += f"   📊 Name: {gem['name']}\n"
        report += f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}\n"
        report += f"   {sentiment} 24h: {gem['price_change'] or 0:.1f}%\n"
        report += f"   📈 Vol/MCap: {gem['vol_mcap_ratio']:.1f}%\n"
        report += f"   🤝 Buy Ratio: {gem['buy_ratio']*100:.1f}% ({gem['buys']}/{gem['sells']})\n"
        report += f"   🔄 Transactions: {gem['total_txns']}\n"
        report += f"   🌐 DexScreener: {gem['url']}\n"
    
    # Market overview
    report += f"\n📊 MARKET OVERVIEW:\n"
    report += f"• Total Alpha Candidates: {total_candidates}\n"
    report += f"• Avg Alpha Score: {avg_score:.1f}/100\n"
    report += f"• Avg Vol/MCap Ratio: {avg_vol_mcap:.1f}%\n"
    report += f"• Avg Buy Pressure: {avg_buy_ratio*100:.1f}%\n"
    
    # Strategy guidance
    top_gem = candidates[0] if candidates else None
    if top_gem:
        report += f"\n💡 STRATEGY INSIGHT:\n"
        if top_gem['alpha_score'] >= 70:
            report += "• Strong alpha detected - monitor closely\n"
        elif top_gem['alpha_score'] >= 50:
            report += f"• Monitor {top_gem['symbol']} for momentum shifts\n"
        else:
            report += "• Weak signals - proceed with caution\n"
    
    report += "\n⚠️ HIGH RISK - RESEARCH BEFORE TRADING"
    return report

def main():
    print("🔍 Starting memecoin alpha scan...")
    
    pairs = fetch_memecoins()
    print(f"Total unique pairs fetched: {len(pairs)}")
    
    candidates = filter_alpha_candidates(pairs)
    print(f"Alpha candidates found: {len(candidates)}")
    
    report = generate_summary_report(candidates)
    print("\n" + report)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"cron_alpha_report_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved: {filename}")
    
    # For cron delivery - just print the report
    return report

if __name__ == "__main__":
    result = main()
    # Print final result for cron delivery
    print(result)