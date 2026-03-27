# Collaboration Directive: r01 × r03
**Agent Pair:** Vision/Optics (r01) + Hardware/Physics (r03)  
**Focus Domain:** Optical System Feasibility & Sensor Physics  
**Cycle:** 1

---

## Mission
Define the physical boundaries of passive particle detection. What can we actually see without active illumination?

## Critical Questions
1. **What is the minimum particle size detectable under ambient lighting?**
   - Scatter cross-section calculations
   - Ambient photon budget
   - Sensor SNR requirements

2. **Which wavelength bands maximize passive detection?**
   - Visible vs near-IR ambient
   - Contrast against background
   - Sensor sensitivity curves

3. **Lens/optics tradeoffs for sub-pixel accuracy**
   - Depth of field vs numerical aperture
   - Diffraction limits
   - Aberration impact on centroid calculation

---

## Deliverables for Next Cycle
- [ ] Photon budget calculation for 1μm, 10μm, 100μm particles
- [ ] Recommended sensor specifications (QE, pixel pitch, noise floor)
- [ ] Optical configuration matrix (tradeoff table)

## Blocker Risk Assessment
- HIGH: If ambient photon budget insufficient → requires active illumination pivot
- MEDIUM: If sensor requirements exceed edge compute cost targets
- LOW: Optical complexity

---

**Next Sync:** Report findings to r05 (Systems) before Cycle 2 review
