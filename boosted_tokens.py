#!/usr/bin/env python3
import requests
import json

print("🔍 DexScreener Boosted Tokens Scan")
print("=" * 60)

try:
    response = requests.get('https://api.dexscreener.com/token-boosts/latest/v1', timeout=10)
    data = response.json()
    
    print(f"📊 Raw response type: {type(data)}")
    
    if isinstance(data, list):
        sol_tokens = [t for t in data if t.get('chainId') == 'solana' and t.get('marketCap', 0) > 0]
        print(f"✅ Found {len(sol_tokens)} boosted Solana tokens:\n")
        
        # Sort by market cap
        sol_tokens.sort(key=lambda x: x.get('marketCap', 0), reverse=True)
        
        target_count = 0
        for t in sol_tokens:
            symbol = t.get('symbol', 'Unknown')
            name = t.get('name', 'Unknown') 
            market_cap = t.get('marketCap', 0)
            volume_24h = t.get('volume24h', 0)
            price_change = t.get('priceChange24h', 0)
            
            # Check if it's in our target range
            if 1000 <= market_cap <= 500000:
                target_count += 1
                print(f"🎯 TARGET: {symbol:12} - {name:35} - MCAP: ${market_cap:9,} - Vol: ${volume_24h:9,} - Δ%: {price_change:+6.1f}%")
            else:
                print(f"   {symbol:12} - {name:35} - MCAP: ${market_cap:9,} - Vol: ${volume_24h:9,} - Δ%: {price_change:+6.1f}%")
        
        print(f"\n🎯 Found {target_count} tokens in target range ($1K-$500K MCAP)")
        
    else:
        print("❌ Unexpected response format - not a list")
        print(f"Response sample: {str(data)[:500]}")
        
except Exception as e:
    print(f"❌ Error: {e}")