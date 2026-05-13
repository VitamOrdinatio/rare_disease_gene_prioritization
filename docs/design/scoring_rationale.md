# scoring_rationale.md

# RDGP Scoring Rationale (Draft v0.1)

## Repository

`rare_disease_gene_prioritization (RDGP)`

---

## Purpose

This document defines the scientific rationale, conceptual philosophy, and evidence-integration principles underlying scoring behavior within RDGP.

This document is intended to:

- constrain future RDGP implementation behavior
- prevent scoring drift
- preserve interpretability
- preserve uncertainty semantics
- ensure ecosystem coherence
- guide DEX-RDGP implementation planning
- maintain compatibility with upstream interface specifications

This document defines scientific reasoning principles rather than exact implementation formulas.

RDGP scores records at the (sample_id, gene_id) level after VDB-derived variant evidence has been aggregated to gene-level evidence.

> RDGP operates on aggregated gene-level evidence representations rather than directly scoring raw variant rows.

---

# 1. Core Philosophical Objective

RDGP v1 is designed as:

```text
an explainable sample-scoped evidence convergence system
for rare-disease candidate gene prioritization
```

RDGP integrates:

- sample-specific variant evidence
- phenotype-scoped semantic priors
- optional functional evidence
- uncertainty-aware interpretation logic

into a unified prioritization framework intended for human review.

---

## RDGP Does NOT Attempt To

RDGP v1 does not attempt to:

- prove causality
- provide clinical diagnosis
- replace expert interpretation
- maximize novelty discovery
- function as a black-box predictor
- function as a deterministic truth engine

RDGP prioritization is suggestive and evidence-oriented rather than diagnostic.

---

# 2. Primary Optimization Target

RDGP v1 primarily optimizes for:

```text
Explainable multi-layer evidence convergence
for rare-disease candidate prioritization.
```

Operationally:

```text
Genes should rise in rank when multiple independent evidence layers
converge in support of biological plausibility within a sample and
phenotype-aware context.
```

This prioritization philosophy intentionally balances:

- sample-specific evidence
- phenotype relevance
- biological interpretability
- uncertainty preservation
- limited discovery sensitivity

without collapsing into:

- known-gene rediscovery
- novelty maximization
- pure burden accumulation
- purely literature-derived ranking

---

# 3. Core Prioritization Philosophy

RDGP prioritization should follow the following hierarchy:

```text
1. Strong direct sample-specific variant evidence
2. Additional sample-specific burden evidence
3. Phenotype-scoped contextual prior support
4. Optional functional/transcriptomic support
5. Explicit uncertainty and quality interpretation
```

The system is designed around the principle:

```text
strong evidence anchors;
weak evidence supports;
uncertainty remains visible.
```

---

## Biological Evidence vs Computational Convenience

RDGP scoring behavior must prioritize biological interpretability over computational convenience.

Implementation simplifications must not silently redefine biological meaning.

Examples of unacceptable collapse include:

- treating missingness as zero
- treating uncertainty as automatic negative evidence
- treating all evidence channels as equally informative
- compressing biologically distinct variant classes into indistinguishable scores
- allowing implementation constraints to determine biological semantics

Where computational simplification is necessary, the simplification must remain:

- explicit
- documented
- interpretable
- scientifically defensible

---

# 4. Evidence Hierarchy

## Highest-Priority Evidence

The strongest evidence categories are:

- pathogenic or likely pathogenic variants
- high-confidence LOF events
- severe predicted coding consequences
- strong sample-specific evidence with high-quality provenance

These forms of evidence should strongly influence prioritization.

---

## Supporting Evidence

Supporting evidence may include:

- multiple moderate-impact variants
- rare variant burden
- phenotype-scoped GSC support
- transcriptomic convergence
- network convergence
- expression perturbation evidence

Supporting evidence should contribute in bounded ways.

---

## Weak Evidence

Weak evidence includes:

- VUS observations
- sparse annotations
- weak functional predictions
- low-confidence priors
- incomplete evidence channels

Weak evidence may increase review priority but should not dominate ranking independently.

---

# 5. Strongest-Hit Anchoring

RDGP v1 should use a:

```text
strongest-hit anchored prioritization philosophy
```

