#!/bin/bash

# Memecoin Alpha Scanner Stop Script

echo "🛑 Stopping Memecoin Alpha Scanner..."

# Stop scanner if running
if [ -f "scanner.pid" ]; then
    SCANNER_PID=$(cat scanner.pid)
    if ps -p $SCANNER_PID > /dev/null; then
        echo "⏹️  Stopping scanner (PID: $SCANNER_PID)..."
        kill $SCANNER_PID
        sleep 2
        if ps -p $SCANNER_PID > /dev/null; then
            echo "⚠️  Scanner not responding, force stopping..."
            kill -9 $SCANNER_PID
        fi
        echo "✅ Scanner stopped"
    else
        echo "⚠️  Scanner PID file exists but process not running"
    fi
    rm -f scanner.pid
else
    echo "❌ Scanner PID file not found"
fi

# Stop monitor if running
if [ -f "monitor.pid" ]; then
    MONITOR_PID=$(cat monitor.pid)
    if ps -p $MONITOR_PID > /dev/null; then
        echo "⏹️  Stopping monitor (PID: $MONITOR_PID)..."
        kill $MONITOR_PID
        sleep 2
        if ps -p $MONITOR_PID > /dev/null; then
            echo "⚠️  Monitor not responding, force stopping..."
            kill -9 $MONITOR_PID
        fi
        echo "✅ Monitor stopped"
    else
        echo "⚠️  Monitor PID file exists but process not running"
    fi
    rm -f monitor.pid
else
    echo "❌ Monitor PID file not found"
fi

# Kill any remaining processes
pkill -f "memecoin_scanner.py" 2>/dev/null
pkill -f "monitor_alerts.py" 2>/dev/null

echo ""
echo "🛑 All scanner processes stopped"
echo "📊 Checking remaining processes:"
pgrep -f "memecoin" || echo "✅ No memecoin processes running"
echo ""
echo "💡 To restart: ./start_scanner.sh"