#!/usr/bin/env python3
"""
Enhanced Alpha Scanner - More comprehensive memecoin detection
"""

import requests
import json
from datetime import datetime
import traceback

def try_multiple_endpoints():
    """Try various DexScreener endpoints for better coverage"""
    endpoints = [
        # New tokens endpoint (recent launches)
        "https://api.dexscreener.com/latest/dex/tokens/new",
        # Trending tokens
        "https://api.dexscreener.com/latest/dex/tokens/trending", 
        # Chain-specific searches
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=base",
        "https://api.dexscreener.com/latest/dex/search?q=polygon",
        "https://api.dexscreener.com/latest/dex/search?q=arbitrum",
        "https://api.dexscreener.com/latest/dex/search?q=bnb",
        # Specific memecoin-related searches
        "https://api.dexscreener.com/latest/dex/search?q=memecoin",
        "https://api.dexscreener.com/latest/dex/search?q=meme",
        "https://api.dexscreener.com/latest/dex/search?q=doge",
        "https://api.dexscreener.com/latest/dex/search?q=shib"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    all_pairs = []
    seen = set()
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                if not isinstance(pairs, list):
                    print(f"⚠️ Unexpected response format from {endpoint}")
                    continue
                    
                for pair in pairs:
                    pair_id = pair.get('pairAddress')
                    if pair_id and pair_id not in seen:
                        seen.add(pair_id)
                        all_pairs.append(pair)
                
                print(f"✓ Fetched {len(pairs)} pairs from {endpoint.split('?')[0]}")
            else:
                print(f"✗ HTTP {response.status_code}: {endpoint}")
        except Exception as e:
            print(f"✗ Error with {endpoint}: {str(e)[:100]}")
    
    return all_pairs

def calculate_alpha_score(token_data):
    """Calculate comprehensive alpha score (0-100)"""
    score = 0
    
    # Market cap score (lower mcap = higher score, max 35 points)
    mcap = token_data.get('mcap', 0)
    if mcap > 0:
        if mcap < 50000: score += 35
        elif mcap < 100000: score += 30  
        elif mcap < 150000: score += 25
        elif mcap < 200000: score += 20
    
    # Volume score (higher volume = higher score, max 25 points)
    volume = token_data.get('volume', 0)
    if volume > 10000: score += 25
    elif volume > 5000: score += 20
    elif volume > 2000: score += 15
    elif volume > 1000: score += 10
    
    # Buy pressure score (max 20 points)
    buy_ratio = token_data.get('buy_ratio', 0)
    if buy_ratio > 0.7: score += 20
    elif buy_ratio > 0.6: score += 15
    elif buy_ratio > 0.5: score += 10
    elif buy_ratio > 0.4: score += 5
    
    # Transaction velocity score (max 15 points)
    total_txns = token_data.get('buys', 0) + token_data.get('sells', 0)
    if total_txns > 1000: score += 15
    elif total_txns > 500: score += 10
    elif total_txns > 100: score += 5
    
    # Volume/Mcap ratio score (high ratio = strong signal, max 5 points)
    if mcap > 100:
        vol_mcap_ratio = volume / mcap
        if vol_mcap_ratio > 0.5: score += 5
        elif vol_mcap_ratio > 0.2: score += 3
        elif vol_mcap_ratio > 0.1: score += 2
    
    return min(100, score)

def filter_memecoin_candidates(pairs):
    """Filter for potential alpha memecoins"""
    candidates = []
    
    for pair in pairs:
        try:
            # Extract market cap - try multiple fields
            mcap = pair.get('fdv', 0)
            if not mcap:
                mcap = pair.get('marketCap', 0)
            if not mcap:
                continue
                
            # Convert to float if string
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
            if volume < 500:
                continue
            
            # Extract transaction data
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Price change
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            token_data = {
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
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
            
            # Calculate alpha score
            token_data['alpha_score'] = calculate_alpha_score(token_data)
            
            # Only include tokens with basic alpha signals
            if token_data['buy_ratio'] > 0.4 and token_data['alpha_score'] > 20:
                candidates.append(token_data)
                
        except Exception as e:
            print(f"Error processing token: {e}")
            continue
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(candidates, timestamp):
    """Generate comprehensive alpha report"""
    report_lines = []
    
    report_lines.append("🎯 ENHANCED MEMECOIN ALPHA SCANNER")
    report_lines.append("=" * 50)
    report_lines.append(f"Scan Time: {timestamp}")
    report_lines.append("Market Focus: Sub $30k-$200k MCap Gems")
    report_lines.append("Alpha Detection: Pre-mainstream attention")
    report_lines.append("")
    
    if not candidates:
        report_lines.append("🔍 No alpha gems detected in target range")
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
        report_lines.append(f"Alpha Candidates Found: {total_gems} tokens")
        report_lines.append(f"Average Alpha Score: {avg_score:.1f}/100")
        report_lines.append(f"Average Market Cap: ${avg_mcap:,.0f}")
        report_lines.append(f"Average Volume: ${avg_volume:,.0f}")
        report_lines.append("")
        
        report_lines.append("💡 ALPHA SIGNALS")
        report_lines.append(f"Strong (>60): {len(strong_gems)} tokens")
        report_lines.append(f"Moderate (40-60): {len(moderate_gems)} tokens")
        report_lines.append(f"Weak (<40): {len(weak_gems)} tokens")
        report_lines.append("")
        
        # Top gems
        top_gems = candidates[:5]
        report_lines.append("🔥 TOP ALPHA GEMS")
        
        for i, gem in enumerate(top_gems, 1):
            vol_mcap_ratio = gem['volume'] / gem['mcap'] if gem['mcap'] > 0 else 0
            
            report_lines.append(f"#{i} {gem['symbol']} — Alpha: {gem['alpha_score']:.1f}/100")
            report_lines.append(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume']:,.0f}")
            report_lines.append(f"   📈 24h: ▲{gem['price_change']:.1f}%")
            report_lines.append(f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}%")
            report_lines.append(f"   🌐 Chain: {gem['chain']} | Dex: pumpswap")
            report_lines.append(f"   🔗 {gem['url']}")
            report_lines.append("")
    
    # Trading outlook
    if candidates:
        best_gem = candidates[0]
        if best_gem['alpha_score'] > 70:
            report_lines.append("📋 TRADING OUTLOOK")
            report_lines.append(f"✅ STRONG SIGNAL DETECTED: {best_gem['symbol']} showing alpha potential")
            report_lines.append("Consider strategic position entry with tight risk management")
            report_lines.append("")
    
    report_lines.append("ℹ️ Next alpha scan in 5 minutes")
    report_lines.append("⚠️ DISCLAIMER: High-risk, speculative assets - NFA")
    
    return '\n'.join(report_lines)

def main():
    print("🔍 Starting enhanced alpha scan...")
    
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (%Z)")
    
    # Fetch data
    pairs = try_multiple_endpoints()
    print(f"Total unique pairs collected: {len(pairs)}")
    
    # Filter candidates
    candidates = filter_memecoin_candidates(pairs)
    print(f"Filtered alpha candidates: {len(candidates)}")
    
    # Generate report
    report = generate_report(candidates, timestamp)
    
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save report
    output_file = f"cron_alpha_scanner_report_20260304.txt"
    with open(output_file, "w") as f:
        f.write(report)
    
    print(f"\n📄 Report saved to {output_file}")
    
    return report

if __name__ == "__main__":
    try:
        result = main()
    except Exception as e:
        print(f"❌ Scan failed: {e}")
        traceback.print_exc()