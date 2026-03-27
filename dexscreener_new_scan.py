#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

print("🧠 ALPHA MEMECOIN SCANNER - NEW TOKENS")
print("============================================================")
print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
print("Market Cap Range: $30,000 - $200,000")
print()

# Fetch new tokens
cmd = 'curl -s "https://api.dexscreener.com/latest/dex/search?q=new"'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

data = json.loads(result.stdout)
pairs = data.get('pairs', [])

alpha_candidates = []

for pair in pairs:
    try:
        mcap = pair.get('fdv', 0)
        if mcap < 30000 or mcap > 200000:
            continue
            
        token_info = pair.get('baseToken', {})
        volume_24h = pair.get('volume', {}).get('h24', 0)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        price_change = pair.get('priceChange', {}).get('h24', 0)
        
        txns = pair.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = buys / total_txns if total_txns > 0 else 0
        
        # Calculate alpha score
        alpha_score = 0
        
        # Volume score (max 25)
        if volume_24h > 10000:
            alpha_score += 25
        elif volume_24h > 5000:
            alpha_score += 15
        elif volume_24h > 1000:
            alpha_score += 5
        
        # Liquidity score (max 15)
        if liquidity > 5000:
            alpha_score += 15
        elif liquidity > 2000:
            alpha_score += 10
            
        # Buy pressure (max 20)
        if buy_ratio > 0.6:
            alpha_score += 20
        elif buy_ratio > 0.5:
            alpha_score += 10
            
        # Price momentum (max 20)
        if price_change > 20:
            alpha_score += 20
        elif price_change > 10:
            alpha_score += 10
        elif price_change > 5:
            alpha_score += 5
            
        alpha_candidates.append({
            'symbol': token_info.get('symbol', 'Unknown'),
            'name': token_info.get('name', 'Unknown'),
            'mcap': mcap,
            'volume': volume_24h,
            'price_change': price_change,
            'liquidity': liquidity,
            'buy_ratio': buy_ratio * 100,
            'alpha_score': alpha_score,
            'url': pair.get('url'),
            'age': pair.get('pairCreatedAt', 0)
        })
        
    except Exception as e:
        continue

# Sort by alpha score
alpha_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)

print(f"Qualifying New Tokens Found: {len(alpha_candidates)}")
print()

if alpha_candidates:
    print("🔥 NEW ALPHA OPPORTUNITIES")
    print("-" * 40)
    
    for i, gem in enumerate(alpha_candidates[:5], 1):
        print(f"{i}. {gem['symbol']} - Alpha: {gem['alpha_score']}/80")
        print(f"   💰 Market Cap: ${gem['mcap']:,.0f}")
        print(f"   📈 24h Change: {gem['price_change']:.1f}%")
        print(f"   🔥 Volume: ${gem['volume']:,.0f}")
        print(f"   📊 Vol/Mcap Ratio: {(gem['volume']/gem['mcap']*100):.1f}%")
        print(f"   💧 Liquidity: ${gem['liquidity']:,.0f}")
        print(f"   🛒 Buy Ratio: {gem['buy_ratio']:.1f}%")
        print(f"   🔗 URL: {gem['url']}")
        print()
else:
    print("⚠️ No new alpha gems found in the 30k-200k range")
    print("Either the market is quiet or alpha opportunities are already saturated.")
    print()

print("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")