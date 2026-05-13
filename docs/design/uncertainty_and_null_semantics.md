
# uncertainty_and_null_semantics.md

# RDGP Uncertainty and Null Semantics (Draft v0.1)

## Repository

`rare_disease_gene_prioritization (RDGP)`

---

# Purpose

This document defines the uncertainty semantics, null-state semantics, ambiguity handling philosophy, and unresolved-state behavior for RDGP.

The purpose of this document is to:

- preserve epistemic transparency
- prevent semantic collapse
- preserve explainability
- prevent hidden certainty inflation
- preserve discovery sensitivity
- constrain DEX-RDGP implementation behavior
- stabilize interpretation semantics
- support future probabilistic extensions
- maintain ecosystem coherence

This document defines conceptual semantic behavior rather than finalized implementation logic.

RDGP uncertainty semantics apply at the `(sample_id, gene_id)` reasoning layer after upstream VDB-derived evidence has been aggregated. This document does not redefine VAP calling, VDB storage, GSC phenotype-prior generation, or RSP functional analysis.

---

# Core Philosophy

RDGP uncertainty semantics prioritize:

```text
transparent uncertainty-aware interpretation
```

over:

```text
artificially clean deterministic certainty
```

RDGP is designed for:

- sparse evidence contexts
- incomplete biological knowledge
- uncertain mappings
- evolving annotations
- heterogeneous evidence quality
- translational interpretation

Therefore:

```text
uncertainty is expected
```

and should remain:
- explicit
- explainable
- structured
- auditable
- semantically meaningful

rather than hidden or silently collapsed.

---

# Uncertainty as Semantic Structure

In RDGP:

```text
uncertainty is a first-class semantic dimension
```

rather than passive metadata.

Uncertainty should influence:

- confidence interpretation
- explainability
- review prioritization
- downstream interpretability
- uncertainty propagation
- warning behavior
- edge-case interpretation

---

## Null State Table

| State | Meaning | Score effect | Confidence effect |
|---|---|---|---|
| unknown | insufficient knowledge | neutral | may reduce interpretive certainty |
| missing | expected source absent | neutral | may reduce completeness |
| not_evaluated | workflow did not assess | neutral | flags incomplete run |
| unsupported | evaluated, no support found | neutral by default; weakly plausibility-reducing only when explicitly justified | context-dependent |
| unresolved | ambiguity not resolved | usually neutral | reduces confidence |
| conflicting | sources disagree | usually neutral | reduces confidence / warning |
| contradictory | plausibility-reducing evidence | may reduce score cautiously | reduces confidence |
| low_quality | unreliable evidence | may dampen score | reduces confidence |

## Important Constraint

Uncertainty does NOT necessarily imply:

- hard score penalties
- aggressive ranking suppression
- biological implausibility
- contradiction

Instead, uncertainty primarily shapes:

- confidence
- caution
- interpretability
- auditability

---

## Confidence-First Interaction Principle

Default RDGP behavior should treat uncertainty states as:

```text
confidence-affecting
before
score-affecting
```

In general:

- uncertainty reduces interpretive certainty before reducing biological plausibility
- unresolved states reduce confidence before suppressing prioritization
- missingness reduces completeness before reducing score
- unsupported evidence remains distinct from contradictory evidence

---

## Important Constraint

Score reduction caused by uncertainty should require:

- explicit justification
- biologically defensible rationale
- documented implementation behavior

rather than implicit default penalties.

---

## Examples

| Condition                     | Default behavior                      |
| ----------------------------- | ------------------------------------- |
| unresolved transcript mapping | confidence reduction                  |
| missing transcriptomics       | completeness warning                  |
| conflicting assertions        | confidence reduction + review warning |
| poor QC                       | reliability reduction                 |
| impossible inheritance model  | plausibility-reducing evidence        |

---

# Semantic Transparency Principle

RDGP should preserve distinctions between:

- unknown
- unresolved
- unsupported
- conflicting
- contradictory
- not evaluated
- missing
- low quality
- ambiguous

These states are NOT biologically or epistemically equivalent.

They must not collapse into:
- zero
- null
- benign
- unsupported
- automatic contradiction

---

# Unknown vs Missing vs Unsupported vs Unresolved

## Unknown

```text
The system lacks sufficient knowledge to determine state.
```

Examples:

- no transcriptomic evidence available
- no curated annotation available
- disease mechanism poorly characterized

Unknown should remain semantically neutral by default.

Unknown does NOT imply:

- negative evidence
- benignity
- implausibility
- unsupported status

---

## Missing

```text
Expected data source unavailable or absent.
```

Examples:

- missing database
- unavailable annotation source
- failed external query
- unavailable cohort overlay

Missingness represents absence of accessible information rather than biological interpretation.

