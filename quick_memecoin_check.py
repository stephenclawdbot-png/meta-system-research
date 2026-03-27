#!/usr/bin/env python3
import requests
import json
from datetime import datetime

print("🔍 Quick DexScreener Memecoin Scan")
print("=" * 60)

# Fetch data from DexScreener
base_url = 'https://api.dexscreener.com/latest/dex'
try:
    response = requests.get(f'{base_url}/search?q=solana', timeout=10)
    data = response.json()
    
    if 'pairs' not in data:
        print("❌ No pairs data received")
        exit(1)
        
    print(f"✅ Found {len(data['pairs'])} total pairs")
    
    # Filter by MCAP range
    filtered = [t for t in data['pairs'] if 1000 <= t.get('marketCap', 0) <= 1000000]
    print(f"💰 MCAP $1K-$1M: {len(filtered)} tokens")
    
    # Sort by MCAP
    filtered.sort(key=lambda x: x.get('marketCap', 0), reverse=True)
    
    # Show top 20
    print("\n📊 Top 20 Tokens by Market Cap:")
    print("-" * 80)
    for i, token in enumerate(filtered[:20]):
        base = token.get('baseToken', {})
        mcap = token.get('marketCap', 0)
        volume = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        
        # Calculate age
        age = "Unknown"
        if token.get('pairCreatedAt'):
            created_dt = datetime.fromtimestamp(token.get('pairCreatedAt') / 1000)
            age_days = (datetime.now() - created_dt).days
            age_hours = (datetime.now() - created_dt).seconds // 3600
            age = f"{age_days}d {age_hours}h"
        
        print(f"{i+1:2d}. {base.get('symbol', 'Unknown'):15} | MCAP: ${mcap:8,.0f} | Vol: ${volume:6,.0f} | "
              f"Δ%: {price_change:+6.1f}% | TXNs: {total_txns:4d} ({buy_ratio:4.1f}% buys) | Age: {age}")
        
except Exception as e:
    print(f"❌ Error: {e}")