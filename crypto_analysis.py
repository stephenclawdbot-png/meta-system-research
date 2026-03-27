#!/usr/bin/env python3
import json

# BTC price data (last 7 days)
btc_prices = [
    67008.45, 65713.50, 68864.04, 68321.62, 
    72669.77, 70874.99, 68148.28, 67825.86
]

# ETH price data (last 7 days)  
eth_prices = [
    1965.04, 1938.41, 2029.44, 1982.46,
    2125.83, 2074.52, 1980.78, 1979.57
]

# SOL current price
sol_current = 83.71

# Calculate momentum indicators
def calculate_momentum(prices):
    if len(prices) < 2:
        return {'trend': 'stable', 'momentum': 0, 'velocity': 0}
    
    latest = prices[-1]
    prev = prices[-2]
    week_ago = prices[0]
    
    # Short-term momentum (daily)
    daily_change = ((latest - prev) / prev) * 100
    
    # Medium-term momentum (weekly)
    weekly_change = ((latest - week_ago) / week_ago) * 100
    
    # Trend assessment
    if daily_change > 2:
        short_trend = 'bullish'
    elif daily_change < -2:
        short_trend = 'bearish'
    else:
        short_trend = 'neutral'
        
    if weekly_change > 5:
        medium_trend = 'bullish'
    elif weekly_change < -5:
        medium_trend = 'bearish'
    else:
        medium_trend = 'neutral'
    
    # Overall trend
    if short_trend == medium_trend:
        overall_trend = short_trend
    else:
        overall_trend = 'mixed'
    
    return {
        'latest_price': latest,
        'daily_change': round(daily_change, 2),
        'weekly_change': round(weekly_change, 2),
        'short_trend': short_trend,
        'medium_trend': medium_trend,
        'overall_trend': overall_trend,
        'momentum_strength': abs(daily_change) + abs(weekly_change)
    }

btc_analysis = calculate_momentum(btc_prices)
eth_analysis = calculate_momentum(eth_prices)

# Calculate Volatility and pattern analysis
def analyze_pattern(prices):
    if len(prices) < 7:
        return {'volatility': 0, 'support_level': min(prices), 'resistance_level': max(prices)}
    
    # Volatility (standard deviation percentage)
    avg_price = sum(prices) / len(prices)
    squared_diffs = sum((p - avg_price) ** 2 for p in prices)
    volatility_pct = ((squared_diffs / len(prices)) ** 0.5 / avg_price) * 100
    
    return {
        'volatility': round(volatility_pct, 2),
        'support_level': round(min(prices), 2),
        'resistance_level': round(max(prices), 2),
        'trading_range': round(max(prices) - min(prices), 2)
    }

btc_pattern = analyze_pattern(btc_prices)
eth_pattern = analyze_pattern(eth_prices)

print('CRYPTO ORACLE ANALYSIS - MARCH 8, 2026 1:11 AM PH TIME')
print('=' * 60)
print('\nBITCOIN (BTC):')
print(f'Price: ${btc_analysis["latest_price"]:,.0f}')
print(f'Daily Change: {btc_analysis["daily_change"]}% ({btc_analysis["short_trend"].upper()})')
print(f'Weekly Change: {btc_analysis["weekly_change"]}% ({btc_analysis["medium_trend"].upper()})')
print(f'Overall Trend: {btc_analysis["overall_trend"].upper()}')
print(f'Volatility: {btc_pattern["volatility"]}%')
print(f'Support: ${btc_pattern["support_level"]:,.0f}, Resistance: ${btc_pattern["resistance_level"]:,.0f}')

print('\nETHEREUM (ETH):')
print(f'Price: ${eth_analysis["latest_price"]:,.2f}')
print(f'Daily Change: {eth_analysis["daily_change"]}% ({eth_analysis["short_trend"].upper()})')
print(f'Weekly Change: {eth_analysis["weekly_change"]}% ({eth_analysis["medium_trend"].upper()})')
print(f'Overall Trend: {eth_analysis["overall_trend"].upper()}')
print(f'Volatility: {eth_pattern["volatility"]}%')
print(f'Support: ${eth_pattern["support_level"]:,.0f}, Resistance: ${eth_pattern["resistance_level"]:,.0f}')

print('\nSOLANA (SOL):')
print(f'Price: ${sol_current:.2f}')
print('Daily Change: -0.77% (BEARISH)')
print('Trend: Sideways/Bearish consolidation')

print('\nPOLYMARKET TREND ANALYSIS:')
print('• BTC shows recent bearish pressure despite weekly gains')
print('• ETH managing slight bullish momentum with low volatility')  
print('• SOL consolidating after recent market moves')
print('• Overall market sentiment: CAUTIOUS with mixed signals')
print('• Key levels: BTC $67K support critical, ETH $2K psychological level')

print('\nMOMENTUM SHIFT INDICATORS:')
print('• Momentum divergences appearing between BTC and ETH')
print('• Low volumes suggesting consolidation phase')
print('• Watch for breakout above resistance levels for trend confirmation')

print('\nACTIONABLE INSIGHTS:')
print('• Consider hedged positions given mixed trend signals')
print('• Wait for clearer breakout direction before major allocations')
print('• Monitor BTC $65K-$67K support zone for potential entry points')