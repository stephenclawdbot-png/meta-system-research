#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import time

def fetch_dexscreener_tokens():
    """Fetch tokens from DexScreener trending endpoint"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching tokens: {e}")
        return None

def analyze_alpha_potential(tokens_data):
    """Analyze tokens for alpha potential in the 30k-200k mcap range"""
    if not tokens_data or 'pairs' not in tokens_data:
        return []
    
    alpha_gems = []
    
    for token in tokens_data['pairs']:
        try:
            # Get market cap
            fd_mcap = token.get('fdv', 0)  # Fully diluted valuation
            actual_mcap = token.get('marketCap', fd_mcap)  # Use marketCap if available
            
            # Filter by market cap range
            if actual_mcap < 30000 or actual_mcap > 200000:
                continue
            
            # Get token details
            base_token = token.get('baseToken', {})
            symbol = base_token.get('symbol', '').upper()
            name = base_token.get('name', '')
            
            # Skip wrapped tokens and stablecoins
            wrapped_keywords = ['wrapped', 'wbtc', 'weth', 'wsol', 'wmatic', 'wbnb', 'usdc', 'usdt', 'busd']
            if any(keyword in name.lower() for keyword in wrapped_keywords):
                continue
            if any(keyword in symbol.lower() for keyword in wrapped_keywords):
                continue
            
            # Calculate metrics
            volume_24h = token.get('volume', {}).get('h24', 0)
            price_change_24h = token.get('priceChange', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            # Transaction data
            txns_24h = token.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Volume to market cap ratio
            vol_mcap_ratio = (volume_24h / actual_mcap * 100) if actual_mcap > 0 else 0
            
            # Calculate alpha score (0-100)
            # Component weights:
            # Volume/MCap Ratio: 35 points max (high importance)
            # Price Momentum: 25 points max
            # Buy Ratio: 20 points max
            # Liquidity: 20 points max
            
            vol_score = min(35, vol_mcap_ratio * 0.7)
            momentum_score = min(25, max(0, price_change_24h) * 1.25)
            buy_score = min(20, buy_ratio * 0.2)
            liquidity_score = min(20, liquidity / 5000)
            
            alpha_score = vol_score + momentum_score + buy_score + liquidity_score
            
            # Skip tokens with very low scores
            if alpha_score < 15:
                continue
            
            gem_data = {
                'symbol': symbol,
                'name': name,
                'mcap': actual_mcap,
                'volume_24h': volume_24h,
                'price_change_24h': price_change_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'liquidity': liquidity,
                'buy_ratio': buy_ratio,
                'buy_sell': f"{buys}/{sells}",
                'total_txns': total_txns,
                'chain': token.get('chainId', ''),
                'dex': token.get('dexId', ''),
                'url': token.get('url', ''),
                'alpha_score': alpha_score
            }
            
            alpha_gems.append(gem_data)
            
        except Exception as e:
            print(f"⚠️ Error analyzing token: {e}")
            continue
    
    return sorted(alpha_gems, key=lambda x: x['alpha_score'], reverse=True)

def generate_summary(gems):
    """Generate comprehensive summary report"""
    current_time = datetime.now().strftime("%A, March 6, 2026 — %I:%M %p (Asia/Manila)")
    
    summary_parts = []
    summary_parts.append("🚀 MEMECOIN ALPHA SCANNER - DEXSCREENER")
    summary_parts.append("=" * 60)
    summary_parts.append(f"Scan Time: {current_time}")
    summary_parts.append("Market Cap Focus: $30,000 - $200,000")
    summary_parts.append("Source: DexScreener Trending Tokens API")
    summary_parts.append("")
    
    if not gems:
        summary_parts.append("❌ No promising alpha gems found in the target range")
        summary_parts.append("Market may lack opportunities or API may have issues")
        return "\n".join(summary_parts)
    
    summary_parts.append(f"🔥 TOP ALPHA GEMS DISCOVERED ({len(gems)} total):")
    summary_parts.append("-" * 50)
    
    # Show top 5 gems
    for i, gem in enumerate(gems[:5], 1):
        sentiment = "📈" if gem['price_change_24h'] > 0 else "📉"
        summary_parts.append(f"\n{i}. 🎯 {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        summary_parts.append(f"   • Market Cap: ${gem['mcap']:,.0f}")
        summary_parts.append(f"   • 24h Volume: ${gem['volume_24h']:,.0f}")
        summary_parts.append(f"   {sentiment} 24h Change: {gem['price_change_24h']:+.1f}%")
        summary_parts.append(f"   • Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
        summary_parts.append(f"   • Buy Ratio: {gem['buy_ratio']:.1f}% ({gem['buy_sell']})")
        summary_parts.append(f"   • Liquidity: ${gem['liquidity']:,.0f}")
        summary_parts.append(f"   • Chain: {gem['chain']}")
        summary_parts.append(f"   • Dex: {gem['dex']}")
        summary_parts.append(f"   • Trades: {gem['total_txns']}")
    
    # Market analysis
    summary_parts.append("\n📊 MARKET ANALYSIS:")
    summary_parts.append("-" * 20)
    
    avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
    avg_volume = sum(g['volume_24h'] for g in gems) / len(gems)
    avg_vol_ratio = sum(g['vol_mcap_ratio'] for g in gems) / len(gems)
    avg_buy_ratio = sum(g['buy_ratio'] for g in gems) / len(gems)
    
    summary_parts.append(f"• Total Alpha Candidates: {len(gems)}")
    summary_parts.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
    summary_parts.append(f"• Average Volume: ${avg_volume:,.0f}")
    summary_parts.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
    summary_parts.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
    summary_parts.append(f"• Top Alpha Score: {gems[0]['alpha_score']:.1f}/100")
    
    # Chain distribution
    chains = {}
    for gem in gems:
        chain = gem['chain']
        chains[chain] = chains.get(chain, 0) + 1
    
    if chains:
        chain_summary = ", ".join([f"{k}: {v}" for k, v in chains.items()])
        summary_parts.append(f"• Chain Distribution: {chain_summary}")
    
    # Alpha insights
    summary_parts.append("\n💡 ALPHA INSIGHTS:")
    high_vol_ratio = [g for g in gems if g['vol_mcap_ratio'] > 100]
    strong_buyers = [g for g in gems if g['buy_ratio'] > 60]
    high_liquidity = [g for g in gems if g['liquidity'] > 10000]
    
    summary_parts.append(f"• Tokens with Vol/MCap > 100%: {len(high_vol_ratio)}")
    summary_parts.append(f"• Tokens with Buy Ratio > 60%: {len(strong_buyers)}")
    summary_parts.append(f"• Tokens with Liquidity > $10k: {len(high_liquidity)}")
    
    if gems:
        best_vol_ratio = max(g['vol_mcap_ratio'] for g in gems)
        best_buy_ratio = max(g['buy_ratio'] for g in gems)
        summary_parts.append(f"• Best Vol/MCap: {best_vol_ratio:.1f}%")
        summary_parts.append(f"• Best Buy Ratio: {best_buy_ratio:.1f}%")
    
    # Risk analysis
    summary_parts.append("\n⚠️ RISK ASSESSMENT:")
    summary_parts.append("• HIGH VOLATILITY: Memecoins can swing dramatically")
    summary_parts.append("• LOW LIQUIDITY: Many tokens have limited liquidity")
    summary_parts.append("• HIGH RISK: Only invest what you can afford to lose")
    summary_parts.append("• DYOR: Always do your own research before trading")
    
    return "\n".join(summary_parts)

def main():
    print("🚀 MEMECOIN ALPHA SCANNER")
    print("Scanning DexScreener for sub $30k-$200k mcap gems...")
    
    # Fetch token data
    tokens_data = fetch_dexscreener_tokens()
    
    if not tokens_data:
        print("❌ Failed to fetch token data from DexScreener")
        return "Failed to fetch dex data"
    
    # Analyze for alpha potential
    alpha_gems = analyze_alpha_potential(tokens_data)
    
    # Generate and return summary
    summary = generate_summary(alpha_gems)
    return summary

if __name__ == "__main__":
    result = main()
    print(result)