# RDGP System Contract

## Repository

`rare_disease_gene_prioritization` (`RDGP`)

## Artifact Type

DEX-owned system contract.

## Intended Placement

```text
rare_disease_gene_prioritization/docs/contracts/system_contract.md
```

## Contract Status

Draft v0.2 for review before implementation.

---

# 1. Purpose

This document defines the enforceable system contract for the `rare_disease_gene_prioritization` repository.

RDGP is the reasoning layer of the VitamOrdinatio translational bioinformatics ecosystem. It integrates upstream evidence into sample-scoped, gene-level prioritization outputs while preserving biological semantics, uncertainty, confidence, provenance, and interface boundaries.

This contract converts the SAGE-RDGP scientific governance stack into DEX-RDGP implementation constraints.

Governed scientific inputs include:

- `scoring_rationale.md`
- `evidence_taxonomy.md`
- `uncertainty_and_null_semantics.md`
- `validation_strategy.md`
- `confidence_modeling_framework.md`
- `inheritance_reasoning_framework.md`

---

# 2. Repository Role

RDGP answers:

```text
For a given sample, which genes are most strongly supported by available evidence, and why?
```

RDGP produces:

```text
sample-scoped gene prioritization
```

not:

```text
variant calling
variant annotation
persistent variant storage
gene-set construction
RNA-seq processing
clinical diagnosis
```

RDGP must remain an explainable, deterministic, review-oriented prioritization framework.

---

# 3. Ecosystem Boundary

| Repository | Owns | Primary Identity Space |
|---|---|---|
| `VAP` | variant calling and annotation | `(sample_id, variant_id)` |
| `VDB` | persistent variant/sample/gene/annotation storage | variant/sample/database entities |
| `GSC` | phenotype-scoped gene priors | `(phenotype, gene_id)` |
| `RSP` | transcriptomic and network evidence | `(dataset_id, contrast_id, gene_id)` |
| `RDGP` | sample-scoped gene reasoning | `(sample_id, gene_id)` |

RDGP must not collapse upstream identity spaces into an ambiguous universal evidence table.

---

# 4. Core Identity Model

RDGP's primary reasoning unit is:

```text
(sample_id, gene_id)
```

Each output row represents:

```text
one gene evaluated within one biological sample
```

If RDGP later evaluates multiple phenotypes per sample, the identity must explicitly expand to:

```text
(sample_id, selected_phenotype, gene_id)
```

This expansion must never occur silently.

---

# 5. System Invariants

The following invariants are mandatory.

## 5.1 Identity Invariant

RDGP outputs must preserve one row per `(sample_id, gene_id)` for a single selected phenotype context unless an explicitly documented expanded mode is enabled.

## 5.2 No Silent Row Multiplication

Joins to GSC, RSP, VDB-like inputs, or evidence tables must not silently multiply rows.

If one-to-many relationships exist, RDGP must either:

1. aggregate deterministically before scoring, or
2. emit an explicitly expanded evidence table separate from prioritized gene outputs.

## 5.3 Score / Confidence / Uncertainty Separation

RDGP must preserve separation between:

- `priority_score` or `composite_score`
- `confidence`
- `confidence_tier`
- `confidence_state`
- `uncertainty_state`
- `quality_flag`
- `evidence_strength`
- `evidence_direction`
- `biological_plausibility`
- `contradiction_state`

These must not collapse into one scalar.

`priority_score` represents prioritization strength.

`confidence` represents interpretive reliability.

`uncertainty_state` represents known ambiguity, incompleteness, unresolved interpretation, or epistemic limitation.

`quality_flag` represents technical or analytical reliability.

These concepts may interact, but they must remain independently explainable and operationally reconstructable.

## 5.4 Null and Missingness Invariant

RDGP must distinguish:

```text
missing
unknown
not_evaluated
unsupported
unresolved
ambiguous
conflicting
contradictory
low_quality
zero_observed
```

These states must not be silently converted to:

```text
0
False
benign
negative evidence
biological irrelevance
```

## 5.5 GSC Context Invariant

GSC evidence may only be attached when `selected_phenotype` is explicit.

GSC support represents phenotype-scoped prior evidence, not sample-specific biological evidence.

