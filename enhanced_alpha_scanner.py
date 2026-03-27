#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins_with_filters():
    """Fetch memecoins with stricter filtering"""
    searches = ["dog", "cat", "meme", "ai", "pepe", "wif", "bonk", "elon", "doge", "shib", "floki"]
    all_tokens = []
    
    for search_term in searches:
        url = f"https://api.dexscreener.com/latest/dex/search?q={search_term}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            filtered_tokens = []
            
            if not data or 'pairs' not in data:
                continue
            
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                volume_24h = token.get('volume', {}).get('h24', 0)
                price_change = token.get('priceChange', {}).get('h24', 0)
                
                # STRICTER FILTERS:
                # 30k-200k mcap, min $5k volume, positive momentum preferred
                if (30000 <= mcap <= 200000 and 
                    volume_24h >= 5000 and 
                    mcap > 0):
                    
                    # Additional metrics
                    dex_id = token.get('dexId', '')
                    chain_id = token.get('chainId', '')
                    
                    # Skip unreliable chains/dexes
                    unreliable_chains = ['ethereum', 'bitcoin']  # High gas = less memecoin activity
                    if chain_id.lower() in unreliable_chains:
                        continue
                    
                    token_info = {
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': volume_24h,
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': price_change,
                        'txns_24h': token.get('txns', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': dex_id,
                        'chain': chain_id
                    }
                    filtered_tokens.append(token_info)
            
            all_tokens.extend(filtered_tokens)
            
        except Exception as e:
            print(f"Error searching for '{search_term}': {e}")
            continue
    
    return all_tokens

def calculate_enhanced_alpha_score(token):
    """Enhanced alpha scoring with more factors"""
    # Base components
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Chain/Dex bonus points
    dex_bonus = 0
    chain_bonus = 0
    
    # Solana gets bonus (fast, cheap, memecoin friendly)
    if 'solana' in token['chain'].lower():
        chain_bonus += 10
    
    # Preferred Dexes
    good_dexes = ['raydium', 'orca', 'jupiter']
    if any(dex in token['dex'].lower() for dex in good_dexes):
        dex_bonus += 5
    
    # Volume tier bonuses
    volume_bonus = min(15, token['volume_24h'] / 10000)
    
    # Momentum bonus
    momentum_bonus = 0
    if momentum > 10:
        momentum_bonus = min(10, momentum / 5)
    
    # Calculate composite score
    alpha_score = min(
        100,
        (vol_mcap_ratio * 0.4) +           # Volume/MCap ratio (40%)
        (momentum * 0.3) +                 # Price momentum (30%)
        volume_bonus +                     # Absolute volume bonus (max 15%)
        chain_bonus +                      # Chain bonus (max 10%)
        dex_bonus +                        # Dex bonus (max 5%)
        momentum_bonus                     # Momentum bonus (max 10%)
    )
    
    return round(alpha_score, 1)

def analyze_potential(token):
    """Provide investment potential analysis"""
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    potential_signals = []
    
    # High volume relative to market cap
    if vol_mcap_ratio > 50:
        potential_signals.append("🚀 High vol/mcap ratio (unusual interest)")
    elif vol_mcap_ratio > 20:
        potential_signals.append("📈 Good vol/mcap ratio (healthy activity)")
    
    # Positive momentum
    if token['price_change_24h'] > 20:
        potential_signals.append("🔥 Strong momentum")
    elif token['price_change_24h'] > 0:
        potential_signals.append("📊 Positive momentum")
    
    # Chain advantages
    if 'solana' in token['chain'].lower():
        potential_signals.append("🌐 Solana (fast/low fees)")
    elif 'bsc' in token['chain'].lower():
        potential_signals.append("💸 Binance Smart Chain (accessible)")
    
    # Volume ranking
    if token['volume_24h'] > 10000:
        potential_signals.append("💰 Healthy volume")
    elif token['volume_24h'] > 5000:
        potential_signals.append("💼 Decent volume")
    
    return potential_signals

def main():
    print("💎 ENHANCED MEMECOIN ALPHA SCANNER - STRATEGIC FINDINGS")
    print("=" * 70)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap | Min Volume: $5k")
    print("=" * 70)
    
    # Fetch tokens with filters
    tokens = fetch_memecoins_with_filters()
    
    if not tokens:
        print("\n❌ No high-quality memecoins found after applying filters")
        print("This indicates:")
        print("• Low memecoin activity in target range")
        print("• Increased market maturity (fewer new moonshots)")
        print("• Possible market consolidation")
        return
    
    # Enhanced scoring and sorting
    scored_tokens = []
    for token in tokens:
        alpha_score = calculate_enhanced_alpha_score(token)
        token['alpha_score'] = alpha_score
        token['vol_mcap_ratio'] = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        scored_tokens.append(token)
    
    # Sort by alpha score
    scored_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("\n🔥 TOP ALPHA MEMECOINS (Filtered Results):")
    print("-" * 60)
    
    for i, token in enumerate(scored_tokens[:15], 1):
        potential_signals = analyze_potential(token)
        
        print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   💰 MCap: ${token['mcap']:,.0f} | Vol 24h: ${token['volume_24h']:,.0f}")
        print(f"   📈 Price Change: {token['price_change_24h']:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {token['vol_mcap_ratio']:.1f}%")
        print(f"   ⛓️ Chain: {token['chain']} | Dex: {token['dex']}")
        
        if potential_signals:
            print("   ✅ Potential Signals:")
            for signal in potential_signals:
                print(f"      • {signal}")
        
        print(f"   🔗 {token['url']}")
        print()
    
    # Strategic Analysis
    print("📊 MARKET INSIGHTS:")
    print("-" * 30)
    
    # Chain distribution
    chain_distribution = {}
    for token in scored_tokens:
        chain = token['chain']
        chain_distribution[chain] = chain_distribution.get(chain, 0) + 1
    
    print(f"• Total Quality Gems Found: {len(scored_tokens)}")
    print(f"• Chain Distribution: {dict(sorted(chain_distribution.items(), key=lambda x: x[1], reverse=True))}")
    print(f"• Avg Alpha Score: {sum(t['alpha_score'] for t in scored_tokens)/len(scored_tokens):.1f}/100")
    print(f"• Avg Vol/MCap Ratio: {sum(t['vol_mcap_ratio'] for t in scored_tokens)/len(scored_tokens):.1f}%")
    print(f"• Avg Volume: ${sum(t['volume_24h'] for t in scored_tokens)/len(scored_tokens):,.0f}")
    
    # Market sentiment
    positive_count = sum(1 for t in scored_tokens if t['price_change_24h'] > 0)
    print(f"• Market Sentiment: {positive_count}/{len(scored_tokens)} tokens positive ({positive_count/len(scored_tokens)*100:.0f}%)")
    
    print("\n💡 INVESTMENT CONSIDERATIONS:")
    print("• Focus on tokens with Vol/MCap >20% for momentum plays")
    print("• Solana tokens offer better liquidity and faster trading")
    print("• Monitor transaction counts and social engagement")
    print("• Consider entry timing during consolidation phases")
    
    print("\n⚠️ DISCLAIMER: Memecoins = extreme volatility. DYOR!")

if __name__ == "__main__":
    main()