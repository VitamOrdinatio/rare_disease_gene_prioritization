# Rare Disease Gene Prioritization (RDGP)

## Overview

Rare Disease Gene Prioritization (RDGP) is a transparent and reproducible translational bioinformatics framework for prioritizing candidate disease-associated genes within biological samples.

RDGP is designed for:

- rare disease genomics
- mitochondrial disease workflows
- epilepsy genomics
- translational variant interpretation
- explainable ranking pipelines
- phenotype-aware gene prioritization

The framework emphasizes:

- deterministic execution
- semantic rigor
- explainability
- validation-first design
- stable output schemas
- provenance preservation
- confidence-aware reasoning

RDGP is intentionally designed to avoid opaque black-box prioritization behavior.

Instead of producing a single uninterpretable score, RDGP decomposes prioritization into transparent evidence channels with explicit confidence semantics.

---

## Why RDGP Exists

Rare disease interpretation pipelines often produce large candidate gene lists with limited transparency regarding:

- why genes ranked highly
- how phenotype priors influenced prioritization
- whether missing evidence was treated as absence
- how confidence differs from prioritization strength
- whether outputs are reproducible and schema-stable

RDGP was designed to address these limitations through explicit semantic-state preservation, transparent score decomposition, qualitative confidence modeling, deterministic ranking behavior, and validation-first architecture.

---

# Repository Role Within the Ecosystem

RDGP operates within a larger interoperable bioinformatics ecosystem.

Primary upstream/downstream relationships include:

| Repository | Relationship |
|---|---|
| reproducible_pipeline_framework (RPF) | shared architectural foundation |
| gene_set_consensus (GSC) | phenotype-scoped prior knowledge overlays |
| variant_annotation_pipeline (VAP) | variant-level annotation inputs |
| rnaseq_pipeline (RSP) | future transcriptomic convergence overlays |
| variant_database (VDB) | future persistent evidence storage |

RDGP is primarily responsible for:

```text
(sample_id, gene_id)
```

---

# Core Reasoning Identity

The primary RDGP reasoning identity is:

```text
(sample_id, gene_id)
```

Each prioritized row represents:

```text
one gene evaluated within one biological sample
```

RDGP v1 currently assumes:

```text
one selected phenotype context per run
```

Future versions may support:

- multi-phenotype reasoning
- inheritance-aware modeling
- transcriptomic convergence overlays
- network-level evidence integration
- noncoding evidence reasoning

---

# Design Philosophy

RDGP v1 was built around several core principles.

## Transparent Scoring

RDGP avoids opaque monolithic prioritization scores.

Priority scores are decomposed into explicit evidence channels:

- variant evidence
- phenotype-scoped GSC priors
- optional functional evidence

All score components remain inspectable.

---

# Confidence Is Separate From Score

RDGP explicitly separates:

```text
prioritization strength
```

from:

```text
interpretive reliability
```

Confidence is:

- qualitative-first
- explainable
- limitation-aware
- non-probabilistic

Missing optional evidence is not treated as negative evidence.

---

# Semantic-State Preservation

RDGP distinguishes between:

- missing
- unsupported
- unresolved
- not_evaluated
- no_match
- ambiguous
- conflicting

These states are preserved explicitly throughout pipeline execution.

---

# Deterministic Execution

RDGP prioritizes reproducibility.

The framework enforces:

- deterministic ranking
- stable output schemas
- explicit tie-breaking
- run manifests
- validation summaries
- provenance tracking

---

# Repository Structure

```text
rare_disease_gene_prioritization/
├── config/
├── data/
├── docs/
├── logs/
├── results/
├── scripts/
├── src/
├── tests/
└── README.md
```

---

# Quickstart

## Current Technology Stack

- Python 3.12
- pandas
- pytest
- YAML configuration
- TSV-based evidence interfaces
- deterministic filesystem-based execution

## Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run Tests

```bash
pytest
```

Current repository status:

```text
51 passing tests
```

Current test coverage includes:

- schema validation
- semantic invariant validation
- phenotype-scoped overlays
- scoring guardrails
- confidence anti-collapse behavior
- deterministic ranking
- explainability generation
- integration pipeline execution
- output schema stabilization

---

# Example Pipeline Execution

Run the example RDGP pipeline:

```bash
PYTHONPATH=src python scripts/run_pipeline.py
```

Validate configured inputs independently:

```bash
PYTHONPATH=src python scripts/validate_inputs.py
```

---

# Example Outputs

Each execution creates a deterministic run directory:

`results/runs/<run_id>/`

Example structure:

```text
results/runs/run_20260513_211745_123456/
├── reports/
│   ├── validation_report.md
│   └── validation_summary.yaml
├── tables/
│   ├── prioritized_genes.tsv
│   └── gene_evidence_matrix.tsv
└── run_manifest.yaml
```

---

# Primary Outputs

## `prioritized_genes.tsv`

Primary review-oriented output.

Contains:

- deterministic rank
- priority score
- confidence tier
- confidence explanation
- phenotype overlay status
- provenance summaries
- evidence summaries

---

## `gene_evidence_matrix.tsv`

Extended debugging and interpretability matrix.

Contains:

- intermediate evidence fields
- overlay states
- score decompositions
- confidence metadata
- validation-related context

---

## `validation_report.md`

Human-readable validation report.

---

## `validation_summary.yaml`

Machine-readable validation summary suitable for:

- CI workflows
- regression testing
- pipeline auditing

---

## `run_manifest.yaml`

Run provenance manifest containing:

- run identifiers
- phenotype context
- scoring profile
- validation profile
- runtime metadata
- input references

---

# Validation Philosophy

RDGP uses validation-first architecture.

The repository enforces:

- schema validation
- semantic invariant validation
- output schema stability
- anti-row-multiplication safeguards
- deterministic ranking behavior
- explainability preservation

The goal is to prevent:

- silent semantic drift
- hidden scoring collapse
- provenance loss
- unstable outputs

---

# Current RDGP v1 Capabilities

Current implemented capabilities include:

- fixture-first architecture
- TSV-based evidence ingestion
- phenotype-scoped GSC overlays
- transparent scoring decomposition
- qualitative confidence modeling
- deterministic ranking
- explainability generation
- run manifests
- validation reporting
- schema stabilization
- integration testing

---

# Current RDGP v1 Limitations

RDGP v1 intentionally limits scope to stabilize architecture first.

Current limitations include:

- single phenotype context per run
- no inheritance-aware reasoning yet
- no transcriptomic overlays yet
- no network convergence modeling yet
- no noncoding prioritization yet
- no persistent database backend yet
- no probabilistic calibration layer

These are planned future expansion areas.

---

# Future Roadmap

Planned future development includes:

- inheritance-aware evidence modeling
- transcriptomic convergence overlays
- pathway-level convergence reasoning
- noncoding evidence interpretation
- VDB integration
- RSP integration
- multi-phenotype prioritization
- evidence-level long-form modeling
- cohort-level prioritization
- explainable network reasoning

---

# Development Status

Current status:

```text
Phase 1 architectural implementation underway
```

The repository currently prioritizes:

- semantic correctness
- architectural stability
- reproducibility
- explainability
- validation rigor

before large-scale scientific expansion.

---

# License

MIT license

---

# Acknowledgments

RDGP development incorporates design collaboration across:

- DEX (software engineering architecture)
- SAGE (scientific reasoning and evidence semantics)
- LANE (strategic translational alignment)

with final human review and scientific ownership retained by the repository author.