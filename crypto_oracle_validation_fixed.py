#!/usr/bin/env python3
"""
Crypto Oracle Validation Call for Polymarket Trends
Analyzes BTC/ETH/SOL momentum and trend shifts
"""

import requests
import json
from datetime import datetime

def get_crypto_data():
    """Get current crypto prices and market data"""
    try:
        # CoinGecko API for comprehensive crypto data
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def analyze_momentum(data):
    """Analyze momentum signals for BTC, ETH, SOL"""
    momentum_analysis = {}
    
    if data:
        for coin_id, coin_data in data.items():
            symbol = coin_id.upper()
            price = coin_data.get('usd', 0)
            change_24h = coin_data.get('usd_24h_change', 0)
            market_cap = coin_data.get('usd_market_cap', 0)
            volume = coin_data.get('usd_24h_vol', 0)
            
            # Momentum classification
            if change_24h > 5:
                momentum = "STRONG_BULLISH"
            elif change_24h > 2:
                momentum = "BULLISH"
            elif change_24h > -2:
                momentum = "SIDEWAYS"
            elif change_24h > -5:
                momentum = "BEARISH"
            else:
                momentum = "STRONG_BEARISH"
            
            momentum_analysis[symbol] = {
                'price': price,
                'change_24h': change_24h,
                'momentum': momentum,
                'market_cap': market_cap,
                'volume': volume
            }
    
    return momentum_analysis

def analyze_trend_shifts(analysis):
    """Look for trend shift signals"""
    trend_shifts = []
    
    for symbol, data in analysis.items():
        change = data['change_24h']
        momentum = data['momentum']
        
        # Trend shift candidates
        if abs(change) >= 3:  # 3%+ movement
            direction = "UP" if change > 0 else "DOWN"
            signal_strength = "STRONG" if abs(change) >= 5 else "MODERATE"
            
            trend_shifts.append({
                'symbol': symbol,
                'direction': direction,
                'change_percent': change,
                'signal_strength': signal_strength,
                'momentum': momentum
            })
    
    return trend_shifts

def format_summary(analysis, trend_shifts):
    """Format the validation summary"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    summary = f"⚡ CRYPTO ORACLE VALIDATION CALL ⚡\n\n📊 MARKET OVERVIEW - {timestamp}\n\n"
    
    # Current prices and momentum
    for symbol, data in analysis.items():
        summary += f"💰 **{symbol}**: ${data['price']:,.2f} ({data['change_24h']:+.2f}%)\n"
        summary += f"   📈 Momentum: {data['momentum']}\n"
        summary += f"   💰 Market Cap: ${data['market_cap']/1e9:,.1f}B\n"
        summary += f"   🔄 24h Volume: ${data['volume']/1e6:,.1f}M\n\n"
    
    # Trend shifts
    if trend_shifts:
        summary += "🔄 TREND SHIFT SIGNALS 🔄\n\n"
        for shift in trend_shifts:
            summary += f"🏃 **{shift['symbol']}** trending {shift['direction']} {abs(shift['change_percent']):.1f}%\n"
            summary += f"   Signal Strength: {shift['signal_strength']}\n"
            summary += f"   Momentum Category: {shift['momentum']}\n\n"
    else:
        summary += "📊 Markets are relatively stable - no major trend shifts detected\n\n"
    
    # Polymarket correlation analysis
    summary += "🎯 POLYMARKET CORRELATIONS\n"
    summary += "• BTC dominance drives broader crypto sentiment\n"
    summary += "• ETH momentum often precedes altcoin rotations\n"
    summary += "• SOL volatility creates prediction market opportunities\n\n"
    
    summary += f"_Crypto Oracle validated at {timestamp}_"
    
    return summary

def main():
    """Main validation function"""
    print("🔮 CRYPTO ORACLE VALIDATION STARTING...")
    
    # Get current market data
    data = get_crypto_data()
    
    if not data:
        print("❌ Failed to fetch crypto market data")
        return "Error: Unable to fetch market data. Check API connectivity."
    
    # Analyze momentum
    momentum_analysis = analyze_momentum(data)
    
    # Identify trend shifts
    trend_shifts = analyze_trend_shifts(momentum_analysis)
    
    # Generate summary
    summary = format_summary(momentum_analysis, trend_shifts)
    
    print("✅ Crypto Oracle validation complete")
    return summary

if __name__ == "__main__":
    result = main()
    print("\n" + result)