---

## Not Evaluated

```text
The pipeline or workflow never assessed the evidence category.
```

Examples:

- transcriptomics module disabled
- inheritance logic not run
- noncoding analysis skipped

Not evaluated is distinct from:
- unsupported
- missing
- contradiction

---

## Unsupported

```text
Evidence was evaluated and no supporting evidence emerged.
```

Examples:

- no phenotype-prior overlap identified
- no convergence signal identified
- no inheritance consistency identified

Unsupported does NOT imply contradiction or implausibility.

---

## Unresolved

```text
The system cannot confidently resolve ambiguity.
```

Examples:

- unresolved transcript assignment
- unresolved inheritance configuration
- unresolved phenotype specificity
- unresolved gene mapping

Unresolved should remain a first-class semantic state.

---

## Conflicting

```text
Multiple evidence sources disagree.
```

Examples:

- conflicting ClinVar assertions
- discordant prediction systems
- inconsistent transcript annotations

Conflict should generally:
- reduce confidence
- trigger warnings
- increase review priority

Conflict should not silently resolve into hidden consensus.

---

## Contradictory

```text
Evidence directly reduces biological plausibility.
```

Examples:

- impossible inheritance model
- impossible zygosity configuration
- strong benign assertion conflicting with severe pathogenic interpretation

Contradiction should be used conservatively in RDGP v1.

---

# Unknown Remains Neutral

One of the core RDGP principles is:

```text
unknown ≠ negative
```

Examples of semantically neutral unknown states:

- no transcriptomic evidence available
- no ClinVar assertion available
- no phenotype overlay identified
- no convergence analysis available

Unknown should not silently become:

- plausibility reduction
- contradiction
- benignity
- negative evidence

---

# Interface-Specific Semantic Examples

The following examples illustrate uncertainty semantics within the RDGP ecosystem.

---

## GSC Example

```text
no_gsc_match
```

means:

```text
no phenotype-prior support identified
```

It does NOT mean:

- phenotype contradiction
- biological implausibility
- evidence against the gene

---

## RSP Example

```text
missing_expression_support
```

means:

```text
optional functional evidence unavailable
```

It does NOT imply:

- absent biological relevance
- contradiction
- prioritization failure

---

## Mapping Example

```text
ambiguous_gene_mapping
```

means:

```text
gene assignment unresolved
```

This should generally:

- reduce confidence
- preserve ambiguity
- trigger review visibility

rather than silently assigning a single assumed target gene.

---

## Variant Evidence Example

```text
variant_count = 0
```

is NOT equivalent to:

```text
variant evidence unavailable
```

These represent distinct semantic conditions.

---

## Cohort Evidence Example

Cohort-derived transcriptomic convergence evidence should not silently become:

```text
direct patient-specific evidence
```

RDGP should preserve evidence scope explicitly.

---

# Uncertainty Propagation

Uncertainty should propagate semantically downstream.

Example:

```text
ambiguous transcript assignment
→ uncertain variant consequence
→ uncertain pathogenic interpretation
→ reduced interpretive confidence
```

Uncertainty propagation should primarily affect:

- confidence
- interpretability
- review emphasis
- warning semantics

rather than automatically causing:

- severe ranking suppression
- exclusion
- implausibility assignment

## Example Propagation Behaviors

Examples of semantically valid propagation behavior include:

| Upstream condition | Downstream effect |
|---|---|
| ambiguous transcript mapping | uncertain consequence interpretation |
| unresolved consequence interpretation | reduced pathogenic confidence |
| missing transcriptomics | reduced evidence completeness |
| conflicting pathogenicity assertions | review warning + confidence reduction |
| poor QC | reliability reduction |
| unstable gene mapping | unresolved gene-level interpretation |

---

## Important Constraint

Propagation should preserve semantic meaning rather than collapse all uncertainty into:

```text
generic score suppression
```

Different uncertainty sources should remain distinguishable downstream whenever possible.

---

# Partial Interpretability

RDGP explicitly supports:

```text
partially resolved interpretations
```

A gene may remain:

- high-priority
- biologically plausible
- review-worthy

while still containing:
- unresolved evidence
- ambiguous mappings
- incomplete annotations
- uncertain mechanisms

---

# Reliability vs Plausibility

Reliability-reducing evidence should generally affect confidence before plausibility, while plausibility-reducing evidence requires stronger biological justification.

RDGP distinguishes between:

```text
evidence that reduces reliability
```

and:

```text
evidence that reduces biological plausibility
```

These are not equivalent.

---

# Epistemic Uncertainty vs Biological Uncertainty

Not all uncertainty originates from the same source.

RDGP distinguishes between:

```text
epistemic uncertainty
```

and:

```text
biological uncertainty
```

---

