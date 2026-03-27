#!/usr/bin/env python3
"""
Cron memecoin alpha scanner for 30k-200k market cap tokens
Scan DexScreener API directly for latest data
"""

import requests
import json
from datetime import datetime

DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"

def scan_memecoins():
    """Scan DexScreener for memecoins in target market cap range"""
    try:
        # Query DexScreener for memecoin tokens
        response = requests.get(f"{DEXSCREENER_API}/search?q=solana", timeout=10)
        
        if response.status_code != 200:
            return {"error": f"API returned status {response.status_code}"}
        
        data = response.json()
        tokens = data.get('pairs', [])
        
        # Filter for our market cap range
        target_tokens = []
        for token in tokens:
            mcap = token.get('marketCap', token.get('fdv', 0))
            if 30000 <= mcap <= 200000:
                target_tokens.append(token)
        
        # Sort by creation date (newest first) and recent volume
        target_tokens.sort(key=lambda x: (
            x.get('volume', {}).get('h24', 0) / x.get('marketCap', 1),
            x.get('pairCreatedAt', 0)
        ), reverse=True)
        
        return target_tokens[:10]  # Limit to top 10
        
    except Exception as e:
        return {"error": str(e)}

def generate_report(tokens):
    """Generate plain text report for the cron delivery"""
    timestamp = datetime.now().strftime('%A, March %d, %Y — %I:%M %p (Asia/Manila)')
    
    report_lines = [
        "MEMECOIN ALPHA SCANNER REPORT",
        "=" * 50,
        f"Scan Time: {timestamp}",
        f"Target: Sub 30k-200k Market Cap Memecoins",
        "\nTOP ALPHA POTENTIALS:\n"
    ]
    
    if isinstance(tokens, dict) and 'error' in tokens:
        report_lines.append(f"❌ Scan failed: {tokens['error']}")
        return "\n".join(report_lines)
    
    if not tokens:
        report_lines.append("❌ No tokens found in target market cap range")
        return "\n".join(report_lines)
    
    for i, token in enumerate(tokens[:7], 1):
        ticker = token.get('baseToken', {}).get('symbol', 'Unknown').upper()
        mcap = token.get('marketCap', token.get('fdv', 0))
        volume = token.get('volume', {}).get('h24', 0)
        price = token.get('priceUsd', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        liquidity = token.get('liquidity', {}).get('usd', 0)
        age_hours = (datetime.now().timestamp() - token.get('pairCreatedAt', 0)/1000) / 3600
        
        vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
        buy_ratio = (buys / (buys + sells)) * 100 if (buys + sells) > 0 else 50
        
        # Calculate alpha potential score (simplified)
        alpha_score = min(100, (
            min(40, vol_mcap_ratio * 0.4) +  # Volume/MCap ratio importance
            max(0, min(20, price_change * 0.2)) +  # Price momentum
            min(15, liquidity / 10000 * 15) +  # Liquidity depth
            min(10, buy_ratio / 10) +  # Buy pressure
            max(0, min(15, max(0, 15 - (age_hours / 48))))  # Freshness bonus
        ))
        
        report_lines.extend([
            f"🎯 #{i} {ticker} - Alpha Potential: {alpha_score:.0f}/100",
            f"   💰 MCap: ${mcap:,.0f} | Vol: ${volume:,.0f}",
            f"   📈 Price: ${float(price):.8f} ({price_change:+}%)",
            f"   🔥 Vol/MCap: {vol_mcap_ratio:.1f}%",
            f"   🔄 Buy Ratio: {buy_ratio:.1f}%",
            f"   💧 Liquidity: ${liquidity:,.0f}",
            f"   ⏳ Age: {age_hours:.1f} hours",
            f"   🔗 https://dexscreener.com/{token.get('chainId', 'solana')}/{token.get('pairAddress', '')}",
            ""
        ])
    
    # Add market summary
    if tokens:
        avg_mcap = sum(t.get('marketCap', t.get('fdv', 0)) for t in tokens) / len(tokens)
        avg_volume = sum(t.get('volume', {}).get('h24', 0) for t in tokens) / len(tokens)
        avg_ratio = sum((t.get('volume', {}).get('h24', 0) / t.get('marketCap', 1) * 100) if t.get('marketCap', 1) > 0 else 0 for t in tokens) / len(tokens)
        
        report_lines.extend([
            "📊 MARKET SUMMARY:",
            f"• Tokens Scanned: {len(tokens)} in range",
            f"• Average MCap: ${avg_mcap:,.0f}",
            f"• Average Volume: ${avg_volume:,.0f}", 
            f"• Average Vol/MCap: {avg_ratio:.1f}%",
            "",
            "💡 ALPHA SIGNALS:",
            "• Vol/MCap > 25% = Strong interest",
            "• Buy Ratio > 55% = Accumulation phase",
            "• Age < 24h = Fresh launch opportunity",
            "• Liquidity > $50k = Lower risk",
            "",
            "⚠️ DISCLAIMER: High risk memecoins - Not financial advice"
        ])
    
    return "\n".join(report_lines)

if __name__ == "__main__":
    tokens = scan_memecoins()
    report = generate_report(tokens)
    print(report)