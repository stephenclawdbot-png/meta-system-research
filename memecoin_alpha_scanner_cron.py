#!/usr/bin/env python3
"""
Memecoin Alpha Scanner - Sub 30k-200k MCap Focus
Direct DexScreener API For High-Average Gas Fees
Short descriptive report format
"""

import requests
import json
from datetime import datetime
import time

# Queries that consistently yield memecoins
MEMECOIN_QUERIES = ["meme", "doge", "pepe", "shib", "floki", "elon", "cat", "dog", "based", "degen"]

# Exchange/trading-related terms
TRADING_QUERIES = ["gains", "ape", "gm", "wagmi", "snipe", "alpha", "crypto", "coin", "token"]

# Gaming/Web3 terms
GAMING_QUERIES = ["game", "nft", "metaverse", "web3", "play", "earn"]

ALL_QUERIES = MEMECOIN_QUERIES + TRADING_QUERIES + GAMING_QUERIES

def fetch_dexscreener_search(query):
    """Fetch tokens from DexScreener search API"""
    url = f"https://api.dexscreener.com/latest/dex/search/?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Query '{query}' failed: {response.status_code}")
            return {"pairs": []}
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return {"pairs": []}

def calculate_alpha_score(token_data):
    """Calculate alpha score based on various memecoin metrics"""
    score = 0
    
    # Market cap importance (max 30 points)
    mcap = token_data.get('marketCap', 0)
    if mcap:
        # Score higher for middle-range mcap (50k-150k)
        if 50000 <= mcap <= 150000:
            score += 25
        elif 30000 <= mcap <= 200000:
            score += 20
        else:
            score += 10
    
    # Volume/MCap ratio (max 25 points)
    volume = token_data.get('volume', {}).get('h24', 0)
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    if vol_mcap_ratio > 100:  # High volume relative to mcap
        score += 25
    elif vol_mcap_ratio > 50:
        score += 20
    elif vol_mcap_ratio > 20:
        score += 15
    elif vol_mcap_ratio > 10:
        score += 10
    elif vol_mcap_ratio > 5:
        score += 5
    
    # Price momentum (max 20 points)
    price_change = token_data.get('priceChange', {}).get('h24', 0)
    if price_change > 50:
        score += 20
    elif price_change > 20:
        score += 15
    elif price_change > 10:
        score += 12
    elif price_change > 5:
        score += 8
    elif price_change > 0:
        score += 4
    
    # Buy pressure (max 15 points)
    txns = token_data.get('txns', {}).get('h24', {})
    buys = txns.get('buys', 0)
    sells = txns.get('sells', 0)
    total_txns = buys + sells
    buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
    
    if buy_ratio > 70:
        score += 15
    elif buy_ratio > 60:
        score += 12
    elif buy_ratio > 50:
        score += 8
    elif buy_ratio > 40:
        score += 4
    
    # Liquidity score (max 10 points)
    liquidity = token_data.get('liquidity', {}).get('usd', 0)
    if liquidity > 50000:
        score += 10
    elif liquidity > 20000:
        score += 8
    elif liquidity > 10000:
        score += 6
    elif liquidity > 5000:
        score += 4
    elif liquidity > 1000:
        score += 2
    
    return min(100, score)

