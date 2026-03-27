#!/usr/bin/env python3
"""
Alpha Scanner with 30k-150k Market Cap Focus
Filters results from DexScreener API for specific range
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_data():
    """Fetch data from dexscreener API"""
    try:
        # DexScreener API endpoint for trending/new tokens
        url = "https://api.dexscreener.com/latest/dex/tokens/trending"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return None

def filter_30k_150k_gems(data):
    """Filter gems in 30k-150k market cap range"""
    if not data or 'pairs' not in data:
        return []
    
    gems = []
    for pair in data['pairs']:
        mcap = pair.get('marketCap')
        
        if mcap and 30000 <= mcap <= 150000:
            volume = pair.get('volume', {}).get('h24', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            txns_24h = pair.get('txns', {}).get('h24', {})
            buy_count = txns_24h.get('buys', 0)
            sell_count = txns_24h.get('sells', 0)
            total_txns = buy_count + sell_count
            buy_ratio = buy_count / total_txns if total_txns > 0 else 0
            
            gems.append({
                'symbol': pair.get('baseToken', {}).get('symbol'),
                'name': pair.get('baseToken', {}).get('name'),
                'mcap': mcap,
                'volume': volume,
                'price_change': price_change,
                'buy_ratio': buy_ratio,
                'total_txns': total_txns,
                'url': pair.get('url'),
                'chain': pair.get('chainId'),
                'dex': pair.get('dexId'),
                'liquidity': pair.get('liquidity', {}).get('usd', 0)
            })
    
    # Sort by market cap (closest to 30k first for potential upside)
    gems.sort(key=lambda x: abs(x['mcap'] - 30000))
    return gems

def calculate_alpha_score(gem):
    """Calculate alpha score based on multiple factors"""
    score = 0
    
    # Volume score (max 25 points)
    if gem['volume'] > 5000:
        score += 25
    elif gem['volume'] > 1000:
        score += 15
    elif gem['volume'] > 500:
        score += 10
    elif gem['volume'] > 100:
        score += 5
    
    # Price momentum score (max 20 points)
    if gem['price_change'] > 5:
        score += 20
    elif gem['price_change'] > 2:
        score += 15
    elif gem['price_change'] > 0:
        score += 10
    elif gem['price_change'] > -2:
        score += 5
    
    # Buy pressure score (max 15 points)
    if gem['buy_ratio'] > 0.6:
        score += 15
    elif gem['buy_ratio'] > 0.55:
        score += 10
    elif gem['buy_ratio'] > 0.5:
        score += 5
    
    # Transaction activity score (max 10 points)
    if gem['total_txns'] > 50:
        score += 10
    elif gem['total_txns'] > 20:
        score += 7
    elif gem['total_txns'] > 10:
        score += 4
    elif gem['total_txns'] > 5:
        score += 2
    
    # Liquidity score (max 10 points)
    if gem['liquidity'] > 10000:
        score += 10
    elif gem['liquidity'] > 5000:
        score += 7
    elif gem['liquidity'] > 2000:
        score += 5
    elif gem['liquidity'] > 1000:
        score += 3
    
    return score

def main():
    print("🧠 ALPHA SCANNER - 30K-150K MCAP FOCUS")
    print("=" * 60)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %H:%M %p')} (Asia/Manila)")
    print("Market Cap Range: $30,000 - $150,000")
    print("=" * 60)
    
    data = fetch_dexscreener_data()
    gems = filter_30k_150k_gems(data)
    
    print(f"\n💰 Found {len(gems)} Alpha Gems in Target Range")
    print("-" * 50)
    
    if gems:
        # Calculate alpha scores
        for gem in gems:
            gem['alpha_score'] = calculate_alpha_score(gem)
        
        # Sort by alpha score descending
        gems.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        for i, gem in enumerate(gems[:10], 1):
            print(f"\n🎯 #{i} {gem['symbol']} - {gem['name']}")
            print(f"   ⚡ Alpha Score: {gem['alpha_score']}/85")
            print(f"   💰 Market Cap: ${gem['mcap']:,}")
            print(f"   📈 24h Volume: ${gem['volume']:,}")
            print(f"   📊 Price Change: {gem['price_change']}%")
            print(f"   📈 Buy/Sell Ratio: {gem['buy_ratio']:.1%}")
            print(f"   🔄 Transactions: {gem['total_txns']}/24h")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 DexScreener: {gem['url']}")
            
        print(f"\n📊 SUMMARY:")
        print("-" * 30)
        avg_score = sum(g['alpha_score'] for g in gems) / len(gems)
        print(f"• Average Alpha Score: {avg_score:.1f}/85")
        print(f"• Total Tokens Found: {len(gems)}")
        print(f"• Average Market Cap: ${sum(g['mcap'] for g in gems) / len(gems):,.0f}")
        print(f"• Average Volume: ${sum(g['volume'] for g in gems) / len(gems):,.0f}")
        
    else:
        print("❌ No tokens matching 30k-150k criteria found")
    
    print(f"\n⚠️ Disclaimer: Alpha scanner results only. DYOR before investing.")
    print("Market conditions change rapidly. High risk micro-cap space.")

if __name__ == "__main__":
    main()