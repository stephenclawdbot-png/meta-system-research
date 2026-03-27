# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Stephen's Capabilities

### Current Services
- **Crypto Oracle**: Peak analytical capability achieved (framework evolution complete - 18+ hours continuous operation)
- **NBA Oracle**: ACTIVATED ✅ (live game monitoring, automated updates, betting analysis)

## NBA Oracle Details

### Features
- Real-time game data from ESPN API
- Automated updates at 7:00 AM, 1:00 PM, 3:00 PM, 5:00 PM, 9:00 PM
- Gambling picks with confidence levels
- Live scores and player statistics

### Commands
```bash
# Manual updates
python3 nba_monitor.py briefing      # Morning briefing
python3 nba_monitor.py updates       # Live updates
python3 nba_monitor.py recap         # Evening recap

# Run scheduler
python3 nba_monitor.py run
```

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
