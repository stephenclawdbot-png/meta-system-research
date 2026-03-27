#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime

print("💰 REAL POLYMARKET BETTING FEED - LIVE DATA")
print("="*60)
print("Wednesday, February 18, 2026 — 17:50 PM GMT+8")
print("ACTUAL LIVE MARKET DATA FOR BETTING")
print()

try:
    # CoinGecko API endpoint for BTC, ETH, SOL
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']
        
        sol_price = data['solana']['usd']
        sol_change = data['solana']['usd_24h_change']
        
        print("📊 LIVE PRICE DATA FROM COINGECKO API")
        print("-"*40)
        
        print(f"BTC: ${btc_price:,.2f} {'▲+' if btc_change > 0 else '▼'}{btc_change:.2f}%")
        print(f"   📈 {datetime.now().strftime('%H:%M GMT+8')}")
        print(f"   💹 24h Change: {btc_change:.2f}%")
        print()
        
        print(f"ETH: ${eth_price:,.2f} {'▲+' if eth_change > 0 else '▼'}{eth_change:.2f}%")
        print(f"   📈 {datetime.now().strftime('%H:%M GMT+8')}")
        print(f"   💹 24h Change: {eth_change:.2f}%")
        print()
        
        print(f"SOL: ${sol_price:,.2f} {'▲+' if sol_change > 0 else '▼'}{sol_change:.2f}%")
        print(f"   📈 {datetime.now().strftime('%H:%M GMT+8')}")
        print(f"   💹 24h Change: {sol_change:.2f}%")
        
    else:
        print("❌ API Error: Could not fetch real prices")
        print(f"   Status Code: {response.status_code}")
        print("   Using fallback: Check CoinGecko manually")
        
except Exception as e:
    print("⚠️ CONNECTION ERROR: Cannot fetch live data")
    print(f"   Error: {e}")
    print("   Setup CoinGecko API key for live feeds")

print()
print("🎯 POLYMARKET BETTING GUIDE")
print("-"*25)
print("• Use actual price movements for betting")
print("• Monitor 15-min intervals")
print("• Check directions (▲/▼) for UP/DOWN bets")
print("• Real data = real betting decisions")
print()

print("🔧 TECHNICAL STATUS:")
print("-"*20)
print("• API Integration: REQUIRES SETUP")
print("• Real-time data: Available via CoinGecko")
print("• Current feed: Manual API calls needed")
print()

print("⚠️ CRITICAL: Do not bet without real data")
print("Setup proper API integration first")