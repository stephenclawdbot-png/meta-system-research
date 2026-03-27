#!/usr/bin/env python3
"""Test CoinGecko API integration"""

import requests

def test_coingecko():
    symbols = ['BTC', 'ETH', 'SOL']
    coin_ids = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum', 
        'SOL': 'solana'
    }
    
    for symbol in symbols:
        try:
            coin_id = coin_ids[symbol]
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            print(f"Testing {symbol} ({coin_id})...")
            
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                current_price = data['market_data']['current_price']['usd']
                price_change_24h = data['market_data']['price_change_percentage_24h']
                volume_24h = data['market_data']['total_volume']['usd']
                
                print(f"Price: ${current_price:,.2f}")
                print(f"24h Change: {price_change_24h:.2f}%")
                print(f"24h Volume: ${volume_24h:,.0f}")
            else:
                print(f"Error: {response.text[:200]}")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"Error for {symbol}: {e}")
            print("-" * 50)

if __name__ == "__main__":
    test_coingecko()