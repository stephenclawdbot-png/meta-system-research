#!/usr/bin/env python3
import requests

print("🔍 Testing DexScreener API...")

url = "https://api.dexscreener.com/latest/dex/tokens/trending"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

try:
    print(f"📡 Making request to: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Content-Type: {response.headers.get('content-type')}")
    print(f"✅ Content Length: {len(response.text)} characters")
    
    # Try to parse JSON
    if response.status_code == 200:
        data = response.json()
        print(f"✅ JSON parsed successfully")
        print(f"✅ Keys in response: {list(data.keys()) if data else 'None'}")
        
        if data and 'pairs' in data:
            print(f"✅ Found {len(data['pairs'])} pairs")
            # Show first few pairs
            for i in range(min(3, len(data['pairs']))):
                pair = data['pairs'][i]
                symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
                mcap = pair.get('marketCap', 0)
                print(f"   - {symbol}: ${mcap:,.0f} mcap")
        else:
            print("❌ No 'pairs' key in response")
            print(f"Full response: {data}")
    else:
        print(f"❌ Non-200 response: {response.text[:200]}...")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()