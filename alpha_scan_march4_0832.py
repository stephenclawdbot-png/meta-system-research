#!/usr/bin/env python3
import requests
from datetime import datetime

print("🚀 MEMECOIN ALPHA SCANNER UPDATE")
print("=" * 50)
print("Scan Time:", datetime.now().strftime("%A, March 4, 2026 — %I:%M %p (Asia/Manila)"))
print("Target Range: $30K-$200K Market Cap")
print("Source: DexScreener API")
print()

# Search multiple queries to get comprehensive coverage
queries = ['memecoin', 'new', 'solana', 'meme', 'hype']
alpha_gems = []

for query in queries:
    try:
        url = f'https://api.dexscreener.com/latest/dex/search?q={query}'
        response = requests.get(url)
        data = response.json()
        
        if 'pairs' in data:
            for pair in data['pairs']:
                if 'fdv' in pair:
                    mcap = pair['fdv']
                    volume = pair.get('volume', {}).get('h24', 0)
                    
                    # Filter criteria
                    if 30000 <= mcap <= 200000 and volume > 1000:
                        
                        # Alpha scoring
                        price_change = pair.get('priceChange', {}).get('h24', 0)
                        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
                        
                        # Simple score (volume dominance weighted)
                        alpha_score = min(100, vol_mcap_ratio * 0.7 + max(0, price_change) * 0.3)
                        
                        gem = {
                            'symbol': pair['baseToken']['symbol'].upper(),
                            'name': pair['baseToken']['name'],
                            'mcap': mcap,
                            'volume': volume,
                            'price_change': price_change,
                            'vol_mcap_ratio': vol_mcap_ratio,
                            'alpha_score': alpha_score,
                            'url': pair['url'],
                            'dex': pair['dexId'],
                            'chain': pair['chainId'],
                            'liquidity': pair.get('liquidity', {}).get('usd', 0)
                        }
                        
                        # Avoid duplicates
                        if gem['symbol'] not in [g['symbol'] for g in alpha_gems]:
                            alpha_gems.append(gem)
                            
    except Exception as e:
        print(f"Error with query '{query}': {e}")

# Sort by alpha score
alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)

if alpha_gems:
    print(f"💎 FOUND {len(alpha_gems)} ALPHA GEMS IN TARGET RANGE")
    print("-" * 50)
    
    for i, gem in enumerate(alpha_gems[:5], 1):
        print(f"🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        print(f"   📛 Name: {gem['name']}")
        print(f"   💰 MCap: ${gem['mcap']:,}")
        print(f"   📈 24h Volume: ${gem['volume']:,}")
        print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
        print(f"   🎯 24h Change: {gem['price_change']:.1f}%")
        print(f"   💧 Liquidity: ${gem['liquidity']:,}")
        print(f"   ⛓️ Chain: {gem['chain']}")
        print(f"   🔗 Dex: {gem['dex']}")
        print(f"   🔗 {gem['url']}")
        print()
    
    # Market summary
    avg_score = sum(g['alpha_score'] for g in alpha_gems) / len(alpha_gems)
    avg_vol_ratio = sum(g['vol_mcap_ratio'] for g in alpha_gems) / len(alpha_gems)
    
    print("📊 MARKET SUMMARY:")
    print(f"• Total Alpha Gems: {len(alpha_gems)}")
    print(f"• Average Alpha Score: {avg_score:.1f}/100")
    print(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
    print(f"• Best Opportunity: {alpha_gems[0]['symbol']} ({alpha_gems[0]['alpha_score']:.1f}/100)")
    
else:
    print("⚠️ No alpha gems found in target range")
    print("Market appears quiet or tokens outside range")

print()
print("⚠️ DISCLAIMER: High risk memecoin scanning - Not financial advice")