#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_pairs():
    """Fetch pairs using different DexScreener endpoints"""
    print("📡 Fetching DexScreener data...")
    
    endpoints = [
        "https://api.dexscreener.com/latest/dex",
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=meme",
        "https://api.dexscreener.com/latest/dex/search?q=coin"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    for endpoint in endpoints:
        try:
            print(f"Trying: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data and data['pairs']:
                    print(f"✅ Found {len(data['pairs'])} pairs from {endpoint}")
                    return data['pairs']
                else:
                    print(f"❌ No pairs in {endpoint}")
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    return []

def filter_alpha_gems(pairs):
    """Filter pairs in the 30k-200k mcap range"""
    alpha_gems = []
    
    for pair in pairs:
        try:
            # Get market cap (try fdv first, then marketCap)
            market_cap = pair.get('fdv', pair.get('marketCap', 0))
            
            # Filter by market cap range
            if market_cap < 30000 or market_cap > 200000:
                continue
                
            # Extract basic info
            base_token = pair.get('baseToken', {})
            symbol = base_token.get('symbol', '').upper()
            name = base_token.get('name', '')
            
            # Skip wrapped/stables
            wrapped_keywords = ['wrapped', 'wbtc', 'weth', 'wsol', 'usdc', 'usdt']
            if any(keyword in name.lower() for keyword in wrapped_keywords):
                continue
            
            # Get volume and price data
            volume_24h = pair.get('volume', {}).get('h24', 0)
            price_change_24h = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            
            # Transaction data
            txns_24h = pair.get('txns', {}).get('h24', {})
            buys = txns_24h.get('buys', 0)
            sells = txns_24h.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
            
            # Volume to market cap ratio
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Alpha score calculation
            vol_score = min(35, vol_mcap_ratio * 0.5)
            momentum_score = min(25, max(0, price_change_24h) * 1.25)
            buy_score = min(20, buy_ratio * 0.2)
            liquidity_score = min(20, liquidity / 5000)
            
            alpha_score = vol_score + momentum_score + buy_score + liquidity_score
            
            # Filter out very low scores
            if alpha_score < 10:
                continue
            
            gem = {
                'symbol': symbol,
                'name': name,
                'mcap': market_cap,
                'volume_24h': volume_24h,
                'price_change_24h': price_change_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'liquidity': liquidity,
                'buy_ratio': buy_ratio,
                'buy_sell': f"{buys}/{sells}",
                'total_txns': total_txns,
                'chain': pair.get('chainId', ''),
                'dex': pair.get('dexId', ''),
                'url': pair.get('url', ''),
                'alpha_score': alpha_score
            }
            
            alpha_gems.append(gem)
            
        except Exception as e:
            print(f"⚠️ Error processing pair: {e}")
            continue
    
    return sorted(alpha_gems, key=lambda x: x['alpha_score'], reverse=True)

def generate_report(gems):
    """Generate the final report"""
    scan_time = datetime.now().strftime("%A, March 6, 2026 — %I:%M %p (Asia/Manila)")
    
    report = []
    report.append("🚀 DEXSCREENER MEMECOIN ALPHA SCANNER")
    report.append("=" * 60)
    report.append(f"Scan Time: {scan_time}")
    report.append("Target Range: $30,000 - $200,000 Market Cap")
    report.append("Source: DexScreener API Search Endpoints")
    report.append("")
    
    if not gems:
        report.append("❌ No alpha gems found in the target range")
        report.append("✅ API Status: Live but returning limited/no data")
        report.append("📊 Market may be quiet or API structure changed")
        return "\n".join(report)
    
    report.append(f"💎 TOP ALPHA GEMS FOUND ({len(gems)} total):")
    report.append("-" * 50)
    
    # Show top gems
    for i, gem in enumerate(gems[:8], 1):
        sentiment = "📈" if gem['price_change_24h'] > 0 else "📉"
        report.append(f"\n{i}. 🔥 {gem['symbol']} - Alpha: {gem['alpha_score']:.1f}/100")
        report.append(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}")
        report.append(f"   {sentiment} Change: {gem['price_change_24h']:+.1f}%") 
        report.append(f"   🔥 Vol/MCap: {gem['vol_mcap_ratio']:.1f}%")
        report.append(f"   🤝 Buy Ratio: {gem['buy_ratio']:.1f}% ({gem['buy_sell']})")
        report.append(f"   💧 Liquidity: ${gem['liquidity']:,.0f}")
        report.append(f"   🔗 Chain: {gem['chain']} | Dex: {gem['dex']}")
        report.append(f"   🔗 {gem['url']}")
    
    # Market analysis
    report.append("\n📊 MARKET OVERVIEW:")
    report.append("-" * 20)
    
    avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
    avg_volume = sum(g['volume_24h'] for g in gems) / len(gems)
    avg_vol_ratio = sum(g['vol_mcap_ratio'] for g in gems) / len(gems)
    avg_buy_ratio = sum(g['buy_ratio'] for g in gems) / len(gems)
    
    report.append(f"• Alpha Candidates: {len(gems)}")
    report.append(f"• Avg MCap: ${avg_mcap:,.0f}") 
    report.append(f"• Avg Volume: ${avg_volume:,.0f}")
    report.append(f"• Avg Vol/MCap: {avg_vol_ratio:.1f}%")
    report.append(f"• Avg Buy Ratio: {avg_buy_ratio:.1f}%")
    report.append(f"• Top Alpha Score: {gems[0]['alpha_score']:.1f}/100")
    
    # Risk assessment
    report.append("\n⚠️ RISK NOTICE:")
    report.append("• HIGH VOLATILITY: Memecoins are extremely speculative")
    report.append("• LOW LIQUIDITY: Many have limited trading pools")
    report.append("• DYOR: Always research before investing")
    report.append("• NFA: This is informational only")
    
    return "\n".join(report)

def main():
    print("🔍 DexScreener Alpha Scanner")
    print("Scanning for sub $30k-$200k mcap memecoins...\n")
    
    # Fetch pairs
    pairs = fetch_dexscreener_pairs()
    
    if not pairs:
        print("❌ No pairs found from DexScreener APIs")
        summary = "DexScreener API returned no data - market may be quiet or API structure changed"
    else:
        print(f"✅ Found {len(pairs)} total pairs")
        gems = filter_alpha_gems(pairs)
        summary = generate_report(gems)
    
    return summary

if __name__ == "__main__":
    result = main()
    print("\n" + result)