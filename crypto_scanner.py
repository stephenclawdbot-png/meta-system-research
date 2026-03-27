#!/usr/bin/env python3
"""
BTC/ETH/SOL Polymarket Trend Analysis Scanner
Continuously monitors cryptocurrency markets for significant movements
"""

import requests
import time
import json
import asyncio
import websockets
from datetime import datetime
import logging
from typing import Dict, List, Optional
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CryptoScreener:
    def __init__(self, telegram_channel: str = "-1002328055394"):
        self.telegram_channel = telegram_channel
        self.last_prices = {
            "BTC": 0,
            "ETH": 0,
            "SOL": 0
        }
        self.threshold_percent = 3.0  # 3% threshold
        self.check_interval = 30  # seconds
        
        # Technical analysis thresholds
        self.high_volume_multiplier = 2.0
        self.breakout_thresholds = {
            "BTC": 1000,  # USD breakouts
            "ETH": 50,
            "SOL": 3
        }
        
        # Market data sources
        self.data_sources = {
            "coinbase": "https://api.coinbase.com/v2/prices/{}-USD/spot",
            "binance": "https://api.binance.com/api/v3/ticker/price?symbol={}USDT",
            "coingecko": "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd&include_24hr_change=true"
        }
        
        # Coin mappings
        self.coin_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum", 
            "SOL": "solana"
        }
        
    def get_price_from_coinbase(self, symbol: str) -> Optional[float]:
        """Get price from Coinbase API"""
        try:
            url = self.data_sources["coinbase"].format(symbol)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return float(data["data"]["amount"])
        except Exception as e:
            logger.error(f"Coinbase API error for {symbol}: {e}")
        return None
    
    def get_price_from_binance(self, symbol: str) -> Optional[float]:
        """Get price from Binance API"""
        try:
            url = self.data_sources["binance"].format(symbol)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return float(data["price"])
        except Exception as e:
            logger.error(f"Binance API error for {symbol}: {e}")
        return None
    
    def get_price_from_coingecko(self, symbol: str) -> Optional[Dict]:
        """Get price and 24h change from CoinGecko"""
        try:
            coin_id = self.coin_ids[symbol]
            url = self.data_sources["coingecko"].format(coin_id)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                coin_data = data[coin_id]
                return {
                    "price": coin_data["usd"],
                    "change_24h": coin_data.get("usd_24h_change", 0)
                }
        except Exception as e:
            logger.error(f"CoinGecko API error for {symbol}: {e}")
        return None
    
    def calculate_price_movement(self, current_price: float, previous_price: float) -> float:
        """Calculate percentage price movement"""
        if previous_price == 0:
            return 0
        return ((current_price - previous_price) / previous_price) * 100
    
    def detect_significant_movement(self, symbol: str, current_price: float, change_24h: float) -> bool:
        """Detect if movement is significant based on thresholds"""
        
        # Price movement analysis
        if self.last_prices[symbol] > 0:
            movement = self.calculate_price_movement(current_price, self.last_prices[symbol])
            
            # Check threshold breaches
            if abs(movement) >= self.threshold_percent:
                logger.info(f"Significant price movement detected: {symbol} {movement:.2f}%")
                return True
        
        # Volume/change analysis (using 24h change as proxy)
        if abs(change_24h) >= self.threshold_percent:
            logger.info(f"Significant 24h change detected: {symbol} {change_24h:.2f}%")
            return True
            
        return False
    
    def generate_alert_message(self, symbol: str, current_price: float, 
                              change_24h: float, source: str) -> str:
        """Generate formatted Telegram alert message"""
        movement = 0
        if self.last_prices[symbol] > 0:
            movement = self.calculate_price_movement(current_price, self.last_prices[symbol])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S GMT+8")
        
        message = f"🚨 **{symbol} Market Alert** 🚨\n"
        message += f"📊 **Price**: ${current_price:,.2f}\n"
        
        if movement != 0:
            direction = "📈" if movement > 0 else "📉"
            message += f"{direction} **Movement**: {movement:+.2f}%\n"
        
        message += f"📅 **24h Change**: {change_24h:+.2f}%\n"
        message += f"🕐 **Time**: {timestamp}\n"
        message += f"📡 **Source**: {source}\n"
        
        # Add technical indicators
        if abs(movement) >= 5:
            message += "\n⚡ **HIGH VOLATILITY ALERT**\n"
        elif abs(movement) >= 3:
            message += "\n⚠️ **Significant Movement Detected**\n"
            
        # Trend analysis
        if change_24h > 5:
            message += "📊 **Trend**: Strong Bullish Momentum\n"
        elif change_24h < -5:
            message += "📊 **Trend**: Strong Bearish Pressure\n"
        elif change_24h > 0:
            message += "📊 **Trend**: Bullish Bias\n"
        else:
            message += "📊 **Trend**: Bearish Bias\n"
            
        return message
    
    def send_telegram_alert(self, message: str) -> bool:
        """Send alert to Telegram channel"""
        try:
            # Using OpenClaw message tool
            # This would be called via subprocess or API
            logger.info(f"Telegram alert ready: {message[:100]}...")
            # Implementation would depend on OpenClaw integration
            return True
        except Exception as e:
            logger.error(f"Telegram send error: {e}")
            return False
    
    async def monitor_markets(self):
        """Main monitoring loop"""
        logger.info("Starting cryptocurrency market monitoring...")
        
        # Initialize prices
        for symbol in ["BTC", "ETH", "SOL"]:
            data = self.get_price_from_coingecko(symbol)
            if data:
                self.last_prices[symbol] = data["price"]
                logger.info(f"Initial {symbol} price: ${data['price']:.2f}")
        
        while True:
            try:
                for symbol in ["BTC", "ETH", "SOL"]:
                    # Get latest data
                    data = self.get_price_from_coingecko(symbol)
                    
                    if not data:
                        continue
                        
                    current_price = data["price"]
                    change_24h = data["change_24h"]
                    
                    # Check for significant movements
                    if self.detect_significant_movement(symbol, current_price, change_24h):
                        alert_msg = self.generate_alert_message(
                            symbol, current_price, change_24h, "CoinGecko"
                        )
                        self.send_telegram_alert(alert_msg)
                    
                    # Update last price
                    self.last_prices[symbol] = current_price
                    
                    # Log status
                    logger.info(f"{symbol}: ${current_price:.2f} (24h: {change_24h:.2f}%)")
                
                # Wait before next check
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error

# Alternative implementation using WebSocket for real-time data
class WebSocketMonitor:
    def __init__(self, telegram_channel: str):
        self.telegram_channel = telegram_channel
        self.symbols = ["BTC", "ETH", "SOL"]
        
    async def binance_websocket(self):
        """Connect to Binance WebSocket for real-time data"""
        uri = "wss://stream.binance.com:9443/ws"
        streams = [f"{symbol.lower()}usdt@ticker" for symbol in self.symbols]
        stream_url = f"{uri}/{'/'.join(streams)}"
        
        try:
            async with websockets.connect(stream_url) as websocket:
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    self.process_websocket_data(data)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
    
    def process_websocket_data(self, data: dict):
        """Process real-time WebSocket data"""
        # Implementation for real-time analysis
        pass

def main():
    """Main entry point"""
    screener = CryptoScreener()
    
    try:
        # Run the monitoring loop
        asyncio.run(screener.monitor_markets())
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()