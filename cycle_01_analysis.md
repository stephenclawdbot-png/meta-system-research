# Cycle 1 Analysis — AETHER Research Consortium

**Date:** 2026-03-27 19:40 UTC  
**Cycle:** 1/10  
**Director:** Stephen

---

## What's Working
- **Framework established:** All 3 collaboration directives instantiated and scoped
- **Agent roles clear:** r01 (Optics), r02 (CV), r03 (Hardware), r05 (Signal), r06 (Physics/Math)
- **Blocker identified:** Depth-peeling-free tracking feasibility is the critical path

## What's Breaking
- **No empirical data yet:** All analysis theoretical
- **Cascading uncertainty:** SNR feasibility → motion model → GPU real-time constraints
- **Ambitious target:** <16ms latency for volumetric presence requires sub-frame processing

## Refinement or Pivot
**Refinement.** Too early to pivot. Need:
1. r05 SNR feasibility proof (Cycle 2)
2. r01/r03 hardware-optics trade study (Cycle 2)
3. r02/r06 motion model requirements (Cycle 2)

If SNR infeasible → pivot to active particle tracking (fluorescent/doped)
If motion model requires full CFD → pivot to physics-lite approach (correlation tracking)

## New Agent Collaborations Needed
Cycle 2 spawns:
- **r05 → r01/r03:** Hardware SNR → optical design feedback loop
- **r02 → r06:** Kalman filter architecture meeting
- **All hands:** Feasibility checkpoint at Cycle 3

---

## Critical Question for Cycle 2
**"What is the minimum scattering cross-section detectable with $5K hardware budget at 30fps?"**

Cycles to pivot decision: 8 remaining (deadline: Cycle 10)