This means:

```text
A strong direct evidence event should anchor prioritization more
strongly than accumulation of many weak signals alone.
```

Examples of anchoring evidence:

- ClinVar pathogenic variant
- high-confidence LOF
- canonical splice disruption
- highly deleterious coding event
- strong phenotype-relevant pathogenic annotation

---

## Rationale

Naive additive systems are vulnerable to:

- burden inflation
- large-gene bias
- annotation accumulation artifacts
- literature bias
- weak-signal pileup

Strongest-hit anchoring preserves interpretability and clinical realism.

---

# 6. Bounded Additive Support

Secondary evidence should contribute through:

```text
bounded additive support
```

rather than:

```text
unbounded linear accumulation
```

---

## Saturation Principle

Weak evidence channels should exhibit:

```text
diminishing returns
```

Examples:

- additional VUS variants
- additional weak burden observations
- repeated low-confidence annotations

Each additional weak signal should generally contribute less than the previous signal unless supported by independent orthogonal evidence.

---

## Orthogonal Convergence

Weak evidence becomes more meaningful when independent evidence channels converge.

Examples:

- weak variant evidence + strong phenotype prior
- weak burden + transcriptomic support
- moderate variant severity + functional convergence

Independent convergence is more informative than repeated evidence from a single channel.

---

# 7. GSC Prior Semantics

GSC support represents:

```text
phenotype-scoped contextual prior evidence
```

not:

```text
sample-specific biological evidence
```

---

## GSC Role in RDGP

GSC should:

- contextualize prioritization
- stabilize ranking
- increase phenotype relevance
- support known-gene recovery
- improve interpretability

GSC should NOT:

- dominate sample evidence
- independently create high-priority calls
- act as a hard filter
- suppress genes lacking prior support

GSC support must not be attached unless selected_phenotype is explicitly defined.

---

## Required GSC Guardrails

### Guardrail 1

```text
No GSC-only high-priority prioritization.
```

### Guardrail 2

```text
Missing GSC support must not disqualify a gene.
```

### Guardrail 3

```text
GSC support must remain distinguishable from sample-specific evidence.
```

### Guardrail 4

```text
GSC influence should remain bounded and interpretable.
```

---

## Rationale

If GSC dominates scoring:

```text
RDGP collapses into a known-gene rediscovery system.
```

The prioritization system must preserve sensitivity to under-characterized genes.

---

# 7A. Optional Functional and Transcriptomic Support

RDGP may optionally incorporate functional evidence derived from transcriptomic or network-level analyses.

Examples may include:

- differential expression
- network convergence
- pathway perturbation
- coexpression support
- transcriptomic outlier behavior

Such evidence may originate from RSP-derived analyses or future functional evidence systems.

Functional evidence may originate from cohort-level or dataset-level analyses and therefore may not represent direct patient-specific evidence.

RDGP should preserve distinctions between:

- sample-specific evidence
- phenotype-scoped prior evidence
- cohort-derived functional evidence

---

## Functional Evidence Role

Functional evidence should function as:

```text
contextual biological support
```

rather than:

```text
direct proof of disease causality
```

---

## Important Constraints

Functional evidence:

- should remain distinguishable from sample-specific variant evidence
- should not independently create high-priority calls
- should not override strong contradictory sample evidence
- may increase confidence in convergent biological plausibility

---

## Orthogonal Convergence Principle

Functional evidence becomes most informative when converging with:

- variant severity
- phenotype relevance
- rare variant burden
- GSC contextual support

Independent convergence across orthogonal evidence layers is more biologically informative than repeated support from a single evidence channel.

---

## Optionality Principle

Absence of transcriptomic or functional evidence must not penalize genes lacking such evidence channels.

RDGP v1 must remain functional even when no RSP-derived evidence is available.

---

# 8. Burden Semantics

RDGP v1 should reward:

```text
severity more strongly than raw burden
```

while allowing burden to contribute as supporting evidence.

---

## Why Burden Must Be Bounded

Raw burden is vulnerable to:

- large-gene effects
- sequencing artifacts
- annotation density artifacts
- biologically irrelevant accumulation

Therefore:

```text
variant_count alone must never dominate prioritization.
```

---

