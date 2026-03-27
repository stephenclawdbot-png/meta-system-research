#!/usr/bin/env python3
"""
Alpha Scanner - Final Cron Version
Optimized for 5-minute interval scanning of sub-200k memecoins on DexScreener
Returns plain text report designed for automatic delivery
"""

import requests
import json
from datetime import datetime
import time

def scan_dexscreener_memecoins():
    """Scan DexScreener for memecoins in 30k-200k range"""
    searches = ["meme", "dog", "cat", "pepe", "elon", "ai", "bonk", "wif", 
                "shib", "doge", "baby", "coin", "token", "kitty"]
    all_tokens = []
    
    for search in searches:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={search}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            
            if 'pairs' in data:
                for pair in data['pairs']:
                    mcap = pair.get('fdv', 0)
                    
                    # Target: sub-200k gems with activity
                    if 30000 <= mcap <= 200000:
                        vol = pair.get('volume', {}).get('h24', 0)
                        price_chg = pair.get('priceChange', {}).get('h24', 0)
                        
                        # Require minimum volume
                        if vol < 500:
                            continue
                            
                        alpha = calculate_memecoin_alpha(mcap, vol, price_chg)
                        
                        token = {
                            'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                            'mcap': mcap,
                            'volume': vol,
                            'price_chg': price_chg,
                            'chain': pair.get('chainId', ''),
                            'dex': pair.get('dexId', ''),
                            'url': pair.get('url', ''),
                            'alpha': alpha
                        }
                        
                        all_tokens.append(token)
            
            time.sleep(0.3)
            
        except Exception as e:
            continue
    
    # De-duplicate and sort
    seen = set()
    unique = []
    for t in all_tokens:
        if t['symbol'] not in seen:
            seen.add(t['symbol'])
            unique.append(t)
    
    return sorted(unique, key=lambda x: x['alpha'], reverse=True)

def calculate_memecoin_alpha(mcap, volume, price_change):
    """Calculate alpha score focusing on volume/mcap ratio"""
    try:
        # Primary signal: volume/market cap ratio (50% weight)
        ratio = (volume / mcap) * 100 if mcap > 0 else 0
        ratio_score = min(50, ratio * 2.5)
        
        # Momentum bonus for positive movement (30% weight)
        momentum_score = min(30, max(0, price_change) * 1.2)
        
        # Market cap position bonus (20% weight) - prefer smaller caps
        mcap_bonus = max(0, 20 * (1 - (mcap - 30000) / 170000))
        
        return round(ratio_score + momentum_score + mcap_bonus, 1)
    except:
        return 0

def generate_cron_summary(tokens):
    """Generate concise cron report"""
    lines = []
    
    # Header
    lines.append(f"🧠 MEMECOIN ALPHA SCANNER - {datetime.now().strftime('%m/%d %H:%M')}")
    lines.append("Target: 30k-200k gems (DexScreener)")
    lines.append("")
    
    if not tokens:
        lines.append("No significant alpha detected")
        lines.append("Market appears quiet")
        return "\n".join(lines)
    
    # Stats
    strong = [t for t in tokens if t['alpha'] >= 60]
    moderate = [t for t in tokens if 40 <= t['alpha'] < 60]
    
    lines.append(f"Found {len(tokens)} tokens | Strong: {len(strong)} | Moderate: {len(moderate)}")
    
    # Top 3-5 gems
    for i, token in enumerate(tokens[:5], 1):
        vol_ratio = (token['volume'] / token['mcap']) * 100
        
        lines.append(f"{i}. {token['symbol']}: {token['alpha']}/100")
        lines.append(f"   MCap: ${token['mcap']:,} | Vol: ${token['volume']:,}")
        lines.append(f"   Ratio: {vol_ratio:.1f}% | Chg: {token['price_chg']:.1f}%")
        lines.append(f"   Chain: {token['chain']}")
    
    # Assessment
    lines.append("")
    if strong:
        top = tokens[0]
        ratio = (top['volume'] / top['mcap']) * 100
        lines.append(f"🔥 STRONG: {top['symbol']} showing alpha potential")
        lines.append(f"   High vol/mcap ratio ({ratio:.1f}%) detected")
    elif moderate:
        lines.append("⚠️ MODERATE: Monitor volume growth")
    else:
        lines.append("🔴 LIMITED: Wait for stronger signals")
    
    lines.append("")
    lines.append("Next scan: 5 min")
    lines.append("NFA - DYOR")
    
    return "\n".join(lines)

def main():
    """Main execution - returns plain text for cron delivery"""
    tokens = scan_dexscreener_memecoins()
    report = generate_cron_summary(tokens)
    
    # Print plain text (for cron delivery)
    print(report)
    
    # Save with timestamp for logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"alpha_cron_{timestamp}.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()