## 5.6 Optional Evidence Invariant

Optional evidence channels, including RSP-derived evidence, must not penalize genes when absent, unavailable, or not evaluated.

## 5.7 Provenance Invariant

Every prioritized output must preserve enough provenance to explain which upstream sources contributed to the ranking.

## 5.8 Explainability Invariant

Every prioritized gene must be able to answer:

- why did this gene rank?
- what evidence contributed?
- what evidence was missing?
- what evidence was uncertain?
- what evidence was conflicting?
- what scope did each evidence item have?
- what provenance supports each item?

## 5.9 Confidence Anti-Collapse Invariant

Confidence must remain explicit, explainable, semantically visible, independently auditable, and operationally reconstructable.

Confidence must not silently become:

- score suppression
- contradiction
- biological implausibility
- diagnosis certainty
- truth probability
- novelty penalty
- hidden probabilistic certainty

Confidence reductions must identify their source, such as:

- provenance limitation
- mapping instability
- transcript instability
- annotation conflict
- QC/reliability concern
- incomplete evaluation
- evidence missingness
- scope incoherence
- redundant/correlated evidence support

## 5.10 Confidence Is Not Consensus Invariant

Agreement among evidence sources must not automatically inflate confidence.

RDGP must distinguish:

```text
orthogonal evidence convergence
```

from:

```text
redundant or correlated source agreement
```

Repeated weak or derivative evidence must not create artificial confidence inflation.

---

## 5.11 Inheritance Compatibility Invariant

RDGP inheritance-aware reasoning must preserve distinction between:

- inheritance compatibility
- inheritance conflict
- inheritance uncertainty
- inheritance incompleteness
- inheritance confidence
- inheritance plausibility

Inheritance reasoning must remain:

- explainable
- semantically reconstructable
- biologically contextual
- uncertainty-aware
- deterministic
- validation-friendly

RDGP must reason primarily about:

```text
inheritance compatibility
```

rather than:

```text
inheritance certainty
```

Inheritance-aware reasoning must not silently collapse into:

- hidden score suppression
- deterministic diagnosis
- opaque plausibility penalties
- automatic exclusion logic

Missing inheritance evidence must not automatically imply contradiction, implausibility, or diagnostic exclusion.

---

# 6. Required Input Model

RDGP v1 may consume fixture-based tables before VDB and RSP are fully online.

The implementation must treat fixtures as interface-compatible stand-ins, not as final upstream systems.

## 6.1 Gene Evidence Input Model

Minimum input identity:

```text
(sample_id, gene_id)
```

---

### Required Core Fields

Required fields:

| Field | Required | Notes |
|---|---:|---|
| `sample_id` | yes | biological sample identifier |
| `gene_id` | conditionally required | preferred stable gene identifier; if absent, gene_symbol fallback must be explicitly enabled and gene_mapping_status must be fallback or unresolved |
| `gene_symbol` | yes | human-readable gene symbol |
| `variant_count` | yes | total retained observed variants, or explicit null state |
| `rare_variant_count` | yes | must not treat missing frequency as rare |
| `high_impact_variant_count` | yes | high-impact variant burden |
| `pathogenic_variant_count` | yes | after annotation conflict handling |
| `likely_pathogenic_variant_count` | yes | after annotation conflict handling |
| `vus_variant_count` | yes | VUS count |
| `likely_benign_variant_count` | yes | likely benign count |
| `benign_variant_count` | yes | benign count |
| `max_variant_severity` | yes | strongest observed variant consequence/severity |
| `quality_summary` | yes | sample-gene QC/reliability status |
| `variant_provenance_summary` | yes | upstream evidence summary |
| `gene_mapping_status` | yes | stable/fallback/ambiguous/missing |
| `source_pipeline` | yes | e.g., VAP/VDB fixture |
| `run_id` | yes | upstream or aggregation run provenance |

---

### Optional Inheritance-Aware Fields

Optional fields:

| Field                     | Required | Notes                                           |
| ------------------------- | -------: | ----------------------------------------------- |
| `inheritance_mode`        | optional | conceptual inheritance interpretation context   |
| `zygosity_context`        | optional | biological zygosity interpretation              |
| `inheritance_uncertainty` | optional | unresolved inheritance ambiguity                |
| `heteroplasmy_context`    | optional | mitochondrial burden interpretation placeholder |

