#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def scan_dexscreener():
    """Scan DexScreener for trending tokens in 30k-200k range"""
    
    endpoints = [
        "https://api.dexscreener.com/latest/dex/search?q=solana&limit=100",
        "https://api.dexscreener.com/latest/dex/search?q=meme&limit=100", 
        "https://api.dexscreener.com/latest/dex/search?q=coin&limit=100",
        "https://api.dexscreener.com/latest/dex/search?q=token&limit=100",
        "https://api.dexscreener.com/latest/dex/search?q=defi&limit=100"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; AlphaScanner/1.0)',
        'Accept': 'application/json'
    }
    
    found_tokens = {}
    
    for endpoint in endpoints:
        try:
            print(f"🔍 Scanning {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'pairs' in data and data['pairs']:
                    for pair in data['pairs']:
                        try:
                            # Get market cap (try multiple fields)
                            mcap = pair.get('marketCap', pair.get('fdv', 0))
                            
                            # Filter by our range
                            if 30000 <= mcap <= 200000:
                                # Get volume
                                volume = pair.get('volume', {}).get('h24', 0)
                                
                                # Only consider tokens with reasonable activity
                                if volume > 100:
                                    symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                                    
                                    # Skip duplicates
                                    if symbol not in found_tokens:
                                        found_tokens[symbol] = {
                                            'symbol': symbol,
                                            'name': pair.get('baseToken', {}).get('name', ''),
                                            'mcap': mcap,
                                            'volume': volume,
                                            'price_change': pair.get('priceChange', {}).get('h24', 0),
                                            'liquidity': pair.get('liquidity', {}).get('usd', 0),
                                            'chain': pair.get('chainId', ''),
                                            'txns': pair.get('txns', {}).get('h24', {}),
                                            'age': pair.get('pairCreatedAt', None),
                                            'url': pair.get('url', '')
                                        }
                        except Exception as e:
                            continue
                else:
                    print(f"⚠️ No pairs found in {endpoint}")
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error {e}")
    
    return list(found_tokens.values())

def calculate_alpha_score(token):
    """Calculate alpha score (0-100)"""
    score = 0
    
    # Volume/MCap ratio (max 40 pts)
    vol_mcap_ratio = token['volume'] / token['mcap'] * 100 if token['mcap'] > 0 else 0
    score += min(40, vol_mcap_ratio * 2)
    
    # Price momentum (max 25 pts)
    price_change = token.get('price_change', 0)
    if price_change > 0:
        score += min(25, price_change * 0.5)
    
    # Transaction activity (max 20 pts)
    txns = token.get('txns', {})
    total_txns = txns.get('buys', 0) + txns.get('sells', 0)
    if total_txns > 100:
        score += min(20, total_txns * 0.1)
    
    # Liquidity (max 15 pts)
    liquidity = token.get('liquidity', 0)
    if liquidity > 10000:
        score += min(15, liquidity / 1000)
    
    return min(100, score)

def generate_report(tokens):
    """Generate final report"""
    timestamp = datetime.now().strftime("%A, March 6, 2026 — %I:%M %p (Asia/Manila)")
    
    report = []
    report.append("🚀 MEMECOIN ALPHA SCANNER CRON REPORT")
    report.append("=" * 50)
    report.append(f"Scan Time: {timestamp}")
    report.append("Market Cap Target: $30,000 - $200,000")
    report.append("Scanner: DexScreener API (multiple endpoints)")
    report.append("")
    
    if not tokens:
        report.append("❌ No alpha gems found in target range")
        report.append("🔍 Markets may be quiet or API limitations")
        return "\n".join(report)
    
    # Calculate scores
    scored_tokens = []
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
        scored_tokens.append(token)
    
    # Sort by alpha score
    scored_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Filter tokens with minimum score
    top_tokens = [t for t in scored_tokens if t['alpha_score'] >= 20]
    
    report.append(f"🔥 ALPHA GEMS DISCOVERED ({len(top_tokens)} total):")
    report.append("-" * 30)
    
    for i, token in enumerate(top_tokens[:10], 1):
        txns = token.get('txns', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        
        report.append(f"")
        report.append(f"{i}. 🚀 **{token['symbol']}** - Alpha: {token['alpha_score']:.1f}/100")
        report.append(f"   💰 Market Cap: ${token['mcap']:,.0f}")
        report.append(f"   📊 Volume 24h: ${token['volume']:,.0f}")
        report.append(f"   📈 Price Change: {token['price_change']:+.1f}%" )
        report.append(f"   🔄 Vol/MCap Ratio: {token['volume']/token['mcap']*100:.1f}%")
        report.append(f"   🤝 Transactions: {total_txns} ({buy_ratio:.1f}% buys)")
        report.append(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
        report.append(f"   🔗 Chain: {token['chain']}")
        
        if token.get('url'):
            report.append(f"   🔗 DexScreener: {token['url']}")
    
    # Market summary
    if top_tokens:
        avg_mcap = sum(t['mcap'] for t in top_tokens) / len(top_tokens)
        avg_volume = sum(t['volume'] for t in top_tokens) / len(top_tokens)
        avg_score = sum(t['alpha_score'] for t in top_tokens) / len(top_tokens)
        
        report.append("")
        report.append("📊 MARKET DYNAMICS:")
        report.append(f"• Alpha Candidates: {len(top_tokens)}")
        report.append(f"• Avg Market Cap: ${avg_mcap:,.0f}")
        report.append(f"• Avg Volume: ${avg_volume:,.0f}")
        report.append(f"• Avg Alpha Score: {avg_score:.1f}/100")
    
    report.append("")
    report.append("⚠️ RISK ASSESSMENT:")
    report.append("• HIGH VOLATILITY: These are speculative micro-cap assets")
    report.append("• LIMITED DATA: API returns may be incomplete")
    report.append("• DYOR: Always conduct thorough research")
    
    return "\n".join(report)

def main():
    print("🔍 DexScreener Alpha Scanner")
    print("Scanning for gems in $30k-$200k range...\n")
    
    tokens = scan_dexscreener()
    print(f"✅ Found {len(tokens)} tokens in target range")
    
    report = generate_report(tokens)
    
    print("\n" + report)
    
    # Save to file for cron
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"cron_alpha_report_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"\n📄 Report saved to: {filename}")

if __name__ == "__main__":
    main()