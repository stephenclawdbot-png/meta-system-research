#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

# Set of memecoin-related keywords
MEMECOIN_KEYWORDS = [
    "meme", "memecoin", "pepe", "doge", "shiba", "bonk", "wojak", 
    "cat", "dog", "frog", "catcoin", "dogcoin", "wif", "wifhat",
    "kitty", "puppy", "elon", "musk", "smiley", "smile", "based",
    "chad", "alpha", "beta", "gm", "gn", "wagmi", "hamburger",
    "bigmac", "coke", "wendy", "harambe", "gom", "corona",
    "poop", "shitcoin", "floki", "elonmask", "richer", "basedball"
]

def search_dexscreener(keyword):
    """Search DexScreener for a specific keyword"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API returned status {response.status_code} for keyword {keyword}")
            return None
    except Exception as e:
        print(f"Error fetching data for {keyword}: {e}")
        return None

def filter_alpha_candidates(data, min_mcap=30000, max_mcap=200000):
    candidates = []
    
    if not data or 'pairs' not in data:
        return candidates
    
    for token in data['pairs']:
        market_cap = token.get('marketCap', 0)
        
        # Filter by market cap range and focus on Solana
        if market_cap and min_mcap <= market_cap <= max_mcap and token.get('chainId') == 'solana':
            base_token = token.get('baseToken', {})
            
            # Skip tokens with very low volume
            volume_24h = token.get('volume', {}).get('h24', 0)
            if volume_24h < 1000:  # Minimum volume
                continue
                
            # Calculate alpha metrics
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Calculate buy ratio
            txns_24h = token.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Skip tokens with low buy ratio
            if buy_ratio < 45:
                continue
                
            # Price changes
            price_change_24h = token.get('priceChange', {}).get('h24', 0)
            
            # Liquidity
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            # Skip tokens with very low liquidity
            if liquidity < 1000:
                continue
            
            # Calculate composite alpha score (0-100)
            alpha_score = 0
            
            # Volume/MCap ratio component (max 40 points)
            vol_score = min(40, vol_mcap_ratio * 0.4)
            
            # Buy ratio component (max 30 points)
            buy_score = min(30, buy_ratio * 0.3)
            
            # Price momentum component (max 20 points)
            momentum_score = min(20, max(0, price_change_24h) * 0.5)
            
            # Liquidity component (max 10 points)
            liquidity_score = min(10, liquidity / 10000)
            
            alpha_score = vol_score + buy_score + momentum_score + liquidity_score
            
            # Skip tokens with very low alpha score
            if alpha_score < 30:
                continue
            
            candidate = {
                'symbol': base_token.get('symbol', 'Unknown'),
                'name': base_token.get('name', 'Unknown'),
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'price_usd': token.get('priceUsd', 0),
                'price_change_24h': price_change_24h,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_ratio': buy_ratio,
                'buy_sell_ratio': f"{buys}/{sells}",
                'pair_address': token.get('pairAddress', ''),
                'url': token.get('url', ''),
                'search_keyword': data.get('keyword', 'unknown'),
                'chain': token.get('chainId', '')
            }
            candidates.append(candidate)
    
    return candidates

def generate_report(candidates):
    current_time = datetime.now().strftime('%A, March 4, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 ENHANCED MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 65)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Focus: $30,000 - $200,000")
    report.append("Chain Focus: Solana")
    report.append("Sources: DexScreener API with 20+ memecoin keywords")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Market may lack promising opportunities currently")
        return "\n".join(report)
    
    # Remove duplicates by pair address
    unique_candidates = {}
    for candidate in candidates:
        key = candidate['pair_address']
        if key not in unique_candidates or candidate['alpha_score'] > unique_candidates[key]['alpha_score']:
            unique_candidates[key] = candidate
    
    final_candidates = list(unique_candidates.values())
    final_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report.append(f"🔥 TOP ALPHA GEMS DISCOVERED ({len(final_candidates)} total):")
    
    for i, candidate in enumerate(final_candidates[:10], 1):
        report.append(f"\n{i}. 🔗 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • Market Cap: ${candidate['market_cap']:,}")
        report.append(f"   • 24h Volume: ${candidate['volume_24h']:,}")
        report.append(f"   • Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change_24h']:.1f}%")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,}")
        report.append(f"   • Buy Ratio: {candidate['buy_ratio']:.1f}%")
        report.append(f"   • Transactions: {candidate['buy_sell_ratio']}")
        report.append(f"   • Keyword: {candidate.get('search_keyword', 'unknown')}")
    
    # Market analysis
    report.append("\n📊 MARKET ANALYSIS:")
    avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in final_candidates) / len(final_candidates)
    avg_buy_ratio = sum(c['buy_ratio'] for c in final_candidates) / len(final_candidates)
    avg_mcap = sum(c['market_cap'] for c in final_candidates) / len(final_candidates)
    avg_liquidity = sum(c['liquidity'] for c in final_candidates) / len(final_candidates)
    
    report.append(f"• Total unique tokens: {len(final_candidates)}")
    report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
    report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
    report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
    report.append(f"• Average Liquidity: ${avg_liquidity:,.0f}")
    report.append(f"• Top Alpha Score: {max(c['alpha_score'] for c in final_candidates):.1f}")
    
    # Keyword analysis
    keywords_used = set(c.get('search_keyword', 'unknown') for c in final_candidates)
    if keywords_used:
        report.append(f"• Keywords producing results: {len(keywords_used)}")
    
    # Alpha insights
    report.append("\n💡 ALPHA INSIGHTS:")
    high_volume_candidates = [c for c in final_candidates if c['vol_mcap_ratio'] > 100]
    strong_buy_ratio = [c for c in final_candidates if c['buy_ratio'] > 70]
    
    report.append(f"• Tokens with Vol/MCap > 100%: {len(high_volume_candidates)}")
    report.append(f"• Tokens with Buy Ratio > 70%: {len(strong_buy_ratio)}")
    
    # Risk assessment
    report.append("\n⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile - DYOR required")
    report.append("• Only invest what you can afford to lose")
    report.append("• Monitor key metrics: volume, buy ratio, liquidity")
    
    return "\n".join(report)

def main():
    print("🔍 Enhanced memecoin alpha scanner starting...")
    print(f"Searching with {len(MEMECOIN_KEYWORDS)} keywords...")
    
    all_candidates = []
    successful_searches = 0
    
    for keyword in MEMECOIN_KEYWORDS:
        print(f"Searching for '{keyword}'...")
        data = search_dexscreener(keyword)
        if data:
            data['keyword'] = keyword  # Track which keyword found this
            candidates = filter_alpha_candidates(data)
            all_candidates.extend(candidates)
            successful_searches += 1
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n✅ Completed {successful_searches}/{len(MEMECOIN_KEYWORDS)} searches")
    
    report = generate_report(all_candidates)
    return report

if __name__ == "__main__":
    result = main()
    print(result)