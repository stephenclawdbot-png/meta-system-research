#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Search for memecoins on DexScreener"""
    urls = [
        'https://api.dexscreener.com/latest/dex/search?q=dog',  # Dog-themed memes
        'https://api.dexscreener.com/latest/dex/search?q=cat',   # Cat-themed memes  
        'https://api.dexscreener.com/latest/dex/search?q=frog',  # Frog memes
        'https://api.dexscreener.com/latest/dex/search?q=coin', # Coin-themed
        'https://api.dexscreener.com/latest/dex/search?q=inu',  # Inu memes
        'https://api.dexscreener.com/latest/dex/search?q=elon', # Elon-themed
        'https://api.dexscreener.com/latest/dex/search?q=sol',   # Solana memes
        'https://api.dexscreener.com/latest/dex/search?q=meme',  # General memes
        'https://api.dexscreener.com/latest/dex/search?q=pepe',  # Pepe
        'https://api.dexscreener.com/latest/dex/search?q=bonk',  # Bonk
        'https://api.dexscreener.com/latest/dex/search?q=doge',  # Doge
    ]
    
    all_pairs = []
    
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('pairs'):
                    all_pairs.extend(data['pairs'])
                    
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    # Remove duplicates based on pairAddress
    seen = set()
    unique_pairs = []
    for pair in all_pairs:
        pair_addr = pair.get('pairAddress')
        if pair_addr and pair_addr not in seen:
            seen.add(pair_addr)
            unique_pairs.append(pair)
    
    return unique_pairs

