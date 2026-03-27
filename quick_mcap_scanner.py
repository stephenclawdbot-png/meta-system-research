#!/usr/bin/env python3
"""
Quick MCap Scanner for Sub 30k-200k Memecoins
Direct DexScreener API scan
"""

import requests
import json
from datetime import datetime

def scan_low_mcap_tokens():
    """Scan for tokens in $30k-$200k range"""
    
    search_terms = ["meme", "dog", "cat", "pepe", "elon", "ai", "bonk", "wif", "shib", "doge", "baby", "kitty", "pup"]
    
    found_tokens = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                continue
                
            data = response.json()
            
            if 'pairs' not in data:
                continue
            
            for pair in data['pairs']:
                mcap = pair.get('fdv', 0)
                
                if 30000 <= mcap <= 200000:
                    volume_24h = pair.get('volume', {}).get('h24', 0)
                    price_change = pair.get('priceChange', {}).get('h24', 0)
                    
                    # Skip if no volume
                    if volume_24h < 100:
                        continue
                    
                    token_data = {
                        'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                        'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': volume_24h,
                        'price_change_24h': price_change,
                        'chain': pair.get('chainId', ''),
                        'dex': pair.get('dexId', ''),
                        'url': pair.get('url', ''),
                        'buy_ratio': calculate_buy_ratio(pair),
                        'age': pair.get('pairCreatedAt', 0)
                    }
                    
                    found_tokens.append(token_data)
                    
        except Exception as e:
            continue
    
    # Remove duplicates and sort by MCap
    unique_tokens = {}
    for token in found_tokens:
        key = f"{token['symbol']}-{token['chain']}"
        if key not in unique_tokens or token['volume_24h'] > unique_tokens[key]['volume_24h']:
            unique_tokens[key] = token
    
    return sorted(unique_tokens.values(), key=lambda x: x['mcap'])

def calculate_buy_ratio(pair):
    """Calculate buy/sell ratio"""
    try:
        txn_data = pair.get('txns', {}).get('h24', {})
        buys = txn_data.get('buys', 0)
        sells = txn_data.get('sells', 0)
        
        if buys + sells > 0:
            return buys / (buys + sells)
        return 0
    except:
        return 0

def generate_summary(tokens):
    """Generate plain text summary"""
    
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🧠 Alpha Scanner Report
{'=' * 40}
Scan Time: {current_time}
Focus: Sub $30k-$200k Memecoins
{'=' * 40}

"""
    
    if not tokens:
        report += "🔴 NO ALPHA SIGNALS DETECTED\n\n"
        report += "The $30k-$200k memecoin range appears quiet.\n"
        report += "Market conditions may be unfavorable for alpha detection.\n"
        return report
    
    report += f"📊 MARKET OVERVIEW\n"
    report += f"Tokens Found: {len(tokens)}\n"
    report += f"Avg MCap: ${sum(t['mcap'] for t in tokens) / len(tokens):,.0f}\n"
    report += f"Avg Volume: ${sum(t['volume_24h'] for t in tokens) / len(tokens):,.0f}\n\n"
    
    # Filter for stronger signals
    high_volume_tokens = [t for t in tokens if t['volume_24h'] > t['mcap'] * 0.05]
    positive_momentum = [t for t in tokens if t['price_change_24h'] > 0]
    
    # Top picks
    report += f"🔥 TOP ALPHA CANDIDATES\n\n"
    
    for i, token in enumerate(tokens[:10], 1):
        vol_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        buy_ratio_pct = token['buy_ratio'] * 100
        
        report += f"#{i} {token['symbol']}\n"
        report += f"   MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}\n"
        report += f"   Vol/MCap: {vol_ratio:.1f}% | Buy Ratio: {buy_ratio_pct:.0f}%\n"
        
        if token['price_change_24h'] > 0:
            report += f"   📈 24h: +{token['price_change_24h']:.1f}%\n"
        else:
            report += f"   📉 24h: {token['price_change_24h']:.1f}%\n"
            
        report += f"   Chain: {token['chain']} | Dex: {token['dex']}\n"
        report += f"\n"
    
    # Alpha assessment
    report += f"💡 ALPHA ASSESSMENT\n"
    report += f"High Volume Signals: {len(high_volume_tokens)} tokens\n"
    report += f"Positive Momentum: {len(positive_momentum)} tokens\n\n"
    
    if len(high_volume_tokens) > 0:
        report += f"📍 Best Opportunities: " + ", ".join([t['symbol'] for t in high_volume_tokens[:3]]) + "\n"
        report += "Monitored for volume continuation and momentum\n"
    else:
        report += "⚠️ Limited alpha opportunities detected\n"
        report += "Wait for stronger volume signals\n"
    
    report += "\n⚠️ DISCLAIMER: High risk, do your own research\n"
    
    return report

def main():
    print("🔄 Scanning DexScreener for sub-$200k memecoins...")
    tokens = scan_low_mcap_tokens()
    summary = generate_summary(tokens)
    print(summary)
    
    # Save timestamped copy
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"quick_scan_{timestamp}.txt", "w") as f:
        f.write(summary)
    
    print(f"📁 Saved: quick_scan_{timestamp}.txt")

if __name__ == "__main__":
    main()