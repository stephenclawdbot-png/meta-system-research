#!/usr/bin/env python3
import requests
import json
from datetime import datetime

DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"

# Filter out major/non-memecoin tokens
MAJOR_TOKENS = {
    'SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'WIF', 'BONK', 'TRUMP', 'DOGE', 'SHIB',
    'WBTC', 'WETH', 'MATIC', 'AVAX', 'ARB', 'OP', 'ADA', 'XRP', 'LINK', 'LTC',
    'ATOM', 'DOT', 'SUI', 'APT', 'SEI', 'NEAR'
}

class TargetedMemecoinScanner:
    def __init__(self, min_mcap=30000, max_mcap=200000):
        self.min_mcap = min_mcap
        self.max_mcap = max_mcap
        
    def fetch_memecoins(self):
        """Fetch recent memecoins from DexScreener with memecoin-specific queries"""
        print("🔍 Scanning DexScreener for memecoins...")
        
        # Popular memecoin search queries
        queries = [
            "memecoin", "meme", "pepe", "wojak", "doge", "shib", "bonk", "wif", "trump", 
            "famous", "celebrity", "anime", "political", "animal", "cat", "dog", "bird", 
            "elon", "x", "twitter", "facebook", "tesla", "apple", "google", "microsoft",
            "funny", "weird", "strange", "odd", "unique", "random", "test", "token", 
            "project", "community", "degen", "degens", "ape", "apes", "moon", "mars",
            "rocket", "pump", "dump", "hodl", "yolo", "fomo", "new", "fresh", "hot"
        ]
        
        all_tokens = []
        processed_pairs = set()
        
        for query in queries:
            print(f"   Searching: '{query}'...")
            try:
                response = requests.get(f"{DEXSCREENER_API}/search?q={query}&limit=50", timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data and 'pairs' in data:
                        for pair in data['pairs']:
                            pair_id = pair.get('pairAddress', '')
                            if pair_id not in processed_pairs:
                                processed_pairs.add(pair_id)
                                
                                # Check if this looks like a memecoin (not a major token)
                                base_symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                                if base_symbol not in MAJOR_TOKENS:
                                    all_tokens.append(pair)
            except Exception as e:
                print(f"   Error searching '{query}': {e}")
        
        # Also fetch new tokens
        try:
            response = requests.get(f"{DEXSCREENER_API}/tokens/new?limit=30", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    for pair in data['pairs']:
                        pair_id = pair.get('pairAddress', '')
                        if pair_id not in processed_pairs:
                            processed_pairs.add(pair_id)
                            base_symbol = pair.get('baseToken', {}).get('symbol', '').upper()
                            if base_symbol not in MAJOR_TOKENS:
                                all_tokens.append(pair)
        except Exception as e:
            print(f"   Error fetching new tokens: {e}")
        
        print(f"📍 Found {len(all_tokens)} potential memecoin candidates")
        return all_tokens
    
    def analyze_memecoin(self, token):
        """Analyze if token qualifies as memecoin alpha"""
        try:
            mcap = token.get('fdv', token.get('marketCap', 0))
            volume = token.get('volume', {}).get('h24', 0)
            
            # Filter by market cap range
            if not (self.min_mcap <= mcap <= self.max_mcap):
                return None
            
            # Filter out suspiciously low volume
            if volume < 1000:  # $1k minimum volume
                return None
            
            # Check if memecoin-like - exclude major tokens
            base_symbol = token.get('baseToken', {}).get('symbol', '').upper()
            quote_symbol = token.get('quoteToken', {}).get('symbol', '').upper()
            
            if base_symbol in MAJOR_TOKENS:
                return None
            
            # Calculate age
            age_hours = self.calculate_age(token.get('pairCreatedAt', 0))
            
            # Older tokens (>24h) are less likely to be alpha
            if age_hours > 48:
                return None
            
            # Calculate buy ratio
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0.5
            
            # Calculate memecoin score
            score = self.calculate_memecoin_score(token, buy_ratio)
            
            return {
                'symbol': base_symbol,
                'name': token.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume_24h': volume,
                'price': token.get('priceUsd', 0),
                'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                'liquidity': token.get('liquidity', {}).get('usd', 0),
                'txns_24h': buys + sells,
                'buy_ratio': buy_ratio,
                'score': score,
                'age_hours': age_hours,
                'url': token.get('url', ''),
                'dex': token.get('dexId', '')
            }
        except Exception as e:
            return None
    
    def calculate_memecoin_score(self, token, buy_ratio):
        """Score tokens for memecoin alpha potential (0-100)"""
        mcap = token.get('fdv', token.get('marketCap', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        liquidity = token.get('liquidity', {}).get('usd', 0)
        
        # Volume/MCap ratio (most important for memecoins)
        vol_mcap_ratio = min(100, (volume / mcap * 100) if mcap > 0 and volume > 0 else 0)
        
        # Price momentum (capped at 25)
        momentum_score = max(0, min(25, price_change))
        
        # Age bonus (newer is better for memecoins)
        age_hours = self.calculate_age(token.get('pairCreatedAt', 0))
        age_score = min(20, max(0, (24 - age_hours) / 24 * 20))
        
        # Buy ratio bonus
        buy_score = min(15, buy_ratio * 15)
        
        # Liquidity bonus (safety check)
        liquidity_score = min(15, liquidity / 10000 * 15)
        
        # Transaction activity
        txns = token.get('txns', {}).get('h24', {})
        txn_count = sum(txns.get('buy', txns.get('buys', 0)), txns.get('sell', txns.get('sells', 0)))
        txn_score = min(10, txn_count / 500 * 10)
        
        # Memecoin name bonus
        symbol = token.get('baseToken', {}).get('symbol', '').upper()
        name_bonus = 5 if len(symbol) <= 4 and any(c in symbol for c in ['PEPE', 'DOGE', 'MEME', 'WIF', 'BONK']) else 0
        
        total_score = (
            min(35, vol_mcap_ratio * 0.35) +  # Volume/mcap (35 pts max)
            momentum_score * 0.25 +           # Momentum (25 pts max)
            age_score +                      # Age (20 pts max)
            buy_score +                      # Buy ratio (15 pts max)
            liquidity_score +               # Liquidity (15 pts max)
            txn_score +                     # Transaction activity (10 pts max)
            name_bonus                      # Name bonus (5 pts max)
        )
        
        return min(100, total_score)
    
    def calculate_age(self, created_timestamp):
        """Calculate age in hours since creation"""
        if not created_timestamp:
            return 24
        
        created_dt = datetime.fromtimestamp(created_timestamp / 1000)
        now = datetime.now()
        age_hours = (now - created_dt).total_seconds() / 3600
        
        return age_hours
    
    def run_scan(self):
        """Run comprehensive memecoin scan"""
        all_tokens = self.fetch_memecoins()
        
        print("\n🔬 Analyzing tokens...")
        alpha_tokens = []
        for token in all_tokens:
            analysis = self.analyze_memecoin(token)
            if analysis:
                alpha_tokens.append(analysis)
        
        # Sort by score
        alpha_tokens.sort(key=lambda x: x['score'], reverse=True)
        
        # Generate report
        report = {
            'scan_time': datetime.now().isoformat(),
            'mcaps': [self.min_mcap, self.max_mcap],
            'total_candidates': len(all_tokens),
            'qualified_tokens': len(alpha_tokens),
            'alpha_gems': alpha_tokens[:10],  # Top 10
            'market_metrics': {
                'avg_score': sum(t['score'] for t in alpha_tokens[:5]) / len(alpha_tokens[:5]) if alpha_tokens else 0,
                'avg_mcap': sum(t['mcap'] for t in alpha_tokens[:5]) / len(alpha_tokens[:5]) if alpha_tokens else 0,
                'avg_volume': sum(t['volume_24h'] for t in alpha_tokens[:5]) / len(alpha_tokens[:5]) if alpha_tokens else 0,
                'avg_buy_ratio': sum(t['buy_ratio'] for t in alpha_tokens[:5]) / len(alpha_tokens[:5]) if alpha_tokens else 0,
                'avg_age': sum(t['age_hours'] for t in alpha_tokens[:5]) / len(alpha_tokens[:5]) if alpha_tokens else 0
            }
        }
        
        return report
    
    def print_report(self):
        """Print formatted report"""
        report = self.run_scan()
        
        print("\n" + "="*70)
        print("🎯 TARGETED MEMECOIN ALPHA SCANNER")
        print("="*70)
        print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
        print(f"Market Cap Target: ${self.min_mcap:,} - ${self.max_mcap:,}")
        
        metrics = report['market_metrics']
        print(f"\n📊 SCAN RESULTS:")
        print(f"• Total Candidates: {report['total_candidates']}")
        print(f"• Qualified Tokens: {report['qualified_tokens']}")
        
        if report['alpha_gems']:
            print(f"• Average Score: {metrics['avg_score']:.1f}/100")
            print(f"• Average MCap: ${metrics['avg_mcap']:,.0f}")
            print(f"• Average Volume: ${metrics['avg_volume']:,.0f}")
            print(f"• Average Buy Ratio: {metrics['avg_buy_ratio']*100:.1f}%")
            print(f"• Average Age: {metrics['avg_age']:.1f} hours")
        
        if report['alpha_gems']:
            print(f"\n🔥 TOP MEMECOIN ALPHA GEMS:")
            print("-" * 70)
            
            for i, token in enumerate(report['alpha_gems'], 1):
                print(f"#{i} {token['symbol']} - Score: {token['score']:.1f}/100")
                print(f"   Name: {token['name']}")
                print(f"   MCap: ${token['mcap']:,}")
                print(f"   Volume: ${token['volume_24h']:,}")
                print(f"   Vol/MCap: {(token['volume_24h']/token['mcap']*100 if token['mcap']>0 else 0):.1f}%")
                print(f"   Price Δ: {token['price_change_24h']:+.1f}%")
                print(f"   Buy Ratio: {token['buy_ratio']*100:.1f}%")
                print(f"   Liquidity: ${token['liquidity']:,}")
                print(f"   Transactions: {token['txns_24h']}")
                print(f"   Age: {token['age_hours']:.1f}h")
                print(f"   Dex: {token['dex']}")
                print(f"   {token['url']}")
                print()
                
                if i >= 3:  # Limit to top 3
                    break
        else:
            print("\n📭 No memecoin alpha gems detected this scan")
        
        print("\n⚠️  DISCLAIMER: Memecoins are extremely high risk - Not financial advice")

if __name__ == "__main__":
    scanner = TargetedMemecoinScanner(min_mcap=30000, max_mcap=200000)
    scanner.print_report()