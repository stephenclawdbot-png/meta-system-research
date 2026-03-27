#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import sys

def fetch_dexscreener_top_pairs():
    """Fetch top pairs from DexScreener API"""
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('pairs', [])
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def filter_gems(pairs):
    """Filter tokens in the 30k-200k mcap range with strong volume"""
    gems = []
    
    for pair in pairs:
        mcap = pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter by market cap
        if mcap < 30000 or mcap > 200000:
            continue
            
        # Filter out low volume tokens
        if volume_24h < 1000:
            continue
            
        # Calculate volume/mcap ratio
        vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
        
        # Filter for high volume/mcap ratio (healthy activity)
        if vol_mcap_ratio < 10:
            continue
            
        token_info = {
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
            'mcap': mcap,
            'volume_24h': volume_24h,
            'price': pair.get('priceUsd', 0),
            'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
            'url': pair.get('url', ''),
            'dex': pair.get('dexId', ''),
            'chain': pair.get('chainId', ''),
            'liquidity': pair.get('liquidity', {}).get('usd', 0),
            'txns': pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0),
            'buy_ratio': pair.get('txns', {}).get('h24', {}).get('buys', 0) / max(1, pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0)) if pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0) > 0 else 0
        }
        gems.append(token_info)
    
    return gems

def calculate_alpha_score(token):
    """Calculate comprehensive alpha score"""
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Score components
    vol_mcap_score = min(40, vol_mcap_ratio * 0.8)
    momentum_score = min(25, momentum * 2)
    volume_score = min(20, token['volume_24h'] / 10000)
    buy_ratio_score = token['buy_ratio'] * 15
    
    alpha_score = vol_mcap_score + momentum_score + volume_score + buy_ratio_score
    return min(100, alpha_score)

def main():
    print("🚀 QUICK MEMECOIN ALPHA SCANNER")
    print("=" * 50)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Volume Filter: Minimum $1k 24h volume")
    print("Vol/MCap Filter: Minimum 10% ratio")
    print()
    
    pairs = fetch_dexscreener_top_pairs()
    if not pairs:
        print("❌ No data returned from DexScreener API")
        return
    
    gems = filter_gems(pairs)
    
    if not gems:
        print("❌ No memecoins meeting criteria found")
        print("Market may be quiet or filters too strict")
        return
    
    # Calculate scores and sort
    for gem in gems:
        gem['alpha_score'] = calculate_alpha_score(gem)
    gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"🔥 TOP ALPHA GEMS DETECTED ({len(gems)} total)")
    print("=" * 60)
    
    for i, gem in enumerate(gems[:8], 1):
        vol_mcap_ratio = (gem['volume_24h'] / gem['mcap']) * 100 if gem['mcap'] > 0 else 0
        
        print(f"🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        print(f"   📛 Name: {gem['name']}")
        print(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {gem['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   🤝 Buy Ratio: {gem['buy_ratio'] * 100:.1f}%")
        print(f"   🔄 Transactions: {gem['txns']}")
        print(f"   💧 Liquidity: ${gem['liquidity']:,.0f}")
        print(f"   🌐 Dex: {gem['dex']} | Chain: {gem['chain']}")
        print(f"   🔗 {gem['url']}")
        print()
    
    # Summary
    if gems:
        print("📊 SCAN SUMMARY:")
        print("-" * 20)
        print(f"Total Gems Found: {len(gems)}")
        print(f"Highest Alpha Score: {gems[0]['alpha_score']:.1f}/100")
        print(f"Average MCap: ${sum(g['mcap'] for g in gems)/len(gems):,.0f}")
        print(f"Average Volume: ${sum(g['volume_24h'] for g in gems)/len(gems):,.0f}")
        print(f"Average Vol/MCap Ratio: {sum((g['volume_24h']/g['mcap'])*100 for g in gems)/len(gems):.1f}%")
    print("\n⚠️ HIGH RISK - Do your own research!")

if __name__ == "__main__":
    main()