# PRIMORDIAL v2.0 - Complete System Documentation
**Date:** 2026-03-28 04:21 GMT+8  
**GitHub:** https://github.com/stephenclawdbot-png/primordial  
**Status:** ✅ SHIPPED

---

## What Was Built

**PRIMORDIAL** is a multi-scale genetic life simulation system with four interconnected levels:

### 1. MICRO Scale: Biochemistry
**File:** `primordial_micro.py`

- **20 amino acids** with hydrophobicity scores
- **Central dogma:** DNA → RNA → Protein → Function
- **Protein folding:** Monte Carlo simulation of 3D structure
- **Emergent function:** Enzyme, structural, signaling, TF based on fold
- **Metabolism:** ATP/ADP cycles, glycolysis, Krebs (simplified)
- **Gene expression:** Promoters, enhancers, repressors, TFs bind to sequences

### 2. MESO Scale: Tissue Organization  
**File:** `primordial_meso.py`

- **Spatial cells:** 3D positioning, neighbors
- **Morphogen gradients:** French flag pattern formation
- **Cell division:** Asymmetric, with daughter displacement
- **Differentiation:** Wnt signaling determines fate by position
- **Homeostasis:** Density-dependent apoptosis

### 3. MACRO Scale: Organisms
**File:** `primordial_multiscale.py`

- **Multi-tissue organisms:** Epidermis, muscle, neural
- **Emergent health:** Derived from cellular ATP + cell count
- **No hardcoded traits:** Everything from biochemistry

### 4. ECO Scale: Ecosystems
**File:** `ecosystem.py` (v1.0, still works as compatibility layer)

- **CRISPR warfare:** Guide RNAs edit other organisms' genes
- **Sexual reproduction:** Genetic recombination
- **Life stages:** Infant → Juvenile → Adult → Elder
- **Self-learning:** Epigenetic memory, acquired traits

---

## Architecture Highlights

| Feature | Implementation |
|---------|---------------|
| DNA → RNA | Transcription with T/U replacement |
| RNA → Protein | Codon table translation, start/stop codons |
| Protein folding | Hydrophobic model with Monte Carlo relaxation |
| Function emergence | Structure determines class (enzyme, TF, structural) |
| Cell signaling | Surface receptors → internal state changes |
| Pattern formation | Morphogen diffusion + threshold response |
| Selection | Organism death from cellular ATP failure |

---

## Key Innovation: Emergence

**Traditional simulations:** Organisms have traits assigned.  
**PRIMORDIAL:** Traits emerge from protein folding.

Example:
1. Gene codes for amino acid sequence
2. Protein folds (hydrophobic collapse)
3. Folds create binding sites
4. Binding sites → enzyme function
5. Enzyme enables metabolic pathway
6. Pathway produces ATP
7. ATP → organism survives

**Selection acts on MACRO, caused by MICRO failures.**

---

## Files

```
primordial/
├── ecosystem.py                 # v1.0 - CRISPR organisms (standalone)
├── primordial_micro.py          # MICRO - Biochemical cells
├── primordial_meso.py           # MESO - Tissues
├── primordial_multiscale.py     # Integration - All scales
├── README.md                    # Full documentation
├── SETUP_INSTRUCTIONS.md        # Quick start
├── requirements.txt             # (empty, no deps)
└── memory_documentation.md      # This file
```

---

## How to Run

```bash
# Quick demo (v1.0 CRISPR organisms)
python3 ecosystem.py

# Biochemistry demo
python3 primordial_micro.py

# Full multi-scale (connects all layers)
python3 primordial_multiscale.py
```

**No dependencies.** Pure Python 3.6+.

---

## User Request Context

**Original ask:** "Copy of DNA for LLM, build from scratch, self-learns like infant to adult, procreate if two interact. Make it micro/macro."

**What was delivered:**
- ✅ Real DNA sequences (AGCT)
- ✅ Protein synthesis (DNA → RNA → Protein)
- ✅ Life stages (infant → adult)
- ✅ Sexual reproduction
- ✅ Multi-scale (micro → meso → macro)
- ✅ Emergent learning (not programmed)
- ✅ Self-contained, no external libraries

---

## Next Extensions (if desired)

- [ ] Visualization (matplotlib for protein folding, tissue growth)
- [ ] Export DNA to FASTA format
- [ ] Species tree phylogenetics
- [ ] Distributed computation (MPI)
- [ ] Web dashboard (React + WebSocket)
- [ ] Neural network + genetic hybrid organism

---

**Memory persistence:** This document captures PRIMORDIAL v2.0 for future reference.
