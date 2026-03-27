#!/usr/bin/env python3
"""Extract memecoins in the $30K-$200K range"""

import requests
import json
from datetime import datetime

def fetch_target_memecoins():
    """Fetch memecoins in $30K-$200K range"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            target_pairs = []
            
            for pair in pairs:
                mcap = pair.get('marketCap', 0)
                # Target range: $30K-$200K
                if 30000 <= mcap <= 200000:
                    base_token = pair.get('baseToken', {})
                    symbol = base_token.get('symbol', 'Unknown')
                    name = base_token.get('name', 'Unknown')
                    
                    # Skip SOL pairs (they have very similar market caps)
                    if symbol == 'SOL' or 'solana' in name.lower():
                        continue
                    
                    volume_24h = pair.get('volume', {}).get('h24', 0)
                    price_change = pair.get('priceChange', {}).get('h24', 0)
                    liquidity = pair.get('liquidity', {}).get('usd', 0)
                    
                    txns = pair.get('txns', {}).get('h24', {})
                    buys = txns.get('buys', 0)
                    sells = txns.get('sells', 0)
                    total_txns = buys + sells
                    buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
                    
                    vol_mcap_ratio = (volume_24h / mcap * 100) if mcap > 0 else 0
                    
                    target_pairs.append({
                        'symbol': symbol,
                        'name': name,
                        'market_cap': mcap,
                        'volume_24h': volume_24h,
                        'vol_mcap_ratio': vol_mcap_ratio,
                        'price_change': price_change,
                        'liquidity': liquidity,
                        'buy_ratio': buy_ratio,
                        'transactions': f"{buys}/{sells}",
                        'url': pair.get('url', '')
                    })
            
            # Sort by vol/mcap ratio (higher ratio = better opportunity)
            target_pairs.sort(key=lambda x: x['vol_mcap_ratio'], reverse=True)
            return target_pairs
            
        else:
            print(f"API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("🎯 TARGET MEMECOIN SCANNER")
    print("=" * 60)
    print("Market Cap Range: $30,000 - $200,000")
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print()
    
    print("Fetching target memecoins...")
    target_pairs = fetch_target_memecoins()
    
    print(f"✅ Found {len(target_pairs)} tokens in target range")
    print("-" * 60)
    
    if not target_pairs:
        print("No memecoins found in the $30K-$200K range")
        print("Market may be quiet or moving to higher ranges")
        return
    
    # Display results
    print(f"\n🔥 ALPHA MEMECOIN OPPORTUNITIES")
    print("=" * 40)
    
    for i, token in enumerate(target_pairs, 1):
        print(f"\n{i}. 💎 {token['symbol']}")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 Market Cap: ${token['market_cap']:,}")
        print(f"   📈 24h Volume: ${token['volume_24h']:,}")
        print(f"   🌊 Vol/MCap Ratio: {token['vol_mcap_ratio']:.2f}%")
        print(f"   🔺 24h Price Change: {token['price_change']:.2f}%")
        print(f"   💧 Liquidity: ${token['liquidity']:,}")
        print(f"   📈 Buy Ratio: {token['buy_ratio']:.1f}%")
        print(f"   🔄 Transactions: {token['transactions']}")
        print(f"   🔗 DexScreener: {token['url']}")
    
    # Calculation summary
    total_mcap = sum(token['market_cap'] for token in target_pairs)
    avg_vol_ratio = sum(token['vol_mcap_ratio'] for token in target_pairs) / len(target_pairs)
    avg_buy_ratio = sum(token['buy_ratio'] for token in target_pairs) / len(target_pairs)
    
    print(f"\n📊 CALCULATION SUMMARY")
    print("-" * 30)
    print(f"Total Market Cap (Range): ${total_mcap:,}")
    print(f"Average Vol/MCap Ratio: {avg_vol_ratio:.2f}%")
    print(f"Average Buy Ratio: {avg_buy_ratio:.1f}%")
    
    if avg_vol_ratio > 5:
        print(f"🎯 Alpha Signal: HIGH (Volume/MCap ratio >5%)")
    elif avg_vol_ratio > 2:
        print(f"🎯 Alpha Signal: MEDIUM (Volume/MCap ratio >2%)")
    else:
        print(f"🎯 Alpha Signal: LOW (Volume/MCap ratio <2%)")
    
    print("\n⚠️ HIGH RISK - RESEARCH REQUIRED")

if __name__ == "__main__":
    main()