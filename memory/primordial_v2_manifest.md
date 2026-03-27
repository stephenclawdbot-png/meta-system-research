# PRIMORDIAL v2.0 - Multiscale Genetic Life System
**Created:** 2026-03-28 04:18 GMT+8

## Architecture Overview

PRIMORDIAL v2.0 introduces **multi-scale emergent simulation**:

| Scale | Entity | Time Step | Key Processes |
|-------|--------|-----------|---------------|
| **MICRO** | Cells/Organelles | Milliseconds | Protein synthesis, ATP production, membrane potentials |
| **MESO** | Tissues | Seconds | Cell signaling, differentiation, morphogenesis |
| **MACRO** | Organisms | Minutes | Metabolism, reproduction, CRISPR warfare |
| **ECO** | Ecosystems | Hours | Competition, speciation, mass extinction events |

## Design Philosophy

**Emergence through composition:**
- MICRO processes produce emergent MACRO behaviors
- No hand-coded organism traits - everything emerges from biochemistry
- Genes code for proteins → proteins form pathways → pathways enable functions

## Key Innovations

### 1. Real Biochemistry (Not Abstracted)
- 20 amino acids, folded into functional proteins
- Central dogma: DNA → RNA → Protein → Function
- ATP as energy currency (not abstract "health")
- Metabolic pathways (glycolysis, Krebs) emerge from protein interactions

### 2. Cellular Automata + Systems Biology
- Each cell = agent with internal state
- Neighboring cells exchange signals
- Tissues self-organize through morphogen gradients

### 3. Genetic Regulatory Networks
- Genes have promoters, enhancers, repressors
- Transcription factors bind to regulatory sequences
- Network topology evolves, creating new cell types

## Implementation Plan

1. **Core Biochemistry** - Implement protein folding simulation
2. **Cell Agent** - Internal metabolism, division, death
3. **Tissue Layer** - Spatial organization, signaling
4. **Integration Layer** - Connect to v1.0 organisms
5. **Emergence Observation** - Automated analysis

## Memory References
- Local path: `/Users/clawdbot/.openclaw/workspace/primordial/`
- GitHub repo: awaiting push
- Status: v1.0 complete, v2.0 in development
