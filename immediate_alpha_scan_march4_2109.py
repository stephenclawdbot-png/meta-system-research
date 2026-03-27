#!/usr/bin/env python3
"""
Immediate Alpha Scanner - March 4, 9:09 PM Focus
Target: 30k-200k mcap memecoins with real volume and momentum
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_data(query_type="new"):
    """Fetch data from DexScreener API"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={query_type}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return None

def calculate_strict_alpha_score(pair):
    """Calculate alpha score with stricter criteria"""
    score = 0
    mcap = pair.get('fdv', 0)
    volume = pair.get('volume', {}).get('h24', 0)
    price_change = pair.get('priceChange', {}).get('h24', 0)
    liquidity = pair.get('liquidity', {}).get('usd', 0)
    
    # TXN data structure is nested
    txns_h24 = pair.get('txns', {}).get('h24', {})
    buyers = txns_h24.get('buys', 0) if isinstance(txns_h24, dict) else 0
    sellers = txns_h24.get('sells', 0) if isinstance(txns_h24, dict) else 0
    total_txns = buyers + sellers
    
    # STRICT FILTERS FIRST - must pass minimums
    # Minimum volume threshold
    if volume < 1000:
        return 0
    
    # Minimum activity threshold
    if total_txns < 20:
        return 0
    
    # Minimum buy ratio
    buy_ratio = buyers / total_txns if total_txns > 0 else 0
    if buy_ratio < 0.4:
        return 0
    
    # NOW CALCULATE SCORE
    
    # Volume Score (0-40 points) - higher weight
    if volume > 50000:
        score += 40
    elif volume > 20000:
        score += 30
    elif volume > 5000:
        score += 20
    elif volume > 2000:
        score += 10
    
    # Volume/MCap Ratio Score (0-25 points)
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    if vol_mcap_ratio > 50:
        score += 25
    elif vol_mcap_ratio > 20:
        score += 20
    elif vol_mcap_ratio > 10:
        score += 15
    elif vol_mcap_ratio > 5:
        score += 10
    elif vol_mcap_ratio > 2:
        score += 5
    
    # Price Momentum Score (0-20 points)
    if price_change > 50:
        score += 20
    elif price_change > 20:
        score += 15
    elif price_change > 10:
        score += 10
    elif price_change > 5:
        score += 7
    elif price_change > 0:
        score += 5
    
    # Buy/Sell Pressure (0-15 points)
    if buy_ratio > 0.8:
        score += 15
    elif buy_ratio > 0.7:
        score += 12
    elif buy_ratio > 0.6:
        score += 9
    elif buy_ratio > 0.5:
        score += 6
    elif buy_ratio > 0.4:
        score += 3
    
    return score

def scan_for_real_alpha():
    """Scan with focused criteria"""
    alpha_candidates = []
    
    # High-probability searches
    search_terms = ["meme", "pump", "coin", "solana", "base", "bnb", "ethereum"]
    
    for term in search_terms:
        print(f"🔍 Scanning for '{term}'...")
        data = fetch_dexscreener_data(term)
        
        if data and 'pairs' in data:
            for pair in data['pairs']:
                mcap = pair.get('fdv', 0)
                
                # Only consider 30k-200k range
                if 30000 <= mcap <= 200000:
                    # Calculate strict score
                    alpha_score = calculate_strict_alpha_score(pair)
                    
                    if alpha_score > 0:  # Only include if passes basic filters
                        volume = pair.get('volume', {}).get('h24', 0)
                        price_change = pair.get('priceChange', {}).get('h24', 0)
                        liquidity = pair.get('liquidity', {}).get('usd', 0)
                        
                        txns_h24 = pair.get('txns', {}).get('h24', {})
                        buyers = txns_h24.get('buys', 0) if isinstance(txns_h24, dict) else 0
                        sellers = txns_h24.get('sells', 0) if isinstance(txns_h24, dict) else 0
                        total_txns = buyers + sellers
                        buy_ratio = buyers / total_txns if total_txns > 0 else 0
                        
                        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
                        
                        # Avoid duplicates
                        symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                        
                        if not any(c['symbol'] == symbol for c in alpha_candidates):
                            alpha_candidates.append({
                                'symbol': symbol,
                                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                                'mcap': mcap,
                                'volume': volume,
                                'vol_mcap_ratio': vol_mcap_ratio,
                                'price_change': price_change,
                                'liquidity': liquidity,
                                'txns': total_txns,
                                'buyers': buyers,
                                'sellers': sellers,
                                'buy_ratio': buy_ratio,
                                'alpha_score': alpha_score,
                                'chain': pair.get('chainId', 'Unknown'),
                                'pair_address': pair.get('pairAddress'),
                                'dex_url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                                'created_at': pair.get('pairCreatedAt', '')
                            })
    
    # Sort by alpha score
    alpha_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_candidates

