# RDGP Implementation Plan

## Repository

`rare_disease_gene_prioritization` (`RDGP`)

## Artifact Type

DEX-owned implementation plan.

## Intended Placement

```text
rare_disease_gene_prioritization/docs/plans/implementation_plan.md
```

## Plan Status

Draft v0.1 for review before implementation.

---

# 1. Purpose

This document defines the implementation plan for RDGP v1.

It translates the RDGP system contract and SAGE-RDGP scientific governance stack into a controlled, testable, fixture-first software development sequence.

This plan is governed by:

- `docs/contracts/system_contract.md`
- `scoring_rationale.md`
- `evidence_taxonomy.md`
- `uncertainty_and_null_semantics.md`
- `validation_strategy.md`
- `confidence_modeling_framework.md`

RDGP implementation must preserve:

- sample-scoped gene reasoning
- deterministic scoring
- confidence/score/uncertainty separation
- null and missingness semantics
- provenance traceability
- explainability
- validation-first behavior
- interface compatibility with future VDB, GSC, and RSP integrations

---

# 2. Implementation Philosophy

RDGP v1 should be built as:

```text
a deterministic, explainable, fixture-first gene prioritization engine
```

not as:

```text
a black-box predictor
a clinical diagnostic engine
a VDB replacement
a variant annotator
a transcriptomics pipeline
```

The correct early implementation posture is:

```text
contracts first
fixtures second
validators third
minimal scoring fourth
outputs fifth
integration later
```

Implementation must be small, modular, auditable, and commit-sized.

---

# 3. Primary v1 Goal

RDGP v1 should produce a deterministic ranked gene table from fixture-compatible gene evidence inputs and optional GSC overlays.

Minimum v1 behavior:

1. Load a gene-level evidence table keyed by `(sample_id, gene_id)`.
2. Validate schema and identity constraints.
3. Optionally attach a selected phenotype-scoped GSC overlay.
4. Preserve null, uncertainty, confidence, and provenance semantics.
5. Compute transparent score components.
6. Produce a ranked `prioritized_genes.tsv`.
7. Produce intermediate evidence and validation outputs.
8. Pass semantic anti-collapse validation tests.

---

# 4. Non-Goals for v1

RDGP v1 will not:

- connect directly to a live VDB database
- require RSP-derived evidence
- implement full inheritance modeling
- implement full noncoding interpretation
- implement mitochondrial heteroplasmy logic
- implement probabilistic or ML prioritization
- claim clinical diagnostic certainty
- perform raw variant annotation
- perform raw RNA-seq or network analysis

These are future extensions.

---

# 5. Repository Scaffold Alignment

The current RDGP scaffold should be aligned toward the following structure:

```text
rare_disease_gene_prioritization/
├── README.md
├── LICENSE
├── Makefile
├── requirements.txt
├── config/
│   ├── config.yaml
│   ├── scoring_profiles/
│   │   └── default_v1.yaml
│   └── validation_profiles/
│       └── default_v1.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── example/
├── docs/
│   ├── architecture.md
│   ├── data_schema.md
│   ├── workflow.md
│   ├── notes.md
│   ├── maps/
│   │   └── milestone_map.md
│   ├── contracts/
│   │   └── system_contract.md
│   ├── plans/
│   │   └── implementation_plan.md
│   ├── design/
│   │   ├── scoring_rationale.md
│   │   ├── evidence_taxonomy.md
│   │   ├── uncertainty_and_null_semantics.md
│   │   ├── validation_strategy.md
│   │   └── confidence_modeling_framework.md
│   └── validation/
│       └── validation_plan.md
├── logs/
├── results/
│   └── runs/
├── scripts/
│   ├── run_pipeline.py
│   └── validate_inputs.py
├── src/
│   └── rdgp/
│       ├── __init__.py
│       ├── config.py
│       ├── io.py
│       ├── schemas.py
│       ├── validators.py
│       ├── evidence.py
│       ├── gsc_overlay.py
│       ├── scoring.py
│       ├── confidence.py
│       ├── ranking.py
│       ├── explainability.py
│       ├── provenance.py
│       ├── manifest.py
│       └── logging_utils.py
└── tests/
    ├── unit/
    ├── integration/
    ├── validation/
    └── fixtures/
```

