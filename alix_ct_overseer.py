#!/usr/bin/env python3
"""
Alix CT Overseer - Autonomous Dispute Resolution for Crypto Twitter
Account: @wino65
Mode: SUGGEST (human review required)
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuration
MEMORY_FILE = Path(__file__).parent / "memory" / "alix-ct-overseer.json"
LOG_FILE = Path(__file__).parent / "memory" / "alix-ct-overseer.log"
CREDENTIALS = {
    "username": "wino65",
    "password": None  # Loaded from 1Password at runtime
}

class CTOverseer:
    def __init__(self):
        self.memory = self._load_memory()
        self.mode = self.memory.get("account", {}).get("mode", "suggest")
    
    def _load_memory(self):
        """Load dispute tracking memory."""
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE) as f:
                return json.load(f)
        return self._init_memory()
    
    def _init_memory(self):
        """Initialize fresh memory structure."""
        return {
            "system_version": "1.0.0-ct-overseer",
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "account": {
                "handle": "wino65",
                "platform": "x",
                "mode": "suggest"
            },
            "disputes": {"active": [], "resolved": [], "stats": {}},
            "ruling_queue": {
                "pending_approval": [],
                "approved": [],
                "rejected": [],
                "auto_posted": []
            }
        }
    
    def _save_memory(self):
        """Persist memory to disk."""
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def _log(self, event, data=None):
        """Log system event."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "data": data
        }
        self.memory.setdefault("logs", []).append(entry)
        self._save_memory()
    
    def intake_dispute(self, topic, party1, party2, context, source_tweet=None):
        """
        Register a new dispute for arbitration.
        
        Format: "@wino65 ARBITRATE [topic] [party1] vs [party2] [context]"
        """
        case_id = f"CT-{datetime.now().strftime('%Y%m%d')}-{len(self.memory['disputes']['active']) + 1:03d}"
        
        dispute = {
            "case_id": case_id,
            "topic": topic,
            "party1": {"handle": party1, "position": None},
            "party2": {"handle": party2, "position": None},
            "context": context,
            "source": source_tweet,
            "status": "pending_review",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "deadline": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
            "evidence": [],
            "ruling": None
        }
        
        self.memory["disputes"]["active"].append(dispute)
        self._log("dispute_intake", {"case_id": case_id, "topic": topic})
        self._save_memory()
        
        return {
            "status": "received",
            "case_id": case_id,
            "acknowledgment": f"Case {case_id} received. Analyzing evidence. Ruling within 24h.",
            "mode": self.mode
        }
    
    def draft_ruling(self, case_id):
        """
        Draft a ruling for a dispute.
        In SUGGEST mode, queues for human approval.
        """
        for dispute in self.memory["disputes"]["active"]:
            if dispute["case_id"] == case_id:
                # TODO: Implement actual analysis
                # For now, placeholder ruling structure
                
                ruling = {
                    "case_id": case_id,
                    "drafted_at": datetime.now(timezone.utc).isoformat(),
                    "tweet_draft": f"Ruling on {dispute['topic']}: [Analysis pending]",
                    "thread_draft": ["Full reasoning: [pending evidence review]"],
                    "confidence": 0.0,  # Will be calculated
                    "sources": [],
                    "escalation_level": "yellow",  # Always queue in SUGGEST mode
                    "status": "pending_approval"
                }
                
                dispute["ruling"] = ruling
                self.memory["ruling_queue"]["pending_approval"].append(ruling)
                self._log("ruling_drafted", {"case_id": case_id, "confidence": ruling["confidence"]})
                self._save_memory()
                
                return ruling
        
        return None
    
    def list_pending_rulings(self):
        """List all rulings awaiting human approval."""
        return self.memory["ruling_queue"]["pending_approval"]
    
    def approve_ruling(self, case_id, modifications=None):
        """Human approves a ruling for posting."""
        for ruling in self.memory["ruling_queue"]["pending_approval"]:
            if ruling["case_id"] == case_id:
                ruling["status"] = "approved"
                ruling["approved_at"] = datetime.now(timezone.utc).isoformat()
                ruling["modifications"] = modifications
                
                self.memory["ruling_queue"]["approved"].append(ruling)
                self.memory["ruling_queue"]["pending_approval"].remove(ruling)
                
                self._log("ruling_approved", {"case_id": case_id})
                self._save_memory()
                
                return {
                    "status": "approved",
                    "action": "ready_to_post",
                    "tweet": ruling["tweet_draft"]
                }
        
        return None
    
    def reject_ruling(self, case_id, reason):
        """Human rejects a ruling."""
        for ruling in self.memory["ruling_queue"]["pending_approval"]:
            if ruling["case_id"] == case_id:
                ruling["status"] = "rejected"
                ruling["rejected_at"] = datetime.now(timezone.utc).isoformat()
                ruling["rejection_reason"] = reason
                
                self.memory["ruling_queue"]["rejected"].append(ruling)
                self.memory["ruling_queue"]["pending_approval"].remove(ruling)
                
                self._log("ruling_rejected", {"case_id": case_id, "reason": reason})
                self._save_memory()
                
                return {"status": "rejected", "case_id": case_id}
        
        return None
    
    def get_status(self):
        """Get current system status."""
        return {
            "mode": self.mode,
            "account": self.memory["account"]["handle"],
            "pending_disputes": len(self.memory["disputes"]["active"]),
            "pending_approval": len(self.memory["ruling_queue"]["pending_approval"]),
            "total_resolved": len(self.memory["disputes"]["resolved"]),
            "api_status": self.memory["account"].get("api_status", "unknown")
        }


def main():
    overseer = CTOverseer()
    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command> [args...]")
        print("Commands: status, intake, draft, pending, approve, reject")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        import pprint
        pprint.pprint(overseer.get_status())
    
    elif cmd == "intake" and len(sys.argv) >= 6:
        # intake <topic> <party1> <party2> <context...>
        result = overseer.intake_dispute(
            topic=sys.argv[2],
            party1=sys.argv[3],
            party2=sys.argv[4],
            context=" ".join(sys.argv[5:])
        )
        import pprint
        pprint.pprint(result)
    
    elif cmd == "pending":
        rulings = overseer.list_pending_rulings()
        print(f"Pending rulings: {len(rulings)}")
        for r in rulings:
            print(f"  - {r['case_id']}: {r['tweet_draft'][:50]}...")
    
    elif cmd == "approve" and len(sys.argv) >= 3:
        # approve <case_id> [modifications...]
        mods = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = overseer.approve_ruling(sys.argv[2], modifications=mods)
        import pprint
        pprint.pprint(result)
    
    else:
        print(f"Unknown or incomplete command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
