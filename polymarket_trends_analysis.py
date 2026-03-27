#!/usr/bin/env python3
"""
POLYMARKET TRENDS ANALYSIS
Analyzes BTC/ETH/SOL momentum shifts, institutional flows, and trend reversals
Provides actionable insights for polymarket betting decisions
"""

import requests
import json
from datetime import datetime

def fetch_market_data():
    """Fetch comprehensive crypto market data"""
    try:
        # Get prices and 24h changes from CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def analyze_momentum_trends(price_data):
    """Analyze momentum and trend shifts"""
    trends = {}
    
    for coin_id, data in price_data.items():
        price = data.get('usd', 0)
        change_24h = data.get('usd_24h_change', 0)
        market_cap = data.get('usd_market_cap', 0)
        volume = data.get('usd_24h_vol', 0)
        
        coin_name = coin_id.upper()
        
        # Momentum analysis
        momentum_score = 0
        momentum_text = "STAGNANT"
        
        if abs(change_24h) > 10:
            momentum_score = 5
            momentum_text = "EXPLOSIVE VOLATILITY"
        elif abs(change_24h) > 5:
            momentum_score = 4
            momentum_text = "STRONG TREND"
        elif abs(change_24h) > 2:
            momentum_score = 3
            momentum_text = "MODERATE TREND"
        elif abs(change_24h) > 1:
            momentum_score = 2
            momentum_text = "SLOW TREND"
        elif abs(change_24h) > 0:
            momentum_score = 1
            momentum_text = "MINOR DRIFT"
        
        # Direction
        direction = "BULLISH" if change_24h > 0 else "BEARISH"
        
        trends[coin_name] = {
            'price': price,
            'change_24h': change_24h,
            'market_cap': market_cap,
            'volume': volume,
            'momentum_score': momentum_score,
            'momentum_text': momentum_text,
            'direction': direction,
            'actionable_signal': generate_signal(momentum_score, direction)
        }
    
    return trends

def generate_signal(momentum_score, direction):
    """Generate actionable trading signal"""
    if momentum_score >= 4:
        if direction == "BULLISH":
            return "🚨 STRONG BUY - High conviction bullish momentum"
        else:
            return "📉 STRONG SELL - Clear bearish pressure"
    elif momentum_score >= 3:
        if direction == "BULLISH":
            return "📈 MODERATE BUY - Good directional momentum"
        else:
            return "📉 MODERATE SELL - Bearish pressure building"
    elif momentum_score >= 2:
        if direction == "BULLISH":
            return "📊 MILD BUY - Slower bullish drift"
        else:
            return "📊 MILD SELL - Slower bearish drift"
    else:
        return "🔄 HOLD - Wait for clearer momentum"

def analyze_institutional_flows(trends):
    """Analyze institutional flows based on volume patterns"""
    flows = {}
    
    for coin, data in trends.items():
        volume = data['volume']
        market_cap = data['market_cap']
        
        # Simple volume/MC ratio analysis
        volume_ratio = (volume / market_cap) * 100 if market_cap > 0 else 0
        
        flow_intensity = "LOW"
        if volume_ratio > 5:
            flow_intensity = "VERY HIGH"
        elif volume_ratio > 3:
            flow_intensity = "HIGH"
        elif volume_ratio > 1:
            flow_intensity = "MODERATE"
        
        flows[coin] = {
            'volume_ratio': volume_ratio,
            'intensity': flow_intensity
        }
    
    return flows

def generate_polymarket_recommendations(trends, flows):
    """Generate polymarket betting recommendations"""
    recommendations = {}
    
    for coin, trend_data in trends.items():
        flow_data = flows[coin]
        
        momentum = trend_data['momentum_score']
        action = trend_data['actionable_signal']
        intensity = flow_data['intensity']
        
        # Risk assessment
        volatility_risk = "LOW"
        if trend_data['momentum_score'] >= 4:
            volatility_risk = "HIGH"
        elif trend_data['momentum_score'] >= 3:
            volatility_risk = "MEDIUM"
        
        # Betting recommendation
        bet_size = None
        if momentum >= 4:
            bet_size = "HIGH CONVICTION - Higher stakes"
        elif momentum >= 3:
            bet_size = "MODERATE CONVICTION - Medium stakes"
        elif momentum >= 2:
            bet_size = "LOW CONVICTION - Small positions"
        else:
            bet_size = "OBSERVE - No positions"
        
        recommendations[coin] = {
            'bet_recommendation': action,
            'bet_size': bet_size,
            'risk_level': volatility_risk,
            'confidence': f"{momentum}/5",
            'timeline': "15-min window" if momentum >= 4 else "30-min window" if momentum >= 3 else "1-hour+"
        }
    
    return recommendations

def main():
    """Main analysis function"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    
    print(f"🎯 POLYMARKET CRYPTO TRENDS ANALYSIS")
    print(f"Time: {timestamp}")
    print("=" * 70)
    
    # Fetch market data
    price_data = fetch_market_data()
    
    if not price_data:
        print("❌ Failed to fetch market data")
        return
    
    # Analyze trends
    trends = analyze_momentum_trends(price_data)
    flows = analyze_institutional_flows(trends)
    recommendations = generate_polymarket_recommendations(trends, flows)
    
    print("\n📊 LIVE MARKET DATA")
    print("-" * 40)
    
    for coin, data in trends.items():
        print(f"{coin}:")
        print(f"  Price: ${data['price']:,.2f}")
        print(f"  24h Change: {data['change_24h']:+.2f}% ({data['direction']})")
        print(f"  Momentum: {data['momentum_score']}/5 - {data['momentum_text']}")
        print(f"  Signal: {data['actionable_signal']}")
    
    print("\n🏛️ INSTITUTIONAL FLOWS")
    print("-" * 40)
    
    for coin, data in flows.items():
        print(f"{coin}:")
        print(f"  Volume/MC Ratio: {data['volume_ratio']:.2f}%")
        print(f"  Flow Intensity: {data['intensity']}")
    
    print("\n💸 POLYMARKET BETTING RECOMMENDATIONS")
    print("-" * 50)
    
    for coin, rec in recommendations.items():
        print(f"{coin} BETTING ADVICE:")
        print(f"  Recommendation: {rec['bet_recommendation']}")
        print(f"  Bet Size: {rec['bet_size']}")
        print(f"  Risk Level: {rec['risk_level']}")
        print(f"  Confidence: {rec['confidence']}")
        print(f"  Timeline: {rec['timeline']}")
        print()
    
    print("\n⚠️ DISCLAIMER: Not financial advice - for educational purposes only")
    print("Always DYOR and manage risk appropriately")

if __name__ == "__main__":
    main()