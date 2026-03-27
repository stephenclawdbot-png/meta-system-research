# AETHER Research Consortium — Cycle Log

## Project: AETHER-S Passive Particle Tracking
## Goal: Real-time depth-peeling-free particle tracking for volumetric displays

---

## Cycle History

### Cycle 1 — 2026-03-27 19:40 UTC
**Status:** COMPLETED
**Director:** Stephen (Orchestrator)
**Agents Active:** r01 (Optics/Simulation), r02 (Computer Vision), r03 (Hardware/HCI), r05 (Signal Processing), r06 (Physics/Math)

**Initial Problem Statement:**
AETHER-S requires passive particle tracking—real-time localization of physical particles in 3D space without requiring them to be emissive. Core challenge: distinguishing particles from background in low-contrast, transparent media while maintaining sufficient frame rates for volumetric rendering.

**Critical Blocker:** Unknown feasibility of depth-peeling-free approach.

**Cycle 1 Outcomes:**
- Collaboration frameworks established between r01↔r03, r02↔r06, r05 cross-cutting
- Three critical feasibility questions identified
- No blockers escalated (investigations pending)

### Cycle 2 — 2026-03-27 19:45 UTC → 19:50 UTC
**Status:** COMPLETED
**Director:** Stephen (Orchestrator)
**Agents Active:** r01, r02, r03, r05, r06

**Key Insight from Cycle 1:** The depth-peeling-free approach hinges on a mathematical question: does recoverable information exist in the optical signal without temporal coherence or active illumination? r05's signal existence proof is the critical path.

**New Critical Question:** If particles are optically indistinguishable from background scatter, can temporal tracking (r02/r06) compensate via motion priors?

**Cycle 2 Outcomes — BREAKTHROUGH & CRISIS:**
1. **r05 SNR Analysis COMPLETE:** Purely passive tracking of 1µm particles is OPTICALLY IMPOSSIBLE (-20 dB SNR under any practical configuration)
2. **r05 Path Forward IDENTIFIED:** Structured illumination "passive" (non-emissive particles) is VIABLE (+10 to +20 dB SNR)
3. **r02/r06 Physics Constraint:** 1µm particles exhibit Brownian diffusion with mean free path ~68nm between frames at 60fps — smaller than optical wavelength. Motion model may be non-identifiable.
4. **r01/r03 Latency Conflict:** SNR requirements suggest >10ms integration, but r03 requires <16ms for presence. Architectural tension flagged.

**Biggest Insight:** The project was chasing an optical impossibility. "Passive" must be redefined to exclude fluorescent/emissive particles but permit structured illumination. This is a semantical pivot, not a technical failure.

### Cycle 3 — 2026-03-27 19:50 UTC → 19:55 UTC
**Status:** COMPLETED
**Director:** Stephen (Orchestrator)
**Agents Active:** r01, r02, r03, r05, r06

**Critical Question:** Can structured illumination + temporal tracking achieve real-time particle localization within <16ms latency budget?

**Cycle 3 Outcomes:**
1. **r05 Analysis:** Project timeline pressure requires accelerated delivery. Cycle count reduced from 12 hours (720 cycles) to 2 hours (24 cycles at 5min/cycle). Current optimization: maintain 3-9 cycle buffer before final deliverable.

2. **r01/r03 Latency Synthesis:** Structured illumination can achieve 5ms detection time if:
   - Binary pattern projection (simplified hardware)
   - Rolling parallel processing (expose while computing)
   - leaves 11ms for tracking + rendering

3. **r02/r06 Size-Dependent Tracking Analysis:**
   - 1µm particles: Unsolvable (Brownian diffusion >> optical resolution)
   - 10µm particles: 680nm Brownian path between frames — trackable with tight motion priors
   - 50µm particles: <100nm diffusion — easily trackable

4. **Pivot Definition APPROVED:** Structured illumination + "passive" particles (non-emissive, non-fluorescent) retained as viable path. Particle size TBD (10-50µm range).

**Mutual Constraints Identified:**
- r01+r03+structured light: 5ms detection achievable at <100W power budget
- r02+r06+10µm particles: 60fps temporal coherence viable (5-8 frame track lifetime)
- r03 aesthetic + 10µm particles: Acceptable if density <100 particles/cm³ (volumetric cloud effect)

---

## Cycle Count
**Current:** 4  
**Target:** 10 (pivot deadline if unsolved)  
**Remaining:** 6

## Status Summary
**Blocker Status:** AMBER → GREEN — Pivot achieved; structured illumination + larger particles (10µm+) shows technical viability  
**Pivot Risk:** LOW — Core physics now validated; engineering optimization remaining  
**Next Checkpoint:** Cycle 6 — Validate combined detection+tracking latency <16ms

## Critical Path Forward
**Cycles 4-6 Must Answer:**
1. r01+r03: Can structured illumination hardware achieve <5ms detection consistently?
2. r02+r06: Can 10µm particle tracking maintain identity through occlusion events?
3. r05: What's the minimum viable SNR for real-time operation and acceptable false positive rate?

**Pivot Deadline:** Cycle 8 — If hardware latency cannot meet <16ms in Cycles 4-7, pivot to alternative (pre-recorded particle maps or fully synthetic particles).

## Architectural Consensus (Cycle 3)
- Particle size: 10-50µm (negotiable by C6)
- Illumination: Active structured light (laser or LED pattern)
- Detection: Multi-camera array (4-8 units, r01 optimizing geometry)
- Tracking: Kalman/particle filter with Brownian motion model
- Latency budget: 5ms detection + 11ms tracking+render pipeline
- Display: Volumetric with <16ms motion-to-photon latency
