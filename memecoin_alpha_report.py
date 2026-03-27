#!/usr/bin/env python3
import json
from datetime import datetime

# Fresh DexScreener data with memecoins
dex_data = {
    "schemaVersion": "1.0.0",
    "pairs": [
        {
            "chainId": "solana",
            "dexId": "pumpswap",
            "url": "https://dexscreener.com/solana/8ittpmfhz8srxfy5u5xoasdevdbf3gs6xjxzwp8g1nft",
            "pairAddress": "8ittpMFhz8SrxFy5u5xoaSDeVdbF3gS6xjXZwP8G1nFt",
            "baseToken": {
                "address": "5446sW7E8jCzLXnT9npZNfDwBnQugVc3XdfEbqPBpump",
                "name": "The Baby Elephant",
                "symbol": "Solana"
            },
            "quoteToken": {
                "address": "So11111111111111111111111111111111111111112",
                "name": "Wrapped SOL",
                "symbol": "SOL"
            },
            "priceNative": "0.000002440",
            "priceUsd": "0.0002035",
            "txns": {
                "m5": {"buys": 529, "sells": 424},
                "h1": {"buys": 4523, "sells": 4357},
                "h6": {"buys": 9174, "sells": 9539},
                "h24": {"buys": 9174, "sells": 9539}
            },
            "volume": {
                "h24": 564990.98,
                "h6": 564990.98,
                "h1": 305644.82,
                "m5": 54232.17
            },
            "priceChange": {
                "m5": 3.5,
                "h1": 418,
                "h6": 488,
                "h24": 488
            },
            "liquidity": {
                "usd": 36295.05,
                "base": 89147018,
                "quote": 217.6554
            },
            "fdv": 203536,
            "marketCap": 203536,
            "pairCreatedAt": 1772427561000,
            "info": {
                "imageUrl": "https://cdn.dexscreener.com/cms/images/2zhihuds9VukXEC_?width=800&height=800&quality=90",
                "header": "https://cdn.dexscreener.com/cms/images/zPRzPAazNeGJrtGz?width=1500&height=500&quality=90",
                "openGraph": "https://cdn.dexscreener.com/token-images/og/solana/5446sW7E8jCzLXnT9npZNfDwBnQugVc3XdfEbqPBpump?timestamp=1772433000000",
                "websites": [{"url": "https://lakelandcurrents.com/meet-solana-howletts-wild-animal-parks-new-baby-elephant/", "label": "Website"}],
                "socials": [{"url": "https://x.com/i/communities/2028325266930487624", "type": "twitter"}]
            },
            "boosts": {"active": 10}
        },
        {
            "chainId": "solana",
            "dexId": "pumpfun",
            "url": "https://dexscreener.com/solana/76nqtfkbh3xkmcypyambkhdazezsjxgml5movdv1wy5q",
            "pairAddress": "76nQTFkbH3XkmCyPYaMbkHDAzezSJXgmL5MovDV1Wy5Q",
            "baseToken": {
                "address": "6AjA9GpSbb1u3K3d5YdXiRsAMGcUVjc7t9nhHfp1pump",
                "name": "Solana the baby elephant",
                "symbol": "Solana"
            },
            "quoteToken": {
                "address": "So11111111111111111111111111111111111111112",
                "name": "Wrapped SOL",
                "symbol": "SOL"
            },
            "priceNative": "0.0000001773",
            "priceUsd": "0.00001479",
            "txns": {
                "m5": {"buys": 32, "sells": 21},
                "h1": {"buys": 298, "sells": 206},
                "h6": {"buys": 567, "sells": 345},
                "h24": {"buys": 567, "sells": 345}
            },
            "volume": {
                "h24": 38315.56,
                "h6": 38315.56,
                "h1": 22906.36,
                "m5": 2723.92
            },
            "priceChange": {
                "m5": 33.83,
                "h1": 102,
                "h6": 505,
                "h24": 505
            },
            "fdv": 14798.39,
            "marketCap": 14798.39,
            "pairCreatedAt": 1771521676000
        },
        {
            "chainId": "solana",
            "dexId": "meteora",
            "url": "https://dexscreener.com/solana/2wdryvcjctkohkykdq1dgj4av26a7s6xgtjavrfx8ya7",
            "pairAddress": "2WDRyVcjcTKoHKyKDQ1DGj4Av26A7s6xGtJavrFX8ya7",
            "labels": ["DLMM"],
            "baseToken": {
                "address": "5446sW7E8jCzLXnT9npZNfDwBnQugVc3XdfEbqPBpump",
                "name": "The Baby Elephant",
                "symbol": "Solana"
            },
            "quoteToken": {
                "address": "So11111111111111111111111111111111111111112",
                "name": "Wrapped SOL",
                "symbol": "SOL"
            },
            "priceNative": "0.000002537",
            "priceUsd": "0.0002117",
            "txns": {
                "m5": {"buys": 15, "sells": 9},
                "h1": {"buys": 15, "sells": 9},
                "h6": {"buys": 15, "sells": 9},
                "h24": {"buys": 15, "sells": 9}
            },
            "volume": {
                "h24": 1147.72,
                "h6": 1147.72,
                "h1": 1147.72,
                "m5": 1147.72
            },
            "priceChange": {
                "m5": 3.43,
                "h1": 3.43,
                "h6": 3.43,
                "h24": 3.43
            },
            "liquidity": {
                "usd": 3575.7,
                "base": 2583881,
                "quote": 36.2879
            },
            "fdv": 211741,
            "marketCap": 211741,
            "pairCreatedAt": 1772432830000,
            "info": {
                "imageUrl": "https://cdn.dexscreener.com/cms/images/2zhihuds9VukXEC_?width=800&height=800&quality=90",
                "header": "https://cdn.dexscreener.com/cms/images/zPRzPAazNeGJrtGz?width=1500&height=500&quality=90",
                "openGraph": "https://cdn.dexscreener.com/token-images/og/solana/5446sW7E8jCzLXnT9npZNfDwBnQugVc3XdfEbqPBpump?timestamp=1772433000000",
                "websites": [{"url": "https://lakelandcurrents.com/meet-solana-howletts-wild-animal-parks-new-baby-elephant/", "label": "Website"}],
                "socials": [{"url": "https://x.com/i/communities/2028325266930487624", "type": "twitter"}]
            },
            "boosts": {"active": 10}
        },
        {
            "chainId": "ethereum",
            "dexId": "uniswap",
            "url": "https://dexscreener.com/ethereum/0x41f50f520f5095fc8403df083285232b822611c3",
            "pairAddress": "0x41F50f520f5095fC8403DF083285232B822611c3",
            "labels": ["v2"],
            "baseToken": {
                "address": "0x3D806324b6Df5AF3c1a81aCbA14A8A62Fe6D643F",
                "name": "BarbieCrashBandicootRFK888Inu",
                "symbol": "SOLANA"
            },
            "quoteToken": {
                "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "name": "Wrapped Ether",
                "symbol": "WETH"
            },
            "priceNative": "0.00000000000008018",
            "priceUsd": "0.0000000001575",
            "txns": {
                "m5": {"buys": 0, "sells": 0},
                "h1": {"buys": 0, "sells": 0},
                "h6": {"buys": 1, "sells": 1},
                "h24": {"buys": 6, "sells": 8}
            },
            "volume": {
                "h24": 553.78,
                "h6": 179.34,
                "h1": 0,
                "m5": 0
            },
            "priceChange": {
                "h6": 2.16,
                "h24": -0.02
            },
            "liquidity": {
                "usd": 90573.8,
                "base": 287397827942362,
                "quote": 23.04527
            },
            "fdv": 140066,
            "marketCap": 140066,
            "pairCreatedAt": 1690494251000,
            "info": {
                "imageUrl": "https://cdn.dexscreener.com/cms/images/353eddc2d48f515ba9246400574d1853093895d6c78a8ca0d676dc1a513da431?width=800&height=800&quality=90",
                "header": "https://cdn.dexscreener.com/cms/images/5d3332c644eda58a686dbe323e5b29ab749dddb01ad19125cdb8b918f815f82?width=1500&height=500&quality=90",
                "openGraph": "https://cdn.dexscreener.com/token-images/og/ethereum/0x3d806324b6df5af3c1a81acba14a8a62fe6d643f?timestamp=1772433000000",
                "websites": [{"url": "https://www.solanacoin.online/", "label": "Website"}, {"url": "https://opensea.io/collection/bandicoot-manlets", "label": "Cootz NFT"}],
                "socials": [{"url": "https://twitter.com/tickerSOL", "type": "twitter"}, {"url": "https://telegram.me/SOLANAPORTALRFK", "type": "telegram"}]
            }
        }
    ]
}

