#!/usr/bin/env python3
"""
DexScreener Alpha Scanner - Focus on 30k-200k Market Cap Range
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

def analyze_alpha_gems():
    """Analyze DexScreener data for alpha gems in 30k-150k range"""
    alpha_gems = []
    
    # Check new tokens
    new_data = fetch_dexscreener_data("new")
    if new_data:
        for pair in new_data.get('pairs', []):
            mcap = pair.get('fdv', 0)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            
            # Apply 30k-150k market cap filter
            if 30000 <= mcap <= 150000:
                # Calculate alpha score
                score = calculate_alpha_score(pair)
                
                txns_h24 = pair.get('txns', {}).get('h24', {})
                alpha_gems.append({
                    'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                    'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                    'liquidity': pair.get('liquidity', {}).get('usd', 0),
                    'txns_24h': pair.get('txns', {}),
                    'buyers': txns_h24.get('buys', 0),
                    'sellers': txns_h24.get('sells', 0),
                    'pair_address': pair.get('pairAddress'),
                    'dex_url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                    'alpha_score': score,
                    'age': pair.get('pairCreatedAt', ''),
                    'chain': pair.get('chainId', '')
                })
    
    # Check trending tokens
    trending_data = fetch_dexscreener_data("trending")
    if trending_data:
        for pair in trending_data.get('pairs', []):
            mcap = pair.get('fdv', 0)
            volume_24h = pair.get('volume', {}).get('h24', 0)
            
            # Apply 30k-150k market cap filter
            if 30000 <= mcap <= 150000:
                # Avoid duplicates
                symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                if not any(g['symbol'] == symbol for g in alpha_gems):
                    score = calculate_alpha_score(pair)
                    
                    txns_h24 = pair.get('txns', {}).get('h24', {})
                    alpha_gems.append({
                        'symbol': symbol,
                        'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': volume_24h,
                        'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                        'liquidity': pair.get('liquidity', {}).get('usd', 0),
                        'txns_24h': pair.get('txns', {}),
                        'buyers': txns_h24.get('buys', 0),
                        'sellers': txns_h24.get('sells', 0),
                        'pair_address': pair.get('pairAddress'),
                        'dex_url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                        'alpha_score': score,
                        'age': pair.get('pairCreatedAt', ''),
                        'chain': pair.get('chainId', '')
                    })
    
    # Check various crypto-related queries to broaden search
    search_terms = ["solana", "ethereum", "base", "arbitrum", "bnb", "meme", "coin"]
    for term in search_terms:
        search_data = fetch_dexscreener_data(term)
        if search_data:
            for pair in search_data.get('pairs', []):
                mcap = pair.get('fdv', 0)
                volume_24h = pair.get('volume', {}).get('h24', 0)
                
                # Apply 30k-200k market cap filter
                if 30000 <= mcap <= 200000:
                    # Avoid duplicates
                    symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                    if not any(g['symbol'] == symbol for g in alpha_gems):
                        score = calculate_alpha_score(pair)
                        
                        txns_h24 = pair.get('txns', {}).get('h24', {})
                        alpha_gems.append({
                            'symbol': symbol,
                            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                            'mcap': mcap,
                            'volume_24h': volume_24h,
                            'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                            'liquidity': pair.get('liquidity', {}).get('usd', 0),
                            'txns_24h': pair.get('txns', {}),
                            'buyers': txns_h24.get('buys', 0),
                            'sellers': txns_h24.get('sells', 0),
                            'pair_address': pair.get('pairAddress'),
                            'dex_url': f"https://dexscreener.com/{pair.get('chainId', '')}/{pair.get('pairAddress', '')}",
                            'alpha_score': score,
                            'age': pair.get('pairCreatedAt', ''),
                            'chain': pair.get('chainId', '')
                        })
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def calculate_alpha_score(pair):
    """Calculate alpha score based on multiple factors"""
    score = 0
    mcap = pair.get('fdv', 0)
    volume = pair.get('volume', {}).get('h24', 0)
    price_change = pair.get('priceChange', {}).get('h24', 0)
    liquidity = pair.get('liquidity', {}).get('usd', 0)
    txns = pair.get('txns', {}).get('h24', 0)
    buyers = pair.get('buys', 0)
    sellers = pair.get('sells', 0)
    
    # Volume Score (0-30 points)
    if volume > 10000:
        score += 30
    elif volume > 5000:
        score += 20
    elif volume > 1000:
        score += 10
    elif volume > 500:
        score += 5
    
    # Volume/MCap Ratio Score (0-20 points)
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
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
    txns_h24 = txns.get('h24', {}) if isinstance(txns, dict) else {}
    buy_count = txns_h24.get('buys', 0)
    sell_count = txns_h24.get('sells', 0)
    total_txns = buy_count + sell_count
    
    if total_txns > 100:
        score += 10
    elif total_txns > 50:
        score += 7
    elif total_txns > 20:
        score += 5
    elif total_txns > 10:
        score += 3
    
    # Buy/Sell Pressure (0-10 points)
    buy_ratio = buy_count / (buy_count + sell_count) if (buy_count + sell_count) > 0 else 0
    if buy_ratio > 0.7:
        score += 10
    elif buy_ratio > 0.6:
        score += 7
    elif buy_ratio > 0.5:
        score += 5
    
    return score

def generate_report():
    """Generate comprehensive alpha scanner report"""
    timestamp = datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')
    
    print(f"💰 DEXSCREENER ALPHA SCANNER - SUB 30K-150K MCAP")
    print("=" * 70)
    print(f"Scan Time: {timestamp}")
    print(f"Market Cap Range: $30,000 - $150,000")
    print("=" * 70)
    print()
    
    alpha_gems = analyze_alpha_gems()
    
    if alpha_gems:
        print(f"💎 Found {len(alpha_gems)} Alpha Gems")
        print("-" * 70)
        print()
        
        for gem in alpha_gems[:10]:  # Show top 10
            vol_mcap_ratio = (gem['volume_24h'] / gem['mcap'] * 100) if gem['mcap'] > 0 else 0
            buy_sell_ratio = gem['buyers'] / (gem['buyers'] + gem['sellers']) if (gem['buyers'] + gem['sellers']) > 0 else 0
            
            print(f"🎯 {gem['symbol']} ({gem['name']})")
            print(f"   ⚡ Alpha Score: {gem['alpha_score']}/110")
            print(f"   💰 Market Cap: ${gem['mcap']:,}")
            print(f"   📈 24h Volume: ${gem['volume_24h']:,}")
            print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
            print(f"   📊 Price Change: {gem['price_change_24h']:.2f}%")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            buy_count = gem.get('buyers', 0) if isinstance(gem.get('buyers'), int) else 0
            sell_count = gem.get('sellers', 0) if isinstance(gem.get('sellers'), int) else 0
            total_txns = buy_count + sell_count
            actual_buy_ratio = buy_count / (buy_count + sell_count) if (buy_count + sell_count) > 0 else 0
            print(f"   🔄 Transactions: {total_txns}/24h ({buy_count} buys, {sell_count} sells)")
            print(f"   📈 Buy/Sell Ratio: {actual_buy_ratio:.1%}")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 DexScreener: {gem['dex_url']}")
            print()
    else:
        print("⚠️ No alpha gems found in the 30k-150k range")
        print("Market conditions may be quiet or filters too strict")
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
    
    print("⚠️ Disclaimer: Alpha scanner results only. DYOR before investing.")
    print("Market conditions change rapidly. High risk micro-cap space.")

if __name__ == "__main__":
    generate_report()