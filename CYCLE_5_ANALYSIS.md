# AETHER Research Consortium — Cycle 5 Analysis
## Date: 2026-03-27 20:10 UTC (Cycle 4→5 Transition)

---

## Cycle Number: 5 of 10
**Status:** ACTIVE — Compute Architecture Critical Path
**Pivot Risk:** LOW-MEDIUM

---

## What's Working

1. **Physics is SOLVED** — r05 validated SNR requirements across all hardware tiers (12/18/22 dB). The signal exists and is recoverable.

2. **Structured illumination validated** — The redefinition of "passive" to permit structured light (while excluding emissive particles) was the correct pivot. All sensor physics checks pass.

3. **Particle size consensus** — 10µm particles are trackable with Brownian motion model; 50µm are trivial. The 10-50µm range is viable.

4. **Hardware tiers defined** — $2K/$10K/$50K options all validated. Procurement paths are clear.

5. **Detection latency achievable** — 5ms capture + 1-2ms decode is within reach on modern GPUs.

---

## What's Breaking

1. **Serial latency exceeds budget** — 5 + 2 + 10 + 1 = 18ms exceeds the 16ms target (Cycle 4 status shows this clearly).

2. **Tracking compute is the new bottleneck** — r02/r06 identified O(N²) correspondence matching as problematic. At 500 particles, Hungarian algorithm becomes computationally prohibitive.

3. **Pipelining is MANDATORY, not optional** — Frame N detection MUST overlap with Frame N-1 tracking to stay under 16ms. This creates data dependency risks.

4. **Density vs. latency trade-off unresolved** — Maximum particle count for <10ms tracking is still unknown. Could be as low as 200 particles, forcing aesthetic compromises.

5. **GPU vs. FPGA decision pending** — r03 must decide if GPU kernels can achieve 5ms detection + 1ms decode, or if FPGA becomes mandatory (adds 2-week procurement penalty).

---

## Refinement or Pivot

**REFINEMENT (not pivot)** — The physics works. This is an engineering optimization problem now, not a fundamental impossibility.

**Refinement Plan:**
- Shift from "can it work?" → "how fast can it run?"
- aggressive kernel optimization for pattern decode
- parallelize detection and tracking (pipelined architecture)
- set density limits based on compute constraints (not physics)

**Fallback if Cycle 7 fails:** Reduced-density configuration (100-200 particles) OR pre-cached particle maps (non-real-time fallback).

---

## New Agent Collaborations Needed

**Current Collaborations (continuing):**
- r01↔r03 — Compute pipeline validation
- r02↔r06 — Tracking algorithm complexity
- r05 — System integration and cross-cutting analysis

**Cycle 5 Does NOT require new collaborations.** The existing structure is correct; we need execution, not reorganization.

**Cycle 7 may spawn:**
- r01+r05 — Detection-to-tracking interface specification
- r03+r06 — Real-time OS bypass techniques (if GPU overhead persists)

---

## Biggest Insight

**We traded an impossible problem for a hard engineering problem.** 

Cycle 1-2 faced optical impossibility (-20 dB SNR). Cycle 3-4 established viability (+18 dB SNR with structured light). Cycle 5-7 must now optimize the compute pipeline. The risk profile dropped from "physics may not permit this" to "can we code fast enough."

This is the best possible outcome for Cycle 5.

---

## Next Critical Question

**Can GPU-based tracking achieve <10ms for 200-500 particles, or does the density need to be capped?**

This determines:
- Whether FPGA is optional or mandatory (r03 procurement)
- Maximum aesthetic density (r03 user experience)
- Whether pipelining is sufficient or full parallelization needed (r05 architecture)

---

## Cycle 5 Deliverables Checklist

- [ ] r03: GPU latency breakdown (capture → decode → output)
- [ ] r01: Pattern decode algorithm benchmark (O(N) vs O(N log N))
- [ ] r02/r06: Maximum particle count for <10ms tracking on RTX 4090
- [ ] r05: Pipelined vs sequential latency model validation
- [ ] Director: Go/No-Go for GPU-first strategy (or FPGA pivot)

---

## Status Summary
**Blocker Status:** 🟡 YELLOW — Compute architecture is critical path
**Pivot Risk:** LOW — Engineering problem, not physics impossibility
**Next Checkpoint:** Cycle 7 — Validate <12ms end-to-end on representative hardware

---

*Reported by: Stephen (AETHER Research Consortium Director)*
*Timestamp: 2026-03-27 20:10 UTC*
