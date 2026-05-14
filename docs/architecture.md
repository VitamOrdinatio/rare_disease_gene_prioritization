# RDGP Architecture

## Repository

`rare_disease_gene_prioritization`

---

# Purpose

Rare Disease Gene Prioritization (RDGP) is an explainable translational bioinformatics framework for prioritizing candidate disease-associated genes within biological samples.

RDGP was designed around several core architectural goals:

- transparent reasoning
- deterministic execution
- semantic-state preservation
- validation-first design
- confidence-aware interpretation
- reproducible outputs
- provenance preservation

The framework intentionally avoids opaque black-box prioritization systems.

---

# Core Reasoning Identity

The primary RDGP reasoning identity is:

```text
(sample_id, gene_id)
```

Each output row represents:

```text
one gene evaluated within one biological sample
```

This identity is preserved throughout pipeline execution.

RDGP v1 currently assumes:

```text
one selected phenotype context per run
```

Future versions may support:

- multi-phenotype reasoning
- inheritance-aware modeling
- cohort-level prioritization
- transcriptomic overlays
- pathway convergence overlays
- noncoding evidence reasoning

---

# High-Level Architectural Flow

RDGP v1 currently follows this execution model:

```text
input evidence
    ↓
schema validation
    ↓
semantic invariant validation
    ↓
phenotype-scoped GSC overlays
    ↓
transparent scoring
    ↓
qualitative confidence modeling
    ↓
deterministic ranking
    ↓
explainability generation
    ↓
output serialization
    ↓
validation reporting
```

---

# Repository Architecture

```text
rare_disease_gene_prioritization/
├── config/
├── data/
├── docs/
├── logs/
├── results/
├── scripts/
├── src/
│   └── rdgp/
├── tests/
└── README.md
```

---

# Core Pipeline Components


## 1. Input Evidence Layer

Primary v1 evidence inputs include:

- gene evidence tables
- phenotype-scoped GSC overlays
- optional future functional evidence

Current interfaces use:

```text
TSV-based deterministic inputs
```

to maximize transparency and reproducibility.

---

## 2. Validation Layer

Validation occurs before prioritization logic executes.

Current validation responsibilities include:

- schema validation
- semantic-state validation
- required field validation
- phenotype overlay validation
- output schema stabilization

The validation layer exists to prevent:

- silent semantic drift
- malformed evidence ingestion
- unstable outputs
- hidden pipeline corruption

---

## 3. Semantic-State Preservation

RDGP explicitly prohibits silent semantic collapse between distinct biological or interpretive states.

A core RDGP architectural principle is:

```text
semantic states must remain explicit
```

RDGP intentionally distinguishes between:

- missing
- unresolved
- unsupported
- not_evaluated
- ambiguous
- conflicting
- no_match

These states are preserved rather than silently collapsed into null values.

This distinction is critically important for:

- translational interpretation
- explainability
- reproducibility
- downstream reasoning integrity

---

## 4. Phenotype-Scoped GSC Overlay Layer

RDGP integrates phenotype-aware overlays from:

```text
gene_set_consensus (GSC)
```

The overlay layer:

- preserves row identity
- prevents silent row multiplication
- supports deterministic joins
- distinguishes unsupported phenotype contexts from missing evidence

Current overlay preference order:

```text
gene_id
    ↓
optional gene_symbol fallback
```

RDGP explicitly treats:

```text
no_gsc_match
```

as:

```text
absence of phenotype-prior support
```

and not contradiction.

---

## 5. Transparent Scoring Architecture

RDGP scoring is intentionally decomposed into inspectable components.

Current scoring channels include:

| Evidence Channel          | Purpose                         |
| ------------------------- | ------------------------------- |
| variant_evidence_score    | sample-specific variant support |
| gsc_prior_score           | phenotype-scoped prior support  |
| functional_evidence_score | optional functional evidence    |

The final:

```text
priority_score
```

is a transparent aggregation of explicit components.

RDGP intentionally avoids:

- opaque monolithic scoring
- hidden probabilistic collapse
- uninterpretable weighting systems

---

## 6. Confidence Architecture

