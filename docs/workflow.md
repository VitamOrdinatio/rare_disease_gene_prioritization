# RDGP Workflow

## Repository

`rare_disease_gene_prioritization`

---

# Purpose

This document describes the operational workflow of the Rare Disease Gene Prioritization (RDGP) framework.

The workflow document focuses on:

- repository execution
- validation flow
- pipeline orchestration
- output interpretation
- reproducibility behavior
- operational expectations

This document complements:

- `README.md`
- `docs/architecture.md`
- `docs/data_schema.md`

---

# High-Level Workflow

RDGP v1 currently follows this operational sequence:

```text
configure run
    ↓
validate inputs
    ↓
load evidence
    ↓
apply phenotype-scoped overlays
    ↓
compute transparent scores
    ↓
compute inheritance compatibility context
    ↓
compute qualitative confidence
    ↓
perform deterministic ranking
    ↓
generate explainability outputs
    ↓
serialize outputs
    ↓
write manifests and validation reports
```

---

# Repository Initialization

## Create Virtual Environment

RDGP uses:

```text
one repository = one virtual environment
```

recommended under:

```text
.venv/
```

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Running Tests

RDGP uses validation-first testing.

Run the full test suite:

```bash
pytest
```

Current test coverage includes:

- schema validation
- semantic invariant testing
- scoring guardrails
- confidence anti-collapse testing
- deterministic ranking behavior
- explainability generation
- integration execution
- output schema stabilization

---

# Configuration Workflow

Primary runtime configuration is controlled through:

```text
config/config.yaml
```

Current configuration categories include:

- selected phenotype
- evidence input tables
- scoring profile
- validation profile
- output root
- strict mode behavior
- GSC overlay enablement

---

# Input Evidence Workflow

RDGP v1 currently consumes:

| Input Type                          | Purpose                        |
| ----------------------------------- | ------------------------------ |
| gene evidence table                 | sample-specific evidence       |
| GSC overlay table                   | phenotype-scoped prior support |
| optional future functional evidence | future expansion area          |

Current interfaces are intentionally:

```text
TSV-based
```

for transparency and reproducibility.

---

# Validation Workflow

Validation occurs before prioritization execution.

## Standalone Validation

Run validation independently:

```bash
PYTHONPATH=src python scripts/validate_inputs.py
```

Validation responsibilities include:

- schema validation
- semantic invariant validation
- overlay validation
- output schema expectations
- required field validation

Validation failures are designed to stop execution early.

---

# Pipeline Execution Workflow

All major execution stages are designed to remain independently inspectable and testable.

Run the primary RDGP pipeline:

```bash
PYTHONPATH=src python scripts/run_pipeline.py
```

Current execution stages include:

```text
input loading
    ↓
schema validation
    ↓
semantic validation
    ↓
GSC overlay integration
    ↓
transparent scoring
    ↓
inheritance compatibility reasoning
    ↓
qualitative confidence modeling
    ↓
deterministic ranking
    ↓
explainability generation
    ↓
output serialization
```

---

# Runtime Output Workflow

Each execution creates a deterministic run directory:

`results/runs/<run_id>/`

Example:

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

# Logging Workflow

Pipeline execution logs are written under:

`logs/<run_id>/`

Current logging includes:

- execution start/stop
- validation status
- pipeline stage transitions
- output generation
- manifest generation

---

# Output Interpretation Workflow

## `prioritized_genes.tsv`

Primary review-oriented output.

Each row represents:

```text
one gene evaluated within one biological sample
```

Primary review fields include:

- rank
- priority_score
- confidence_tier
- confidence_explanation
- evidence_summary
- provenance_summary
- gsc_overlay_status

---

## `gene_evidence_matrix.tsv`

Extended debugging and interpretability output.

Contains:

- intermediate evidence fields
- score decomposition fields
- overlay metadata
- confidence metadata
- semantic-state context

This table is intended for:

- debugging
- regression analysis
- validation review
- interpretability inspection

---

# Validation Reporting Workflow

RDGP produces both:

```text
human-readable validation
```

and:

```text
machine-readable validation
```

outputs.

## `validation_report.md`

Human-readable validation report.

Intended for:

- reviewers
- developers
- translational interpretation workflows

---

## `validation_summary.yaml`

Machine-readable validation summary.

Intended for:

