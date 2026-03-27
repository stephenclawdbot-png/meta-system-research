#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def search_memecoins():
    """Search DexScreener for memecoin keywords"""
    
    keywords = [
        "pepe", "doge", "bonk", "wif", "cat", "frog", "inu", "hamster", 
        "rocket", "baby", "based", "sam", "slerf", "trump", "maga"
    ]
    
    all_found = []
    
    print("🧠 MEMECOIN SCANNER - DexScreener Search")
    print("=" * 80)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print("Target: $30K - $200K Market Cap")
    print("Scanning for memecoin keywords...\n")
    
    for keyword in keywords:
        try:
            endpoint = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
            response = requests.get(endpoint, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and 'pairs' in data and data['pairs']:
                    for token in data['pairs']:
                        mcap = token.get('marketCap', token.get('fdv', 0))
                        
                        # Filter by mcap range
                        if 30000 <= mcap <= 200000:
                            symbol = token.get('baseToken', {}).get('symbol', '').upper()
                            volume = token.get('volume', {}).get('h24', 0)
                            
                            # Must have some volume
                            if volume >= 500:
                                token_info = {
                                    'keyword': keyword,
                                    'symbol': symbol,
                                    'name': token.get('baseToken', {}).get('name', ''),
                                    'mcap': mcap,
                                    'volume': volume,
                                    'price': token.get('priceUsd', 0),
                                    'price_change': token.get('priceChange', {}).get('h24', 0),
                                    'liquidity': token.get('liquidity', {}).get('usd', 0),
                                    'url': token.get('url', ''),
                                    'chain': token.get('chainId', '')
                                }
                                
                                # Avoid duplicates
                                if not any(t['symbol'] == symbol for t in all_found):
                                    all_found.append(token_info)
                
                print(f"✓ {keyword}: {len(data['pairs']) if data and 'pairs' in data else 0} tokens")
                
            else:
                print(f"✗ {keyword}: API error {response.status_code}")
                
        except Exception as e:
            print(f"✗ {keyword}: Error {e}")
    
    if all_found:
        # Sort by volume/mcap ratio
        all_found.sort(key=lambda x: x['volume']/x['mcap'] if x['mcap'] > 0 else 0, reverse=True)
        
        # Take top results
        top_results = all_found[:8]
        
        print(f"\n🔥 FOUND {len(all_found)} TOKENS ({len(top_results)} top results):")
        print("-" * 80)
        
        for i, token in enumerate(top_results, 1):
            vol_ratio = token['volume'] / token['mcap'] * 100 if token['mcap'] > 0 else 0
            print(f"🎯 #{i} {token['symbol']} (via '{token['keyword']}')")
            print(f"   💰 Market Cap: ${token['mcap']:,.0f}")
            print(f"   📈 24h Volume: ${token['volume']:,.0f} ({vol_ratio:.1f}% ratio)")
            print(f"   ⚡ Price Change: {token['price_change']:+.1f}%")
            print(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
            print(f"   🔗 {token['url']}")
            print()
        
        # Stats
        avg_mcap = sum(t['mcap'] for t in top_results) / len(top_results)
        avg_volume = sum(t['volume'] for t in top_results) / len(top_results)
        avg_ratio = sum(t['volume']/t['mcap'] for t in top_results) / len(top_results) * 100
        
        print("📊 SUMMARY STATISTICS:")
        print("-" * 80)
        print(f"• Tokens Found: {len(all_found)}")
        print(f"• Avg Market Cap: ${avg_mcap:,.0f}")
        print(f"• Avg 24h Volume: ${avg_volume:,.0f}")
        print(f"• Avg Volume Ratio: {avg_ratio:.1f}%")
        
        # Top pick analysis
        if top_results:
            top_pick = top_results[0]
            print(f"\n💡 TOP PICK ANALYSIS: {top_pick['symbol']}")
            print("-" * 80)
            vol_ratio_pick = top_pick['volume'] / top_pick['mcap'] * 100
            
            print(f"• Volume Efficiency: {vol_ratio_pick:.1f}% (volume/mcap)")
            print(f"• Buy Pressure: {top_pick['price_change']:+.1f}% price increase")
            print(f"• Liquidity Score: ${top_pick['liquidity']:,.0f}")
            print(f"• Discovery: Found via '{top_pick['keyword']}' search")
        
    else:
        print("\n❌ No memecoins found in target range")

if __name__ == "__main__":
    search_memecoins()