#!/usr/bin/env python3
"""
Enhanced Memecoin Alpha Scanner v3.0
Focuses on DexScreener for sub 30k-200k mcap memecoins
Detects alpha before mainstream attention with improved metrics
"""

import requests
import json
from datetime import datetime
import time
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemecoinAlphaScanner:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.search_terms = ["meme", "dog", "cat", "pepe", "elon", "ai", "bonk", "wif", "shib", "baby", "coin"]
        self.mcap_range = (30000, 200000)  # Sub 30k-200k focus
        
    def fetch_dexscreener_pairs(self, search_term: str) -> List[Dict]:
        """Fetch pairs from DexScreener search API"""
        url = f"{self.base_url}/search?q={search_term}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'pairs' not in data:
                return []
                
            return data['pairs']
        except Exception as e:
            logger.warning(f"Error fetching {search_term}: {e}")
            return []
    
    def filter_alpha_candidates(self, pairs: List[Dict]) -> List[Dict]:
        """Filter tokens in target mcap range with alpha potential"""
        filtered = []
        
        for pair in pairs:
            mcap = pair.get('fdv', 0)
            
            # Filter by market cap range
            if not (self.mcap_range[0] <= mcap <= self.mcap_range[1]):
                continue
            
            # Extract key metrics
            vol_24h = pair.get('volume', {}).get('h24', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            dex_id = pair.get('dexId', '')
            chain_id = pair.get('chainId', '')
            
            # Skip pairs with no recent activity
            if vol_24h <= 100:  # Minimum volume threshold
                continue
            
            token_info = {
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'mcap': mcap,
                'volume_24h': vol_24h,
                'price': pair.get('priceUsd', 0),
                'price_change_24h': price_change,
                'dex': dex_id,
                'chain': chain_id,
                'url': pair.get('url', ''),
                'txns_24h': len(pair.get('txns', {}).get('h24', [])),
                'buy_ratio': self.calculate_buy_ratio(pair),
                'liquidity': pair.get('liquidity', {}).get('usd', 0)
            }
            
            filtered.append(token_info)
        
        return filtered
    
    def calculate_buy_ratio(self, pair: Dict) -> float:
        """Calculate buy/sell ratio from transaction data"""
        try:
            txns = pair.get('txns', {}).get('h24', [])
            if not txns:
                return 0
            
            buy_count = sum(1 for txn in txns if txn.get('tradeType') == 'BUY')
            return (buy_count / len(txn)) * 100
        except:
            return 0
    
    def calculate_alpha_score(self, token: Dict) -> float:
        """Calculate comprehensive alpha score (0-100)"""
        try:
            # Volume/MCap ratio (most important - 40% weight)
            vol_mcap_ratio = min(50, (token['volume_24h'] / token['mcap']) * 100) if token['mcap'] > 0 else 0
            
            # Price momentum (25% weight)
            momentum_score = min(25, max(0, token['price_change_24h'])) if token['price_change_24h'] else 0
            
            # Transaction activity (15% weight)
            txn_score = min(15, token['txns_24h'] / 10)
            
            # Buy ratio sentiment (20% weight)
            sentiment_score = min(20, token['buy_ratio'] / 5)
            
            alpha_score = (
                vol_mcap_ratio * 0.4 +
                momentum_score * 0.25 +
                txn_score * 0.15 +
                sentiment_score * 0.2
            )
            
            return round(min(100, alpha_score), 1)
        except:
            return 0
    
    def scan_memecoins(self) -> List[Dict]:
        """Complete memecoin scan across all search terms"""
        all_tokens = []
        
        for term in self.search_terms:
            logger.info(f"Scanning for '{term}' memecoins...")
            pairs = self.fetch_dexscreener_pairs(term)
            filtered = self.filter_alpha_candidates(pairs)
            all_tokens.extend(filtered)
            
            # Rate limiting
            time.sleep(0.5)
        
        # Remove duplicates by symbol
        seen_symbols = set()
        unique_tokens = []
        
        for token in all_tokens:
            if token['symbol'] not in seen_symbols:
                seen_symbols.add(token['symbol'])
                unique_tokens.append(token)
        
        # Calculate alpha scores
        for token in unique_tokens:
            token['alpha_score'] = self.calculate_alpha_score(token)
        
        return sorted(unique_tokens, key=lambda x: x['alpha_score'], reverse=True)
    
    def generate_report(self, tokens: List[Dict]) -> str:
        """Generate comprehensive alpha scan report"""
        report = []
        
        # Header
        report.append("🎯 MEMECOIN ALPHA SCANNER - ENHANCED V3.0")
        report.append("=" * 60)
        report.append(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
        report.append(f"Market Cap Range: ${self.mcap_range[0]:,} - ${self.mcap_range[1]:,}")
        report.append("Focus: Early alpha detection pre-mainstream attention")
        report.append("")
        
        if not tokens:
            report.append("❌ No alpha candidates found in target range")
            return "\n".join(report)
        
        # Market overview
        report.append("📊 MARKET OVERVIEW")
        report.append("-" * 30)
        report.append(f"Total Alpha Candidates: {len(tokens)} tokens")
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_vol = sum(t['volume_24h'] for t in tokens) / len(tokens)
        avg_alpha = sum(t['alpha_score'] for t in tokens) / len(tokens)
        report.append(f"Average Market Cap: ${avg_mcap:,.0f}")
        report.append(f"Average Volume: ${avg_vol:,.0f}")
        report.append(f"Average Alpha Score: {avg_alpha:.1f}/100")
        report.append("")
        
        # Top alpha gems
        report.append("🔥 TOP ALPHA GEMS (Sorted by Alpha Score)")
        report.append("-" * 50)
        
        for i, token in enumerate(tokens[:10], 1):
            vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
            
            report.append(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
            report.append(f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio")
            report.append(f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token['buy_ratio']:.1f}% buy ratio")
            report.append(f"   🔄 Activity: {token['txns_24h']} txns")
            report.append(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
            report.append(f"   🌐 Chain: {token['chain']}")
            report.append(f"   🔗 {token['url']}")
            report.append("")
        
        # Alpha signal analysis
        report.append("💡 KEY ALPHA SIGNALS DETECTED")
        report.append("-" * 30)
        
        strong_alpha = [t for t in tokens if t['alpha_score'] >= 60]
        moderate_alpha = [t for t in tokens if 40 <= t['alpha_score'] < 60]
        weak_alpha = [t for t in tokens if t['alpha_score'] < 40]
        
        report.append(f"Strong Alpha (>60): {len(strong_alpha)} tokens")
        report.append(f"Moderate Alpha (40-60): {len(moderate_alpha)} tokens")
        report.append(f"Weak Alpha (<40): {len(weak_alpha)} tokens")
        report.append("")
        
        # Recommendations
        report.append("📋 TRADING RECOMMENDATIONS")
        report.append("-" * 30)
        
        if strong_alpha:
            report.append("✅ STRONG OPPORTUNITIES: Consider positions in top alpha gems")
            report.append("   Focus on tokens with high volume/mcap ratios (>25%)")
        elif moderate_alpha:
            report.append("⚠️ MODERATE OPPORTUNITIES: Wait for confirmation signals")
            report.append("   Monitor volume growth before entering")
        else:
            report.append("🔴 LIMITED OPPORTUNITIES: Market appears quiet")
            report.append("   Wait for better market conditions")
        
        report.append("")
        report.append("⚠️ DISCLAIMER: High-risk memecoin assets - DYOR required")
        report.append("Next alpha scan in 5-15 minutes")
        
        return "\n".join(report)

def main():
    """Main execution function"""
    scanner = MemecoinAlphaScanner()
    
    print("🔄 Scanning DexScreener for memecoin alpha...")
    tokens = scanner.scan_memecoins()
    
    report = scanner.generate_report(tokens)
    print(report)
    
    # Save detailed data for analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"alpha_scan_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    logger.info(f"Scan complete. Data saved to {filename}")

if __name__ == "__main__":
    main()