## Notes

- `docs/design/` is where the SAGE-assisted design documents are kept.
- Large datasets must not be committed.
- Test fixtures should remain small and synthetic.
- Runtime outputs should be written under `results/runs/<run_id>/`.
- `.venv/` must remain untracked.

---

# 6. Configuration Strategy

RDGP must be configuration-driven.

## 6.1 Primary Config

Recommended file:

```text
config/config.yaml
```

Required concepts:

```yaml
run:
  run_id: auto
  strict_mode: true

inputs:
  gene_evidence_table: data/example/gene_evidence.tsv
  gsc_overlay_table: data/example/gsc_overlay.tsv
  functional_evidence_table: null

analysis:
  selected_phenotype: epilepsy_example
  enable_gsc_overlay: true
  enable_functional_evidence: false

scoring:
  profile: default_v1

validation:
  profile: default_v1

outputs:
  output_root: results/runs
```

## 6.2 Scoring Profile

Recommended file:

```text
config/scoring_profiles/default_v1.yaml
```

The scoring profile should define:

- channel enablement
- score component names
- severity tiers
- bounded additive behavior
- GSC cap or tier behavior
- missingness behavior
- calibration rules
- confidence behavior references
- output component fields

Exact numerical values should be conservative, documented, and easy to revise.

## 6.3 Validation Profile

Recommended file:

```text
config/validation_profiles/default_v1.yaml
```

The validation profile should define:

- required input schemas
- required output schemas
- strict vs permissive failure behavior
- semantic invariant checks
- required warning flags
- required provenance fields
- required confidence fields

---

# 7. Data Model and Fixture Strategy

RDGP v1 should use small synthetic fixtures before live VDB/RSP integration.

## 7.1 Required Fixture Files

Recommended initial fixtures:

```text
tests/fixtures/gene_evidence_minimal.tsv
tests/fixtures/gsc_overlay_minimal.tsv
tests/fixtures/gene_evidence_edge_cases.tsv
tests/fixtures/gsc_overlay_edge_cases.tsv
tests/fixtures/expected_prioritized_genes_minimal.tsv
tests/fixtures/expected_validation_report_minimal.yaml
```

Optional example files for public demo:

```text
data/example/gene_evidence.tsv
data/example/gsc_overlay.tsv
```

`tests/fixtures/` and `data/example/` serve distinct purposes:

- `tests/fixtures/` supports validation and deterministic testing
- `data/example/` supports public demonstrations, walkthroughs, and reproducible example runs

Files may overlap conceptually but should remain organizationally distinct.


## 7.2 Minimal Gene Evidence Fixture Schema

Required columns:

```text
sample_id
gene_id
gene_symbol
variant_count
rare_variant_count
high_impact_variant_count
pathogenic_variant_count
likely_pathogenic_variant_count
vus_variant_count
likely_benign_variant_count
benign_variant_count
max_variant_severity
quality_summary
variant_provenance_summary
gene_mapping_status
source_pipeline
run_id
```

## 7.3 Minimal GSC Overlay Fixture Schema

Required columns:

```text
phenotype
gene_id
gene_symbol
consensus_score
semantic_consensus_score
source_count
weighted_source_sum
semantic_channel_summary
source_list
active_score
scoring_profile
gsc_version
release_id
run_id
provenance_id
```

## 7.4 Edge-Case Fixture Requirements

At minimum, fixtures should include:

- a strong sample-specific candidate with GSC support
- a strong sample-specific candidate without GSC support
- a GSC-supported gene with weak sample evidence
- a gene with missing optional RSP evidence
- a gene with ambiguous mapping
- a gene with conflicting annotation state
- a gene with low-quality evidence
- a gene with `variant_count = 0`
- a gene with variant evidence unavailable or not evaluated
- a novel under-characterized candidate with strong sample evidence but sparse priors

