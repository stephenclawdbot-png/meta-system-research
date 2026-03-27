import json, sys
import urllib.request

# Fetch data from DexScreener API
url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
with urllib.request.urlopen(url) as response:
    data = json.load(response)

memecoins = []
for pair in data.get('pairs', []):
    mcap = pair.get('marketCap', 0)
    if mcap and 30000 <= mcap <= 200000:
        memecoins.append(pair)

print(f'Found {len(memecoins)} memecoins in 30k-200k mcap range:')
print()
for coin in memecoins[:10]:
    print(f"{coin['baseToken']['symbol']} ({coin['baseToken']['name']})")
    print(f"  Market Cap: ${coin['marketCap']:,}")
    print(f"  24h Volume: ${coin['volume']['h24']:,}")
    print(f"  Price: ${coin['priceUsd']}")
    change = coin.get('priceChange', {}).get('h24', 0)
    print(f"  24h Change: {change}%")
    print(f"  Liquidity: ${coin['liquidity']['usd']:,}")
    print(f"  URL: {coin['url']}")
    print()