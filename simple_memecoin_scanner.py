#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

def search_tokens(query_term):
    """Search DexScreener for tokens with given query term"""
    url = f"https://api.dexscreener.com/latest/dex/search/?q={query_term}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error searching tokens: {e}")
        return None

def filter_memecoins(data, min_mcap=30000, max_mcap=200000):
    """Filter memecoins by market cap and extract key metrics"""
    candidates = []
    
    if not data or 'pairs' not in data:
        return candidates
    
    for token in data['pairs']:
        market_cap = token.get('marketCap')
        
        # Skip tokens without market cap or outside our range
        if not market_cap or market_cap < min_mcap or market_cap > max_mcap:
            continue
            
        # Extract key metrics
        base_token = token.get('baseToken', {})
        volume_24h = token.get('volume', {}).get('h24', 0)
        buy_sells = token.get('txns', {}).get('h24', {})
        buys = buy_sells.get('buys', 0)
        sells = buy_sells.get('sells', 0)
        total_txns = buys + sells
        
        # Skip tokens with zero/low volume or insufficient transactions
        if volume_24h < 100 or total_txns < 5:
            continue
        
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        volume_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
        liquidity = token.get('liquidity', {}).get('usd', 0)
        
        # Skip tokens with extremely low liquidity
        if liquidity < 100:
            continue
        
        # Enhanced alpha scoring
        # Volume/MCap Ratio: 40% weight (higher = better)
        volume_score = min(40, volume_mcap_ratio * 0.4)
        
        # Buy Ratio: 25% weight (higher = more buying pressure)
        buy_score = min(25, buy_ratio * 0.25)
        
        # Price Momentum: 15% weight (positive momentum preferred)
        price_change = token.get('priceChange', {}).get('h24', 0)
        momentum_score = max(0, min(15, price_change * 0.3))
        
        # Liquidity Quality: 10% weight (adequate liquidity)
        liquidity_score = min(10, liquidity / 5000)
        
        # Trading Activity: 10% weight (adequate transaction count)
        activity_score = min(10, min(total_txns / 10, 10))
        
        alpha_score = volume_score + buy_score + momentum_score + liquidity_score + activity_score
        
        candidate = {
            'symbol': base_token.get('symbol', 'Unknown'),
            'name': base_token.get('name', 'Unknown'),
            'market_cap': market_cap,
            'price_usd': token.get('priceUsd', 0),
            'volume_24h': volume_24h,
            'volume_mcap_ratio': volume_mcap_ratio,
            'price_change_24h': price_change,
            'buy_ratio': buy_ratio,
            'buys': buys,
            'sells': sells,
            'total_txns': total_txns,
            'liquidity': liquidity,
            'chain': token.get('chainId', 'Unknown'),
            'pair_address': token.get('pairAddress', ''),
            'url': token.get('url', ''),
            'alpha_score': alpha_score
        }
        candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(candidates, query_term):
    """Generate alpha scanner report"""
    current_time = datetime.now().strftime('%A, March 6, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 50)
    report.append(f"Scan Time: {current_time}")
    report.append(f"Target Range: $30,000 - $200,000")
    report.append(f"Search Query: {query_term}")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Market may lack promising opportunities currently")
        return "\n".join(report)
    
    report.append(f"🔥 TOP ALPHA GEMS DISCOVERED ({len(candidates)} total):")
    report.append("")
    
    for i, candidate in enumerate(candidates[:10], 1):
        trend_emoji = "📈" if candidate['price_change_24h'] > 0 else "📉"
        report.append(f"{i}. {trend_emoji} **{candidate['symbol']}** - Alpha Score: **{candidate['alpha_score']:.1f}/100**")
        report.append(f"   • Name: {candidate['name']}")
        report.append(f"   • Market Cap: **${candidate['market_cap']:,.0f}**")
        report.append(f"   • 24h Volume: ${candidate['volume_24h']:,.0f}")
        report.append(f"   • Vol/MCap Ratio: {candidate['volume_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change_24h']:+.1f}%")
        report.append(f"   • Buy Ratio: {candidate['buy_ratio']:.1f}% ({candidate['buys']}/{candidate['sells']})")
        report.append(f"   • Chain: {candidate['chain']}")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,.0f}")
        report.append("")
    
    # Market statistics
    report.append("📊 MARKET STATISTICS:")
    report.append(f"• Total candidates found: {len(candidates)}")
    if candidates:
        avg_vol_ratio = sum(c['volume_mcap_ratio'] for c in candidates) / len(candidates)
        avg_buy_ratio = sum(c['buy_ratio'] for c in candidates) / len(candidates)
        avg_mcap = sum(c['market_cap'] for c in candidates) / len(candidates)
        
        report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
        report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
        report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
        report.append(f"• Highest Alpha Score: {max(c['alpha_score'] for c in candidates):.1f}")
    
    # Risk disclaimer
    report.append("")
    report.append("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile - DYOR required")
    report.append("• Only invest what you can afford to lose")
    report.append("• Monitor key metrics: volume, buy ratio, liquidity")
    
    return "\n".join(report)

def main():
    """Main scanning function"""
    print("🔍 Scanning DexScreener for memecoin alpha opportunities...")
    
    # Search terms for memecoins
    search_terms = ["dog", "cat", "meme", "pepe", "shiba", "elon", "bonk", "wif", "turbo", "bome"]
    
    all_candidates = []
    
    for term in search_terms:
        print(f"Searching for '{term}' tokens...")
        data = search_tokens(term)
        if data:
            candidates = filter_memecoins(data)
            all_candidates.extend(candidates)
        time.sleep(1)  # Rate limiting
    
    # Remove duplicates
    unique_candidates = {}
    for candidate in all_candidates:
        key = candidate['pair_address']
        if key not in unique_candidates or candidate['alpha_score'] > unique_candidates[key]['alpha_score']:
            unique_candidates[key] = candidate
    
    final_candidates = list(unique_candidates.values())
    final_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report = generate_report(final_candidates, ", ".join(search_terms))
    return report

if __name__ == "__main__":
    result = main()
    print(result)