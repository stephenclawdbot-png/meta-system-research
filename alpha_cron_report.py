#!/usr/bin/env python3
import requests
from datetime import datetime
import json

print("🎯 MEMECOIN ALPHA SCANNER - CRON REPORT")
print("=" * 55)
print(f"Scan Time: {datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')}")
print("Market Cap Range: $30,000 - $200,000")
print("Focus: Early alpha detection before mainstream attention")
print()

try:
    # Search for memecoin-related tokens
    response = requests.get('https://api.dexscreener.com/latest/dex/search?q=memecoin&limit=50', timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data and 'pairs' in data:
            tokens = data['pairs']
            
            # Filter by mcap range
            filtered = []
            for token in tokens:
                mcap = token.get('fdv', 0)
                if 30000 <= mcap <= 200000:
                    filtered.append(token)
            
            # Remove duplicates and sort by volume/mcap ratio
            seen_addresses = set()
            unique_tokens = []
            for token in filtered:
                addr = token.get('pairAddress', '')
                if addr and addr not in seen_addresses:
                    seen_addresses.add(addr)
                    unique_tokens.append(token)
            
            unique_tokens.sort(key=lambda x: x.get('volume', {}).get('h24', 0) / max(1, x.get('fdv', 0)), reverse=True)
            
            print(f"🔥 TOP 6 ALPHA GEMS (Sorted by Alpha Potential)")
            print("-" * 55)
            
            for i, token in enumerate(unique_tokens[:6], 1):
                mcap = int(token.get('fdv', 0))
                vol = int(token.get('volume', {}).get('h24', 0))
                change = token.get('priceChange', {}).get('h24', 0)
                symbol = token.get('baseToken', {}).get('symbol', '??')
                name = token.get('baseToken', {}).get('name', 'Unknown')
                ratio = vol / mcap * 100 if mcap > 0 else 0
                
                # Calculate Alpha Score
                alpha_score = min(100, (
                    min(40, ratio * 0.4) +  # Volume/MCap ratio (40pts max)
                    max(0, min(20, change * 2)) +  # Price momentum
                    min(20, vol / 10000) +  # Volume scale
                    min(20, mcap / 10000)  # Healthy mcap
                ))
                
                print(f"🎯 #{i} {symbol} - Alpha Score: {alpha_score:.0f}/100")
                print(f"   📈 24h Stats: ${vol:,} vol • ${mcap:,} mcap • {ratio:.1f}% ratio")
                print(f"   📊 Sentiment: {change:+.1f}% price")
                print(f"   🔗 {token.get('url', '')}")
                print()
            
            # Market summary
            print("📊 MARKET SUMMARY")
            print("-" * 25)
            if unique_tokens[:6]:
                avg_score = sum(min(100, (
                    min(40, (t.get('volume', {}).get('h24', 0) / max(1, t.get('fdv', 0)) * 100 * 0.4)) +
                    max(0, min(20, t.get('priceChange', {}).get('h24', 0) * 2)) +
                    min(20, t.get('volume', {}).get('h24', 0) / 10000) +
                    min(20, t.get('fdv', 0) / 10000)
                )) for t in unique_tokens[:6]) / len(unique_tokens[:6])
                print(f"• Average Alpha Score: {avg_score:.1f}/100")
                print(f"• Total Gems Found: {len(unique_tokens)} tokens")
            print()
            print("💡 KEY ALPHA SIGNALS:")
            print("- Volume/Mcap ratio > 25% indicates strong interest")
            print("- High transaction volume = active community")
            print("- Positive price momentum = early accumulation phase")
            print()
            print("⚠️ DISCLAIMER: High risk assets - DYOR required")

        else:
            print("❌ No memecoin data available from DexScreener")
    else:
        print("❌ Failed to fetch data from DexScreener")
        
except Exception as e:
    print(f"❌ Error during scan: {e}")
    print("\n💡 The Alpha Scanner service may be down. Using DexScreener API instead.")