RDGP explicitly separates:

```text
prioritization strength
```

from:

```text
interpretive reliability
```

Confidence modeling is:

- qualitative-first
- explainable
- limitation-aware
- non-probabilistic

Current qualitative tiers include:

- high
- moderate
- limited
- low
- unresolved

Importantly:

```text
missing optional evidence is not negative evidence
```

Confidence reduction may occur due to:

- ambiguous mapping
- low-quality evidence
- conflicting annotations
- incomplete evidence coverage

without directly collapsing prioritization scores.

---

## 7. Deterministic Ranking

Deterministic behavior is critical for translational reproducibility, regression testing, scientific review, and downstream auditability.

RDGP ranking behavior is deterministic.

Tie-breaking behavior is explicitly controlled using:

- priority score
- confidence tier
- variant evidence score
- GSC prior score
- gene symbol
- gene ID

This guarantees stable outputs across executions.

---

## 8. Explainability Layer

RDGP generates explicit human-readable interpretability outputs.

Current explainability outputs include:

- evidence summaries
- provenance summaries
- confidence explanations
- evidence status summaries

The explainability layer exists to ensure that prioritization decisions remain reconstructable.

---

## 9. Output Serialization

RDGP writes deterministic outputs under:

`results/runs/<run_id>/`

Primary outputs include:

```text
prioritized_genes.tsv
gene_evidence_matrix.tsv
validation_report.md
validation_summary.yaml
run_manifest.yaml
```

Output schemas are stabilized and validated.

---

## 10. Provenance and Reproducibility

RDGP preserves execution provenance through:

- run manifests
- logging
- deterministic outputs
- explicit validation summaries
- stable schemas

This supports:

- reproducibility
- auditing
- regression testing
- translational review workflows

---

# Internal Module Layout

```text
src/rdgp/
├── confidence.py
├── config.py
├── explainability.py
├── gsc_overlay.py
├── io.py
├── logging_utils.py
├── manifest.py
├── ranking.py
├── schemas.py
├── scoring.py
└── validators.py
```

---

# Current Testing Architecture

RDGP uses validation-first testing strategy.

Current testing categories include:

- unit tests
- validation tests
- integration tests
- semantic invariant tests
- output schema tests
- scoring guardrail tests
- confidence anti-collapse tests

The repository currently maintains:

```text
full green test execution prior to architectural commits
```

---

# Current Ecosystem Relationships

RDGP currently integrates conceptually with:

| Repository                            | Relationship                       |
| ------------------------------------- | ---------------------------------- |
| reproducible_pipeline_framework (RPF) | architectural foundation           |
| gene_set_consensus (GSC)              | phenotype priors                   |
| variant_annotation_pipeline (VAP)     | upstream variant evidence          |
| rnaseq_pipeline (RSP)                 | future transcriptomic overlays     |
| variant_database (VDB)                | future persistent evidence storage |

---

# Current Architectural Boundaries

These exclusions are intentional v1 stabilization decisions designed to preserve semantic correctness, interpretability, deterministic execution, and architectural auditability before introducing higher-order reasoning complexity.

RDGP v1 intentionally excludes:

- probabilistic calibration
- inheritance-aware reasoning
- transcriptomic convergence
- network propagation
- noncoding prioritization
- persistent database layers
- distributed execution
- machine learning prioritization

---

# Future Architectural Expansion Areas

Planned future development areas include:

- inheritance-aware evidence structures
- transcriptomic convergence overlays
- pathway-level reasoning
- network convergence modeling
- noncoding evidence interpretation
- VDB integration
- RSP integration
- evidence-level long-form modeling
- multi-phenotype prioritization
- explainable network reasoning

Future biological reasoning expansion is additionally guided by:
`docs/design/future_biological_reasoning_extensions.md`

---

# Architectural Philosophy Summary

RDGP prioritizes:

```text
semantic correctness
    before
scientific expansion
```

and:

```text
explainability
    before
algorithmic complexity
```

The repository is intentionally evolving from:

```text
ranking engine
```

toward:

```text
explainable translational reasoning framework
```

through controlled, validation-first architectural maturation.

---