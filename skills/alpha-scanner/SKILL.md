---
name: alpha-scanner
description: Query the Alpha Scanner for real-time meme coin gems detected from Pump.fun and DexScreener. The scanner runs every 5 minutes, tracks new Solana token launches, applies alpha filters (mcap, volume, buy ratio, age, liquidity), scores them, and surfaces only NEW unseen gems that pass all criteria.
homepage: http://localhost:3111
metadata:
  {
    "openclaw":
      {
        "emoji": "💎",
        "requires": { "server": "localhost:3111" },
        "install":
          [
            {
              "id": "scanner",
              "kind": "custom",
              "setup": "Alpha Scanner service running on localhost:3111",
              "label": "Verify Alpha Scanner service running",
            },
          ],
      },
  }
---

# Alpha Scanner Skill

Query the Alpha Scanner for real-time meme coin gems detected from Pump.fun and DexScreener.

## API Base
http://localhost:3111

## Available Endpoints

### GET /api/gems
Fetch current alpha gems sorted by score.

**Query params:**
- `limit` (int, default 20) — Max results
- `min_score` (int, default 0) — Minimum alpha score (0-100)
- `source` (string) — Filter by source: pump or dex

**Example:**
```bash
curl "http://localhost:3111/api/gems?limit=5&min_score=60"
```

**Response fields per gem:**
- `ticker` — Token symbol
- `address` — Solana contract address
- `alphaScore` — 0-100 composite score
- `alphaBreakdown` — Score component breakdown
- `mcap` — Market cap in USD
- `volume24h` — 24h trading volume
- `liquidity` — Pool liquidity in USD
- `buyRatio` — Percentage of buy transactions
- `ageHuman` — Human readable age (e.g. "2h 15m")
- `links.pump` — Pump.fun URL
- `links.dexscreener` — DexScreener URL
- `links.birdeye` — Birdeye URL
- `socials` — Website, twitter, telegram if available

### GET /api/status
Get scanner operational status including scan count, tracked tokens, and current filter config.

### GET /api/token/{address}
Look up a specific token by contract address.

### POST /api/scan
Manually trigger an immediate scan cycle.

### POST /api/config
Update alpha filter criteria on the fly.

**Body example:**
```json
{
  "filters": {
    "MIN_MCAP": 10000,
    "MAX_MCAP": 2000000,
    "MIN_VOLUME_24H": 5000,
    "MIN_BUY_RATIO": 0.55
  }
}
```

### GET /api/feed
Raw JSON feed of all alpha gems (also saved to `data/alpha_feed.json`).

## Usage Patterns

- **"Show me the hottest new gems"** → `GET /api/gems?limit=5&min_score=50`
- **"Any pump.fun alphas right now?"** → `GET /api/gems?source=pump&min_score=30`
- **"Check if this token is alpha"** → `GET /api/token/{address}`
- **"Run a fresh scan now"** → `POST /api/scan`
- **"Make filters stricter — only high volume"** → `POST /api/config` with `{"filters": {"MIN_VOLUME_24H": 50000}}`
- **"What's the scanner doing?"** → `GET /api/status`

## Alpha Score Breakdown

Score is 0-100 composed of:
- **Volume (25pts)** — Higher 24h volume = more interest
- **MCap/Vol Ratio (20pts)** — Low mcap + high volume = undervalued
- **Buy Pressure (15pts)** — More buys than sells = accumulation
- **Age Freshness (15pts)** — Newer tokens score higher
- **Liquidity (10pts)** — Healthy liquidity pool
- **Socials (10pts)** — Has website/twitter/telegram
- **Txn Velocity (5pts)** — Accelerating transaction rate

## Filter Criteria (defaults)

Tokens must pass ALL to be considered alpha:
- **MCap**: $5K – $5M
- **Volume 24h**: > $1K
- **Transactions**: > 10
- **Buy ratio**: > 50%
- **Age**: 5 min – 24 hours
- **Liquidity**: > $1K

## Quick Start

```bash
# Check if scanner is running
curl http://localhost:3111/api/status

# Get top 5 alpha gems
curl "http://localhost:3111/api/gems?limit=5&min_score=70"

# Manual scan
curl -X POST http://localhost:3111/api/scan
```

## Integration Examples

### Python
```python
import requests

def get_alpha_gems(limit=10, min_score=60):
    response = requests.get(
        "http://localhost:3111/api/gems",
        params={"limit": limit, "min_score": min_score}
    )
    return response.json()
```

### Bash Script
```bash
#!/bin/bash
ALPHA_API="http://localhost:3111/api/gems"

# Get top 3 gems with score > 50
curl -s "$ALPHA_API?limit=3&min_score=50" | jq '.[] | {ticker: .ticker, score: .alphaScore, mcap: .mcap}'
```

## Notes

- Scanner runs automatically every 5 minutes
- Results are sorted by alphaScore descending
- Use `min_score` parameter to filter for higher quality gems
- Token addresses are Solana contract addresses
- All currency values are in USD