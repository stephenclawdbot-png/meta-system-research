#!/usr/bin/env python3
"""
Cron Memecoin Alpha Scanner - Final Version
Auto-detects sub-200k memecoins with alpha potential via DexScreener
Built for continuous 5-minute interval scanning
"""

import requests
import json
from datetime import datetime
import time

def scan_memecoin_alpha():
    """Core alpha scanning function for cron execution"""
    
    # Broad search terms for comprehensive coverage
    search_terms = ["meme", "coin", "token", "dog", "cat", "pepe", "elon", "ai", 
                   "bonk", "wif", "shib", "doge", "baby", "kitty", "pup"]
    
    all_tokens = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                continue
                
            data = response.json()
            
            if not data or 'pairs' not in data:
                continue
            
            for pair in data['pairs']:
                mcap = pair.get('fdv', 0)
                
                # Focus on sub-200k gems with actual activity
                if not (30000 <= mcap <= 200000):
                    continue
                
                volume_24h = pair.get('volume', {}).get('h24', 0)
                price_change = pair.get('priceChange', {}).get('h24', 0)
                
                # Minimum volume threshold for signal
                if volume_24h < 500:
                    continue
                
                # Enhanced alpha scoring
                token_data = {
                    'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                    'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price_change_24h': price_change,
                    'chain': pair.get('chainId', ''),
                    'dex': pair.get('dexId', ''),
                    'url': pair.get('url', ''),
                    'txns_24h': len(pair.get('txns', {}).get('h24', [])),
                    'alpha_score': calculate_alpha_score(mcap, volume_24h, price_change)
                }
                
                all_tokens.append(token_data)
                
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"⚠️ Error scanning {term}: {e}")
            continue
    
    # Remove duplicates and sort by alpha
    unique_tokens = []
    seen_symbols = set()
    
    for token in all_tokens:
        if token['symbol'] not in seen_symbols:
            seen_symbols.add(token['symbol'])
            unique_tokens.append(token)
    
    return sorted(unique_tokens, key=lambda x: x['alpha_score'], reverse=True)

def calculate_alpha_score(mcap, volume, price_change):
    """Optimized alpha scoring for sub-200k memecoins"""
    try:
        # Volume/MCap ratio (primary signal)
        vol_mcap_ratio = (volume / mcap) * 100 if mcap > 0 else 0
        vol_score = min(40, vol_mcap_ratio * 2)  # More sensitive scoring
        
        # Price momentum (reward positive movement)
        momentum_score = min(30, max(0, price_change) * 1.5)
        
        # Market cap position (smaller = more alpha potential)
        mcap_score = max(0, 30 * (1 - (mcap - 30000) / 170000))
        
        alpha_score = vol_score + momentum_score + mcap_score
        
        return round(min(100, alpha_score), 1)
    except:
        return 0

def generate_alpha_report(tokens):
    """Generate formatted report for cron delivery"""
    
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER - CRON EXECUTION
{'=' * 50}
Scan Time: {current_time}
Market Focus: $30k-$200k memecoins
Alpha Detection: Pre-mainstream attention

"""
    
    if not tokens:
        report += "🔴 CURRENT MARKET STATUS\n"
        report += "No active alpha signals detected in target range.\n"
        report += "The sub-$200k memecoin market appears quiet.\n\n"
        report += "💡 SUGGESTION: Check again during peak trading hours\n\n"
    else:
        # Market statistics
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_volume = sum(t['volume_24h'] for t in tokens) / len(tokens)
        avg_alpha = sum(t['alpha_score'] for t in tokens) / len(tokens)
        
        report += f"📊 MARKET OVERVIEW\n"
        report += f"Alpha Candidates Found: {len(tokens)} tokens\n"
        report += f"Average Alpha Score: {avg_alpha:.1f}/100\n"
        report += f"Average Market Cap: ${avg_mcap:,.0f}\n"
        report += f"Average Volume: ${avg_volume:,.0f}\n\n"
        
        # Alpha signal breakdown
        strong_alpha = [t for t in tokens if t['alpha_score'] >= 60]
        moderate_alpha = [t for t in tokens if 40 <= t['alpha_score'] < 60]
        weak_alpha = [t for t in tokens if t['alpha_score'] < 40]
        
        report += f"💡 ALPHA SIGNALS\n"
        report += f"Strong (>60): {len(strong_alpha)} tokens\n"
        report += f"Moderate (40-60): {len(moderate_alpha)} tokens\n"
        report += f"Weak (<40): {len(weak_alpha)} tokens\n\n"
        
        # Top 5 alpha gems
        report += "🔥 TOP ALPHA GEMS\n"
        
        for i, token in enumerate(tokens[:5], 1):
            report += f"#{i} {token['symbol']} — Alpha: {token['alpha_score']}/100\n"
            report += f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}\n"
            if token['price_change_24h'] > 0:
                report += f"   📈 24h: ▲{token['price_change_24h']:.1f}%\n"
            else:
                report += f"   📉 24h: ▼{abs(token['price_change_24h']):.1f}%\n"
            vol_ratio = (token['volume_24h'] / token['mcap']) * 100
            report += f"   🔥 Vol/MCap: {vol_ratio:.1f}%\n"
            report += f"   🌐 Chain: {token['chain']} | Dex: {token['dex']}\n"
            report += f"   🔗 {token['url']}\n"
            report += "\n"
        
        # Trading recommendations
        report += "📋 TRADING OUTLOOK\n"
        if strong_alpha:
            top_gem = tokens[0]
            report += f"✅ STRONG SIGNAL DETECTED: {top_gem['symbol']} showing alpha potential\n"
            report += "Consider strategic position entry with tight risk management\n"
        elif moderate_alpha:
            report += "⚠️ MODERATE SIGNAL: Monitor volume growth before position entry\n"
            report += "Focus on tokens with increasing transaction activity\n"
        else:
            report += "🔴 LIMITED OPPORTUNITY: Market conditions suboptimal\n"
            report += "Wait for stronger volume signals or positive momentum\n"
        
        report += "\n"
    
    report += "ℹ️ Next alpha scan in 5 minutes\n"
    report += "⚠️ DISCLAIMER: High-risk, speculative assets - NFA\n"
    
    return report

def main():
    """Main execution - designed for cron automation"""
    print("🧠 Starting Cron Memecoin Alpha Scanner...\n")
    
    # Run alpha scan
    tokens = scan_memecoin_alpha()
    
    # Generate report
    report = generate_alpha_report(tokens)
    
    # Output for cron delivery
    print(report)
    
    # Save timestamped report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    with open(f"cron_alpha_scan_{timestamp}.txt", "w") as f:
        f.write(report)
    
    # Log summary
    print(f"\n📁 Report saved: cron_alpha_scan_{timestamp}.txt")
    print(f"🔍 Scanned {len(tokens)} alpha candidates")
    print("✅ Cron execution complete")

if __name__ == "__main__":
    main()