---

## 6.2 Optional GSC Overlay Input

GSC input must be phenotype-scoped.

Minimum identity:

```text
(selected_phenotype, gene_id)
```

Required fields when used:

| Field | Required | Notes |
|---|---:|---|
| `phenotype` | yes | selected phenotype context |
| `gene_id` | yes | preferred join key |
| `gene_symbol` | yes | fallback join key only when gene_id unavailable |
| `consensus_score` | yes | raw GSC score |
| `semantic_consensus_score` | preferred | semantic score when available |
| `source_count` | preferred | number of supporting sources |
| `weighted_source_sum` | preferred | weighted source support |
| `semantic_channel_summary` | preferred | evidence channel explanation |
| `source_list` | yes | source provenance |
| `active_score` | preferred | selected GSC score field |
| `scoring_profile` | yes | GSC scoring profile |
| `gsc_version` | yes | GSC version |
| `release_id` | yes | GSC release identifier |
| `run_id` | yes | GSC run provenance |
| `provenance_id` | preferred | source-level provenance |

## 6.3 Optional Functional/RSP Input

RSP-derived evidence is optional for v1.

If present, RDGP must preserve:

| Field | Required | Notes |
|---|---:|---|
| `dataset_id` | yes | RSP dataset identity |
| `contrast_id` | yes | RSP contrast identity |
| `gene_id` | yes | join key |
| `functional_evidence_type` | yes | expression/network/pathway/etc. |
| `functional_support` | yes | calibrated or raw support field |
| `evidence_scope` | yes | cohort/dataset/sample-specific distinction |
| `method` | yes | RSP or convergence method |
| `run_id` | yes | upstream run provenance |
| `provenance_id` | preferred | source provenance |

RSP evidence must not be treated as patient-specific unless explicitly encoded as patient-specific by a future interface.

---

# 7. Join Rules

## 7.1 RDGP Base Table

RDGP begins from a gene-level evidence table keyed by:

```text
(sample_id, gene_id)
```

## 7.2 GSC Join

Preferred join:

```sql
RDGP.gene_id = GSC.gene_id
AND
GSC.phenotype = selected_phenotype
```

Fallback join:

```sql
RDGP.gene_symbol = GSC.gene_symbol
AND
GSC.phenotype = selected_phenotype
```

Fallback joins must be explicitly flagged.

Required overlay status values:

| Status | Meaning |
|---|---|
| `matched_gene_id` | joined by stable gene ID |
| `matched_gene_symbol` | joined by fallback gene symbol |
| `no_gsc_match` | no phenotype-prior support found |
| `ambiguous_gene_mapping` | unresolved gene identity conflict |
| `unsupported_phenotype_context` | selected phenotype unavailable or unsupported |

## 7.3 Functional Evidence Join

Functional evidence joins must preserve dataset/contrast scope and must not be treated as direct sample evidence unless explicitly specified.

---

# 8. Required Output Model

## 8.1 Primary Output

Recommended primary output:

```text
results/tables/prioritized_genes.tsv
```

---

### Required Fields

| Field | Required | Notes |
|---|---:|---|
| `sample_id` | yes | primary identity |
| `gene_id` | yes | primary identity |
| `gene_symbol` | yes | display label |
| `selected_phenotype` | yes when GSC used | phenotype context |
| `rank` | yes | deterministic rank |
| `priority_score` | yes | prioritization strength |
| `confidence_tier` | yes | qualitative interpretive reliability tier |
| `confidence_state` | yes | primary confidence interpretation |
| `confidence_explanation` | yes | human-readable explanation of confidence behavior |
| `confidence_flags` | yes | review-triggering confidence limitations |
| `variant_evidence_score` | yes | sample-specific variant component |
| `gsc_prior_score` | yes when GSC used | phenotype-scoped prior component |
| `functional_evidence_score` | optional | RSP/functional component |
| `uncertainty_state` | yes | primary uncertainty state |
| `evidence_status_summary` | yes | missing/unsupported/conflicting/etc. |
| `quality_flag` | yes | reliability/QC summary |
| `gsc_overlay_status` | yes when GSC used | GSC join state |
| `gene_mapping_status` | yes | stable/fallback/ambiguous/missing |
| `evidence_summary` | yes | human-readable explanation |
| `provenance_summary` | yes | upstream traceability |
| `run_id` | yes | RDGP run identifier |

