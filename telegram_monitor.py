#!/usr/bin/env python3
"""
BTC/ETH/SOL Polymarket Trend Analysis Monitor with Telegram Broadcasting
"""

import time
import subprocess
import os
import json
from datetime import datetime
import requests
import signal
import sys

class TelegramCryptoMonitor:
    def __init__(self):
        self.scanner_process = None
        self.last_alert_time = datetime.now()
        self.alert_cooldown = 300  # 5 minutes between alerts
        self.telegram_group_id = "-1002328055394"
        self.significant_threshold = 3.0  # 3% price change threshold
        
    def start_scanner(self):
        """Start the crypto scanner as a background process"""
        try:
            # Make the script executable
            os.chmod('crypto_scanner.py', 0o755)
            
            # Start the scanner
            self.scanner_process = subprocess.Popen(
                ['python3', 'crypto_scanner.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"🚀 Crypto scanner started with PID: {self.scanner_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Failed to start scanner: {e}")
            return False
    
    def check_alerts(self):
        """Check if alerts have been generated and need to be sent"""
        try:
            # Check if alert flag exists
            if os.path.exists('ALERT_FLAG'):
                # Read the alert flag timestamp
                with open('ALERT_FLAG', 'r') as f:
                    flag_time = datetime.fromisoformat(f.read().strip())
                
                # Check if we should send alert (cooldown respected)
                if (datetime.now() - flag_time).total_seconds() >= self.alert_cooldown:
                    # Read the actual alert data
                    if os.path.exists('crypto_alerts.json'):
                        with open('crypto_alerts.json', 'r') as f:
                            alert_data = json.load(f)
                        
                        # Check if alerts are significant enough
                        if self.is_significant_alert(alert_data):
                            # Format alert message
                            message = self.format_telegram_message(alert_data)
                            
                            # Remove the flag to prevent duplicate alerts
                            os.remove('ALERT_FLAG')
                            
                            return message
            
        except Exception as e:
            print(f"Error checking alerts: {e}")
        
        return None
    
    def is_significant_alert(self, alert_data):
        """Determine if alert is significant enough to send"""
        alerts = alert_data.get('alerts', [])
        
        for alert in alerts:
            # Check price change magnitude
            if alert.get('type') == 'momentum_trend':
                if abs(alert.get('strength', 0)) >= self.significant_threshold:
                    return True
            
            # Volume spikes
            elif alert.get('type') == 'volume_spike':
                if alert.get('factor', 0) >= 2.0:  # 2x volume spike
                    return True
            
            # RSI extremes
            elif alert.get('type') in ['rsi_overbought', 'rsi_oversold']:
                return True
        
        return False
    
    def format_telegram_message(self, alert_data):
        """Format the alert message for Telegram"""
        timestamp = datetime.fromisoformat(alert_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S GMT+8')
        
        message = "⚡ **CRYPTO MARKETS ALERT** ⚡\n"
        message += f"*Time:* {timestamp}\n\n"
        
        # Current prices sentiment
        sentiment = alert_data.get('sentiment', {})
        message += "*MARKET STATUS:*\n"
        
        for symbol in ['BTC', 'ETH', 'SOL']:
            if sentiment.get(symbol):
                sym_sentiment = sentiment[symbol]
                price_data = None
                
                # Find the latest price data for this symbol
                alerts = alert_data.get('alerts', [])
                for alert in alerts:
                    if alert.get('symbol') == symbol:
                        price_data = alert
                        break
                
                if price_data:
                    price = price_data.get('current_price', 'N/A')
                    if isinstance(price, float):
                        price = f"${price:,.2f}"
                    
                    change_pct = ""
                    if price_data.get('type') == 'momentum_trend':
                        strength = price_data.get('strength', 0)
                        direction = price_data.get('direction', '')
                        change_pct = f" ({direction} {abs(strength):.1f}%)"
                    
                    message += f"• {symbol}: {price}{change_pct} - {sym_sentiment.upper()}\n"
        
        message += "\n"
        
        # Key patterns detected
        message += "*KEY PATTERNS:*\n"
        alerts = alert_data.get('alerts', [])
        
        if alerts:
            for alert in alerts[:3]:  # Show top 3 alerts
                symbol = alert.get('symbol', 'UNKNOWN')
                alert_type = alert.get('type', '')
                
                if alert_type == 'momentum_trend':
                    direction = alert.get('direction', '').upper()
                    strength = alert.get('strength', 0)
                    message += f"• {symbol} {direction} momentum ({strength:.1f}%)\n"
                
                elif alert_type == 'volume_spike':
                    factor = alert.get('factor', 0)
                    message += f"• {symbol} volume spike ({factor:.1f}x avg)\n"
                
                elif alert_type == 'rsi_overbought':
                    rsi = alert.get('rsi_value', 0)
                    message += f"• {symbol} RSI overbought ({rsi:.1f})\n"
                
                elif alert_type == 'rsi_oversold':
                    rsi = alert.get('rsi_value', 0)
                    message += f"• {symbol} RSI oversold ({rsi:.1f})\n"
        else:
            message += "• No significant patterns detected\n"
        
        message += "\n"
        
        # Actionable signals
        message += "*ACTIONABLE SIGNALS:*\n"
        if any('bullish' in str(sentiment.get(sym, '')).lower() for sym in ['BTC', 'ETH', 'SOL']):
            message += "• Watch for continuation patterns\n"
        if any('bearish' in str(sentiment.get(sym, '')).lower() for sym in ['BTC', 'ETH', 'SOL']):
            message += "• Monitor for potential reversals\n"
        if any(alert.get('type') == 'volume_spike' for alert in alerts):
            message += "• Volume confirming price action\n"
        
        # General recommendation
        bullish_count = sum(1 for sym in ['BTC', 'ETH', 'SOL'] if sentiment.get(sym) == 'bullish')
        bearish_count = sum(1 for sym in ['BTC', 'ETH', 'SOL'] if sentiment.get(sym) == 'bearish')
        
        if bullish_count >= 2:
            message += "• Trend bias: BULLISH\n"
        elif bearish_count >= 2:
            message += "• Trend bias: BEARISH\n"
        else:
            message += "• Market: MIXED/UNCLEAR\n"
        
        return message
    
    def send_telegram_alert(self, message):
        """Send alert to Telegram group"""
        print("\n" + "="*60)
        print("📢 READY TO BROADCAST TO TELEGRAM GROUP:")
        print("="*60)
        print(message)
        print("="*60)
        print(f"Group ID: {self.telegram_group_id}")
        print("="*60 + "\n")
        
        # Save the message for potential manual sending or integration
        alert_file = f"telegram_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(alert_file, 'w') as f:
            f.write(message)
        
        print(f"⚠️  Alert saved to {alert_file}")
        print("To enable actual Telegram broadcasting, configure message.send() tool")
        print("="*60 + "\n")
    
    def run(self):
        """Main monitoring loop"""
        print("🎯 Starting BTC/ETH/SOL Polymarket Trend Analysis Monitor")
        print("Monitoring: BTC, Ethereum, Solana")
        print("Focus: Momentum shifts, institutional sentiment, technical patterns")
        print("Alert triggers: Trend reversals, breakout patterns, accumulation/distribution")
        print("Telegram Group: -1002328055394")
        print("Significant threshold: 3% price movement")
        print("Scan interval: 60 seconds")
        print("Alert cooldown: 5 minutes")
        print("-" * 70)
        
        # Start the scanner
        if not self.start_scanner():
            return
        
        try:
            while True:
                # Check for alerts every 30 seconds
                alert_message = self.check_alerts()
                if alert_message:
                    self.send_telegram_alert(alert_message)
                    self.last_alert_time = datetime.now()
                
                # Check if scanner is still running
                if self.scanner_process.poll() is not None:
                    print("⚠️ Scanner process terminated, restarting...")
                    if not self.start_scanner():
                        print("❌ Failed to restart scanner, exiting...")
                        break
                
                # Wait before next check
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up processes and files"""
        if self.scanner_process:
            print("Terminating scanner process...")
            self.scanner_process.terminate()
            self.scanner_process.wait()
        
        # Clean up flag files
        for file in ['ALERT_FLAG', 'PENDING_ALERT.txt', 'crypto_alerts.json']:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    monitor = TelegramCryptoMonitor()
    monitor.run()