def filter_alpha_gems(pairs, min_mcap=30000, max_mcap=200000):
    """Filter tokens in the target market cap range with better filtering"""
    candidates = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        total_txns = pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0)
        
        # Enhanced filtering criteria
        if not (min_mcap <= mcap <= max_mcap):
            continue
            
        # Skip low activity tokens
        if volume_24h < 100 or total_txns < 10:
            continue
            
        # Get transaction data
        txns_24h = pair.get('txns', {}).get('h24', {})
        buys = txns_24h.get('buys', 0)
        sells = txns_24h.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        
        # Price change
        price_change = pair.get('priceChange', {}).get('h24', 0)
        
        # Liquidity
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        
        # Enhanced alpha score calculation (0-100)
        alpha_score = 0
        
        # Volume score (max 30 points)
        vol_score = min(30, (volume_24h / 50000) * 30)
        
        # Buy ratio score (max 25 points)
        buy_score = min(25, buy_ratio * 0.25)
        
        # Positive price momentum score (max 20 points)
        momentum_score = min(20, max(0, price_change) * 0.5)
        
        # Liquidity score (max 15 points) - prioritize reasonable liquidity
        liquidity_score = min(15, (liquidity / 10000) * 0.6)
        
        # Transaction velocity score (max 10 points)
        txn_score = min(10, (total_txns / 500) * 10)
        
        alpha_score = vol_score + buy_score + momentum_score + liquidity_score + txn_score
        
        candidate = {
            'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'market_cap': mcap,
            'volume_24h': volume_24h,
            'price': float(pair.get('priceUsd', 0)),
            'price_change_24h': price_change,
            'liquidity': liquidity,
            'alpha_score': alpha_score,
            'buy_ratio': buy_ratio,
            'buy_count': buys,
            'sell_count': sells,
            'total_txns': total_txns,
            'url': pair.get('url', ''),
            'chain': pair.get('chainId', ''),
            'dex': pair.get('dexId', ''),
            'pair_address': pair.get('pairAddress', ''),
            'age': (datetime.now().timestamp() * 1000 - pair.get('pairCreatedAt', 0)) / (1000 * 3600) if pair.get('pairCreatedAt') else None
        }
        candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_alpha_report(candidates):
    """Generate a refined alpha scanner report"""
    current_time = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🎯 DEXSCREENER ALPHA SCANNER - SUB 30K-200K MCAP GEMS")
    report.append("=" * 65)
    report.append(f"Scan Time: {current_time}")
    report.append(f"Market Cap Focus: $30,000 - $200,000")
    report.append(f"Minimum Filters: $100 daily volume, 10+ transactions")
    report.append(f"Sources: DexScreener Search API")
    report.append("")
    
    if not candidates:
        report.append("❌ No qualifying alpha gems found in the target range")
        report.append("Market may be quiet - consider adjusting criteria")
        return "\n".join(report)
    
    # Filter top candidates (alpha score > 30)
    strong_candidates = [c for c in candidates if c['alpha_score'] > 30]
    
    report.append(f"💎 TOP QUALIFIED ALPHA GEMS ({len(strong_candidates)} of {len(candidates)} pass filters)")
    report.append("-" * 50)
    
    for i, gem in enumerate(strong_candidates[:10], 1):  # Top 10 only
        chain_symbol = "🔗" if gem['chain'] != 'ethereum' else "⛓️"
        age_info = f", Age: {gem['age']:.1f}h" if gem['age'] else ""
        
        report.append(f"\n{i}. {chain_symbol} {gem['symbol']}")
        report.append(f"   Alpha Score: {gem['alpha_score']:.1f}/100")
        report.append(f"   Market Cap: ${gem['market_cap']:,.0f}")
        report.append(f"   24h Volume: ${gem['volume_24h']:,.0f}")
        report.append(f"   Price: ${gem['price']:.6f}")
        report.append(f"   24h Change: {gem['price_change_24h']:+.1f}%")
        report.append(f"   Buy Ratio: {gem['buy_ratio']:.1f}% ({gem['buy_count']}/{gem['sell_count']})")
        report.append(f"   Total Txns: {gem['total_txns']}")
        report.append(f"   Liquidity: ${gem['liquidity']:,.0f}")
        report.append(f"   Chain: {gem['chain']} | DEX: {gem['dex']}{age_info}")
    
    # Market insights
    report.append("\n📊 MARKET INSIGHTS:")
    report.append("-" * 20)
    report.append(f"Total Candidates Found: {len(candidates)}")
    report.append(f"High-Quality Candidates (Score >30): {len(strong_candidates)}")
    
    if strong_candidates:
        avg_mcap = sum(gem['market_cap'] for gem in strong_candidates) / len(strong_candidates)
        avg_vol = sum(gem['volume_24h'] for gem in strong_candidates) / len(strong_candidates)
        avg_buy_ratio = sum(gem['buy_ratio'] for gem in strong_candidates) / len(strong_candidates)
        avg_liquidity = sum(gem['liquidity'] for gem in strong_candidates) / len(strong_candidates)
        
        report.append(f"Average Qualified MCap: ${avg_mcap:,.0f}")
        report.append(f"Average Qualified Volume: ${avg_vol:,.0f}")
        report.append(f"Average Qualified Buy Ratio: {avg_buy_ratio:.1f}%")
        report.append(f"Average Qualified Liquidity: ${avg_liquidity:,.0f}")
        
        # Best performer
        best_gem = max(strong_candidates, key=lambda x: x['alpha_score'])
        report.append(f"\n🏆 TOP PERFORMER:")
        report.append(f"• {best_gem['symbol']} - Alpha Score: {best_gem['alpha_score']:.1f}")
        report.append(f"• Market Cap: ${best_gem['market_cap']:,}")
        report.append(f"• 24h Volume: ${best_gem['volume_24h']:,}")
        report.append(f"• Buy Ratio: {best_gem['buy_ratio']:.1f}%")
    
    # Chain breakdown for qualified candidates
    chains = {}
    for gem in strong_candidates:
        chain = gem['chain']
        chains[chain] = chains.get(chain, 0) + 1
    
    if chains:
        report.append(f"Chain Distribution: {', '.join([f'{k}: {v}' for k, v in chains.items()])}")
    
    # Risk assessment
    report.append("\n⚠️ RISK ASSESSMENT:")
    report.append("• High volatility expected - rapid price changes possible")
    report.append("• Low market cap tokens = higher risk/reward ratio")
    report.append("• Always DYOR and consider position sizing")
    report.append("• Monitor volume and buy ratio for momentum shifts")
    
    # Disclaimer
    report.append("\n❗ DISCLAIMER:")
    report.append("• Alpha scanner results are for informational purposes only")
    report.append("• NOT financial advice - always perform your own due diligence")
    report.append("• Cryptocurrency investments carry significant risk")
    
    return "\n".join(report)

def main():
    print("🔍 Scanning DexScreener for memecoin gems...")
    
    # Fetch all memecoins
    pairs = fetch_memecoins()
    print(f"Found {len(pairs)} total token pairs")
    
    # Filter for alpha gems
    gems = filter_alpha_gems(pairs)
    print(f"Found {len(gems)} tokens in target range with activity")
    
    # Generate report
    report = generate_alpha_report(gems)
    print(report)
    
    return report

if __name__ == "__main__":
    result = main()