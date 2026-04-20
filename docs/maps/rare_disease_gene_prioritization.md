# Milestone Map: rare_disease_gene_prioritization (RDGP)

## Purpose

RDGP transforms heterogeneous variant- and gene-level evidence into a unified, interpretable prioritization framework suitable for clinical-style reasoning.

Inputs:
    • variant evidence (VAP → VDB) 
    • gene-level evidence (GSC) 
    • optional expression evidence (RSP) 

Output:
    • ranked gene list with structured supporting evidence


---

## Layer Ecosystem
1. provider layer (VDB)
2. contract layer (vdb_rdgp_interface)
3. overlay layer (GSC)
4. reasoning layer (RDGP)

---

## Terminology

- "gene-level evidence": aggregated variant and contextual information associated with a gene for a given sample
- "prioritization": ranking genes based on composite evidence rather than binary classification

- "GSC gene-level evidence": source-derived evidence aggregated across datasets
- "RDGP gene-level evidence": sample-specific evidence derived from variant aggregation and overlays

---

## Core Data Model (v1)

RDGP operates on a gene-centric evidence representation derived from VDB.

Fields:
- gene_symbol
- gene_id (if available)
- sample_id
- variant_count
- rare_variant_count
- high_impact_variant_count
- pathogenic_variant_count
- likely_pathogenic_variant_count
- vus_variant_count
- likely_benign_variant_count
- benign_variant_count
- max_variant_severity
- variant_score
- GSC_support (e.g., consensus_score or membership)
- expression_support (optional, from RSP)
- composite_score

### Example Record (v1)

- gene_symbol: POLG
- gene_id: ENSG00000140521
- sample_id: SAMPLE_001
- variant_count: 2
- rare_variant_count: 2
- high_impact_variant_count: 1
- pathogenic_variant_count: 1
- likely_pathogenic_variant_count: 0
- vus_variant_count: 1
- likely_benign_variant_count: 0
- benign_variant_count: 0
- max_variant_severity: LOF
- variant_score: 2 # example derived from scoring rules in M2
- GSC_support: 3
- expression_support: null
- composite_score: 7.5 # example combined from variant_score + GSC_support + optional normalization

---

## Standard Output Format (v1)

RDGP outputs must include:

- gene_symbol
- composite_score
- variant_count
- rare_variant_count
- high_impact_variant_count
- pathogenic_variant_count
- likely_pathogenic_variant_count
- vus_variant_count
- likely_benign_variant_count
- benign_variant_count
- GSC_support
- expression_support (if available)
- evidence_summary (text or structured)

GSC_support = GSC-derived consensus support value, typically consensus_score in v1

---

## Strategic Value (Very High)

This repo demonstrates:
    • translational reasoning 
    • integration across pipelines 
    • handling of uncertainty 
    • evidence weighting 
    • clinical-style prioritization logic 

This is what moves you from:
“pipeline builder” → “clinical bioinformatics thinker”

RDGP represents the transition from data processing to evidence-based clinical reasoning.

---

## Milestones

### M1 — Input Integration Layer (Data Access)
    • Pull data from VDB: 
        ◦ variants 
        ◦ annotations 
        ◦ sample-level context 
    • Join with: 
        ◦ gene mapping 
        ◦ GSC gene-level evidence (if available)

Define a clean internal structure:
    • gene-centric view (important shift) 

Goal:
You can construct a gene-level dataset from variant-level data

---

### M2 — Basic Prioritization Logic (Heuristic Model)

Implement deterministic scoring rules:

- variant impact weighting:
    LOF > missense > synonymous

- rarity weighting:
    lower population frequency increases score

- gene burden:
    multiple variants in the same gene increase score

- annotation weighting:
    pathogenic > likely pathogenic > VUS > likely benign > benign

- GSC support:
    genes with higher consensus scores receive additional weight

Important:
- all scoring must be explainable
- scoring components must be preserved alongside final score

Output:
    • per-gene variant_score and intermediate scoring components

---

### M3 — Multi-Evidence Integration

Add additional signals:
    • GSC support (consensus-based gene weighting)
    • optional RSP: 
        ◦ differential expression 
        ◦ network convergence signal 

Combine evidence into a composite score:

composite_score =
    variant_score
  + GSC_support
  + expression_support (if available)

Note: scoring components may require normalization to ensure comparable scale across evidence types.

GSC_support is derived from GSC consensus_score in v1

Each component must remain individually accessible for interpretability.

Goal:
Ranking reflects integrated evidence across multiple layers, not just variants

---

### M4 — Uncertainty + Edge Case Handling

Explicitly address:
    • genes with sparse evidence 
    • conflicting annotations 
    • variants of uncertain significance 
    • multiple weak signals vs one strong signal 
    • mitochondrial genes / heteroplasmy (even if partial) 
    • missing data:
        - genes lacking certain evidence types (e.g., no expression data) must not be penalized incorrectly

Define:
    • assumptions 
    • limitations 

Goal:
Model is transparent about uncertainty

---

### M5 — Validation Strategy (Critical)

Validation should include:

- known gene recovery:
    curated disease genes should rank highly
- sensitivity analysis:
    evaluate how rankings change with threshold adjustments
- ranking stability:
    small perturbations in input data should not produce extreme ranking shifts
- negative control:
    genes known to be unrelated should not rank highly
- reproducibility:
    identical inputs must produce identical rankings

Goal:
System is defensible, not just plausible

---

### M6 — Output + Interpretability Layer

Each ranked gene must include:

- variant evidence summary
- annotation summary
- GSC support
- expression support (if available)
- contribution of each component to composite score

Goal:
Outputs are interpretable by humans

RDGP outputs must be compatible with downstream interpretation and reporting workflows, including clinical-style review and prioritization reporting.

---

### M7 — Documentation + Clinical Framing

Document:
    • objective 
    • approach 
    • assumptions 
    • limitations 
    • edge cases 
    • validation strategy 
    • implementation details 

Clearly distinguish:
    • detection vs annotation vs prioritization 

Goal:
Repo reads like something a clinical bioinformatics group could review

---

## Release Gate (Public v1.0)

RDGP is portfolio-ready when:
    • integrates VDB data correctly 
    • produces ranked gene lists 
    • uses multiple evidence sources (at least VAP + GSC) 
    • includes clear scoring logic 
    • explains why genes are ranked 
    • includes: 
        ◦ assumptions 
        ◦ limitations 
        ◦ edge cases 
        ◦ validation strategy 
        ◦ implementation details 
    • README tells a coherent clinical story 

---

## Future Upgrades (Post v1.0)
    • improved scoring models (weighted, probabilistic) 
    • machine learning approaches (later, not early) 
    • phenotype integration (if desired) 
    • improved RSP integration 
    • visualization layer (gene networks, ranking plots)

