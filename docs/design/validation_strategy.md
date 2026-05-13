# validation_strategy.md

# RDGP Validation Strategy (Draft v0.1)

## Repository

`rare_disease_gene_prioritization (RDGP)`

---

# Purpose

This document defines the validation philosophy, behavioral verification strategy, semantic integrity checks, and anti-collapse testing framework for RDGP.

RDGP validation is intended to verify that the system remains:

- semantically coherent
- uncertainty-aware
- explainable
- reproducible
- biologically plausible
- interface-compatible
- discovery-capable
- resistant to hidden semantic collapse

This document defines validation strategy rather than finalized test implementation.

---

# Core Validation Philosophy

RDGP validation should be primarily:

```text
semantic-behavior-centric
```

with selective use of predictive and ranking metrics.

RDGP is not merely a ranking engine.

RDGP is an:

```text
explainable evidence integration and prioritization framework
```

Therefore validation must assess:

- whether evidence semantics are preserved
- whether uncertainty states remain distinct
- whether provenance remains traceable
- whether explainability survives scoring
- whether confidence and score remain separated
- whether interface boundaries remain intact
- whether biological plausibility is maintained

not merely:

- whether code runs
- whether output files serialize
- whether known genes rank highly

---

# Validation Stack Dependency

This strategy builds on the prior RDGP scientific-control documents:

| Document | Validation relevance |
|---|---|
| `scoring_rationale.md` | defines prioritization philosophy and score/confidence separation |
| `evidence_taxonomy.md` | defines evidence categories, scope, role, provenance, and taxonomy dimensions |
| `uncertainty_and_null_semantics.md` | defines null states, uncertainty propagation, unresolved states, and anti-collapse behavior |
| `validation_strategy.md` | verifies that these behaviors survive implementation |

Validation should enforce the design stack rather than validate RDGP as a generic scoring script.

---

# RDGP Validation Boundary

RDGP validates behavior at the:

```text
(sample_id, gene_id)
```

reasoning layer after upstream evidence has been aggregated from VDB and contextualized through optional GSC and RSP-derived evidence.

This document does not validate:

- raw variant calling in VAP
- persistent database storage internals in VDB
- GSC gene-set construction
- RSP transcriptomic pipeline execution

However, RDGP validation must verify that evidence from those systems is consumed without semantic distortion.

---

# Must-Pass Invariants vs Evaluation Metrics

RDGP validation should distinguish:

```text
must-pass invariants
```

from:

```text
evaluation metrics
```

---

## Must-Pass Invariants

Must-pass invariants define required semantic behavior.

Failure of an invariant should be treated as a system defect.

Examples:

- missing evidence must not silently become zero
- unsupported evidence must not become contradiction
- unresolved evidence must not silently resolve
- confidence must remain distinct from score
- GSC no-match must not become negative evidence
- cohort-derived evidence must not become patient-specific evidence
- provenance must remain traceable
- evidence category, scope, role, direction, quality, confidence, and status must remain independently representable

---

## Evaluation Metrics

Evaluation metrics characterize system behavior but do not alone define correctness.

Examples:

- known-gene recovery
- ranking stability
- perturbation sensitivity
- discovery-preservation behavior
- explainability completeness
- confidence calibration behavior

A system may perform well on one evaluation metric while still failing semantic validation.

Confidence calibration metrics should be interpreted as measures of interpretive reliability behavior rather than absolute biological truth estimation.

---

# Layered Validation Architecture

RDGP validation should operate across multiple layers.

| Layer | Validation purpose |
|---|---|
| schema | structural correctness of inputs and outputs |
| interface | cross-repo boundary preservation |
| semantics | taxonomy/null/uncertainty preservation |
| scoring | ranking behavior and component behavior |
| explainability | interpretability and evidence traceability |
| perturbation | robustness under evidence changes |
| edge cases | behavior under known failure modes |
| biological plausibility | translational sanity and rare-disease realism |

RDGP validation assumes a compositional evidence architecture in which evidence dimensions remain independently interpretable rather than collapsed into opaque aggregate states.

---

# 1. Schema Validation

Schema validation verifies that expected fields are present, well-typed, and structurally consistent.

Examples:

- required identifiers exist
- `sample_id` is present where sample-scoped evidence is expected
- `gene_id` or accepted fallback gene identity is present
- evidence category fields are populated where required
- score and confidence fields are separately represented
- provenance fields are retained
- null-state fields preserve explicit values

Schema validation is necessary but not sufficient.

A schema-valid output can still be biologically incoherent.

---

# 2. Interface Validation

Interface validation verifies that RDGP preserves upstream identity spaces and evidence boundaries.

RDGP must preserve distinctions between:

