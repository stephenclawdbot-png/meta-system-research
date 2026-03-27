#!/usr/bin/env python3
"""
Test the memecoin scanner functionality without Telegram
"""

import sys
sys.path.append('.')

from memecoin_scanner import MemecoinScanner
import time

# Test the scanner
def test_scanner():
    scanner = MemecoinScanner()
    
    print("🚀 Testing memecoin scanner...")
    print("Scanning for tokens with criteria:")
    print("- Market Cap: $30K - $100K")
    print("- Volume: > $1K")
    print("- Age: < 24h")
    print("- Buy Ratio: >60%")
    print("-" * 50)
    
    # Run one scan cycle
    promising_tokens = scanner.scan_all_domains()
    
    if promising_tokens:
        print(f"\n🎯 Found {len(promising_tokens)} promising tokens!")
        for token in promising_tokens:
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
            name = token.get('baseToken', {}).get('name', 'Unknown')
            market_cap = token.get('marketCap', 0)
            volume = token.get('volume', {}).get('h24', 0)
            buy_ratio = token.get('buyRatio', 0)
            price = token.get('priceUsd', 0)
            
            print(f"\n📊 Token: {symbol} ({name})")
            print(f"💵 Price: ${price:.6f}")
            print(f"💰 Market Cap: ${market_cap:,.0f}")
            print(f"📈 Volume 24h: ${volume:,.0f}")
            print(f"📊 Buy Ratio: {buy_ratio:.1f}%")
            print(f"🔗 Dex URL: {token.get('url', 'N/A')}")
    else:
        print("📭 No tokens matching criteria found in this scan")

if __name__ == "__main__":
    test_scanner()