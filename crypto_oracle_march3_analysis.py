#!/usr/bin/env python3
import requests
from datetime import datetime
import json

def get_current_crypto_data():
    """Get real BTC, ETH, SOL prices with detailed technical analysis"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'btc_price': data['bitcoin']['usd'],
                'btc_change_24h': data['bitcoin']['usd_24h_change'],
                'btc_volume': data['bitcoin']['usd_24h_vol'],
                'btc_market_cap': data['bitcoin']['usd_market_cap'],
                'eth_price': data['ethereum']['usd'],
                'eth_change_24h': data['ethereum']['usd_24h_change'],
                'eth_volume': data['ethereum']['usd_24h_vol'],
                'eth_market_cap': data['ethereum']['usd_market_cap'],
                'sol_price': data['solana']['usd'],
                'sol_change_24h': data['solana']['usd_24h_change'],
                'sol_volume': data['solana']['usd_24h_vol'],
                'sol_market_cap': data['solana']['usd_market_cap'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M GMT+8')
            }
        else:
            return None
    except Exception as e:
        return None

def analyze_momentum_trends(price_data):
    """Analyze momentum and trend shifts"""
    if not price_data:
        return {"error": "No price data available"}
    
    analysis = {}
    
    # BTC Analysis
    btc_change = price_data['btc_change_24h']
    btc_vol = price_data['btc_volume']
    btc_mc = price_data['btc_market_cap']
    
    analysis['btc'] = {
        'momentum': 'strong_positive' if btc_change > 2.0 else 'positive' if btc_change > 0 else 'negative' if btc_change < -2.0 else 'neutral',
        'trend': 'uptrend' if btc_change > 0.5 else 'downtrend' if btc_change < -0.5 else 'consolidation',
        'volume_support': 'high' if btc_vol > 40000000000 else 'moderate' if btc_vol > 20000000000 else 'low',
        'dominance': btc_mc / 1000000000000  # Trillions
    }
    
    # ETH Analysis
    eth_change = price_data['eth_change_24h']
    eth_vol = price_data['eth_volume']
    eth_mc = price_data['eth_market_cap']
    
    analysis['eth'] = {
        'momentum': 'strong_positive' if eth_change > 2.0 else 'positive' if eth_change > 0 else 'negative' if eth_change < -2.0 else 'neutral',
        'trend': 'uptrend' if eth_change > 0.5 else 'downtrend' if eth_change < -0.5 else 'consolidation',
        'volume_support': 'high' if eth_vol > 15000000000 else 'moderate' if eth_vol > 8000000000 else 'low',
        'dominance': eth_mc / 1000000000000
    }
    
    # SOL Analysis
    sol_change = price_data['sol_change_24h']
    sol_vol = price_data['sol_volume']
    sol_mc = price_data['sol_market_cap']
    
    analysis['sol'] = {
        'momentum': 'strong_positive' if sol_change > 2.0 else 'positive' if sol_change > 0 else 'negative' if sol_change < -2.0 else 'neutral',
        'trend': 'uptrend' if sol_change > 0.5 else 'downtrend' if sol_change < -0.5 else 'consolidation',
        'volume_support': 'high' if sol_vol > 2000000000 else 'moderate' if sol_vol > 1000000000 else 'low',
        'dominance': sol_mc / 100000000000
    }
    
    # Overall trend analysis
    total_momentum = (btc_change + eth_change + sol_change) / 3
    analysis['overall'] = {
        'market_momentum': 'bullish' if total_momentum > 0.5 else 'bearish' if total_momentum < -0.5 else 'neutral',
        'total_volume': btc_vol + eth_vol + sol_vol,
        'market_health': 'strong' if total_momentum > 0 and analysis['btc']['volume_support'] == 'high' else 'moderate'
    }
    
    return analysis

print("🔮 CRYPTO ORACLE VALIDATION - POLYMARKET TRENDS")
print("="*70)
print("BTC/ETH/SOL Momentum & Trend Shift Analysis")
print("Tuesday, March 3rd, 2026 — 12:36 PM (Asia/Manila)")
print()

# Get current market data
price_data = get_current_crypto_data()

if price_data:
    print("📊 LIVE MARKET DATA")
    print("-"*40)
    print(f"Time: {price_data['timestamp']}")
    print()
    
    btc_symbol = "▲" if price_data['btc_change_24h'] > 0 else "▼"
    eth_symbol = "▲" if price_data['eth_change_24h'] > 0 else "▼"
    sol_symbol = "▲" if price_data['sol_change_24h'] > 0 else "▼"
    
    # Format volumes
    def format_volume(vol):
        if vol >= 1000000000:
            return f"${vol/1000000000:.2f}B"
        elif vol >= 1000000:
            return f"${vol/1000000:.2f}M"
        else:
            return f"${vol:,.0f}"
    
    btc_vol_str = format_volume(price_data['btc_volume'])
    eth_vol_str = format_volume(price_data['eth_volume'])
    sol_vol_str = format_volume(price_data['sol_volume'])
    
    print("💰 MARKET POSITION:")
    print(f"BTC: ${price_data['btc_price']:,.2f} {btc_symbol}{abs(price_data['btc_change_24h']):.2f}% (Vol: {btc_vol_str})")
    print(f"ETH: ${price_data['eth_price']:,.2f} {eth_symbol}{abs(price_data['eth_change_24h']):.2f}% (Vol: {eth_vol_str})")
    print(f"SOL: ${price_data['sol_price']:,.2f} {sol_symbol}{abs(price_data['sol_change_24h']):.2f}% (Vol: {sol_vol_str})")
    print()
    
    # Perform momentum analysis
    trend_analysis = analyze_momentum_trends(price_data)
    
    print("🎯 MOMENTUM & TREND ANALYSIS")
    print("-"*35)
    
    # BTC Analysis
    btc_analysis = trend_analysis['btc']
    print(f"BITCOIN (BTC):")
    print(f"  Momentum: {btc_analysis['momentum'].replace('_', ' ').title()}")
    print(f"  Trend: {btc_analysis['trend'].title()}")
    print(f"  Volume Support: {btc_analysis['volume_support'].title()}")
    print(f"  Market Cap: ${btc_analysis['dominance']:.2f}T")
    print()
    
    # ETH Analysis
    eth_analysis = trend_analysis['eth']
    print(f"ETHEREUM (ETH):")
    print(f"  Momentum: {eth_analysis['momentum'].replace('_', ' ').title()}")
    print(f"  Trend: {eth_analysis['trend'].title()}")
    print(f"  Volume Support: {eth_analysis['volume_support'].title()}")
    print(f"  Market Cap: ${eth_analysis['dominance']:.2f}T")
    print()
    
    # SOL Analysis
    sol_analysis = trend_analysis['sol']
    print(f"SOLANA (SOL):")
    print(f"  Momentum: {sol_analysis['momentum'].replace('_', ' ').title()}")
    print(f"  Trend: {sol_analysis['trend'].title()}")
    print(f"  Volume Support: {sol_analysis['volume_support'].title()}")
    print(f"  Market Cap: ${sol_analysis['dominance']:.2f}B")
    print()
    
    # Overall Analysis
    overall = trend_analysis['overall']
    total_vol_str = format_volume(overall['total_volume'])
    print(f"OVERALL MARKET:")
    print(f"  Momentum Bias: {overall['market_momentum'].title()}")
    print(f"  Total Volume: {total_vol_str}")
    print(f"  Market Health: {overall['market_health'].title()}")
    print()
    
    print("📈 TREND SHIFT POTENTIAL")
    print("-"*25)
    
    # Trend shift analysis
    shifts = []
    
    if abs(price_data['btc_change_24h']) > 1.5:
        shifts.append("BTC showing significant momentum shift")
    if abs(price_data['eth_change_24h']) > 1.5:
        shifts.append("ETH showing momentum acceleration")
    if abs(price_data['sol_change_24h']) > 3.0:
        shifts.append("SOL exhibiting volatile momentum")
    
    if shifts:
        for shift in shifts:
            print(f"• {shift}")
    else:
        print("• Markets in relatively stable trending patterns")
    
    print()
    print("🔍 POLYMARKET TRENDS IMPLICATION")
    print("-"*30)
    overall_trend = trend_analysis['overall']['market_momentum']
    if overall_trend == 'bullish':
        print("• Bias favors bullish market predictions")
        print("• Institutional volume supports upward momentum")
    elif overall_trend == 'bearish':
        print("• Bearish sentiment dominates market")
        print("• Caution advised for bullish predictions")
    else:
        print("• Neutral/consolidating market conditions")
        print("• Market direction unclear - wait for catalyst")
    
else:
    print("❌ Could not fetch current market data")
    print("💰 Using placeholder analysis based on market trends")
    print()
    print("⚠️ MARKET ANALYSIS UNAVAILABLE")
    print("• Data source temporarily inaccessible")
    print("• Retry suggested for accurate trend assessment")

print()
print("⚠️ DISCLAIMER: Crypto Oracle Validation using CoinGecko API")
print("Analysis provided for informational purposes only")