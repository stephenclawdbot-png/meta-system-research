# COLLABORATION DIRECTIVE: R01 (Physics) + R03 (Optics)
**Cycle 2 Mission: Distributed Scanning System Design**

---

## Objective
Design the distributed laser scanning system to activate passive retroreflective particles in the AETHER-S (Sparse) configuration.

---

## Background from Cycle 1

**The Problem:** Single-emitter voxel addressing rate is 60,000x too slow for 1M voxels.
**The Solution:** Distributed array of low-power emitters, each covering subset of volume.

**New Targets for AETHER-S:**
- 100K effective voxels (down from 1M)
- 30Hz refresh (down from 60Hz, persistence of vision acceptable)
- 3.3M voxels/sec system-wide (down from 60M)
- Per-emitter target: ~33K voxels/sec with 100 emitters

---

## Your Collaboration Tasks

### R01 (Physics Lead): Beam Physics & Safety

**Task 1: Power Density Analysis**
- Given: Passive retroreflective particles with reflectivity R
- Calculate: Minimum irradiance at particle to achieve visible reflected light
- Consider: Ambient room lighting (~100-500 lux) as baseline
- Constraint: Must stay Class 1 eye-safe for reflected beams

**Task 2: Beam Divergence & Coverage**
- Calculate: Beam divergence needed to cover room volume from perimeter
- Trade-off: Narrow beam = better resolution but needs more emitters
- Room dims: 4m × 4m × 2.5m (40m³)

**Task 3: Interference & Cross-Talk**
- Multiple beams may intersect at same voxel
- Analyze: Interference patterns, potential constructive/destructive effects
- Propose: Synchronization scheme or wavelength multiplexing to avoid interference

**Deliverable:** Power budget per emitter with safety margins

---

### R03 (Optics Lead): Scanning & Voxel Addressing

**Task 1: Scanning Architecture**
- Design: Mirror galvanometer vs MEMS vs acousto-optic deflectors
- Compare: Speed, precision, cost, reliability
- Target: 33K voxels/sec per emitter with 100×100 raster

**Task 2: Voxel Overlap Strategy**
- Multiple emitters see same particle from different angles
- Design: Time-division vs wavelength-division multiplexing
- Goal: Smooth voxel appearance without flicker from handoff between emitters

**Task 3: Calibration & Tracking**
- Each emitter needs to know where particles are
- Propose: Initial calibration scan + periodic recalibration
- Consider: Passive particles don't emit—how to detect them?
  - Options: Impulse response, coherent detection, reference grid

**Deliverable:** Emitter specifications and scanning pattern algorithms

---

## Joint Deliverables

### 1. Emitter Array Configuration
**Question:** How many emitters minimum?
**Parameters:**
- Room: 4m × 4m × 2.5m
- Target: 100K voxels at 30Hz
- Each emitter: ? kHz scan rate

**To Calculate:**
```
Emitters needed = (Total voxels × Refresh rate) / (Emitter scan rate)
```

Example: If each emitter can scan at 50kHz (50,000 voxels/sec):
- Required system rate: 3,000,000 voxels/sec
- Emitters needed: 3,000,000 / 50,000 = 60 emitters

**Target output:** Emitter placement map (ceiling perimeter positions)

---

### 2. Safety Protocol Specification
**Joint Responsibility**

Even with Class 1 reflected light, multiple beam intersection could create hotspots.

**Define:**
- Maximum simultaneous beams at single voxel: ?
- Emergency shutdown triggers
- Viewer position detection (eye safety distance)

---

### 3. Scan Synchronization Protocol
**How do 100 emitters coordinate without complex wiring?**

**Options to evaluate:**
1. **GPS-like timing:** All emitters synchronized to central clock via distributed protocol
2. **Leader-follower:** One emitter drives timing, others follow with known latency
3. **Asynchronous with collision detection:** Random access with retry on interference
4. **Precomputed frames:** Each emitter has full knowledge of frame, acts independently

**Recommend:** Best approach for 100-emitter scale

---

## Design Constraints

| Parameter | Constraint | Source |
|-----------|-----------|--------|
| Eye safety | Class 1 | IEC 60825-1 |
| Latency | <50ms end-to-end | R04 perceptual requirements |
| Cost per emitter | <$100 | Practical deployment |
| Power per emitter | <10W | 100 emitters = 1kW total budget |
| Room intrusion | Minimal | Aesthetic requirement |

---

## Success Criteria

✅ Emitter count determined (target: 50-200 range)  
✅ Per-emitter specifications defined  
✅ Scanning pattern algorithm specified  
✅ Safety analysis complete  
✅ Cost estimate per emitter  

---

## Questions for R02/R06

**Before finalizing:**
- What is actual retroreflector efficiency? (need R02 data)
- How stable are acoustic pressure nodes? (need R02 data)
- Can emitters be wirelessly powered? (need R06 data)

**Deliver findings to:** CYCLE_LOG.md (update with "R01-R03 Results")

**Time limit:** 15 minutes (Cycle 2 duration)
