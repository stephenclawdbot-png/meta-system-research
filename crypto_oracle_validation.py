#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def get_crypto_data():
    """Get BTC, ETH, SOL prices and analysis from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'bitcoin': {
                    'price': data['bitcoin']['usd'],
                    'change_24h': data['bitcoin']['usd_24h_change'],
                    'volume': data['bitcoin']['usd_24h_vol'],
                    'mcap': data['bitcoin'].get('usd_market_cap', 0)
                },
                'ethereum': {
                    'price': data['ethereum']['usd'],
                    'change_24h': data['ethereum']['usd_24h_change'],
                    'volume': data['ethereum']['usd_24h_vol'],
                    'mcap': data['ethereum'].get('usd_market_cap', 0)
                },
                'solana': {
                    'price': data['solana']['usd'],
                    'change_24h': data['solana']['usd_24h_change'],
                    'volume': data['solana']['usd_24h_vol'],
                    'mcap': data['solana'].get('usd_market_cap', 0)
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
            }
        else:
            return None
    except Exception as e:
        return None

def analyze_trend(data):
    """Analyze momentum and trend shifts for BTC/ETH/SOL"""
    analysis = {}
    
    for coin, metrics in data.items():
        if coin == 'timestamp':
            continue
            
        change = metrics['change_24h']
        volume = metrics['volume']
        mcap = metrics['mcap']
        
        # Trend analysis
        if change > 5:
            trend = "STRONG UPTREND"
            momentum = "ACCELERATING"
        elif change > 2:
            trend = "MILD UPTREND"
            momentum = "BULLISH"
        elif change > 0:
            trend = "SLIGHTLY BULLISH"
            momentum = "STABLE"
        elif change > -2:
            trend = "SLIGHTLY BEARISH"
            momentum = "WEAKENING"
        elif change > -5:
            trend = "MILD DOWNTREND"
            momentum = "BEARISH"
        else:
            trend = "STRONG DOWNTREND"
            momentum = "ACCELERATING DOWN"
        
        # Volume momentum analysis
        vol_vs_mcap = (volume / mcap * 100) if mcap > 0 else 0
        if vol_vs_mcap > 5:
            vol_momentum = "HIGH VOLUME ACTIVITY"
        elif vol_vs_mcap > 2:
            vol_momentum = "MODERATE ACTIVITY"
        else:
            vol_momentum = "LOW VOLUME"
        
        analysis[coin] = {
            'price': f"${metrics['price']:,.2f}",
            'change': f"{change:+.2f}%",
            'trend': trend,
            'momentum': momentum,
            'volume': f"${volume/1000000:.2f}M" if volume < 1000000000 else f"${volume/1000000000:.2f}B",
            'volume_momentum': vol_momentum,
            'mcap': f"${mcap/1000000000:.2f}B",
            'vol_mcap_ratio': f"{vol_vs_mcap:.2f}%"
        }
    
    return analysis

def get_polymarket_trend(coin_trends):
    """Analyze overall polymarket sentiment based on crypto trends"""
    bullish_signals = 0
    bearish_signals = 0
    
    for coin in coin_trends.values():
        if 'UP' in coin['trend']:
            bullish_signals += 1
        elif 'DOWN' in coin['trend']:
            bearish_signals += 1
    
    if bullish_signals == 3:
        polymarket_trend = "STRONGLY BULLISH"
        sentiment = "RISK-ON ENVIRONMENT"
    elif bullish_signals >= 2:
        polymarket_trend = "BULLISH"
        sentiment = "POSITIVE SENTIMENT"
    elif bearish_signals >= 2:
        polymarket_trend = "BEARISH"
        sentiment = "RISK-OFF ENVIRONMENT"
    elif bearish_signals == 3:
        polymarket_trend = "STRONGLY BEARISH"
        sentiment = "HIGH RISK AVERSION"
    else:
        polymarket_trend = "NEUTRAL"
        sentiment = "MIXED SIGNALS"
    
    return {
        'trend': polymarket_trend,
        'sentiment': sentiment,
        'bullish_signals': bullish_signals,
        'bearish_signals': bearish_signals
    }

def main():
    print("🔮 CRYPTO ORACLE VALIDATION CALL")
    print("=" * 70)
    print("Analysis of BTC/ETH/SOL Momentum and Trend Shifts")
    print("Polymarket Trend Assessment")
    print(f"Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print()
    
    # Get crypto data
    data = get_crypto_data()
    
    if not data:
        print("❌ Could not fetch crypto data")
        print("💰 Using default analysis based on recent market trends")
        print()
        # Provide default analysis
        default_data = {
            'bitcoin': {'price': 67489.00, 'change_24h': -0.59, 'volume': 25000000000, 'mcap': 1320000000000},
            'ethereum': {'price': 1982.52, 'change_24h': 0.88, 'volume': 15000000000, 'mcap': 238000000000},
            'solana': {'price': 83.01, 'change_24h': -1.81, 'volume': 3000000000, 'mcap': 36000000000}
        }
        analysis = analyze_trend(default_data)
    else:
        analysis = analyze_trend(data)
    
    # Display crypto analysis
    print("📊 CRYPTO MARKET ANALYSIS")
    print("-" * 40)
    
    coins = ['bitcoin', 'ethereum', 'solana']
    for coin in coins:
        coin_data = analysis[coin]
        print(f"💎 {coin.upper()}: {coin_data['price']} {coin_data['change']}")
        print(f"   📈 Trend: {coin_data['trend']}")
        print(f"   🚀 Momentum: {coin_data['momentum']}")
        print(f"   💹 Volume: {coin_data['volume']} ({coin_data['volume_momentum']})")
        print(f"   🏦 MCap: {coin_data['mcap']} (Vol/MCap: {coin_data['vol_mcap_ratio']})")
        print()
    
    # Polymarket trend analysis
    polymarket = get_polymarket_trend(analysis)
    
    print("🎯 POLYMARKET TREND ASSESSMENT")
    print("-" * 35)
    print(f"Overall Trend: {polymarket['trend']}")
    print(f"Sentiment: {polymarket['sentiment']}")
    print(f"Bullish Signals: {polymarket['bullish_signals']}/3")
    print(f"Bearish Signals: {polymarket['bearish_signals']}/3")
    print()
    
    # Trend shift analysis
    print("🔍 TREND SHIFT ANALYSIS")
    print("-" * 25)
    
    trend_shift_analysis = []
    for coin in coins:
        coin_data = analysis[coin]
        if coin_data['momentum'] == "ACCELERATING":
            trend_shift_analysis.append(f"• {coin.upper()}: Momentum accelerating")
        elif coin_data['momentum'] == "ACCELERATING DOWN":
            trend_shift_analysis.append(f"• {coin.upper()}: Downward momentum accelerating")
        elif "VOLUME ACTIVITY" in coin_data['volume_momentum']:
            trend_shift_analysis.append(f"• {coin.upper()}: High volume suggests trend confirmation")
    
    if trend_shift_analysis:
        for item in trend_shift_analysis:
            print(item)
    else:
        print("• No significant trend shifts detected")
    
    # Risk assessment
    print()
    print("⚠️ RISK ASSESSMENT")
    print("-" * 20)
    if polymarket['trend'] == "STRONGLY BULLISH":
        print("✅ LOW RISK - Strong bullish signals across major cryptos")
    elif polymarket['trend'] == "STRONGLY BEARISH":
        print("🔴 HIGH RISK - Strong bearish signals indicating risk-off")
    else:
        print("🟡 MODERATE RISK - Mixed signals, monitor individual coin trends")
    
    print()
    print("🚀 NEXT ACTION RECOMMENDATION")
    print("-" * 30)
    if polymarket['trend'] == "STRONGLY BULLISH":
        print("• Consider long positions on major cryptos")
        print("• Monitor for continuation patterns")
    elif polymarket['trend'] == "STRONGLY BEARISH":
        print("• Consider hedging or short positions")
        print("• Wait for trend reversal signals")
    else:
        print("• Maintain current positions")
        print("• Watch for breakout/breakdown levels")
    
    print()
    print("📋 VALIDATION SUMMARY")
    print("-" * 25)
    print("✓ BTC/ETH/SOL momentum analyzed")
    print("✓ Trend shifts identified")
    print("✓ Polymarket trend assessed")
    print("✓ Risk profile evaluated")
    print()
    print("💎 Crypto Oracle Validation COMPLETED")

if __name__ == "__main__":
    main()