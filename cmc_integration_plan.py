#!/usr/bin/env python3
import requests
from datetime import datetime

class CoinMarketCapMCP:
    """CoinMarketCap MCP Integration Framework"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com"
        self.mcp_url = "https://mcp.coinmarketcap.com/mcp"
        
    def get_latest_prices(self, symbols=["BTC", "ETH", "SOL"]):
        """Get latest prices from CoinMarketCap API"""
        if not self.api_key:
            return "API key required"
            
        try:
            url = f"{self.base_url}/v1/cryptocurrency/quotes/latest"
            params = {
                'symbol': ','.join(symbols),
                'convert': 'USD'
            }
            headers = {
                'X-CMC_PRO_API_KEY': self.api_key
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return f"API Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {e}"

class CoinGeckoIntegration:
    """Current CoinGecko Integration"""
    
    def get_latest_prices(self):
        """Get latest prices using current CoinGecko API"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,solana',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return f"API Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

def compare_systems():
    """Compare CoinGecko vs CoinMarketCap systems"""
    
    print("🦞 CRYPTO ORACLE DATA SOURCE COMPARISON")
    print("=" * 60)
    print("\n📊 CURRENT SYSTEM: CoinGecko API")
    print("-" * 30)
    print("✅ Advantages:")
    print("   • No API key required")
    print("   • Free tier with generous limits")
    print("   • Proven reliability with our oracle")
    print("   • Simple integration")
    print("   • Broad cryptocurrency coverage")
    print("\n❌ Limitations:")
    print("   • Limited advanced technical analysis")
    print("   • No built-in entity recognition (MCP)")
    print("   • Basic pricing data only")
    
    print("\n🔮 PROPOSED SYSTEM: CoinMarketCap MCP")
    print("-" * 35)
    print("✅ Advantages:")
    print("   • 10,000+ cryptocurrencies")
    print("   • Built-in technical analysis tools")
    print("   • On-chain metrics available")
    print("   • Semantic search capabilities")
    print("   • Pay-per-call option (x402)")
    print("   • MCP protocol for AI-native integration")
    print("\n❌ Disadvantages:")
    print("   • Requires API key management")
    print("   • Potential rate limits on free tier")
    print("   • More complex integration")
    print("   • Potential costs for heavy usage")
    
    print("\n💡 Migration Path:")
    print("1. Get CoinMarketCap API key (free tier)")
    print("2. Create dual integration (CoinGecko fallback)")
    print("3. Test CoinMarketCap data accuracy/update frequency")
    print("4. Gradually transition with monitoring")
    print("5. Full transition once proven reliable")  

def current_system_test():
    """Test current CoinGecko system"""
    print("\n🔍 TESTING CURRENT COINGECKO SYSTEM")
    print("-" * 35)
    
    cg = CoinGeckoIntegration()
    data = cg.get_latest_prices()
    
    if isinstance(data, dict):
        print("✅ CoinGecko API Working Perfectly")
        print(f"BTC: ${data['bitcoin']['usd']:,.2f} ({data['bitcoin']['usd_24h_change']:+.2f}%)")
        print(f"ETH: ${data['ethereum']['usd']:,.2f} ({data['ethereum']['usd_24h_change']:+.2f}%)")
        print(f"SOL: ${data['solana']['usd']:,.2f} ({data['solana']['usd_24h_change']:+.2f}%)")
    else:
        print(f"❌ CoinGecko Error: {data}")

if __name__ == "__main__":
    compare_systems()
    current_system_test()
    
    print("\n🎯 IMMEDIATE RECOMMENDATION:")
    print("Current CoinGecko system is working excellently.")
    print("CoinMarketCap MCP offers future benefits but requires investment.")
    print("\n💡 Action Plan:")
    print("1. Register for CoinMarketCap API (exploration)")
    print("2. Test side-by-side with current system")  
    print("3. Migrate if meaningful improvements identified")
    print("4. Keep CoinGecko as fallback during transition")