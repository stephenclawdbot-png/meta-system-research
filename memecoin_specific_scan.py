#!/usr/bin/env python3
"""
Memecoin-Specific Alpha Scanner - Focus on actual memecoins excluding large caps
"""

import requests
import json
from datetime import datetime

def enhance_endpoints():
    """More targeted endpoints for memecoins"""
    endpoints = [
        # Chain-specific with memecoin-like patterns
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=base",
        "https://api.dexscreener.com/latest/dex/search?q=polygon", 
        "https://api.dexscreener.com/latest/dex/search?q=arbitrum",
        "https://api.dexscreener.com/latest/dex/search?q=bnb",
        
        # Memecoin-specific searches
        "https://api.dexscreener.com/latest/dex/search?q=meme",
        "https://api.dexscreener.com/latest/dex/search?q=dog",
        "https://api.dexscreener.com/latest/dex/search?q=cat",
        "https://api.dexscreener.com/latest/dex/search?q=pepe",
        "https://api.dexscreener.com/latest/dex/search?q=shib",
        "https://api.dexscreener.com/latest/dex/search?q=floki",
        "https://api.dexscreener.com/latest/dex/search?q=elon",
        "https://api.dexscreener.com/latest/dex/search?q=bonk",
        
        # Popular memecoin patterns
        "https://api.dexscreener.com/latest/dex/search?q=token",
        "https://api.dexscreener.com/latest/dex/search?q=coin",
        "https://api.dexscreener.com/latest/dex/search?q=kitty",
        "https://api.dexscreener.com/latest/dex/search?q=wif",
        "https://api.dexscreener.com/latest/dex/search?q=pump",
        "https://api.dexscreener.com/latest/dex/search?q=moon"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    all_pairs = []
    seen = set()
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                if not isinstance(pairs, list):
                    continue
                
                for pair in pairs:
                    pair_id = pair.get('pairAddress')
                    if pair_id and pair_id not in seen:
                        seen.add(pair_id)
                        all_pairs.append(pair)
                
                print(f"✓ Fetched {len(pairs)} pairs from {endpoint.split('?q=')[1][:20]}")
        except Exception as e:
            print(f"✗ Error with {endpoint}: {str(e)[:80]}")
    
    return all_pairs

def is_memecoin(symbol, name):
    """Identify if token is likely a memecoin"""
    symbol_lower = str(symbol).lower()
    name_lower = str(name).lower()
    
    # List of major coins to exclude
    excluded_tokens = ['bnb', 'sol', 'eth', 'btc', 'matic', 'avax', 'ada', 'dot', 
                      'ltc', 'xrp', 'doge', 'shib', 'usdc', 'usdt', 'dai']
    
    # If it's a major token, exclude
    if symbol_lower in excluded_tokens:
        return False
    
    # Memecoin indicators
    memecoin_keywords = [
        'meme', 'doge', 'shib', 'pepe', 'floki', 'elon', 'bonk', 'wif',
        'cat', 'dog', 'kitty', 'puppy', 'moon', 'pump', 'rocket',
        'based', 'degens', 'alpha', 'omega', 'sigma', 'chad'
    ]
    
    # Check if contains memecoin keywords
    for keyword in memecoin_keywords:
        if keyword in symbol_lower or keyword in name_lower:
            return True
    
    # Check for animal/nature themes (common memecoin patterns)
    animal_keywords = ['cat', 'dog', 'frog', 'bee', 'bird', 'fish', 'bear', 'bull',
                      'whale', 'shark', 'ape', 'monkey', 'panda', 'tiger', 'lion']
    
    for keyword in animal_keywords:
        if keyword in symbol_lower or keyword in name_lower:
            return True
    
    # Check for absurd/silly names (typical memecoins)
    if len(symbol_lower) <= 6 and not symbol_lower.isalpha():
        return True
    
    return False

def enhanced_memecoin_filter(pairs):
    """Filter specifically for memecoins"""
    candidates = []
    
    for pair in pairs:
        try:
            # Extract basic info
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            
            # Skip if not a memecoin
            if not is_memecoin(symbol, name):
                continue
            
            # Extract market cap
            mcap = pair.get('fdv', 0)
            if not mcap:
                mcap = pair.get('marketCap', 0)
            if not mcap:
                continue
            
            if isinstance(mcap, str):
                mcap = float(mcap.replace(',', ''))
            
            # Filter by market cap range
            if mcap < 30000 or mcap > 200000:
                continue
            
            # Extract volume
            volume_data = pair.get('volume', {})
            volume = volume_data.get('h24', 0)
            if isinstance(volume, str):
                volume = float(volume.replace(',', ''))
            
            # Minimum volume filter
            if volume < 100:
                continue
            
            # Transaction data
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            token_data = {
                'symbol': symbol,
                'name': name,
                'mcap': mcap,
                'volume': volume,
                'price_change': price_change,
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'chain': pair.get('chainId', 'Unknown'),
                'pair_address': pair.get('pairAddress', ''),
                'url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                'created_at': pair.get('pairCreatedAt', '')
            }
            
            # Calculate alpha score specifically for memecoins
            score = 0
            
            # Volume score (max 35)
            if volume > 10000: score += 35
            elif volume > 5000: score += 30
            elif volume > 2000: score += 25
            elif volume > 500: score += 15
            elif volume > 100: score += 10
            
            # Buy ratio score (max 30)
            if buy_ratio > 0.6: score += 30
            elif buy_ratio > 0.55: score += 25
            elif buy_ratio > 0.5: score += 20
            elif buy_ratio > 0.45: score += 15
            elif buy_ratio > 0.4: score += 10
            
            # Market cap position (lower is better for memecoins, max 20)
            if mcap < 50000: score += 20
            elif mcap < 100000: score += 15
            elif mcap < 150000: score += 10
            elif mcap < 200000: score += 5
            
            # Transaction activity (max 10)
            if total_txns > 200: score += 10
            elif total_txns > 100: score += 8
            elif total_txns > 50: score += 5
            elif total_txns > 20: score += 3
            
            # Price momentum (max 5)
            if price_change > 10: score += 5
            elif price_change > 5: score += 3
            elif price_change > 0: score += 1
            
            token_data['alpha_score'] = min(100, score)
            
            # Only include tokens with decent alpha signals
            if token_data['alpha_score'] > 20 and token_data['buy_ratio'] > 0.4:
                candidates.append(token_data)
                
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_memecoin_report(candidates, timestamp):
    """Generate memecoin-specific report"""
    report_lines = []
    
    report_lines.append("🚀 MEMECOIN ALPHA SCANNER")
    report_lines.append("=" * 50)
    report_lines.append(f"Scan Time: {timestamp}")
    report_lines.append("Market Focus: $30k-$200k MCap MEMECOINS")
    report_lines.append("Alpha Detection: Pre-mainstream attention")
    report_lines.append("")
    
    if not candidates:
        report_lines.append("🔍 No promising memecoins detected in target range")
        report_lines.append("Market may be quiet or API limitations encountered")
    else:
        # Market overview
        total_gems = len(candidates)
        avg_score = sum(c['alpha_score'] for c in candidates) / total_gems
        avg_mcap = sum(c['mcap'] for c in candidates) / total_gems
        avg_volume = sum(c['volume'] for c in candidates) / total_gems
        
        strong_gems = [c for c in candidates if c['alpha_score'] >= 60]
        moderate_gems = [c for c in candidates if 40 <= c['alpha_score'] < 60]
        weak_gems = [c for c in candidates if c['alpha_score'] < 40]
        
        report_lines.append("📊 MARKET OVERVIEW")
        report_lines.append(f"Memecoin Candidates: {total_gems} tokens")
        report_lines.append(f"Average Alpha Score: {avg_score:.1f}/100")
        report_lines.append(f"Average MCap: ${avg_mcap:,.0f}")
        report_lines.append(f"Average Volume: ${avg_volume:,.0f}")
        report_lines.append("")
        
        report_lines.append("💡 ALPHA POTENTIAL")
        report_lines.append(f"Strong (>60): {len(strong_gems)} tokens")
        report_lines.append(f"Moderate (40-60): {len(moderate_gems)} tokens")
        report_lines.append(f"Weak (<40): {len(weak_gems)} tokens")
        report_lines.append("")
        
        # Top memecoins
        top_gems = candidates[:5]
        report_lines.append("💎 TOP MEMECOIN GEMS")
        
        for i, gem in enumerate(top_gems, 1):
            vol_mcap_ratio = gem['volume'] / gem['mcap'] * 100 if gem['mcap'] > 0 else 0
            
            report_lines.append(f"#{i} {gem['symbol']} — Alpha: {gem['alpha_score']:.1f}/100")
            report_lines.append(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume']:,.0f}")
            report_lines.append(f"   📈 24h: ▲{gem['price_change']:.1f}%")
            report_lines.append(f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}%")
            report_lines.append(f"   💸 Buy Ratio: {gem['buy_ratio']:.1%}")
            report_lines.append(f"   🌐 Chain: {gem['chain']}")
            report_lines.append(f"   🔗 {gem['url']}")
            report_lines.append("")
    
    # Trading outlook
    if candidates:
        best_gem = candidates[0]
        report_lines.append("📋 TRADING OUTLOOK")
        if best_gem['alpha_score'] > 70:
            report_lines.append(f"🎯 STRONG ALPHA: {best_gem['symbol']} showing memecoin potential")
            report_lines.append("Consider small position with strict risk management")
        elif best_gem['alpha_score'] > 50:
            report_lines.append(f"📊 MODERATE SIGNAL: {best_gem['symbol']} worth monitoring")
            report_lines.append("Watch for further momentum before entering")
        else:
            report_lines.append("⚠️ Limited alpha signals detected")
            report_lines.append("Focus on risk management and wait for stronger setups")
        report_lines.append("")
    
    report_lines.append("ℹ️ Next scan in 5 minutes")
    report_lines.append("💎 Focus on actual memecoins, excluding large caps")
    report_lines.append("⚠️ HIGH RISK - Memecoins are volatile - NFA")
    
    return '\n'.join(report_lines)

def main():
    print("🚀 Starting memecoin-specific alpha scan...")
    
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (%Z)")
    
    # Fetch data
    pairs = enhance_endpoints()
    print(f"Total pairs collected: {len(pairs)}")
    
    # Filter for memecoins
    candidates = enhanced_memecoin_filter(pairs)
    print(f"Memecoin candidates found: {len(candidates)}")
    
    # Generate report
    report = generate_memecoin_report(candidates, timestamp)
    
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save cron report
    output_file = f"cron_memecoin_alpha_report_20260304.txt"
    with open(output_file, "w") as f:
        f.write(report)
    
    print(f"\n📄 Memecoin report saved to {output_file}")
    
    return report

if __name__ == "__main__":
    result = main()