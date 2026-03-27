#!/usr/bin/env python3
"""
CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS
Analyze BTC/ETH/SOL momentum and trend shifts
Current time: Monday, March 9th, 2026 — 10:43 AM (Asia/Manila)
"""

import requests
import json
from datetime import datetime
import time

class CryptoOraclePolymarketAnalyzer:
    def __init__(self):
        self.coin_data_url = "https://api.coingecko.com/api/v3/coins/markets"
        self.polymarket_api = "https://gamma-api.polymarket.com/contracts"
        
    def fetch_real_time_data(self):
        """Fetch current BTC/ETH/SOL data from CoinGecko"""
        try:
            params = {
                'vs_currency': 'usd',
                'ids': 'bitcoin,ethereum,solana',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(self.coin_data_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            crypto_data = {}
            for coin in data:
                symbol = coin['symbol'].upper()
                crypto_data[symbol] = {
                    'price': coin['current_price'],
                    'change_24h': coin['price_change_percentage_24h'],
                    'volume_24h': coin['total_volume'],
                    'market_cap': coin['market_cap'],
                    'name': coin['name']
                }
            
            return crypto_data
            
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return {}
    
    def analyze_momentum_advanced(self, crypto_data):
        """Advanced momentum analysis with Polymarket-style scoring"""
        momentum_analysis = {}
        
        for symbol, data in crypto_data.items():
            price_change = data['change_24h']
            volume = data['volume_24h']
            market_cap = data['market_cap']
            
            # Advanced momentum scoring (0-100 with multiple factors)
            base_score = 50
            
            # Price momentum contribution (max 25 points)
            price_momentum = 0
            if price_change > 0:
                price_momentum = min(25, price_change * 2.5)
            else:
                price_momentum = max(-25, price_change * 2.5)
            
            # Volume momentum (max 20 points)
            volume_ratio = volume / market_cap
            volume_momentum = 0
            if volume_ratio > 0.03:  # High volume relative to market cap
                volume_momentum = 20
            elif volume_ratio > 0.015:
                volume_momentum = 10
            elif volume_ratio < 0.005:  # Low volume
                volume_momentum = -10
            
            # Market cap adjusted momentum (larger coins get less volatility scoring)
            market_cap_adjustment = max(0.5, min(1.5, 1000000000000 / market_cap))
            
            # Combined score
            total_score = base_score + price_momentum + volume_momentum
            total_score *= market_cap_adjustment
            
            # Clamp to 0-100 range
            total_score = max(0, min(100, total_score))
            
            momentum_analysis[symbol] = {
                'momentum_score': round(total_score, 1),
                'strength': self.classify_momentum(total_score),
                'price_momentum': price_momentum,
                'volume_momentum': volume_momentum,
                'volume_ratio': volume_ratio,
                'market_cap_factor': market_cap_adjustment
            }
        
        return momentum_analysis
    
    def classify_momentum(self, score):
        """Classify momentum strength"""
        if score >= 80:
            return "STRONG_BULLISH"
        elif score >= 65:
            return "BULLISH"
        elif score >= 50:
            return "NEUTRAL_BULLISH"
        elif score >= 40:
            return "NEUTRAL"
        elif score >= 20:
            return "BEARISH"
        else:
            return "STRONG_BEARISH"
    
    def detect_trend_shifts(self, crypto_data, momentum_analysis):
        """Detect potential trend shifts and reversals"""
        shifts = []
        
        # Look for divergence patterns
        scores = [m['momentum_score'] for m in momentum_analysis.values()]
        avg_score = sum(scores) / len(scores)
        divergence = max(scores) - min(scores)
        
        if divergence > 25:
            shifts.append("High divergence detected - selective opportunities")
        
        for symbol, data in crypto_data.items():
            momentum = momentum_analysis[symbol]
            
            # Overbought/oversold signals
            if data['change_24h'] > 8:
                shifts.append(f"{symbol} potentially overbought (+{data['change_24h']:.1f}%)")
            elif data['change_24h'] < -8:
                shifts.append(f"{symbol} potentially oversold ({data['change_24h']:.1f}%)")
            
            # Volume divergence signals
            if momentum['volume_ratio'] > 0.04 and abs(data['change_24h']) < 2:
                shifts.append(f"{symbol} high volume with low price change - breakout potential")
            elif momentum['volume_ratio'] < 0.005 and abs(data['change_24h']) > 3:
                shifts.append(f"{symbol} low volume move - weak momentum")
        
        return shifts
    
    def calculate_polymarket_probabilities(self, crypto_data, momentum_analysis):
        """Calculate Polymarket-style probability estimates"""
        probabilities = {}
        
        for symbol, momentum in momentum_analysis.items():
            score = momentum['momentum_score']
            
            # Base probability derived from momentum score
            base_prob = (score / 100) * 80 + 10  # Scale 0-100 to 10-90%
            
            # Adjust based on recent performance
            price_change = crypto_data[symbol]['change_24h']
            if price_change > 0:
                prob_adjustment = min(5, price_change)
            else:
                prob_adjustment = max(-5, price_change)
            
            # Volume confidence adjustment
            volume_ratio = momentum['volume_ratio']
            volume_confidence = min(5, volume_ratio * 100)  # Higher volume = higher confidence
            
            final_prob = base_prob + prob_adjustment + volume_confidence
            final_prob = max(10, min(90, final_prob))  # Cap at reasonable bounds
            
            probabilities[symbol] = {
                'probability': round(final_prob),
                'confidence': self.get_confidence_level(volume_ratio)
            }
        
        return probabilities
    
    def get_confidence_level(self, volume_ratio):
        """Determine confidence level based on volume"""
        if volume_ratio > 0.03:
            return "HIGH"
        elif volume_ratio > 0.015:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_cross_asset_analysis(self, crypto_data, momentum_analysis):
        """Analyze relationships between assets"""
        analysis = {
            'market_sentiment': 'NEUTRAL',
            'dominant_trend': 'MIXED',
            'correlation_strength': 'MODERATE'
        }
        
        bullish_count = sum(1 for m in momentum_analysis.values() if 'BULLISH' in m['strength'])
        bearish_count = sum(1 for m in momentum_analysis.values() if 'BEARISH' in m['strength'])
        
        if bullish_count >= 2:
            analysis['market_sentiment'] = 'BULLISH'
            analysis['dominant_trend'] = 'UPWARD'
        elif bearish_count >= 2:
            analysis['market_sentiment'] = 'BEARISH'
            analysis['dominant_trend'] = 'DOWNWARD'
        
        # Correlation strength based on divergence
        scores = [m['momentum_score'] for m in momentum_analysis.values()]
        max_divergence = max(scores) - min(scores)
        
        if max_divergence < 15:
            analysis['correlation_strength'] = 'STRONG'
        elif max_divergence < 30:
            analysis['correlation_strength'] = 'MODERATE'
        else:
            analysis['correlation_strength'] = 'WEAK'
        
        return analysis
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("🔮 CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS")
        print("=" * 80)
        print("Analyzing BTC/ETH/SOL Momentum & Trend Shifts")
        print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
        print()
        
        # Fetch real-time data
        crypto_data = self.fetch_real_time_data()
        
        if not crypto_data:
            print("❌ Failed to fetch crypto data")
            return
        
        # Run analysis
        momentum_analysis = self.analyze_momentum_advanced(crypto_data)
        trend_shifts = self.detect_trend_shifts(crypto_data, momentum_analysis)
        probabilities = self.calculate_polymarket_probabilities(crypto_data, momentum_analysis)
        cross_analysis = self.generate_cross_asset_analysis(crypto_data, momentum_analysis)
        
        # Output results
        print("📊 REAL-TIME CRYPTO ANALYSIS:")
        print("-" * 80)
        for symbol, data in crypto_data.items():
            momentum = momentum_analysis[symbol]
            change_sign = "+" if data['change_24h'] > 0 else ""
            print(f"{symbol: <6} | ${data['price']:,.2f} | {change_sign}{data['change_24h']:.1f}% | Momentum: {momentum['strength']} ({momentum['momentum_score']:.0f}/100)")
        
        print()
        print("🎯 ADVANCED MOMENTUM ANALYSIS:")
        print("-" * 35)
        for symbol, momentum in momentum_analysis.items():
            print(f"{symbol}: {momentum['strength']} | Score: {momentum['momentum_score']:.0f}/100")
            print(f"  - Price Momentum: {momentum['price_momentum']:+.1f} pts")
            print(f"  - Volume Momentum: {momentum['volume_momentum']:+.1f} pts")
            print(f"  - Volume Ratio: {momentum['volume_ratio']:.4f}")
        
        print()
        print("⚡ TREND SHIFT DETECTION:")
        print("-" * 35)
        if trend_shifts:
            for shift in trend_shifts:
                print(f"• {shift}")
        else:
            print("• No significant shift signals detected")
        
        print()
        print("🎰 POLYMARKET-STYLE PROBABILITY ESTIMATES:")
        print("-" * 45)
        for symbol, prob_data in probabilities.items():
            print(f"• {symbol} upward probability: {prob_data['probability']}% (confidence: {prob_data['confidence']})")
        
        print()
        print("🌍 CROSS-ASSET ANALYSIS:")
        print("-" * 30)
        print(f"• Market Sentiment: {cross_analysis['market_sentiment']}")
        print(f"• Dominant Trend: {cross_analysis['dominant_trend']}")
        print(f"• Correlation Strength: {cross_analysis['correlation_strength']}")
        
        print()
        print("💡 STRATEGIC IMPLICATIONS:")
        print("-" * 30)
        
        # Generate strategic insights
        bullish_coins = [s for s, m in momentum_analysis.items() if 'BULLISH' in m['strength']]
        bearish_coins = [s for s, m in momentum_analysis.items() if 'BEARISH' in m['strength']]
        
        if bullish_coins:
            print(f"• Focus opportunities: {', '.join(bullish_coins)}")
        if bearish_coins:
            print(f"• Caution areas: {', '.join(bearish_coins)}")
        
        if cross_analysis['correlation_strength'] == 'STRONG':
            print("• High correlation suggests market-wide movement")
        elif cross_analysis['correlation_strength'] == 'WEAK':
            print("• Low correlation indicates selective opportunities")
        
        print()
        print("📈 NEXT 24H OUTLOOK:")
        print("-" * 25)
        
        for symbol, momentum in momentum_analysis.items():
            if momentum['strength'] == "STRONG_BULLISH":
                print(f"• {symbol}: Continued upward momentum likely")
            elif momentum['strength'] == "STRONG_BEARISH":
                print(f"• {symbol}: Downward pressure persists")
            elif "BULLISH" in momentum['strength']:
                print(f"• {symbol}: Mild upward bias")
            elif "BEARISH" in momentum['strength']:
                print(f"• {symbol}: Mild downward bias")
            else:
                print(f"• {symbol}: Sideways consolidation expected")
        
        print()
        print("⚠️ DISCLAIMER: Crypto markets are highly volatile. This is analysis, not financial advice.")
        print(f"   Oracle validation completed at {datetime.now().strftime('%I:%M %p')}")
        print()
        print("#CryptoOracle #PolyMarketTrends #MomentumAnalysis #TrendShifts")
        
        return {
            'crypto_data': crypto_data,
            'momentum_analysis': momentum_analysis,
            'trend_shifts': trend_shifts,
            'probabilities': probabilities,
            'cross_analysis': cross_analysis
        }

if __name__ == "__main__":
    analyzer = CryptoOraclePolymarketAnalyzer()
    results = analyzer.generate_validation_report()