## Epistemic Uncertainty

Epistemic uncertainty reflects:

```text
limitations in available knowledge or evidence
```

Examples include:

- missing database
- sparse annotations
- unresolved mapping
- no transcriptomic analysis performed
- unavailable cohort evidence
- incomplete literature support

---

## Biological Uncertainty

Biological uncertainty reflects:

```text
intrinsic biological complexity or variability
```

Examples include:

- incomplete penetrance
- variable expressivity
- tissue-specific effects
- context-dependent pathogenicity
- conflicting disease mechanisms
- heterogeneous phenotypic behavior

---

## Why This Distinction Matters

Epistemic uncertainty and biological uncertainty should not be treated as identical conditions.

Examples:

| Condition | Type |
|---|---|
| missing ClinVar annotation | epistemic uncertainty |
| unresolved transcript mapping | epistemic uncertainty |
| incomplete penetrance | biological uncertainty |
| variable expressivity | biological uncertainty |

---

# Unresolved-State Preservation

RDGP explicitly preserves unresolved states.

Examples include:

- unresolved mapping
- unresolved transcript assignment
- unresolved inheritance
- unresolved phenotype specificity

Unresolved does NOT imply:

- unsupported
- low quality
- implausibility
- contradiction

---

# Explainability Requirements

RDGP outputs should explain:

- what uncertainty exists
- where uncertainty originated
- how uncertainty propagated
- whether uncertainty affects confidence
- whether uncertainty affects plausibility
- whether evidence remains unresolved
- which evidence was missing vs unsupported vs contradictory

---

# Implementation Constraints

DEX-RDGP should preserve uncertainty semantics explicitly.

DEX-RDGP should avoid:

- silent null collapse
- implicit negative priors
- forced resolution
- hidden uncertainty suppression
- uncertainty-to-zero conversion
- unsupported-to-contradiction conversion

---

# Recommended Semantic Fields

The following fields represent recommended semantic structures for uncertainty-aware RDGP implementations.

These are conceptual guidance fields rather than finalized schema requirements.

| Field | Purpose |
|---|---|
| `uncertainty_state` | primary uncertainty classification |
| `null_state` | missing vs unsupported vs not evaluated |
| `resolution_state` | resolved vs unresolved |
| `conflict_state` | disagreement tracking |
| `confidence_effect` | interpretive impact |
| `score_effect` | prioritization impact |
| `uncertainty_source` | origin of uncertainty |
| `propagation_source` | upstream uncertainty dependency |
| `warning_flags` | review-triggering indicators |
| `review_priority` | interpretive review emphasis |
| `gene_mapping_status` | mapping stability |
| `evidence_completeness` | completeness indicator |
| `scope_awareness` | sample vs cohort vs external context |
| `selected_phenotype` | phenotype context used for phenotype-scoped uncertainty interpretation |
| `source_name` | evidence or uncertainty source system |
| `source_version` | source version when available |

---

## Important Constraint

DEX-RDGP should avoid encoding all uncertainty semantics into:

```text
a single null value
```

or:

```text
a single confidence scalar
```

Uncertainty dimensions should remain independently representable whenever possible.

---

# Validation Implications

Validation should assess:

- uncertainty preservation
- null-state preservation
- explainability retention
- unresolved-state behavior
- uncertainty propagation stability
- resistance to semantic collapse
- hidden certainty inflation
- reproducibility

## Recommended Semantic Validation Checks

Validation should verify that:

- missing GSC support does not automatically reduce prioritization score
- missing RSP evidence does not become implicit contradiction
- unsupported evidence remains distinguishable from contradictory evidence
- unresolved mapping remains unresolved rather than silently resolved
- conflicting assertions remain visible in outputs
- uncertainty propagation preserves interpretability
- low-quality evidence remains distinguishable from biologically contradictory evidence
- missingness does not silently collapse into zero
- cohort-derived evidence remains distinguishable from patient-specific evidence

---

## Anti-Collapse Validation Principle

Validation should explicitly test whether semantic distinctions survive implementation.

Examples include ensuring that:

```text
missing
unsupported
unresolved
conflicting
and contradictory
```

remain operationally distinct after:

- scoring
- aggregation
- serialization
- export
- visualization
- downstream integration

---

# Summary Principles

## Core Uncertainty Principle

```text
uncertainty is a semantic structure,
not merely metadata
```

## Core Neutrality Principle

```text
unknown ≠ negative
```

## Core Anti-Collapse Principle

```text
missing
not evaluated
unsupported
unresolved
ambiguous
conflicting
contradictory
unknown
and low quality

are not equivalent states
```

## Core Explainability Principle

```text
RDGP should preserve interpretable uncertainty
rather than forcing artificial certainty
```

# End of uncertainty_and_null_semantics.md