def calculate_alpha_score(coin):
    """Calculate alpha score based on memecoin metrics"""
    market_cap = coin.get('marketCap', 0)
    volume_24h = coin.get('volume', {}).get('h24', 0)
    
    # Get transaction data
    txns_24h = coin.get('txns', {}).get('h24', {})
    total_txns = txns_24h.get('buys', 0) + txns_24h.get('sells', 0)
    buy_ratio = txns_24h.get('buys', 0) / total_txns if total_txns > 0 else 0
    
    price_change = coin.get('priceChange', {}).get('h24', 0)
    liquidity = coin.get('liquidity', {}).get('usd', 0)
    
    # Score components (max 100 points total)
    score = 0
    
    # Volume/Market Cap ratio (most important - 35 points max)
    volume_mcap_ratio = volume_24h / market_cap if market_cap > 0 else 0
    score += min(volume_mcap_ratio * 100, 35)
    
    # Buy/Sell ratio (25 points max)
    buy_ratio_score = buy_ratio * 25 if buy_ratio > 0.5 else 0
    score += buy_ratio_score
    
    # Price momentum (20 points max)
    if price_change > 0:
        score += min(price_change / 5, 20)
    elif price_change < -20:
        score -= 5  # Penalize heavy losses
    
    # Liquidity health (10 points max)
    liquidity_score = min(liquidity / market_cap * 20, 10) if market_cap > 0 else 0
    score += liquidity_score
    
    # Transaction velocity (5 points max)
    txn_velocity = min(total_txns / 50, 5)
    score += txn_velocity
    
    # Social presence (5 points max)
    socials = coin.get('info', {}).get('socials', [])
    websites = coin.get('info', {}).get('websites', [])
    if socials:
        score += len(socials) if len(socials) <= 5 else 5
    elif websites:
        score += 2
    
    # Boost presence bonus
    boosts = coin.get('boosts', {}).get('active', 0)
    if boosts > 0:
        score += min(boosts, 5)
    
    return min(score, 100)

