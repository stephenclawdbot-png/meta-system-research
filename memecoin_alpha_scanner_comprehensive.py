#!/usr/bin/env python3
import json
import requests
from datetime import datetime

# Function to fetch memecoin data from multiple DexScreener searches
def fetch_memecoin_data():
    tokens = []
    
    # Search terms for memecoins
    search_terms = ["memecoin", "pump", "bonk", "doge", "shib", "sats", "cat", "inu"]
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url)
            data = response.json()
            
            if 'pairs' in data:
                tokens.extend(data['pairs'])
                print(f"✓ Found {len(data['pairs'])} tokens for search term: {term}")
            else:
                print(f"✗ No results for search term: {term}")
                
        except Exception as e:
            print(f"❌ Error fetching {term}: {e}")
    
    # Remove duplicates based on pairAddress
    seen_addresses = set()
    unique_tokens = []
    for token in tokens:
        if token.get('pairAddress') not in seen_addresses:
            seen_addresses.add(token.get('pairAddress'))
            unique_tokens.append(token)
    
    return unique_tokens

# Function to filter memecoins by market cap range and calculate alpha metrics
def filter_alpha_candidates(data, min_mcap=30000, max_mcap=200000):
    candidates = []
    
    for token in data:
        # Focus on Solana chain (where most memecoins are)
        if token.get('chainId') != 'solana':
            continue
            
        market_cap = token.get('marketCap', 0)
        
        # Filter by market cap range
        if min_mcap <= market_cap <= max_mcap:
            base_token = token.get('baseToken', {})
            
            # Skip if symbol contains "SOL" or is the actual SOL token
            symbol = base_token.get('symbol', '').upper()
            name = base_token.get('name', '').lower()
            if 'SOL' in symbol or 'solana' in name or symbol == 'SOL':
                continue
            
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
            vol_score = min(40, vol_mcap_ratio * 0.4)
            buy_score = min(30, buy_ratio * 0.3)
            momentum_score = min(20, max(0, price_change_24h) * 0.5)
            liquidity_score = min(10, liquidity / 10000)
            
            # Additional scoring for age freshness
            created_at = token.get('pairCreatedAt')
            age_freshness = 0
            if created_at:
                # Lower score for very old tokens, higher for newer ones
                age_days = (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60 * 24)
                if age_days < 7:  # Tokens <1 week old get bonus
                    age_freshness = min(10, (7 - age_days) * 1.5)
            
            alpha_score = vol_score + buy_score + momentum_score + liquidity_score + age_freshness
            
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
                'created_at': token.get('pairCreatedAt'),
                'age_days': (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60 * 24) if created_at else 999
            }
            candidates.append(candidate)
    
    # Sort by alpha score descending
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

# Generate detailed report
def generate_report(candidates):
    current_time = datetime.now().strftime('%A, March 2, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 60)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Target: $30,000 - $200,000")
    report.append("Sources: DexScreener API (multi-term search)")
    report.append("")

    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Market conditions may have shifted - try adjusting the filters")
        return "\n".join(report)
    
    report.append(f"🔥 DISCOVERED {len(candidates)} POTENTIAL ALPHA GEMS:")
    report.append("")
    
    # Top candidates (show up to 15 for comprehensive view)
    max_candidates = min(15, len(candidates))
    
    for i, candidate in enumerate(candidates[:max_candidates], 1):
        report.append(f"{i}. 🎯 {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • Name: {candidate['name'][:50]}{'...' if len(candidate['name']) > 50 else ''}")
        report.append(f"   • Market Cap: ${candidate['market_cap']:,}")
        report.append(f"   • 24h Volume: ${candidate['volume_24h']:,}")
        report.append(f"   • Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change_24h']:+.1f}%")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,}")
        report.append(f"   • Buy/Sell Ratio: {candidate['buy_sell_ratio']} ({candidate['buy_ratio']:.1f}% buys)")
        report.append(f"   • Age: {candidate['age_days']:.1f} days")
        report.append(f"   • DexScreener: {candidate['url']}")
        report.append("")
    
    # Market observations
    report.append("📊 MARKET ANALYSIS:")
    report.append(f"• Total candidates in range: {len(candidates)}")
    
    if candidates:
        avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in candidates) / len(candidates)
        avg_buy_ratio = sum(c['buy_ratio'] for c in candidates) / len(candidates)
        avg_mcap = sum(c['market_cap'] for c in candidates) / len(candidates)
        avg_age = sum(c['age_days'] for c in candidates) / len(candidates)
        
        report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
        report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
        report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
        report.append(f"• Average Age: {avg_age:.1f} days")
        report.append(f"• Highest Alpha Score: {max(c['alpha_score'] for c in candidates):.1f}")
        
        # Find youngest tokens
        youngest = min(candidates, key=lambda x: x['age_days'])
        report.append(f"• Youngest Token: {youngest['symbol']} ({youngest['age_days']:.1f} days)")
    
    # Alpha insights
    report.append("")
    report.append("💡 ALPHA INSIGHTS:")
    if candidates:
        report.append("• Volume/Market Cap ratio indicates liquidity efficiency")
        report.append("• Higher buy ratios suggest bullish sentiment")
        report.append("• Positive price momentum shows growing interest")
        report.append("• Younger tokens (<7 days) often indicate early opportunities")
    
    # Risk assessment
    report.append("")
    report.append("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Always conduct your own research before investing")
    report.append("• Memecoins are extremely volatile")
    report.append("• Only risk what you can afford to lose")
    report.append("• Past performance does not guarantee future results")
    
    return "\n".join(report)

def main():
    print("🔍 Comprehensive memecoin alpha scanning in progress...")
    print("Searching DexScreener for: memecoin, pump, bonk, doge, shib, sats, cat, inu")
    print("=" * 60)
    
    try:
        data = fetch_memecoin_data()
        print(f"\n✅ Total unique tokens found: {len(data)}")
        
        candidates = filter_alpha_candidates(data)
        print(f"✅ Filtered to {len(candidates)} tokens in $30K-$200K mcap range")
        
        report = generate_report(candidates)
        return report
        
    except Exception as e:
        error_report = f"❌ Error during memecoin scan: {e}\n"
        error_report += "The DexScreener API may be experiencing issues or rate limiting."
        return error_report

if __name__ == "__main__":
    result = main()
    print("\n" + result)