def filter_memecoin_gems(data):
    """Filter tokens in the 30k-200k mcap range and calculate alpha scores"""
    gems = []
    
    for pair in data.get('pairs', [])[:50]:  # Limit to top 50 results
        try:
            market_cap = pair.get('marketCap', 0)
            
            # Skip major tokens and very low mcap
            symbol = pair.get('baseToken', {}).get('symbol', '').upper()
            if symbol in ['SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'WETH', 'WBTC', 'BNB', 'AVAX']:
                continue
            
            if not (30000 <= market_cap <= 200000):
                continue
            
            # Skip tokens with no volume
            volume_24h = pair.get('volume', {}).get('h24', 0)
            if volume_24h < 10:
                continue
            
            # Calculate alpha score
            alpha_score = calculate_alpha_score(pair)
            
            # Only keep tokens with decent alpha score
            if alpha_score >= 20:
                gem = {
                    'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                    'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                    'marketCap': market_cap,
                    'volume24h': volume_24h,
                    'priceChange24h': pair.get('priceChange', {}).get('h24', 0),
                    'liquidity': pair.get('liquidity', {}).get('usd', 0),
                    'alphaScore': alpha_score,
                    'chain': pair.get('chainId', 'Unknown'),
                    'pairAddress': pair.get('pairAddress', ''),
                    'url': pair.get('url', ''),
                    'txns24h': pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
                }
                gems.append(gem)
                
        except Exception as e:
            continue
    
    return sorted(gems, key=lambda x: x['alphaScore'], reverse=True)

def generate_summary_report(gems):
    """Generate clean summary report"""
    current_time = datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP")
    report.append("=" * 60)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Focus: $30,000 - $200,000")
    report.append("") 
    
    if not gems:
        report.append("❌ No alpha gems detected in target range")
        report.append("Market may be quiet or filters too strict")
        return "\n".join(report)
    
    report.append(f"🔥 TOP ALPHA GEMS ({len(gems)} total):")
    report.append("-" * 60)
    
    # Show top 8 gems
    for i, gem in enumerate(gems[:8], 1):
        vol_mcap_ratio = (gem['volume24h'] / gem['marketCap'] * 100) if gem['marketCap'] > 0 else 0
        buy_txns = gem['txns24h'].get('buys', 0)
        sell_txns = gem['txns24h'].get('sells', 0)
        buy_ratio = (buy_txns / (buy_txns + sell_txns) * 100) if (buy_txns + sell_txns) > 0 else 0
        
        report.append(f"🎯 #{i} {gem['symbol']} - Alpha: {gem['alphaScore']}/100")
        report.append(f"   💰 MCap: ${gem['marketCap']:,} | Vol: ${gem['volume24h']:,}")
        report.append(f"   📈 24h Change: {gem['priceChange24h']:+.1f}%")
        report.append(f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}% | Buy Ratio: {buy_ratio:.1f}%")
        report.append(f"   🌐 Chain: {gem['chain']}")
        report.append(f"   🔗 URL: {gem['url']}")
        
        if i < len(gems[:8]):  # Add spacing between gems
            report.append("")
    
    # Overall market stats
    report.append("\n📊 MARKET ANALYSIS:")
    report.append("-" * 60)
    
    if gems:
        avg_mcap = sum(g['marketCap'] for g in gems) / len(gems)
        avg_volume = sum(g['volume24h'] for g in gems) / len(gems)
        avg_alpha = sum(g['alphaScore'] for g in gems) / len(gems)
        
        report.append(f"• Total Gems: {len(gems)} tokens")
        report.append(f"• Average MCap: ${avg_mcap:,.0f}")
        report.append(f"• Average Volume: ${avg_volume:,.0f}") 
        report.append(f"• Average Alpha Score: {avg_alpha:.1f}/100")
        report.append(f"• Top Alpha: {max(g['alphaScore'] for g in gems)}/100")
        
        # Chain distribution
        chains = {}
        for g in gems:
            chain = g['chain']
            chains[chain] = chains.get(chain, 0) + 1
        
        if chains:
            report.append(f"• Chain Breakdown: {', '.join([f'{k}: {v}' for k, v in chains.items()])}")
    
    report.append("\n⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile - DYOR required")
    report.append("• Only invest what you can afford to lose")
    report.append("• Monitor key metrics: volume, buy ratio, liquidity")
    
    return "\n".join(report)

def main():
    """Main scanner function"""
    print("🔍 Scanning DexScreener for memecoin alpha...")
    
    all_gems = []
    
    # Scan with different queries
    for query in ALL_QUERIES[:8]:  # Limit to first 8 queries for speed
        print(f"Query: {query}")
        data = fetch_dexscreener_search(query)
        gems = filter_memecoin_gems(data)
        all_gems.extend(gems)
        time.sleep(1)  # Rate limiting
    
    # Remove duplicates
    unique_gems = {}
    for gem in all_gems:
        key = gem['pairAddress']
        if key not in unique_gems or gem['alphaScore'] > unique_gems[key]['alphaScore']:
            unique_gems[key] = gem
    
    final_gems = list(unique_gems.values())
    final_gems.sort(key=lambda x: x['alphaScore'], reverse=True)
    
    # Generate report
    report = generate_summary_report(final_gems)
    return report

if __name__ == "__main__":
    result = main()
    print(result)