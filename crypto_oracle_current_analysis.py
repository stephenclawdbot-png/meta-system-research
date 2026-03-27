#!/usr/bin/env python3
"""
Crypto Oracle - BTC/ETH/SOL Polymarket Trend Analysis
Single-run analysis for cron job execution
"""

import requests
import json
from datetime import datetime
import os
from typing import Dict, List, Optional

class CryptoOracle:
    def __init__(self):
        self.coin_ids = {
            "BTC": "bitcoin",
            "ETH": "ethereum", 
            "SOL": "solana"
        }
        
        # CoinGecko API endpoint
        self.coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        
    def get_current_data(self, symbol: str) -> Optional[Dict]:
        """Get current price and market data"""
        try:
            coin_id = self.coin_ids[symbol]
            url = self.coingecko_url.format(coin_id)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                coin_data = data[coin_id]
                return {
                    "symbol": symbol,
                    "price": coin_data["usd"],
                    "change_24h": coin_data.get("usd_24h_change", 0),
                    "volume_24h": coin_data.get("usd_24h_vol", 0)
                }
        except Exception as e:
            print(f"Error fetching {symbol} data: {e}")
        return None
    
    def analyze_trend(self, change_24h: float, volume: float) -> str:
        """Analyze trend based on price change and volume"""
        
        if change_24h > 8:
            return "STRONG BULLISH"
        elif change_24h > 3:
            return "BULLISH"
        elif change_24h > 0:
            return "SLIGHTLY BULLISH"
        elif change_24h == 0:
            return "FLAT"
        elif change_24h > -3:
            return "SLIGHTLY BEARISH"
        elif change_24h > -8:
            return "BEARISH"
        else:
            return "STRONG BEARISH"
    
    def calculate_momentum_score(self, change_24h: float, volume: float) -> int:
        """Calculate momentum score (0-100)"""
        # Base score from price movement
        if change_24h > 0:
            score = min(50 + (change_24h * 5), 100)
        else:
            score = max(50 + (change_24h * 5), 0)
            
        # Volume bonus
        if volume > 1000000000:  # High volume
            score += 10
        elif volume < 100000000:  # Low volume
            score -= 10
            
        return max(0, min(100, int(score)))
    
    def detect_trend_shift(self, data: Dict) -> str:
        """Detect if trend is shifting"""
        change = data["change_24h"]
        vol = data["volume_24h"]
        
        if abs(change) > 5 and vol > 500000000:
            if change > 0:
                return "BREAKOUT BULLISH"
            else:
                return "BREAKDOWN BEARISH"
        elif abs(change) > 2:
            if change > 0:
                return "GAINING BULLISH MOMENTUM"
            else:
                return "LOSING SUPPORT LEVELS"
        else:
            return "CONSOLIDATING"
    
    def generate_analysis_summary(self) -> Dict:
        """Generate comprehensive analysis of all three coins"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S GMT+8")
        
        symbols = ["BTC", "ETH", "SOL"]
        results = {}
        
        for symbol in symbols:
            data = self.get_current_data(symbol)
            if data:
                trend = self.analyze_trend(data["change_24h"], data["volume_24h"])
                momentum = self.calculate_momentum_score(data["change_24h"], data["volume_24h"])
                shift = self.detect_trend_shift(data)
                
                results[symbol] = {
                    "price": data["price"],
                    "change_24h": data["change_24h"],
                    "volume_24h": data["volume_24h"],
                    "trend": trend,
                    "momentum_score": momentum,
                    "trend_shift": shift
                }
        
        return {
            "timestamp": timestamp,
            "analysis": results
        }
    
    def format_analysis_for_output(self, summary: Dict) -> str:
        """Format analysis into readable text output"""
        output = []
        output.append("=== CRYPTO ORACLE VALIDATION CALL ===")
        output.append(f"Time: {summary['timestamp']}")
        output.append("")
        output.append("POLYMARKET TRENDS ANALYSIS - BTC/ETH/SOL")
        output.append("=" * 50)
        
        for symbol, data in summary['analysis'].items():
            output.append(f"\n**{symbol} Analysis:**")
            output.append(f"💰 Price: ${data['price']:,.2f}")
            output.append(f"📈 24h Change: {data['change_24h']:+.2f}%")
            output.append(f"📊 24h Volume: ${data['volume_24h']:,.0f}")
            output.append(f"📊 Trend: {data['trend']}")
            output.append(f"⚡ Momentum Score: {data['momentum_score']}/100")
            output.append(f"🔄 Trend Shift: {data['trend_shift']}")
        
        # Overall market assessment
        output.append("\n" + "=" * 50)
        output.append("OVERALL MARKET ASSESSMENT:")
        
        scores = [data["momentum_score"] for data in summary['analysis'].values()]
        avg_score = sum(scores) / len(scores) if scores else 50
        
        if avg_score >= 70:
            output.append("🚨 MARKET MOMENTUM: STRONGLY BULLISH")
        elif avg_score >= 60:
            output.append("📈 MARKET MOMENTUM: BULLISH")
        elif avg_score >= 40:
            output.append("⚖️ MARKET MOMENTUM: NEUTRAL")
        elif avg_score >= 30:
            output.append("📉 MARKET MOMENTUM: BEARISH")
        else:
            output.append("🔥 MARKET MOMENTUM: STRONGLY BEARISH")
        
        output.append(f"Average Momentum Score: {avg_score:.1f}/100")
        
        # Detect significant shifts
        shifts = [data["trend_shift"] for data in summary['analysis'].values()]
        bullish_shifts = sum(1 for shift in shifts if "BULLISH" in shift)
        bearish_shifts = sum(1 for shift in shifts if "BEARISH" in shift)
        
        if bullish_shifts >= 2:
            output.append("\n🚀 SIGNAL: Multiple coins showing bullish momentum")
        elif bearish_shifts >= 2:
            output.append("\n⚠️ SIGNAL: Multiple coins under bearish pressure")
        
        output.append("")
        output.append("=== END OF ANALYSIS ===")
        
        return "\n".join(output)

def main():
    """Main execution function"""
    oracle = CryptoOracle()
    
    try:
        print("Fetching current cryptocurrency data...")
        summary = oracle.generate_analysis_summary()
        
        if summary['analysis']:
            analysis_text = oracle.format_analysis_for_output(summary)
            print(analysis_text)
        else:
            print("ERROR: Could not fetch cryptocurrency data")
            
    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()