- regression testing
- CI workflows
- automated auditing
- reproducibility tracking

---

# Manifest Workflow

Each execution produces:

`run_manifest.yaml`

The manifest records:

- run ID
- phenotype context
- strict mode
- scoring profile
- validation profile
- input references
- runtime metadata

The manifest exists to preserve:

- reproducibility
- provenance
- execution traceability

---

# Semantic-State Workflow

RDGP intentionally preserves semantic distinctions throughout execution.

The workflow explicitly distinguishes between:

- missing
- unresolved
- unsupported
- no_match
- not_evaluated
- ambiguous
- conflicting

These states are intentionally preserved during:

- ingestion
- overlay integration
- scoring
- confidence modeling
- serialization

RDGP explicitly prohibits:

```text
silent semantic collapse
```

between biologically distinct interpretive states.

---

# Confidence Workflow

RDGP confidence modeling is intentionally separated from prioritization scoring.

Confidence reflects:

```text
interpretive reliability
```

rather than:

```text
disease probability
```

Current confidence tiers include:

- high
- moderate
- limited
- low
- unresolved

Confidence may decrease due to:

- mapping ambiguity
- low-quality evidence
- conflicting evidence
- incomplete evidence coverage

without directly collapsing priority scores.

---

# Inheritance Compatibility Workflow

RDGP now supports bounded inheritance-aware reasoning.

Inheritance reasoning currently supports:

- autosomal dominant
- autosomal recessive
- X-linked
- mitochondrial
- unresolved inheritance states

Current inheritance outputs include:

- inheritance_support
- inheritance_conflict
- inheritance_explanation
- inheritance_uncertainty

Inheritance reasoning currently behaves as:

```text
semantic interpretive context
```

rather than:

```text
hard diagnostic filtering
```

Inheritance reasoning may influence:

- confidence semantics
- interpretive caution
- explainability

but does not currently:

- suppress ranking scores
- exclude genes automatically
- perform pedigree reasoning
- perform Bayesian segregation analysis

Inheritance-aware outputs currently appear primarily within:

```text
gene_evidence_matrix.tsv
```

while reviewer-facing prioritized outputs remain intentionally stabilized.


---

# Deterministic Execution Workflow

RDGP prioritizes deterministic execution behavior.

Deterministic behavior includes:

- stable ranking
- explicit tie-breaking
- stable output schemas
- reproducible run structures
- stable validation outputs

This supports:

- scientific reproducibility
- regression testing
- translational review
- pipeline auditability

---

# Troubleshooting Workflow

## Common Validation Failures

### Missing Required Columns

Cause:

```text
schema mismatch
```

Typical resolution:

- inspect TSV headers
- compare against docs/data_schema.md
- rerun validation

---

### Output Schema Failures

Cause:

```text
pipeline-generated columns differ from schema contract
```

Typical resolution:

- inspect PRIORITIZED_GENES_COLUMNS
- inspect pipeline serialization logic
- rerun schema validation tests

---

### Semantic Invariant Failures

Cause:

```text
semantic-state preservation violation
```

Typical resolution:

- inspect null handling
- inspect overlay merge behavior
- inspect scoring assumptions

---

# Current Operational Boundaries

These exclusions are intentional operational stabilization decisions designed to preserve deterministic execution, explainability, and validation integrity before introducing higher-order biological reasoning complexity.

RDGP v1 intentionally excludes:

- pedigree-aware inheritance reasoning
- phase-resolved compound heterozygosity
- transcriptomic overlays
- network convergence modeling
- noncoding prioritization
- persistent database backends
- probabilistic calibration
- machine learning prioritization

These exclusions are intentional stabilization decisions.

---

# Future Workflow Expansion Areas

Planned future operational expansions include:

- advanced inheritance-aware execution
- pedigree-aware inheritance reasoning
- phase-resolved compound heterozygosity
- transcriptomic convergence overlays
- pathway-level overlays
- evidence-item modeling
- VDB integration
- RSP integration
- multi-phenotype workflows
- cohort-level prioritization

---

# Workflow Philosophy Summary

RDGP prioritizes:

```text
validation
    before
expansion
```

and:

```text
explainability
    before
complexity
```

The operational workflow is intentionally designed to preserve:

- semantic correctness
- deterministic behavior
- reproducibility
- interpretability
- translational auditability