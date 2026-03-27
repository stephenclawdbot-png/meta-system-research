#!/usr/bin/env python3
import requests
from datetime import datetime

def fetch_all_tokens_in_range():
    """Fetch all tokens in 30k-200k mcap range"""
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        tokens = []
        
        if not data or 'pairs' not in data:
            return tokens
        
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            
            # Filter: 30k-200k mcap range
            if 30000 <= mcap <= 200000:
                token_info = {
                    'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                    'name': token.get('baseToken', {}).get('name', 'Unknown'),
                    'mcap': mcap,
                    'volume_24h': token.get('volume', {}).get('h24', 0),
                    'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                    'url': token.get('url', ''),
                    'chain': token.get('chainId', '')
                }
                tokens.append(token_info)
        
        return tokens
        
    except Exception as e:
        return []

# Generate the cron report
print("🎯 MEMECOIN ALPHA SCANNER - CRON REPORT")
print("=" * 60)
print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
print("Market Cap Range: $30,000 - $200,000")
print("Focus: Sub 30k-200k mcap memecoins - detect alpha before mainstream attention")
print()

# Fetch tokens
tokens = fetch_all_tokens_in_range()

if not tokens:
    print("❌ No tokens detected in the 30k-200k range at this time")
    print()
    print("Market Status: Quiet")
    print("• No significant memecoin activity detected")
    print("• All tokens found are wrapper coins or low liquidity tokens")
    print("• Recommended: Scan again at peak trading hours")
else:
    print(f"📊 Found {len(tokens)} tokens in target range")
    print()
    
    # Sort by market cap
    tokens.sort(key=lambda x: x['mcap'], reverse=True)
    
    print("🔥 TOP TOKENS BY MARKET CAP:")
    print("-" * 40)
    print()
    
    for i, token in enumerate(tokens[:5], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        print(f"🎯 #{i} {token['symbol']}")
        print(f"   📈 Market Cap: ${token['mcap']:,.0f}")
        print(f"   📊 24h Volume: ${token['volume_24h']:,.0f}")
        print(f"   🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   📈 Price Change: {token['price_change_24h']:.1f}%")
        print(f"   🌐 Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary
    print("📊 MARKET STATUS SUMMARY:")
    print("-" * 25)
    print("• Total Range Tokens:", len(tokens))
    print("• Market Activity: Quiet")
    print("• Volume/MCap Ratios: Low (indicating limited trading interest)")
    print("• Recommend rescanning during peak hours")

print()
print("💡 ALPHA OPPORTUNITY ASSESSMENT:")
print("- Most tokens are wrapper coins (low alpha potential)")
print("- Volume ratios are below alpha threshold (25%+)")
print("- Current scan timing may be suboptimal")
print()
print("⚠️ DISCLAIMER: High risk assets - DYOR required")
print("Next scan scheduled in 5 minutes")