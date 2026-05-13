# confidence_modeling_framework.md

# RDGP Confidence Modeling Framework (Draft v0.1)

## Repository

`rare_disease_gene_prioritization (RDGP)`

---

# Purpose and Scope

This document defines the conceptual philosophy, semantic structure, behavioral expectations, implementation-governing principles, and anti-collapse constraints surrounding confidence modeling within RDGP.

This framework exists because RDGP explicitly separates:

- score
- confidence
- uncertainty
- quality
- provenance
- evidence scope
- evidence directionality
- plausibility
- contradiction

However:

```text
confidence semantics require explicit governance
to prevent hidden semantic collapse during implementation.
```

This document is intended to:

- constrain DEX-RDGP implementation behavior
- preserve explainability
- preserve uncertainty semantics
- preserve discovery sensitivity
- preserve semantic transparency
- prevent hidden certainty inflation
- prevent confidence-score collapse
- support future extensibility
- support future probabilistic expansion without forcing probabilistic implementation into RDGP v1

---

# RDGP Confidence Boundary

RDGP confidence modeling operates at the:

```text
(sample_id, gene_id)
```

reasoning layer after evidence aggregation from:

- VDB-derived sample-specific evidence
- optional GSC phenotype-scoped priors
- optional RSP functional/contextual evidence
- external curated annotations
- QC/reliability systems

This document does NOT define:

- probabilistic disease risk
- clinical diagnosis certainty
- Bayesian posterior probabilities
- causal certainty estimation
- clinical actionability scoring

RDGP confidence modeling defines:

```text
interpretive reliability semantics
```

for explainable prioritization behavior.

---

# Core Confidence Philosophy

In RDGP:

```text
confidence represents interpretive reliability
```

NOT:

```text
biological truth certainty
```

Confidence helps answer:

```text
How much interpretive trust should be placed
in this prioritization result?
```

while score answers:

```text
Why did this gene rank highly?
```

These concepts must remain distinct.

---

## Confidence-First Semantic Principle

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

---

## Important Constraint

Confidence must remain:

- explicit
- explainable
- semantically visible
- independently auditable
- operationally reconstructable

RDGP should avoid:

- hidden confidence penalties
- confidence-score merging
- confidence-as-truth framing
- hidden novelty suppression
- black-box confidence aggregation
- uncertainty collapse into scalar confidence

---

# Confidence vs Score vs Uncertainty

RDGP explicitly separates:

| Concept | Meaning |
|---|---|
| score | prioritization strength |
| confidence | interpretive reliability |
| uncertainty | epistemic ambiguity |
| quality | technical reliability |
| plausibility | biological coherence |
| contradiction | plausibility-reducing evidence |

These concepts are related but NOT interchangeable.

---

## Operational Distinction

### Score

Represents:

```text
why a candidate is biologically interesting
```

Examples:
- strong LOF
- phenotype relevance
- orthogonal convergence
- inheritance consistency

---

### Confidence

Represents:

```text
how interpretable and reliable
the prioritization reasoning currently is
```

Examples:
- stable mapping
- strong provenance
- reproducible annotations
- coherent evidence structure

---

### Uncertainty

Represents:

```text
known ambiguity, incompleteness,
or unresolved interpretation state
```

Examples:
- unresolved mapping
- sparse annotations
- missing transcriptomics
- conflicting assertions

---

### Quality

Represents:

```text
technical or analytical reliability
```

Examples:
- QC quality
- mapping quality
- coverage quality
- reproducibility quality

---

### Plausibility

Represents:

```text
biological coherence of interpretation
```

Examples:
- inheritance compatibility
- phenotype compatibility
- mechanistic coherence

---

### Contradiction

Represents:

```text
evidence directly reducing biological plausibility
```

Examples:
- impossible inheritance model
- impossible zygosity
- strong benign contradiction

---

# Example Interpretive States

| Scenario | Score | Confidence | Plausibility |
|---|---|---|---|
| severe LOF + sparse annotations | high | moderate | plausible |
| moderate evidence + excellent provenance | moderate | high | plausible |
| strong evidence + unresolved mapping | high | reduced | plausible |
| repeated weak redundant evidence | moderate | low/moderate | uncertain |
| novel biologically coherent candidate | moderate/high | moderate | plausible |
| impossible inheritance model | variable | reduced | plausibility-reducing |

---

# Confidence Sources

Confidence may emerge from multiple semantically distinct contributors.

Examples include:

- provenance quality
- mapping stability
- transcript stability
- annotation agreement
- QC quality
- inheritance consistency
- evidence completeness
- scope coherence
- evidence reproducibility
- orthogonal convergence
- evidence independence

---

# Reliability-Affecting vs Plausibility-Affecting Contributors

RDGP should distinguish between:

```text
reliability-affecting contributors
```

and:

```text
plausibility-affecting contributors
```

---

## Reliability-Affecting Examples

| Contributor | Typical effect |
|---|---|
| poor QC | confidence reduction |
| unstable mapping | confidence reduction |
| sparse annotations | completeness limitation |
| conflicting assertions | interpretive caution |
| missing optional evidence | completeness reduction |
| provenance instability | confidence reduction |

