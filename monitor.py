#!/usr/bin/env python3
"""
Monitor script that runs the crypto scanner and pings when alerts are detected
"""

import time
import subprocess
import os
import json
from datetime import datetime
import requests
import signal
import sys

class CryptoMonitor:
    def __init__(self):
        self.scanner_process = None
        self.last_alert_check = datetime.now()
        self.alert_cooldown = 300  # 5 minutes between alerts
        
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
                        
                        # Format alert message
                        message = self.format_alert_message(alert_data)
                        
                        # Remove the flag to prevent duplicate alerts
                        os.remove('ALERT_FLAG')
                        
                        return message
            
        except Exception as e:
            print(f"Error checking alerts: {e}")
        
        return None
    
    def format_alert_message(self, alert_data):
        """Format the alert message for Telegram"""
        timestamp = datetime.fromisoformat(alert_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S GMT+8')
        
        message = f"🚨 **CRYPTO MARKET ALERT** 🚨\n"
        message += f"*Time:* {timestamp}\n\n"
        
        # Add individual alerts
        if alert_data.get('alerts'):
            message += "*ALERTS DETECTED:*\n\n"
            for alert in alert_data['alerts']:
                symbol = alert.get('symbol', 'UNKNOWN')
                alert_type = alert.get('type', '')
                
                if alert_type == 'momentum_trend':
                    message += f"📊 *{symbol} - {alert['direction'].upper()} MOMENTUM*\n"
                    message += f"Price: ${alert['current_price']:.2f}\n"
                    message += f"Strength: {alert['strength']:.1f}% move\n\n"
                
                elif alert_type == 'volume_spike':
                    message += f"📈 *{symbol} - VOLUME SPIKE*\n"
                    message += f"Volume: {alert['current_volume']:.0f} (avg: {alert['avg_volume']:.0f})\n"
                    message += f"Spike Factor: {alert['factor']:.1f}x\n\n"
                
                elif alert_type == 'rsi_overbought':
                    message += f"⚠️ *{symbol} - OVERBOUGHT (RSI)*\n"
                    message += f"RSI: {alert['rsi_value']:.1f}\n"
                    message += f"Price: ${alert['current_price']:.2f}\n\n"
                
                elif alert_type == 'rsi_oversold':
                    message += f"🛑 *{symbol} - OVERSOLD (RSI)*\n"
                    message += f"RSI: {alert['rsi_value']:.1f}\n"
                    message += f"Price: ${alert['current_price']:.2f}\n\n"
        
        # Add market sentiment
        if alert_data.get('sentiment'):
            message += "*MARKET SENTIMENT:*\n"
            for symbol, sentiment in alert_data['sentiment'].items():
                message += f"{symbol}: {sentiment}\n"
        
        return message
    
    def send_alert(self, message):
        """Send alert via Telegram (placeholder - would need bot integration)"""
        print("\n" + "="*50)
        print("📢 ALERT READY FOR SENDING:")
        print("="*50)
        print(message)
        print("="*50)
        print("(In production, this would send via Telegram)")
        print("="*50 + "\n")
        
        # In a real implementation, this would use message.send or a webhook
        # For now, we'll simulate by writing to a file that the main agent can check
        with open('PENDING_ALERT.txt', 'w') as f:
            f.write(message)
    
    def run(self):
        """Main monitoring loop"""
        print("🎯 Starting BTC/ETH/SOL Polymarket Trend Analysis Monitor")
        print("Monitoring: BTC, Ethereum, Solana")
        print("Focus: Momentum shifts, institutional sentiment, technical patterns")
        print("Alert triggers: Trend reversals, breakout patterns, accumulation/distribution")
        print("Scan interval: 60 seconds")
        print("Alert cooldown: 5 minutes")
        print("-" * 60)
        
        # Start the scanner
        if not self.start_scanner():
            return
        
        try:
            while True:
                # Check for alerts every 30 seconds
                alert_message = self.check_alerts()
                if alert_message:
                    self.send_alert(alert_message)
                
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
    monitor = CryptoMonitor()
    monitor.run()