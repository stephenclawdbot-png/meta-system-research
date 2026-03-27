#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import time

class EnhancedAlphaScanner:
    def __init__(self, min_mcap=30000, max_mcap=200000):
        self.min_mcap = min_mcap
        self.max_mcap = max_mcap
        
    def fetch_specific_endpoints(self):
        """Fetch from specific DexScreener endpoints that work"""
        endpoints = [
            "https://api.dexscreener.com/latest/dex/search?q=memecoin",
            "https://api.dexscreener.com/latest/dex/search?q=solana",
            "https://api.dexscreener.com/latest/dex/search?q=pepe",
            "https://api.dexscreener.com/latest/dex/search?q=doge",
            "https://api.dexscreener.com/latest/dex/search?q=bonk",
            "https://api.dexscreener.com/latest/dex/search?q=wif",
            "https://api.dexscreener.com/latest/dex/search?q=slerf",
            "https://api.dexscreener.com/latest/dex/search?q=cat",
            "https://api.dexscreener.com/latest/dex/search?q=ai",
            "https://api.dexscreener.com/latest/dex/search?q=trump",
            "https://api.dexscreener.com/latest/dex/search?q=maga",
            "https://api.dexscreener.com/latest/dex/search?q=based",
            "https://api.dexscreener.com/latest/dex/search?q=sam",
            "https://api.dexscreener.com/latest/dex/search?q=rocket",
            "https://api.dexscreener.com/latest/dex/search?q=baby",
            "https://api.dexscreener.com/latest/dex/search?q=inu",
            "https://api.dexscreener.com/latest/dex/search?q=frog",
            "https://api.dexscreener.com/latest/dex/search?q=hamster",
            "https://api.dexscreener.com/latest/dex/search?q=money",
            "https://api.dexscreener.com/latest/dex/search?q=cash",
        ]
        
        all_tokens = []
        seen_addresses = set()
        
        for endpoint in endpoints:
            try:
                print(f"Fetching from {endpoint.split('=')[-1]}...")
                response = requests.get(endpoint, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data and 'pairs' in data:
                        for token in data['pairs']:
                            base_address = token.get('baseToken', {}).get('address')
                            if base_address and base_address not in seen_addresses:
                                seen_addresses.add(base_address)
                                all_tokens.append(token)
                        print(f"  Found {len(data['pairs'])} tokens")
                # Be nice to the API
                time.sleep(0.5)
            except Exception as e:
                print(f"Error fetching from {endpoint}: {e}")
        
        return all_tokens
    
    def filter_and_score_tokens(self, tokens):
        """Filter tokens by mcap range and apply memecoin criteria"""
        filtered = []
        
        for token in tokens:
            try:
                # Use FDV if available, fallback to marketCap
                mcap = token.get('marketCap', token.get('fdv', 0))
                
                # Skip if no market cap
                if mcap == 0:
                    continue
                    
                # Filter by our range
                if self.min_mcap <= mcap <= self.max_mcap:
                    volume = token.get('volume', {}).get('h24', 0)
                    
                    # Additional memecoin criteria
                    symbol = token.get('baseToken', {}).get('symbol', '').lower()
                    name = token.get('baseToken', {}).get('name', '').lower()
                    
                    # Must have at least $100 volume and be somewhat active
                    if volume >= 100:
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                            'mcap': mcap,
                            'volume': volume,
                            'price': token.get('priceUsd', 0),
                            'price_change': token.get('priceChange', {}).get('h24', 0),
                            'liquidity': token.get('liquidity', {}).get('usd', 0),
                            'txns': self.sum_transactions(token.get('txns', {})),
                            'buy_ratio': self.calculate_buy_ratio(token),
                            'alpha_score': self.calculate_alpha_score(token),
                            'url': token.get('url', ''),
                            'chain': token.get('chainId', ''),
                            'age': self.calculate_age(token.get('pairCreatedAt', 0))
                        }
                        filtered.append(token_info)
            except Exception as e:
                continue
        
        return filtered
    
    def sum_transactions(self, txns_data):
        """Sum transactions across time periods"""
        total = 0
        if txns_data.get('h24'):
            total += sum(txns_data['h24'].values())
        if txns_data.get('h6'):
            total += sum(txns_data['h6'].values())
        if txns_data.get('h1'):
            total += sum(txns_data['h1'].values())
        return total
    
    def calculate_buy_ratio(self, token):
        """Calculate buy ratio"""
        txns = token.get('txns', {})
        h24 = txns.get('h24', {})
        buys = h24.get('buys', 0)
        sells = h24.get('sells', 0)
        
        if buys + sells == 0:
            return 0.5
        
        return buys / (buys + sells)
    
    def calculate_alpha_score(self, token):
        """Calculate alpha score (0-100)"""
        mcap = token.get('marketCap', token.get('fdv', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        if mcap <= 0:
            return 0
        
        # Volume/MCap ratio (30 pts max)
        vol_mcap = (volume / mcap) * 100
        vol_score = min(30, vol_mcap * 0.3)
        
        # Price momentum (20 pts max)
        price_score = min(20, max(0, price_change) * 0.2)
        
        # Liquidity (20 pts max)
        liquidity = token.get('liquidity', {}).get('usd', 0)
        liq_score = min(20, liquidity / 10000 * 20)
        
        # Transaction activity (15 pts max)
        txns = self.sum_transactions(token.get('txns', {}))
        txn_score = min(15, txns / 200 * 15)
        
        # Buy ratio (10 pts max)
        buy_ratio = self.calculate_buy_ratio(token)
        buy_score = min(10, buy_ratio * 10)
        
        # Age penalty (5 pts max)
        age = self.calculate_age(token.get('pairCreatedAt', 0))
        age_score = max(0, min(5, 5 - (age / 24) * 0.5))
        
        return vol_score + price_score + liq_score + txn_score + buy_score + age_score
    
    def calculate_age(self, timestamp):
        """Calculate age in hours"""
        if not timestamp:
            return 24
        
        created_dt = datetime.fromtimestamp(timestamp / 1000)
        now = datetime.now()
        return (now - created_dt).total_seconds() / 3600
    
    def scan_and_report(self):
        """Run scan and generate report"""
        print("🧠 ENHANCED MEMECOIN ALPHA SCANNER")
        print("=" * 80)
        print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
        print(f"Target Range: ${self.min_mcap:,} - ${self.max_mcap:,} Market Cap")
        print("Scanning DexScreener for alpha memecoin opportunities...\n")
        
        # Fetch tokens
        tokens = self.fetch_specific_endpoints()
        print(f"\nTotal tokens found: {len(tokens)}")
        
        # Filter and score
        filtered = self.filter_and_score_tokens(tokens)
        print(f"Tokens in target range: {len(filtered)}")
        
        if not filtered:
            print("\n❌ No suitable alpha gems found in target range")
            return
        
        # Sort by alpha score
        filtered.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        # Take top 12
        top_tokens = filtered[:12]
        
        # Metrics
        avg_mcap = sum(t['mcap'] for t in top_tokens) / len(top_tokens)
        avg_volume = sum(t['volume'] for t in top_tokens) / len(top_tokens)
        avg_vol_mcap = sum(t['volume']/t['mcap'] if t['mcap']>0 else 0 for t in top_tokens) / len(top_tokens) * 100
        avg_buy_ratio = sum(t['buy_ratio'] for t in top_tokens) / len(top_tokens)
        avg_alpha = sum(t['alpha_score'] for t in top_tokens) / len(top_tokens)
        
        # Report
        print(f"\n📊 MARKET SUMMARY")
        print("-" * 80)
        print(f"• Total Tokens Analyzed: {len(tokens)}")
        print(f"• Eligible Alpha Gems: {len(filtered)}")
        print(f"• Average Market Cap: ${avg_mcap:,.0f}")
        print(f"• Average Volume: ${avg_volume:,.0f}")
        print(f"• Average Volume/MCap Ratio: {avg_vol_mcap:.1f}%")
        print(f"• Average Buy Ratio: {avg_buy_ratio*100:.1f}%")
        print(f"• Average Alpha Score: {avg_alpha:.1f}/100")
        
        print(f"\n🔥 TOP {len(top_tokens)} ALPHA GEMS (Sorted by Alpha Score)")
        print("-" * 80)
        
        for i, token in enumerate(top_tokens, 1):
            print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']:.1f}/100")
            print(f"   📈 24h Stats: ${token['volume']:,.0f} vol • ${token['mcap']:,.0f} mcap • {(token['volume']/token['mcap']*100 if token['mcap']>0 else 0):.1f}% ratio")
            print(f"   📊 Sentiment: {token['price_change']:.1f}% price • {token['buy_ratio']*100:.1f}% buy ratio")
            print(f"   🔄 Activity: {token['txns']} txns total")
            print(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
            print(f"   ⏳ Age: {token['age']:.1f} hours")
            print(f"   🌐 Chain: {token['chain']}")
            print(f"   🔗 {token['url']}")
            print()
        
        # Risk assessment
        print("💡 ALPHA SIGNALS DETECTED")
        print("-" * 80)
        
        best_token = top_tokens[0] if top_tokens else None
        if best_token:
            vol_ratio = best_token['volume'] / best_token['mcap'] * 100 if best_token['mcap'] > 0 else 0
            
            if vol_ratio > 50:
                signal = "🚀 STRONG: Excellent volume efficiency"
            elif vol_ratio > 20:
                signal = "📈 GOOD: Healthy trading activity"
            else:
                signal = "📉 WEAK: Limited volume action"
            
            print(f"• Top Alpha: {best_token['symbol']} ({best_token['alpha_score']:.1f}/100)")
            print(f"• Key Signal: {signal}")
            
            if best_token['liquidity'] < 5000:
                print("⚠️ RISK: Very low liquidity (high slippage risk)")
            elif best_token['liquidity'] < 20000:
                print("⚠️ RISK: Limited liquidity")
            else:
                print("✅ LIQUIDITY: Adequate pool depth")
                
            if best_token['buy_ratio'] > 0.7:
                print("📈 BULLISH: Strong buy pressure")
            elif best_token['buy_ratio'] > 0.6:
                print("📈 POSITIVE: More buyers than sellers")
            else:
                print("📊 NEUTRAL: Balanced trading")
        
        print(f"\n⚠️ DISCLAIMER: High risk memecoin alpha detection at {datetime.now().strftime('%I:%M %p')}")
        print("   DYOR (Do Your Own Research) required before any investment")

if __name__ == "__main__":
    scanner = EnhancedAlphaScanner(min_mcap=30000, max_mcap=200000)
    scanner.scan_and_report()