---

# 8. Pipeline Architecture

RDGP v1 should use a small staged pipeline.

Recommended stages:

```text
stage_01_load_config
stage_02_validate_inputs
stage_03_load_gene_evidence
stage_04_attach_gsc_overlay
stage_05_build_evidence_matrix
stage_06_compute_scores
stage_07_compute_confidence
stage_08_rank_genes
stage_09_generate_explanations
stage_10_write_outputs
stage_11_validate_outputs
```

The implementation may expose these as functions/modules rather than standalone numbered scripts, but logs and validation reports should preserve stage names.

---

# 9. Module Plan

## 9.1 `config.py`

Responsibilities:

- load YAML configuration
- validate required config sections
- resolve paths
- assign or accept `run_id`
- expose immutable config object

Key tests:

- missing config section fails clearly
- selected phenotype required when GSC overlay enabled
- paths resolve correctly

---

## 9.2 `io.py`

Responsibilities:

- read TSV inputs
- write TSV outputs
- enforce tabular formats
- preserve explicit missing values
- avoid implicit type coercion that collapses null states

Key tests:

- missing fields detected
- explicit null-state values preserved
- output columns written deterministically

---

## 9.3 `schemas.py`

Responsibilities:

- define required input schemas
- define output schema
- define allowed values for key status fields
- provide schema validation helpers

Key schema groups:

- gene evidence schema
- GSC overlay schema
- functional evidence schema placeholder
- prioritized genes output schema
- evidence items schema
- validation report schema

---

## 9.4 `validators.py`

Responsibilities:

- enforce schema validation
- enforce identity preservation
- detect silent row multiplication
- validate null-state distinctions
- validate provenance fields
- validate confidence/score separation
- validate required output fields

Key tests:

- `missing` does not equal `zero_observed`
- `no_gsc_match` does not become contradiction
- confidence fields remain separate from score fields
- row counts remain explainable after joins

---

## 9.5 `evidence.py`

Responsibilities:

- represent evidence categories and statuses
- normalize evidence/status labels
- preserve evidence taxonomy fields
- construct long-form evidence records where feasible

Do not collapse:

- evidence category
- evidence scope
- evidence direction
- evidence strength
- evidence confidence
- evidence quality
- evidence status

into one enum.

---

## 9.6 `gsc_overlay.py`

Responsibilities:

- attach phenotype-scoped GSC overlays
- require explicit `selected_phenotype`
- prefer `gene_id` joins
- allow gene-symbol fallback only when configured
- emit `gsc_overlay_status`
- prevent silent row multiplication

Strict-mode behavior should require stable `gene_id` joins by default.

Fallback to `gene_symbol` should require explicit configuration enablement and should emit visible mapping-status flags.

Required statuses:

```text
matched_gene_id
matched_gene_symbol
no_gsc_match
ambiguous_gene_mapping
unsupported_phenotype_context
```

---

## 9.7 `scoring.py`

Responsibilities:

- compute transparent score components
- implement strongest-hit anchoring
- implement bounded additive support
- apply GSC guardrails
- avoid missing-evidence penalties
- preserve intermediate score fields
- avoid hidden weights

Initial score components:

```text
variant_evidence_score
gsc_prior_score
functional_evidence_score
priority_score
```

Implementation should remain profile-driven.

---

## 9.8 `confidence.py`

Responsibilities:

- compute qualitative confidence fields
- preserve confidence separate from score
- preserve confidence sources/modifiers
- avoid confidence-score collapse
- distinguish orthogonal convergence from redundant agreement where possible
- emit human-readable confidence explanation

Initial confidence fields:

```text
confidence_state
confidence_tier
confidence_sources
confidence_modifiers
confidence_flags
confidence_explanation
confidence_completeness
confidence_limitations
```

Confidence should remain qualitative-first in v1.

---

## 9.9 `ranking.py`