---

### Optional Fields

| Field | Required | Notes |
|---|---:|---|
| `inheritance_support` | optional | inheritance compatibility interpretation |
| `inheritance_conflict` | optional | inheritance plausibility tension |
| `inheritance_explanation` | optional | explainable inheritance reasoning |
| `inheritance_uncertainty` | optional | unresolved inheritance ambiguity |

---

## 8.2 Secondary Outputs

Recommended secondary outputs:

```text
results/tables/gene_evidence_matrix.tsv
results/tables/evidence_items.tsv
results/reports/validation_report.md
results/run_manifest.yaml
logs/<run_id>/pipeline.log
```

`gene_evidence_matrix.tsv` should preserve intermediate scoring and evidence-channel fields.

`evidence_items.tsv` should preserve evidence-level records where feasible.

`run_manifest.yaml` should record configuration, input files, run IDs, selected phenotype, scoring profile, and software/environment metadata.

---

# 9. Scoring Contract Requirements

RDGP v1 scoring must follow SAGE-RDGP scoring governance.

## 9.1 Conceptual Scoring Rule

RDGP follows:

```text
strong evidence anchors;
weak evidence supports;
uncertainty remains visible.
```

## 9.2 Required Behavior

Scoring must support:

- deterministic outputs
- strongest-hit anchoring
- bounded additive support
- diminishing returns for repeated weak evidence
- GSC influence guardrails
- optional functional evidence
- raw scale calibration before channel combination
- preserved intermediate score components

## 9.3 Prohibited Behavior

Scoring must not:

- rely on hidden weights
- treat GSC support as sample-specific evidence
- allow GSC-only high-priority calls by default
- penalize missing GSC support by default
- penalize missing RSP support by default
- treat missing population frequency as rare
- merge confidence into score
- allow unbounded raw burden inflation
- convert uncertainty into automatic contradiction
- silently convert inheritance incompatibility into hidden score penalties

## 9.4 Scoring Profiles

RDGP should support scoring profiles through configuration.

A scoring profile should define:

- evidence channel enablement
- channel calibration behavior
- channel caps
- scoring weights or tiers if used
- confidence behavior if implemented
- uncertainty handling behavior
- output fields

Exact numerical values must be documented and versioned.

---

# 10. Confidence Contract Requirements

RDGP confidence behavior is governed by `confidence_modeling_framework.md`.

## 10.1 Confidence Definition

Confidence represents:

```text
interpretive reliability
```

not:

```text
biological truth certainty
disease probability
clinical diagnosis certainty
Bayesian posterior probability
causal certainty
clinical actionability
```

Confidence helps answer:

```text
How much interpretive trust should be placed in this prioritization result?
```

Score helps answer:

```text
Why did this gene rank highly?
```

These concepts must remain distinct.

## 10.2 Confidence-First Semantic Rule

Confidence should primarily influence:

- interpretive caution
- review prioritization
- uncertainty visibility
- explainability
- auditability
- evidence transparency

before influencing:

- prioritization score
- biological plausibility

Reliability-affecting evidence should generally affect confidence before score.

Plausibility-affecting evidence requires stronger biological justification and must remain semantically distinct from reliability reduction.

## 10.3 Confidence Dimensionality

Confidence may emerge from multiple semantically distinct reliability dimensions, including:

- provenance confidence
- mapping confidence
- annotation confidence
- QC confidence
- inheritance confidence
- reproducibility confidence
- completeness confidence
- scope coherence confidence
- convergence confidence
- inheritance compatibility confidence

RDGP v1 does not require formal multidimensional confidence modeling.

However, implementation must preserve enough semantic structure to allow future confidence dimensionality without ontology collapse.

## 10.4 Confidence Propagation

Confidence must propagate semantically rather than through generic penalties.

Examples:

