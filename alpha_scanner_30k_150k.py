#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime, timedelta

def fetch_dexscreener_tokens():
    """Fetch trending tokens from DexScreener API"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        filtered_tokens = []
        
        if not data or 'pairs' not in data:
            return filtered_tokens
            
        for token in data.get('pairs', []):
            # Filter criteria - specifically 30k-150k range
            mcap = token.get('fdv', 0)
            volume_24h = token.get('volume', {}).get('h24', 0)
            
            # Specific focus: 30k-150k mcap range
            if 30000 <= mcap <= 150000:
                # Additional alpha detection filters
                if volume_24h >= 1000:  # Min $1k volume
                    token_info = {
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': volume_24h,
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', '')
                    }
                    filtered_tokens.append(token_info)
        
        return filtered_tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - 30K-150K FOCUS")
    print("=" * 60)
    print("Filter: 30k-150k MCap Range | Min $1k Volume")
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)"))
    print()
    
    tokens = fetch_dexscreener_tokens()
    
    if not tokens:
        print("❌ No tokens matching 30k-150k criteria found")
        return
    
    # Sort by volume/mcap ratio to find gems
    tokens.sort(key=lambda x: x['volume_24h'] / x['mcap'], reverse=True)
    
    print("🔥 TOP ALPHA DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:8], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100
        
        # Calculate alpha score based on volume ratio and price momentum
        alpha_score = min(80, (vol_mcap_ratio * 0.8) + (max(0, token['price_change_24h']) * 0.2))
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {alpha_score:.1f}/80")
        print(f"   💰 MCap: ${token['mcap']:,.0f}")
        print(f"   📈 24h Vol: ${token['volume_24h']:,.0f}")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   💸 Price: ${token['price']:.6f}")
        print(f"   📊 24h Change: {token['price_change_24h']:.1f}%")
        print(f"   🌐 Dex: {token['dex']}")
        print(f"   🔗 {token['url']}")
        print()
    
    print("💎 SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(tokens)} tokens")
    print(f"Top Performer: {tokens[0]['symbol'] if tokens else 'N/A'}")
    print(f"Volume Leader: {max(tokens, key=lambda x: x['volume_24h'])['symbol'] if tokens else 'N/A'}")
    print("Market Focus: High volume activity in micro-cap range")
    print()
    print("⚠️ DISCLAIMER: NFA - High risk memecoin scanning")

if __name__ == "__main__":
    main()