Responsibilities:

- assign deterministic ranks
- define deterministic tie-breaking
- preserve stable ordering
- avoid nondeterministic sorting

Recommended tie-breakers:

```text
priority_score descending
confidence_tier ordered
variant_evidence_score descending
gsc_prior_score descending
gene_symbol ascending
gene_id ascending
```

Tie-breaking must be documented.

---

## 9.10 `explainability.py`

Responsibilities:

- create `evidence_summary`
- create `provenance_summary`
- create confidence explanations
- expose missing/uncertain/conflicting evidence states

Every ranked gene should explain:

- why it ranked
- what evidence contributed
- what evidence was missing
- what evidence was uncertain
- what confidence limitations exist

---

## 9.11 `provenance.py`

Responsibilities:

- preserve source names
- preserve source versions
- preserve upstream run IDs
- preserve selected phenotype
- preserve scoring profile
- preserve RDGP run ID
- assemble provenance summaries

---

## 9.12 `manifest.py`

Responsibilities:

- write `run_manifest.yaml`
- record input paths
- record output paths
- record config path
- record selected phenotype
- record scoring profile
- record validation profile
- record run ID
- record timestamp
- record software/package versions where feasible

---

## 9.13 `logging_utils.py`

Responsibilities:

- initialize per-run log path
- log pipeline stages
- log validation summaries
- log warnings and explicit degradations
- log output locations

---

# 10. Scoring Implementation Plan

## 10.1 v1 Scoring Philosophy

RDGP scoring follows:

```text
strong evidence anchors;
weak evidence supports;
uncertainty remains visible;
confidence remains reconstructable;
provenance remains traceable.
```

## 10.2 Initial Scoring Components

Recommended initial components:

| Component | Meaning |
|---|---|
| `variant_evidence_score` | sample-specific evidence score |
| `gsc_prior_score` | phenotype-scoped prior score |
| `functional_evidence_score` | optional functional/RSP evidence score |
| `priority_score` | calibrated composite prioritization score |

Initial v1 scoring profiles should use biologically meaningful qualitative tiers mapped into small bounded numeric components for deterministic ranking behavior.

> Qualitative biological interpretation should remain the conceptual **source of truth**, while bounded numeric representations should remain implementation-facing ranking helpers.

The implementation must avoid unbounded raw additive scoring behavior.

## 10.3 Variant Evidence Score

Variant evidence should be severity-anchored.

Possible v1 logic:

- use `max_variant_severity` as strongest-hit anchor
- add bounded support from:
  - rare variant count
  - high-impact count
  - pathogenic/likely pathogenic count
  - VUS count with low/bounded contribution
- cap or saturate repeated weak evidence
- preserve component values

Do not allow raw `variant_count` alone to dominate.

## 10.4 GSC Prior Score

GSC support should be contextual and bounded.

Required guardrails:

- no GSC-only high-priority calls by default
- no GSC support does not penalize a gene
- GSC support remains phenotype-scoped
- raw GSC scale must be calibrated before combination
- GSC fields remain explainable

## 10.5 Functional Evidence Score

Functional evidence is optional in v1.

If absent:

```text
functional_evidence_score = null or not_evaluated
```

not:

```text
0 penalty
```

If present, it must preserve dataset/contrast scope.

## 10.6 Composite Priority Score

`priority_score` should combine calibrated components.

The implementation must not combine raw channel scales directly unless the profile explicitly calibrates them.

## 10.7 Missingness and Score

Missingness should not automatically reduce priority score unless explicitly justified.

Examples:

| Condition | Default score behavior |
|---|---|
| no GSC match | neutral |
| missing RSP evidence | neutral |
| missing ClinVar annotation | neutral |
| missing population frequency | not counted as rare |
| low-quality evidence | may dampen if profile specifies |
| contradictory evidence | may reduce cautiously |

---

# 11. Confidence Implementation Plan

## 11.1 v1 Confidence Philosophy

Confidence represents:

```text
interpretive reliability
```

