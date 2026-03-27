# META-SYSTEM Heartbeat Guide
## What To Do Every 5 Minutes

### Step 1: Load State (30 seconds)
Read these files IN ORDER:
1. `PROJECT_REGISTRY.json` — Current project statuses
2. `REVOLUTION_TRACKS.md` — Cross-project context
3. Each active project's documentation

### Step 2: Check Project Health (60 seconds)
For each active project:
- Is the critical blocker still blocking?
- Has new insight emerged that changes feasibility?
- Should status change (validating → documenting → prototyping)?

### Step 3: Advance Each Project (90 seconds)
**AETHER:** Cycle 2 → Cycle 3
- Focus: Particle tracking solution
- If solved: Move to documenting, create repo
- If unsolvable: Consider abandonment

**SILENT:** Cycle 0 → Cycle 1
- Focus: Hardware acquisition, testbed build
- Create GitHub repo (when token fixed)
- Order components

**Slot C:** Generate new concept
- What simple thing should exist but doesn't?
- 15-minute ideation sprint
- If promising: Initialize as new project

### Step 4: Generate Documentation (60 seconds)
- Update PROJECT_REGISTRY.json
- Write cycle summaries to project docs
- Commit to git

### Step 5: Public Updates (30 seconds)
- Post breakthroughs to X (@wino65)
- Update GitHub repos
- Notify user of major milestones

### Decision Matrix

| Situation | Action |
|-----------|--------|
| Project stuck >3 cycles | Abandon or pivot |
| Breakthrough achieved | Advance phase |
| Slot C filled | Wait for graduation |
| All 3 slots blocked | Escalate to user |
| Auto-rotation | >8h inactive → new idea |

### Memory Persistence
ALWAYS update:
- PROJECT_REGISTRY.json (current state)
- CYCLE_LOG.md (history)
- Individual project docs (technical details)

### Never Forget
- Document WHY decisions were made
- Link to sources and papers
- Record BOM changes
- Note failed approaches

---

*This heartbeat runs you. Follow it. Iterate. Ship.*