## Recommended Burden Philosophy

```text
severity anchors prioritization;
burden modifies prioritization.
```

---

## Examples of Burden-Supportive Context

Burden may become more meaningful when combined with:

- inheritance consistency
- compound heterozygosity
- recurrence
- phenotype relevance
- transcriptomic support
- functional convergence

# 8A. Variant Severity Semantics

RDGP v1 prioritization is severity-anchored rather than burden-anchored.

Variant severity should reflect the estimated biological impact of an observed variant event while preserving uncertainty and annotation provenance.

Examples of potentially high-severity evidence include:

- high-confidence loss-of-function variants
- canonical splice disruption
- pathogenic or likely pathogenic clinical assertions
- severe coding consequences
- strongly deleterious coding predictions

Lower-severity evidence may include:

- moderate missense effects
- weakly supported splice predictions
- synonymous variants
- uncertain or conflicting predictions

---

# 8B. Pathogenicity Assertion Semantics

Clinical pathogenicity assertions represent an important but non-absolute evidence channel within RDGP.

Examples include:

- ClinVar assertions
- expert-curated classifications
- pathogenicity annotations from trusted external sources

---

# 8C. Population Frequency Semantics

RDGP v1 assumes that rarity may increase the plausibility of rare-disease relevance, but rarity alone is insufficient for prioritization.

Population frequency should therefore function as:

```text
a contextual weighting modifier
```

rather than:

```text
a standalone prioritization driver
```

---


## Pathogenicity Weighting Principle

RDGP should generally prioritize:

```text
pathogenic > likely pathogenic > VUS > likely benign > benign
```

while preserving:

- provenance
- conflicts
- uncertainty
- source identity

---

## Important Constraints

Clinical assertions should inform prioritization strongly when:

- concordant
- well-supported
- phenotype-relevant
- supported by sample-specific evidence

However:

- conflicting assertions must remain visible
- VUS observations should not dominate ranking independently
- absence of ClinVar evidence must not be interpreted as benignity

---

## Conflict Semantics

Conflicting pathogenicity assertions should generally:

- reduce confidence
- increase interpretive caution
- preserve explainability

Conflict should not be silently collapsed into a single resolved truth state.

---

## Rare Variant Principle

Rare variants may contribute additional support when combined with:

- severe predicted consequence
- pathogenic annotation
- phenotype relevance
- transcriptomic convergence
- independent orthogonal evidence

---

## Important Constraints

Low-frequency variants should not automatically receive high prioritization.

RDGP should avoid:

- rarity-only prioritization
- burden inflation driven solely by rare variants
- overinterpretation of sparse population databases

---

## Missing Frequency Data

Missing population frequency data must remain semantically distinct from:

```text
ultra-rare
```

Missingness must not silently convert into rarity support.

---

## Severity Anchoring Principle

RDGP prioritization should generally prefer:

```text
one strong high-confidence damaging event
```

over: 

```text
many weak unsupported events
```

unless multiple weaker events gain support through independent orthogonal evidence such as:

- inheritance consistency
- recurrence
- phenotype relevance
- transcriptomic convergence
- network convergence

---

## Important Constraint

Severity should remain interpretable rather than overly compressed into a single hidden numerical transformation.

RDGP outputs should preserve enough intermediate information to explain:

- why a variant was considered severe
- which annotations contributed
- where uncertainty remained

---

# 9. Score vs Confidence vs Uncertainty

RDGP v1 intentionally separates:

- prioritization strength
- interpretive confidence
- uncertainty structure

These concepts must not collapse into a single scalar value.

---

## 9.1 Composite Score

The composite score represents:

```text
evidence convergence strength
```

It answers:

```text
Why did this gene rise in rank?
```

The score should primarily reflect:

- sample-specific evidence
- anchored severity
- bounded supporting evidence
- phenotype-aware contextual support
- optional functional evidence

The composite score does NOT directly represent certainty.

Composite score ranking should be interpreted as heuristic prioritization ordering rather than probabilistic disease likelihood estimation.

---

## 9.2 Confidence

Confidence represents:

```text
interpretive reliability
```

It answers:

```text
How much interpretive trust should be placed
in the prioritization result?
```

Confidence may depend on:

