#!/usr/bin/env python3
import time
import requests
import json
from datetime import datetime, timedelta
import subprocess
import sys

# Telegram configuration
TELEGRAM_BOT_TOKEN = ""  # Will be set from environment
TELEGRAM_CHANNEL_ID = "-1002328055394"

# API endpoints
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"

# Track previous prices for movement detection
price_history = {
    'bitcoin': {'price': 0, 'timestamp': datetime.now()},
    'ethereum': {'price': 0, 'timestamp': datetime.now()},
    'solana': {'price': 0, 'timestamp': datetime.now()}
}

# Volume tracking
volume_tracking = {
    'BTCUSDT': {'volume': 0, 'avg_volume': None, 'spikes': []},
    'ETHUSDT': {'volume': 0, 'avg_volume': None, 'spikes': []},
    'SOLUSDT': {'volume': 0, 'avg_volume': None, 'spikes': []}
}

def send_telegram_message(message):
    """Send message to Telegram channel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Message sent to Telegram")
            return True
        else:
            print(f"❌ Failed to send message: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def get_binance_data(symbol):
    """Get data from Binance API"""
    try:
        response = requests.get(f"{BINANCE_API}?symbol={symbol}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"❌ Binance API error for {symbol}: {e}")
        return None

def get_coingecko_data():
    """Get data from CoinGecko API"""
    try:
        ids = "bitcoin,ethereum,solana"
        url = f"{COINGECKO_API}?ids={ids}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"❌ CoinGecko API error: {e}")
        return None

def detect_significant_movement(asset, current_price, previous_price):
    """Detect 3%+ price movements"""
    if previous_price <= 0:
        return False, 0
    
    percentage_change = ((current_price - previous_price) / previous_price) * 100
    return abs(percentage_change) >= 3, percentage_change

def analyze_volume_spike(symbol, current_volume):
    """Detect volume spikes (2x+ average)"""
    tracking = volume_tracking[symbol]
    
    # Calculate average volume (using last 10 readings)
    if tracking['avg_volume'] is None:
        tracking['volume'] = current_volume
        tracking['spikes'].append(current_volume)
        if len(tracking['spikes']) >= 5:
            tracking['avg_volume'] = sum(tracking['spikes']) / len(tracking['spikes'])
        return False, 0
    
    # Check for spike
    volume_spike = (current_volume / tracking['avg_volume']) if tracking['avg_volume'] > 0 else 0
    
    # Update average
    tracking['spikes'].append(current_volume)
    if len(tracking['spikes']) > 10:
        tracking['spikes'].pop(0)
    tracking['avg_volume'] = sum(tracking['spikes']) / len(tracking['spikes'])
    
    return volume_spike >= 2, volume_spike

def analyze_technical_patterns(data):
    """Simple technical pattern analysis"""
    patterns = []
    
    # Example patterns based on price action
    price_change = float(data.get('priceChangePercent', 0))
    
    if price_change > 5:
        patterns.append("Strong bullish momentum")
    elif price_change < -5:
        patterns.append("Strong bearish momentum")
    elif abs(price_change) < 1:
        patterns.append("Consolidation phase")
    
    return patterns

def scan_markets():
    """Perform market scan and send alerts"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    print(f"\n📊 MARKET SCAN - {timestamp}")
    print("=" * 50)
    
    # Get CoinGecko data for prices
    cg_data = get_coingecko_data()
    if not cg_data:
        print("❌ Failed to get CoinGecko data")
        return
    
    alerts = []
    
    # Analyze major cryptocurrencies
    assets = [
        ('bitcoin', 'BTC', 'BTCUSDT'),
        ('ethereum', 'ETH', 'ETHUSDT'),
        ('solana', 'SOL', 'SOLUSDT')
    ]
    
    for asset_id, symbol, binance_symbol in assets:
        if asset_id in cg_data:
            current_price = cg_data[asset_id]['usd']
            price_change = cg_data[asset_id]['usd_24h_change']
            
            # Get Binance volume data
            binance_data = get_binance_data(binance_symbol)
            
            # Check price movement
            previous_data = price_history[asset_id]
            has_movement, pct_change = detect_significant_movement(
                asset_id, current_price, previous_data['price']
            )
            
            # Check volume spike if Binance data available
            volume_spike_detected = False
            spike_ratio = 0
            
            if binance_data:
                current_volume = float(binance_data.get('volume', 0))
                volume_spike_detected, spike_ratio = analyze_volume_spike(
                    binance_symbol, current_volume
                )
            
            # Technical patterns
            patterns = analyze_technical_patterns(binance_data) if binance_data else []
            
            # Update price history
            price_history[asset_id] = {'price': current_price, 'timestamp': datetime.now()}
            
            # Generate alert if significant movement detected
            alert_parts = []
            
            if has_movement:
                trend = "📈 UP" if pct_change > 0 else "📉 DOWN"
                alert_parts.append(f"• **{symbol}**: {trend} {abs(pct_change):.1f}%")
            
            if volume_spike_detected:
                alert_parts.append(f"• **Volume**: {spike_ratio:.0f}x average")
            
            if patterns:
                alert_parts.append(f"• **Pattern**: {patterns[0]}")
            
            if len(alert_parts) >= 2:  # Only alert for significant signals
                alert_message = f"⚡ **CRYPTO MARKET MOVES** ⚡\n" + "\n".join(alert_parts)
                alerts.append(alert_message)
                
                print(f"✅ {symbol} - Movement detected")
                print(f"   Price: ${current_price:,.2f} ({price_change:+.1f}%)")
                print(f"   Alert: {alert_message}")
            
            print(f"📊 {symbol}: ${current_price:,.2f} ({price_change:+.2f}%)")
    
    # Send alerts
    for alert in alerts:
        if send_telegram_message(alert):
            print(f"📤 Alert sent: {alert[:50]}...")

def main():
    """Main monitoring loop"""
    print("🚀 CRYPTO MARKET MONITOR STARTED")
    print("📊 Monitoring BTC/ETH/SOL for:")
    print("   • 3%+ price movements")
    print("   • 2x+ volume spikes")
    print("   • Technical breakout patterns")
    print("📤 Broadcasting alerts to Telegram group: -1002328055394")
    print("⏰ Timezone: GMT+8 (Asia/Manila)")
    print("💡 Press Ctrl+C to stop")
    print("-" * 60)
    
    scan_count = 0
    
    while True:
        scan_count += 1
        print(f"\n🔄 Scan #{scan_count} starting...")
        
        scan_markets()
        
        print(f"✅ Scan #{scan_count} completed")
        print("⏳ Waiting 60 seconds for next scan...")
        
        # Wait 60 seconds before next scan
        time.sleep(60)

if __name__ == "__main__":
    # Check if Telegram token is available
    import os
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        print("Please set TELEGRAM_BOT_TOKEN to enable Telegram alerts")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Crypto market monitor stopped")
        print("Thanks for using the crypto oracle!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Restarting in 30 seconds...")
        time.sleep(30)
        main()