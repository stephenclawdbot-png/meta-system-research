#!/bin/bash
# Alix CT Overseer - Master Script
# Runs all monitoring and posting cycles

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check for X mentions (every 10 min)
monitor_mentions() {
    log "Monitoring X mentions..."
    python3 "$SCRIPT_DIR/alix_xapi.py" check 2>/dev/null || true
}

# Process dispute queue
process_disputes() {
    log "Processing dispute queue..."
    python3 "$SCRIPT_DIR/alix_ct_overseer.py" status
}

# Post from queue (requires browser automation)
post_content() {
    log "Posting from queue..."
    # This will use browser automation when available
}

# Main execution
case "$1" in
    monitor)
        monitor_mentions
        ;;
    process)
        process_disputes
        ;;
    post)
        post_content
        ;;
    full)
        monitor_mentions
        process_disputes
        post_content
        ;;
    *)
        echo "Usage: $0 {monitor|process|post|full}"
        exit 1
        ;;
esac
