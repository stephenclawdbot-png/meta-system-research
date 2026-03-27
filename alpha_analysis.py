#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def analyze_alpha_potential():
    """Analyze potential alpha tokens from scan results"""
    
    # Search for trending memecoins
    search_terms = ["new", "ai", "meme", "coin", "cat", "dog", "pepe"]
    
    all_results = []
    
    for term in search_terms:
        url = "https://api.dexscreener.com/latest/dex/search"
        params = {"q": term, "limit": 20}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if "pairs" in data:
                for pair in data["pairs"]:
                    # Only include Solana tokens
                    if "solana" not in pair.get("chainId", "").lower():
                        continue
                        
                    # Skip SOL token itself
                    if pair.get("baseToken", {}).get("symbol", "") == "SOL":
                        continue
                        
                    market_cap = pair.get("marketCap", 0)
                    volume_24h = pair.get("volume", {}).get("h24", 0)
                    
                    # Check transaction data for buy/sell ratio
                    txns = pair.get("txns", {})
                    buys = txns.get("h24", {}).get("buys", 0)
                    sells = txns.get("h24", {}).get("sells", 0)
                    total_txns = buys + sells
                    buy_ratio = buys / total_txns if total_txns > 0 else 0
                    
                    # Age
                    created_at = pair.get("pairCreatedAt", 0)
                    age_hours = (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60) if created_at else 0
                    
                    token_data = {
                        "symbol": pair.get("baseToken", {}).get("symbol", "Unknown"),
                        "name": pair.get("baseToken", {}).get("name", "Unknown"),
                        "market_cap": market_cap,
                        "volume_24h": volume_24h,
                        "age_hours": age_hours,
                        "age_mins": age_hours * 60,
                        "buy_ratio": buy_ratio,
                        "total_txns": total_txns,
                        "price_usd": pair.get("priceUsd", 0),
                        "url": pair.get("url", ""),
                        "search_term": term,
                        "chain": pair.get("chainId", "")
                    }
                    
                    # Skip tokens with no market cap or extremely low volume
                    if market_cap > 100 and volume_24h > 1:
                        all_results.append(token_data)
        except Exception as e:
            continue
    
    # Remove duplicates by symbol
    unique_results = {}
    for result in all_results:
        symbol = result["symbol"]
        if symbol not in unique_results or result["age_hours"] < unique_results[symbol]["age_hours"]:
            unique_results[symbol] = result
    
    # Apply alpha criteria
    alpha_candidates = []
    
    for token in unique_results.values():
        # Focus on sub-200k market cap
        if token["market_cap"] > 200000:
            continue
            
        # Age-based scoring: newer tokens score higher (less than 24h preferred)
        age_score = max(0, 100 - min(token["age_hours"], 48) * 2)
        
        # Volume/MCap ratio scoring
        volume_mcap_ratio = token["volume_24h"] / max(token["market_cap"], 1)
        volume_score = min(100, volume_mcap_ratio * 1000)
        
        # Buy ratio scoring
        buy_score = token["buy_ratio"] * 100 if token["buy_ratio"] else 0
        
        # Transaction activity scoring
        txn_score = min(100, token["total_txns"] / 50 * 100)
        
        # Composite alpha score
        alpha_score = (age_score * 0.3 + volume_score * 0.3 + buy_score * 0.2 + txn_score * 0.2)
        
        token["alpha_score"] = alpha_score
        token["age_score"] = age_score
        token["volume_score"] = volume_score
        token["buy_score"] = buy_score
        token["txn_score"] = txn_score
        
        if alpha_score > 20:  # Minimum threshold
            alpha_candidates.append(token)
    
    # Sort by alpha score
    alpha_candidates.sort(key=lambda x: x["alpha_score"], reverse=True)
    
    return alpha_candidates

if __name__ == "__main__":
    results = analyze_alpha_potential()
    
    print(f"🎯 Alpha Scanner Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Scanning for sub $200k memecoins with alpha potential\n")
    
    if results:
        print(f"Found {len(results)} potential alpha opportunities:")
        print("=" * 80)
        
        for i, token in enumerate(results[:15], 1):  # Top 15
            print(f"{i}. {token['symbol']} ({token['name']})")
            print(f"   Alpha Score: {token['alpha_score']:.1f}/100")
            print(f"   Market Cap: ${token['market_cap']:,.0f}")
            print(f"   24h Volume: ${token['volume_24h']:,.0f}")
            print(f"   Age: {token['age_hours']:.1f} hours ({token['age_mins']:.0f} min)")
            print(f"   Buy Ratio: {token['buy_ratio']:.1%}")
            print(f"   Transactions: {token['total_txns']}")
            print(f"   Breakdown: Age({token['age_score']:.1f}) Vol({token['volume_score']:.1f}) Buy({token['buy_score']:.1f}) Txn({token['txn_score']:.1f})")
            print(f"   DexScreener: {token['url']}")
            print()
    else:
        print("No alpha opportunities detected in current scan.")
        print("This could indicate:")
        print("- No promising new memecoins launched")
        print("- Market conditions unfavorable for alpha")
        print("- Scanner filters too restrictive")
        print("\nAlpha Scanner Service Status: ⚠️ OFFLINE")
        print("The dedicated alpha scanner service is not running on localhost:3111")
        print("This analysis uses DexScreener API directly with limited filtering.")
        
    # Show market conditions summary
    print("\n📊 Market Conditions:")
    memecoins_found = len(results)
    
    if memecoins_found == 0:
        print("No alpha detectable - market may be quiet")
    elif memecoins_found < 3:
        print("Limited alpha opportunities - low activity period")
    elif memecoins_found < 8:
        print("Moderate alpha opportunities - normal conditions")
    else:
        print("High alpha opportunities - active memecoin market")