not:

```text
disease probability
truth certainty
diagnostic certainty
```

## 11.2 Qualitative-First Confidence

Initial implementation should use qualitative confidence states, not probabilistic scores.

Initial v1 confidence tiers:

```text
high
moderate
limited
low
unresolved
```

Definitions should preserve semantic distinction between:

- limited evidence completeness
- low interpretive reliability
- unresolved ambiguity/conflict

> These tiers should remain qualitative-first in v1.

---

## 11.3 Confidence Inputs

Confidence may consider:

- gene mapping status
- QC / quality summary
- conflicting annotation state
- provenance completeness
- evidence completeness
- optional evidence availability
- GSC overlay status
- orthogonal convergence
- source redundancy indicators when available

## 11.4 Confidence Outputs

Minimum confidence outputs:

```text
confidence_state
confidence_tier
confidence_flags
confidence_explanation
confidence_completeness
confidence_limitations
```

Preferred later outputs:

```text
confidence_sources
confidence_modifiers
confidence_scope
confidence_provenance
confidence_propagation_source
confidence_reproducibility
```

## 11.5 Confidence Anti-Collapse Rules

Implementation must not:

- use confidence as hidden score suppression
- collapse confidence into uncertainty
- collapse confidence into plausibility
- treat novelty as low confidence by default
- treat sparse priors as contradiction
- inflate confidence from redundant evidence
- output an unexplained confidence scalar

## 11.6 Confidence Validation

Tests must verify:

- high score can coexist with reduced confidence
- low score can coexist with high confidence
- missing optional evidence does not automatically create low confidence
- ambiguous mapping reduces mapping confidence and triggers flags
- conflicting annotations produce warnings
- redundant evidence does not automatically inflate confidence
- confidence explanations are reconstructable

---

# 12. Output Plan

## 12.1 Output Directory

Runtime outputs should follow:

```text
results/runs/<run_id>/
├── run_manifest.yaml
├── tables/
│   ├── prioritized_genes.tsv
│   ├── gene_evidence_matrix.tsv
│   └── evidence_items.tsv
└── reports/
    └── validation_report.md
```

Logs should follow:

```text
logs/<run_id>/pipeline.log
```

## 12.2 Primary Output: `prioritized_genes.tsv`

Minimum columns:

```text
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
```

## 12.3 Secondary Output: `gene_evidence_matrix.tsv`

Should include all primary output fields plus intermediate scoring fields, raw counts, calibrated components, and semantic status fields.

## 12.4 Secondary Output: `evidence_items.tsv`

Should preserve evidence-level long-form records where feasible.

`evidence_items.tsv` is optional in early v1 implementations while long-form evidence modeling matures.

However, the architecture should preserve compatibility with future evidence-level expansion.

Minimum conceptual fields:

```text
evidence_id
sample_id
gene_id
gene_symbol
evidence_category
evidence_subtype
evidence_scope
evidence_role
evidence_direction
evidence_strength
evidence_confidence
evidence_quality
evidence_status
source_name
source_version
source_record_id
provenance_id
run_id
selected_phenotype
gene_mapping_status
```

## 12.5 Validation Report

`validation_report.md` should summarize:

- schema validation
- interface validation
- semantic anti-collapse validation
- scoring behavior validation
- confidence validation
- provenance validation
- reproducibility validation
- warnings
- explicit degradations
- pass/fail status

RDGP should generate both:

- a human-readable Markdown validation report
- a machine-readable YAML validation summary

Markdown supports review, interpretation, and portfolio readability.

YAML supports automated validation checks, regression testing, and future CI-compatible workflows.

This cleanly separates:

```text
human auditability (MD)
vs
machine interoperability (YAML)
```

---

# 13. Validation Implementation Plan

## 13.1 Validation Layers

RDGP validation should include:

1. Schema validation
2. Interface validation
3. Semantic validation
4. Scoring validation
5. Confidence validation
6. Explainability validation
7. Provenance validation
8. Reproducibility validation
9. Perturbation validation
10. Edge-case validation

