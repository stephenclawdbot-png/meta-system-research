#!/usr/bin/env python3
import requests
import json
from datetime import datetime

print("🎯 Memecoin Alpha Scanner Report")
print("=" * 60)
print(f"📅 Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("💰 Target Range: $30,000 - $200,000 Market Cap")
print("")

try:
    # Fetch data from DexScreener
    response = requests.get('https://api.dexscreener.com/latest/dex/search?q=solana', timeout=10)
    data = response.json()
    
    pairs = data.get('pairs', [])
    print(f"📊 Found {len(pairs)} total pairings")
    
    # Filter for our target MCAP range
    target_tokens = [p for p in pairs if 30000 <= p.get('marketCap', 0) <= 200000]
    
    print(f"\n🎯 Found {len(target_tokens)} tokens in target MCAP range:")
    print("-" * 80)
    
    if target_tokens:
        # Sort by MCAP (lowest first - most potential)
        target_tokens.sort(key=lambda x: x.get('marketCap', 0))
        
        for i, token in enumerate(target_tokens, 1):
            base = token.get('baseToken', {})
            symbol = base.get('symbol', 'Unknown')
            name = base.get('name', 'Unknown')
            mcap = token.get('marketCap', 0)
            volume_24h = token.get('volume', {}).get('h24', 0)
            price_change = token.get('priceChange', {}).get('h24', 0)
            
            # Calculate transaction metrics
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Token age
            age_str = "Unknown"
            if token.get('pairCreatedAt'):
                created_dt = datetime.fromtimestamp(token.get('pairCreatedAt') / 1000)
                age_hours = (datetime.now() - created_dt).total_seconds() / 3600
                age_str = f"{age_hours:.1f}h"
            
            print(f"{i}. {symbol}: {name}")
            print(f"   💰 Market Cap: ${mcap:,}")
            print(f"   📈 24h Volume: ${volume_24h:,}")
            print(f"   📊 Price Change: {price_change:+.1f}%")
            print(f"   🔄 Transactions: {total_txns:,} (Buys: {buys} / Ratio: {buy_ratio:.1f}%)")
            print(f"   ⏱️ Age: {age_str}")
            
            # DexScreener link
            pair_address = token.get('pairAddress', '')
            if pair_address:
                print(f"   🔗 DexScreener: https://dexscreener.com/solana/{pair_address}")
            print("-" * 40)
    else:
        print("📭 No opportunities found in target range at this time")
        print("")
        print("🔍 Checking broader range for comparison...")
        
        # Show tokens just above and below our range
        below_range = [p for p in pairs if 1000 <= p.get('marketCap', 0) < 30000]
        above_range = [p for p in pairs if 200000 < p.get('marketCap', 0) <= 1000000]
        
        print(f"   Below range ($1K-$30K): {len(below_range)} tokens")
        print(f"   Above range ($200K-$1M): {len(above_range)} tokens")

except Exception as e:
    print(f"❌ Scanner error: {e}")

print("\n✅ Scan complete")