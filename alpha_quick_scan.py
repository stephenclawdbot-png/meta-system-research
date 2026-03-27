#!/usr/bin/env python3
import json
import sys
import requests

def scan_category(category):
    url = f"https://api.dexscreener.com/latest/dex/search?q={category}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            pairs = data.get("pairs", [])
            
            tokens = []
            for token in pairs:
                mcap = token.get("fdv", 0)
                if 30000 <= mcap <= 200000:
                    volume = token.get("volume", {}).get("h24", 0)
                    if volume > 100:  # Filter for some minimum volume
                        alpha_score = min(100, (volume / mcap * 100) * 0.6) if mcap > 0 else 0
                        tokens.append({
                            "symbol": token.get("baseToken", {}).get("symbol", "Unknown"),
                            "mcap": mcap,
                            "volume": volume,
                            "vol_ratio": volume / mcap * 100 if mcap > 0 else 0,
                            "percent_change": token.get("priceChange", {}).get("h24", 0),
                            "alpha_score": alpha_score,
                            "url": token.get("url", ""),
                            "chain": token.get("chainId", "")
                        })
            
            tokens.sort(key=lambda x: x["alpha_score"], reverse=True)
            return tokens[:10]
        
    except Exception as e:
        print(f"Error scanning {category}: {e}")
        return []

# Categories to scan
categories = ["memecoin", "dog", "cat", "bonk", "pepe", "ai", "meme", "solana", "sam", "eleslo"]

print("🧠 MEMECOIN ALPHA SCANNER - 30K-200K MCAP")
print("=" * 60)
print("Scan Time: Wednesday, March 4th, 2026 — 8:52 AM (Asia/Manila)")
print("Target Range: $30k - $200k Market Cap")
print()

all_tokens = []

for category in categories:
    tokens = scan_category(category)
    if tokens:
        print(f"{category.upper()}: {len(tokens)} tokens")
        all_tokens.extend(tokens)

# Remove duplicates
seen_symbols = set()
unique_tokens = []
for token in all_tokens:
    if token['symbol'] not in seen_symbols:
        seen_symbols.add(token['symbol'])
        unique_tokens.append(token)

# Sort by alpha score
unique_tokens.sort(key=lambda x: x["alpha_score"], reverse=True)

print(f"\n🔥 TOP ALPHA MEMECOINS DETECTED (Top {len(unique_tokens[:10])})")
print("-" * 50)

for i, token in enumerate(unique_tokens[:10], 1):
    print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']:.1f}/100")
    print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol24h: ${token['volume']:,.0f}")
    print(f"   📈 24h Change: {token['percent_change']:.1f}% | Vol/MCap: {token['vol_ratio']:.1f}%")
    print(f"   🌐 Chain: {token['chain']}")
    print(f"   🔗 {token['url']}")
    print()

if unique_tokens:
    avg_mcap = sum(t['mcap'] for t in unique_tokens[:10]) / len(unique_tokens[:10])
    avg_volume = sum(t['volume'] for t in unique_tokens[:10]) / len(unique_tokens[:10])
    avg_vol_mcap = sum(t['vol_ratio'] for t in unique_tokens[:10]) / len(unique_tokens[:10])
    
    print("📊 MARKET SUMMARY")
    print("-" * 20)
    print(f"Total Gems Found: {len(unique_tokens)} tokens")
    if unique_tokens:
        top_token = unique_tokens[0]
        print(f"🥇 Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']:.1f}/100)")
        print(f"💰 Avg MCap: ${avg_mcap:,.0f}")
        print(f"📈 Avg Volume: ${avg_volume:,.0f}")
        print(f"🚀 Avg Vol/MCap Ratio: {avg_vol_mcap:.1f}%")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - NFA")