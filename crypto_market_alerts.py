#!/usr/bin/env python3
"""
CRYPTO MARKET ALERTS - Real-time BTC/ETH/SOL monitoring
Broadcasts 3%+ movements and volume spikes to Telegram
"""

import requests
import time
from datetime import datetime
import json

# Telegram channel ID
TELEGRAM_CHANNEL_ID = "-1002328055394"

# API endpoints
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"

# Price tracking
last_prices = {
    'BTC': 0,
    'ETH': 0,
    'SOL': 0
}

def get_crypto_data():
    """Get current crypto prices"""
    try:
        # CoinGecko for price and change
        cg_response = requests.get(
            f"{COINGECKO_API}?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true",
            timeout=10
        )
        
        if cg_response.status_code == 200:
            data = cg_response.json()
            
            # Binance for volume
            symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
            binance_data = {}
            
            for symbol in symbols:
                try:
                    bn_response = requests.get(f"{BINANCE_API}?symbol={symbol}", timeout=5)
                    if bn_response.status_code == 200:
                        binance_data[symbol[:-4]] = bn_response.json()
                except:
                    pass
            
            return data, binance_data
        else:
            return None, None
            
    except Exception as e:
        print(f"❌ API error: {e}")
        return None, None

def format_alert_message(asset, current_price, price_change, volume_data=None):
    """Format market movement alert"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    
    message = f"⚡ **CRYPTO MARKET MOVES** ⚡\n"
    message += f"• **{asset}**: trending {'up' if price_change > 0 else 'down'} {abs(price_change):.1f}%\n"
    message += f"• **Price**: ${current_price:,.2f}\n"
    
    # Add volume info if available
    if volume_data:
        volume = float(volume_data.get('volume', 0))
        quote_volume = float(volume_data.get('quoteVolume', 0))
        message += f"• **24h Volume**: ${quote_volume:,.0f}\n"
    
    # Technical signals
    if abs(price_change) > 10:
        message += "• **Pattern**: Extreme momentum\n"
    elif abs(price_change) > 5:
        message += "• **Pattern**: Strong breakout\n"
    else:
        message += "• **Signal**: Accumulation phase\n"
    
    message += f"\n_({timestamp})_"
    return message

def should_alert(asset, price_change):
    """Check if movement warrants alert"""
    return abs(price_change) >= 3

def broadcast_telegram_alert(message):
    """Send alert to Telegram channel"""
    print(f"📤 Broadcasting to Telegram: {message[:100]}...")
    
    # Using subprocess to leverage your existing Telegram setup
    # This assumes you have telegram-cli configured
    try:
        import subprocess
        # Format for telegram-cli
        cmd = f"telegram-cli -W -e 'msg -{TELEGRAM_CHANNEL_ID} \"{message}\"'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Alert sent successfully")
            return True
        else:
            print(f"❌ Telegram error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram broadcast error: {e}")
        return False

def market_scan():
    """Perform market scan and trigger alerts"""
    cg_data, binance_data = get_crypto_data()
    
    if not cg_data:
        print("❌ Failed to fetch market data")
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"\n📊 Market Scan - {timestamp}")
    
    alerts_sent = 0
    
    # Check each asset
    assets = [
        ('bitcoin', 'BTC'),
        ('ethereum', 'ETH'), 
        ('solana', 'SOL')
    ]
    
    for asset_id, symbol in assets:
        if asset_id in cg_data:
            price = cg_data[asset_id]['usd']
            price_change = cg_data[asset_id]['usd_24h_change']
            
            # Check if significant movement
            if should_alert(symbol, price_change):
                volume_data = binance_data.get(symbol) if binance_data else None
                alert_message = format_alert_message(symbol, price, price_change, volume_data)
                
                print(f"🚨 {symbol} ALERT: {price_change:+.1f}% movement")
                
                # Broadcast alert
                if broadcast_telegram_alert(alert_message):
                    alerts_sent += 1
            
            print(f"📈 {symbol}: ${price:,.2f} ({price_change:+.2f}%)")
    
    if alerts_sent > 0:
        print(f"✅ Sent {alerts_sent} alerts to Telegram")
    else:
        print("💤 No significant movements detected")

def main():
    """Main monitoring loop"""
    print("🚀 CRYPTO MARKET ALERT SYSTEM")
    print("📊 Monitoring BTC/ETH/SOL every 60 seconds")
    print("⚡ Alerting on 3%+ price movements")
    print("📤 Broadcasting to Telegram group: -1002328055394")
    print("⏰ Timezone: GMT+8")
    print("-" * 50)
    
    scan_count = 0
    
    while True:
        scan_count += 1
        print(f"\n🔄 Scan #{scan_count}")
        
        try:
            market_scan()
        except Exception as e:
            print(f"❌ Scan error: {e}")
        
        # Wait 60 seconds
        print("⏳ Waiting 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")