# Evidence Context Representation Framework

## Repository

`rare_disease_gene_prioritization`

---

# Purpose

This document defines the future-facing semantic representation framework for evidence-context modeling within RDGP.

The purpose of this framework is to ensure that future biological reasoning expansion remains:

- semantically coherent
- biologically contextual
- explainable
- provenance-aware
- uncertainty-preserving
- modular
- compositional
- validation-friendly

This framework exists to prevent future ontology collapse as RDGP expands beyond transparent ranking into deeper biological reasoning.

---

# Core Architectural Principle

RDGP must not treat biological evidence as:

```text
flat interchangeable scalar support
```

Instead, future RDGP evidence records should preserve:

```text
context-aware semantic evidence representations
```

where:
- evidence meaning
- biological scope
- temporal scope
- tissue scope
- mechanism scope
- confidence
- uncertainty
- provenance

remain independently reconstructable.

---

# Why This Framework Exists

As RDGP evolves, future biological reasoning layers may include:

- mechanistic reasoning
- developmental timing
- tissue vulnerability
- transcript-aware interpretation
- dosage sensitivity
- pathway convergence
- oligogenic interaction
- temporal disease progression
- network convergence
- transcriptomic overlays

Without explicit evidence-context modeling, these dimensions risk collapsing into:

- hidden scoring inflation
- opaque plausibility penalties
- biologically incoherent aggregation
- untraceable reasoning
- non-reconstructable prioritization logic

This framework exists to preserve semantic decomposition before future implementation expansion occurs.

---

# Evidence Representation Philosophy

RDGP evidence records should evolve toward:

```text
compositional biological context modeling
```

rather than:

```text
flat evidence scoring
```

Evidence items should preserve:

- what the evidence means
- what biological scope the evidence applies to
- what uncertainty exists
- what context modifies interpretation
- what provenance generated the evidence
- what limitations remain unresolved

---

# Evidence Identity Philosophy

Future evidence representations must preserve explicit identity scope.

Evidence identity must remain distinguishable across:

- sample-level evidence
- phenotype-level evidence
- cohort-level evidence
- pathway-level evidence
- transcript-level evidence
- network-level evidence

Future evidence systems must not silently collapse distinct biological identity spaces into undifferentiated evidence aggregates.

Examples of distinct identity scopes include:

| Evidence Type | Identity Example |
|---|---|
| sample-specific variant evidence | `(sample_id, gene_id)` |
| phenotype prior evidence | `(phenotype, gene_id)` |
| transcriptomic evidence | `(dataset_id, contrast_id, gene_id)` |
| pathway evidence | `(pathway_id, gene_id)` |
| network convergence evidence | `(network_context, gene_id)` |

Identity preservation is required for:

- explainability
- provenance
- auditability
- semantic correctness
- future compositional reasoning

---

# Core Semantic Axes

Future evidence records may preserve multiple independent semantic axes.

These axes must remain semantically distinguishable.

---

## 1. Evidence Category Axis

Describes the broad class of evidence.

Examples:

- variant evidence
- phenotype prior evidence
- transcriptomic evidence
- pathway evidence
- network evidence
- mechanistic evidence
- developmental evidence
- tissue-context evidence
- inheritance evidence
- structural evidence

Purpose:

```text
what kind of evidence is this?
```

---

## 2. Evidence Direction Axis

Describes how evidence influences interpretation.

Examples:

- supportive
- contradictory
- reliability-reducing
- context-modifying
- uncertainty-preserving
- unresolved

Purpose:

```text
how should this evidence affect interpretation?
```

Evidence direction must remain distinguishable from:

- confidence
- score magnitude
- mechanism context
- evidence category

---

## 3. Evidence Scope Axis

Describes the scope to which evidence applies.

Examples:

- sample-specific
- phenotype-specific
- cohort-derived
- tissue-derived
- developmental-stage-specific
- pathway-level
- external-prior
- literature-derived

Purpose:

```text
what biological scope does this evidence represent?
```

---

## 4. Biological Context Axis

Describes biological contextual interpretation.

Examples:

- mitochondrial context
- neuronal vulnerability
- developmental context
- metabolic context
- inflammatory context
- cancer context

Purpose:

```text
what biological system context modifies interpretation?
```

---

## 5. Mechanism Context Axis

Describes mechanism-aware interpretation.

Examples:

- loss_of_function
- gain_of_function
- dominant_negative
- haploinsufficiency
- dosage_sensitive
- unresolved_mechanism

Purpose:

```text
what biological mechanism context is implied?
```

Mechanism context must remain distinguishable from:

- confidence
- pathogenicity
- prioritization score
- inheritance compatibility

---

## 6. Tissue Context Axis

Describes tissue-specific vulnerability or relevance.

Examples:

- CNS
- muscle
- cardiac
- hepatic
- multisystem
- unknown

Purpose:

```text
what tissue context modifies interpretation?
```

---

## 7. Temporal / Developmental Context Axis

Describes temporal biological context.

Examples:

- embryonic
- developmental
- juvenile
- adult
- degenerative
- progressive
- acute
- unresolved

Purpose:

```text
what temporal context modifies biological interpretation?
```

---

