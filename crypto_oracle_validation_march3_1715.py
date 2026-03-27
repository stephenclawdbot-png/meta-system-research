#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def get_crypto_data():
    """Fetch current crypto data from CoinGecko API"""
    try:
        # Get price data
        price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        price_response = requests.get(price_url)
        price_data = price_response.json()
        
        # Get market data with volume
        market_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana&order=market_cap_desc&per_page=3&page=1&sparkline=false"
        market_response = requests.get(market_url)
        market_data = market_response.json()
        
        return price_data, market_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

def analyze_momentum(price_change):
    """Analyze momentum based on 24h price change"""
    if price_change > 5:
        return "VERY BULLISH (HIGH MOMENTUM)", 5
    elif price_change > 2:
        return "BULLISH (UPTREND CONFIRMED)", 4
    elif price_change > 0:
        return "MODERATE BULLISH", 3
    elif price_change > -2:
        return "NEUTRAL", 2
    else:
        return "BEARISH", 1

def analyze_volume_intensity(volume_mc_ratio):
    """Analyze institutional flow intensity"""
    if volume_mc_ratio > 10:
        return "VERY HIGH", "HIGH"
    elif volume_mc_ratio > 5:
        return "HIGH", "MEDIUM-HIGH"
    elif volume_mc_ratio > 2:
        return "MODERATE", "MEDIUM"
    else:
        return "LOW", "LOW"

def assess_polymarket_strategy(momentum_score, volume_intensity):
    """Assess Polymarket betting recommendations"""
    if momentum_score >= 4 and volume_intensity == "HIGH":
        return "HIGH CONVICTION BUY", "LOW"
    elif momentum_score >= 3:
        return "MODERATE CONVICTION BUY", "MEDIUM"
    else:
        return "NEUTRAL", "MEDIUM-HIGH"

def main():
    print("🦞 CRYPTO ORACLE VALIDATION CALL")
    print("=" * 60)
    print("POLYMARKET TREND ANALYSIS - BTC/ETH/SOL MOMENTUM")
    print(f"TIMESTAMP: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (%Z)')}")
    print()
    
    price_data, market_data = get_crypto_data()
    
    if not price_data or not market_data:
        print("❌ Failed to fetch market data")
        return
    
    print("📊 MARKET DATA ANALYSIS")
    print("-" * 30)
    
    assets = []
    
    for asset_data in market_data:
        symbol = asset_data["symbol"].upper()
        price = asset_data["current_price"]
        market_cap = asset_data["market_cap"]
        volume = asset_data["total_volume"]
        volume_mc_ratio = (volume / market_cap) * 100 if market_cap > 0 else 0
        
        # Get price change from price_data
        coin_key = asset_data["id"]
        price_change = price_data[coin_key]["usd_24h_change"]
        
        momentum_text, momentum_score = analyze_momentum(price_change)
        volume_intensity, flow_intensity = analyze_volume_intensity(volume_mc_ratio)
        
        assets.append({
            "symbol": symbol,
            "price": price,
            "change": price_change,
            "market_cap": market_cap,
            "volume": volume,
            "volume_mc_ratio": volume_mc_ratio,
            "momentum_text": momentum_text,
            "momentum_score": momentum_score,
            "volume_intensity": volume_intensity,
            "flow_intensity": flow_intensity
        })
        
        print(f"{symbol}:")
        print(f"  Price: ${price:,.2f} ({price_change:+.2f}%)")
        print(f"  Market Cap: ${market_cap / 1e9:.1f}B")
        print(f"  24h Volume: ${volume / 1e6:.1f}M")
        print(f"  Volume/MC Ratio: {volume_mc_ratio:.2f}% ({volume_intensity})")
        print(f"  Momentum: {momentum_text}")
        print()
    
    print("📈 MOMENTUM ASSESSMENT")
    print("-" * 25)
    
    for asset in assets:
        polymarket_action, risk_level = assess_polymarket_strategy(
            asset["momentum_score"], asset["volume_intensity"]
        )
        asset["polymarket_action"] = polymarket_action
        asset["risk_level"] = risk_level
        
        print(f"{asset['symbol']}:")
        print(f"  Momentum Score: {asset['momentum_score']}/5")
        print(f"  Institutional Flow: {asset['flow_intensity']}")
        print(f"  Polymarket Position: {polymarket_action}")
        print(f"  Risk Level: {risk_level}")
        print()
    
    print("🎯 POLYMARKET BETTING RECOMMENDATIONS")
    print("-" * 40)
    
    for asset in assets:
        print(f"{asset['symbol']}: {asset['polymarket_action']}")
        print(f"  • Confidence: {'High' if asset['momentum_score'] >= 4 else 'Moderate'}")
        print(f"  • Risk Level: {asset['risk_level']}")
        print(f"  • Action Window: 30 minutes")
        print()
    
    print("⚡ TREND SHIFT ANALYSIS")
    print("-" * 25)
    
    # Check for trend shifts
    positive_momentum_count = sum(1 for asset in assets if asset["change"] > 0)
    strong_momentum_count = sum(1 for asset in assets if asset["change"] > 2)
    
    if positive_momentum_count == 3:
        print("✅ MARKET-WIDE BULLISH BIAS CONFIRMED")
        print("   All three assets showing positive momentum")
    elif strong_momentum_count >= 2:
        print("✅ STRONG BULLISH MOMENTUM DETECTED")
        print("   Majority of assets showing strong momentum")
    else:
        print("⚠️  MIXED MARKET SIGNALS")
        print("   Divergence in asset momentum detected")
    
    print()
    print("📅 NEXT VALIDATION: 17:30 GMT+8")
    print()
    print("⚠️ DISCLAIMER: NFA - Market analysis only. Maximum risk management required.")
    print()
    print("Oracle Framework Operational - Polymarket Trend Validation Complete")

if __name__ == "__main__":
    main()