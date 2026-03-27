# Collaboration Directive: r05
**Agent:** Systems Integration Lead (r05)  
**Focus Domain:** System Architecture & Integration  
**Cycle:** 1

---

## Mission
Map the integration landscape. Identify bottlenecks before they become blockers.

## Critical Questions
1. **Hardware platform constraints**
   - Target compute (Jetson? Coral? Custom?)
   - Memory bandwidth limits
   - Power/thermal ceiling
   - Camera interface (MIPI/CSI/GigE/USB3)

2. **Pipeline latency breakdown**
   - Sensor readout time
   - Transfer to compute
   - Processing time
   - Output/action latency
   - Where is the 16ms budget spent?

3. **Integration risks**
   - Camera driver stability
   - Real-time OS requirements
   - Debugging/monitoring capabilities
   - Manufacturing repeatability

---

## Deliverables for Next Cycle
- [ ] Reference hardware platform recommendation
- [ ] Latency budget allocation spreadsheet
- [ ] Top 3 integration risk mitigations

## Blocker Risk Assessment
- HIGH: If total latency >16ms with any candidate hardware
- MEDIUM: Memory bandwidth insufficient for full-frame processing
- LOW: Driver/integration issues (solvable with time)

---

## Cross-Team Coordination
**Receives from:**
- r01+r03: Optical/sensor requirements → hardware selection
- r02+r06: Algorithm compute requirements → platform validation

**Provides to:**
- All teams: Feasibility feedback on proposed approaches

---

**Next Sync:** Cycle 2 review — synthesize all inputs into go/no-go for optical+algorithmic approach