def generate_immediate_report():
    """Generate focused report"""
    timestamp = datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')
    
    print(f"🔥 IMMEDIATE ALPHA SCANNER - STRICT FILTERS")
    print("=" * 70)
    print(f"Scan Time: {timestamp}")
    print(f"Market Cap Range: $30,000 - $200,000")
    print("=" * 70)
    print()
    
    alpha_candidates = scan_for_real_alpha()
    
    if alpha_candidates:
        print(f"💎 QUALITY ALPHA GEMS FOUND: {len(alpha_candidates)}")
        print("-" * 70)
        print()
        
        for candidate in alpha_candidates[:5]:  # Top 5 only
            print(f"🎯 {candidate['symbol']} ({candidate['name']})")
            print(f"   ⚡ Alpha Score: {candidate['alpha_score']}/100")
            print(f"   💰 Market Cap: ${candidate['mcap']:,}")
            print(f"   📈 24h Volume: ${candidate['volume']:,}")
            print(f"   🔥 Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
            print(f"   📊 Price Change: {candidate['price_change']:.1f}%")
            print(f"   💧 Liquidity: ${candidate['liquidity']:,}")
            print(f"   🔄 Transactions: {candidate['txns']}/24h ({candidate['buyers']} buys, {candidate['sellers']} sells)")
            print(f"   📈 Buy Ratio: {candidate['buy_ratio']:.1%}")
            print(f"   🌐 Chain: {candidate['chain']}")
            print(f"   🔗 DexScreener: {candidate['dex_url']}")
            print()
    else:
        print("⚠️ No alpha gems passed strict filters")
        print("Market conditions are quiet or criteria too restrictive")
        print()
    
    # Market sentiment
    total_potential = len(alpha_candidates)
    if total_potential > 0:
        avg_score = sum(c['alpha_score'] for c in alpha_candidates) / total_potential
        avg_mcap = sum(c['mcap'] for c in alpha_candidates) / total_potential
        avg_volume = sum(c['volume'] for c in alpha_candidates) / total_potential
        
        print("📊 MARKET SENTIMENT:")
        print("-" * 30)
        print(f"• Quality Gems Found: {total_potential}")
        print(f"• Average Score: {avg_score:.1f}/100")
        print(f"• Avg MCap: ${avg_mcap:,.0f}")
        print(f"• Avg Volume: ${avg_volume:,.0f}")
        print()
        
        # Actionable insight
        if avg_score > 50:
            print("🔔 MARKET INSIGHT: Strong alpha opportunities detected!")
        elif avg_score > 30:
            print("🔔 MARKET INSIGHT: Moderate alpha opportunities present")
        else:
            print("🔔 MARKET INSIGHT: Quiet market - consider waiting for better conditions")
    else:
        print("📉 MARKET SENTIMENT: Very quiet - no quality alpha detected")
    
    print()
    print("⚡ FILTER CRITERIA APPLIED:")
    print("-" * 30)
    print("• Minimum Volume: $1,000")
    print("• Minimum Transactions: 20")
    print("• Minimum Buy Ratio: 40%")
    print("• Market Cap Range: $30k-$200k")
    print()
    
    print("💡 STRATEGY RECOMMENDATION:")
    print("-" * 30)
    if alpha_candidates:
        print("• Focus on tokens with highest vol/mcap ratio")
        print("• Prioritize strong buy pressure (60%+ buy ratio)")
        print("• Avoid low liquidity pools")
        print("• Monitor transaction velocity closely")
    else:
        print("• Wait for better market conditions")
        print("• Consider expanding search criteria slightly")
        print("• Monitor for unexpected volume spikes")
    print()
    
    print("⚠️ DISCLAIMER: High-risk micro-cap analysis. DYOR before any action.")

if __name__ == "__main__":
    generate_immediate_report()