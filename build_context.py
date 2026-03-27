#!/usr/bin/env python3
"""
Context Injection Script
Builds agent context in proper order: soul > memory > short_term > daily_log
"""

import os
from datetime import datetime

def load_file(path):
    """Load a file's content"""
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return "# File not found: " + path

def build_context():
    """Build the full context for agent startup"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    daily_log_path = f"logs/daily_log_{today}.md"
    
    context_parts = [
        "## 🧠 AGENT CONTEXT - Loaded in Order",
        "",
        "### [LAYER 1] SOUL - Identity (Immutable)",
        load_file("soul.md"),
        "",
        "### [LAYER 2] PERSONALITY - Learned Expression (Slow Evolving)",
        load_file("personality.md"),
        "",
        "### [LAYER 3] MEMORY - Long-term Knowledge (Stable)",  
        load_file("memory.md"),
        "",
        "### [LAYER 4] SHORT-TERM - Session Focus (Dynamic)",
        load_file("short_term.md"),
        "",
        "### [LAYER 5] DAILY LOG - Today's Raw Events",
        load_file(daily_log_path),
        "",
        "## 🎯 ACTIVE CONTEXT COMPLETE"
    ]
    
    return "\n---\n".join(context_parts)

if __name__ == "__main__":
    print(build_context())