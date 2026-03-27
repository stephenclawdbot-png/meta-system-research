#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins_dexscreener():
    '''Fetch memecoins using DexScreener search with broader criteria'''
    try:
        response = requests.get('https://api.dexscreener.com/latest/dex/search?q=solana')
        response.raise_for_status()
        data = response.json()
        return data.get('pairs', [])
    except Exception as e:
        print(f'Error: {e}')
        return []

def calculate_alpha_score(token):
    '''Calculate alpha score based on memecoin metrics'''
    try:
        mcap = token.get('fdv', 0)
        volume = token.get('volume', {}).get('h24', 0)
        change = token.get('priceChange', {}).get('h24', 0)
        
        if mcap <= 0 or volume <= 0:
            return 0
        
        # Score components
        vol_mcap_ratio = (volume / mcap) * 100
        momentum_score = max(0, change)
        volume_score = min(100, volume / 5000)
        
        # Weighted score (max 100)
        alpha_score = min(100, 
            vol_mcap_ratio * 0.5 +    # Volume/MCap ratio (most important)
            momentum_score * 0.3 +    # Positive momentum
            volume_score * 0.2         # Absolute volume
        )
        
        return round(alpha_score, 1)
    except:
        return 0

print("🧠 MEMECOIN ALPHA SCANNER - DEXSCREENER")
print("=" * 60)
print("Scan Time:", datetime.now().strftime("%A, March %d, %Y — %I:%M %p (GMT+8)"))
print("Target Range: $30k - $200k Market Cap")

# Fetch data
tokens = fetch_memecoins_dexscreener()

# Filter for 30k-200k mcap range
filtered_tokens = [
    t for t in tokens 
    if t.get('fdv', 0) >= 30000 and t.get('fdv', 0) <= 200000
]

print(f"Total Tokens Scanned: {len(filtered_tokens)}")
print()

if not filtered_tokens:
    print("❌ No memecoins found in target range")
    exit()

# Calculate scores and sort
scored_tokens = []
for token in filtered_tokens:
    score = calculate_alpha_score(token)
    if score > 0:
        scored_tokens.append({
            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
            'mcap': token.get('fdv', 0),
            'volume': token.get('volume', {}).get('h24', 0),
            'change': token.get('priceChange', {}).get('h24', 0),
            'score': score,
            'url': token.get('url', '')
        })

# Sort by alpha score
scored_tokens.sort(key=lambda x: x['score'], reverse=True)

print("🔥 TOP ALPHA MEMECOINS DETECTED:")
print("-" * 50)

for i, token in enumerate(scored_tokens[:10], 1):
    vol_mcap_ratio = (token['volume'] / token['mcap']) * 100
    print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['score']}/100")
    print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume']:,.0f}")
    print(f"   📈 24h Change: {token['change']:.2f}%")
    print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
    print(f"   🔗 {token['url']}")
    print()

# Summary
print("📊 ALPHA SCANNER SUMMARY:")
print("-" * 30)
print(f"• High Alpha Tokens (>50 score): {len([t for t in scored_tokens if t['score'] > 50])}")
print(f"• Good Alpha Tokens (>30 score): {len([t for t in scored_tokens if t['score'] > 30])}")
print(f"• Total Alpha Detected: {len(scored_tokens)} tokens")
if scored_tokens:
    print(f"• Average Alpha Score: {sum(t['score'] for t in scored_tokens)/len(scored_tokens):.1f}/100")
else:
    print("• Average Alpha Score: 0/100")
print()
print("⚠️ DISCLAIMER: Cryptocurrency investments carry high risk - NFA")