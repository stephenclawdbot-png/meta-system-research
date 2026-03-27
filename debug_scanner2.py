#!/usr/bin/env python3
import requests
import json

print("🔍 Testing DexScreener API...")

url = "https://api.dexscreener.com/latest/dex/tokens/trending"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

try:
    print(f"📡 Making request to: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Raw response text: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ JSON parsed: {data}")
        
        # Try direct fetch instead of trending
        print("\n📡 Trying direct tokens fetch...")
        url2 = "https://api.dexscreener.com/latest/dex/tokens/solana"
        response2 = requests.get(url2, headers=headers, timeout=10)
        print(f"✅ Status Code (solana): {response2.status_code}")
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Solana tokens count: {len(data2['pairs']) if 'pairs' in data2 else 'N/A'}")
            if 'pairs' in data2:
                for i in range(min(5, len(data2['pairs']))):
                    pair = data2['pairs'][i]
                    symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                    mcap = pair.get('fdv', 0)
                    print(f"   - {symbol}: ${mcap:,.0f} fdv")
                    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()