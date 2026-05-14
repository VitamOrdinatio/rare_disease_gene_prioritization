# RDGP Data Schema

## Repository

`rare_disease_gene_prioritization`

---

# Purpose

This document defines the initial RDGP v1 tabular data schemas.

RDGP v1 uses fixture-compatible TSV inputs and deterministic TSV, YAML, and Markdown outputs.

The primary reasoning identity is:

(sample_id, gene_id)

For v1, RDGP assumes one selected phenotype context per run.

---

# Primary Output: prioritized_genes.tsv

prioritized_genes.tsv is the primary review-oriented output table.

Each row represents:

one gene evaluated within one biological sample

## Required Column Order

sample_id
gene_id
gene_symbol
selected_phenotype
rank
priority_score
confidence_tier
confidence_state
confidence_explanation
confidence_flags
variant_evidence_score
gsc_prior_score
functional_evidence_score
uncertainty_state
evidence_status_summary
quality_flag
gsc_overlay_status
gene_mapping_status
evidence_summary
provenance_summary
run_id

## Column Semantics

| Column | Meaning |
|---|---|
| sample_id | biological sample identifier |
| gene_id | stable gene identifier when available |
| gene_symbol | human-readable gene symbol |
| selected_phenotype | phenotype context used for GSC overlay |
| rank | deterministic within-sample rank |
| priority_score | prioritization strength, not disease probability |
| confidence_tier | qualitative interpretive reliability tier |
| confidence_state | primary confidence interpretation |
| confidence_explanation | human-readable confidence explanation |
| confidence_flags | confidence limitation flags |
| variant_evidence_score | sample-specific variant evidence component |
| gsc_prior_score | phenotype-scoped GSC prior component |
| functional_evidence_score | optional functional evidence component or not_evaluated |
| uncertainty_state | primary uncertainty state |
| evidence_status_summary | compact status summary across evidence channels |
| quality_flag | technical/reliability summary |
| gsc_overlay_status | GSC overlay status |
| gene_mapping_status | stable/fallback/ambiguous/missing/unresolved |
| evidence_summary | human-readable prioritization explanation |
| provenance_summary | source and run provenance summary |
| run_id | upstream or RDGP run identifier retained for traceability |

---

# Secondary Output: gene_evidence_matrix.tsv

gene_evidence_matrix.tsv contains all fields in prioritized_genes.tsv plus intermediate evidence, score, confidence, and overlay columns.

This output is intended for debugging, validation, and interpretability.

---

# Optional Output: evidence_items.tsv

evidence_items.tsv is optional in early v1.

It is reserved for future long-form evidence modeling.

When implemented, it should preserve evidence-level records with source, scope, status, confidence, and provenance fields.

---

# Validation Outputs

RDGP writes:

validation_report.md
validation_summary.yaml

validation_report.md is human-readable.

validation_summary.yaml is machine-readable and intended for regression testing and CI-compatible workflows.

---

# Run Manifest

Each run writes:

run_manifest.yaml

The run manifest records:

- run ID
- selected phenotype
- strict mode
- input paths
- scoring profile
- validation profile
- software/runtime metadata

---

# Schema Stability Principle

RDGP v1 should avoid silent output schema drift.

If required primary output fields change, the contract, implementation plan, tests, and this schema document must be updated together.

# End of data_schema.md
