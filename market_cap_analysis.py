#!/usr/bin/env python3
"""Analyze current Solana token market cap distribution"""

import requests
import json
from datetime import datetime

def analyze_market_caps():
    """Fetch and analyze Solana token market caps"""
    try:
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('pairs', [])
            
            if not pairs:
                print("No pairs found")
                return
                
            print(f"Found {len(pairs)} Solana trading pairs")
            print("-" * 50)
            
            # Analyze market cap distribution
            mcap_values = []
            non_zero_mcaps = []
            
            for pair in pairs:
                mcap = pair.get('marketCap', 0)
                mcap_values.append(mcap)
                if mcap > 0:
                    non_zero_mcaps.append(mcap)
                
            print(f"Total pairs: {len(pairs)}")
            print(f"Pairs with non-zero MCap: {len(non_zero_mcaps)}")
            print(f"Min MCap: ${min(mcap_values) if mcap_values else 0:,}")
            print(f"Max MCap: ${max(mcap_values) if mcap_values else 0:,}")
            print(f"Total MCap: ${sum(mcap_values):,}")
            
            if non_zero_mcaps:
                avg_mcap = sum(non_zero_mcaps) / len(non_zero_mcaps)
                print(f"Avg MCap (non-zero): ${avg_mcap:,.0f}")
                
            # Show distribution by ranges
            ranges = [
                (0, 10000, "Micro<10K"),
                (10000, 30000, "Small 10K-30K"),
                (30000, 200000, "Target 30K-200K"),
                (200000, 1000000, "Medium 200K-1M"),
                (1000000, 10000000, "Large 1M-10M"),
                (10000000, float('inf'), "Huge>10M")
            ]
            
            print("\n📊 MARKET CAP DISTRIBUTION")
            print("-" * 40)
            
            for min_range, max_range, label in ranges:
                count = len([m for m in mcap_values if min_range <= m <= max_range])
                total_mcap = sum([m for m in mcap_values if min_range <= m <= max_range])
                print(f"{label}: {count} tokens (Total: ${total_mcap:,})")
                
            # Show top 10 tokens by market cap
            print("\n🏆 TOP 10 TOKENS BY MARKET CAP")
            print("-" * 40)
            
            # Create list with token info
            token_data = []
            for pair in pairs:
                mcap = pair.get('marketCap', 0)
                if mcap == 0:
                    continue
                    
                base_token = pair.get('baseToken', {})
                symbol = base_token.get('symbol', 'Unknown')
                name = base_token.get('name', 'Unknown')
                volume_24h = pair.get('volume', {}).get('h24', 0)
                price_change = pair.get('priceChange', {}).get('h24', 0)
                
                token_data.append({
                    'symbol': symbol,
                    'name': name,
                    'market_cap': mcap,
                    'volume_24h': volume_24h,
                    'price_change': price_change,
                    'url': pair.get('url', '')
                })
            
            # Sort by market cap descending
            token_data.sort(key=lambda x: x['market_cap'], reverse=True)
            
            for i, token in enumerate(token_data[:10], 1):
                print(f"{i}. {token['symbol']} - ${token['market_cap']:,}")
                print(f"   Volume 24h: ${token['volume_24h']:,}")
                print(f"   24h Change: {token['price_change']:.2f}%")
                print(f"   Name: {token['name']}")
                
        else:
            print(f"API error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("📈 SOLANA MARKET CAP ANALYSIS")
    print("=" * 50)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')}")
    print()
    analyze_market_caps()