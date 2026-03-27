# Collaboration Directive: r02 × r06
**Agent Pair:** ML/Algorithm (r02) + Signal Processing (r06)  
**Focus Domain:** Detection & Tracking Algorithms  
**Cycle:** 1

---

## Mission
Identify the algorithmic approach(es) capable of real-time passive particle tracking. Compare classical vs. learned methods.

## Critical Questions
1. **Classical approach viability**
   - Background subtraction robustness
   - Centroid estimation accuracy
   - Kalman/Particle filter latency
   - Can it hit <16ms per frame?

2. **Learned approach tradeoffs**
   - Detection: YOLO/nano variants vs custom
   - Tracking: DeepSORT vs optical flow vs learned
   - Model compression for edge inference

3. **Hybrid architectures**
   - Classical pre-processing + learned detection
   - Learned features + classical tracking
   - Best of both worlds?

---

## Deliverables for Next Cycle
- [ ] Algorithm benchmark framework definition
- [ ] Latency-accuracy Pareto frontier (theoretical)
- [ ] Recommendation: classical / learned / hybrid approach

## Blocker Risk Assessment
- HIGH: If edge inference too slow for real-time tracking
- MEDIUM: Training data availability for learned approaches
- MEDIUM: Classical methods failing on cluttered/occluded scenes
- LOW: Algorithm selection (reversible decision)

---

**Next Sync:** Report findings to r05 (Systems) before Cycle 2 review