## 8. Transcript / Isoform Context Axis

Describes transcript-aware consequence interpretation.

Examples:

- canonical_transcript
- tissue_specific_isoform
- nonsense_mediated_decay_sensitive
- splice_sensitive
- transcript_uncertain

Purpose:

```text
what transcript-aware context modifies interpretation?
```

---

## 9. Interaction Context Axis

Describes interaction-aware evidence relationships.

Examples:

- oligogenic_interaction
- pathway_convergence
- network_convergence
- mitochondrial_nuclear_interaction
- compensatory_relationship
- unresolved_interaction

Purpose:

```text
what multi-factor biological interaction context exists?
```

---

## 10. Confidence Context Axis

Describes interpretive reliability.

Examples:

- high_confidence
- moderate_confidence
- limited_confidence
- unresolved_confidence

Purpose:

```text
how reliable is this evidence interpretation?
```

Confidence context must remain distinct from:

- biological plausibility
- prioritization strength
- mechanism support

---

## 11. Uncertainty Context Axis

Describes unresolved ambiguity or incompleteness.

Examples:

- unresolved
- ambiguous
- conflicting
- unsupported
- not_evaluated
- low_quality

Purpose:

```text
what unresolved interpretive limitation exists?
```

---

## 12. Provenance Context Axis

Describes evidence origin and traceability.

Examples:

- source repository
- dataset identifier
- run identifier
- publication source
- algorithm version
- processing pipeline

Purpose:

```text
where did this evidence originate?
```

---

# Anti-Collapse Principles

Future evidence systems must not silently collapse:

| Distinction | Must Remain Separate |
|---|---|
| score vs confidence | yes |
| mechanism vs pathogenicity | yes |
| uncertainty vs contradiction | yes |
| inheritance vs mechanism | yes |
| tissue relevance vs causal evidence | yes |
| pathway convergence vs direct sample evidence | yes |
| developmental timing vs disease severity | yes |
| cohort evidence vs sample evidence | yes |

---

# Context Orthogonality Principle

Future evidence contexts should remain as orthogonal as possible.

Examples:

- tissue context should not automatically imply mechanism
- developmental timing should not automatically imply severity
- pathway convergence should not automatically imply causality
- transcript relevance should not automatically imply pathogenicity

Biological contexts may interact, but future RDGP systems should preserve enough semantic decomposition to reconstruct those interactions explicitly.

---

# Evidence Composition Philosophy

Future evidence composition should remain semantically explainable rather than implicitly probabilistic unless formal probabilistic modeling is explicitly introduced, validated, versioned, and transparently documented.

Future RDGP evidence composition should remain:

```text
modular
```

rather than:

```text
monolithic
```

Evidence layers should compose through:

- explicit semantic relationships
- explainable aggregation
- context-aware interpretation
- provenance-preserving linkage

rather than:

- hidden weight accumulation
- opaque plausibility inflation
- irreversible evidence flattening

---

# Future Evidence Item Architecture

Future evidence systems may eventually evolve toward:

```text
one evidence item = one semantically contextualized biological statement
```

rather than:

```text
one row = collapsed aggregate interpretation
```

Future evidence-item representations may support:

- long-form evidence tables
- graph-aware reasoning
- network-aware evidence linkage
- pathway-aware convergence
- transcript-aware reasoning
- developmental-context interpretation
- tissue-aware prioritization
- mechanistic interaction modeling

---

# Validation Philosophy

Future evidence-context implementations must remain:

- deterministic
- explainable
- reconstructable
- provenance-aware
- semantically decomposed
- biologically contextual
- uncertainty-preserving

Validation must verify that semantic axes remain distinguishable.

---

# Current Implementation Status

This framework is currently:

```text
future-facing architectural guidance
```

and is not yet a required implementation substrate.

RDGP v1 currently implements only bounded subsets of:

- confidence semantics
- inheritance semantics
- mechanistic semantics

This framework exists to preserve future architectural extensibility before ontology expansion occurs.

---

# Initial Evidence Substrate Scope

Initial `src/rdgp/evidence.py` implementation should include:

| Capability | Include in Initial Evidence Substrate? |
|---|---|
| evidence item normalization | yes |
| semantic field preservation | yes |
| evidence identity preservation | yes |
| provenance preservation | yes |
| uncertainty preservation | yes |
| direction semantics | yes |
| context decomposition | yes |
| score aggregation | no |
| probabilistic fusion | no |
| ontology traversal | no |
| network reasoning | no |

The initial evidence substrate should preserve semantic structure rather than perform higher-order biological interpretation.

Interpretive reasoning should remain delegated to specialized reasoning layers such as inheritance, mechanism, phenotype, transcript, pathway, or future network reasoning modules.

---

# Architectural Philosophy Summary

RDGP is evolving toward:

```text
compositional biological reasoning
```

rather than:

```text
scalar evidence aggregation
```

The long-term architectural objective is to preserve:

- semantic clarity
- biological contextualization
- uncertainty visibility
- provenance traceability
- explainability
- modular reasoning extensibility

without sacrificing:

- deterministic behavior
- validation rigor
- translational auditability
- implementation coherence

# End of evidence_context_representation.md