- VDB-derived sample-specific variant evidence
- GSC phenotype-scoped gene prior evidence
- RSP cohort-scoped or dataset-scoped functional evidence
- externally curated evidence such as ClinVar
- pipeline/system-level QC evidence

---

## Interface Validation Examples

Validation should verify that:

- GSC evidence is attached only with explicit selected phenotype context
- GSC no-match remains `no_gsc_match` or equivalent unsupported-prior state
- RSP-derived evidence remains cohort/dataset-scoped unless explicitly patient-specific
- VDB-derived variant evidence remains sample-specific
- external curated assertions remain distinct from sample observations
- gene mapping status remains visible after aggregation

---

# 3. Semantic Validation

Semantic validation verifies that evidence meanings survive implementation.

Validation should ensure that the following distinctions remain operationally distinct:

```text
missing
not evaluated
unsupported
unresolved
ambiguous
conflicting
contradictory
unknown
low quality
zero observed evidence
```

These states must not collapse during:

- scoring
- aggregation
- serialization
- export
- visualization
- downstream integration

Validation should explicitly verify that semantic distinctions survive serialization, export, and downstream interchange formats.

---

## Anti-Collapse Guarantees

RDGP validation should explicitly test that:

- missing ≠ unsupported
- unsupported ≠ contradiction
- unresolved ≠ resolved
- ambiguous ≠ low quality
- unknown ≠ negative
- low quality ≠ biological contradiction
- confidence ≠ score
- cohort evidence ≠ patient-specific evidence
- external curated evidence ≠ direct sample observation

These are core semantic invariants.

---

# 4. Scoring Validation

Scoring validation should verify that RDGP ranking behavior follows the scoring rationale.

Validation should assess:

- deterministic score generation
- preservation of intermediate scoring components
- bounded additive behavior
- strongest-hit anchoring
- no unbounded burden inflation
- no GSC-dominant ranking behavior
- no hidden novelty penalty
- no implicit penalty for missing optional evidence

---

## Score/Confidence Separation

Validation must ensure:

```text
score = prioritization strength
confidence = interpretive reliability
```

A gene should be able to be:

- high-score but low-confidence
- moderate-score but high-confidence
- low-score but well-explained
- unranked because required identity mapping failed

If implementation collapses confidence into score, validation should fail.

---

# 5. Explainability Validation

Explainability validation verifies that RDGP outputs can answer:

- why did this gene rank?
- what evidence contributed?
- what evidence was missing?
- what evidence was uncertain?
- what evidence was conflicting?
- what provenance supports each evidence item?
- what evidence scope did each item have?
- what confidence modifiers applied?
- what score components contributed?

Loss of explainability should count as validation degradation.

---

## Explainability Completeness

Each prioritized gene should retain enough information to reconstruct:

- supporting evidence
- missing evidence
- uncertainty states
- scope distinctions
- provenance chain
- confidence rationale
- scoring component contribution

---

# 6. Perturbation Validation

Perturbation validation assesses whether RDGP behaves coherently when evidence layers change.

This is a core validation strategy for RDGP.

---

## Recommended Perturbations

Validation should test behavior when:

- GSC support is removed
- GSC support is changed
- RSP evidence is missing
- ClinVar annotations are absent
- QC flags are introduced
- conflicting annotations are introduced
- gene mapping ambiguity is injected
- population frequency is missing
- phenotype prior support is unavailable
- low-quality variants are included or excluded

---

## Perturbation Expectations

Expected behavior:

- missing GSC should not automatically penalize score
- missing RSP should not make a gene biologically implausible
- conflicting annotations should reduce confidence and trigger warnings
- ambiguous mapping should remain unresolved unless explicitly resolved
- low-quality evidence should affect reliability semantics
- known-gene recovery should not depend entirely on GSC dominance
- biologically plausible under-characterized candidates should remain eligible

---

# 7. Discovery-Preservation Validation

RDGP should validate that plausible novel or under-characterized candidates can still surface under sparse prior knowledge conditions.

This prevents RDGP from becoming:

- literature-biased
- GSC-dominated
- ClinVar-dependent
- hostile to discovery
- a known-gene rediscovery engine

---

## Discovery-Preservation Scenarios

Validation should evaluate behavior under:

- absent ClinVar support
- missing GSC support
- missing RSP support
- sparse annotation
- novel LOF-like evidence
- weak but convergent multi-layer support
- under-characterized gene contexts

Discovery preservation does not mean maximizing novelty.

It means avoiding hidden penalties against under-characterized but biologically plausible candidates.

---

# 8. Known-Gene Recovery Validation

Known-gene recovery remains useful but should be treated as:

```text
a sanity-check validation dimension
```

