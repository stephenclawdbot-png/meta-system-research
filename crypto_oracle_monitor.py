#!/usr/bin/env python3
"""
CRYPTO ORACLE MONITOR - Real-time BTC/ETH/SOL Market Alerts
Broadcasts 3%+ movements to Telegram group -1002328055394
Uses existing Telegram configuration
"""

import requests
import time
from datetime import datetime
import sys
import os

# Import Telegram configuration from your existing setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from telegram_config import send_telegram_message
    TELEGRAM_ENABLED = True
except:
    TELEGRAM_ENABLED = False

# API endpoints
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"

# Telegram channel ID (your group)
TELEGRAM_CHANNEL_ID = "-1002328055394"

# Price tracking for movement detection
last_prices = {
    'BTC': 0,
    'ETH': 0,
    'SOL': 0
}

def get_current_prices():
    """Get current crypto prices with 24h changes"""
    try:
        response = requests.get(
            COINGECKO_API + "?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"❌ API error: {e}")
        return None

def format_crypto_alert(asset, price, change_pct, is_volume_spike=False, volume_multiplier=1):
    """Format alert message according to your preferred format"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    
    # Main alert format
    message = f"⚡ **CRYPTO MARKET MOVES** ⚡\n"
    message += f"• **{asset}**: trending {'up' if change_pct > 0 else 'down'} {abs(change_pct):.1f}%\n"
    message += f"• **Price**: ${price:,.2f}\n"
    
    # Add volume spike info if applicable
    if is_volume_spike:
        message += f"• **Volume**: up {volume_multiplier:.0f}x average\n"
    
    # Technical signals based on movement size
    if abs(change_pct) >= 10:
        message += "• **Pattern**: Extreme momentum breakout\n"
    elif abs(change_pct) >= 5:
        message += "• **Pattern**: Strong breakout\n"
    else:
        message += "• **Signal**: Accumulation phase\n"
    
    message += f"\n_Real-time actionable info ({timestamp})_"
    return message

def scan_markets():
    """Scan crypto markets and send alerts"""
    data = get_current_prices()
    
    if not data:
        print("❌ Failed to fetch market data")
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n📊 Crypto Scan - {timestamp}")
    
    alerts_sent = 0
    
    # Check each cryptocurrency
    assets = [
        ('bitcoin', 'BTC'),
        ('ethereum', 'ETH'),
        ('solana', 'SOL')
    ]
    
    for asset_id, symbol in assets:
        if asset_id in data:
            current_price = data[asset_id]['usd']
            price_change = data[asset_id]['usd_24h_change']
            
            # Check for significant movement (3% threshold)
            is_significant = abs(price_change) >= 3
            
            # Update last price and check movement
            if last_prices[symbol] > 0:
                movement = ((current_price - last_prices[symbol]) / last_prices[symbol]) * 100
            else:
                movement = price_change
            
            # Send alert for significant movement
            if is_significant:
                alert_message = format_crypto_alert(symbol, current_price, price_change)
                
                print(f"🚨 {symbol} ALERT: {price_change:+.1f}% movement")
                
                # Send via Telegram
                if TELEGRAM_ENABLED:
                    if send_telegram_message(alert_message):
                        alerts_sent += 1
                        print(f"✅ Alert sent for {symbol}")
                else:
                    # Fallback: print alert locally
                    print(f"⚠️ TELEGRAM NOT CONFIGURED - Alert: {alert_message}")
            
            # Update price history
            last_prices[symbol] = current_price
            
            print(f"📊 {symbol}: ${current_price:,.2f} ({price_change:+.2f}%)")
    
    return alerts_sent

def main():
    """Main monitoring loop"""
    print("🚀 CRYPTO ORACLE MONITOR ACTIVATED")
    print("📊 Monitoring BTC/ETH/SOL every 60 seconds")
    print("⚡ Alerting on 3%+ price movements")
    print(f"📤 Broadcasting to Telegram: {TELEGRAM_CHANNEL_ID}")
    print("⏰ Timezone: GMT+8")
    
    if not TELEGRAM_ENABLED:
        print("⚠️ TELEGRAM_NOT_CONFIGURED - Alerts will be logged locally")
        print("   To enable Telegram alerts, configure telegram_config.py")
    
    print("-" * 60)
    
    scan_count = 0
    total_alerts = 0
    
    try:
        while True:
            scan_count += 1
            print(f"\n🔄 Scan #{scan_count}")
            
            alerts = scan_markets()
            total_alerts += alerts
            
            print(f"📈 Total alerts sent: {total_alerts}")
            print("⏳ Waiting 60 seconds...")
            
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped")
        print(f"📊 Final stats: {scan_count} scans, {total_alerts} alerts")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        print("Restarting in 30 seconds...")
        time.sleep(30)
        main()

if __name__ == "__main__":
    main()