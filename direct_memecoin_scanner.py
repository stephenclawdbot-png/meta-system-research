#!/usr/bin/env python3
"""
Direct Memecoin Scanner - Using DexScreener API
Scans for tokens in $30k-$200k market cap range
"""

import requests
import json
from datetime import datetime

def fetch_dexscreener_tokens():
    """Fetch tokens from DexScreener"""
    try:
        # Fetch trending/new tokens on Solana
        url = "https://api.dexscreener.com/latest/dex/search?q=sol"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'pairs' in data:
                return data['pairs']
            else:
                print("No 'pairs' found in response")
                return []
        else:
            print(f"API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def filter_memecoin_opportunities(tokens, min_mcap=30000, max_mcap=200000):
    """Filter tokens by market cap range and calculate alpha metrics"""
    opportunities = []
    
    if not tokens:
        return opportunities
        
    for token in tokens:
        try:
            # Get market cap - handle different field names
            market_cap = token.get('marketCap', 0)
            
            # Filter by market cap range
            if min_mcap <= market_cap <= max_mcap:
                # Extract token details
                base_token = token.get('baseToken', {})
                quote_token = token.get('quoteToken', {})
                
                symbol = base_token.get('symbol', 'Unknown')
                name = base_token.get('name', 'Unknown')
                
                # Skip main SOL pairs
                if symbol == 'SOL' or 'solana' in name.lower():
                    continue
                    
                # Get volume and other metrics
                volume_24h = token.get('volume', {}).get('h24', 0)
                price_usd = token.get('priceUsd', 0)
                price_change_24h = token.get('priceChange', {}).get('h24', 0)
                liquidity = token.get('liquidity', {}).get('usd', 0)
                
                # Get transaction data
                txns = token.get('txns', {}).get('h24', {})
                buys = txns.get('buys', 0)
                sells = txns.get('sells', 0)
                total_txns = buys + sells
                buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
                
                # Calculate alpha score
                vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
                
                # Simple alpha scoring
                alpha_score = min(100, vol_mcap_ratio *2531314159)  # Cap at 100
                
                opportunity = {
                    'symbol': symbol,
                    'name': name,
                    'market_cap': market_cap,
                    'volume_24h': volume_24h,
                    'price_usd': price_usd,
                    'price_change_24h': price_change_24h,
                    'liquidity': liquidity,
                    'buy_ratio': buy_ratio,
                    'txns': f"{buys}/{sells}",
                    'vol_mcap_ratio': vol_mcap_ratio,
                    'alpha_score': alpha_score,
                    'url': token.get('url', '')
                }
                
                opportunities.append(opportunity)
                
        except Exception as e:
            print(f"Error processing token {token.get('baseToken', {}).get('symbol', 'Unknown')}: {e}")
            continue
    
    # Sort by alpha score
    opportunities.sort(key=lambda x: x['alpha_score'], reverse=True)
    return opportunities

def main():
    print("🎯 MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Target Market Cap: $30,000 - $200,000")
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print()
    
    print("Fetching DexScreener data...")
    tokens = fetch_dexscreener_tokens()
    
    if not tokens:
        print("❌ No tokens found from DexScreener API")
        return
        
    print(f"✅ Found {len(tokens)} total tokens")
    
    # Filter for memecoin opportunities
    opportunities = filter_memecoin_opportunities(tokens)
    
    print(f"🎯 Found {len(opportunities)} alpha opportunities")
    print("-" * 60)
    
    if not opportunities:
        print("No memecoins found in the 30k-200k market cap range.")
        print("Market may be quiet or tokens may have moved out of this range.")
        return
    
    # Display top opportunities
    for i, opp in enumerate(opportunities[:10], 1):
        print(f"\n{i}. 💎 {opp['symbol']} - Alpha Score: {opp['alpha_score']:.1f}/100")
        print(f"   📛 Name: {opp['name']}")
        print(f"   💰 Market Cap: ${opp['market_cap']:,}")
        print(f"   📈 24h Volume: ${opp['volume_24h']:,}")
        print(f"   🌊 Vol/MCap Ratio: {opp['vol_mcap_ratio']:.2f}%")
        print(f"   💵 Price: ${opp['price_usd']:.8f}")
        print(f"   🔺 24h Change: {opp['price_change_24h']:.2f}%")
        print(f"   💧 Liquidity: ${opp['liquidity']:,}")
        print(f"   📈 Buy Ratio: {opp['buy_ratio']:.1f}%")
        print(f"   🔄 Transactions: {opp['txns']}")
        print(f"   🔗 DexScreener: {opp['url']}")
    
    print("\n📊 SUMMARY")
    print("-" * 30)
    print(f"Total Opportunities: {len(opportunities)}")
    if opportunities:
        avg_mcap = sum(opp['market_cap'] for opp in opportunities) / len(opportunities)
        avg_vol_ratio = sum(opp['vol_mcap_ratio'] for opp in opportunities) / len(opportunities)
        avg_buy_ratio = sum(opp['buy_ratio'] for opp in opportunities) / len(opportunities)
        print(f"Average Market Cap: ${avg_mcap:,.0f}")
        print(f"Average Vol/MCap Ratio: {avg_vol_ratio:.2f}%")
        print(f"Average Buy Ratio: {avg_buy_ratio:.1f}%")
        print(f"Top Alpha Score: {max(opp['alpha_score'] for opp in opportunities):.1f}")
    
    print("\n⚠️ HIGH RISK INVESTMENT - DO YOUR OWN RESEARCH")

if __name__ == "__main__":
    main()