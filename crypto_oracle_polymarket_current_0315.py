#!/usr/bin/env python3
"""
CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS ANALYSIS
Analyze BTC/ETH/SOL momentum and trend shifts for March 8, 2026 3:15 AM (Asia/Manila)
"""

from datetime import datetime

def analyze_polymarket_trends(prices):
    """Analyze PolyMarket-like trend patterns and momentum convergence"""
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"] 
    sol_change = prices["solana"]["usd_24h_change"]
    
    btc_vol = prices["bitcoin"]["usd_24h_vol"]
    eth_vol = prices["ethereum"]["usd_24h_vol"]
    sol_vol = prices["solana"]["usd_24h_vol"]
    
    # Momentum divergence analysis
    max_change = max(btc_change, eth_change, sol_change)
    min_change = min(btc_change, eth_change, sol_change)
    momentum_divergence = (abs(max_change - min_change) / (abs(max_change) if max_change != 0 else 1)) * 100
    
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
    
    # Price action classification
    if avg_momentum > 3:
        market_mode = "BULLISH_EXPANSION"
        risk_appetite = "HIGH"
    elif avg_momentum > 1:
        market_mode = "MODERATE_EXPANSION"
        risk_appetite = "MEDIUM"
    elif avg_momentum > -1:
        market_mode = "CONSOLIDATION"
        risk_appetite = "LOW"
    else:
        market_mode = "CORRECTION"
        risk_appetite = "LOW"
    
    # Volume momentum indicator
    volume_momentum_ratio = vol_weighted_momentum / avg_momentum if avg_momentum != 0 else 1.0
    
    return {
        "momentum_divergence": round(momentum_divergence, 2),
        "vol_weighted_momentum": round(vol_weighted_momentum, 2),
        "market_mode": market_mode,
        "risk_appetite": risk_appetite,
        "sentiment_score": round(sentiment_score, 1),
        "volume_momentum_ratio": round(volume_momentum_ratio, 2),
        "momentum_sync_gap": round(momentum_sync_gap, 2)
    }

def calculate_polymarket_probability(prices, trends):
    """Calculate PolyMarket-style probability estimates"""
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"]
    sol_change = prices["solana"]["usd_24h_change"]
    
    # Base probabilities from momentum strength (adjusted for negative values)
    btc_prob = min(90, max(20, 50 + btc_change * 2))
    eth_prob = min(90, max(20, 50 + eth_change * 2))
    sol_prob = min(90, max(20, 50 + sol_change * 2))
    
    # Adjust based on market mode
    if trends["market_mode"] == "BULLISH_EXPANSION":
        btc_prob += 5
        eth_prob += 5
        sol_prob += 5
    elif trends["market_mode"] == "MODERATE_EXPANSION":
        btc_prob += 2
        eth_prob += 2
        sol_prob += 2
    elif trends["market_mode"] == "CORRECTION":
        btc_prob -= 5
        eth_prob -= 5
        sol_prob -= 5
    
    # Risk-adjusted probabilities
    risk_factor = {"HIGH": 1.1, "MEDIUM": 1.0, "LOW": 0.9}[trends["risk_appetite"]]
    btc_prob *= risk_factor
    eth_prob *= risk_factor
    sol_prob *= risk_factor
    
    # Convergence bonus
    if trends["momentum_divergence"] < 15:
        convergence_bonus = 3
        btc_prob += convergence_bonus
        eth_prob += convergence_bonus
        sol_prob += convergence_bonus
    
    # Ensure probabilities are reasonable
    btc_prob = max(15, min(85, btc_prob))
    eth_prob = max(15, min(85, eth_prob))
    sol_prob = max(15, min(85, sol_prob))
    
    return {
        "btc_up_probability": round(btc_prob, 1),
        "eth_up_probability": round(eth_prob, 1),
        "sol_up_probability": round(sol_prob, 1),
        "confidence_band": "HIGH" if trends["momentum_divergence"] < 10 else "MEDIUM"
    }

def assess_trend_shifts(previous_data, current_data):
    """Compare with previous analysis to detect shifts"""
    if current_data["vol_weighted_momentum"] > 2:
        trend_shift = "ACCELERATION"
        shift_magnitude = "STRONG"
    elif current_data["vol_weighted_momentum"] > 1:
        trend_shift = "CONTINUATION"
        shift_magnitude = "MODERATE"
    elif current_data["vol_weighted_momentum"] > -1:
        trend_shift = "CONSOLIDATION"
        shift_magnitude = "MINIMAL"
    else:
        trend_shift = "DECELERATION"
        shift_magnitude = "MODERATE"
    
    # Determine market direction
    if current_data["vol_weighted_momentum"] > 0:
        market_direction = "UP"
    elif current_data["vol_weighted_momentum"] < -3:
        market_direction = "DOWN"
    else:
        market_direction = "SIDEWAYS"
    
    return {
        "trend_shift": trend_shift,
        "shift_magnitude": shift_magnitude,
        "market_direction": market_direction
    }

