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
        
    def fetch_memecoins(self):
        """Fetch recent memecoins from DexScreener"""
        endpoints = [
            "/search?q=memecoin&limit=100",
            "/search?q=solana&limit=50",
            "/tokens/new?limit=30",
            "/tokens/popular?limit=30"
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
                mcap = token.get('fdv', token.get('marketCap', 0))
                
                # Filter by market cap range
                if self.min_mcap <= mcap <= self.max_mcap:
                    alpha_score = self.calculate_alpha_score(token)
                    
                    token_info = {
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown').upper(),
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
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
                pass  # Skip malformed tokens
        
        return filtered
    
    def calculate_alpha_score(self, token):
        """Calculate 0-100 alpha score based on multiple factors"""
        mcap = token.get('fdv', token.get('marketCap', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        # Volume/MCap ratio (most important)
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 and volume > 0 else 0
        
        # Price momentum
        momentum_score = max(0, min(price_change, 100))
        
        # Liquidity bonus
        liquidity = token.get('liquidity', {}).get('usd', 0)
        liquidity_score = min(30, liquidity / 5000 * 30)  # Bonus up to 30 points for liquidity
        
        # Transaction activity bonus
        txns = sum(token.get('txns', {}).get('h24', {}).values()) if token.get('txns', {}).get('h24') else 0
        txn_score = min(15, txns / 500 * 15)  # Bonus up to 15 points for activity
        
        # Age bonus (newer is better)
        age_hours = self.calculate_age(token.get('pairCreatedAt', 0))
        age_score = max(0, min(15, 15 - (age_hours / 24 * 15)))  # Bonus up to 15 points for freshness
        
        # Buy ratio bonus
        buy_ratio = self.calculate_buy_ratio(token)
        buy_score = min(10, buy_ratio * 10)  # Bonus up to 10 points
        
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
            return 0.5  # Neutral if no data
        
        return buys / (buys + sells)
    
    def calculate_age(self, created_timestamp):
        """Calculate age in hours since creation"""
        if not created_timestamp:
            return 24  # Default if unknown
        
        created_dt = datetime.fromtimestamp(created_timestamp / 1000)
        now = datetime.now()
        age_hours = (now - created_dt).total_seconds() / 3600
        
        return age_hours
    
    def generate_report(self):
        """Generate comprehensive alpha report"""
        tokens = self.fetch_memecoins()
        filtered_tokens = self.filter_and_score_tokens(tokens)
        
        # Sort by alpha score
        filtered_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
        
        # Limit to top 10
        top_tokens = filtered_tokens[:10]
        
        # Calculate market metrics
        if top_tokens:
            avg_mcap = sum(t['mcap'] for t in top_tokens) / len(top_tokens)
            avg_volume = sum(t['volume_24h'] for t in top_tokens) / len(top_tokens)
            avg_vol_mcap_ratio = sum((t['volume_24h']/t['mcap'] if t['mcap']>0 else 0) for t in top_tokens) / len(top_tokens) * 100
            avg_buy_ratio = sum(t['buy_ratio'] for t in top_tokens) / len(top_tokens)
            
            metrics = {
                'total_scanned': len(tokens),
                'tokens_in_range': len(filtered_tokens),
                'average_mcap': round(avg_mcap),
                'average_volume': round(avg_volume),
                'average_vol_mcap_ratio': round(avg_vol_mcap_ratio, 1),
                'average_buy_ratio': round(avg_buy_ratio * 100, 1),
                'average_alpha_score': round(sum(t['alpha_score'] for t in top_tokens) / len(top_tokens), 1)
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
        print(f"• Tokens Scanned: {metrics['total_scanned']}")
        print(f"• Eligible Tokens: {metrics['tokens_in_range']}")
        print(f"• Avg MCap: ${metrics['average_mcap']:,}")
        print(f"• Avg Volume: ${metrics['average_volume']:,}")
        print(f"• Avg Vol/MCap: {metrics['average_vol_mcap_ratio']}%")
        print(f"• Avg Buy Ratio: {metrics['average_buy_ratio']}%")
        print(f"• Avg Alpha Score: {metrics['average_alpha_score']}/100")
        print()
        
        if report['alpha_gems']:
            print("🔥 TOP ALPHA GEMS:")
            print("-" * 60)
            
            for i, token in enumerate(report['alpha_gems'][:5], 1):
                print(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']:.1f}/100")
                print(f"   💰 MCap: ${token['mcap']:,} | Vol: ${token['volume_24h']:,}")
                print(f"   📈 24h Change: {token['price_change_24h']:.1f}%")
                print(f"   🔥 Vol/MCap: {(token['volume_24h']/token['mcap']*100 if token['mcap']>0 else 0):.1f}%")
                print(f"   🔄 Buy Ratio: {token['buy_ratio']*100:.1f}%")
                print(f"   💧 Liquidity: ${token['liquidity']:,}")
                print(f"   ⏳ Age: {token['age_hours']:.1f} hours")
                print(f"   🌐 Dex: {token['dex']}")
                print(f"   🔗 {token['url']}")
                print()
        
        print("💡 KEY INSIGHTS:")
        if report['alpha_gems']:
            top_token = report['alpha_gems'][0]
            print(f"• Highest Alpha: {top_token['symbol']} ({top_token['alpha_score']:.1f}/100)")
            
            # Risk assessment
            if top_token['liquidity'] < 10000:
                print("⚠️  HIGH RISK: Low liquidity detected")
            elif top_token['liquidity'] < 50000:
                print("⚠️  MEDIUM RISK: Limited liquidity")
            else:
                print("✅ GOOD: Healthy liquidity")
                
            # Volume efficiency
            vol_ratio = top_token['volume_24h'] / top_token['mcap'] * 100
            if vol_ratio > 50:
                print("🚀 STRONG: Excellent volume efficiency")
            elif vol_ratio > 20:
                print("📈 GOOD: Solid market activity")
            else:
                print("📉 WEAK: Low trading volume")
        
        print()
        print("⚠️ DISCLAIMER: Extremely high risk memecoin scanning - NFA")

if __name__ == "__main__":
    scanner = AlphaScanner(min_mcap=30000, max_mcap=200000)
    scanner.print_report()