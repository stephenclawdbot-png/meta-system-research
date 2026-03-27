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
    """Filter tokens in the target market cap range"""
    candidates = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        
        # Filter by market cap
        if min_mcap <= mcap <= max_mcap:
            volume_24h = pair.get('volume', {}).get('h24', 0)
            
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
            
            # Alpha score calculation (0-100)
            alpha_score = 0
            
            # Volume score (max 35 points)
            vol_score = min(35, (volume_24h / 50000) * 35)
            
            # Buy ratio score (max 30 points)
            buy_score = min(30, buy_ratio * 0.3)
            
            # Price momentum score (max 20 points)
            momentum_score = min(20, max(0, price_change) * 0.5)
            
            # Liquidity score (max 15 points)
            liquidity_score = min(15, liquidity / 10000)
            
            alpha_score = vol_score + buy_score + momentum_score + liquidity_score
            
            candidate = {
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'market_cap': mcap,
                'volume_24h': volume_24h,
                'price': pair.get('priceUsd', 0),
                'price_change_24h': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_ratio': buy_ratio,
                'buy_sell_ratio': f"{buys}/{sells}",
                'total_txns': total_txns,
                'url': pair.get('url', ''),
                'chain': pair.get('chainId', ''),
                'dex': pair.get('dexId', ''),
                'pair_address': pair.get('pairAddress', '')
            }
            candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(candidates):
    """Generate the alpha scanner report"""
    current_time = datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')
    
    report = []
    report.append("🚀 DEXSCREENER ALPHA SCANNER - SUB $30K-$200K GEMS")
    report.append("=" * 60)
    report.append(f"Scan Time: {current_time}")
    report.append(f"Market Cap Focus: $30,000 - $200,000")
    report.append(f"Sources: DexScreener Search API")
    report.append("")
    
    if not candidates:
        report.append("❌ No alpha gems found in the target range")
        report.append("Try adjusting filters or check market conditions")
        return "\n".join(report)
    
    report.append(f"💎 TOP ALPHA GEMS DISCOVERED ({len(candidates)} total)")
    report.append("-" * 40)
    
    for i, gem in enumerate(candidates[:20], 1):  # Top 20
        chain_symbol = "🔗" if gem['chain'] != 'ethereum' else "⛓️"
        
        report.append(f"\n{i}. {chain_symbol} {gem['symbol']}")
        report.append(f"   Alpha Score: {gem['alpha_score']:.1f}/100")
        report.append(f"   Market Cap: ${gem['market_cap']:,.0f}")
        report.append(f"   24h Volume: ${gem['volume_24h']:,.0f}")
        report.append(f"   Price: ${float(gem['price']):.6f}")
        report.append(f"   24h Change: {gem['price_change_24h']:+.1f}%")
        report.append(f"   Buy Ratio: {gem['buy_ratio']:.1f}% ({gem['buy_sell_ratio']})")
        report.append(f"   Total Txns: {gem['total_txns']}")
        report.append(f"   Liquidity: ${gem['liquidity']:,.0f}")
        report.append(f"   Chain: {gem['chain']} | DEX: {gem['dex']}")
    
    # Market stats
    report.append("\n📊 MARKET STATISTICS:")
    report.append("-" * 20)
    report.append(f"Total Candidates: {len(candidates)}")
    avg_mcap = sum(gem['market_cap'] for gem in candidates) / len(candidates)
    avg_vol = sum(gem['volume_24h'] for gem in candidates) / len(candidates)
    avg_buy_ratio = sum(gem['buy_ratio'] for gem in candidates) / len(candidates)
    avg_liquidity = sum(gem['liquidity'] for gem in candidates) / len(candidates)
    
    report.append(f"Average MCap: ${avg_mcap:,.0f}")
    report.append(f"Average Volume: ${avg_vol:,.0f}")
    report.append(f"Average Buy Ratio: {avg_buy_ratio:.1f}%")
    report.append(f"Average Liquidity: ${avg_liquidity:,.0f}")
    
    # Chain breakdown
    chains = {}
    for gem in candidates:
        chain = gem['chain']
        chains[chain] = chains.get(chain, 0) + 1
    
    report.append(f"Chain Distribution: {', '.join([f'{k}: {v}' for k, v in chains.items()])}")
    
    # Risk warning
    report.append("\n⚠️ IMPORTANT DISCLAIMER:")
    report.append("• This is NOT financial advice")
    report.append("• Memecoins are extremely high risk")
    report.append("• Always do your own research (DYOR)")
    report.append("• Only risk what you can afford to lose")
    
    return "\n".join(report)

def main():
    print("🔍 Scanning DexScreener for memecoin gems...")
    
    # Fetch all memecoins
    pairs = fetch_memecoins()
    print(f"Found {len(pairs)} total token pairs")
    
    # Filter for alpha gems
    gems = filter_alpha_gems(pairs)
    
    # Generate report
    report = generate_report(gems)
    print(report)
    
    return report

if __name__ == "__main__":
    result = main()