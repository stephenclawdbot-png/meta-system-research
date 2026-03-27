#!/usr/bin/env python3
"""
Generate memecoin alpha scanner report for cron delivery
"""

import requests
from datetime import datetime

def scan_and_report():
    try:
        # Fetch data from DexScreener
        response = requests.get("https://api.dexscreener.com/latest/dex/search?q=solana", timeout=10)
        data = response.json()
        
        tokens_in_range = []
        for token in data.get('pairs', [])[:100]:  # Limit to first 100
            mcap = token.get('marketCap', token.get('fdv', 0))
            if 30000 <= mcap <= 200000:
                tokens_in_range.append(token)
        
        # Sort by volume/mcap ratio (highest first)
        tokens_in_range.sort(key=lambda x: x.get('volume', {}).get('h24', 0) / max(1, x.get('marketCap', 1)), reverse=True)
        
        # Generate report
        timestamp = datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")
        
        report = [
            "MEMECOIN ALPHA SCANNER REPORT",
            "=" * 50,
            f"Scan Time: {timestamp}",
            f"Market Cap Range: $30,000 - $200,000",
            "\nTOP 7 ALPHA POTENTIALS:\n"
        ]
        
        if not tokens_in_range:
            report.append("❌ No tokens found in target market cap range")
            return "\n".join(report)
        
        for i, token in enumerate(tokens_in_range[:7], 1):
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown').upper()
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
            
            report.extend([
                f"🎯 #{i} {symbol}",
                f"   📈 Volume: ${volume:,.0f} (Vol/MCap: {vol_mcap_ratio:.1f}%)",
                f"   💰 MCap: ${mcap:,.0f} | Price: ${price:.6f} ({change:+.1f}%)",
                f"   🔄 Buy Ratio: {buy_ratio*100:.1f}% | Liquidity: ${liquidity:,.0f}",
                ""
            ])
        
        # Market summary
        avg_mcap = sum(t.get('marketCap', t.get('fdv', 0)) for t in tokens_in_range[:7]) / len(tokens_in_range[:7])
        avg_volume = sum(t.get('volume', {}).get('h24', 0) for t in tokens_in_range[:7]) / len(tokens_in_range[:7])
        avg_ratio = sum((t.get('volume', {}).get('h24', 0) / t.get('marketCap', 1) * 100) for t in tokens_in_range[:7]) / len(tokens_in_range[:7])
        
        report.extend([
            "📊 MARKET SUMMARY:",
            f"• Average MCap: ${avg_mcap:,.0f}",
            f"• Average Volume: ${avg_volume:,.0f}",
            f"• Average Vol/MCap Ratio: {avg_ratio:.1f}%",
            "",
            "💡 KEY ALPHA SIGNALS:",
            "• High Vol/MCap ratio (>25%) indicates strong interest",
            "• Buy ratio >60% suggests accumulation phase",
            "• Low age (<24h) = fresh opportunity",
            "",
            "⚠️ DISCLAIMER: High risk memecoins - DYOR required"
        ])
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error during scan: {str(e)}"

if __name__ == "__main__":
    print(scan_and_report())