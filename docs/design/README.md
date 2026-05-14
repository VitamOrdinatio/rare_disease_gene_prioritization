# RDGP Design Canon

## Purpose

The `docs/design/` directory contains the scientific and semantic design canon for RDGP.

These documents define:

- biological reasoning philosophy
- semantic governance
- evidence interpretation boundaries
- confidence semantics
- inheritance semantics
- uncertainty behavior
- validation philosophy
- future extensibility constraints

This directory represents the conceptual reasoning architecture of RDGP.

---

# Why These Documents Exist

RDGP was intentionally designed as:

```text
a transparent translational reasoning architecture
```

rather than:

- a black-box ranking engine
- a monolithic pathogenicity scorer
- a probabilistic collapse framework
- a hidden rules engine

The design canon exists to ensure that:

- implementation follows explicit scientific intent
- semantic behavior remains stable over time
- future architectural expansion remains coherent
- biological reasoning remains explainable
- evidence semantics remain decomposed
- confidence and prioritization remain distinct
- uncertainty remains explicitly represented

---

# Design-First Development Philosophy

RDGP development follows:

```text
design → contract → implementation → validation
```

rather than:

```text
implementation-first experimentation
```

This ordering is intentional.

The goal is to stabilize:

- semantics
- architectural boundaries
- biological assumptions
- evidence decomposition
- validation expectations

before expanding implementation complexity.

---

# Relationship to Other Repository Layers

The design canon informs all downstream repository layers.

| Layer | Relationship |
|---|---|
| `docs/contracts/` | enforceable implementation boundaries |
| `src/rdgp/` | implementation substrate |
| `tests/validation/` | semantic invariant enforcement |
| `scripts/` | deterministic execution interfaces |
| `results/` | semantically governed outputs |

The design documents are intentionally upstream of implementation.

Implementation should conform to the design canon, not redefine it implicitly.

---

# Current Design Documents

## `confidence_modeling_framework.md`

Defines qualitative confidence semantics.

Separates:

```text
interpretive reliability
```

from:

```text
prioritization strength
```

---

## `evidence_context_representation.md`

Defines the semantic evidence substrate.

Preserves:

- evidence identity
- context decomposition
- provenance
- uncertainty
- confidence separation
- directional evidence semantics

without requiring probabilistic collapse.

---

## `evidence_taxonomy.md`

Defines evidence categories and evidence organization principles.

Supports decomposed evidence representation rather than monolithic scoring.

---

## `future_biological_reasoning_extensions.md`

Defines intentionally deferred future biological reasoning dimensions.

Includes future architectural planning for:

- mechanistic reasoning
- phenotype reasoning
- developmental reasoning
- tissue-context reasoning
- oligogenic reasoning
- temporal reasoning
- pathway convergence reasoning

This document primarily exists to preserve future extensibility.

---

## `inheritance_reasoning_framework.md`

Defines inheritance-aware reasoning semantics.

Separates:

- inheritance compatibility
- confidence impact
- mechanistic interpretation
- evidence exclusion behavior

Inheritance context modifies interpretation rather than functioning as a hard exclusion engine.

---

## `scoring_rationale.md`

Defines transparent prioritization philosophy.

Explains:

- score decomposition
- evidence weighting
- semantic preservation
- anti-collapse philosophy
- explainability goals

---

## `uncertainty_and_null_semantics.md`

Defines explicit semantic handling for:

- missing
- unsupported
- unresolved
- ambiguous
- conflicting
- not_evaluated

Prevents silent semantic collapse.

---

## `validation_strategy.md`

Defines semantic validation philosophy.

Validation is treated as:

```text
architectural enforcement
```

rather than merely functional testing.

---

# Architectural Themes Across the Design Canon

Several major architectural principles recur throughout RDGP design.

## Semantic Decomposition

RDGP prefers:

```text
multiple explicit semantic fields
```

over:

```text
single opaque aggregate scores
```

---

## Explainability Preservation

Biological interpretation should remain inspectable and reconstructable.

Evidence identity should not disappear during prioritization.

---

## Confidence Is Not Probability

RDGP confidence modeling is:

- qualitative-first
- explainability-oriented
- limitation-aware
- uncertainty-preserving

The framework intentionally avoids pseudo-probabilistic certainty inflation.

---

## Anti-Collapse Philosophy

RDGP intentionally resists:

- semantic flattening
- irreversible aggregation
- hidden weighting behavior
- probabilistic overcompression
- ontology collapse

---

## Future Extensibility

RDGP is intentionally evolving toward:

```text
compositional biological reasoning
```

rather than:

```text
fixed scalar ranking
```

Therefore the architecture preserves:

- modular evidence representation
- semantic orthogonality
- provenance decomposition
- contextual extensibility
- future reasoning compatibility

---

# Important Repository Constraint

The design canon defines:

```text
architectural intent
```

not necessarily:

```text
current implementation completeness
```

Some design documents intentionally describe:

- future reasoning layers
- deferred capabilities
- architectural scaffolding
- extension pathways

that are not yet implemented in RDGP v1.

This distinction is intentional.

---

# Current RDGP Design Maturity

The current design canon supports:

- transparent scoring
- confidence-aware reasoning
- inheritance-aware reasoning
- semantic-state preservation
- mechanistic extensibility
- evidence-context decomposition
- validation-first architecture
- deterministic execution

while preserving future compatibility for substantially more advanced biological reasoning layers.

---

# Intended Audience

This directory is primarily intended for:

- repository maintainers
- future RDGP developers
- scientific collaborators
- translational bioinformatics reviewers
- architecture reviewers
- future DEX/SAGE alignment workflows

These documents function as the conceptual operating system for RDGP development.