#!/usr/bin/env python3
import requests
from datetime import datetime
import time

def fetch_new_solana_tokens():
    """Fetch newest tokens on Solana to find potential meme gems"""
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        potential_gems = []
        
        if not data or 'pairs' not in data:
            return potential_gems
        
        for token in data.get('pairs', [])[:50]:  # Check first 50 results
            mcap = token.get('fdv', 0)
            name = token.get('baseToken', {}).get('name', '').lower()
            symbol = token.get('baseToken', {}).get('symbol', '').lower()
            dex_id = token.get('dexId', '').lower()
            
            # Focus on Solana with pumpfun and new meme coins
            if (dex_id == 'pumpfun' or dex_id == 'pumpswap') and 30000 <= mcap <= 200000:
                token_info = {
                    'name': token.get('baseToken', {}).get('name', 'Unknown'),
                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': token.get('volume', {}).get('h24', 0),
                    'price': token.get('priceUsd', 0),
                    'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                    'url': token.get('url', ''),
                    'dex': token.get('dexId', ''),
                    'chain': token.get('chainId', ''),
                    'created_at': token.get('pairCreatedAt', 0)
                }
                potential_gems.append(token_info)
        
        return potential_gems
        
    except Exception as e:
        print(f"Error fetching Solana tokens: {e}")
        return []

def calculate_potential_score(token):
    """Calculate potential score for new tokens"""
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # New tokens benefit from recency
    recency_bonus = min(50, max(0, 100 - (time.time() - token['created_at']/1000) / 3600))
    
    potential_score = min(
        100,
        (vol_mcap_ratio * 0.4) +        # Trading activity
        (momentum * 0.3) +              # Price momentum  
        (min(100, token['volume_24h'] / 500) * 0.1) +  # Absolute volume
        (recency_bonus * 0.2)            # Recency bonus
    )
    
    return round(potential_score, 1)

def main():
    print("🧠 POTENTIAL MEMECOIN SCANNER - PUMPFUN FOCUS")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print("Target: Solana pump.fun tokens | MCap: $30k-200k")
    print()
    
    # Fetch potential tokens
    tokens = fetch_new_solana_tokens()
    
    if not tokens:
        print("❌ No potential memecoins found in target range")
        return
    
    # Sort by potential score
    for token in tokens:
        token['potential_score'] = calculate_potential_score(token)
    tokens.sort(key=lambda x: x['potential_score'], reverse=True)
    
    print(f"💎 TOP POTENTIAL MEMECOINS ({len(tokens)} total):")
    print("-" * 60)
    
    for i, token in enumerate(tokens[:8], 1):
        age_hours = (time.time() - token['created_at']/1000) / 3600 if token['created_at'] > 0 else 0
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"🚀 #{i} {token['symbol']} - Potential Score: {token['potential_score']}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   ⏰ Age: {age_hours:.1f} hours")
        print(f"   🌐 Dex: {token['dex']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Potential Gems: {len(tokens)} tokens")
    if tokens:
        avg_score = sum(t['potential_score'] for t in tokens) / len(tokens)
        print(f"🧠 Average Potential Score: {avg_score:.1f}/100")
        print(f"💰 Total Combined MCap: ${sum(t['mcap'] for t in tokens):,.0f}")
        print(f"📊 Range: ${min(t['mcap'] for t in tokens):,}-${max(t['mcap'] for t in tokens):,}")
    print()
    print("⚠️ DISCLAIMER: High risk/High reward - DYOR/NFA")

if __name__ == "__main__":
    main()