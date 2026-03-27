#!/bin/bash

# Memecoin Alpha Scanner Startup Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Memecoin Alpha Scanner..."
echo "📈 Focus: 30k-100k mcap gems with >$1k volume"
echo "⏰ Running continuously with Telegram alerts"
echo ""

# Create necessary directories
mkdir -p alerts logs

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found, installing dependencies..."
    python3 -m venv venv
    venv/bin/pip install requests watchdog
    source venv/bin/activate
fi

# Check if scanner is already running
SCANNER_PID=$(pgrep -f "memecoin_scanner.py")
if [ -n "$SCANNER_PID" ]; then
    echo "⚠️  Scanner already running (PID: $SCANNER_PID)"
    echo "Stopping existing scanner..."
    kill $SCANNER_PID
    sleep 2
fi

# Check if monitor is already running
MONITOR_PID=$(pgrep -f "monitor_alerts.py")
if [ -n "$MONITOR_PID" ]; then
    echo "⚠️  Monitor already running (PID: $MONITOR_PID)"
    echo "Stopping existing monitor..."
    kill $MONITOR_PID
    sleep 2
fi

# Start scanner in background
echo "🔍 Starting scanner process..."
nohup venv/bin/python3 memecoin_scanner.py > logs/scanner.log 2>&1 &
SCANNER_PID=$!
echo "✅ Scanner started (PID: $SCANNER_PID)"

# Start monitor in background
echo "👀 Starting alert monitor..."
nohup venv/bin/python3 monitor_alerts.py > logs/monitor.log 2>&1 &
MONITOR_PID=$!
echo "✅ Monitor started (PID: $MONITOR_PID)"

# Save PIDs for later management
echo $SCANNER_PID > scanner.pid
echo $MONITOR_PID > monitor.pid

echo ""
echo "🎯 System Status:"
echo "   - Scanner: ✅ Running (PID: $SCANNER_PID)"
echo "   - Monitor: ✅ Running (PID: $MONITOR_PID)"
echo "   - Logs: logs/scanner.log, logs/monitor.log"
echo "   - Alerts: alerts/ directory"
echo ""
echo "📊 To check status: tail -f logs/scanner.log"
echo "🔔 To stop: ./stop_scanner.sh"
echo "📋 To view recent alerts: ls -la alerts/"
echo ""
echo "🚀 Memecoin Alpha Scanner is now LIVE!"
echo "Watching for 30k-100k mcap gems with big volume..."