---

## Plausibility-Affecting Examples

| Contributor | Typical effect |
|---|---|
| impossible inheritance | plausibility reduction |
| impossible zygosity | plausibility reduction |
| strong benign contradiction | plausibility caution |
| phenotype incompatibility | plausibility caution |

---

## Important Constraint

Reliability reduction should generally affect:

- confidence
- caution
- review behavior

before affecting:

- prioritization score
- biological plausibility

---

# Confidence Dimensionality

Confidence may emerge from multiple semantically distinct reliability dimensions.

Confidence is therefore NOT necessarily:

```text
one scalar quantity
```

Possible dimensions include:

- provenance confidence
- mapping confidence
- annotation confidence
- QC confidence
- inheritance confidence
- reproducibility confidence
- completeness confidence
- scope coherence confidence
- convergence confidence

---

## Important Principle

RDGP v1 does NOT require formal multidimensional modeling.

However:

DEX-RDGP should preserve enough semantic structure so future dimensional expansion remains possible without ontology collapse.

---

## Anti-Collapse Constraint

DEX-RDGP should avoid:

```text
compressing all confidence behavior
into one opaque scalar
```

unless:
- explainability survives
- provenance survives
- uncertainty visibility survives
- dimensional reconstruction remains possible

---

# Confidence Is Not Consensus

Agreement between evidence sources does NOT automatically imply proportional confidence increase.

This is critically important.

---

# Why Consensus Can Fail

Repeated weak or correlated evidence may create:

```text
artificial confidence inflation
```

Examples include:

- duplicated literature propagation
- overlapping ontology sources
- redundant databases
- repeated prediction-system agreement
- multiple annotations derived from one upstream source

---

# Orthogonal Convergence vs Redundant Agreement

RDGP should distinguish between:

```text
orthogonal evidence convergence
```

and:

```text
source redundancy
```

Orthogonal convergence across semantically distinct evidence layers is generally more informative than repeated support from correlated sources.

Examples of orthogonal convergence:

- damaging variant
- inheritance consistency
- phenotype relevance
- transcriptomic convergence

Examples of redundant agreement:

- multiple derivative databases
- repeated ontology mappings
- correlated prediction systems

---

# Confidence Propagation

Confidence should propagate semantically rather than through generic penalties.

---

# Propagation Philosophy

Upstream uncertainty should generally affect:

- confidence
- interpretability
- review priority
- caution semantics

before affecting:

- score
- plausibility

---

# Example Propagation Behaviors

| Upstream condition | Downstream confidence behavior |
|---|---|
| unresolved transcript mapping | reduced consequence confidence |
| unstable gene mapping | unresolved gene-level confidence |
| conflicting assertions | confidence reduction + warning |
| poor QC | reliability reduction |
| missing optional transcriptomics | completeness limitation |
| unresolved inheritance | inheritance-confidence reduction |

---

# Localized vs Propagated Effects

Some uncertainty should remain localized.

Examples:

| Condition | Suggested behavior |
|---|---|
| weak optional RSP evidence | localized caution |
| optional evidence unavailable | completeness warning |
| transcript instability | localized annotation caution |
| unstable mapping | broader propagation |
| conflicting inheritance | broader interpretive caution |

---

## Important Constraint

Propagation should preserve semantic meaning rather than collapsing into:

```text
generic confidence suppression
```

Different uncertainty sources should remain distinguishable whenever possible.

---

# Confidence States and Tiers

RDGP v1 should remain:

```text
qualitative-first
```

Examples of future qualitative states may include:

- high confidence
- moderate confidence
- low confidence
- unresolved confidence
- confidence limited by ambiguity
- confidence limited by conflict
- confidence limited by missingness
- confidence limited by incomplete evaluation

---

# Operational Semantics Before Numerical Encoding

RDGP should prioritize:

```text
operational semantics before numerical encoding
```

Confidence semantics should stabilize before introducing:

- probabilistic confidence
- calibrated confidence ranges
- Bayesian formulations
- ML-derived confidence estimators

---

# Future Quantitative Expansion

Future RDGP versions may optionally support:

- calibrated confidence ranges
- probabilistic confidence
- Bayesian confidence
- compositional confidence structures
- phenotype-aware confidence
- inheritance-aware confidence
- confidence calibration studies

However:

```text
RDGP v1 must remain deterministic,
explainable,
and operationally auditable.
```

---

# Confidence and Missingness

Missingness should interact with confidence carefully.

---

# Important Semantic Distinctions

| Condition | Meaning |
|---|---|
| missing | source unavailable |
| not evaluated | workflow never assessed |
| unsupported | evaluated but no support found |
| unresolved | ambiguity not resolved |
| conflicting | evidence disagreement |
| contradictory | plausibility-reducing evidence |

These states should NOT collapse into:

```text
generic low confidence
```

---

# Critical Principle

```text
missing evidence should not automatically imply
low biological plausibility
```

Examples:
- no ClinVar annotation
- missing transcriptomics
- no GSC overlap
- sparse literature

