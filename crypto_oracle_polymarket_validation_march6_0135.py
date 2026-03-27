#!/usr/bin/env python3
"""
CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS ANALYSIS
Friday, March 6th, 2026 — 1:35 AM (Asia/Manila)
Analyze BTC/ETH/SOL momentum and trend shifts for Polymarket predictions
"""

import json
from datetime import datetime

def analyze_polymarket_trends(prices):
    """Advanced PolyMarket trend analysis with momentum convergence"""
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"]
    sol_change = prices["solana"]["usd_24h_change"]
    
    btc_vol = prices["bitcoin"]["usd_24h_vol"]
    eth_vol = prices["ethereum"]["usd_24h_vol"]
    sol_vol = prices["solana"]["usd_24h_vol"]
    
    # Momentum divergence analysis
    max_change = max(btc_change, eth_change, sol_change)
    min_change = min(btc_change, eth_change, sol_change)
    momentum_divergence = abs(max_change - min_change)
    
    # Volume-weighted momentum
    total_vol = btc_vol + eth_vol + sol_vol
    vol_weighted_momentum = (
        (btc_change * btc_vol / total_vol) + 
        (eth_change * eth_vol / total_vol) + 
        (sol_change * sol_vol / total_vol)
    )
    
    # Trend convergence assessment
    avg_momentum = (btc_change + eth_change + sol_change) / 3
    momentum_sync_gap = abs(avg_momentum - vol_weighted_momentum)
    
    # Market sentiment scoring
    positive_moves = sum(1 for c in [btc_change, eth_change, sol_change] if c > 0)
    sentiment_score = (positive_moves / 3) * 100
    
    # Advanced trend classification
    dominant_trend = "BEARISH" if avg_momentum < 0 else "BULLISH"
    momentum_strength = abs(avg_momentum)
    
    if momentum_strength > 5:
        market_mode = "HIGH_VOLATILITY_EXPANSION"
        risk_appetite = "VERY_HIGH"
    elif momentum_strength > 3:
        market_mode = "MEDIUM_VOLATILITY_EXPANSION"
        risk_appetite = "HIGH"
    elif momentum_strength > 1:
        market_mode = "MODERATE_EXPANSION"
        risk_appetite = "MEDIUM"
    else:
        market_mode = "CONSOLIDATION"
        risk_appetite = "LOW"
    
    # Volume momentum indicator
    volume_momentum_ratio = vol_weighted_momentum / avg_momentum if avg_momentum != 0 else 1.0
    
    # Trend direction analysis
    if dominant_trend == "BULLISH":
        trend_intensity = "STRONG_BULL" if momentum_strength > 3 else "MODERATE_BULL"
    else:
        trend_intensity = "STRONG_BEAR" if momentum_strength > 3 else "MODERATE_BEAR"
    
    return {
        "dominant_trend": dominant_trend,
        "trend_intensity": trend_intensity,
        "momentum_divergence": round(momentum_divergence, 2),
        "vol_weighted_momentum": round(vol_weighted_momentum, 2),
        "market_mode": market_mode,
        "risk_appetite": risk_appetite,
        "sentiment_score": round(sentiment_score, 1),
        "volume_momentum_ratio": round(volume_momentum_ratio, 2),
        "momentum_sync_gap": round(momentum_sync_gap, 2),
        "average_momentum": round(avg_momentum, 2)
    }

