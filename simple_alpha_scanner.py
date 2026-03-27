#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

def fetch_top_tokens():
    """Fetch top tokens from DexScreener's main API"""
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    headers = {'User-Agent': 'OpenClaw/1.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def filter_alpha_candidates(data, min_mcap=30000, max_mcap=200000):
    if not data or 'pairs' not in data:
        return []
    
    candidates = []
    
    for token in data['pairs']:
        market_cap = token.get('marketCap', 0)
        
        # Filter by market cap range
        if min_mcap <= market_cap <= max_mcap:
            # Calculate key metrics
            volume_24h = token.get('volume', {}).get('h24', 0)
            vol_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            txns_24h = token.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Calculate alpha score
            score = 0
            score += min(40, vol_ratio * 0.4)        # Volume momentum
            score += min(30, buy_ratio * 0.3)        # Buy pressure
            score += min(20, max(0, token.get('priceChange', {}).get('h24', 0)) * 0.5)  # Price momentum
            score += min(10, token.get('liquidity', {}).get('usd', 0) / 10000)  # Liquidity
            
            candidate = {
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'vol_ratio': vol_ratio,
                'price_change': token.get('priceChange', {}).get('h24', 0),
                'liquidity': token.get('liquidity', {}).get('usd', 0),
                'buy_ratio': buy_ratio,
                'buy_count': buys,
                'sell_count': sells,
                'alpha_score': score,
                'url': token.get('url', '')
            }
            candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(candidates):
    current_time = datetime.now().strftime('%A, March 4, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🎯 MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 50)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Range: $30K-$200K")
    report.append("Source: DexScreener API")
    report.append("")
    
    if not candidates:
        report.append("❌ No tokens found in the target market cap range")
        report.append("The market may be quiet or API may have limited data")
        report.append("Consider widening the mcap range to $10K-$500K")
        return "\n".join(report)
    
    report.append(f"🔍 TOP ALPHA CANDIDATES ({len(candidates)} total):")
    
    for i, candidate in enumerate(candidates[:10], 1):
        report.append(f"\n{i}. {candidate['symbol']} - Alpha: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • MCap: ${candidate['market_cap']:,.0f}")
        report.append(f"   • Volume: ${candidate['volume_24h']:,.0f} ({candidate['vol_ratio']:.1f}%)")
        report.append(f"   • Price: {candidate['price_change']:+.1f}%")
        report.append(f"   • Buys/Sells: {candidate['buy_count']}/{candidate['sell_count']}")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,.0f}")
    
    # Market summary
    if candidates:
        avg_score = sum(c['alpha_score'] for c in candidates) / len(candidates)
        avg_vol = sum(c['vol_ratio'] for c in candidates) / len(candidates)
        avg_buy = sum(c['buy_ratio'] for c in candidates) / len(candidates)
        
        report.append(f"\n📊 MARKET SUMMARY:")
        report.append(f"• Total tokens: {len(candidates)}")
        report.append(f"• Avg Alpha Score: {avg_score:.1f}/100")
        report.append(f"• Avg Volume Ratio: {avg_vol:.1f}%")
        report.append(f"• Avg Buy Ratio: {avg_buy:.1f}%")
    
    report.append("\n⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile")
    report.append("• Do your own research before investing")
    report.append("• Only risk what you can afford to lose")
    
    return "\n".join(report)

def main():
    print("Scanning DexScreener for alpha memecoins...")
    
    data = fetch_top_tokens()
    if not data:
        return "❌ Failed to fetch data from DexScreener API"
    
    candidates = filter_alpha_candidates(data)
    report = generate_report(candidates)
    
    return report

if __name__ == "__main__":
    result = main()
    print(result)