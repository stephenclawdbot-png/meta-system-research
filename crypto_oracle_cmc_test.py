#!/usr/bin/env python3
"""
Crypto Oracle - CoinMarketCap Integration Test
Test script for migrating from CoinGecko to CoinMarketCap MCP
"""

import requests
from datetime import datetime
import json

class CoinMarketCapOracle:
    """CoinMarketCap Crypto Oracle Implementation"""
    
    def __init__(self):
        # Placeholder for API key - would need to be configured
        self.api_key = "YOUR_CMC_API_KEY_HERE"
        self.base_url = "https://pro-api.coinmarketcap.com"
        
    def get_prices(self):
        """Get BTC/ETH/SOL prices from CoinMarketCap"""
        if self.api_key == "YOUR_CMC_API_KEY_HERE":
            return {
                'status': 'API_KEY_REQUIRED',
                'message': 'Please register at pro.coinmarketcap.com and set your API key'
            }
            
        try:
            url = f"{self.base_url}/v1/cryptocurrency/quotes/latest"
            params = {
                'symbol': 'BTC,ETH,SOL',
                'convert': 'USD'
            }
            headers = {
                'X-CMC_PRO_API_KEY': self.api_key
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'SUCCESS',
                    'data': data
                }
            else:
                return {
                    'status': 'API_ERROR',
                    'error': f"Status Code: {response.status_code}",
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e)
            }

def main():
    print("🦞 CRYPTO ORACLE - COINMARKETCAP INTEGRATION TEST")
    print("=" * 65)
    
    # Test current CoinGecko system
    print("\n🔍 CURRENT SYSTEM: CoinGecko API")
    print("-" * 30)
    
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            cg_data = response.json()
            btc_price = cg_data['bitcoin']['usd']
            eth_price = cg_data['ethereum']['usd']
            sol_price = cg_data['solana']['usd']
            
            print("✅ CoinGecko API Working:")
            print(f"BTC: ${btc_price:,.2f}")
            print(f"ETH: ${eth_price:,.2f}")
            print(f"SOL: ${sol_price:,.2f}")
        else:
            print(f"❌ CoinGecko Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ CoinGecko Connection Error: {e}")
    
    # Test CoinMarketCap integration
    print("\n🔍 PROPOSED SYSTEM: CoinMarketCap MCP")
    print("-" * 30)
    
    cmc = CoinMarketCapOracle()
    result = cmc.get_prices()
    
    if result['status'] == 'SUCCESS':
        print("✅ CoinMarketCap MCP Ready")
        print("Would provide richer data with API key")
    elif result['status'] == 'API_KEY_REQUIRED':
        print("🔑 CoinMarketCap API Key Required")
        print("Visit: https://pro.coinmarketcap.com/signup")
        print("Free tier available - 30 calls/min limit")
    else:
        print(f"❌ CoinMarketCap Test: {result['error']}")
        
    print("\n💡 NEXT STEPS FOR CMC MIGRATION:")
    print("1. Register for CoinMarketCap API key")
    print("2. Configure API key in crypto_oracle_cmc_test.py")
    print("3. Test data accuracy and reliability")
    print("4. Update crypto oracle scripts with dual providers")
    print("5. Gradual migration with CoinGecko fallback")
    print("\n⏰ Current Priority:")
    print("CoinGecko system works perfectly. CMC migration optional enhancement.")

if __name__ == "__main__":
    main()