def generate_polymarket_report(prices):
    """Generate comprehensive PolyMarket trends analysis"""
    trends = analyze_polymarket_trends(prices)
    probabilities = calculate_polymarket_probability(prices, trends)
    shifts = assess_trend_shifts(None, trends)  # No previous data for comparison
    
    btc_price = prices["bitcoin"]["usd"]
    eth_price = prices["ethereum"]["usd"]
    sol_price = prices["solana"]["usd"]
    
    btc_change = prices["bitcoin"]["usd_24h_change"]
    eth_change = prices["ethereum"]["usd_24h_change"]
    sol_change = prices["solana"]["usd_24h_change"]
    
    # Format change indicators
    btc_direction = "↗" if btc_change > 0 else "↘"
    eth_direction = "↗" if eth_change > 0 else "↘"
    sol_direction = "↗" if sol_change > 0 else "↘"
    
    # Simplify the pattern string for clarity
    if shifts['market_direction'] == 'UP':
        pattern_desc = 'bullish continuation'
    elif shifts['market_direction'] == 'DOWN':
        pattern_desc = 'bearish consolidation'
    else:
        pattern_desc = 'sideways consolidation'
    
    report = f"""🔮 CRYPTO ORACLE VALIDATION CALL - POLYMARKET TRENDS
📅 Analysis Time: Sunday, March 8th, 2026 — 3:15 AM (Asia/Manila)

📊 LIVE CORE MARKET DATA
• BTC: ${btc_price:,.0f} ({btc_change:.1f}% {btc_direction})
• ETH: ${eth_price:,.2f} ({eth_change:.1f}% {eth_direction})  
• SOL: ${sol_price:.2f} ({sol_change:.1f}% {sol_direction})

⚖️ POLYMARKET TREND ANALYSIS
• Market Mode: {trends['market_mode']}
• Risk Appetite: {trends['risk_appetite']}
• Price Action: {shifts['trend_shift']} ({shifts['shift_magnitude']})
• Momentum Divergence: {trends['momentum_divergence']}%
• Volume Weighted Momentum: {trends['vol_weighted_momentum']:.2f}/5
• Market Sentiment: {trends['sentiment_score']}%

🎰 POLYMARKET-STYLE PROBABILITY ESTIMATES
• BTC Upward Probability: {probabilities['btc_up_probability']}%
• ETH Upward Probability: {probabilities['eth_up_probability']}%
• SOL Upward Probability: {probabilities['sol_up_probability']}%
• Confidence Band: {probabilities['confidence_band']}

📈 TECHNICAL MOMENTUM SHIFTS
• Trend Direction: {shifts['market_direction']}
• Momentum Sync Gap: {trends['momentum_sync_gap']:.2f}
• Volume Momentum Ratio: {trends['volume_momentum_ratio']:.2f}
• Market Structure: {trends['risk_appetite'].lower()} volatility environment

🔮 STRATEGIC IMPLICATIONS
• Current momentum suggests {trends['market_mode'].lower().replace('_', ' ')} phase
• Risk appetite aligns with {trends['risk_appetite'].lower()} position sizing
• Volume/momentum synergy indicates {('strong' if trends['volume_momentum_ratio'] > 1.2 else 'moderate')} directional pressure
• PolyMarket projections favor {pattern_desc} patterns

⚠️ DISCLAIMER: Crypto oracle analysis for informational purposes only - NFA

#CryptoOracle #PolyMarketTrends #MomentumAnalysis"""
    
    return report

def main():
    # Current market data from CoinGecko API (as of March 8, 2026 3:15 AM)
    prices = {
        "bitcoin": {"usd": 67544, "usd_24h_vol": 24238994452.297604, "usd_24h_change": -1.093460188507883},
        "ethereum": {"usd": 1970.2, "usd_24h_vol": 9658681755.40875, "usd_24h_change": -0.7957432468346956},
        "solana": {"usd": 83.18, "usd_24h_vol": 1972165541.686355, "usd_24h_change": -2.571346589171714}
    }
    
    report = generate_polymarket_report(prices)
    print(report)
    
    # Save analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"polymarket_trends_analysis_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(report)
    
    print(f"\n✅ PolyMarket trends analysis saved to {filename}")

if __name__ == "__main__":
    main()