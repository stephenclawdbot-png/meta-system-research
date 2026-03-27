#!/usr/bin/env python3
"""
Enhanced Memecoin Scanner for Alpha Opportunities
Scans DexScreener for memecoins with $10k–$500k market cap (wider range)
"""

import requests
import json
import time
from datetime import datetime

class EnhancedMemecoinScanner:
    def __init__(self):
        self.dexscreener_base = "https://api.dexscreener.com"
        self.target_mcap_range = (10000, 500000)  # Wider range: $10k - $500k
        
    def fetch_trending_pairs(self):
        """Fetch trending pairs from DexScreener"""
        try:
            url = f"{self.dexscreener_base}/latest/dex/search?q=trending"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('pairs', [])
        except Exception as e:
            print(f"Error fetching trending pairs: {e}")
        return []
    
    def fetch_new_pairs(self):
        """Fetch newly created pairs from DexScreener"""
        try:
            # Try different searches for new tokens
            searches = ["new", "recent", "just", "created"]
            all_pairs = []
            
            for search_term in searches:
                url = f"{self.dexscreener_base}/latest/dex/search?q={search_term}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    all_pairs.extend(data.get('pairs', []))
        except Exception as e:
            print(f"Error fetching new pairs: {e}")
        return all_pairs
    
    def fetch_solana_pairs(self):
        """Fetch Solana-specific trending pairs"""
        try:
            url = f"{self.dexscreener_base}/latest/dex/chains/solana"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('pairs', [])
        except Exception as e:
            print(f"Error fetching Solana pairs: {e}")
        return []
    
    def analyze_token_metrics(self, pairs):
        """Analyze token metrics for alpha opportunities"""
        opportunities = []
        
        for pair in pairs:
            try:
                # Extract metrics
                mcap = pair.get('marketCap', 0)
                fdv = pair.get('fdv', 0)
                effective_mcap = mcap if mcap > 0 else fdv
                
                # Skip if no market cap
                if not effective_mcap or effective_mcap < self.target_mcap_range[0] or effective_mcap > self.target_mcap_range[1]:
                    continue
                
                # Volume data
                volume_data = pair.get('volume', {})
                volume_24h = volume_data.get('h24', 0) if isinstance(volume_data, dict) else volume_data
                
                # Skip tokens with very low volume
                if volume_24h < 100:
                    continue
                
                # Price change
                price_change_data = pair.get('priceChange', {})
                price_change_24h = price_change_data.get('h24', 0) if isinstance(price_change_data, dict) else price_change_data
                
                # Liquidity
                liquidity_data = pair.get('liquidity', {})
                liquidity = liquidity_data.get('usd', 0) if isinstance(liquidity_data, dict) else liquidity_data
                
                # Age calculation
                age_hours = 24
                if 'pairCreatedAt' in pair:
                    try:
                        created_at = datetime.fromtimestamp(pair['pairCreatedAt'] / 1000)
                        age_hours = (datetime.now() - created_at).total_seconds() / 3600
                    except:
                        pass
                
                # Transaction data
                txns_24h = pair.get('txns', {}).get('h24', {})
                buys = txns_24h.get('buys', 0)
                sells = txns_24h.get('sells', 0)
                total_txns = buys + sells
                buy_ratio = buys / total_txns if total_txns > 0 else 0
                
                # Alpha scoring
                volume_ratio = volume_24h / effective_mcap if effective_mcap > 0 else 0
                momentum_score = max(0, price_change_24h) * 0.1
                age_score = max(0, 48 - age_hours) / 48 * 0.5  # Bonus for tokens <48h old
                liquidity_score = min(1, liquidity / 5000) * 0.3  # Bonus for liquidity > $5k
                activity_score = min(1, total_txns / 50) * 0.2    # Bonus for high transaction count
                
                alpha_score = volume_ratio + momentum_score + age_score + liquidity_score + activity_score
                
                opportunities.append({
                    'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                    'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                    'market_cap': effective_mcap,
                    'volume_24h': volume_24h,
                    'price_change_24h': price_change_24h,
                    'liquidity': liquidity,
                    'age_hours': age_hours,
                    'alpha_score': alpha_score,
                    'buy_ratio': buy_ratio,
                    'total_txns_24h': total_txns,
                    'chain': pair.get('chainId', ''),
                    'exchange': pair.get('dexId', ''),
                    'url': pair.get('url', '')
                })
                    
            except Exception as e:
                print(f"Error analyzing pair: {e}")
        
        # Sort by alpha score descending
        opportunities.sort(key=lambda x: x['alpha_score'], reverse=True)
        return opportunities
    
    def scan(self):
        """Main scanning function"""
        print("Enhanced memecoin scan starting...")
        
        # Fetch data from multiple sources
        trending_pairs = self.fetch_trending_pairs()
        new_pairs = self.fetch_new_pairs()
        solana_pairs = self.fetch_solana_pairs()
        
        # Combine all pairs
        all_pairs = trending_pairs + new_pairs + solana_pairs
        
        # Remove duplicates based on pair address
        unique_pairs = {}
        for pair in all_pairs:
            addr = pair.get('pairAddress', '')
            if addr:
                unique_pairs[addr] = pair
        
        all_pairs = list(unique_pairs.values())
        
        print(f"Found {len(all_pairs)} unique trading pairs")
        
        # Analyze opportunities
        opportunities = self.analyze_token_metrics(all_pairs)
        
        return opportunities

def main():
    scanner = EnhancedMemecoinScanner()
    opportunities = scanner.scan()
    
    print("\n=== ENHANCED MEMECOIN ALPHA OPPORTUNITIES ===")
    print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Market Cap Range: ${scanner.target_mcap_range[0]:,} - ${scanner.target_mcap_range[1]:,}")
    print(f"Found {len(opportunities)} opportunities")
    print("-" * 50)
    
    if not opportunities:
        print("No qualifying memecoin opportunities found.")
        print("Consider widening the market cap range or checking different time periods.")
        return
    
    for i, opp in enumerate(opportunities[:20], 1):  # Top 20
        print(f"\n#{i} {opp['name']} ({opp['symbol']})")
        print(f"  Market Cap: ${opp['market_cap']:,.2f}")
        print(f"  24h Volume: ${opp['volume_24h']:,.2f}")
        print(f"  Volume/Mcap Ratio: {(opp['volume_24h']/opp['market_cap']*100):.2f}%")
        print(f"  24h Change: {opp['price_change_24h']:.2f}%")
        print(f"  Liquidity: ${opp['liquidity']:,.2f}")
        print(f"  Buy Ratio: {opp['buy_ratio']:.0%}")
        print(f"  Total TXs: {opp['total_txns_24h']}")
        print(f"  Age: {opp['age_hours']:.1f} hours")
        print(f"  Chain: {opp['chain']}")
        print(f"  Exchange: {opp['exchange']}")
        print(f"  Alpha Score: {opp['alpha_score']:.3f}")
        if opp['url']:
            print(f"  URL: {opp['url']}")

if __name__ == "__main__":
    main()