#!/usr/bin/env python3
"""Manually trigger a test alert to verify the Telegram alert pipeline"""

import json
from datetime import datetime

def create_test_alert():
    """Create a test alert to verify the pipeline"""
    
    # Create test alert data
    alert_data = {
        'timestamp': datetime.now().isoformat(),
        'alerts': [
            {
                'symbol': 'BTC',
                'type': 'momentum_trend',
                'direction': 'bullish',
                'strength': 3.5,
                'current_price': 67625.00
            },
            {
                'symbol': 'ETH',
                'type': 'volume_spike', 
                'factor': 2.4,
                'current_volume': 22000000000,
                'avg_volume': 19000000000
            }
        ],
        'sentiment': {
            'BTC': 'bullish',
            'ETH': 'bullish',
            'SOL': 'neutral'
        },
        'message': "⚡ **TEST ALERT** ⚡\nTest of Telegram alert pipeline\nMarket movement detected"
    }
    
    # Save alert data
    with open('crypto_alerts.json', 'w') as f:
        json.dump(alert_data, f, indent=2)
    
    # Create alert flag
    with open('ALERT_FLAG', 'w') as f:
        f.write(datetime.now().isoformat())
    
    print("✅ Test alert created!")
    print("The Telegram monitor should detect this alert within 30 seconds")
    print("Check telegram_monitor.log for output")
    
if __name__ == "__main__":
    create_test_alert()