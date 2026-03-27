#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

def search_dexscreener(query):
    """Search DexScreener"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def filter_tokens(data, min_mcap=30000, max_mcap=200000):
    """Filter tokens by market cap and calculate alpha metrics"""
    candidates = []
    if not data or 'pairs' not in data or not data['pairs']:
        return candidates
    
    for token in data['pairs']:
        market_cap = token.get('marketCap', 0)
        
        # Focus on Solana chain and market cap range
        if min_mcap <= market_cap <= max_mcap and token.get('chainId') == 'solana':
            volume_24h = token.get('volume', {}).get('h24', 0)
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total = buys + sells
            buy_ratio = (buys / total * 100) if total > 0 else 0
            price_change = token.get('priceChange', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            # Volume filters
            if volume_24h < 1000:  # Minimum volume
                continue
            
            # Transaction filters
            if total < 5:
                continue
                
            # Buy ratio filter
            if buy_ratio < 55:  # More buys than sells
                continue
            
            # Liquidity filter
            if liquidity < 1000:  # Minimum liquidity
                continue
            
            # Calculate volume/market cap ratio
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Advanced alpha score (0-100)
            # Volume/MCap ratio component (40 points max)
            vol_score = min(40, vol_mcap_ratio * 0.4)
            
            # Buy ratio component (30 points max)
            buy_score = min(30, buy_ratio * 0.3)
            
            # Price momentum component (20 points max)
            momentum_score = min(20, max(0, price_change) * 0.1)
            
            # Liquidity safety component (10 points max)
            liquidity_score = min(10, liquidity / 5000)
            
            alpha_score = vol_score + buy_score + momentum_score + liquidity_score
            
            # Age consideration (approximate from creation timestamp)
            created_at = token.get('pairCreatedAt')
            age_hours = None
            if created_at:
                age_hours = (time.time() - created_at/1000) / 3600
                # Boost score for newer tokens
                if age_hours < 24:
                    alpha_score *= 1.1  # 10% boost for tokens < 24h old
            
            candidate = {
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                'market_cap': market_cap,
                'volume': volume_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'buy_ratio': buy_ratio,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_sell': f"{buys}/{sells}",
                'url': token.get('url', ''),
                'pair_address': token.get('pairAddress', ''),
                'age_hours': age_hours
            }
            candidates.append(candidate)
    
    return candidates

def generate_report(candidates, keywords_used):
    """Generate comprehensive alpha report"""
    current_time = datetime.now().strftime('%A, March 4, 2026 — %I:%M %p (Asia/Manila)')
    report = []
    
    report.append("🧠 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP")
    report.append("=" * 65)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Target: $30,000 - $200,000")
    report.append("Chain Focus: Solana")
    report.append(f"Keywords Searched: {', '.join(keywords_used)}")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in target range")
        report.append("Market conditions may be unfavorable")
        return "\n".join(report)
    
    # Remove duplicates
    unique_candidates = {}
    for candidate in candidates:
        key = candidate['pair_address']
        if key not in unique_candidates or candidate['alpha_score'] > unique_candidates[key]['alpha_score']:
            unique_candidates[key] = candidate
    
    final_candidates = list(unique_candidates.values())
    final_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report.append(f"🔥 TOP ALPHA GEMS DISCOVERED ({len(final_candidates)} total):")
    report.append("")
    
    for i, candidate in enumerate(final_candidates[:8], 1):
        age_info = f", Age: {candidate['age_hours']:.1f}h" if candidate['age_hours'] else ""
        report.append(f"{i}. 🎯 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • Market Cap: ${candidate['market_cap']:,.0f}")
        report.append(f"   • 24h Volume: ${candidate['volume']:,.0f}")
        report.append(f"   • Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change']:+.1f}%")
        report.append(f"   • Buy Ratio: {candidate['buy_ratio']:.1f}% ({candidate['buy_sell']})")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,.0f}{age_info}")
        report.append(f"   • DexScreener: {candidate['url']}")
        report.append("")
    
    # Market analysis
    report.append("📊 MARKET ANALYSIS:")
    report.append(f"• Total qualifying tokens: {len(final_candidates)}")
    
    if final_candidates:
        avg_mcap = sum(c['market_cap'] for c in final_candidates) / len(final_candidates)
        avg_volume = sum(c['volume'] for c in final_candidates) / len(final_candidates)
        avg_buy_ratio = sum(c['buy_ratio'] for c in final_candidates) / len(final_candidates)
        avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in final_candidates) / len(final_candidates)
        top_score = max(c['alpha_score'] for c in final_candidates)
        
        report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
        report.append(f"• Average Volume: ${avg_volume:,.0f}")
        report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
        report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
        report.append(f"• Top Alpha Score: {top_score:.1f}/100")
    
    # Alpha insights
    report.append("")
    report.append("💡 KEY METRICS TO WATCH:")
    report.append("• Volume/MCap Ratio > 100% = High trading interest")
    report.append("• Buy Ratio > 60% = Strong accumulation")
    report.append("• Age < 24h = Fresh opportunity")
    report.append("• Liquidity > $10K = Better price stability")
    
    # Risk assessment
    report.append("")
    report.append("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile - DYOR required")
    report.append("• Only invest what you can afford to lose")
    report.append("• Monitor key metrics: volume, buy ratio, liquidity")
    
    return "\n".join(report)

def main():
    print("🔍 Running Alpha Scanner - DexScreener API")
    
    # Popular memecoin keywords
    keywords = ["bonk", "wif", "pepe", "doge", "shib", "harambe", "floki", "elon", "kitty", 
                "puppy", "cat", "dog", "frog", "based", "wagmi", "hodl", "richer", "chad"]
    
    all_candidates = []
    successful_searches = []
    
    for keyword in keywords:
        print(f"Searching '{keyword}'...")
        data = search_dexscreener(keyword)
        if data and data.get('pairs'):
            candidates = filter_tokens(data)
            all_candidates.extend(candidates)
            successful_searches.append(keyword)
            time.sleep(0.3)  # Rate limiting
    
    print(f"\n✅ Completed {len(successful_searches)}/{len(keywords)} searches")
    
    report = generate_report(all_candidates, successful_searches)
    return report

if __name__ == "__main__":
    result = main()
    print(result)