## 13.2 Minimal Must-Pass Tests

RDGP v1 must test:

- `(sample_id, gene_id)` identity preservation
- no silent row multiplication after GSC overlay
- missing GSC support is not negative evidence
- missing RSP evidence is not a score penalty
- missing population frequency is not interpreted as rare
- unsupported is not contradictory
- unresolved is not silently resolved
- confidence is distinct from score
- confidence is distinct from uncertainty
- confidence reductions are explainable
- redundant evidence does not automatically inflate confidence
- provenance is retained
- explainability fields are present
- deterministic ranking is reproducible

## 13.3 Fixture-Based Validation Scenarios

Initial validation fixtures should include:

| Scenario | Purpose |
|---|---|
| known-gene recovery | sanity check |
| discovery-preservation candidate | prevents prior-dominance |
| no GSC match | tests neutral missing prior |
| missing RSP evidence | tests optional evidence behavior |
| ambiguous mapping | tests confidence + warning |
| conflicting annotation | tests conflict preservation |
| low-quality evidence | tests reliability behavior |
| zero observed vs missing evidence | tests null semantics |
| GSC-only support | tests GSC guardrail |
| repeated weak evidence | tests bounded accumulation |

---

# 14. Makefile Plan

Recommended targets:

```make
setup
test
test-unit
test-integration
test-validation
run-example
validate-example
clean-results
```

Initial behavior:

| Target | Purpose |
|---|---|
| `make setup` | create or document environment setup |
| `make test` | run all pytest tests |
| `make test-unit` | unit tests only |
| `make test-integration` | integration tests only |
| `make test-validation` | semantic validation tests only |
| `make run-example` | run fixture/example pipeline |
| `make validate-example` | validate generated example outputs |
| `make clean-results` | remove generated runtime outputs only |

---

# 15. Requirements Plan

Initial `requirements.txt` should remain lightweight.

Likely dependencies:

```text
pandas
pyyaml
pytest
```

Optional later:

```text
pydantic
pandera
rich
```

Recommendation:

- start with minimal dependencies
- avoid heavy frameworks
- add schema libraries only if they provide clear value
- keep portfolio reproducibility simple

---

# 16. Development Sequence

## Commit 1 — Contract and Plan

Files:

```text
docs/contracts/system_contract.md
docs/plans/implementation_plan.md
```

Goal:

- freeze design-control artifacts

## Commit 2 — Repo Scaffold Alignment

Files/directories:

```text
config/
config/scoring_profiles/
config/validation_profiles/
logs/
results/runs/
tests/unit/
tests/integration/
tests/validation/
tests/fixtures/
src/rdgp/
requirements.txt
Makefile
.gitignore
```

Goal:

- establish implementation scaffold

## Commit 3 — Fixtures and Schemas

Files:

```text
tests/fixtures/*.tsv
src/rdgp/schemas.py
src/rdgp/validators.py
tests/unit/test_schemas.py
tests/validation/test_semantic_states.py
```

Goal:

- define and validate data contracts before scoring

## Commit 4 — Config and IO

Files:

```text
src/rdgp/config.py
src/rdgp/io.py
config/config.yaml
tests/unit/test_config.py
tests/unit/test_io.py
```

Goal:

- deterministic config loading and TSV IO

## Commit 5 — GSC Overlay

Files:

```text
src/rdgp/gsc_overlay.py
tests/unit/test_gsc_overlay.py
tests/validation/test_no_silent_row_multiplication.py
tests/validation/test_no_gsc_match.py
```

Goal:

- phenotype-scoped overlay with identity preservation

## Commit 6 — Scoring Engine

Files:

```text
src/rdgp/scoring.py
config/scoring_profiles/default_v1.yaml
tests/unit/test_scoring.py
tests/validation/test_scoring_guardrails.py
```

Goal:

- transparent score components and guardrails

## Commit 7 — Confidence Engine

Files:

