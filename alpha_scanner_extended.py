#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

def fetch_extended_data():
    """Fetch broader set of tokens from DexScreener"""
    search_terms = [
        "sol", "dog", "cat", "ape", "elon", "pepe", "bonk", "floki", "shib", 
        "squid", "moon", "mars", "ai", "game", "protocol", "finance", "defi",
        "meme", "degenerate", "wagmi", "gm", "gn", "nouns", "frog", "whale"
    ]
    
    all_pairs = []
    
    for term in search_terms:
        try:
            cmd = f"curl -s \"https://api.dexscreener.com/latest/dex/search?q={term}\""
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('pairs'):
                    all_pairs.extend(data['pairs'])
                    print(f"Found {len(data['pairs'])} pairs for '{term}'")
        except Exception as e:
            print(f"Error fetching '{term}': {e}")
    
    return all_pairs

def analyze_extended_candidates(pairs):
    """Analyze with broader criteria"""
    candidates = []
    seen_tokens = set()
    
    for pair in pairs:
        try:
            mcap = pair.get('fdv', 0)
            
            # Extended mcap range
            if 10000 <= mcap <= 300000:
                base_token = pair.get('baseToken', {})
                token_address = base_token.get('address')
                
                # Skip duplicates
                if token_address in seen_tokens:
                    continue
                seen_tokens.add(token_address)
                
                symbol = base_token.get('symbol', 'UNKNOWN')
                quote_token = pair.get('quoteToken', {})
                
                # Accept USDC, USDT, USD, or USDe pairs
                if quote_token.get('symbol') not in ['USDC', 'USDT', 'USDe', 'USD', 'USDC.e']:
                    continue
                
                volume_24h = pair.get('volume', {}).get('h24', 0)
                liquidity = pair.get('liquidity', {}).get('usd', 0)
                price_change_24h = pair.get('priceChange', {}).get('h24', 0)
                
                # Skip if volume too low
                if volume_24h < 100:
                    continue
                
                # Calculate enhanced alpha score (0-100)
                alpha_score = 0
                
                # Volume contribution (max 25)
                if volume_24h > 50000:
                    alpha_score += 25
                elif volume_24h > 20000:
                    alpha_score += 20
                elif volume_24h > 10000:
                    alpha_score += 15
                elif volume_24h > 5000:
                    alpha_score += 10
                elif volume_24h > 1000:
                    alpha_score += 5
                
                # Liquidity contribution (max 20)
                if liquidity > 10000:
                    alpha_score += 20
                elif liquidity > 5000:
                    alpha_score += 15
                elif liquidity > 2000:
                    alpha_score += 10
                elif liquidity > 500:
                    alpha_score += 5
                
                # Price momentum (max 20)
                if price_change_24h > 20:
                    alpha_score += 20
                elif price_change_24h > 10:
                    alpha_score += 15
                elif price_change_24h > 5:
                    alpha_score += 10
                elif price_change_24h > 0:
                    alpha_score += 5
                
                # Transaction ratio (max 25)
                txns_24h = pair.get('txns', {}).get('h24', {})
                buys = txns_24h.get('buys', 0)
                sells = txns_24h.get('sells', 0)
                total_txns = buys + sells
                
                if total_txns > 0:
                    buy_ratio = buys / total_txns
                    if buy_ratio > 0.7:
                        alpha_score += 25
                    elif buy_ratio > 0.6:
                        alpha_score += 20
                    elif buy_ratio > 0.55:
                        alpha_score += 15
                    elif buy_ratio > 0.5:
                        alpha_score += 10
                
                # Age/freshness proxy (max 10)
                info = pair.get('info', {})
                socials = info.get('socials', [])
                websites = info.get('websites', [])
                
                if socials or websites:
                    alpha_score += 10
                
                candidates.append({
                    'symbol': symbol,
                    'name': base_token.get('name', 'Unknown'),
                    'address': token_address,
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'liquidity': liquidity,
                    'price_change_24h': price_change_24h,
                    'alpha_score': alpha_score,
                    'transaction_info': f"{buys}/{sells}",
                    'buy_ratio': buy_ratio if total_txns > 0 else 0,
                    'socials': len(socials),
                    'websites': len(websites),
                    'dex_url': pair.get('url'),
                    'pair_address': pair.get('pairAddress')
                })
                
        except Exception as e:
            continue
    
    return candidates

def generate_extended_report(alpha_gems, timestamp):
    """Generate comprehensive report"""
    # Filter for best candidates
    high_alpha = [gem for gem in alpha_gems if gem['alpha_score'] >= 30]
    
    report = f"""🔥 EXTENDED ALPHA SCANNER REPORT
======================================
Scan Time: {timestamp}
Market Cap Range: $10,000 - $300,000 (Extended)
Total Tokens Analyzed: {len(alpha_gems)}
High Alpha Candidates (Score >= 30): {len(high_alpha)}

TOP ALPHA PICKS:
"""
    
    if high_alpha:
        for gem in high_alpha[:8]:  # Show top 8
            report += f"""
🎯 {gem['symbol']} - Score: {gem['alpha_score']}/100
   MCap: ${gem['mcap']:,.0f} | Vol 24h: ${gem['volume_24h']:,.0f}
   Δ Price: {gem['price_change_24h']:.1f}% | Liq: ${gem['liquidity']:,.0f}
   Buy Ratio: {gem['buy_ratio']:.0%} | Socials: {gem['socials']}
   Dex: {gem['dex_url']}
"""
    else:
        report += "\n⚠️ No high-alpha gems found. Market may be quiet or consolidating.\n"
    
    # Show some mid-range candidates if no high-alpha
    if len(high_alpha) < 3:
        mid_alpha = [gem for gem in alpha_gems if gem['alpha_score'] >= 20]
        if mid_alpha:
            report += "\n📊 MID-RANGE WATCHLIST (Score 20-29):\n"
            for gem in mid_alpha[:3]:
                report += f"""   {gem['symbol']} - Score: {gem['alpha_score']} | MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}\n"""
    
    report += """

🔧 SCANNER CONFIGURATION:
- Extended MCap Range: $10k - $300k
- Minimum Volume: $100
- Alpha Score Threshold: 30+/100 (High Alpha)
- Buy/Sell Ratio Optimized
- Comprehensive Token Discovery
"""
    
    return report

if __name__ == "__main__":
    print("🔍 Extended Alpha Scanner - Broad Token Discovery...")
    
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)")
    
    pairs = fetch_extended_data()
    print(f"Total pairs collected: {len(pairs)}")
    
    alpha_gems = analyze_extended_candidates(pairs)
    print(f"Alpha candidates analyzed: {len(alpha_gems)}")
    
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report = generate_extended_report(alpha_gems, timestamp)
    print(report)