not:

```text
the primary optimization target
```

Known-gene recovery can assess:

- phenotype alignment
- prioritization sanity
- basic biological plausibility
- scoring component behavior

However, over-optimizing for known-gene recovery risks:

- literature circularity
- rediscovery bias
- GSC dominance
- suppression of novel candidates

Known-gene recovery should be balanced with discovery-preservation validation.

---

# 9. Edge-Case Validation

RDGP should include explicit edge-case validation suites.

Recommended edge cases include:

- ambiguous gene mapping
- conflicting transcript consequences
- conflicting pathogenicity assertions
- unresolved inheritance
- missing databases
- unavailable optional evidence channels
- low-quality variants
- structural variants
- noncoding assignments
- mitochondrial variants
- heteroplasmy placeholders
- cohort-derived RSP evidence
- no GSC match
- `variant_count = 0` vs missing variant evidence

Edge cases are where semantic collapse and hidden assumptions most often emerge.

---

# 10. Biological Plausibility Validation

Biological plausibility validation asks whether outputs remain biologically interpretable.

This differs from deterministic correctness.

A system can be:

- schema-valid
- deterministic
- reproducible

while still producing biologically incoherent prioritization.

Validation should check:

- whether severe variant evidence behaves differently from weak evidence
- whether burden is bounded
- whether phenotype priors remain contextual
- whether functional evidence remains supportive rather than dominant
- whether QC evidence affects confidence rather than acting as biological evidence
- whether missingness does not become hidden negative evidence

---

# 11. Provenance Validation

Provenance validation ensures that RDGP outputs can trace evidence back to source.

Validation should verify:

- source name is preserved
- source version is preserved when available
- upstream record identifiers are preserved when available
- run IDs are retained
- selected phenotype context is retained for GSC-derived evidence
- dataset/contrast context is retained for RSP-derived evidence
- annotation provenance remains distinguishable from sample observation

Without provenance, explainability cannot be trusted.

---

# 12. Reproducibility Validation

RDGP should be deterministic for identical inputs and configurations.

Validation should verify:

- identical inputs produce identical outputs
- score components are reproducible
- confidence labels are reproducible
- evidence summaries are reproducible
- uncertainty flags are reproducible
- provenance summaries are reproducible

Reproducibility includes both numerical outputs and semantic outputs.

---

# 13. Recommended Validation Artifacts

DEX-RDGP may implement validation through artifacts such as:

- schema validation tests
- unit tests for scoring components
- semantic invariant tests
- perturbation test fixtures
- edge-case fixtures
- gold-standard toy examples
- synthetic sparse-evidence cases
- known-gene recovery panels
- discovery-preservation scenarios
- explainability completeness checks
- provenance retention checks

---

# 14. Minimal v1 Validation Requirements

At minimum, RDGP v1 validation should verify:

1. RDGP preserves `(sample_id, gene_id)` reasoning identity.
2. GSC no-match is not treated as negative evidence.
3. Missing RSP evidence does not penalize genes.
4. Confidence remains distinct from score.
5. Missing, unsupported, unresolved, conflicting, and contradictory states remain distinct.
6. Provenance is retained for each evidence source.
7. Evidence scope is retained.
8. Known-gene recovery is assessed as a sanity check.
9. At least one discovery-preservation scenario is tested.
10. At least one perturbation scenario is tested.
11. At least one edge-case scenario is tested.
12. Explainability fields are present for ranked genes.

---

# 15. Validation Failure Modes

Validation should flag failure when:

- missingness collapses into zero
- unknown becomes negative evidence
- no GSC match suppresses ranking by default
- optional RSP absence penalizes genes
- confidence and score are merged
- provenance is lost
- cohort evidence becomes patient-specific evidence
- external curated evidence becomes sample observation
- unresolved states silently resolve
- known-gene recovery is achieved only through prior dominance
- edge-case behavior becomes hidden
- semantic distinctions degrade across refactors or optimization passes
- uncertainty propagation behavior changes without explicit governance review
- evidence scope distinctions collapse during aggregation

---

# Summary Principles

## Core Validation Principle

```text
RDGP validation verifies semantic behavior,
not merely runtime correctness.
```

## Core Anti-Collapse Principle

```text
Semantically distinct evidence and uncertainty states
must remain operationally distinct.
```

## Core Explainability Principle

```text
A prioritization result is incomplete
if it cannot explain why a gene ranked.
```

## Core Discovery Principle

```text
Validation should ensure that sparse-prior candidates
remain eligible for review when biologically plausible.
```

## Core Interface Principle

```text
Validation should ensure RDGP consumes upstream evidence
without collapsing upstream identity spaces.
```

# End of validation_strategy.md
