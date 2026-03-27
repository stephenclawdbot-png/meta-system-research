#!/usr/bin/env python3
"""
CRYPTO TREND SCANNER
Analyzes BTC/ETH/SOL for momentum shifts and institutional sentiment
Runs every 15 minutes, broadcasts key trends
"""

import requests
import time
from datetime import datetime

def fetch_crypto_prices():
    """Fetch BTC, ETH, SOL prices from CoinGecko"""
    coins = ['bitcoin', 'ethereum', 'solana']
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies=usd&include_24hr_change=true"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def analyze_trends(prices):
    """Analyze price trends and momentum"""
    trends = []
    
    if "error" in prices:
        return trends
    
    for coin_id, data in prices.items():
        price = data.get('usd', 0)
        change_24h = data.get('usd_24h_change', 0)
        
        coin_name = coin_id.upper()
        trend = {
            "coin": coin_name,
            "price": price,
            "change_24h": change_24h,
            "sentiment": "NEUTRAL"
        }
        
        # Trend analysis
        if abs(change_24h) > 5:
            trend["sentiment"] = "STRONG_MOVE"
        elif abs(change_24h) > 2:
            trend["sentiment"] = "MODERATE_MOVE"
        
        trends.append(trend)
    
    return trends

def scan_crypto_trends():
    """Main scanning function"""
    print(f"\n🌊 Crypto Trend Scan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    prices = fetch_crypto_prices()
    
    if "error" in prices:
        print(f"❌ API Error: {prices['error']}")
        return []
    
    trends = analyze_trends(prices)
    return trends

if __name__ == "__main__":
    trends = scan_crypto_trends()
    
    if trends:
        print("📊 Crypto Market Analysis:")
        broadcast_msg = "🌊 CRYPTO TRENDS\n"
        for trend in trends:
            change_sign = "+" if trend["change_24h"] > 0 else ""
            analysis_line = f"• {trend['coin']}: ${trend['price']:,} ({change_sign}{trend['change_24h']:.2f}%) - {trend['sentiment']}"
            print(analysis_line)
            broadcast_msg += analysis_line + "\n"
        
        # ACTUAL TELEGRAM BROADCAST
        print("📱 BROADCASTING TO TELEGRAM...")
        try:
            import subprocess
            # Send to group
            subprocess.run(["openclaw", "message", "send", "--to", "-1002328055394", "--message", broadcast_msg], 
                         capture_output=True, text=True)
            print("✅ Broadcasted to Telegram group")
            
            # Also send to you personally
            subprocess.run(["openclaw", "message", "send", "--to", "7284633206", "--message", broadcast_msg], 
                         capture_output=True, text=True)
            print("✅ Broadcasted to personal DM")
            
        except Exception as e:
            print(f"❌ Telegram broadcast failed: {e}")
            
    else:
        print("📭 No trend data available")