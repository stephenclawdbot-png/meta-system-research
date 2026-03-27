#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def get_coingecko_small_caps():
    """Get small cap coins from CoinGecko"""
    print("Scanning CoinGecko for small cap coins...")
    try:
        # Start from rank 1000+ to get smaller coins
        for page in range(5, 15):  # Pages 5-14
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page={page}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                memecoins = []
                
                for coin in data:
                    mcap = coin.get('market_cap', 0)
                    rank = coin.get('market_cap_rank', 9999)
                    
                    # Target sub-200k MCap coins
                    if mcap and 30000 <= mcap <= 200000:
                        memecoins.append({
                            'name': coin.get('name', 'N/A'),
                            'symbol': coin.get('symbol', '').upper(),
                            'mcap': mcap,
                            'price': coin.get('current_price', 0),
                            'volume_24h': coin.get('total_volume', 0),
                            'rank': rank
                        })
                
                if memecoins:
                    print(f"\nSmall cap gems from CoinGecko (Rank {rank} range):")
                    for coin in memecoins:
                        print(f"  {coin['symbol']} ({coin['name']}):")
                        print(f"    MCap: ${coin['mcap']:,.0f}")
                        print(f"    Price: ${coin['price']:.8f}")
                        print(f"    24h Volume: ${coin['volume_24h']:,.0f}")
                        print(f"    Rank: #{coin['rank']}")
                    return memecoins
                
            else:
                print(f"CoinGecko API error on page {page}: {response.status_code}")
    except Exception as e:
        print(f"Error accessing CoinGecko: {e}")
    
    return []

def analyze_trends():
    """Look for memecoin trends"""
    print("\n🔍 Analyzing memecoin landscape...")
    
    # Check what memecoins are trending
    try:
        trending_response = requests.get("https://api.coingecko.com/api/v3/search/trending")
        if trending_response.status_code == 200:
            trending_data = trending_response.json()
            coins = trending_data.get('coins', [])
            memecoin_trends = []
            
            for coin_info in coins[:10]:
                coin = coin_info.get('item', {})
                mcap = coin.get('market_cap', 0)
                
                if mcap and 30000 <= mcap <= 200000:
                    memecoin_trends.append({
                        'name': coin.get('name', 'N/A'),
                        'symbol': coin.get('symbol', '').upper(),
                        'mcap': mcap,
                        'rank': coin.get('market_cap_rank', 9999)
                    })
            
            if memecoin_trends:
                print("\n🔥 Trending small cap memecoins:")
                for coin in memecoin_trends:
                    print(f"  {coin['symbol']} - ${coin['mcap']:,.0f} MCap")
            else:
                print("No trending small cap memecoins found")
    except Exception as e:
        print(f"Trending API error: {e}")

def main():
    print("🏃 Alpha Scanner Cron Job - Running at", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("="*60)
    
    small_caps = get_coingecko_small_caps()
    
    if not small_caps:
        print("\n⚠️ No small cap gems found in 30k-200k range")
        print("This could mean:")
        print("- Most memecoins are outside this range")
        print("- API limitations preventing access")
        print("- Need to check specific memecoin platforms")
    
    analyze_trends()
    
    print("\n" + "="*60)
    print("💡 Manual Checks Recommended:")
    print("- Direct pump.fun browsing")
    print("- DexScreener Solana new pairs")
    print("- Telegram crypto alpha groups")
    
if __name__ == "__main__":
    main()