- evidence consistency
- provenance quality
- mapping reliability
- annotation agreement
- QC status
- uncertainty structure

A gene may therefore be:

```text
high-priority but uncertain
moderate-priority but highly reliable
low-priority but well-supported
unranked due to mapping failure
```

---

## 9.3 Uncertainty

Uncertainty represents:

```text
structured interpretive caution
```

Uncertainty should remain explicit and explainable.

Examples:

- conflicting annotations
- missing evidence channels
- ambiguous mapping
- unsupported phenotype context
- low read quality
- transcript ambiguity
- sparse prior knowledge

---

## 9.4 Scale Calibration and Normalization control

No evidence channel should dominate composite prioritization solely because of numerical scale magnitude.

The RDGP milestone_map states that `variant_score` + `GSC_support` + `expression_support` may require normalization so that components are comparable.

Recommended solution:

```text
Raw channel scales must not be combined until normalized, capped, tiered, or otherwise calibrated.
```

## Critical Principle

```text
uncertainty informs confidence
not necessarily score
```

---

## Cases Where Uncertainty SHOULD Affect Score

Certain uncertainty categories represent degraded evidence quality and may partially dampen prioritization strength.

Examples:

- failed QC
- ambiguous mapping
- conflicting annotations
- unreliable provenance
- poor read support

---

## Cases Where Uncertainty SHOULD NOT Reduce Score

The following should generally remain neutral rather than penalized:

- missing GSC support
- missing ClinVar evidence
- missing expression support
- novelty
- under-characterized genes

---

# 10. Missingness and Null Semantics

RDGP must preserve semantic distinctions between:

```text
missing
unknown
not evaluated
unsupported
conflicting
low quality
true negative evidence
zero observed evidence
```

These states must not collapse into a single interpretation.

RDGP must avoid introducing implicit negative priors through missingness handling, absent overlays, unavailable databases, or unsupported evidence channels.

Missing support must remain distinguishable from contradictory evidence.

---

## Core Principle

```text
absence of evidence
≠
evidence of absence
```

---

## Examples

### Acceptable

```text
No GSC support available
```

### NOT Acceptable

```text
No GSC support therefore biologically irrelevant
```

---

## Discovery Preservation Principle

Genes lacking:

- GSC support
- ClinVar support
- expression evidence
- literature evidence

must remain eligible for prioritization.

Otherwise RDGP becomes:

- circular
- literature-biased
- hostile to discovery
- incompatible with rare-disease prioritization

---

# 11. Conflict and Quality Semantics

RDGP must distinguish:

- uncertainty
- disagreement
- low quality
- missingness

as separate biological and interpretive states.

---

## Conflicting Evidence

Conflicting annotations should remain visible.

Examples:

- conflicting ClinVar assertions
- inconsistent transcript annotations
- discordant prediction tools

Conflict should generally:

- reduce confidence
- increase interpretive caution
- remain explainable

Conflict should not be silently resolved.

---

## Low-Quality Evidence

Low-quality evidence differs from missing evidence.

Examples:

- failed QC
- poor mapping
- weak read support
- contamination concerns

Low-quality evidence may:

- reduce score
- reduce confidence
- trigger warning flags
- remain reviewable

---

# 12. Explainability Requirements

Each prioritized gene should explain:

- which evidence layers contributed
- which evidence layers were absent
- which evidence layers were uncertain
- why prioritization occurred
- whether support is sample-specific or contextual
- how uncertainty influenced interpretation

---

## Explainability Priority

RDGP v1 prioritizes:

```text
transparent biological reasoning
```

over:

```text
opaque numerical optimization
```

---

# 13. Scientific Assumptions

RDGP v1 assumes:

- upstream evidence is reproducible
- variant aggregation is biologically meaningful
- orthogonal convergence increases plausibility
- evidence channels are not equally informative
- uncertainty is biologically important
- missingness is semantically meaningful
- heuristic prioritization can still be useful

---

# 14. Scientific Limitations

RDGP v1 is limited by:

- heuristic scoring
- incomplete phenotype modeling
- incomplete inheritance modeling
- incomplete noncoding interpretation
- incomplete mitochondrial heteroplasmy modeling
- incomplete transcript-specific reasoning
- incomplete network convergence support

