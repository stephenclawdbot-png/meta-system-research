#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def final_cron_scan():
    """Final cron-compatible alpha scan"""
    
    print("🚀 CRON ALPHA SCANNER - DexScreener Memecoin Scan")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')}")
    print("Target: $30K-$200K MCap Memecoins")
    print()
    
    # Test API - Get PEPE tokens
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=pepe"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and 'pairs' in data:
                # Filter by mcap range
                filtered = []
                for token in data['pairs'][:20]:  # First 20 results
                    mcap = token.get('marketCap', token.get('fdv', 0))
                    
                    if 30000 <= mcap <= 200000:
                        symbol = token.get('baseToken', {}).get('symbol', 'UNKNOWN').upper()
                        volume = token.get('volume', {}).get('h24', 0)
                        price_change = token.get('priceChange', {}).get('h24', 0)
                        liquidity = token.get('liquidity', {}).get('usd', 0)
                        
                        filtered.append({
                            'symbol': symbol,
                            'mcap': mcap,
                            'volume': volume,
                            'vol_ratio': (volume / mcap * 100) if mcap > 0 else 0,
                            'price_change': price_change,
                            'liquidity': liquidity
                        })
                
                print(f"Tokens in range: {len(filtered)}")
                
                if filtered:
                    # Sort by volume/mcap ratio
                    filtered.sort(key=lambda x: x['vol_ratio'], reverse=True)
                    
                    print("\nTOP ALPHA CANDIDATES:")
                    print("-" * 60)
                    
                    for i, token in enumerate(filtered[:5], 1):
                        print(f"{i}. {token['symbol']}")
                        print(f"   MCap: ${token['mcap']:,.0f} | Vol: ${token['volume']:,.0f}")
                        print(f"   Ratio: {token['vol_ratio']:.1f}% | Price: {token['price_change']:+.1f}%")
                        print(f"   Liquidity: ${token['liquidity']:,.0f}")
                        print()
                    
                    # Stats
                    avg_ratio = sum(t['vol_ratio'] for t in filtered) / len(filtered)
                    avg_mcap = sum(t['mcap'] for t in filtered) / len(filtered)
                    
                    print("MARKET SUMMARY:")
                    print("-" * 60)
                    print(f"• Average MCap: ${avg_mcap:,.0f}")
                    print(f"• Average Volume Ratio: {avg_ratio:.1f}%")
                    print(f"• Total Tokens: {len(filtered)}")
                    
                    # Alpha assessment
                    best = filtered[0]
                    print(f"\nALPHA ASSESSMENT:")
                    print("-" * 60)
                    
                    if best['vol_ratio'] > 10:
                        print(f"💎 STRONG: {best['symbol']} has {best['vol_ratio']:.1f}% volume efficiency")
                    elif best['vol_ratio'] > 5:
                        print(f"📈 GOOD: {best['symbol']} has {best['vol_ratio']:.1f}% volume efficiency") 
                    else:
                        print(f"📊 MODERATE: {best['symbol']} has {best['vol_ratio']:.1f}% volume efficiency")
                    
                else:
                    print("❌ No tokens found in target range")
                    
            else:
                print("❌ No token data received")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Scan failed: {e}")
    
    print(f"\nScan completed at {datetime.now().strftime('%I:%M %p')}")

if __name__ == "__main__":
    final_cron_scan()