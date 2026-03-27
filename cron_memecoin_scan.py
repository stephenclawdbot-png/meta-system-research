import json
import datetime

print("🎯 MEMECOIN ALPHA SCANNER - CRON REPORT")
print("="*50)
print(f"Scan Time: {datetime.datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
print(f"Market Cap Range: $30,000 - $200,000")
print("Focus: Early alpha detection before mainstream attention\n")

try:
    # Read the latest memecoin data
    with open('solana_memecoins_latest.json', 'r') as f:
        data = json.load(f)
    
    if 'pairs' in data:
        tokens = data['pairs']
        
        # Filter for 30k-200k mcap tokens
        target_tokens = [t for t in tokens if 30000 <= t.get('marketCap', 0) <= 200000]
        
        print(f"✅ Found {len(target_tokens)} tokens in target range\n")
        
        if target_tokens:
            # Sort by 24h volume/mcap ratio (high ratio = alpha potential)
            target_tokens.sort(key=lambda x: x.get('volume', {}).get('h24', 0) / max(x.get('marketCap', 1), 1), reverse=True)
            
            print("🔥 TOP ALPHA GEMS (Sorted by Alpha Score)")
            print("-" * 40)
            
            for i, token in enumerate(target_tokens[:7], 1):
                token_name = token.get('baseToken', {}).get('name', 'N/A')[:30]
                token_symbol = token.get('baseToken', {}).get('symbol', 'N/A')[:10]
                mcap = token.get('marketCap', 0)
                volume_24h = token.get('volume', {}).get('h24', 0)
                price_change = token.get('priceChange', {}).get('h24', 0)
                
                # Calculate alpha score based on volume ratio and transaction activity
                volume_ratio = (volume_24h / max(mcap, 1)) * 100
                txns_24h = token.get('txns', {}).get('h24', {})
                total_txns = txns_24h.get('buys', 0) + txns_24h.get('sells', 0)
                buy_ratio = (txns_24h.get('buys', 0) / max(total_txns, 1)) * 100
                
                # Alpha score: volume ratio (60%) + buy ratio (40%)
                alpha_score = min(100, volume_ratio * 0.6 + min(buy_ratio, 100) * 0.4)
                
                print(f"🎯 #{i} {token_name} - Alpha Score: {alpha_score:.0f}/100")
                print(f"   📈 24h Stats: ${volume_24h:,.0f} vol • ${mcap:,.0f} mcap • {volume_ratio:.1f}% ratio")
                print(f"   📊 Sentiment: {price_change:+.1f}% price • {buy_ratio:.1f}% buy ratio")
                print(f"   🔄 Activity: {total_txns} txns ({txns_24h.get('buys', 0)} buys/{txns_24h.get('sells', 0)} sells)")
                print(f"   💧 Liquidity: ${token.get('liquidity', {}).get('usd', 0):,.0f}")
                print(f"   🌐 Chain: {token.get('chainId', 'N/A')}")
                print(f"   🔗 {token.get('url', 'N/A')}")
                print()
            
            # Overall summary
            avg_mcap = sum(t.get('marketCap', 0) for t in target_tokens) / len(target_tokens)
            avg_ratio = sum(t.get('volume', {}).get('h24', 0) / max(t.get('marketCap', 1), 1) * 100 for t in target_tokens) / len(target_tokens)
            
            print("📊 MARKET SUMMARY")
            print(f"• Top Performer: {target_tokens[0].get('baseToken', {}).get('name', 'N/A')} ({int(min(100, (target_tokens[0].get('volume', {}).get('h24', 0) / max(target_tokens[0].get('marketCap', 1), 1) * 100 * 0.6 + 
                                 (target_tokens[0].get('txns', {}).get('h24', {}).get('buys', 0) / max(target_tokens[0].get('txns', {}).get('h24', {}).get('buys', 0) + 
                                  max(target_tokens[0].get('txns', {}).get('h24', {}).get('sells', 1), 1) * 100 * 0.4)))}/100)")
            print("\n💡 Key Alpha Signals:")
            print("- Volume/Mcap ratio > 25% indicates strong interest")
            print("- Buy ratio > 60% suggests accumulation phase")
            print("- High transaction volume = active community")
        
        else:
            print("❌ No memecoins found in the target market cap range.")
            
except Exception as e:
    print(f"❌ Error reading memecoin data: {e}")