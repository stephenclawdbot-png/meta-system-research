#!/bin/bash
# NBA Monitoring Cron Setup Script

# Install required Python packages
pip3 install schedule aiohttp --break-system-packages

# Make scripts executable
chmod +x nba_monitor.py nba_oracle.py nba_picks.py

# Create crontab entry for automated monitoring
(crontab -l 2>/dev/null; echo "
# NBA Monitoring System
00 07 * * * cd /Users/clawdbot/.openclaw/workspace && /usr/bin/python3 nba_monitor.py briefing
00 13 * * * cd /Users/clawdbot/.openclaw/workspace && /usr/bin/python3 nba_monitor.py updates  
00 15 * * * cd /Users/clawdbot/.openclaw/workspace && /usr/bin/python3 nba_monitor.py updates
00 17 * * * cd /Users/clawdbot/.openclaw/workspace && /usr/bin/python3 nba_monitor.py updates
00 21 * * * cd /Users/clawdbot/.openclaw/workspace && /usr/bin/python3 nba_monitor.py recap
") | crontab -

echo "✅ NBA Monitoring System Cron Jobs Setup Complete!"
echo ""
echo "📅 Schedule:"
echo "  07:00 - Morning Briefing"
echo "  13:00 - Live Updates"
echo "  15:00 - Live Updates"
echo "  17:00 - Live Updates" 
echo "  21:00 - Evening Recap"
echo ""
echo "📊 Test the system:"
echo "  python3 nba_monitor.py test"
echo ""
echo "🏀 Manual updates:"
echo "  python3 nba_monitor.py briefing"
echo "  python3 nba_monitor.py updates"
echo "  python3 nba_monitor.py recap"