| Upstream condition | Downstream confidence behavior |
|---|---|
| unresolved transcript mapping | reduced consequence confidence |
| unstable gene mapping | unresolved gene-level confidence |
| conflicting assertions | confidence reduction + warning |
| poor QC | reliability reduction |
| missing optional transcriptomics | completeness limitation |
| unresolved inheritance | inheritance-confidence reduction |

Propagation must preserve the source and meaning of confidence effects.

Confidence behavior must not collapse into generic low confidence or hidden score suppression.

## 10.5 Confidence and Missingness

Missingness may affect evidence completeness or interpretive certainty, but missing optional evidence must not automatically imply:

- biological implausibility
- contradiction
- irrelevance
- low ranking
- diagnostic exclusion

Examples:

- missing RSP evidence may create a completeness limitation, not a biological penalty
- no ClinVar annotation may represent sparse prior knowledge, not benignity
- no GSC overlap may represent lack of phenotype-prior support, not negative evidence

## 10.6 Confidence Is Not Consensus

RDGP must distinguish orthogonal convergence from redundant agreement.

Orthogonal convergence may strengthen confidence when independent evidence layers support the same interpretation.

Redundant agreement must not automatically inflate confidence.

Examples of redundant agreement include:

- derivative databases
- repeated ontology mappings
- correlated prediction systems
- multiple annotations derived from one upstream source
- duplicated literature propagation

## 10.7 Required Confidence Output Semantics

RDGP outputs should preserve confidence information through fields such as:

| Field | Required | Purpose |
|---|---:|---|
| `confidence_state` | yes | primary confidence interpretation |
| `confidence_tier` | yes | qualitative confidence label |
| `confidence_sources` | preferred | contributors affecting confidence |
| `confidence_modifiers` | preferred | conditions altering confidence |
| `confidence_explanation` | yes | human-readable explanation |
| `confidence_scope` | preferred | scope context for confidence reasoning |
| `confidence_flags` | yes | review-triggering confidence limitations |
| `confidence_provenance` | preferred | provenance affecting confidence |
| `confidence_propagation_source` | preferred | upstream uncertainty dependency |
| `confidence_completeness` | preferred | evidence completeness indicator |
| `confidence_limitations` | preferred | unresolved or cautionary conditions |

Exact field implementation may be refined in `implementation_plan.md`, but confidence semantics must remain reconstructable.

## 10.8 Prohibited Confidence Behavior

RDGP must not:

- merge confidence into priority score
- represent confidence only as an unexplained scalar
- use confidence as hidden score suppression
- treat sparse evidence as biological implausibility
- treat novelty as low confidence by default
- inflate confidence from redundant source agreement
- convert uncertainty into scalar confidence without explanation
- use pseudo-probabilistic language unsupported by implementation

## 10.9 Confidence Validation Requirements

Validation must verify that:

- confidence remains distinct from score
- confidence remains distinct from uncertainty
- confidence remains distinct from plausibility
- confidence reductions are explainable
- confidence propagation is semantically interpretable
- confidence is reproducible for identical inputs/configuration
- missing optional evidence does not excessively suppress confidence
- redundant evidence does not artificially inflate confidence
- confidence explanations remain reconstructable

---

# 11. Null, Missingness, and Uncertainty Contract

RDGP must preserve the following semantic states where applicable:

| State | Meaning | Default Score Effect | Default Confidence Effect |
|---|---|---|---|
| `unknown` | insufficient knowledge | neutral | may reduce certainty |
| `missing` | expected source absent | neutral | may reduce completeness |
| `not_evaluated` | workflow did not assess | neutral | flags incomplete run |
| `unsupported` | evaluated, no support found | neutral by default | context-dependent |
| `unresolved` | ambiguity not resolved | usually neutral | reduces confidence |
| `ambiguous` | multiple plausible interpretations | usually neutral | reduces confidence |
| `conflicting` | sources disagree | usually neutral | reduces confidence/warning |
| `contradictory` | plausibility-reducing evidence | may reduce score cautiously | reduces confidence |
| `low_quality` | unreliable evidence | may dampen score | reduces confidence |
| `zero_observed` | evaluated and count is zero | zero for that count | not missing |

