#!/usr/bin/env python3

import json
import sys

def analyze_memecoins(data):
    """Analyze memecoins from DexScreener API response"""
    
    # Filter for tokens in the target market cap range (30k-200k)
    target_tokens = []
    
    for pair in data.get('pairs', []):
        market_cap = pair.get('marketCap', 0)
        
        # Check if it's in our target range
        if market_cap and 30000 <= market_cap <= 200000:
            target_tokens.append({
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'market_cap': market_cap,
                'price': pair.get('priceUsd', 0),
                'volume_24h': pair.get('volume', {}).get('h24', 0),
                'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
                'chain': pair.get('chainId', 'Unknown'),
                'dex': pair.get('dexId', 'Unknown'),
                'url': pair.get('url', '')
            })
    
    # Sort by volume/market_cap ratio to find higher activity
    target_tokens.sort(key=lambda x: x.get('volume_24h', 0) / max(1, x.get('market_cap', 1)), reverse=True)
    
    return target_tokens

# Read the JSON data from stdin
if len(sys.argv) > 1:
    # Read from file
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
else:
    # Read from stdin
    try:
        data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # Handle the case where we have incomplete JSON from head command
        print("Error: Could not parse JSON data")
        sys.exit(1)

tokens = analyze_memecoins(data)

if tokens:
    print(f"\n🚀 Alpha Scanner Results ({len(tokens)} tokens found)\n")
    print("="*80)
    
    for i, token in enumerate(tokens, 1):
        print(f"\n{i}. {token['name']} ({token['symbol']})")
        print(f"   Market Cap: ${token['market_cap']:,.2f}")
        print(f"   Price: ${token['price']:.6f}")
        print(f"   24h Volume: ${token['volume_24h']:,.2f}")
        print(f"   Change 24h: {token['price_change_24h']:.1f}%")
        print(f"   Chain: {token['chain']} | DEX: {token['dex']}")
        print(f"   Link: {token['url']}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 Summary: Found {len(tokens)} potential alpha gems")
else:
    print("❌ No tokens found in the 30k-200k market cap range")