RDGP prioritization remains suggestive rather than definitive.

---

# 14A. Edge Cases and Boundary Conditions

RDGP must explicitly preserve and interpret edge-case conditions rather than silently collapsing them into default scoring behavior.

---

## Ambiguous Gene Mapping

Variants with ambiguous gene mapping should:

- preserve ambiguity explicitly
- reduce confidence where appropriate
- remain traceable to underlying mapping logic

Ambiguous mapping should not silently resolve into a single assumed gene target.

---

## Missing vs Zero Evidence

RDGP must distinguish between:

```text
variant_count = 0
```

and:

```text
variant evidence unavailable or not evaluated
```

These states are biologically and computationally distinct.

---

## No GSC Match

```text
no_gsc_match
```

means:

```text
no phenotype-prior support identified
```

It does NOT mean:

- phenotype mismatch
- biological irrelevance
- negative evidence

---

## Unsupported Phenotype Context

A selected phenotype context may be:

- incomplete
- weakly characterized
- unsupported by available GSC overlays

RDGP should preserve this uncertainty explicitly.

---

## Structural Variants

Structural variants may not conform to the same assumptions as SNVs or indels.

RDGP v1 should preserve compatibility placeholders for:

- deletions
- duplications
- rearrangements
- complex events

even if scoring support remains incomplete.

---

## Noncoding Variants

Noncoding variants may involve:

- nearest-gene assignment
- regulatory assignment
- enhancer-target relationships
- locus-window overlays

Noncoding gene assignment should remain distinguishable from direct coding disruption.

---

## Mitochondrial Variants and Heteroplasmy

Mitochondrial variants may violate assumptions associated with diploid nuclear interpretation.

RDGP v1 should preserve explicit support for:

- mitochondrial gene labeling
- mitochondrial variant identity
- future heteroplasmy-aware reasoning

even if heteroplasmy modeling remains incomplete.

---

## Conflicting Annotation Sources

Conflicting annotations should remain detectable and explainable.

RDGP should avoid silently collapsing:

- discordant transcript annotations
- discordant pathogenicity assertions
- conflicting prediction tools
- inconsistent provenance

into a single hidden truth state.

---

# 15. Validation Implications

Validation should assess:

- known-gene recovery
- ranking stability
- sensitivity to threshold changes
- uncertainty behavior
- robustness to missing evidence
- resistance to burden inflation
- reproducibility
- explainability

---

## Validation Philosophy

A valid prioritization system is not merely plausible.

It should behave:

- predictably
- reproducibly
- explainably
- defensibly

under perturbation and edge-case analysis.

---

# 16. Guidance for DEX-RDGP

DEX-RDGP should implement:

- deterministic scoring
- preserved intermediate values
- bounded evidence accumulation
- explicit uncertainty representation
- separate score and confidence semantics
- provenance-preserving outputs
- explainable ranking logic

DEX-RDGP should avoid:

- hidden weighting
- silent evidence collapse
- unbounded additive scoring
- GSC-dominant prioritization
- novelty penalties
- opaque confidence derivation

---

# 17. Forward Compatibility

This scoring philosophy is designed to remain compatible with future:

- inheritance-aware models
- phenotype-aware reasoning
- probabilistic scoring
- transcriptomic convergence scoring
- network-convergence frameworks
- noncoding prioritization
- machine-learning augmentation

Future versions should preserve explainability and uncertainty semantics even if scoring sophistication increases.

---

# 18. Summary Principles

## Core RDGP Philosophy

```text
RDGP prioritizes genes through explainable convergence
of heterogeneous evidence layers.
```

---

## Core Prioritization Rule

```text
strong evidence anchors prioritization;
weak evidence contributes context;
uncertainty remains explicit.
```

---

## Core Uncertainty Rule

```text
uncertainty informs confidence
without automatically suppressing prioritization.
```

---

## Core Discovery Rule

```text
missing external support
must not disqualify biologically plausible genes.
```

---

## Core Explainability Rule

```text
Every prioritized gene should explain:
- why it ranked
- what evidence contributed
- what evidence was missing
- what evidence was uncertain
- how reliable the prioritization appears
```

---

# End of scoring_rationale.md