def analyze_memecoins():
    """Main analysis function"""
    min_mcap = 30000
    max_mcap = 200000
    
    promising_coins = []
    
    for coin in dex_data.get('pairs', []):
        market_cap = coin.get('marketCap', 0)
        symbol = coin.get('baseToken', {}).get('symbol', '')
        
        # Filter by market cap range and exclude non-memecoins
        if min_mcap <= market_cap <= max_mcap and "SOL" not in symbol and "ELEPHANT" not in symbol:
            # Calculate alpha score
            alpha_score = calculate_alpha_score(coin)
            
            promising_coins.append({
                'symbol': coin['baseToken']['symbol'],
                'name': coin['baseToken']['name'],
                'market_cap': market_cap,
                'volume_24h': coin.get('volume', {}).get('h24', 0),
                'price': coin.get('priceUsd', 0),
                'price_change_24h': coin.get('priceChange', {}).get('h24', 0),
                'liquidity': coin.get('liquidity', {}).get('usd', 0),
                'total_txns': coin.get('txns', {}).get('h24', {}).get('buys', 0) + coin.get('txns', {}).get('h24', {}).get('sells', 0),
                'buy_ratio': coin.get('txns', {}).get('h24', {}).get('buys', 0) / (coin.get('txns', {}).get('h24', {}).get('buys', 0) + coin.get('txns', {}).get('h24', {}).get('sells', 0)) if coin.get('txns', {}).get('h24', {}).get('buys', 0) + coin.get('txns', {}).get('h24', {}).get('sells', 0) > 0 else 0,
                'alpha_score': alpha_score,
                'url': coin.get('url', ''),
                'socials': coin.get('info', {}).get('socials', []),
                'websites': coin.get('info', {}).get('websites', []),
                'chain': coin.get('chainId', '')
            })
    
    # Sort by alpha score
    promising_coins.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    return promising_coins

def generate_report():
    """Generate formatted report"""
    coins = analyze_memecoins()
    
    report = []
    report.append("💎 MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 60)
    report.append(f"📊 Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+8')}")
    report.append(f"🎯 Market Cap Range: $30k-$200k")
    report.append(f"📈 Found {len(coins)} promising memecoins")
    report.append("")
    
    if not coins:
        report.append("🚫 No memecoins detected in the specified range")
        report.append("Market may be quiet or criteria too specific")
        return report
    
    for i, coin in enumerate(coins, 1):
        report.append(f"{i}. 🎯 **{coin['symbol']}** (Alpha Score: {coin['alpha_score']:.1f}/100)")
        report.append(f"   💰 Market Cap: ${coin['market_cap']:,}")
        report.append(f"   📈 24h Volume: ${coin['volume_24h']:,}")
        report.append(f"   🔥 Price Change: {coin['price_change_24h']:+.2f}%")
        report.append(f"   📊 Buy Ratio: {coin['buy_ratio']:.1%}")
        report.append(f"   🔄 Transactions: {coin['total_txns']}")
        report.append(f"   💧 Liquidity: ${coin['liquidity']:,}")
        report.append(f"   🌐 Chain: {coin['chain'].upper()}")
        report.append(f"   📛 Name: {coin['name']}")
        
        # Social indicators
        social_count = len(coin['socials']) + len(coin['websites'])
        if social_count > 0:
            report.append(f"   🔗 Socials: {social_count} links")
        
        report.append(f"   📍 URL: {coin['url']}")
        
        # Risk rating
        risk = "LOW" if coin['alpha_score'] > 60 else "MEDIUM" if coin['alpha_score'] > 40 else "HIGH"
        report.append(f"   ⚠️  Risk: {risk}")
        report.append("")
    
    # Overall market summary
    if coins:
        avg_score = sum(c['alpha_score'] for c in coins) / len(coins)
        report.append("📊 MARKET SUMMARY:")
        report.append(f"   Average Alpha Score: {avg_score:.1f}/100")
        report.append(f"   Top Gem: {coins[0]['symbol']} ({coins[0]['alpha_score']:.1f})")
        report.append(f"   Total Volume in Range: ${sum(c['volume_24h'] for c in coins):,}")
        
        if avg_score > 70:
            report.append("💎 **MARKET CONSENSUS: STRONG BULLISH SIGNALS**")
        elif avg_score > 50:
            report.append("📈 **MARKET CONSENSUS: POSITIVE MOMENTUM**")
        else:
            report.append("⚠️  **MARKET CONSENSUS: CAUTION ADVISED**")
    
    return report

if __name__ == "__main__":
    report_lines = generate_report()
    
    for line in report_lines:
        print(line)