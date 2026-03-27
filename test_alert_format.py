#!/usr/bin/env python3
"""Test the Telegram alert formatting"""

from datetime import datetime

def test_message_format():
    # Simulate alert data
    alert_data = {
        'timestamp': datetime.now().isoformat(),
        'alerts': [
            {
                'symbol': 'BTC',
                'type': 'momentum_trend',
                'direction': 'bullish',
                'strength': 3.2,
                'current_price': 67564.00
            },
            {
                'symbol': 'ETH', 
                'type': 'volume_spike',
                'factor': 2.3,
                'current_volume': 21000000000,
                'avg_volume': 19000000000
            }
        ],
        'sentiment': {
            'BTC': 'bullish',
            'ETH': 'bullish',
            'SOL': 'neutral'
        }
    }
    
    # Format the message
    timestamp = datetime.fromisoformat(alert_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S GMT+8')
    
    message = "⚡ **CRYPTO MARKETS ALERT** ⚡\n"
    message += f"*Time:* {timestamp}\n\n"
    
    # Market status
    message += "*MARKET STATUS:*\n"
    sentiment = alert_data.get('sentiment', {})
    
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
    
    # Key patterns
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

if __name__ == "__main__":
    formatted_message = test_message_format()
    print("📋 Telegram Alert Format Test:")
    print("="*60)
    print(formatted_message)
    print("="*60)