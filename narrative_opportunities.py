#!/usr/bin/env python3
"""
NARRATIVE CREATION ANALYSIS
What's working vs what gaps exist for new token creation
"""

print("🎨 FRESH NARRATIVE OPPORTUNITIES")
print("=" * 70)

opportunities = [
    ("📱 TIKTOK VIRAL SOUNDS/MEMES", {
        "gap": "No tokens tied to viral TikTok audio moments",
        "example": "'Just give me my money' sound, Stanley cup trends",
        "why_work": "Massive Gen Z audience, instant recognition",
        "rarity": "RARE"
    }),
    
    ("🎮 GAMING NOSTALGIA", {
        "gap": "Retro gaming references underexplored",
        "example": "Runescape, Minecraft, Roblox, Habbo Hotel",
        "why_work": "Millennial/Gen Z nostalgia = emotional buy",
        "rarity": "UNDEREXPLOITED"
    }),
    
    ("🏋️ FITNESS/ATHLETE MEMES", {
        "gap": "Only GIGA MAXXING exists",
        "example": "5AM club, cold plunges, 'discipline over motivation'",
        "why_work": "Gym bro culture massive, always bullish on self",
        "rarity": "WIDE OPEN"
    }),
    
    ("💼 CORPORATE MEME/ANTI-WORK", {
        "gap": "No tokens about corporate culture",
        "example": "'Looks like we're done here', quiet quitting",
        "why_work": "Relatable to massive workforce, shareable",
        "rarity": "UNDONE"
    }),
    
    ("🧠 PSYCHEDELIC/CONSCIOUSNESS", {
        "gap": "Underexplored despite Elon's intelligence mentions",
        "example": "DMT, spiritual awakening, ego death",
        "why_work": "Overlap with tech/AI consciousness trends",
        "rarity": "NICHE"
    }),
    
    ("🍕 FOOD MEMES", {
        "gap": "Surprisingly empty considering 'cult of...' trend",
        "example": "Olive Garden unlimited breadsticks, specific chains",
        "why_work": "Universal appeal, low barrier to entry",
        "rarity": "WIDE OPEN"
    }),
    
    ("📺 STREAMER CONTENT", {
        "gap": "Rarely tokenized despite massive communities",
        "example": "Kai Cenat moments, xQc drama, streamer slang",
        "why_work": "Built-in audiences, parasocial investment",
        "rarity": "RARE"
    }),
    
    ("🎵 MUSIC/ARTIST SPECIFIC", {
        "gap": "Only generic music references",
        "example": "Drake meme formats, Taylor Swift moments",
        "why_work": "Stan culture = cult-like hodlers",
        "rarity": "UNDONE"
    }),
]

for i, (theme, details) in enumerate(opportunities, 1):
    print(f"\n{i}. {theme}")
    print(f"   Gap: {details['gap']}")
    print(f"   Example: {details['example']}")
    print(f"   Why it works: {details['why_work']}")
    print(f"   Rarity: {details['rarity']}")

print("\n\n🏆 TOP 3 RECOMMENDATIONS:")
print("=" * 70)
print("""
1. FITNESS MEME (highest conviction)
   → "Discipline DAO" or "5AM Club Token"
   → Targets gym/fitness Twitter which is huge and engaged
   → Self-improvement narrative = bullish psychology

2. CORPORATE ANTI-WORK
   → "MeetingThatCouldveBeenEmail"
   → "Corporate Survival Token"
   → Relatable, funny, infinite meme potential

3. GAMING NOSTALGIA
   → Pick one iconic game (Runescape, Minecraft)
   → Specific reference = cult following
   → Millennial money = real liquidity
""")

print("\n❌ AVOID (oversaturated):")
print("-" * 70)
print("• Dog coins (DOGE competition too strong)")
print("• Generic AI tokens (overdone since ChatGPT)")
print("• Political (unless huge news moment)")
print("• Generic animal coins (needs angle)")
