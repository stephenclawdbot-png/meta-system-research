#!/usr/bin/env python3
import json
import requests
import time
from datetime import datetime

def fetch_dexscreener_memecoins():
    """Fetch memecoins from DexScreener trending/new endpoints"""
    gems = []
    
    # Try trending tokens
    print("📊 Searching DexScreener trending...")
    try:
        # Multiple potential endpoints
        endpoints = [
            "https://api.dexscreener.com/latest/dex/tokens/trending",
            "https://api.dexscreener.com/latest/dex/tokens/new",
            "https://api.dexscreener.com/latest/dex/search?q=pepe",
            "https://api.dexscreener.com/latest/dex/search?q=cat",
            "https://api.dexscreener.com/latest/dex/search?q=doge",
            "https://api.dexscreener.com/latest/dex/search?q=shib",
            "https://api.dexscreener.com/latest/dex/search?q=moon",
            "https://api.dexscreener.com/latest/dex/search?q=elon",
            "https://api.dexscreener.com/latest/dex/search?q=bonk",
            "https://api.dexscreener.com/latest/dex/search?q=floki"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint)
                if response.status_code == 200:
                    data = response.json()
                    if 'pairs' in data and data['pairs']:
                        print(f"✅ Found {len(data['pairs'])} pairs from {endpoint.split('/')[-1]}")
                        
                        for token in data['pairs']:
                            base_token = token.get('baseToken', {})
                            
                            # Skip if no symbol
                            if not base_token.get('symbol'):
                                continue
                                
                            # Skip SOL itself
                            if base_token.get('symbol') == 'SOL':
                                continue
                                
                            mcap = token.get('fdv', 0)
                            volume_24h = token.get('volume', {}).get('h24', 0)
                            
                            # Target range: 30k-200k mcap
                            if 30000 <= mcap <= 200000:
                                price_change = token.get('priceChange', {}).get('h24', 0)
                                liquidity = token.get('liquidity', {}).get('usd', 0)
                                
                                txns = token.get('txns', {}).get('h24', {})
                                buys = txns.get('buys', 0) if txns else 0
                                sells = txns.get('sells', 0) if txns else 0
                                total_txns = buys + sells
                                buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
                                
                                # Calculate potential metrics
                                vol_mcap_ratio = (volume_24h / mcap * 100) if mcap > 0 else 0
                                
                                # Skip tokens with extremely low volume
                                if volume_24h < 10:
                                    continue
                                
                                # Alpha scoring - prioritize actual trading volume
                                base_score = min(100, vol_mcap_ratio * 1.5 + buy_ratio * 0.7)
                                # Bonus for higher actual volumes
                                volume_bonus = min(20, volume_24h / 100)  # Up to 20 points for volume
                                score = min(100, base_score + volume_bonus)
                                
                                gem = {
                                    'symbol': base_token.get('symbol'),
                                    'name': base_token.get('name', 'Unknown'),
                                    'mcap': mcap,
                                    'volume_24h': volume_24h,
                                    'vol_mcap_ratio': vol_mcap_ratio,
                                    'price_change': price_change or 0,
                                    'liquidity': liquidity,
                                    'buy_ratio': buy_ratio,
                                    'alpha_score': round(score, 1),
                                    'url': token.get('url', ''),
                                    'chain': token.get('chainId', '')
                                }
                                
                                # Avoid duplicates
                                if not any(g['symbol'] == gem['symbol'] for g in gems):
                                    gems.append(gem)
                    
            except Exception as e:
                print(f"⚠️ Failed {endpoint}: {e}")
                continue
                
    except Exception as e:
        print(f"❌ DexScreener search failed: {e}")
    
    return gems

def main():
    print("🧠 MEMECOIN ALPHA SCANNER - Sub $30K-$200K MCAP Detection")
    print("=" * 70)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print("Scanning DexScreener for trending memecoins with volume momentum...")
    print()
    
    # Fetch gems
    gems = fetch_dexscreener_memecoins()
    
    if gems:
        # Filter and sort
        gems = [g for g in gems if g['alpha_score'] >= 20]
        gems.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        print(f"✅ FOUND {len(gems)} ALPHA MEMECOINS")
        print("-" * 50)
        
        for i, gem in enumerate(gems[:10], 1):  # Show top 10
            print(f"\n{i}. 🎯 {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100")
            print(f"   📛 {gem['name']}")
            print(f"   💰 Market Cap: ${gem['mcap']:,}")
            print(f"   📈 Volume 24h: ${gem['volume_24h']:,}")
            print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
            print(f"   📊 Price Change: {gem['price_change']:.2f}%")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            print(f"   📈 Buy Ratio: {gem['buy_ratio']:.1f}%")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 {gem['url']}")
        
        # Summary
        print(f"\n📊 SUMMARY")
        print("-" * 25)
        print(f"Total Candidates: {len(gems)}")
        print(f"Avg Market Cap: ${sum(g['mcap'] for g in gems)/len(gems):,.0f}")
        print(f"Avg Volume Ratio: {sum(g['vol_mcap_ratio'] for g in gems)/len(gems):.1f}%")
        print(f"Avg Alpha Score: {sum(g['alpha_score'] for g in gems)/len(gems):.1f}/100")
        
    else:
        print("❌ No memecoins found in $30k-$200k mcap range")
        print("This could indicate:")
        print("• Market is quiet (low trading activity)")
        print("• DexScreener API may be experiencing issues")
        print("• No tokens currently match your criteria")
    
    print("\n⚠️ HIGH RISK MEMECOIN TRADING - ALWAYS DO YOUR OWN RESEARCH")
    print("Never invest more than you can afford to lose!")

if __name__ == "__main__":
    main()