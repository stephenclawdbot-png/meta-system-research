#!/usr/bin/env node

// Alpha Scanner Executor - Continuous Framework
// Powered by Stephen's Crypto Oracle Analytics

const cryptoOracleScan = async () => {
  console.log("🔮 CRYPTO ORACLE SCAN - 15min");
  
  try {
    // Fetch major asset data
    const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true');
    const data = await response.json();
    
    const btcChange = data.bitcoin.usd_24h_change;
    const ethChange = data.ethereum.usd_24h_change;
    const solChange = data.solana.usd_24h_change;
    
    // Analyze trends for Polymarket insights
    const prediction = {
      btc_trend: btcChange > 0 ? "" : "",
      eth_trend: ethChange > 0 ? "" : "",
      sol_trend: solChange > 0 ? "" : "",
      momentum_strength: Math.max(Math.abs(btcChange), Math.abs(ethChange), Math.abs(solChange))
    };
    
    return {
      timestamp: new Date().toISOString(),
      scan_type: "crypto_oracle",
      data: data,
      prediction: prediction,
      polymarket_insight: detectPolymarketTrend(data)
    };
  } catch (error) {
    console.error("Crypto oracle scan failed:", error);
    return { error: "Scan failed" };
  }
};

const memecoinScan = async () => {
  console.log("💰 MEMECOIN ALPHA SCAN - 5min");
  
  try {
    // Scan DexScreener for new meme coins
    const response = await fetch('https://api.dexscreener.com/latest/dex/search?q=meme&limit=50');
    const dexscreenerData = await response.json();
    
    // Filter for sub 30k-200k mcap tokens
    const potentialGems = dexscreenerData.pairs.filter(pair => {
      const mcap = pair.fdv || pair.marketCap;
      return mcap >= 30000 && mcap <= 200000 &&
             pair.volume?.h24 >= 1000 &&
             isRecentLaunch(pair.pairCreatedAt) &&
             hasHealthyBuyPressure(pair.txns);
    });
    
    // Sort by strongest signals
    const rankedGems = potentialGems.sort((a, b) => {
      const aScore = calculateAlphaScore(a);
      const bScore = calculateAlphaScore(b);
      return bScore - aScore;
    });
    
    return {
      timestamp: new Date().toISOString(),
      scan_type: "memecoin",
      gems_found: rankedGems.length,
      top_gems: rankedGems.slice(0, 3),
      analysis: performSmartAnalysis(rankedGems)
    };
  } catch (error) {
    console.error("Memecoin scan failed:", error);
    return { error: "Scan failed" };
  }
};

const detectPolymarketTrend = (data) => {
  // Smart detection for institutional vs retail sentiment
  const changes = [
    data.bitcoin.usd_24h_change,
    data.ethereum.usd_24h_change,
    data.solana.usd_24h_change
  ];
  
  const volatility = Math.max(...changes.map(Math.abs));
  const direction = changes.reduce((sum, change) => sum + Math.sign(change), 0);
  
  return {
    overall_bias: direction > 0 ? "bullish" : "bearish",
    volatility_level: volatility > 5 ? "high" : volatility > 2 ? "medium" : "low",
    trend_strength: Math.abs(direction)
  };
};

const isRecentLaunch = (timestamp) => {
  const launchTime = new Date(timestamp);
  const hoursSinceLaunch = (Date.now() - launchTime.getTime()) / (1000 * 60 * 60);
  return hoursSinceLaunch <= 24; // Within 24 hours
};

const hasHealthyBuyPressure = (txns) => {
  const buys = txns?.h24?.buys || 0;
  const sells = txns?.h24?.sells || 0;
  const total = buys + sells;
  return total >= 20 && buys / total >= 0.6; // Minimum 60% buy pressure
};

const calculateAlphaScore = (token) => {
  let score = 0;
  
  // Volume momentum
  score += Math.log10(token.volume?.h24 || 1);
  
  // Buy pressure
  const buys = token.txns?.h24?.buys || 0;
  const sells = token.txns?.h24?.sells || 0;
  const buyRatio = buys / (buys + sells);
  score += buyRatio * 10;
  
  // Liquidity depth
  const liquidity = token.liquidity?.usd || 0;
  score += liquidity > 5000 ? 5 : liquidity > 1000 ? 3 : 1;
  
  return Math.round(score * 100) / 100;
};

const performSmartAnalysis = (gems) => {
  if (gems.length === 0) return { insight: "No alpha detected" };
  
  const bestGem = gems[0];
  return {
    top_gem: bestPair?.baseToken?.symbol || "Unknown",
    alpha_score: calculateAlphaScore(bestGem),
    volume_momentum: bestGem.volume?.h24 || 0,
    buy_pressure: calculateBuyPressure(bestGem.txns),
    liquidity_strength: bestGem.liquidity?.usd || 0,
    recommendation: "Analyze further for timing"
  };
};

const calculateBuyPressure = (txns) => {
  const buys = txns?.h24?.buys || 0;
  const sells = txns?.h24?.sells || 0;
  return buys / (buys + sells);
};

// Export for heartbeat integration
module.exports = { cryptoOracleScan, memecoinScan };