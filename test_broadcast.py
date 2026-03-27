#!/usr/bin/env python3
"""Test broadcast format"""

from datetime import datetime

def format_sample_alert():
    """Show what alert looks like"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')
    
    alert = """⚡ **CRYPTO MARKET MOVES** ⚡
• BTC: trending up 3.2%
• Price: $67,890.00  
• Volume: up 200%
• Pattern: Bull flag breakout
• Signal: Accumulation phase

_Real-time actionable info ({})_
""".format(timestamp)
    
    print(alert)
    return alert

if __name__ == "__main__":
    print("📤 Sample Telegram Alert Format:")
    print("="*50)
    format_sample_alert()
    print("="*50)
    print("\nThis is what alerts will look like in your Telegram group!")