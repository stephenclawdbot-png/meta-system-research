#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def scan_memecoins():
    """Scan DexScreener for sub 30k-200k mcap memecoins"""
    
    # Search for Solana tokens with recent activity
    url = "https://api.dexscreener.com/latest/dex/search"
    params = {
        "q": "solana",
        "limit": 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "pairs" not in data:
            return "No token data available from DexScreener"
        
        # Filter for interesting memecoins
        potential_gems = []
        
        for pair in data["pairs"]:
            # Check if it's Solana chain (chainId can be "solana" or "solana-testnet")
            if "solana" not in pair.get("chainId", "").lower():
                continue
                
            # Get market cap
            market_cap = pair.get("marketCap", 0)
            
            # Filter for sub 30k-200k mcap range
            if market_cap < 30000 or market_cap > 200000:
                continue
            
            # Check for reasonable volume
            volume_24h = pair.get("volume", {}).get("h24", 0)
            if volume_24h < 1000:  # At least $1000 volume
                continue
            
            # Check age (created timestamp)
            created_at = pair.get("pairCreatedAt", 0)
            age_hours = (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60) if created_at else 0
            
            # Only show tokens less than 24h old
            if age_hours > 24:
                continue
            
            # Get transaction activity
            txns = pair.get("txns", {})
            buy_ratio = None
            if txns.get("h24", {}).get("buys", 0) > 0:
                total_txns = txns.get("h24", {}).get("buys", 0) + txns.get("h24", {}).get("sells", 0)
                if total_txns > 0:
                    buy_ratio = txns.get("h24", {}).get("buys", 0) / total_txns
            
            token_data = {
                "symbol": pair.get("baseToken", {}).get("symbol", "Unknown"),
                "name": pair.get("baseToken", {}).get("name", "Unknown"),
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "buy_ratio": buy_ratio,
                "age_hours": age_hours,
                "txns_24h": txns.get("h24", {}).get("buys", 0) + txns.get("h24", {}).get("sells", 0),
                "price_usd": pair.get("priceUsd", 0),
                "url": pair.get("url", ""),
                "chain": pair.get("chainId", "")
            }
            
            potential_gems.append(token_data)
        
        # Sort by volume/mcap ratio (potential for growth)
        potential_gems.sort(key=lambda x: x["volume_24h"] / max(x["market_cap"], 1), reverse=True)
        
        return potential_gems
        
    except Exception as e:
        return f"Error scanning DexScreener: {str(e)}"

if __name__ == "__main__":
    result = scan_memecoins()
    
    if isinstance(result, str):
        print(result)
    else:
        print(f"🎯 Alpha Scanner Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Found {len(result)} potential gems in $30k-$200k range\n")
        
        for i, gem in enumerate(result[:10], 1):  # Top 10
            print(f"{i}. {gem['symbol']} ({gem['name']})")
            print(f"   Market Cap: ${gem['market_cap']:,.0f}")
            print(f"   24h Volume: ${gem['volume_24h']:,.0f}")
            if gem['buy_ratio']:
                print(f"   Buy Ratio: {gem['buy_ratio']:.1%}")
            print(f"   Age: {gem['age_hours']:.1f}h")
            print(f"   Chain: {gem['chain']}")
            print(f"   Price: ${gem['price_usd']:.8f}")
            print(f"   DexScreener: {gem['url']}")
            print()