Implementation must not collapse these states during aggregation, scoring, serialization, export, or validation.

---

# 12. Evidence Taxonomy Contract

RDGP evidence records should preserve independent taxonomy dimensions.

Recommended fields:

| Field | Purpose |
|---|---|
| `evidence_category` | top-level evidence class |
| `evidence_subtype` | specific evidence type |
| `evidence_scope` | sample/phenotype/cohort/external/system scope |
| `evidence_role` | direct, prior, functional, coherence, reliability-modifying |
| `evidence_direction` | positive, neutral/contextual, reliability-reducing, contradictory |
| `evidence_strength` | qualitative or calibrated strength |
| `evidence_confidence` | reliability tier independent of strength |
| `confidence_state` | primary confidence interpretation when evidence affects confidence |
| `confidence_scope` | scope context for confidence reasoning |
| `confidence_flags` | confidence-related review flags |
| `evidence_quality` | QC/reliability state |
| `evidence_status` | present/missing/not_evaluated/unsupported/etc. |
| `source_name` | source system or database |
| `source_version` | source version |
| `source_record_id` | upstream identifier |
| `provenance_id` | internal provenance reference |
| `run_id` | source or RDGP run |
| `selected_phenotype` | required for phenotype-scoped evidence |
| `gene_mapping_status` | stable/fallback/ambiguous/missing |

These fields may be implemented in long-form evidence tables, intermediate matrices, or serialized structured columns, but the semantics must remain recoverable.

---

# 13. Validation Contract

RDGP validation must verify semantic behavior, not just runtime correctness.

## 13.1 Minimal v1 Validation Requirements

RDGP v1 must verify:

1. `(sample_id, gene_id)` identity is preserved.
2. GSC no-match is not treated as negative evidence.
3. Missing RSP evidence does not penalize genes.
4. Confidence remains distinct from score.
5. Confidence remains distinct from uncertainty, quality, plausibility, and contradiction.
6. Confidence reductions remain explainable and reconstructable.
7. Redundant evidence does not automatically inflate confidence.
8. Missing optional evidence does not automatically suppress confidence or score.
9. Missing, unsupported, unresolved, conflicting, contradictory, low-quality, and zero-observed states remain distinct.
10. Provenance is retained for each evidence source.
11. Evidence scope is retained.
12. Known-gene recovery is assessed as a sanity check.
13. At least one discovery-preservation scenario is tested.
14. At least one perturbation scenario is tested.
15. At least one edge-case scenario is tested.
16. Explainability fields are present for ranked genes.
17. inheritance compatibility/conflict semantics remain distinguishable
18. missing inheritance evidence does not become contradiction
19. mitochondrial inheritance context remains distinguishable from Mendelian inheritance context
20. unresolved inheritance remains visible and explainable

## 13.2 Required Test Categories

Recommended test layers:

```text
tests/unit/
tests/integration/
tests/validation/
tests/fixtures/
```

Validation classes:

- schema validation
- interface validation
- semantic anti-collapse validation
- scoring behavior validation
- score/confidence separation validation
- confidence/uncertainty/plausibility separation validation
- confidence explainability validation
- confidence propagation validation
- redundant-evidence confidence inflation validation
- GSC no-match validation
- missing optional evidence validation
- ambiguity/conflict validation
- provenance retention validation
- deterministic reproducibility validation
- discovery-preservation validation
- known-gene recovery sanity validation

---

# 14. Failure Modes

RDGP must fail clearly or degrade explicitly under known failure modes.

## 14.1 Hard-Fail Conditions

RDGP should fail with clear validation errors when:

- required input identity fields are missing
- `sample_id` is missing from sample-scoped evidence
- both `gene_id` and acceptable `gene_symbol` fallback are missing
- selected phenotype is required but absent
- input schema is incompatible with declared profile
- row multiplication occurs unexpectedly
- required provenance fields are absent in strict mode
- required config fields are absent

## 14.2 Explicit-Degradation Conditions

RDGP may continue with warnings when:

- GSC overlay is unavailable
- RSP evidence is unavailable
- optional evidence channels are disabled
- gene mapping falls back to symbol
- gene mapping is ambiguous but preserved
- confidence is limited by ambiguity, conflict, missingness, or incomplete evaluation
- noncoding evidence lacks strong assignment
- structural variant support is incomplete
- mitochondrial heteroplasmy data is unavailable