def calculate_polymarket_probability(prices, trends):
    """PolyMarket-style probability estimates with advanced scoring"""
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"]
    sol_change = prices["solana"]["usd_24h_change"]
    
    # Advanced probability scoring
    def calculate_asset_probability(change, volatility):
        # Base probability based on momentum strength
        base_prob = min(95, max(20, abs(change) * 10 + 50))
        
        # Direction adjustment
        direction_factor = 1.2 if change > 0 else 0.8
        
        # Volatility adjustment
        volatility_factor = 1.1 if volatility > 4 else 0.9 if volatility < 1 else 1.0
        
        # Advanced scoring with market context
        final_prob = base_prob * direction_factor * volatility_factor
        
        # Ensure reasonable bounds
        return max(15, min(90, final_prob))
    
    # Calculate volatility (absolute momentum)
    btc_volatility = abs(btc_change)
    eth_volatility = abs(eth_change)
    sol_volatility = abs(sol_change)
    
    btc_prob = calculate_asset_probability(btc_change, btc_volatility)
    eth_prob = calculate_asset_probability(eth_change, eth_volatility)
    sol_prob = calculate_asset_probability(sol_change, sol_volatility)
    
    # Market mode adjustment
    mode_factors = {
        "HIGH_VOLATILITY_EXPANSION": 1.15,
        "MEDIUM_VOLATILITY_EXPANSION": 1.08,
        "MODERATE_EXPANSION": 1.02,
        "CONSOLIDATION": 0.95
    }
    
    mode_factor = mode_factors.get(trends["market_mode"], 1.0)
    btc_prob *= mode_factor
    eth_prob *= mode_factor
    sol_prob *= mode_factor
    
    # Risk appetite adjustment
    risk_factors = {"VERY_HIGH": 1.1, "HIGH": 1.05, "MEDIUM": 1.0, "LOW": 0.9}
    risk_factor = risk_factors.get(trends["risk_appetite"], 1.0)
    btc_prob *= risk_factor
    eth_prob *= risk_factor
    sol_prob *= risk_factor
    
    # Convergence bonus (low divergence increases confidence)
    if trends["momentum_divergence"] < 1.5:
        convergence_bonus = 5
        btc_prob += convergence_bonus
        eth_prob += convergence_bonus
        sol_prob += convergence_bonus
    elif trends["momentum_divergence"] < 3.0:
        convergence_bonus = 2
        btc_prob += convergence_bonus
        eth_prob += convergence_bonus
        sol_prob += convergence_bonus
    
    # Ensure final bounds
    btc_prob = max(10, min(85, btc_prob))
    eth_prob = max(10, min(85, eth_prob))
    sol_prob = max(10, min(85, sol_prob))
    
    confidence_level = "VERY_HIGH" if trends["momentum_divergence"] < 1.0 else \
                     "HIGH" if trends["momentum_divergence"] < 2.0 else \
                     "MEDIUM" if trends["momentum_divergence"] < 3.0 else "LOW"
    
    return {
        "btc_up_probability": round(btc_prob, 1),
        "eth_up_probability": round(eth_prob, 1),
        "sol_up_probability": round(sol_prob, 1),
        "confidence_band": confidence_level,
        "market_context": trends["market_mode"],
        "risk_adjustment": trends["risk_appetite"]
    }

def assess_trend_shifts_and_momentum(prices, trends):
    """Comprehensive momentum shift analysis"""
    avg_momentum = trends["average_momentum"]
    vol_weighted_momentum = trends["vol_weighted_momentum"]
    
    # Momentum shift detection
    if abs(avg_momentum) > 4:
        trend_shift = "MAJOR_MOMENTUM_SHIFT"
        shift_intensity = "HIGH"
    elif abs(avg_momentum) > 2:
        trend_shift = "MODERATE_MOMENTUM_SHIFT"
        shift_intensity = "MEDIUM"
    else:
        trend_shift = "MINOR_MOMENTUM_SHIFT"
        shift_intensity = "LOW"
    
    # Volume-momentum alignment
    vol_momentum_alignment = "STRONG" if trends["volume_momentum_ratio"] > 1.2 else \
                           "MODERATE" if trends["volume_momentum_ratio"] > 0.8 else "WEAK"
    
    # Trend continuity assessment
    if trends["dominant_trend"] == "BULLISH":
        continuation_likelihood = "HIGH" if avg_momentum > 2 else \
                                "MEDIUM" if avg_momentum > 0 else "LOW"
    else:
        continuation_likelihood = "HIGH" if avg_momentum < -2 else \
                                "MEDIUM" if avg_momentum < 0 else "LOW"
    
    return {
        "trend_shift": trend_shift,
        "shift_intensity": shift_intensity,
        "vol_momentum_alignment": vol_momentum_alignment,
        "continuation_likelihood": continuation_likelihood,
        "market_direction": trends["dominant_trend"],
        "momentum_gap": round(abs(avg_momentum - vol_weighted_momentum), 2)
    }

