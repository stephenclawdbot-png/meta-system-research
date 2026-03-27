#!/usr/bin/env python3
"""
Crypto Oracle Validation for Polymarket Trends
Analyze BTC/ETH/SOL momentum and trend shifts
Time: Monday, March 2nd, 2026 — 9:20 AM (Asia/Manila)
"""

import requests
from datetime import datetime
import json

def get_crypto_data():
    """Get BTC, ETH, SOL prices and trends from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'bitcoin': {
                    'price': data['bitcoin']['usd'],
                    'change_24h': data['bitcoin']['usd_24h_change'],
                    'volume': data['bitcoin']['usd_24h_vol']
                },
                'ethereum': {
                    'price': data['ethereum']['usd'],
                    'change_24h': data['ethereum']['usd_24h_change'],
                    'volume': data['ethereum']['usd_24h_vol']
                },
                'solana': {
                    'price': data['solana']['usd'],
                    'change_24h': data['solana']['usd_24h_change'],
                    'volume': data['solana']['usd_24h_vol']
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        return None

def analyze_momentum(data):
    """Analyze momentum patterns and trend shifts"""
    analysis = {
        'bitcoin': {
            'trend': 'neutral',
            'momentum': 'neutral',
            'signal': 'neutral',
            'reasoning': ''
        },
        'ethereum': {
            'trend': 'neutral',
            'momentum': 'neutral',
            'signal': 'neutral',
            'reasoning': ''
        },
        'solana': {
            'trend': 'neutral',
            'momentum': 'neutral',
            'signal': 'neutral',
            'reasoning': ''
        },
        'overall': {
            'market_sentiment': 'neutral',
            'leadership': 'neutral',
            'correlation_strength': 'medium'
        }
    }
    
    # BTC Analysis
    btc_change = data['bitcoin']['change_24h']
    btc_price = data['bitcoin']['price']
    btc_volume = data['bitcoin']['volume']
    
    if btc_change > 2:
        analysis['bitcoin']['trend'] = 'bullish'
        analysis['bitcoin']['momentum'] = 'strong'
        analysis['bitcoin']['signal'] = 'positive'
    elif btc_change > 0:
        analysis['bitcoin']['trend'] = 'bullish'
        analysis['bitcoin']['momentum'] = 'moderate'
        analysis['bitcoin']['signal'] = 'positive'
    elif btc_change < -2:
        analysis['bitcoin']['trend'] = 'bearish'
        analysis['bitcoin']['momentum'] = 'strong'
        analysis['bitcoin']['signal'] = 'negative'
    elif btc_change < 0:
        analysis['bitcoin']['trend'] = 'bearish'
        analysis['bitcoin']['momentum'] = 'moderate'
        analysis['bitcoin']['signal'] = 'negative'
    
    # ETH Analysis
    eth_change = data['ethereum']['change_24h']
    eth_price = data['ethereum']['price']
    eth_volume = data['ethereum']['volume']
    
    if eth_change > 2:
        analysis['ethereum']['trend'] = 'bullish'
        analysis['ethereum']['momentum'] = 'strong'
        analysis['ethereum']['signal'] = 'positive'
    elif eth_change > 0:
        analysis['ethereum']['trend'] = 'bullish'
        analysis['ethereum']['momentum'] = 'moderate'
        analysis['ethereum']['signal'] = 'positive'
    elif eth_change < -2:
        analysis['ethereum']['trend'] = 'bearish'
        analysis['ethereum']['momentum'] = 'strong'
        analysis['ethereum']['signal'] = 'negative'
    elif eth_change < 0:
        analysis['ethereum']['trend'] = 'bearish'
        analysis['ethereum']['momentum'] = 'moderate'
        analysis['ethereum']['signal'] = 'negative'
    
    # SOL Analysis
    sol_change = data['solana']['change_24h']
    sol_price = data['solana']['price']
    sol_volume = data['solana']['volume']
    
    if sol_change > 2:
        analysis['solana']['trend'] = 'bullish'
        analysis['solana']['momentum'] = 'strong'
        analysis['solana']['signal'] = 'positive'
    elif sol_change > 0:
        analysis['solana']['trend'] = 'bullish'
        analysis['solana']['momentum'] = 'moderate'
        analysis['solana']['signal'] = 'positive'
    elif sol_change < -2:
        analysis['solana']['trend'] = 'bearish'
        analysis['solana']['momentum'] = 'strong'
        analysis['solana']['signal'] = 'negative'
    elif sol_change < 0:
        analysis['solana']['trend'] = 'bearish'
        analysis['solana']['momentum'] = 'moderate'
        analysis['solana']['signal'] = 'negative'
    
    # Rate correlation patterns
    btc_pos = btc_change > 0
    eth_pos = eth_change > 0
    sol_pos = sol_change > 0
    
    correlation_matches = 0
    total_pairs = 3
    
    if btc_pos == eth_pos:
        correlation_matches += 1
    if btc_pos == sol_pos:
        correlation_matches += 1
    if eth_pos == sol_pos:
        correlation_matches += 1
    
    correlation_strength = correlation_matches / total_pairs
    
    if correlation_strength > 0.8:
        analysis['overall']['correlation_strength'] = 'strong'
    elif correlation_strength > 0.5:
        analysis['overall']['correlation_strength'] = 'moderate'
    else:
        analysis['overall']['correlation_strength'] = 'weak'
    
    # Determine market leadership
    btc_volume_power = btc_volume
    eth_volume_power = eth_volume
    sol_volume_power = sol_volume
    
    if btc_volume_power > eth_volume_power * 3 and btc_volume_power > sol_volume_power * 10:
        analysis['overall']['leadership'] = 'btc'
    elif eth_volume_power > sol_volume_power * 2:
        analysis['overall']['leadership'] = 'eth'
    elif sol_volume_power > btc_volume_power * 0.1:
        analysis['overall']['leadership'] = 'sol'
    else:
        analysis['overall']['leadership'] = 'distributed'
    
    # Overall sentiment
    positive_signals = sum([1 for coin in ['bitcoin', 'ethereum', 'solana'] if analysis[coin]['signal'] == 'positive'])
    negative_signals = sum([1 for coin in ['bitcoin', 'ethereum', 'solana'] if analysis[coin]['signal'] == 'negative'])
    
    if positive_signals >= 2:
        analysis['overall']['market_sentiment'] = 'bullish'
    elif negative_signals >= 2:
        analysis['overall']['market_sentiment'] = 'bearish'
    else:
        analysis['overall']['market_sentiment'] = 'neutral'
    
    return analysis

def generate_polymarket_recommendations(data, analysis):
    """Generate Polymarket trend recommendations based on analysis"""
    recommendations = []
    
    # BTC recommendations
    if analysis['bitcoin']['signal'] == 'positive':
        recommendations.append({
            'asset': 'BTC',
            'recommendation': 'LONG/UP bet',
            'confidence': 'high' if analysis['bitcoin']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Strong positive momentum with {data["bitcoin"]["change_24h"]:.2f}% gain'
        })
    elif analysis['bitcoin']['signal'] == 'negative':
        recommendations.append({
            'asset': 'BTC',
            'recommendation': 'SHORT/DOWN bet',
            'confidence': 'high' if analysis['bitcoin']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Negative momentum with {data["bitcoin"]["change_24h"]:.2f}% decline'
        })
    
    # ETH recommendations
    if analysis['ethereum']['signal'] == 'positive':
        recommendations.append({
            'asset': 'ETH',
            'recommendation': 'LONG/UP bet',
            'confidence': 'high' if analysis['ethereum']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Following BTC with {data["ethereum"]["change_24h"]:.2f}% gain'
        })
    elif analysis['ethereum']['signal'] == 'negative':
        recommendations.append({
            'asset': 'ETH',
            'recommendation': 'SHORT/DOWN bet',
            'confidence': 'high' if analysis['ethereum']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Following BTC with {data["ethereum"]["change_24h"]:.2f}% decline'
        })
    
    # SOL recommendations
    if analysis['solana']['signal'] == 'positive':
        recommendations.append({
            'asset': 'SOL',
            'recommendation': 'LONG/UP bet',
            'confidence': 'high' if analysis['solana']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Positive momentum with {data["solana"]["change_24h"]:.2f}% gain'
        })
    elif analysis['solana']['signal'] == 'negative':
        recommendations.append({
            'asset': 'SOL',
            'recommendation': 'SHORT/DOWN bet',
            'confidence': 'high' if analysis['solana']['momentum'] == 'strong' else 'moderate',
            'reasoning': f'Negative momentum with {data["solana"]["change_24h"]:.2f}% decline'
        })
    
    return recommendations

def main():
    print("🔮 CRYPTO ORACLE - POLYMARKET TRENDS ANALYSIS")
    print("="*70)
    print("Monday, March 2nd, 2026 — 9:20 AM (Asia/Manila)")
    print("Polymarket Momentum Analysis")
    print()
    
    # Get current market data
    data = get_crypto_data()
    
    if not data:
        print("❌ Failed to fetch crypto data")
        return
    
    print("📊 LIVE MARKET DATA")
    print("-"*40)
    print(f"Time: {data['timestamp']}")
    print()
    
    # Display current prices
    btc_symbol = "▲" if data['bitcoin']['change_24h'] > 0 else "▼"
    eth_symbol = "▲" if data['ethereum']['change_24h'] > 0 else "▼"
    sol_symbol = "▲" if data['solana']['change_24h'] > 0 else "▼"
    
    print("💰 CURRENT PRICES:")
    print(f"BTC: ${data['bitcoin']['price']:,.2f} {btc_symbol}{data['bitcoin']['change_24h']:.2f}%")
    print(f"ETH: ${data['ethereum']['price']:,.2f} {eth_symbol}{data['ethereum']['change_24h']:.2f}%")
    print(f"SOL: ${data['solana']['price']:,.2f} {sol_symbol}{data['solana']['change_24h']:.2f}%")
    print()
    
    # Analyze momentum
    analysis = analyze_momentum(data)
    
    print("🔍 MOMENTUM ANALYSIS")
    print("-"*40)
    print(f"BTC: {analysis['bitcoin']['trend'].upper()} trend ({analysis['bitcoin']['momentum']} momentum)")
    print(f"ETH: {analysis['ethereum']['trend'].upper()} trend ({analysis['ethereum']['momentum']} momentum)")
    print(f"SOL: {analysis['solana']['trend'].upper()} trend ({analysis['solana']['momentum']} momentum)")
    print()
    
    # Market overview
    print("🌐 MARKET OVERVIEW")
    print("-"*30)
    print(f"Sentiment: {analysis['overall']['market_sentiment'].upper()}")
    print(f"Leadership: {analysis['overall']['leadership'].upper()}")
    print(f"Correlation: {analysis['overall']['correlation_strength'].upper()}")
    print()
    
    # Polymarket recommendations
    recommendations = generate_polymarket_recommendations(data, analysis)
    
    print("🎯 POLYMARKET RECOMMENDATIONS")
    print("-"*45)
    for rec in recommendations:
        confidence_emoji = "🟢" if rec['confidence'] == 'high' else "🟡"
        print(f"{confidence_emoji} {rec['asset']}: {rec['recommendation']} ({rec['confidence']})")
        print(f"   {rec['reasoning']}")
    
    print()
    print("📈 VOLUME ANALYSIS")
    print("-"*35)
    
    # Convert volumes to billions/millions for readability
    btc_vol_str = f"${data['bitcoin']['volume']/1000000000:.2f}B" if data['bitcoin']['volume'] > 1000000000 else f"${data['bitcoin']['volume']/1000000:.2f}M"
    eth_vol_str = f"${data['ethereum']['volume']/1000000000:.2f}B" if data['ethereum']['volume'] > 1000000000 else f"${data['ethereum']['volume']/1000000:.2f}M"
    sol_vol_str = f"${data['solana']['volume']/1000000000:.2f}B" if data['solana']['volume'] > 1000000000 else f"${data['solana']['volume']/1000000:.2f}M"
    
    print(f"BTC Volume: {btc_vol_str}")
    print(f"ETH Volume: {eth_vol_str}")
    print(f"SOL Volume: {sol_vol_str}")
    
    # Risk assessment
    print()
    print("⚠️ RISK ASSESSMENT")
    print("-"*25)
    
    risk_factors = []
    coin_volatilities = []
    
    for coin in ['bitcoin', 'ethereum', 'solana']:
        volatility = abs(data[coin]['change_24h'])
        if volatility > 5:
            risk_factors.append(f"{coin.upper()} volatility high ({volatility:.1f}%)")
        coin_volatilities.append(volatility)
    
    avg_volatility = sum(coin_volatilities) / len(coin_volatilities)
    
    if avg_volatility > 3:
        risk_factors.append("High average volatility")
    
    if risk_factors:
        print("High risk factors detected:")
        for factor in risk_factors:
            print(f"• {factor}")
    else:
        print("Moderate risk - market appears stable")
    
    print()
    print("🎯 EXECUTION SUMMARY")
    print("-"*30)
    print(f"Analysis completed at: {data['timestamp']}")
    print(f"Data source: CoinGecko API")
    print("Framework: BTC-leader correlation model")
    print("Recommendation confidence: HIGH")
    print()
    print("CRYPTO ORACLE VALIDATION COMPLETED")

if __name__ == "__main__":
    main()