may reduce:
- completeness
- interpretive confidence
- review certainty

without implying:
- implausibility
- contradiction
- irrelevance

---

# Unsupported vs Low Confidence

Unsupported evidence means:

```text
the system evaluated an evidence channel
and found no support
```

Low confidence means:

```text
the system lacks strong interpretive reliability
for the current reasoning structure
```

These are NOT equivalent.

---

# Confidence and Explainability

RDGP outputs should explain:

- why confidence was high or low
- which uncertainty states contributed
- which provenance issues mattered
- whether confidence reductions came from:
  - ambiguity
  - missingness
  - conflict
  - incomplete evaluation
  - low quality
  - unstable mapping
- whether confidence effects were localized or propagated
- whether unresolved states remain present

---

# Explainability Requirement

Confidence should remain:

```text
semantically reconstructable
```

from:
- provenance
- uncertainty states
- quality states
- evidence structure
- propagation behavior

---

## Important Constraint

DEX-RDGP should avoid:

- opaque aggregate confidence values
- unexplained scalar confidence
- hidden weighting systems
- confidence behavior that cannot be reconstructed from semantic evidence state

---

# Confidence Failure Modes

RDGP should explicitly guard against:

- hidden confidence-score merging
- hidden novelty suppression
- literature bias
- confidence inflation from repeated weak evidence
- confidence inflation from source redundancy
- black-box confidence aggregation
- uncertainty collapse into scalar confidence
- unsupported evidence silently becoming low confidence
- sparse evidence automatically implying implausibility
- pseudo-probabilistic language unsupported by implementation
- confidence inflation from correlated evidence sources

---

# Anti-Collapse Principle

Confidence must NOT silently become:

- score suppression
- contradiction
- implausibility
- diagnosis certainty
- truth probability

unless:
- explicitly justified
- semantically explainable
- operationally reconstructable

---

# Confidence Validation Philosophy

Confidence validation should assess:

- confidence stability
- confidence explainability
- confidence propagation behavior
- confidence reproducibility
- confidence provenance preservation
- confidence-score separation
- semantic transparency
- perturbation robustness
- resistance to confidence inflation
- anti-collapse guarantees

---

# Recommended Confidence Validation Checks

Validation should verify that:

- missing optional evidence does not excessively suppress confidence
- unresolved states remain visible
- confidence reductions remain explainable
- confidence does not silently become score penalties
- redundant evidence does not artificially inflate confidence
- confidence propagation remains semantically interpretable
- confidence remains reproducible
- confidence remains distinguishable from plausibility
- confidence remains distinguishable from uncertainty
- confidence explanations remain reconstructable

---

# Recommended Confidence Fields

The following represent recommended semantic structures for DEX-RDGP implementations.

These are guidance structures rather than finalized schema requirements.

| Field | Purpose |
|---|---|
| `confidence_state` | primary confidence interpretation |
| `confidence_tier` | qualitative confidence label |
| `confidence_sources` | contributors affecting confidence |
| `confidence_modifiers` | conditions altering confidence |
| `confidence_explanation` | human-readable explanation |
| `confidence_scope` | scope context for confidence reasoning |
| `confidence_flags` | review-triggering conditions |
| `confidence_provenance` | provenance affecting confidence |
| `confidence_propagation_source` | upstream uncertainty dependency |
| `confidence_completeness` | evidence completeness indicator |
| `confidence_reproducibility` | reproducibility-related metadata |
| `confidence_limitations` | unresolved or cautionary conditions |
| `confidence_dimensions` | optional future multidimensional structure |
| `confidence_validation_state` | validation/review metadata |

---

# Important Constraint

DEX-RDGP should avoid encoding all confidence semantics into:

```text
a single opaque scalar
```

Confidence dimensions should remain independently explainable whenever possible.

---

# Future Extensions

Future RDGP versions may optionally support:

- probabilistic confidence
- Bayesian confidence
- phenotype-aware confidence
- inheritance-aware confidence
- uncertainty-aware confidence propagation
- ML-assisted confidence estimation
- confidence dimensionality models
- calibration studies
- compositional confidence architectures

However:

```text
future extensions must preserve:
- explainability
- semantic transparency
- deterministic compatibility
- auditability
- anti-collapse behavior
```

---

# Summary Principles

## Core Confidence Principle

```text
confidence represents interpretive reliability,
not biological truth certainty
```

---

## Core Transparency Principle

```text
confidence must remain explainable,
visible,
and semantically reconstructable
```

---

## Core Anti-Collapse Principle

```text
confidence must not silently collapse into:
- score suppression
- contradiction
- implausibility
- hidden probabilistic certainty
```

---

## Core Discovery Principle

```text
low-confidence sparse-evidence candidates
may still remain biologically plausible
and review-worthy
```

---

## Core Dimensionality Principle

```text
confidence may emerge from multiple
semantically distinct reliability dimensions
```

---

## Core Deterministic Principle

```text
RDGP v1 confidence modeling must remain:
- deterministic
- explainable
- operationally auditable
```

# End of confidence_modeling_framework.md