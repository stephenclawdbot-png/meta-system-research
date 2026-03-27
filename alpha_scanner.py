#!/usr/bin/env python3
import json
import re

# Load the response from web_fetch
def process_dexscreener_data(text):
    # Extract JSON from the wrapped content
    match = re.search(r'<<<EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>\n.*?\n---\n(.*)\n<<<END_EXTERNAL_UNTRUSTED_CONTENT', text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError:
            return None
    return None

def analyze_alpha_gems(data, min_mcap=30000, max_mcap=200000):
    if not data:
        return []
    
    gems = []
    
    for pair in data.get('pairs', []):
        # Skip non-Solana tokens
        if pair.get('chainId') != 'solana':
            continue
            
        mcap = pair.get('marketCap')
        if not mcap or not (min_mcap <= mcap <= max_mcap):
            continue
            
        # Get transaction data
        txns_24h = pair.get('txns', {}).get('h24', {})
        buy_count = txns_24h.get('buys', 0)
        sell_count = txns_24h.get('sells', 0)
        total_txns = buy_count + sell_count
        
        # Calculate buy ratio
        buy_ratio = buy_count / total_txns if total_txns > 0 else 0
        
        # Check volume
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Basic alpha scoring
        alpha_score = 0
        
        # Volume score (max 25 points)
        if volume_24h > 100000:  # High volume
            alpha_score += 25
        elif volume_24h > 50000:
            alpha_score += 15
        elif volume_24h > 10000:
            alpha_score += 10
            
        # Buy pressure score (max 15 points)
        if buy_ratio > 0.7:  # Strong buy pressure
            alpha_score += 15
        elif buy_ratio > 0.6:
            alpha_score += 10
        elif buy_ratio > 0.55:
            alpha_score += 5
            
        # Transaction velocity score (max 5 points)
        if total_txns > 1000:  # High velocity
            alpha_score += 5
        elif total_txns > 500:
            alpha_score += 3
            
        gems.append({
            'symbol': pair.get('baseToken', {}).get('symbol'),
            'name': pair.get('baseToken', {}).get('name'),
            'mcap': mcap,
            'price': pair.get('priceUsd'),
            'volume_24h': volume_24h,
            'price_change_24h': pair.get('priceChange', {}).get('h24'),
            'buy_ratio': buy_ratio,
            'total_txns': total_txns,
            'url': pair.get('url'),
            'dex': pair.get('dexId'),
            'alpha_score': alpha_score,
            'age': None  # Would need creation timestamp
        })
    
    # Sort by alpha score descending
    gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return gems

# Example usage
def main():
    # Read from stdin
    import sys
    text = sys.stdin.read()
    
    data = process_dexscreener_data(text)
    gems = analyze_alpha_gems(data)
    
    print(f"\n🎯 Alpha Scanner Results - {len(gems)} gems found in 30k-200k range\n")
    print("Top Alpha Candidates (sorted by alpha score):")
    print("-" * 80)
    
    for i, gem in enumerate(gems[:15], 1):
        print(f"\n{i}. {gem['symbol']} - {gem['name']}")
        print(f"   Alpha Score: {gem['alpha_score']}/45")
        print(f"   Market Cap: ${gem['mcap']:,}")
        print(f"   24h Volume: ${gem['volume_24h']:,}")
        print(f"   Buy Ratio: {gem['buy_ratio']:.1%}")
        print(f"   Total Txns (24h): {gem['total_txns']}")
        if gem['price_change_24h']:
            print(f"   24h Price Change: {gem['price_change_24h']}%")
        print(f"   DEX: {gem['dex']}")
        print(f"   URL: {gem['url']}")

if __name__ == "__main__":
    main()