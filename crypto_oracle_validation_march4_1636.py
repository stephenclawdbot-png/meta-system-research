import requests
import json
from datetime import datetime

# Get crypto prices from CoinGecko API
def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Error fetching data: {response.status_code}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None

# Simple trend analysis
def analyze_trends(prices):
    trends = {}
    for coin, data in prices.items():
        change = data.get('usd_24h_change', 0)
        if change > 3:
            trend = 'STRONG UPTREND'
        elif change > 1:
            trend = 'UPTREND'
        elif change < -3:
            trend = 'STRONG DOWNTREND'
        elif change < -1:
            trend = 'DOWNTREND'
        else:
            trend = 'SIDEWAYS'
        
        trends[coin] = {
            'price': data['usd'],
            '24h_change': change,
            'market_cap': data.get('usd_market_cap', 0),
            'trend': trend
        }
    
    return trends

# Main analysis
def main():
    print('🚀 CRYPTO ORACLE VALIDATION CALL - Polymarket Trends & Momentum Analysis')
    print('=' * 70)
    print(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # Get current prices
    prices = get_crypto_prices()
    if not prices:
        print('❌ Failed to fetch crypto data')
        return
    
    # Analyze trends
    trends = analyze_trends(prices)
    
    # Display results
    print('📊 BTC/ETH/SOL MOMENTUM ANALYSIS:')
    print('-' * 50)
    
    for coin, data in trends.items():
        coin_name = coin.upper()
        print(f'{coin_name:8} | ${data["price"]:,.2f} | {data["24h_change"]:+.2f}% | {data["trend"]}')
    
    print()
    
    # Overall market sentiment
    bullish_count = sum(1 for data in trends.values() if 'UPTREND' in data['trend'])
    bearish_count = sum(1 for data in trends.values() if 'DOWNTREND' in data['trend'])
    
    if bullish_count >= 2:
        sentiment = 'BULLISH'
    elif bearish_count >= 2:
        sentiment = 'BEARISH'
    else:
        sentiment = 'MIXED'
    
    print(f'🏦 MARKET SENTIMENT: {sentiment}')
    print(f'📈 Bullish assets: {bullish_count}/3')
    print(f'📉 Bearish assets: {bearish_count}/3')
    
    # Key levels to watch
    print()
    print('🎯 KEY LEVELS TO WATCH:')
    print('- BTC: $65K (support), $70K (resistance)')
    print('- ETH: $3,500 (support), $4,000 (resistance)')
    print('- SOL: $150 (support), $180 (resistance)')
    
    print()
    print('💡 NEXT VALIDATION: 30 minutes')

if __name__ == '__main__':
    main()