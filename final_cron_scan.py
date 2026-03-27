#!/usr/bin/env python3
"""
Final cron memecoin alpha scanner
"""

import requests
from datetime import datetime

def scan_memecoins():
    """Scan for memecoins in 30k-200k mcap range"""
    timestamp = datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")
    
    try:
        # Search for various memecoin terms
        searches = ['memecoin', 'coin', 'cat', 'dog', 'pepe', 'baby', 'elon', 'moon', 'mars', 'rocket', 'lambo', 'solana', 'btc', 'eth']
        
        all_tokens = []
        
        for query in searches:
            try:
                response = requests.get(f"https://api.dexscreener.com/latest/dex/search?q={query}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    for token in data.get('pairs', []):
                        # Check if it's a memecoin (based on name/symbol)
                        name = token.get('baseToken', {}).get('name', '').lower()
                        symbol = token.get('baseToken', {}).get('symbol', '').lower()
                        
                        # Memecoin indicators
                        is_memecoin = any(keyword in name + symbol for keyword in ['meme', 'coin', 'cat', 'dog', 'pepe', 'baby', 'elon', 'moon'])
                        
                        if is_memecoin:
                            mcap = token.get('marketCap', token.get('fdv', 0))
                            if 30000 <= mcap <= 200000:
                                all_tokens.append(token)
            except:
                continue
        
        # Remove duplicates by pair address
        unique_tokens = {}
        for token in all_tokens:
            addr = token.get('pairAddress')
            if addr and addr not in unique_tokens:
                unique_tokens[addr] = token
        
        tokens = list(unique_tokens.values())
        
        if not tokens:
            return f'''⚠️ MEMECOIN ALPHA SCANNER
==========================
Scan Time: {timestamp}
No memecoins found in $30k-$200k range
Check back in 5 minutes'''
        
        # Sort by volume/mcap ratio
        tokens.sort(key=lambda x: x.get('volume', {}).get('h24', 0) / max(1, x.get('marketCap', 1)), reverse=True)
        
        # Generate report
        report_lines = [
            "🖤️ MEMECOIN ALPHA SCANNER",
            "=" * 40,
            f"Scan Time: {timestamp}",
            f"Target: Sub $30k-$200k Market Cap",
            "",
            "🎯 TOP ALPHA CANDIDATES:",
            ""
        ]
        
        for i, token in enumerate(tokens[:7], 1):
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown').upper()
            name = token.get('baseToken', {}).get('name', 'Unknown')
            mcap = token.get('marketCap', token.get('fdv', 0))
            volume = token.get('volume', {}).get('h24', 0)
            price = float(token.get('priceUsd', 0))
            change = token.get('priceChange', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            buy_ratio = buys / (buys + sells) if (buys + sells) > 0 else 0
            vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
            
            # Calculate alpha score
            alpha_score = min(100, sum([
                min(40, vol_mcap_ratio * 0.4),  # Vol/mcap ratio
                max(0, min(30, change * 0.3)),  # Price momentum
                min(20, buys / 100 * 0.2),      # Buy pressure
                min(10, liquidity / 1000 * 0.1) # Liquidity
            ]))
            
            report_lines.extend([
                f"🎯 #{i} {symbol} - Score: {alpha_score:.0f}/100",
                f"   💰 MCap: ${mcap:,} | Vol: ${volume:,}",
                f"   📈 Price: ${price:.6f} ({change:+}%)",
                f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}%",
                f"   🔄 Buy Ratio: {buy_ratio*100:.1f}%",
                f"   💧 Liquidity: ${liquidity:,}",
                f"   🔗 {token.get('url', '')}",
                ""
            ])
        
        # Summary
        avg_mcap = sum(t.get('marketCap', t.get('fdv', 0)) for t in tokens[:7]) / len(tokens[:7])
        avg_vol = sum(t.get('volume', {}).get('h24', 0) for t in tokens[:7]) / len(tokens[:7])
        avg_ratio = sum((t.get('volume', {}).get('h24', 0) / t.get('marketCap', 1) * 100) for t in tokens[:7]) / len(tokens[:7])
        avg_buy = sum((txns.get('h24', {}).get('buys', 0) / max(1, txns.get('h24', {}).get('buys', 0) + txns.get('h24', {}).get('sells', 0)) * 100) if txns.get('h24') else 0 for t in tokens[:7]) / len(tokens[:7])
        
        report_lines.extend([
            "📊 MARKET SUMMARY:",
            f"• Average MCap: ${avg_mcap:,.0f}",
            f"• Average Volume: ${avg_vol:,.0f}",
            f"• Average Vol/MCap: {avg_ratio:.1f}%",
            f"• Average Buy Ratio: {avg_buy:.1f}%",
            "",
            "📝 ALPHA CRITERIA:",
            "• Vol/MCap > 50% = Strong signal",
            "• Buy ratio > 60% = Accumulation",
            "• Price change > 20% = Momentum",
            "• Liquidity > $10k = Lower risk",
            "",
            "⚠️ DISCLAIMER: Extremely high risk - Research required"
        ])
        
        return "\n".join(report_lines)
        
    except Exception as e:
        return f"Scan error: {str(e)}"

if __name__ == "__main__":
    result = scan_memecoins()
    print(result)