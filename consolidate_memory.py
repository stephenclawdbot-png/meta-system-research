#!/usr/bin/env python3
"""
Memory Consolidation Script
Periodically moves insights from daily logs to long-term memory
"""

import os
import glob
import json
from datetime import datetime, timedelta

def load_file(path):
    """Load a file's content"""
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return ""

def save_file(path, content):
    """Save content to file"""
    with open(path, 'w') as f:
        f.write(content)

def consolidate_memory():
    """Run memory consolidation process"""
    
    # Get recent daily logs (last 7 days)
    today = datetime.now().strftime("%Y-%m-%d")
    log_files = glob.glob("logs/daily_log_*.md")
    recent_logs = []
    
    for log_file in log_files:
        # Extract date from filename
        try:
            date_str = log_file.split("_")[-1].replace(".md", "")
            log_date = datetime.strptime(date_str, "%Y-%m-%d")
            if datetime.now() - log_date < timedelta(days=7):
                recent_logs.append(log_file)
        except:
            pass
    
    # Load current memory
    current_memory = load_file("memory.md")
    
    # Consolidation prompt (would be sent to LLM in full implementation)
    consolidation_prompt = f"""
You are a memory consolidation agent. Review these daily logs: {recent_logs}

Current long-term memory:
{current_memory}

Your job:
1. Extract new facts about the user worth remembering
2. Identify patterns that appeared more than once  
3. Note any decisions or preferences stated
4. Discard redundant or trivial details

Output: Updated sections to ADD to memory.md only. Do not repeat what's already there.
"""
    
    print("Consolidation prompt ready:")
    print("-" * 50)
    print(consolidation_prompt)
    print("-" * 50)
    print("\nIn full implementation, this would be sent to an LLM for processing.")

if __name__ == "__main__":
    consolidate_memory()