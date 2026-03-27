#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import time

def fetch_solana_memecoins():
    """Fetch specifically Solana-based memecoins from DexScreener"""
    try:
        # Search for Solana memecoins specifically
        memecoin_queries = ["bonk", "dogwifhat", "wif", "popcat", "michi", "wen", "jeo", "myro", "whales", "pump"]
        
        all_pairs = []
        
        # Loop through common memecoin keywords
        for query in memecoin_queries:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data:
                    # Filter for Solana only
                    solana_pairs = [p for p in data['pairs'] if p.get('chainId') == 'solana']
                    all_pairs.extend(solana_pairs)
                    
            time.sleep(0.5)  # Rate limiting
            
        # Also get trending Solana pairs
        url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'pairs' in data:
                solana_pairs = [p for p in data['pairs'] if p.get('chainId') == 'solana']
                all_pairs.extend(solana_pairs)
                
        return {'pairs': all_pairs}
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def analyze_memecoins(data):
    """Analyze Solana memecoins in 30k-200k mcap range"""
    
    if not data or 'pairs' not in data:
        return []
    
    pairs = data['pairs']
    filtered_gems = []
    
    # Remove duplicates by pair address
    unique_pairs = {}
    for pair in pairs:
        addr = pair.get('pairAddress', '')
        if addr:
            unique_pairs[addr] = pair
    
    for pair in unique_pairs.values():
        # Get market cap (use fdv or marketCap fields)
        mcap = pair.get('fdv', pair.get('marketCap', 0))
        volume_24h = pair.get('volume', {}).get('h24', 0)
        
        # Filter for 30k-200k mcap range
        if mcap and 30000 <= mcap <= 200000 and volume_24h >= 100:
            # Calculate alpha score
            txns = pair.get('txns', {}).get('h24', {'buys': 0, 'sells': 0})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Advanced alpha scoring
            alpha_score = 0
            
            # Volume/Price momentum (35 points)
            vol_mcap_ratio = (volume_24h / mcap) * 100
            if vol_mcap_ratio > 10: alpha_score += 15
            if vol_mcap_ratio > 25: alpha_score += 10
            if vol_mcap_ratio > 50: alpha_score += 10
            
            # Buy pressure (20 points)
            if buy_ratio > 0.5: alpha_score += 10
            if buy_ratio > 0.6: alpha_score += 7
            if buy_ratio > 0.7: alpha_score += 3
            
            # Transaction velocity (15 points)
            if total_txns > 50: alpha_score += 5
            if total_txns > 100: alpha_score += 5
            if total_txns > 200: alpha_score += 5
            
            # Liquidity (15 points) 
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            if liquidity > 1000: alpha_score += 5
            if liquidity > 5000: alpha_score += 5
            if liquidity > 10000: alpha_score += 5
            
            # Price momentum (15 points)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            if price_change > 10: alpha_score += 5
            if price_change > 25: alpha_score += 7
            if price_change > 50: alpha_score += 3
            
            gem = {
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume_24h': volume_24h,
                'price_change_24h': price_change,
                'buy_ratio': buy_ratio,
                'buys': buys,
                'sells': sells,
                'total_txns': total_txns,
                'vol_mcap_ratio': vol_mcap_ratio,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'chain': pair.get('chainId', 'Unknown'),
                'url': pair.get('url', ''),
                'pairAddress': pair.get('pairAddress', '')
            }
            
            filtered_gems.append(gem)
    
    # Sort by alpha score
    filtered_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    return filtered_gems

def generate_memecoin_report(gems):
    """Generate cron report for Solana memecoins"""
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 SOLANA MEMECOIN ALPHA SCANNER REPORT
================================================
Scanning DexScreener for sub 30k-200k MCap gems
Scan Time: {timestamp}
Market Cap Range: $30,000 - $200,000
Chain Filter: Solana Only

"""
    
    if not gems:
        report += "🔍 No Solana memecoins detected in target range\nMarket may be quiet or scan needs adjustment\n"
    else:
        report += f"🔥 TOP {min(len(gems), 8)} ALPHA MEMECOINS ({len(gems)} total)\n" + "-" * 40 + "\n"
        
        for i, gem in enumerate(gems[:8], 1):
            report += f"""{i}. {gem['symbol']} - Alpha Score: {gem['alpha_score']}/80
   💰 Market Cap: ${gem['mcap']:,}
   📈 24h Volume: ${gem['volume_24h']:,.0f} ({gem['vol_mcap_ratio']:.1f}%)
   📊 Price Change: {gem['price_change_24h']:.1f}%
   💧 Liquidity: ${gem['liquidity']:,.0f}
   🔄 Transactions: {gem['total_txns']} ({gem['buys']} buys/{gem['sells']} sells - {gem['buy_ratio']:.1%})
   🌐 Chain: {gem['chain']}
   🔗 {gem['url']}

"""
    
    # Add market summary
    if gems:
        avg_score = sum(g['alpha_score'] for g in gems) / len(gems)
        avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
        
        report += f"""📊 MARKET SUMMARY
• Total Candidates: {len(gems)}
• Average Alpha Score: {avg_score:.1f}/80
• Average Market Cap: ${avg_mcap:,.0f}
• Average Volume/MCap Ratio: {sum(g['vol_mcap_ratio'] for g in gems)/len(gems):.1f}%

💡 Detecting alpha memecoins before mainstream attention
DYOR - High risk volatile assets"""
    
    return report

def main():
    print("🔍 Fetching Solana memecoins from DexScreener...")
    
    data = fetch_solana_memecoins()
    
    if data:
        # Save raw data for reference
        with open("solana_memecoins_latest.json", "w") as f:
            json.dump(data, f, indent=2)
    
    gems = analyze_memecoins(data)
    
    report = generate_memecoin_report(gems)
    
    print("\n" + "="*50)
    print(report)
    print("="*50)
    
    # Save report
    with open("solana_memecoin_alpha_report_current.txt", "w") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    result = main()