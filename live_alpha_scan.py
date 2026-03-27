#!/usr/bin/env python3
"""
Live Alpha Scanner for DexScreener - Focus on 30k-200k Market Cap
"""

import json
import requests
from datetime import datetime

def fetch_dexscreener_data(query="new"):
    """Fetch data from DexScreener API"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
    
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

def calculate_alpha_score(pair):
    """Calculate alpha score based on multiple factors"""
    mcap = pair.get('marketCap', 0)
    volume_h24 = pair.get('volume', {}).get('h24', 0)
    price_change = pair.get('priceChange', {}).get('h24', 0)
    liquidity = pair.get('liquidity', {}).get('usd', 0)
    txns_h24 = pair.get('txns', {}).get('h24', {})
    buys = txns_h24.get('buys', 0)
    sells = txns_h24.get('sells', 0)
    
    score = 0
    
    # Volume Score (0-30 points)
    if volume_h24 > 10000:
        score += 30
    elif volume_h24 > 5000:
        score += 20
    elif volume_h24 > 1000:
        score += 10
    elif volume_h24 > 500:
        score += 5
    
    # Volume/MCap Ratio Score (0-20 points)
    vol_mcap_ratio = (volume_h24 / mcap * 100) if mcap > 0 else 0
    if vol_mcap_ratio > 50:
        score += 20
    elif vol_mcap_ratio > 20:
        score += 15
    elif vol_mcap_ratio > 10:
        score += 10
    elif vol_mcap_ratio > 5:
        score += 5
    
    # Price Momentum Score (0-25 points)
    if price_change > 20:
        score += 25
    elif price_change > 10:
        score += 15
    elif price_change > 5:
        score += 10
    elif price_change > 0:
        score += 5
    
    # Liquidity Score (0-15 points)
    if liquidity > 10000:
        score += 15
    elif liquidity > 5000:
        score += 10
    elif liquidity > 2000:
        score += 5
    
    # Activity Score (0-10 points based on transactions)
    total_txns = buys + sells
    if total_txns > 100:
        score += 10
    elif total_txns > 50:
        score += 7
    elif total_txns > 20:
        score += 5
    elif total_txns > 10:
        score += 3
    
    # Buy/Sell Pressure (0-10 points)
    buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0
    if buy_ratio > 0.7:
        score += 10
    elif buy_ratio > 0.6:
        score += 7
    elif buy_ratio > 0.5:
        score += 5
    
    return score

def scan_alpha_gems():
    """Scan for alpha gems in 30k-200k range"""
    alpha_gems = []
    
    # Search queries to try
    queries = ["new", "trending", "meme", "solana", "ethereum", "base"]
    
    for query in queries:
        data = fetch_dexscreener_data(query)
        if data and 'pairs' in data:
            for pair in data['pairs']:
                mcap = pair.get('marketCap', 0)
                if 30000 <= mcap <= 200000:
                    base_token = pair.get('baseToken', {})
                    symbol = base_token.get('symbol', 'Unknown')
                    
                    # Avoid duplicates
                    if not any(g['symbol'] == symbol for g in alpha_gems):
                        txns_h24 = pair.get('txns', {}).get('h24', {})
                        
                        gem = {
                            'symbol': symbol,
                            'name': base_token.get('name', 'Unknown'),
                            'mcap': mcap,
                            'volume_24h': pair.get('volume', {}).get('h24', 0),
                            'price_change': pair.get('priceChange', {}).get('h24', 0),
                            'liquidity': pair.get('liquidity', {}).get('usd', 0),
                            'txns_h24': txns_h24,
                            'buys': txns_h24.get('buys', 0),
                            'sells': txns_h24.get('sells', 0),
                            'pair_address': pair.get('pairAddress'),
                            'dex_url': pair.get('url', ''),
                            'alpha_score': calculate_alpha_score(pair),
                            'chain': pair.get('chainId', '')
                        }
                        alpha_gems.append(gem)
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def generate_report():
    """Generate comprehensive alpha scanner report"""
    timestamp = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')
    
    print("💰 DEXSCREENER ALPHA SCANNER - SUB 30K-200K MCAP")
    print("=" * 70)
    print(f"Scan Time: {timestamp}")
    print(f"Market Cap Range: $30,000 - $200,000")
    print("=" * 70)
    print()
    
    alpha_gems = scan_alpha_gems()
    
    if alpha_gems:
        print(f"💎 Found {len(alpha_gems)} Alpha Gems")
        print("-" * 70)
        print()
        
        for i, gem in enumerate(alpha_gems[:8], 1):  # Show top 8
            vol_mcap_ratio = (gem['volume_24h'] / gem['mcap'] * 100) if gem['mcap'] > 0 else 0
            buy_ratio = (gem['buys'] / (gem['buys'] + gem['sells']) * 100) if (gem['buys'] + gem['sells']) > 0 else 0
            total_txns = gem['buys'] + gem['sells']
            
            print(f"{i}. 🎯 {gem['symbol']} ({gem['name']})")
            print(f"   ⚡ Alpha Score: {gem['alpha_score']}/110")
            print(f"   💰 Market Cap: ${gem['mcap']:,}")
            print(f"   📈 24h Volume: ${gem['volume_24h']:,}")
            print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
            print(f"   📊 Price Change: {gem['price_change']:.2f}%")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            print(f"   🔄 Transactions: {total_txns}/24h ({gem['buys']} buys, {gem['sells']} sells)")
            print(f"   📈 Buy/Sell Ratio: {buy_ratio:.1f}%")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 DexScreener: {gem['dex_url']}")
            print()
    else:
        print("⚠️ No alpha gems found in the 30k-200k range")
        print("Market conditions may be quiet or APIs are unresponsive")
        print()
    
    # Summary statistics
    if alpha_gems:
        avg_score = sum(g['alpha_score'] for g in alpha_gems) / len(alpha_gems)
        avg_mcap = sum(g['mcap'] for g in alpha_gems) / len(alpha_gems)
        avg_volume = sum(g['volume_24h'] for g in alpha_gems) / len(alpha_gems)
        
        print("📊 SUMMARY STATISTICS:")
        print("-" * 30)
        print(f"• Average Alpha Score: {avg_score:.1f}/110")
        print(f"• Average Market Cap: ${avg_mcap:,.0f}")
        print(f"• Average Volume: ${avg_volume:,.0f}")
        print(f"• Total Gems Found: {len(alpha_gems)}")
        print()
    
    print("🧠 ALPHA SCORE EXPLANATION:")
    print("-" * 30)
    print("• Volume (30 pts): Higher = more trader interest")
    print("• Vol/MCap Ratio (20 pts): Low mcap + high volume = undervalued")
    print("• Price Momentum (25 pts): Positive momentum = upside potential")
    print("• Liquidity (15 pts): Healthy pool = easier trading")
    print("• Activity (10 pts): Higher txns = more community")
    print("• Buy Pressure (10 pts): Buy ratio > 50% = accumulation")
    print()
    
    print("⚠️ Disclaimer: High volatility/risk - not financial advice")
    print("Always do your own research before investment decisions.")

if __name__ == "__main__":
    generate_report()