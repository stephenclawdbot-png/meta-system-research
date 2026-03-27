#!/usr/bin/env python3
import requests
from datetime import datetime

# Get current crypto data
def get_crypto_data():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true'
    response = requests.get(url)
    data = response.json()
    
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M GMT+8'),
        'BTC': {
            'price': data['bitcoin']['usd'],
            'change_24h': data['bitcoin']['usd_24h_change'],
            'volume': data['bitcoin']['usd_24h_vol'],
            'mcap': data['bitcoin']['usd_market_cap']
        },
        'ETH': {
            'price': data['ethereum']['usd'],
            'change_24h': data['ethereum']['usd_24h_change'],
            'volume': data['ethereum']['usd_24h_vol'],
            'mcap': data['ethereum']['usd_market_cap']
        },
        'SOL': {
            'price': data['solana']['usd'],
            'change_24h': data['solana']['usd_24h_change'],
            'volume': data['solana']['usd_24h_vol'],
            'mcap': data['solana']['usd_market_cap']
        }
    }

# Analyze momentum trends
def analyze_trends(data):
    trends = {}
    for symbol, info in data.items():
        if symbol != 'timestamp':
            change = info['change_24h']
            
            # Momentum analysis
            if change > 5:
                momentum = 'STRONG_BULLISH'
                trend_dir = 'STRONG_UPTREND'
            elif change > 2:
                momentum = 'BULLISH'
                trend_dir = 'UPTREND'
            elif change > -2:
                momentum = 'NEUTRAL'
                trend_dir = 'SIDEWAYS'
            elif change > -5:
                momentum = 'BEARISH'
                trend_dir = 'DOWNTREND'
            else:
                momentum = 'STRONG_BEARISH'
                trend_dir = 'STRONG_DOWNTREND'
            
            # Volume analysis
            vol_ratio = info['volume'] / info['mcap']
            if vol_ratio > 0.05:
                vol_strength = 'HIGH_VOLUME'
            elif vol_ratio > 0.02:
                vol_strength = 'MODERATE_VOLUME'
            else:
                vol_strength = 'LOW_VOLUME'
            
            trends[symbol] = {
                'momentum': momentum,
                'trend': trend_dir,
                'volume': vol_strength,
                'vol_ratio': vol_ratio
            }
    
    return trends

# Generate oracle summary
def generate_oracle_summary():
    data = get_crypto_data()
    trends = analyze_trends(data)
    
    print('🔮 CRYPTO ORACLE VALIDATION - POLYMARKET TRENDS')
    print('=' * 70)
    print(f'Scan Time: {data["timestamp"]}')
    print()
    
    print('📊 REAL-TIME MARKET POSITION:')
    print('-' * 40)
    for symbol in ['BTC', 'ETH', 'SOL']:
        info = data[symbol]
        change_symbol = '▲' if info['change_24h'] > 0 else '▼'
        print(f'{symbol}: ${info["price"]:,.2f} {change_symbol}{info["change_24h"]:.2f}% | Vol: ${info["volume"]/1e9:.1f}B')
    
    print()
    print('⚡ MOMENTUM ANALYSIS:')
    print('-' * 25)
    for symbol, trend in trends.items():
        print(f'{symbol}: {trend["momentum"]} | Trend: {trend["trend"]}')
    
    print()
    print('🎯 POLYMARKET TRADING VIEW:')
    print('-' * 30)
    total_bearish = sum(1 for t in trends.values() if 'BEARISH' in t['momentum'])
    total_bullish = sum(1 for t in trends.values() if 'BULLISH' in t['momentum'])
    
    if total_bearish >= 2:
        print('MARKET BIAS: BEARISH - Consider short positions')
    elif total_bullish >= 2:
        print('MARKET BIAS: BULLISH - Consider long positions')
    else:
        print('MARKET BIAS: MIXED - Hedging recommended')
    
    print()
    print('🔍 TREND SHIFT INDICATORS:')
    print('-' * 30)
    shift_indicators = []
    for symbol, trend in trends.items():
        if 'STRONG' in trend['momentum'] and trend['volume'] == 'HIGH_VOLUME':
            shift_indicators.append(f'{symbol}: Strong momentum with high volume - potential trend acceleration')
    
    if shift_indicators:
        for indicator in shift_indicators:
            print(f'• {indicator}')
    else:
        print('• Current trends appear stable')
    
    print()
    print('💰 VOLUME ANALYSIS:')
    print('-' * 20)
    for symbol, trend in trends.items():
        print(f'{symbol}: {trend["volume"]} (ratio: {trend["vol_ratio"]:.3f})')
    
    print()
    print('🚀 POLYMARKET IMPLICATIONS:')
    print('-' * 30)
    print('• High volume + strong momentum: Look for trend continuation markets')
    print('• Market-wide bearish sentiment: Consider inverse/hedge positions')
    print('• Strong correlation moves: Monitor BTC dominance patterns')
    
    print()
    print('📈 MARKET STATUS: ✓ ANALYSIS COMPLETE')

generate_oracle_summary()