Degradation must be visible in outputs, logs, and/or validation reports.

---

# 15. Configuration Contract

RDGP should be configuration-driven.

Required configuration concepts:

- selected phenotype
- input paths
- output paths
- scoring profile
- enabled evidence channels
- strict vs permissive validation mode
- GSC overlay behavior
- optional RSP behavior
- null-state handling
- confidence behavior
- confidence output fields
- confidence propagation behavior
- confidence validation behavior
- run metadata

Example future config files:

```text
config/config.yaml
config/scoring_profiles/default_v1.yaml
config/validation_profiles/default_v1.yaml
```

No core path or score parameter should be hard-coded.

---

# 16. Logging and Run Manifest Contract

Each RDGP run must generate:

- a unique `run_id`
- a log file
- a run manifest
- input file records
- configuration records
- selected phenotype record
- scoring profile record
- evidence-channel enablement record
- validation summary
- software/environment metadata when feasible

Recommended paths:

```text
logs/<run_id>/pipeline.log
results/runs/<run_id>/run_manifest.yaml
results/runs/<run_id>/tables/
results/runs/<run_id>/reports/
```

---

# 17. Implementation Gate

DEX-RDGP must not begin functional implementation until:

- this system contract is reviewed
- `docs/plans/implementation_plan.md` is reviewed
- minimal scoring interface is agreed
- minimal validation expectations are agreed
- confidence modeling framework has been integrated into this contract and implementation plan
- user approves transition from design to implementation

---

# 18. Assumptions

- RDGP v1 will start with fixture-compatible inputs before full VDB/RSP integration.
- GSC support is available or can be represented through fixture overlays.
- RDGP v1 prioritizes deterministic explainability over predictive sophistication.
- Optional evidence channels are non-penalizing when absent.
- All scoring behavior must remain auditable.
- The repo will follow the existing portfolio architecture and one-repo-one-venv discipline.

---

# 19. Limitations

- RDGP v1 is heuristic and not diagnostic.
- Confidence modeling is qualitative-first in v1 and governed by `confidence_modeling_framework.md`.
- Inheritance modeling may be incomplete in v1.
- Noncoding interpretation may remain placeholder-level in v1.
- Mitochondrial heteroplasmy may remain placeholder-level in v1.
- RSP integration is optional and future-facing.
- VDB may not yet exist as a live upstream database.

---

# 20. Edge Cases To Preserve

RDGP must explicitly preserve or flag:

- ambiguous gene mapping
- missing gene identifiers
- fallback gene-symbol joins
- no GSC match
- unsupported phenotype context
- missing optional evidence channels
- conflicting pathogenicity assertions
- conflicting transcript consequences
- low-quality variant evidence
- missing population frequency
- structural variants
- noncoding variant assignments
- mitochondrial variants
- heteroplasmy placeholders
- cohort-derived evidence mistaken as sample-specific evidence
- zero observed evidence versus missing evidence
- unresolved phasing
- mitochondrial heteroplasmy uncertainty
- mixed inheritance mechanisms
- incomplete penetrance
- pseudo-dominant inheritance
- sex-limited manifestations
- mosaicism
- mitochondrial-nuclear interaction complexity

---

# 21. Definition of Contract Success

This system contract succeeds when DEX-RDGP can build RDGP without ambiguity about:

- repository role
- identity model
- upstream boundaries
- input expectations
- output expectations
- score/confidence separation
- confidence semantics
- uncertainty behavior
- provenance requirements
- validation invariants
- failure behavior
- implementation gates

---

# 22. Summary

RDGP is an explainable translational reasoning framework.

Its core responsibility is to integrate heterogeneous evidence into deterministic, provenance-aware, sample-scoped gene prioritization outputs while preserving biological meaning and uncertainty.

The governing implementation principle is:

```text
strong evidence anchors;
weak evidence supports;
uncertainty remains visible;
confidence remains reconstructable;
provenance remains traceable;
missingness never becomes hidden negative evidence.
```

# End of system_contract.md
