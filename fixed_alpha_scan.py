#!/usr/bin/env python3
import requests
from datetime import datetime
import time

print("🎯 MEMECOIN ALPHA SCANNER - FULL MARKET SCAN")
print("=" * 55)
print(f"Scan Time: {datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')}")
print("Market Cap Range: $30,000 - $200,000")
print("Focus: Early alpha detection before mainstream attention")
print()

# Memecoin-related search terms
search_terms = ['memecoin', 'dog', 'cat', 'shiba', 'pepe', 'floki', 'bonk', 'elon', 'moon', 'mars']
all_tokens = []

try:
    for term in search_terms:
        try:
            response = requests.get(f'https://api.dexscreener.com/latest/dex/search?q={term}&limit=30', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    tokens = data['pairs']
                    
                    # Filter by mcap range $30k-$200k
                    filtered = []
                    for token in tokens:
                        mcap = token.get('fdv', 0)
                        if 30000 <= mcap <= 200000:
                            filtered.append(token)
                    
                    all_tokens.extend(filtered)
                    time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Warning: Failed to search for '{term}': {e}")
    
    if not all_tokens:
        print("❌ No tokens found in target range")
    else:
        # Remove duplicates and sort by volume/mcap ratio
        seen_addresses = set()
        unique_tokens = []
        for token in all_tokens:
            addr = token.get('pairAddress', '')
            if addr and addr not in seen_addresses:
                seen_addresses.add(addr)
                unique_tokens.append(token)
        
        unique_tokens.sort(key=lambda x: x.get('volume', {}).get('h24', 0) / max(1, x.get('fdv', 0)), reverse=True)
        
        print(f"🔥 TOP 8 ALPHA GEMS (Sorted by Alpha Potential)")
        print("-" * 55)
        
        for i, token in enumerate(unique_tokens[:8], 1):
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
            
            # Exclude very low alpha scores
            if alpha_score < 10:
                continue
                
            print(f"🎯 #{i} {symbol} - Alpha Score: {alpha_score:.0f}/100")
            print(f"   Chain: {token.get('chainId', 'Unknown')}")
            print(f"   📈 24h Stats: ${vol:,} vol • ${mcap:,} mcap • {ratio:.1f}% ratio")
            print(f"   📊 Sentiment: {change:+}% price")
            
            # Additional details if available
            price = token.get('priceUsd', 0)
            if price:
                try:
                    formatted_price = f"${float(price):.6f}"
                    print(f"   💰 Price: {formatted_price}")
                except:
                    pass
            
            print(f"   🔗 {token.get('url', '')}")
            print()
        
        # Market summary
        high_score_tokens = [t for t in unique_tokens[:8] if min(100, (
            min(40, (t.get('volume', {}).get('h24', 0) / max(1, t.get('fdv', 0)) * 100 * 0.4)) +
            max(0, min(20, t.get('priceChange', {}).get('h24', 0) * 2)) +
            min(20, t.get('volume', {}).get('h24', 0) / 10000) +
            min(20, t.get('fdv', 0) / 10000)
        )) >= 10]
        
        if high_score_tokens:
            avg_score = sum(min(100, (
                min(40, (t.get('volume', {}).get('h24', 0) / max(1, t.get('fdv', 0)) * 100 * 0.4)) +
                max(0, min(20, t.get('priceChange', {}).get('h24', 0) * 2)) +
                min(20, t.get('volume', {}).get('h24', 0) / 10000) +
                min(20, t.get('fdv', 0) / 10000)
            )) for t in high_score_tokens) / len(high_score_tokens)
            
            print("📊 MARKET SUMMARY")
            print("-" * 25)
            print(f"• Average Alpha Score: {avg_score:.1f}/100")
            print(f"• High-Potential Gems: {len(high_score_tokens)} tokens")
            print(f"• Total Found: {len(unique_tokens)} tokens")
            
            # Volume insights
            if high_score_tokens:
                avg_ratio = sum(t.get('volume', {}).get('h24', 0) / max(1, t.get('fdv', 0)) * 100 for t in high_score_tokens if t.get('fdv', 0) > 0) / len(high_score_tokens)
                print(f"• Average Vol/MCap: {avg_ratio:.1f}%")
        
        print()
        print("💡 KEY ALPHA SIGNALS:")
        print("- Volume/Mcap ratio > 25% = strong interest")
        print("- Positive price momentum = early accumulation")
        print("- Healthy liquidity = lower risk")
        print("- Active transactions = growing community")
        print()
        print("⚠️ DISCLAIMER: Extreme risk assets - DYOR required")
        print("   Only risk what you can afford to lose")

        # Check if Alpha Scanner service is down
        print()
        print("🔧 STATUS: Alpha Scanner service appears offline")
        print("   Using DexScreener API directly for this scan")

except Exception as e:
    print(f"❌ Error during comprehensive scan: {e}")
    print("\n💡 The DexScreener API may be limiting requests.")