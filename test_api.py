import requests

cg_api = "https://api.coingecko.com/api/v3/simple/price"
response = requests.get(cg_api + "?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")

if response.status_code == 200:
    data = response.json()
    print("CoinGecko API working - Prices:")
    for coin in ["bitcoin", "ethereum", "solana"]:
        if coin in data:
            price = data[coin]["usd"]
            change = data[coin]["usd_24h_change"]
            print(f"{coin.upper()}: ${price:.2f} ({change:.2f}%)")
else:
    print("CoinGecko API failed")