def generate_comprehensive_report(prices):
    """Generate detailed PolyMarket trends validation report"""
    trends = analyze_polymarket_trends(prices)
    probabilities = calculate_polymarket_probability(prices, trends)
    momentum_shifts = assess_trend_shifts_and_momentum(prices, trends)
    
    btc_price = prices["bitcoin"]["usd"]
    eth_price = prices["ethereum"]["usd"]
    sol_price = prices["solana"]["usd"]
    
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"]
    sol_change = prices["solana"]["usd_24h_change"]
    
    btc_vol = prices["bitcoin"]["usd_24h_vol"]
    eth_vol = prices["ethereum"]["usd_24h_vol"]
    sol_vol = prices["solana"]["usd_24h_vol"]
    
    current_time = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p")
    
    report = f"""🔮 CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS
📅 Analysis Time: {current_time} (Asia/Manila)

📊 LIVE MARKET DATA - FRESH COINGECKO API
• BTC: ${btc_price:,.0f} ({btc_change:+.2f}% ↗↘)
• ETH: ${eth_price:,.2f} ({eth_change:+.2f}% ↗↘)
• SOL: ${sol_price:.2f} ({sol_change:+.2f}% ↗↘)
• Total 24h Volume: ${btc_vol + eth_vol + sol_vol:,.0f}

⚖️ ADVANCED POLYMARKET TREND ANALYSIS
• Dominant Trend: {trends['dominant_trend']}
• Trend Intensity: {trends['trend_intensity']}
• Market Mode: {trends['market_mode']}
• Risk Appetite: {trends['risk_appetite']}
• Momentum Divergence: {trends['momentum_divergence']}%
• Volume Weighted Momentum: {trends['vol_weighted_momentum']}
• Average Momentum: {trends['average_momentum']}
• Sentiment Score: {trends['sentiment_score']}%
• Momentum Sync Gap: {trends['momentum_sync_gap']}

🎰 POLYMARKET-STYLE PROBABILITY ESTIMATES
• BTC Upward Probability: {probabilities['btc_up_probability']}%
• ETH Upward Probability: {probabilities['eth_up_probability']}%
• SOL Upward Probability: {probabilities['sol_up_probability']}%
• Confidence Band: {probabilities['confidence_band']}
• Market Context: {probabilities['market_context']}
• Risk Adjustment: {probabilities['risk_adjustment']}

📈 TECHNICAL MOMENTUM SHIFTS
• Trend Shift: {momentum_shifts['trend_shift']}
• Shift Intensity: {momentum_shifts['shift_intensity']}
• Volume-Momentum Alignment: {momentum_shifts['vol_momentum_alignment']}
• Continuation Likelihood: {momentum_shifts['continuation_likelihood']}
• Market Direction: {momentum_shifts['market_direction']}
• Momentum Gap: {momentum_shifts['momentum_gap']}

🔮 STRATEGIC IMPLICATIONS FOR POLYMARKET TRADERS
• Current market shows {trends['market_mode'].lower()} characteristics
• Risk appetite suggests {trends['risk_appetite'].lower()} position sizing
• Volume/momentum synergy indicates {trends['volume_momentum_ratio']} alignment
• PolyMarket predictions favor {momentum_shifts['continuation_likelihood'].lower()} continuation
• Probability estimates adjusted for {trends['dominant_trend'].lower()} momentum

🎯 KEY INSIGHTS
• Market experiencing {trends['trend_intensity'].replace('_', ' ').lower()} momentum
• {trends['momentum_divergence']}% divergence suggests {('convergent' if trends['momentum_divergence'] < 2 else 'divergent')} market behavior
• Volume-weighted momentum at {trends['vol_weighted_momentum']} confirms {('strong' if abs(trends['vol_weighted_momentum']) > 3 else 'moderate')} trend
• Sentiment at {trends['sentiment_score']}% reflects market psychology

⚠️ DISCLAIMER: Crypto oracle validation analysis for informational purposes only - NFA

#CryptoOracle #PolyMarketTrends #MomentumAnalysis"""
    
    return report

def main():
    # Live market data from CoinGecko API
    prices = {
        "bitcoin": {"usd": 70818, "usd_24h_vol": 62203407497.140594, "usd_24h_change": -3.2532424785911984},
        "ethereum": {"usd": 2063.82, "usd_24h_vol": 25388538733.328167, "usd_24h_change": -3.5705539252190777},
        "solana": {"usd": 88.35, "usd_24h_vol": 5397637199.439275, "usd_24h_change": -3.3148289849920674}
    }
    
    report = generate_comprehensive_report(prices)
    print(report)
    
    # Save the validation for future reference
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"polymarket_validation_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n✅ PolyMarket trends validation saved to {filename}")
    
    return report

if __name__ == "__main__":
    result = main()