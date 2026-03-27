#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Test CoinMarketCap API functionality
# Note: Requires API key for full access

def test_coinmarketcap_basic():
    """Test CoinMarketCap API without authentication"""
    try:
        # Try basic endpoint (may require authentication)
        url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        params = {
            'symbol': 'BTC,ETH,SOL',
            'convert': 'USD'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        print("🔍 Testing CoinMarketCap API Access")
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Successfully parsed JSON response")
                print(json.dumps(data, indent=2)[:500] + "...")
            except:
                print("⚠️ Response not JSON (likely redirect or HTML)")
                print(response.text[:200])
        elif response.status_code == 403:
            print("🔒 API requires authentication/API key")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def compare_data_sources():
    """Compare CoinGecko vs CoinMarketCap data quality"""
    print("\n📊 Data Source Comparison")
    print("-" * 30)
    
    # Current CoinGecko implementation
    print("✅ Current Setup: CoinGecko API")
    print("   • Free tier available")
    print("   • No API key required")
    print("   • 10-30 calls/min limit")
    print("   • Broad cryptocurrency coverage")
    print("   • Working reliably for oracle calls")
    
    print("\n🆕 Proposed: CoinMarketCap MCP")
    print("   • Requires API key")
    print("   • 10,000+ cryptocurrencies")
    print("   • Built-in technical analysis")
    print("   • On-chain metrics available")
    print("   • Semantic search capabilities")
    print("   • Pay-per-call option (x402)")
    
    print("\n🔍 Recommendation:")
    print("Current CoinGecko setup is working well.")
    print("CoinMarketCap MCP offers richer features but requires API key.")
    print("Would need to weigh benefits vs complexity of migration.")

# Run tests
if __name__ == "__main__":
    print("🦞 CoinMarketCap API Integration Test")
    print("=" * 50)
    
    test_coinmarketcap_basic()
    compare_data_sources()
    
    print("\n💡 Next Steps:")
    print("1. Get CoinMarketCap API key (free tier available)")
    print("2. Test MCP integration with actual data")
    print("3. Compare data accuracy and update frequency")
    print("4. Decide if migration offers meaningful improvements")