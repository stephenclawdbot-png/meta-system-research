#!/usr/bin/env python3
"""
Memecoin Alpha Scanner v2
Scans DexScreener for memecoins with market caps $10k-$500k
More flexible approach to find newer/trending tokens
"""

import requests
import json
from datetime import datetime
import time
import sys

class MemecoinScanner:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.min_mcap_range = 10000
        self.max_mcap_range = 500000  # Broader range to catch more tokens
        self.target_mcap_range = (30000, 200000)  # Ideal range
        self.alpha_threshold = 50  # Lower threshold
        
        self.previously_found = set()
    
    def fetch_newly_listed(self):
        """Fetch newly listed tokens - these often have alpha potential"""
        try:
            # Try searching for common memecoin patterns
            searches = [
                "solana",
                "memecoin", 
                "meme",
                "coin",
                "inu",
                "dog",
                "cat",
                "pepe"
            ]
            
            all_tokens = []
            
            for query in searches:
                url = f"{self.base_url}/search?q={query}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'pairs' in data:
                        all_tokens.extend(data['pairs'])
                time.sleep(0.1)  # Rate limiting
            
            return all_tokens
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def fetch_solana_tokens(self):
        """Fetch Solana tokens specifically"""
        try:
            response = requests.get(f"{self.base_url}/tokens/solana", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Solana tokens API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Solana tokens fetch error: {e}")
            return None
    
    def calculate_memecoin_score(self, token):
        """Calculate score specifically for memecoins"""
        score = 0
        
        mcap = token.get('marketCap', 0)
        
        # Skip tokens outside our broader range
        if mcap < self.min_mcap_range or mcap > self.max_mcap_range:
            return 0
        
        # MCAP scoring - ideal range gets highest score
        if self.target_mcap_range[0] <= mcap <= self.target_mcap_range[1]:
            score += 25
        elif mcap < self.target_mcap_range[0]:
            score += 15  # Very low MCAP has potential but higher risk
        else:
            score += 10  # Higher than target but still reasonable
        
        # Volume/MCAP ratio is crucial for memecoins
        volume_24h = token.get('volume', {}).get('h24', 0)
        if mcap > 0:
            volume_ratio = volume_24h / mcap
            if volume_ratio >18:
                score += 30  # High volume ratio = massive interest
            elif volume_ratio > 1.0:
                score += 25
            elif volume_ratio > 0.5:
                score += 20
            elif volume_ratio > 0.1:
                score += 10
        
        # Transaction metrics
        txns = token.get('txns', {}).get('h24', {})
        total_txns = txns.get('buys', 0) + txns.get('sells', 0)
        if total_txns > 10000:
            score += 20
        elif total_txns > 5000:
            score += 15
        elif total_txns > 1000:
            score += 10
        elif total_txns > 100:
            score += 5
        
        # Buy/Sell ratio - critical for memecoins
        if total_txns > 0:
            buy_ratio = txns.get('buys', 0) / total_txns
            if buy_ratio > 0.7:
                score += 15
            elif buy_ratio > 0.6:
                score += 10
            elif buy_ratio > 0.55:
                score += 5
        
        # Price momentum
        price_change = token.get('priceChange', {}).get('h24', 0)
        if price_change > 50:
            score += 15
        elif price_change > 25:
            score += 10
        elif price_change > 10:
            score += 5
        
        # Age factor - newer is better for memecoins
        pair_created_at = token.get('pairCreatedAt', 0)
        if pair_created_at:
            age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
            if age_hours < 2:
                score += 15
            elif age_hours < 6:
                score += 10
            elif age_hours < 24:
                score += 5
        
        return score
    
    def scan(self):
        """Perform comprehensive scan"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔍 Memecoin Alpha Scan - {timestamp}")
        print(f"💰 MCAP Range: ${self.min_mcap_range:,} - ${self.max_mcap_range:,}")
        print(f"🎯 Target Range: ${self.target_mcap_range[0]:,} - ${self.target_mcap_range[1]:,}")
        
        # Fetch tokens from multiple sources
        tokens = self.fetch_newly_listed()
        
        solana_data = self.fetch_solana_tokens()
        if solana_data and 'pairs' in solana_data:
            tokens.extend(solana_data['pairs'])
        
        if not tokens:
            print("❌ No tokens retrieved")
            return []
        
        print(f"📊 Analyzing {len(tokens)} tokens...")
        
        alpha_tokens = []
        new_tokens_found = 0
        
        for token in tokens:
            score = self.calculate_memecoin_score(token)
            
            if score >= self.alpha_threshold:
                token_address = token.get('pairAddress', '')
                
                if token_address not in self.previously_found:
                    token['alpha_score'] = score
                    alpha_tokens.append(token)
                    self.previously_found.add(token_address)
                    new_tokens_found += 1
        
        alpha_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        print(f"✅ Found {len(alpha_tokens)} alpha opportunities ({new_tokens_found} new)")
        return alpha_tokens
    
    def format_detailed_alert(self, token):
        """Create detailed alert message"""
        base_token = token.get('baseToken', {})
        ticker = base_token.get('symbol', 'Unknown')
        name = base_token.get('name', 'Unknown')
        mcap = token.get('marketCap', 0)
        volume_24h = token.get('volume', {}).get('h24', 0)
        price = token.get('priceUsd', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        # Calculate key metrics
        volume_mcap_ratio = volume_24h / mcap if mcap > 0 else 0
        
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        
        pair_created_at = token.get('pairCreatedAt', 0)
        age_text = "Unknown"
        if pair_created_at:
            age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
            age_text = f"{age_hours:.1f}h"
        
        alert = f"🚨 **MEMECOIN ALPHA ALERT** 🚨\n"
        alert += f"💎 **{ticker}** - {name}\n"
        alert += f"🎯 **Alpha Score**: {token['alpha_score']}/100\n\n"
        alert += f"📊 **Market Cap**: ${mcap:,}\n"
        alert += f"💰 **Price**: ${price:.8f}\n"
        alert += f"📈 **24h Change**: {price_change:+.2f}%\n"
        alert += f"💹 **Volume/MCAP**: {volume_mcap_ratio:.2f}x\n"
        alert += f"🔄 **Transactions**: {total_txns:,} (Buys: {buy_ratio:.1f}%)\n"
        alert += f"⏱️ **Age**: {age_text}\n"
        alert += f"🔗 **DexScreener**: https://dexscreener.com/solana/{token['pairAddress']}\n"
        
        # Add assessment
        if token['alpha_score'] >= 80:
            alert += "\n💎 **ASSESSMENT**: HIGH CONVICTION - STRONG BUY SIGNAL"
        elif token['alpha_score'] >= 60:
            alert += "\n🔥 **ASSESSMENT**: STRONG POTENTIAL - BUY SIGNAL"
        else:
            alert += "\n⚠️ **ASSESSMENT**: MONITOR - GOOD POTENTIAL"
        
        return alert
    
    def run_scan_and_report(self):
        """Run a single scan and report results"""
        alpha_tokens = self.scan()
        
        if alpha_tokens:
            print(f"\n🎉 **ALPHA REPORT** - Found {len(alpha_tokens)} Opportunities")
            print("=" * 60)
            
            for i, token in enumerate(alpha_tokens, 1):
                alert = self.format_detailed_alert(token)
                print(f"\n{i}. {alert}")
                print("-" * 60)
            
            # Summarize
            avg_score = sum(t['alpha_score'] for t in alpha_tokens) / len(alpha_tokens)
            print(f"\n📈 **SUMMARY**: Average Alpha Score: {avg_score:.1f}/100")
            print(f"💰 **Total MCAP Opportunity**: ${sum(t['marketCap'] for t in alpha_tokens):,}")
            
            return alpha_tokens
        else:
            print("\n📭 No alpha tokens detected in this scan.")
            return []

def main():
    scanner = MemecoinScanner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Continuous scanning mode
        print("🚀 Continuous Memecoin Alpha Scanner Started")
        print("⚡ Scanning every 5 minutes")
        scan_count = 0
        
        while True:
            scan_count += 1
            print(f"\n🔄 Scan #{scan_count}")
            
            tokens = scanner.run_scan_and_report()
            
            print(f"⏳ Next scan in 300 seconds...")
            time.sleep(300)
    else:
        # Single scan mode
        scanner.run_scan_and_report()

if __name__ == "__main__":
    main()