#!/usr/bin/env python3
"""One-time crypto market scan"""

import requests
from datetime import datetime

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

def scan():
    response = requests.get(
        COINGECKO_API + "?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    )
    
    if response.status_code == 200:
        data = response.json()
        print("⚡ CRYPTO MARKET SCAN")
        print("="*50)
        print("Asset      | Price        | 24h Change")
        print("-"*50)
        
        for coin in ['bitcoin', 'ethereum', 'solana']:
            if coin in data:
                price = data[coin]['usd']
                change = data[coin]['usd_24h_change']
                print(f"{coin.upper():10} | ${price:,.2f} | {change:+.2f}%")
        
        print("-"*50)
        return data
    else:
        print("❌ API error")
        return None

def check_alerts(data):
    if not data:
        return
    
    alerts = []
    for coin in ['bitcoin', 'ethereum', 'solana']:
        if coin in data:
            change = data[coin]['usd_24h_change']
            if abs(change) >= 3:
                alerts.append(f"• {coin.upper()}: {change:+.1f}% movement")
    
    if alerts:
        print("\n🚨 ALERT - SIGNIFICANT MOVEMENTS:")
        for alert in alerts:
            print(alert)
    else:
        print("\n✅ No significant movements detected")

if __name__ == "__main__":
    data = scan()
    check_alerts(data)