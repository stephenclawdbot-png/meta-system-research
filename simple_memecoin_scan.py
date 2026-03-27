#!/usr/bin/env python3
"""
Simple DexScreener scan for memecoins in 30k-200k range
"""

import requests
from datetime import datetime

# DexScreener API endpoint
url = "https://api.dexscreener.com/latest/dex/search?q=solana"

print("🚀 DexScreener Memecoin Scanner")
print("💰 Target Market Cap: $30k - $200k")
print(f"📍 Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 50)

try:
    # Fetch data from DexScreener
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        exit(1)
    
    data = response.json()
    
    if 'pairs' not in data:
        print("❌ No pairs data found")
        exit(1)
    
    # Filter tokens in our target range
    filtered_tokens = []
    for token in data['pairs']:
        mcap = token.get('marketCap', 0)
        if mcap and 30000 <= mcap <= 200000:
            filtered_tokens.append(token)
    
    # Sort by market cap
    filtered_tokens.sort(key=lambda x: x.get('marketCap', 0), reverse=False)
    
    print(f"✅ Found {len(filtered_tokens)} tokens in target range:")
    
    if filtered_tokens:
        for i, token in enumerate(filtered_tokens[:10], 1):  # Show top 10
            base_token = token.get('baseToken', {})
            symbol = base_token.get('symbol', 'Unknown')
            name = base_token.get('name', 'Unknown')
            mcap = token.get('marketCap', 0)
            price = token.get('priceUsd', 0)
            volume = token.get('volume', {}).get('h24', 0)
            price_change = token.get('priceChange', {}).get('h24', 0)
            
            # Calculate token age
            pair_created_at = token.get('pairCreatedAt', 0)
            age_hours = "Unknown"
            if pair_created_at:
                age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
                age_hours = f"{age_hours:.1f}h"
            
            print(f"{i}. 💎 {symbol} ({name})")
            print(f"   📊 MCAP: ${int(mcap):,}")
            print(f"   💰 Price: ${float(price):.8f}")
            print(f"   📈 24h Vol: ${int(volume):,}")
            print(f"   📈 24h Chg: {float(price_change):+.2f}%")
            print(f"   ⏱️ Age: {age_hours}")
            
            # Show transaction data if available
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            if total_txns > 0:
                buy_ratio = (buys / total_txns) * 100
                print(f"   🔄 Txns: {total_txns} (Buys: {buys}, Ratio: {buy_ratio:.1f}%)")
            
            # Show DexScreener link
            pair_addr = token.get('pairAddress', '')
            if pair_addr:
                print(f"   🔗 https://dexscreener.com/solana/{pair_addr}")
            
            print("-" * 30)
    else:
        print("📭 No tokens found in the target range at this time.")
        print("💡 Try broadening the search or checking again later.")

except Exception as e:
    print(f"❌ Error: {e}")