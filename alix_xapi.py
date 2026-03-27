#!/usr/bin/env python3
"""
X/Twitter API Integration for Alix CT Overseer
Authentication and posting layer
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# X API v2 endpoints
X_API_BASE = "https://api.twitter.com/2"

class XAPI:
    """
    X API v2 wrapper for Alix CT Overseer.
    
    Free Tier (Essential Access) limits:
    - 500 tweets per month
    - 5000 mentions timeline requests per month
    - OAuth 2.0 App-only or OAuth 1.0a User Context
    
    Free tier cannot post tweets via API — requires Basic ($100/mo).
    Alternative: Use browser automation for free posting.
    """
    
    def __init__(self):
        self.credentials = self._load_credentials()
        self.client = None
    
    def _load_credentials(self):
        """Load credentials from environment or 1Password."""
        return {
            "username": os.getenv("WINO65_USERNAME", "wino65"),
            "password": os.getenv("WINO65_PASSWORD"),  # Will prompt if not set
            "bearer_token": os.getenv("WINO65_BEARER_TOKEN"),
            "api_key": os.getenv("WINO65_API_KEY"),
            "api_secret": os.getenv("WINO65_API_SECRET"),
        }
    
    def check_access_level(self):
        """
        Determine what operations are available.
        Free tier: read-only for mentions
        Basic tier: posting allowed
        """
        if self.credentials["bearer_token"]:
            return "essential"  # Can read mentions
        if self.credentials["api_key"] and self.credentials["api_secret"]:
            return "elevated"  # May allow posting depending on tier
        return "none"
    
    def simulate_post(self, content, reply_to=None):
        """
        In SUGGEST mode, we don't actually post.
        This method simulates what WOULD be posted.
        """
        return {
            "status": "simulated",
            "content": content,
            "reply_to": reply_to,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "note": "SUGGEST mode enabled. Content queued for human approval before posting."
        }
    
    def fetch_mentions(self, since_id=None):
        """Fetch recent mentions of @wino65."""
        # TODO: Implement actual API call
        # Requires: GET /2/users/:id/mentions
        # Need user ID first via GET /2/users/by/username/wino65
        return []


def check_setup():
    """Check if X API is configured properly."""
    api = XAPI()
    level = api.check_access_level()
    
    print(f"X API Access Level: {level}")
    print(f"\nCredentials loaded:")
    print(f"  Username: {api.credentials['username']}")
    print(f"  Bearer token: {'✓ Set' if api.credentials['bearer_token'] else '✗ Missing'}")
    print(f"  API key: {'✓ Set' if api.credentials['api_key'] else '✗ Missing'}")
    print(f"  API secret: {'✓ Set' if api.credentials['api_secret'] else '✗ Missing'}")
    
    if level == "essential":
        print("\n⚠️  Essential tier detected (free)")
        print("   - Can READ mentions")
        print("   - Cannot POST tweets via API")
        print("   - For autonomous posting, need Basic tier ($100/mo)")
        print("   - Alternative: Browser automation for manual posting")
    
    return level


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: alix_xapi.py <command>")
        print("Commands: check, simulate_post")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check":
        check_setup()
    
    elif cmd == "simulate" and len(sys.argv) >= 3:
        api = XAPI()
        result = api.simulate_post(content=sys.argv[2])
        import pprint
        pprint.pprint(result)
