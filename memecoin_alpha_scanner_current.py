#!/usr/bin/env python3
import requests
import json
from datetime import datetime

DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"

class AlphaScanner:
    def __init__(self, min_mcap=30000, max_mcap=200000):
        self.min_mcap = min_mcap
        self.max_mcap = max_mcap
        self.tokens = []
        
    def fetch_memecoins_expanded(self):
        """Fetch memecoins with expanded search terms"""
        search_terms = [
            "pepe", "doge", "shib", "floki", "bonk", "slerf", "wif", "cat", 
            "elon", "trump", "maga", "ai", "meme", "harambe", "hamster",
            "frog", "dragon", "eth", "btc", "luna", "sam", "based",
            "ana", "kitty", "wolf", "moon", "rocket", "safe", "baby",
            "baby", "inu", "pump", "ape", "sam", "click", "water",
            "money", "rich", "cash", "gold", "silver", "diamond",
            "tate", "tucker", "ben", "x", "twit", "twitter", "balls"
        ]
        
        all_tokens = []
        
        # Search popular memecoin terms
        for term in search_terms[:15]:  # Limit to avoid API limits
            try:
                response = requests.get(f"{DEXSCREENER_API}/search?q={term}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data and 'pairs' in data:
                        all_tokens.extend(data['pairs'])
                        print(f"Found {len(data['pairs'])} tokens for '{term}'")
            except Exception as e:
                print(f"Error fetching '{term}': {e}")
        
        # Deduplicate by contract address
        unique_tokens = {}
        for token in all_tokens:
            base_address = token.get('baseToken', {}).get('address')
            if base_address:
                unique_tokens[base_address] = token
        
        return list(unique_tokens.values())
    
    def fetch_emerging_tokens(self):
        """Fetch tokens from trending/new tokens endpoints"""
        endpoints = [
            "/pairs?limit=50",  # General trending
            "/tokens/trending?limit=30",
            "/tokens/hot?limit=20"
        ]
        
        all_tokens = []
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{DEXSCREENER_API}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data and 'pairs' in data:
                        all_tokens.extend(data['pairs'])
            except Exception as e:
                print(f"Error fetching from {endpoint}: {e}")
        
        return all_tokens
    
    def filter_and_score_tokens(self, tokens):
        """Filter tokens by mcap range and calculate alpha scores"""
        filtered = []
        
        for token in tokens:
            try:
                mcap = token.get('marketCap', token.get('fdv', 0))
                
                # Filter by market cap range
                if self.min_mcap <= mcap <= self.max_mcap:
                    alpha_score = self.calculate_alpha_score(token)
                    
                    # Ensure it's actually a memecoin (check volume/trading activity)
                    volume_24h = token.get('volume', {}).get('h24', 0)
                    if volume_24h > 1000:  # At least $1000 volume for memecoin status
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown').upper(),
                            'mcap': mcap,
                            'volume_24h': volume_24h,
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'liquidity': token.get('liquidity', {}).get('usd', 0),
                            'txns_24h': sum(token.get('txns', {}).get('h24', {}).values()) if token.get('txns', {}).get('h24') else 0,
                            'buy_ratio': self.calculate_buy_ratio(token),
                            'alpha_score': alpha_score,
                            'url': token.get('url', ''),
                            'dex': token.get('dexId', ''),
                            'chain': token.get('chainId', ''),
                            'created_at': token.get('pairCreatedAt', 0),
                            'age_hours': self.calculate_age(token.get('pairCreatedAt', 0))
                        }
                        filtered.append(token_info)
            except Exception as e:
                pass
        
        return filtered
    
    def calculate_alpha_score(self, token):
        """Calculate 0-100 alpha score based on multiple factors"""
        mcap = token.get('marketCap', token.get('fdv', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        # Volume/MCap ratio (most important)
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 and volume > 0 else 0
        
        # Price momentum
        momentum_score = max(0, min(abs(price_change), 100)) * (1 if price_change > 0 else 0.7)
        
        # Liquidity bonus
        liquidity = token.get('liquidity', {}).get('usd', 0)
        liquidity_score = min(30, liquidity / 5000 * 30)
        
        # Transaction activity bonus
        txns = sum(token.get('txns', {}).get('h24', {}).values()) if token.get('txns', {}).get('h24') else 0
        txn_score = min(15, txns / 500 * 15)
        
        # Age bonus (newer is better)
        age_hours = self.calculate_age(token.get('pairCreatedAt', 0))
        age_score = max(0, min(15, 15 - (age_hours / 24 * 15)))
        
        # Buy ratio bonus
        buy_ratio = self.calculate_buy_ratio(token)
        buy_score = min(10, buy_ratio * 10)
        
        total_score = (
            min(30, vol_mcap_ratio * 0.3) +  # Volume/mcap ratio (30pts max)
            momentum_score * 0.15 +         # Momentum (15pts max)
            liquidity_score +               # Liquidity (30pts max)
            txn_score +                     # Transaction activity (15pts max)
            age_score +                     # Freshness (15pts max)
            buy_score                       # Buy ratio (10pts max)
        )
        
        return min(100, total_score)
    
    def calculate_buy_ratio(self, token):
        """Calculate buy/sell ratio"""
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        
        if buys + sells == 0:
            return 0.5
        
        return buys / (buys + sells)
    
    def calculate_age(self, created_timestamp):
        """Calculate age in hours since creation"""
        if not created_timestamp:
            return 24
        
        created_dt = datetime.fromtimestamp(created_timestamp / 1000)
        now = datetime.now()
        age_hours = (now - created_dt).total_seconds() / 3600
        
        return age_hours
    
    def generate_report(self):
        """Generate comprehensive alpha report"""
        print("Fetching memecoins...")
        tokens_meme = self.fetch_memecoins_expanded()
        print(f"Found {len(tokens_meme)} tokens from meme searches")
        
        print("Fetching emerging tokens...")
        tokens_emerging = self.fetch_emerging_tokens()
        print(f"Found {len(tokens_emerging)} tokens from trending")
        
        all_tokens = tokens_meme + tokens_emerging
        print(f"Total tokens to analyze: {len(all_tokens)}")
        
        filtered_tokens = self.filter_and_score_tokens(all_tokens)
        print(f"Filtered to {len(filtered_tokens)} eligible tokens")
        
        # Sort by alpha score
        filtered_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        # Limit to top 12
        top_tokens = filtered_tokens[:12]
        
        # Calculate market metrics
        if top_tokens:
            avg_mcap = sum(t['mcap'] for t in top_tokens) / len(top_tokens)
            avg_volume = sum(t['volume_24h'] for t in top_tokens) / len(top_tokens)
            avg_vol_mcap_ratio = sum((t['volume_24h']/t['mcap'] if t['mcap']>0 else 0) for t in top_tokens) / len(top_tokens) * 100
            avg_buy_ratio = sum(t['buy_ratio'] for t in top_tokens) / len(top_tokens)
            avg_alpha_score = sum(t['alpha_score'] for t in top_tokens) / len(top_tokens)
            
            metrics = {
                'total_scanned': len(all_tokens),
                'tokens_in_range': len(filtered_tokens),
                'average_mcap': round(avg_mcap),
                'average_volume': round(avg_volume),
                'average_vol_mcap_ratio': round(avg_vol_mcap_ratio, 1),
                'average_buy_ratio': round(avg_buy_ratio * 100, 1),
                'average_alpha_score': round(avg_alpha_score, 1)
            }
        else:
            metrics = {'no_tokens': True}
        
        return {
            'scan_time': datetime.now().isoformat(),
            'market_cap_range': [self.min_mcap, self.max_mcap],
            'market_metrics': metrics,
            'alpha_gems': top_tokens,
            'disclaimer': 'High risk memecoin scanning - Not financial advice'
        }
    
    def print_report(self):
        """Print formatted report to console"""
        report = self.generate_report()
        
        print("🧠 MEMECOIN ALPHA SCANNER")
        print("=" * 60)
        print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
        print(f"Target Range: ${self.min_mcap:,} - ${self.max_mcap:,} Market Cap")
        print()
        
        metrics = report['market_metrics']
        
        if metrics.get('no_tokens'):
            print("❌ No alpha gems found in target range")
            return
        
        print("📊 MARKET OVERVIEW:")
        print(f"• Total Scanned: {metrics['total_scanned']}")
        print(f"• Eligible Tokens: {metrics['tokens_in_range']}")
        print(f"• Avg MCap: ${metrics['average_mcap']:,}")
        print(f"• Avg Volume: ${metrics['average_volume']:,}")
        print(f"• Avg Vol/MCap: {metrics['average_vol_mcap_ratio']}%")
        print(f"• Avg Buy Ratio: {metrics['average_buy_ratio']}%")
        print(f"• Avg Alpha Score: {metrics['average_alpha_score']}/100")
        print()
        
        if report['alpha_gems']:
            print(f"🔥 TOP {len(report['alpha_gems'])} ALPHA GEMS:")
            print("-" * 60)
            
            for i, token in enumerate(report['alpha_gems'], 1):
                print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']:.1f}/100")
                print(f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {(token['volume_24h']/token['mcap']*100 if token['mcap']>0 else 0):.1f}% ratio")
                print(f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token['buy_ratio']*100:.1f}% buy ratio")
                print(f"   🔄 Activity: {token['txns_24h']} txns")
                print(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
                print(f"   🌐 Chain: {token['chain']}")
                print(f"   🔗 {token['url']}")
                print()
        
        # Final summary
        if report['alpha_gems']:
            top_token = report['alpha_gems'][0]
            print("💡 KEY INSIGHTS:")
            print(f"• Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']:.1f}/100)")
            print(f"• Market Health: {metrics['average_alpha_score']}/100 average score")
            
            # Risk assessment
            if top_token['liquidity'] < 5000:
                print("⚠️ HIGH RISK: Very low liquidity")
            elif top_token['liquidity'] < 20000:
                print("⚠️ MEDIUM RISK: Low liquidity")
            else:
                print("✅ GOOD: Adequate liquidity")
                
            # Trading signal
            avg_vol_ratio = metrics['average_vol_mcap_ratio']
            if avg_vol_ratio > 50:
                print("🚀 STRONG: Excellent trading activity")
            elif avg_vol_ratio > 20:
                print("📈 GOOD: Healthy market interest")
            else:
                print("📉 WEAK: Limited trading volume")
        
        print()
        print("⚠️ DISCLAIMER: High risk alpha scanning - DYOR required")

if __name__ == "__main__":
    scanner = AlphaScanner(min_mcap=30000, max_mcap=200000)
    scanner.print_report()