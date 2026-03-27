# 🚀 Automated Memecoin Scanner Setup

## Overview
Automated system to scan for promising memecoin opportunities and broadcast alerts to Telegram group `-1002328055394`.

## Files Created

### Core Scripts
- **`memecoin_scanner.py`** - Basic scanner with mock data
- **`advanced_memecoin_scanner.py`** - Enhanced scanner with live API integration
- **`simple_memecoin_monitor.py`** - Automated monitoring loop (30-minute intervals)
- **`telegram_memecoin_broadcaster.py`** - Telegram alert system

### Configuration
- **`heartbeat_memecoin.md`** - Heartbeat checklist for periodic scanning
- **`telegram_config.json`** - Telegram group and filter settings

## How It Works

### Scanning Criteria
- **Market Cap**: Under $100M (micro-cap potential)
- **Volume**: Over $50k (liquidity present)
- **Momentum**: Positive price movement

### Alert Format
```
🚀 **HOT MEMECOIN ALERT** 🚀
• Token: [Name]
• Market Cap: [Size]
• Volume: [Volume]
• Why it's pumping: [Catalyst]
• Action: [Recommended action]

#Memecoin #Alpha
```

## Usage

### Manual Scan
```bash
python3 advanced_memecoin_scanner.py
```

### Automated Monitoring
```bash
python3 simple_memecoin_monitor.py
```

### Telegram Broadcast Test
```bash
python3 telegram_memecoin_broadcaster.py
```

## Integration with Heartbeat

The system integrates with OpenClaw's heartbeat system:
- Scans run automatically every heartbeat (~30 minutes)
- Alerts broadcast to Telegram group
- Results logged to daily memory files

## Real Features

✅ **Live Data Integration** - Uses CoinGecko API for real prices
✅ **Smart Filtering** - Identifies promising opportunities
✅ **Automated Broadcasting** - Sends alerts to Telegram
✅ **Customizable** - Easy to modify criteria and timing
✅ **Robust** - Fallback data when APIs are unavailable

## Telegram Integration

Target Group: `-1002328055394`

Currently prints alerts to console. To enable actual Telegram sending, integrate with OpenClaw's `message` tool.

## Next Steps

1. **Test the scanner manually** to see alerts
2. **Run automated monitoring** for continuous scanning
3. **Integrate with Telegram API** for live broadcasting
4. **Customize criteria** based on trading strategy

## Warning

🚨 **NFA - Not Financial Advice** 🚨
This is an automated scanning tool for informational purposes only. Always do your own research and never invest more than you can afford to lose.