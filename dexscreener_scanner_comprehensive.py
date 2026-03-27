#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

def fetch_trending_tokens():
    """Fetch trending tokens from DexScreener trending endpoint"""
    url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching trending tokens: {e}")
        return None

def fetch_new_tokens():
    """Fetch new tokens from DexScreener new tokens endpoint"""
    url = "https://api.dexscreener.com/latest/dex/tokens/new"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"New tokens API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching new tokens: {e}")
        return None

def filter_alpha_candidates(data, min_mcap=30000, max_mcap=200000):
    candidates = []
    
    if data is None or not isinstance(data, dict) or 'pairs' not in data or data['pairs'] is None:
        print(f"Invalid data structure or no pairs: {data}")
        return candidates
    
    for token in data['pairs']:
        market_cap = token.get('marketCap', 0)
        
        # Filter by market cap range
        if min_mcap <= market_cap <= max_mcap:
            base_token = token.get('baseToken', {})
            
            # Skip tokens with very low age
            created_at = token.get('pairCreatedAt')
            if created_at:
                # Assuming Unix timestamp
                age_hours = (time.time() - created_at/1000) / 3600
                if age_hours < 1:  # Skip tokens younger than 1 hour
                    continue
            
            # Calculate alpha metrics
            volume_24h = token.get('volume', {}).get('h24', 0)
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Calculate buy ratio
            txns_24h = token.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Price changes
            price_change_24h = token.get('priceChange', {}).get('h24', 0)
            
            # Liquidity
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            # Calculate composite alpha score (0-100)
            alpha_score = 0
            
            # Volume/MCap ratio component (max 40 points)
            vol_score = min(40, vol_mcap_ratio * 0.4)
            
            # Buy ratio component (max 30 points)
            buy_score = min(30, buy_ratio * 0.3)
            
            # Price momentum component (max 20 points)
            momentum_score = min(20, max(0, price_change_24h) * 0.5)
            
            # Liquidity component (max 10 points)
            liquidity_score = min(10, liquidity / 10000)
            
            alpha_score = vol_score + buy_score + momentum_score + liquidity_score
            
            candidate = {
                'symbol': base_token.get('symbol', 'Unknown'),
                'name': base_token.get('name', 'Unknown'),
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'price_usd': token.get('priceUsd', 0),
                'price_change_24h': price_change_24h,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_ratio': buy_ratio,
                'buy_sell_ratio': f"{buys}/{sells}",
                'pair_address': token.get('pairAddress', ''),
                'url': token.get('url', ''),
                'chain': token.get('chainId', ''),
                'age_hours': age_hours if created_at else None
            }
            candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(candidates):
    current_time = datetime.now().strftime('%A, March 4, 2026 — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🧠 DEXSCREENER ALPHA SCANNER REPORT - SUB 30K-200K MCAP")
    report.append("=" * 65)
    report.append(f"Scan Time: {current_time}")
    report.append("Market Cap Focus: $30,000 - $200,000")
    report.append("Sources: DexScreener Trending/New Tokens API")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Market may lack promising opportunities currently")
        return "\n".join(report)
    
    report.append(f"🔥 TOP ALPHA GEMS DISCOVERED ({len(candidates)} total):")
    
    for i, candidate in enumerate(candidates[:15], 1):  # Top 15
        chain_symbol = "🔗" if candidate['chain'] != 'ethereum' else "⛓️"
        age_info = f", Age: {candidate['age_hours']:.1f}h" if candidate['age_hours'] else ""
        
        report.append(f"\n{i}. {chain_symbol} {candidate['symbol']} - Alpha Score: {candidate['alpha_score']:.1f}/100")
        report.append(f"   • Market Cap: ${candidate['market_cap']:,.0f}")
        report.append(f"   • 24h Volume: ${candidate['volume_24h']:,.0f}")
        report.append(f"   • Vol/MCap Ratio: {candidate['vol_mcap_ratio']:.1f}%")
        report.append(f"   • Price Change: {candidate['price_change_24h']:+.1f}%")
        report.append(f"   • Liquidity: ${candidate['liquidity']:,.0f}")
        report.append(f"   • Buy Ratio: {candidate['buy_ratio']:.1f}%")
        report.append(f"   • Chain: {candidate['chain']}{age_info}")
    
    # Market analysis
    report.append("\n📊 MARKET ANALYSIS:")
    avg_vol_ratio = sum(c['vol_mcap_ratio'] for c in candidates) / len(candidates)
    avg_buy_ratio = sum(c['buy_ratio'] for c in candidates) / len(candidates)
    avg_mcap = sum(c['market_cap'] for c in candidates) / len(candidates)
    avg_liquidity = sum(c['liquidity'] for c in candidates) / len(candidates)
    
    report.append(f"• Total candidates: {len(candidates)} tokens")
    report.append(f"• Average Vol/MCap Ratio: {avg_vol_ratio:.1f}%") 
    report.append(f"• Average Buy Ratio: {avg_buy_ratio:.1f}%")
    report.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
    report.append(f"• Average Liquidity: ${avg_liquidity:,.0f}")
    report.append(f"• Top Alpha Score: {max(c['alpha_score'] for c in candidates):.1f}")
    
    # Chain distribution
    chains = {}
    for c in candidates:
        chain = c['chain']
        chains[chain] = chains.get(chain, 0) + 1
    
    if chains:
        report.append("• Chain Distribution: " + ", ".join([f"{k}: {v}" for k, v in chains.items()]))
    
    # Alpha insights
    report.append("\n💡 ALPHA INSIGHTS:")
    high_volume_candidates = [c for c in candidates if c['vol_mcap_ratio'] > 100]
    strong_buy_ratio = [c for c in candidates if c['buy_ratio'] > 60]
    
    report.append(f"• Tokens with Vol/MCap > 100%: {len(high_volume_candidates)}")
    report.append(f"• Tokens with Buy Ratio > 60%: {len(strong_buy_ratio)}")
    
    if high_volume_candidates:
        best_volume = max(c['vol_mcap_ratio'] for c in high_volume_candidates)
        report.append(f"• Highest Volume Ratio: {best_volume:.0f}%")
    
    # Risk assessment
    report.append("\n⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    report.append("• Memecoins are extremely volatile - DYOR required")
    report.append("• Only invest what you can afford to lose")
    report.append("• Monitor key metrics: volume, buy ratio, liquidity")
    
    return "\n".join(report)

def main():
    print("🔍 Scanning DexScreener for trending/new memecoins...")
    
    all_candidates = []
    
    # Get trending tokens
    print("Fetching trending tokens...")
    trending_data = fetch_trending_tokens()
    print(f"Trending data type: {type(trending_data)}")
    print(f"Trending data: {trending_data}")
    if trending_data and trending_data != 'null':
        trending_candidates = filter_alpha_candidates(trending_data)
        all_candidates.extend(trending_candidates)
    else:
        print("No trending data received or data is null")
    
    # Get new tokens
    print("Fetching new tokens...")
    new_data = fetch_new_tokens()
    print(f"New data type: {type(new_data)}")
    print(f"New data: {new_data}")
    if new_data and new_data != 'null':
        new_candidates = filter_alpha_candidates(new_data)
        all_candidates.extend(new_candidates)
    else:
        print("No new data received or data is null")
    
    # Remove duplicates
    unique_candidates = {}
    for candidate in all_candidates:
        key = candidate['pair_address']
        if key not in unique_candidates or candidate['alpha_score'] > unique_candidates[key]['alpha_score']:
            unique_candidates[key] = candidate
    
    final_candidates = list(unique_candidates.values())
    final_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report = generate_report(final_candidates)
    return report

if __name__ == "__main__":
    result = main()
    print(result)