```text
src/rdgp/confidence.py
tests/unit/test_confidence.py
tests/validation/test_confidence_anti_collapse.py
```

Goal:

- qualitative confidence fields and explanations

## Commit 8 — Ranking and Explainability

Files:

```text
src/rdgp/ranking.py
src/rdgp/explainability.py
tests/unit/test_ranking.py
tests/unit/test_explainability.py
```

Goal:

- deterministic ranking and human-readable summaries

## Commit 9 — Pipeline Runner and Manifest

Files:

```text
scripts/run_pipeline.py
src/rdgp/manifest.py
src/rdgp/logging_utils.py
tests/integration/test_run_example.py
```

Goal:

- end-to-end example run

## Commit 10 — Validation Report

Files:

```text
src/rdgp/validators.py
scripts/validate_inputs.py
tests/validation/
```

Goal:

- validation report and semantic invariant checks

## Commit 11 — Documentation and README Update

Files:

```text
README.md
docs/workflow.md
docs/data_schema.md
docs/architecture.md
```

Goal:

- make repo externally legible

---

# 17. Implementation Gate

Do not begin code implementation until:

- `system_contract.md` has been reviewed and accepted
- `implementation_plan.md` has been reviewed and accepted
- confidence framework has been integrated into the system contract
- minimal scoring profile behavior is agreed
- minimal validation fixture strategy is agreed
- user approves implementation transition

---

# 18. Assumptions

- RDGP v1 can be built before live VDB/RSP availability using interface-compatible fixtures.
- GSC overlay behavior can be tested using synthetic phenotype-scoped overlays.
- Confidence modeling remains qualitative-first in v1.
- Exact numerical scoring weights may be conservative placeholders if clearly documented and config-driven.
- Validation should be implemented early, not retrofitted.
- Example data should be tiny, synthetic, and Git-safe.

---

# 19. Limitations

- This plan does not define final biological scoring weights.
- This plan does not implement direct VDB SQL integration.
- This plan does not implement RSP integration beyond optional schema placeholders.
- This plan does not implement full inheritance modeling.
- This plan does not implement full noncoding or mitochondrial logic.
- This plan assumes a single selected phenotype context for v1.
- This plan does not replace future scoring contract refinement.

---

# 20. Open Questions Before Implementation

These should be resolved before or during early implementation planning:

1. Should scoring and confidence contracts remain embedded within the primary system contract for v1, or be versioned separately later?

2. Should future phenotype-context expansion introduce:
   - multi-phenotype reasoning
   - phenotype-prior weighting
   - phenotype-specific scoring profiles?

3. What future inheritance-aware evidence structures should be introduced after v1 stabilization?

4. Should future RSP integration support:
   - transcriptomic overlays only
   - network convergence overlays
   - pathway-level overlays
   - all three?

5. When should noncoding reasoning contracts become implementation-blocking rather than future-facing?

---

# 21. Recommended Immediate Next Step

After review of this implementation plan:

1. Commit the updated `system_contract.md`.
2. Commit this `implementation_plan.md`.
3. Decide whether to create a separate `scoring_contract.md`.
4. Align the repo scaffold.
5. Build fixtures and schema validators before scoring code.

---

# 22. Definition of v1 Implementation Success

RDGP v1 implementation succeeds when:

- fixture inputs validate correctly
- GSC overlay preserves identity and phenotype context
- no silent row multiplication occurs
- semantic states remain distinct
- confidence remains distinct from score
- missing optional evidence does not penalize candidates
- scoring produces deterministic ranked outputs
- explanations are generated for each ranked gene
- provenance summaries are retained
- validation report confirms semantic invariants
- `make test` passes
- `make run-example` produces expected outputs

---

# 23. Summary

RDGP implementation should proceed through controlled, contract-bound, fixture-first development.

The guiding implementation principle is:

```text
build the semantic skeleton before adding scoring muscle
```

This protects RDGP from becoming a fragile ranking script and preserves its intended role as an explainable translational genomics reasoning framework.

# End of implementation_plan.md
