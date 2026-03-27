#!/usr/bin/env python3
"""
Crypto Oracle Validation - Polymarket Trends Analysis
Analyzes BTC, ETH, SOL momentum and trend shifts for Polymarket prediction markets
"""

import requests
import json
import time
from datetime import datetime, timedelta
import math

class CryptoOracle:
    def __init__(self):
        self.symbols = ['BTC', 'ETH', 'SOL']
        self.coingecko_ids = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana'
        }
        
    def fetch_price_data(self, symbol, days=7):
        """Fetch price data from Yahoo Finance API"""
        try:
            # Map symbols to Yahoo Finance tickers
            yahoo_tickers = {
                'BTC': 'BTC-USD',
                'ETH': 'ETH-USD', 
                'SOL': 'SOL-USD'
            }
            
            ticker = yahoo_tickers[symbol]
            
            # Use yfinance library if available
            try:
                import yfinance as yf
                stock = yf.Ticker(ticker)
                
                # Get historical data
                hist = stock.history(period=f"{days}d", interval="1h")
                
                if hist.empty:
                    print(f"No data available for {symbol}")
                    return []
                
                # Convert to timestamp, price format
                prices = []
                for idx, row in hist.iterrows():
                    timestamp = int(idx.timestamp() * 1000)  # Convert to milliseconds
                    price = float(row['Close'])
                    prices.append((timestamp, price))
                
                return prices
                
            except ImportError:
                print("yfinance not available, trying alternative API...")
                # Fallback to CoinGecko public endpoint
                import random
                # Generate mock data for demonstration
                base_prices = {'BTC': 65000, 'ETH': 3500, 'SOL': 150}
                base_price = base_prices.get(symbol, 100)
                
                prices = []
                current_time = int(time.time() * 1000)
                
                for i in range(24 * days):
                    timestamp = current_time - (24 * days - i) * 3600 * 1000
                    # Add some realistic price movement
                    price = base_price * (1 + random.uniform(-0.01, 0.01) * i)
                    prices.append((timestamp, price))
                
                print(f"⚠️ Using mock data for {symbol} (no API access)")
                return prices
                
        except Exception as e:
            print(f"Error fetching {symbol} data: {e}")
            return []
    
    def calculate_momentum_indicators(self, price_data):
        """Calculate momentum indicators from price data"""
        if len(price_data) < 24:
            return {}
        
        # Get recent data (last 24 hours)
        recent_prices = [p[1] for p in price_data[-24:]]
        
        # Get mid-term data (last 7 days)
        mid_prices = [p[1] for p in price_data[-168:]] if len(price_data) >= 168 else recent_prices
        
        # Short-term momentum (last 6 hours vs previous 6 hours)
        if len(recent_prices) >= 12:
            recent_6h = recent_prices[-6:]
            prev_6h = recent_prices[-12:-6]
            short_momentum = (sum(recent_6h)/6) / (sum(prev_6h)/6) - 1
        else:
            short_momentum = 0
        
        # Medium-term momentum (last 24h vs previous 24h)
        if len(mid_prices) >= 48:
            recent_24h = mid_prices[-24:]
            prev_24h = mid_prices[-48:-24]
            medium_momentum = (sum(recent_24h)/24) / (sum(prev_24h)/24) - 1
        else:
            medium_momentum = short_momentum
            
        # Volatility (standard deviation of returns)
        returns = []
        for i in range(1, len(recent_prices)):
            if recent_prices[i-1] > 0:
                ret = (recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1]
                returns.append(ret)
        
        volatility = math.sqrt(sum([r*r for r in returns]) / len(returns)) if returns else 0
        
        # Current vs all-time high (in last 7 days)
        max_price = max(mid_prices) if mid_prices else 0
        current_price = recent_prices[-1] if recent_prices else 0
        ath_ratio = current_price / max_price - 1 if max_price > 0 else 0
        
        return {
            'short_momentum_pct': round(short_momentum * 100, 2),
            'medium_momentum_pct': round(medium_momentum * 100, 2),
            'volatility_pct': round(volatility * 100, 2),
            'ath_distance_pct': round(ath_ratio * 100, 2),
            'current_price': current_price
        }
    
    def analyze_trend_shifts(self, price_data):
        """Analyze potential trend shifts using moving averages"""
        if len(price_data) < 50:
            return "insufficient_data"
            
        prices = [p[1] for p in price_data]
        
        # Moving averages
        sma_12 = sum(prices[-12:]) / 12
        sma_24 = sum(prices[-24:]) / 24
        sma_50 = sum(prices[-50:]) / 50
        
        # Trend analysis
        current_price = prices[-1]
        
        # Golden cross/death cross signals
        short_vs_long = sma_12 - sma_50
        medium_vs_long = sma_24 - sma_50
        
        signals = []
        
        # Golden cross (bullish)
        if sma_12 > sma_50 and sma_24 < sma_50:
            signals.append("golden_cross_forming")
        elif sma_12 > sma_50 and sma_24 > sma_50:
            signals.append("golden_cross_active")
            
        # Death cross (bearish)  
        if sma_12 < sma_50 and sma_24 > sma_50:
            signals.append("death_cross_forming")
        elif sma_12 < sma_50 and sma_24 < sma_50:
            signals.append("death_cross_active")
            
        # Price vs moving averages
        if current_price > sma_12:
            signals.append("above_short_ma")
        else:
            signals.append("below_short_ma")
            
        if current_price > sma_50:
            signals.append("above_long_ma")
        else:
            signals.append("below_long_ma")
            
        return {
            'signals': signals,
            'sma_12': sma_12,
            'sma_24': sma_24,
            'sma_50': sma_50,
            'price_vs_sma12_pct': round((current_price/sma_12 - 1) * 100, 2),
            'price_vs_sma50_pct': round((current_price/sma_50 - 1) * 100, 2)
        }
    
    def generate_polymarket_insights(self, symbol, momentum_data, trend_data):
        """Generate Polymarket-specific insights for prediction markets"""
        
        insights = []
        confidence_score = 50  # Base confidence
        
        # Momentum-based insights
        momentum_pct = momentum_data['short_momentum_pct']
        volatility_pct = momentum_data['volatility_pct']
        
        if momentum_pct > 3:
            insights.append(f"Strong bullish momentum ({momentum_pct}% short-term)")
            confidence_score += 15
        elif momentum_pct < -3:
            insights.append(f"Strong bearish momentum ({momentum_pct}% short-term)")
            confidence_score -= 15
        
        if volatility_pct > 5:
            insights.append("High volatility - uncertain environment")
            confidence_score -= 10
        elif volatility_pct < 1:
            insights.append("Low volatility - stable conditions")
            confidence_score += 5
        
        # Trend-based insights
        signals = trend_data.get('signals', [])
        
        if 'golden_cross_active' in signals:
            insights.append("Golden cross active - bullish trend")
            confidence_score += 20
        elif 'death_cross_active' in signals:
            insights.append("Death cross active - bearish trend")
            confidence_score -= 20
            
        if 'above_long_ma' in signals:
            insights.append("Trading above long-term average")
            confidence_score += 10
        else:
            insights.append("Trading below long-term average")
            confidence_score -= 10
        
        # Ensure confidence is between 0-100
        confidence_score = max(0, min(100, confidence_score))
        
        return {
            'symbol': symbol,
            'insights': insights,
            'confidence_score': confidence_score,
            'recommendation': self.map_confidence_to_recommendation(confidence_score)
        }
    
    def map_confidence_to_recommendation(self, score):
        """Map confidence score to Polymarket recommendation"""
        if score >= 80:
            return "STRONG_BUY"
        elif score >= 70:
            return "BUY"
        elif score >= 60:
            return "SLIGHT_BUY"
        elif score >= 40:
            return "HOLD"
        elif score >= 30:
            return "SLIGHT_SELL"
        elif score >= 20:
            return "SELL"
        else:
            return "STRONG_SELL"
    
    def run_analysis(self):
        """Run complete analysis for all symbols"""
        print(f"🔮 Crypto Oracle Validation - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)
        
        results = {}
        
        for symbol in self.symbols:
            print(f"\n📊 Analyzing {symbol}...")
            
            # Fetch price data
            price_data = self.fetch_price_data(symbol)
            if not price_data:
                print(f"❌ Failed to fetch {symbol} data")
                continue
                
            # Calculate momentum indicators
            momentum_data = self.calculate_momentum_indicators(price_data)
            if not momentum_data:
                print(f"❌ Insufficient data for {symbol} momentum analysis")
                continue
                
            # Analyze trend shifts
            trend_data = self.analyze_trend_shifts(price_data)
            
            # Generate Polymarket insights
            insights = self.generate_polymarket_insights(symbol, momentum_data, trend_data)
            
            results[symbol] = {
                'momentum': momentum_data,
                'trend': trend_data,
                'insights': insights
            }
            
            # Print results
            print(f"💰 Current Price: ${momentum_data['current_price']:,.2f}")
            print(f"📈 Short-term Momentum: {momentum_data['short_momentum_pct']}%")
            print(f"📊 Medium-term Momentum: {momentum_data['medium_momentum_pct']}%")
            print(f"🌊 Volatility: {momentum_data['volatility_pct']}%")
            print(f"🎯 Trend Signals: {', '.join(trend_data.get('signals', ['none']))}")
            print(f"💡 Insights: {', '.join(insights['insights'])}")
            print(f"🎲 Polymarket Recommendation: {insights['recommendation']} (Confidence: {insights['confidence_score']}/100)")
        
        print("\n" + "=" * 60)
        print("🎯 Polymarket Trading Summary")
        print("=" * 60)
        
        # Generate overall recommendations
        for symbol, data in results.items():
            insights = data['insights']
            print(f"\n{symbol}:")
            print(f"  Recommendation: {insights['recommendation']}")
            print(f"  Confidence: {insights['confidence_score']}/100")
            print(f"  Key Factors: {'; '.join(insights['insights'][:3])}")
        
        return results

if __name__ == "__main__":
    oracle = CryptoOracle()
    results = oracle.run_analysis()