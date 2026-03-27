#!/usr/bin/env python3
"""
DexScreener Scanner for Meme Coins
Scans DexScreener API for memecoins with market cap $30k-$200k
Runs continuous scans to detect alpha opportunities
"""

import requests
import json
from datetime import datetime
import time
import sys

class DexScreenerScanner:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.min_mcap = 30000
        self.max_mcap = 200000
        self.alpha_threshold = 60
        
        # Track previously detected tokens to avoid duplicates
        self.previously_found = set()
    
    def fetch_tokens(self):
        """Fetch tokens from DexScreener API"""
        try:
            response = requests.get(f"{self.base_url}/search?q=solana", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Fetch Error: {e}")
            return None
    
    def calculate_alpha_score(self, token):
        """Calculate alpha score based on multiple factors"""
        score = 0
        
        # Market Cap Score (30k-200k range)
        mcap = token.get('marketCap', 0)
        if self.min_mcap <= mcap <= self.max_mcap:
            # Lower MCAP gets higher score (more room to grow)
            if mcap < 50000:
                score += 25
            elif mcap < 100000:
                score += 20
            else:
                score += 15
        else:
            return 0  # Skip tokens outside our MCAP range
        
        # Volume/MCAP Ratio Score
        volume_24h = token.get('volume', {}).get('h24', 0)
        if mcap > 0:
            volume_ratio = volume_24h / mcap
            if volume_ratio > 1.0:
                score += 25
            elif volume_ratio > 0.5:
                score += 20
            elif volume_ratio > 0.2:
                score += 15
        
        # Transaction Activity
        txns = token.get('txns', {}).get('h24', {})
        total_txns = txns.get('buys', 0) + txns.get('sells', 0)
        if total_txns > 1000:
            score += 15
        elif total_txns > 500:
            score += 10
        elif total_txns > 100:
            score += 5
        
        # Buy/Sell Ratio
        if total_txns > 0:
            buy_ratio = txns.get('buys', 0) / total_txns
            if buy_ratio > 0.6:
                score += 15
            elif buy_ratio > 0.55:
                score += 10
            elif buy_ratio > 0.5:
                score += 5
        
        # Price Momentum
        price_change = token.get('priceChange', {}).get('h24', 0)
        if price_change > 10:
            score += 10
        elif price_change > 5:
            score += 5
        
        # Token Age (newer tokens get higher score)
        pair_created_at = token.get('pairCreatedAt', 0)
        if pair_created_at:
            age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
            if age_hours < 6:
                score += 10
            elif age_hours < 24:
                score += 5
        
        return score
    
    def scan(self):
        """Perform a scan and return alpha opportunities"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🔍 DexScreener Scan - {timestamp}")
        print(f"💰 Target MCAP: ${self.min_mcap:,} - ${self.max_mcap:,}")
        
        data = self.fetch_tokens()
        if not data or 'pairs' not in data:
            print("❌ No data received")
            return []
        
        alpha_tokens = []
        new_tokens_found = 0
        
        for token in data['pairs']:
            score = self.calculate_alpha_score(token)
            
            if score >= self.alpha_threshold:
                token_address = token.get('pairAddress', '')
                
                # Check if we've already found this token
                if token_address not in self.previously_found:
                    token['alpha_score'] = score
                    alpha_tokens.append(token)
                    self.previously_found.add(token_address)
                    new_tokens_found += 1
                else:
                    print(f"📭 Skipping duplicate token: {token_address[:20]}...")
        
        # Sort by alpha score
        alpha_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        print(f"✅ Found {len(alpha_tokens)} alpha opportunities ({new_tokens_found} new)")
        return alpha_tokens
    
    def format_alert(self, token):
        """Format token for alert message"""
        base_token = token.get('baseToken', {})
        ticker = base_token.get('symbol', 'Unknown')
        name = base_token.get('name', 'Unknown')
        mcap = token.get('marketCap', 0)
        volume_24h = token.get('volume', {}).get('h24', 0)
        price = token.get('priceUsd', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        # Calculate token age
        pair_created_at = token.get('pairCreatedAt', 0)
        age_hours = "Unknown"
        if pair_created_at:
            age_hours = (datetime.now().timestamp() - pair_created_at/1000) / 3600
            age_hours = f"{age_hours:.1f}h"
        
        # Get transaction data
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        buy_ratio = (buys / total_txns * 100) if total_txns > 0 else 0
        
        alert = f"🚨 **MEMECOIN ALPHA DETECTED** 🚨\n"
        alert += f"💎 **{ticker}** ({name})\n"
        alert += f"🎯 **Alpha Score**: {token['alpha_score']}/100\n"
        alert += f"📊 **Market Cap**: ${mcap:,}\n"
        alert += f"📈 **24h Volume**: ${volume_24h:,}\n"
        alert += f"💰 **Price**: ${price:.6f}\n"
        alert += f"📈 **24h Change**: {price_change:+.2f}%\n"
        alert += f"🔄 **Transactions**: {total_txns} (Buys: {buys}, Ratio: {buy_ratio:.1f}%)\n"
        alert += f"⏱️ **Age**: {age_hours}\n"
        alert += f"🔗 **DexScreener**: https://dexscreener.com/solana/{token['pairAddress']}\n"
        
        return alert
    
    def run_continuous_scan(self):
        """Run continuous scans every 5 minutes"""
        scan_count = 0
        
        print("🚀 DexScreener Alpha Scanner Started")
        print("⚡ Scanning for memecoins: $30k - $200k MCAP")
        print("🎯 Alpha Threshold: 60/100")
        print("⏰ Interval: 5 minutes")
        print("-" * 60)
        
        while True:
            scan_count += 1
            print(f"\n🔄 Scan #{scan_count} starting...")
            
            try:
                alpha_tokens = self.scan()
                
                if alpha_tokens:
                    print(f"\n🎉 Found {len(alpha_tokens)} potential alpha tokens:")
                    for token in alpha_tokens:
                        alert_message = self.format_alert(token)
                        print(f"\n{alert_message}")
                        print("-" * 50)
                        
                        # In a real implementation, you'd send this to Telegram/other channels
                        # send_telegram_message(alert_message)
                else:
                    print("📭 No new alpha tokens found this round.")
                
                print(f"⏳ Waiting 300 seconds for next scan...")
                time.sleep(300)
                
            except KeyboardInterrupt:
                print("\n🛑 Scanner stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Scan error: {e}")
                time.sleep(60)  # Wait 1 min on error

def main():
    scanner = DexScreenerScanner()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Single scan mode
        tokens = scanner.scan()
        if tokens:
            print(f"\n🔍 Alpha scan results:")
            for token in tokens:
                print(f"\n{scanner.format_alert(token)}")
                print("-" * 50)
        else:
            print("❌ No alpha tokens found in this scan.")
    else:
        # Continuous scan mode
        scanner.run_continuous_scan()

if __name__ == "__main__":
    main()