# NBA Live Data Monitoring System

A comprehensive NBA oracle system that provides real-time game data, automated updates, and betting analysis.

## Features

### ✅ Core Functionality
- **Real-time NBA data** from ESPN API
- **Live game scores** and player stats
- **Team standings** and records
- **Betting lines** and spreads (DraftKings)
- **Game schedules** with detailed information

### 🤖 Automated Updates
- **Morning Briefings** (7:00 AM) - Today's schedule with picks
- **Live Game Updates** (1:00 PM, 3:00 PM, 5:00 PM) - Live scores and status
- **Evening Recaps** (9:00 PM) - Completed games with results

### 📊 Analytics & Picks
- **Advanced game analysis** based on odds and team performance
- **Gambling picks** with confidence levels (High/Medium/Low)
- **Risk analysis** and betting recommendations
- **Performance tracking** of picks over time

## Quick Start

### Installation
```bash
# Install dependencies
pip3 install schedule aiohttp --break-system-packages

# Test the system
python3 nba_monitor.py test
```

### Usage

#### Manual Updates
```bash
# Morning briefing
python3 nba_monitor.py briefing

# Live updates
python3 nba_monitor.py updates

# Evening recap
python3 nba_monitor.py recap
```

#### Automated Scheduling
```bash
# Run automated scheduler
python3 nba_monitor.py run
```

#### Individual Components
```bash
# Test oracle system
python3 nba_oracle.py

# Test picks system
python3 nba_picks.py
```

## Files Overview

- `nba_oracle.py` - Core data fetching and parsing
- `nba_picks.py` - Analytics and gambling recommendations
- `nba_monitor.py` - Complete monitoring system with automation
- `nba_automation.py` - Legacy automation system (use monitor.py instead)
- `nba_broadcast_log.txt` - Log of all broadcasts

## Configuration

### Telegram Integration
Edit `nba_monitor.py` to add your Telegram bot token and chat ID:
```python
monitor = NBAMonitor(
    telegram_bot_token="YOUR_BOT_TOKEN",
    telegram_chat_id="YOUR_CHAT_ID"
)
```

### Timezone Configuration
The system uses UTC by default. Update timezone settings in `nba_oracle.py` for local times.

## Data Sources

### ESPN API Endpoints
- `scoreboard` - Live games, scores, odds
- `standings` - Team records and stats
- `players` - Individual player statistics

### Supported Markets
- Live game status and scores
- Team rankings and win percentages
- Betting odds from DraftKings
- Player performance metrics

## Safety Features

- **Rate limiting** to avoid API abuse
- **Error handling** with graceful fallbacks
- **Gambling disclaimer** included in all picks
- **No real money** - entertainment purposes only

## Monitoring Schedule

| Time | Event | Content |
|------|-------|---------|
| 7:00 AM | Morning Briefing | Today's games + picks |
| 1:00 PM | Live Updates | Live game status |
| 3:00 PM | Live Updates | Live game status |
| 5:00 PM | Live Updates | Live game status |
| 9:00 PM | Evening Recap | Completed games + analysis |

## Future Enhancements

- Historical performance tracking
- Player prop betting analysis
- Multi-source odds comparison
- Discord/WhatsApp integration
- Mobile notifications
- Custom betting strategies

## Legal Notice

⚠️ **DISCLAIMER**: This system is for entertainment and informational purposes only. The picks and recommendations provided are not financial advice. Gambling involves risk, and you should only bet what you can afford to lose. The creators assume no responsibility for any losses incurred.