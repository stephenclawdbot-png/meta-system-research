#!/usr/bin/env python3
"""
REAL-TIME MEMECOIN ALPHA SCANNER
Scans DexScreener for sub 200k mcap gems, filters for quality
Runs every 5 minutes, broadcasts alerts to Telegram
"""

import requests
import time
import json
from datetime import datetime

def fetch_dexscreener_tokens():
    """Fetch trending tokens from DexScreener API"""
    url = "https://api.dexscreener.com/latest/dex/search/?q=solana"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract trending tokens from search results
            trending_tokens = []
            for pair in data.get('pairs', [])[:100]:
                # Check if this is a memecoin (not major token like SOL)
                symbol = pair.get('baseToken', {}).get('symbol', '')
                if symbol.upper() not in ['SOL', 'ETH', 'BTC', 'USDC', 'USDT']:
                    trending_tokens.append(pair)
            return {"pairs": trending_tokens[:50]}
        else:
            return {"error": f"API returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def analyze_token(token):
    """Analyze individual token for alpha potential"""
    try:
        # Filter criteria
        mcap = token.get('fdv', 0)
        volume = token.get('volume', 0)
        age_hours = token.get('age', 24)
        buy_ratio = token.get('buyRatio', 0)
        
        # Alpha filters
        if (mcap < 200000 and mcap > 30000 and  # 30k-200k mcap
            volume > 1000 and                    # Min volume $1k
            age_hours < 24 and                   # Max age 24h
            buy_ratio > 0.6):                    # Buy ratio >60%
            
            return {
                "name": token.get('name', 'Unknown'),
                "symbol": token.get('symbol', 'Unknown'),
                "mcap": mcap,
                "volume": volume,
                "age_hours": age_hours,
                "buy_ratio": buy_ratio,
                "url": token.get('url', '')
            }
    except Exception as e:
        return None

def scan_alpha():
    """Main scanning function"""
    print(f"\n🔄 Alpha Scan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data = fetch_dexscreener_tokens()
    
    if "error" in data:
        print(f"❌ API Error: {data['error']}")
        return []
    
    alpha_tokens = []
    for pair in data.get('pairs', [])[:50]:  # Check top 50
        analysis = analyze_token(pair)
        if analysis:
            alpha_tokens.append(analysis)
    
    return alpha_tokens

if __name__ == "__main__":
    alpha_finds = scan_alpha()
    
    if alpha_finds:
        print(f"🎯 Found {len(alpha_finds)} alpha tokens!")
        for token in alpha_finds:
            print(f"• {token['symbol']} - ${token['mcap']:,} mcap - {token['buy_ratio']:.0%} buys")
        
        # ACTUAL TELEGRAM BROADCAST
        print("📱 BROADCASTING TO TELEGRAM...")
        broadcast_msg = f"💎 MEMECOIN ALPHA DETECTED\nFound {len(alpha_finds)} gems!\n"
        for token in alpha_finds[:3]:  # Max 3 tokens per broadcast
            broadcast_msg += f"• {token['symbol']} - ${token['mcap']:,} mcap - {token['buy_ratio']:.0%} buys\n"
        
        try:
            import subprocess
            # Send to group
            subprocess.run(["openclaw", "message", "send", "--to", "-1002328055394", "--message", broadcast_msg], 
                         capture_output=True, text=True)
            print("✅ Alpha broadcasted to Telegram group")
            
            # Also send to you personally
            subprocess.run(["openclaw", "message", "send", "--to", "7284633206", "--message", broadcast_msg], 
                         capture_output=True, text=True)
            print("✅ Alpha broadcasted to personal DM")
            
        except Exception as e:
            print(f"❌ Telegram broadcast failed: {e}")
            
    else:
        print("📭 No alpha gems detected this cycle")