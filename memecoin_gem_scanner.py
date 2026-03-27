#!/usr/bin/env python3
"""
Advanced DexScreener scanner specifically for memecoins in 30k-200k range
"""

import requests
from datetime import datetime
import re

# Memecoin-related keywords to identify actual memecoins
MEMECOIN_KEYWORDS = [
    'inu', 'dog', 'cat', 'meme', 'elon', 'woof', 'frog', 'pepe', 
    'doge', 'shib', 'floki', 'bonk', 'grok', 'mog', 'honk',
    'wif', 'doge', 'bobo', 'chad', 'smile', 'regan', 'trump',
    'maga', 'harley', 'wif', 'tard', 'correct', 'molly', 'mochi'
]

def is_memecoin(token_name):
    """Check if token name indicates it's a memecoin"""
    if not token_name or token_name.lower() in ['solana', 'sol', 'wrapped sol']:
        return False
    
    name_lower = token_name.lower()
    
    # Check for memecoin keywords
    for keyword in MEMECOIN_KEYWORDS:
        if keyword in name_lower:
            return True
    
    # Check for suspiciously low price (high supply tokens)
    return False

def calculate_memecoin_score(token):
    """Calculate a score to identify promising memecoins"""
    score = 0
    
    # Market Cap in our target range gets base score
    mcap = token.get('marketCap', 0)
    if 30000 <= mcap <= 200000:
        score += 20
    else:
        return 0  # Not in our range
    
    # Volume/MCAP ratio (higher = better)
    volume_24h = token.get('volume', {}).get('h24', 0)
    if mcap > 0:
        volume_ratio = volume_24h / mcap
        if volume_ratio > 0.5:
            score += 20
        elif volume_ratio > 0.2:
            score += 15
        elif volume_ratio > 0.1:
            score += 10
    
    # Buy ratio
    txns = token.get('txns', {}).get('h24', {})
    buys = txns.get('buys', 0)
    sells = txns.get('sells', 0)
    total_txns = buys + sells
    if total_txns > 10:
        buy_ratio = buys / total_txns
        if buy_ratio > 0.6:
            score += 20
        elif buy_ratio > 0.55:
            score += 15
        elif buy_ratio > 0.5:
            score += 10
    
    # Recent price momentum
    price_change = token.get('priceChange', {}).get('h24', 0)
    if price_change > 10:
        score += 15
    elif price_change > 5:
        score += 10
    elif price_change > 0:
        score += 5
    
    # Token age (newer = better)
    pair_created_at = token.get('pairCreatedAt', 0)
    if pair_created_at:
        age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
        if age_hours < 24:
            score += 20
        elif age_hours < 168:  # 1 week
            score += 10
    
    # Check if it's actually a memecoin
    base_token = token.get('baseToken', {})
    token_name = base_token.get('name', '')
    token_symbol = base_token.get('symbol', '')
    
    if is_memecoin(token_name) or is_memecoin(token_symbol):
        score += 25
    else:
        score -= 20  # Penalize non-memecoins
    
    return score

# DexScreener API endpoint
url = "https://api.dexscreener.com/latest/dex/search?q=solana"

print("🚀 Advanced Memecoin Gem Scanner")
print("💰 Target: Memecoins with $30k - $200k MCAP")
print(f"📍 Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🎯 Scoring based on: MCAP range, Volume ratio, Buy pressure, Price momentum, Age")
print("-" * 60)

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
    
    # Score and filter tokens
    scored_tokens = []
    for token in data['pairs']:
        score = calculate_memecoin_score(token)
        if score > 0:  # Only include tokens with positive score
            scored_tokens.append((score, token))
    
    # Sort by score (descending)
    scored_tokens.sort(key=lambda x: x[0], reverse=True)
    
    print(f"✅ Found {len(scored_tokens)} potential memecoin gems:")
    print("🎯 Score breakdown (25 pts each): MCAP range, Volume ratio, Buy pressure, Price momentum, Recent age")
    print("-" * 60)
    
    if scored_tokens:
        for i, (score, token) in enumerate(scored_tokens[:10], 1):  # Show top 10
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
            print(f"   🎯 Total Score: {int(score)}/80")
            print(f"   📊 MCAP: ${int(mcap):,}")
            print(f"   💰 Price: ${float(price):.8f}")
            print(f"   📈 24h Vol: ${int(volume):,}")
            print(f"   📈 24h Chg: {float(price_change):+.2f}%")
            print(f"   ⏱️ Age: {age_hours}")
            
            # Show transaction data
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            if total_txns > 0:
                buy_ratio = (buys / total_txns) * 100
                print(f"   🔄 Txns: {total_txns} (Buys: {buys}, Ratio: {buy_ratio:.1f}%)")
            
            # Calculate and show Volume/MCAP ratio
            if mcap > 0:
                vol_ratio = volume / mcap
                print(f"   📊 Volume/MCAP Ratio: {vol_ratio:.2f}")
            
            # Show DexScreener link
            pair_addr = token.get('pairAddress', '')
            if pair_addr:
                print(f"   🔗 https://dexscreener.com/solana/{pair_addr}")
            
            print("-" * 40)
    else:
        print("📭 No quality memecoin gems found in the target range at this time.")
        print("💡 Market conditions may not be favorable for new memecoin launches.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()