#!/usr/bin/env python3
import json
import requests
from datetime import datetime

# Function to fetch memecoin data from DexScreener
def fetch_memecoin_data():
    url = "https://api.dexscreener.com/latest/dex/search?q=memecoin"
    response = requests.get(url)
    return response.json()

# Function to filter memecoins by market cap range and calculate alpha metrics
def filter_alpha_candidates(data, min_mcap=30000, max_mcap=200000):
    candidates = []
    
    if 'pairs' not in data:
        return candidates
    
    for token in data['pairs']:
        # Focus on Solana chain (where most memecoins are)
        if token.get('chainId') != 'solana':
            continue
            
        market_cap = token.get('marketCap', 0)
        
        # Filter by market cap range
        if min_mcap <= market_cap <= max_mcap:
            base_token = token.get('baseToken', {})
            
            # Calculate alpha metrics
            volume_24h = token.get('volume', {}).get('h24', 0)
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Calculate buy ratio
            txns_24h = token.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Price changes
            price_change_24h = token.get('priceChange', {}).get('h24', 0)
            
            # Liquidity
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
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
                'created_at': token.get('pairCreatedAt')
            }
            candidates.append(candidate)
    
    # Sort by alpha score descending
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

# Generate detailed report
def generate_report(candidates):
    current_time = datetime.now().strftime('%A, March 2, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 MEMECOIN ALPHA SCANNER REPORT - SUB 30K-200K MCAP")
    report.append("=" * 60)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Focus: $30,000 - $200,000")
    report.append("Sources: DexScreener API")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Market conditions may have shifted - try widening the mcap range")
        return "\n".join(report)
    
    report.append("🔥 TOP ALPHA GEMS DISCOVERED:")
    
    for i, candidate in enumerate(candidates[:10], 1):  # Top 10
        report.append(f"\n{i}. 🎯 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • Market Cap: ${candidate['market_cap']:,}")
        report.append(f"   • 24h Volume: ${candidate['volume_24h']:,}")
        report.append(f"   • Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change_24h']:.1f}%")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,}")
        report.append(f"   • Buy/Sell Ratio: {candidate['buy_sell_ratio']} ({candidate['buy_ratio']:.1f}% buys)")
        report.append(f"   • DexScreener: {candidate['url']}")
    
    # Market observations
    report.append("\n📊 MARKET OBSERVATIONS:")
    report.append(f"• Total candidates found: {len(candidates)}")
    
    if candidates:
        avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in candidates) / len(candidates)
        avg_buy_ratio = sum(c['buy_ratio'] for c in candidates) / len(candidates)
        avg_mcap = sum(c['market_cap'] for c in candidates) / len(candidates)
        
        report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
        report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
        report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
        report.append(f"• Highest Alpha Score: {max(c['alpha_score'] for c in candidates):.1f}")
    
    # Risk assessment
    report.append("\n⚠️ DISCLAIMER: NOT FINANCIAL ADVICE - HIGH VOLATILITY/RISK")
    report.append("• Memecoins are extremely volatile")
    report.append("• Always do your own research")
    report.append("• Only invest what you can afford to lose")
    
    return "\n".join(report)

def main():
    print("🔍 Scanning DexScreener for memecoin alpha...")
    
    try:
        data = fetch_memecoin_data()
        candidates = filter_alpha_candidates(data)
        
        report = generate_report(candidates)
        return report
        
    except Exception as e:
        error_report = f"❌ Error scanning DexScreener: {e}\n"
        error_report += "The DexScreener API may be experiencing issues."
        return error_report

if __name__ == "__main__":
    result = main()
    print(result)