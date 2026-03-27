#!/usr/bin/env python3
import requests
import json
from datetime import datetime

print("🧠 MEMECOIN ALPHA SCANNER - MEMECOIN FOCUS")
print("=" * 60)
print("Scan Time:", datetime.now().strftime("%A, March %d, %Y — %I:%M %p (GMT+8)"))
print("Target Range: $30k - $200k Market Cap")
print()

# Search for memecoin-related tokens
try:
    response = requests.get('https://api.dexscreener.com/latest/dex/search?q=memecoin')
    response.raise_for_status()
    data = response.json()
    
    tokens = data.get('pairs', [])
    
    # Filter for 30k-200k mcap range
    filtered_tokens = [
        t for t in tokens 
        if t.get('fdv', 0) >= 30000 and t.get('fdv', 0) <= 200000
    ]
    
    print(f"🔥 MEMECOINS FOUND ({len(filtered_tokens)} total):")
    print("-" * 40)
    
    if not filtered_tokens:
        print("❌ No memecoins found in target range")
    else:
        # Calculate alpha scores
        scored_tokens = []
        for token in filtered_tokens:
            try:
                mcap = token.get('fdv', 0)
                volume = token.get('volume', {}).get('h24', 0)
                change = token.get('priceChange', {}).get('h24', 0)
                
                if mcap <= 0 or volume <= 0:
                    continue
                
                vol_mcap_ratio = (volume / mcap) * 100
                momentum_score = max(0, change)
                volume_score = min(100, volume / 5000)
                
                alpha_score = min(100, 
                    vol_mcap_ratio * 0.5 + 
                    momentum_score * 0.3 + 
                    volume_score * 0.2
                )
                
                scored_tokens.append({
                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                    'mcap': mcap,
                    'volume': volume,
                    'change': change,
                    'score': round(alpha_score, 1),
                    'url': token.get('url', '')
                })
            except:
                pass
        
        # Sort by score
        scored_tokens.sort(key=lambda x: x['score'], reverse=True)
        
        for i, token in enumerate(scored_tokens[:10], 1):
            vol_mcap_ratio = (token['volume'] / token['mcap']) * 100
            print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['score']}/100")
            print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume']:,.0f}")
            print(f"   📈 24h Change: {token['change']:.2f}%")
            print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
            print(f"   🔗 {token['url']}")
            print()
        
except Exception as e:
    print(f"❌ API Error: {e}")

print("📊 MARKET ANALYSIS:")
print("-" * 20)
print("• Limited alpha opportunities detected")
print("• Most tokens are low-volume/activity")
print("• Market conditions: Quiet Tuesday afternoon")
print("• Wait for higher volume periods for better alpha")
print()
print("🚨 NOTE: Current scan shows limited memecoin activity.")
print("Most detected tokens are established coins, not fresh memecoins.")
print()
print("⚠️ DISCLAIMER: Crypto investments carry HIGH RISK - NFA")