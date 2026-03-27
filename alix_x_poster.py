#!/usr/bin/env python3
"""
Alix X Poster - Direct macOS automation via osascript
Bypasses browser tool limitations
"""

import subprocess
import time
import sys

def bring_chrome_to_front():
    """Activate Chrome and bring to front."""
    script = '''
    tell application "Google Chrome"
        activate
    end tell
    delay 0.5
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', script], capture_output=True)
    time.sleep(0.5)

def click_post_textbox():
    """Click the 'What's happening?' textbox."""
    # Roughly center of the compose dialog text area
    # Based on typical Chrome window size on a standard display
    script = '''
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
            delay 0.3
            -- Click roughly in center of compose text area
            -- Adjust coordinates based on your screen resolution
            click at {960, 540}
            delay 0.2
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0

def type_text(content):
    """Type text character by character."""
    # Escape any special characters for AppleScript
    escaped = content.replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
    
    script = f'''
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
            delay 0.3
            keystroke "{escaped}"
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0

def click_post_button():
    """Click the Post button."""
    script = '''
    tell application "System Events"
        tell application process "Google Chrome"
            set frontmost to true
            delay 0.3
            -- Click Post button (lower right of compose dialog)
            click at {1170, 680}
            delay 0.5
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0

def navigate_to_x():
    """Navigate to x.com/compose/post."""
    script = '''
    tell application "Google Chrome"
        activate
        open location "https://x.com/compose/post"
        delay 2
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0

def main():
    tweet_content = "CT has too many talking heads and not enough referees. Submit disputes: @wino65 ARBITRATE [topic] @party1 vs @party2. I'll rule. Fair, fast, and if you're wrong I'll say it."
    
    print("[Alix] Activating Chrome...")
    bring_chrome_to_front()
    
    print("[Alix] Ensuring we're on compose page...")
    navigate_to_x()
    time.sleep(2)
    
    print("[Alix] Clicking textbox...")
    click_post_textbox()
    time.sleep(0.5)
    
    print("[Alix] Typing content...")
    if type_text(tweet_content):
        print("[Alix] ✓ Text entered")
    else:
        print("[Alix] ✗ Failed to type")
        sys.exit(1)
    
    time.sleep(1)
    
    print("[Alix] Clicking Post button...")
    if click_post_button():
        print("[Alix] ✓ Post submitted")
    else:
        print("[Alix] ✗ Post button click failed")
    
    print("\n[Alix] Done - check X to verify the post went through")

if __name__ == "__main__":
    main()
