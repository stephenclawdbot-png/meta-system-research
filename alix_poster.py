#!/usr/bin/env python3
"""
Alix X Poster - Browser automation for autonomous posting
Uses AppleScript on macOS to bypass browser automation limitations
"""

import subprocess
import time
import sys
from pathlib import Path

def activate_chrome():
    """Bring Chrome to front and focus."""
    script = '''
    tell application "Google Chrome"
        activate
        delay 0.5
    end tell
    '''
    subprocess.run(['osascript', '-e', script], capture_output=True)

def post_to_x(content):
    """
    Post content to X using Chrome browser automation.
    Assumes X compose page is already open.
    """
    # Bring Chrome to front
    activate_chrome()
    time.sleep(0.5)
    
    # Click the textbox (approximate position of "What's happening?")
    # Then type the content
    script = f'''
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
            delay 0.3
            -- Click in the text area
            click at {{600, 400}}
            delay 0.2
            -- Select all and clear
            keystroke "a" using command down
            keystroke "delete"
            delay 0.2
            -- Type content
            keystroke "{content}"
            delay 0.5
        end tell
    end tell
    '''
    
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    
    if result.returncode != 0:
        return {"status": "error", "error": result.stderr}
    
    return {"status": "text_entered", "content_preview": content[:50] + "..."}

def click_post_button():
    """Click the Post button."""
    script = '''
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
            delay 0.3
            -- Click Post button (lower right area of compose)
            click at {1170, 650}
            delay 0.5
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 alix_poster.py '<tweet content>'")
        sys.exit(1)
    
    content = sys.argv[1]
    
    print(f"Activating Chrome...")
    activate_chrome()
    
    print(f"Typing content...")
    result = post_to_x(content)
    
    if result["status"] == "error":
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    print(f"Content entered. Waiting before posting...")
    time.sleep(1)
    
    print(f"Clicking Post button...")
    if click_post_button():
        print("✅ Posted successfully")
    else:
        print("⚠️  Post button click may have failed")
    
    print(f"\nPosted content preview: {content[:80]}...")

if __name__ == "__main__":
    main()
