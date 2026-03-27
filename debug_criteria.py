#!/usr/bin/env python3
"""Debug the criteria checking logic"""

from memecoin_scanner import MemecoinScanner

def debug_criteria():
    scanner = MemecoinScanner()
    
    # Test token that should meet criteria
    test_token = {
        'pairAddress': 'test123',
        'baseToken': {'name': 'GoodToken', 'symbol': 'GOOD'},
        'marketCap': '50000',  # $50k
        'priceUsd': '0.0001',
        'volume': {'h24': '2000'},  # $2k volume
        'priceChange': {'h24': '5.5'},  # Positive change
        'liquidity': {'usd': '5000'},  # Good liquidity
        'pairCreatedAt': '2026-02-20T23:00:00Z'  # Recent
    }
    
    print("Testing token criteria step by step...")
    print(f"Token: {test_token.get('baseToken', {}).get('name')}")
    
    # Test market cap
    mcap_str = test_token.get('marketCap', '0')
    print(f"Market cap string: {mcap_str}")
    
    try:
        mcap = float(mcap_str) if isinstance(mcap_str, str) else mcap_str
        print(f"Market cap float: {mcap}")
        print(f"Min cap: {scanner.min_mcap}, Max cap: {scanner.max_mcap}")
        print(f"Market cap valid: {mcap >= scanner.min_mcap and mcap <= scanner.max_mcap}")
    except Exception as e:
        print(f"Market cap error: {e}")
    
    # Test volume
    volume_str = test_token.get('volume', {}).get('h24', '0') if isinstance(test_token.get('volume'), dict) else test_token.get('volume', '0')
    print(f"Volume string: {volume_str}")
    try:
        volume = float(volume_str) if volume_str and volume_str != '0' else 0
        print(f"Volume float: {volume}")
        print(f"Min volume: {scanner.min_volume}")
        print(f"Volume valid: {volume >= scanner.min_volume}")
    except Exception as e:
        print(f"Volume error: {e}")
    
    # Test age
    if test_token.get('pairCreatedAt'):
        try:
            from datetime import datetime
            created_at = datetime.fromisoformat(test_token['pairCreatedAt'].replace('Z', '+00:00'))
            age_hours = (datetime.now() - created_at).total_seconds() / 3600
            print(f"Age in hours: {age_hours}")
            print(f"Max age: {scanner.max_age_hours}")
            print(f"Age valid: {age_hours <= scanner.max_age_hours}")
        except Exception as e:
            print(f"Age error: {e}")
    
    # Test liquidity
    liquidity_str = test_token.get('liquidity', {}).get('usd', '0') if isinstance(test_token.get('liquidity'), dict) else test_token.get('liquidity', '0')
    print(f"Liquidity string: {liquidity_str}")
    try:
        liquidity = float(liquidity_str) if liquidity_str else 0
        print(f"Liquidity float: {liquidity}")
        print(f"Min liquidity: 1000")
        print(f"Liquidity valid: {liquidity >= 1000}")
    except Exception as e:
        print(f"Liquidity error: {e}")
    
    print(f"\nFinal result: {scanner.meets_criteria(test_token)}")

if __name__ == "__main__":
    debug_criteria()