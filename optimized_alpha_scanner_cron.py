#!/usr/bin/env python3
"""
Optimized Alpha Scanner for Cron - Enhanced sensitivity for sub 30k-200k memecoins
Focus on DexScreener real-time data with better alpha detection
"""

import requests
import json
from datetime import datetime
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_dexscreener_data():
    """Enhanced DexScreener fetch with broader search"""
    search_terms = ["meme", "dog", "cat", "pepe", "elon", "ai", "bonk", "wif", 
                   "shib", "baby", "coin", "token", "kitty", "pup"]
    all_pairs = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                all_pairs.extend(data['pairs'])
                logger.info(f"Found {len(data['pairs'])} pairs for '{term}'")
                
            time.sleep(0.3)  # Rate limiting
        except Exception as e:
            logger.warning(f"Error fetching {term}: {e}")
    
    return all_pairs

def filter_and_score_memecoins(pairs):
    """Filter memecoins with enhanced alpha scoring"""
    filtered = []
    
    for pair in pairs:
        mcap = pair.get('fdv', 0)
        
        # Target: Sub 30k-200k memecoins
        if not (30000 <= mcap <= 200000):
            continue
        
        volume_24h = pair.get('volume', {}).get('h24', 0)
        price_change = pair.get('priceChange', {}).get('h24', 0)
        
        # Minimum criteria for alpha potential
        if volume_24h < 500:  # Higher minimum for better signal
            continue
        
        # Calculate enhanced alpha score
        alpha_score = calculate_enhanced_alpha(pair)
        
        token_data = {
            'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'mcap': mcap,
            'volume_24h': volume_24h,
            'price': pair.get('priceUsd', 0),
            'price_change_24h': price_change,
            'dex': pair.get('dexId', ''),
            'chain': pair.get('chainId', ''),
            'url': pair.get('url', ''),
            'txns_24h': len(pair.get('txns', {}).get('h24', [])),
            'liquidity': pair.get('liquidity', {}).get('usd', 0),
            'alpha_score': alpha_score
        }
        
        filtered.append(token_data)
    
    # Remove duplicates by symbol
    seen = set()
    unique_tokens = []
    for token in filtered:
        if token['symbol'] not in seen:
            seen.add(token['symbol'])
            unique_tokens.append(token)
    
    return sorted(unique_tokens, key=lambda x: x['alpha_score'], reverse=True)

def calculate_enhanced_alpha(pair):
    """Enhanced alpha scoring optimized for small-cap memecoins"""
    try:
        mcap = pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        price_change = pair.get('priceChange', {}).get('h24', 0)
        txns = len(pair.get('txns', {}).get('h24', []))
        
        # Enhanced scoring components
        # 1. Volume/MCap Ratio (40% weight) - More sensitive to small movements
        vol_mcap_ratio = min(50, (volume_24h / mcap) * 100) * 0.4 if mcap > 0 else 0
        
        # 2. Price Momentum (30% weight) - Reward positive movement more aggressively
        momentum_multiplier = 2.0 if price_change > 0 else 1.0
        momentum_score = min(30, abs(price_change) * momentum_multiplier) * 0.3
        
        # 3. Transaction Activity (20% weight) - Strong indicator of community activity
        txn_score = min(20, txns / 5) * 0.2
        
        # 4. Age factor (10% weight) - Reduce score for older tokens
        # Assuming newer tokens have more alpha potential
        # Placeholder - most DexScreener data doesn't include creation time
        age_score = 10 * 0.1
        
        alpha_score = vol_mcap_ratio + momentum_score + txn_score + age_score
        
        return round(min(100, alpha_score), 1)
    except:
        return 0

def generate_cron_report(tokens):
    """Generate formatted cron report"""
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report_lines = [
        "🎯 MEMECOIN ALPHA SCANNER - CRON REPORT",
        "=" * 50,
        f"Scan Time: {current_time}",
        "Market Cap Range: $30,000 - $200,000",
        ""
    ]
    
    if not tokens:
        report_lines.extend([
            "❌ No active memecoins found in target range",
            "Market appears quiet at this time.",
            ""
        ])
    else:
        # Market stats
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_vol = sum(t['volume_24h'] for t in tokens) / len(tokens)
        avg_alpha = sum(t['alpha_score'] for t in tokens) / len(tokens)
        
        report_lines.extend([
            "📊 MARKET OVERVIEW",
            f"Total Gems Found: {len(tokens)} tokens",
            f"Average Alpha Score: {avg_alpha:.1f}/100",
            f"Average Market Cap: ${avg_mcap:,.0f}", 
            f"Average Volume: ${avg_vol:,.0f}",
            ""
        ])
        
        # Alpha rating breakdown
        strong = [t for t in tokens if t['alpha_score'] >= 60]
        moderate = [t for t in tokens if 40 <= t['alpha_score'] < 60]
        weak = [t for t in tokens if t['alpha_score'] < 40]
        
        report_lines.extend([
            "💡 ALPHA SIGNAL ANALYSIS",
            f"Strong Alpha (>60): {len(strong)} gems",
            f"Moderate Alpha (40-60): {len(moderate)} gems",
            f"Weak Alpha (<40): {len(weak)} gems",
            ""
        ])
        
        # Top candidates
        report_lines.append("🔥 TOP ALPHA CANDIDATES")
        
        for i, token in enumerate(tokens[:10], 1):
            vol_ratio = (token['volume_24h'] / token['mcap']) * 100
            report_lines.extend([
                f"#{i} {token['symbol']} - Alpha: {token['alpha_score']}/100",
                f"  📊 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}",
                f"  📈 Change: {token['price_change_24h']:.1f}% | Vol/MCap: {vol_ratio:.1f}%",
                f"  ⚡ Activity: {token['txns_24h']} txns",
                f"  🌐 Chain: {token['chain']} | Dex: {token['dex']}",
                ""
            ])
        
        # Recommendations
        report_lines.extend([
            "📋 TRADING SIGNALS",
            ""
        ])
        
        if strong:
            report_lines.append("✅ STRONG SIGNAL: Consider positions in top alpha gems")
            top_gem = tokens[0]
            report_lines.append(f"Focus on: {top_gem['symbol']} (Alpha: {top_gem['alpha_score']})")
        elif moderate:
            report_lines.append("⚠️ MODERATE SIGNAL: Monitor volume growth before entering")
        else:
            report_lines.append("🔴 LIMITED SIGNAL: Market conditions not optimal for alpha")
        
        report_lines.append("")
    
    report_lines.extend([
        "ℹ️ Next scan in 5 minutes",
        "⚠️ DISCLAIMER: High-risk speculative assets - DYOR required"
    ])
    
    return "\n".join(report_lines)

def main():
    """Run the alpha scanner cron job"""
    logger.info("Starting optimized alpha scanner cron job...")
    
    # Fetch data
    pairs = fetch_dexscreener_data()
    logger.info(f"Fetched {len(pairs)} total pairs")
    
    # Filter and score
    tokens = filter_and_score_memecoins(pairs)
    logger.info(f"Filtered to {len(tokens)} alpha candidates")
    
    # Generate report
    report = generate_cron_report(tokens)
    print(report)
    
    # Save for future analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # Save detailed data
    with open(f"alpha_scan_{timestamp}.json", 'w') as f:
        json.dump(tokens, f, indent=2)
    
    # Save cron report
    with open(f"cron_alpha_scanner_report_{timestamp}.txt", 'w') as f:
        f.write(report)
    
    logger.info("Cron job completed successfully")

if __name__ == "__main__":
    main()