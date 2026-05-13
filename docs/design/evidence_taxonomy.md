# evidence_taxonomy.md

# RDGP Evidence Taxonomy (Draft v0.1)

## Repository

`rare_disease_gene_prioritization (RDGP)`

---

# Purpose

This document defines the conceptual evidence taxonomy used within RDGP.

The taxonomy is intended to:

- preserve biological meaning
- preserve evidence provenance
- preserve explainability
- preserve uncertainty semantics
- support deterministic implementation
- support ecosystem coherence
- prevent semantic collapse
- constrain DEX-RDGP implementation behavior
- support future extensibility

This taxonomy defines conceptual evidence organization principles rather than fixed implementation schemas.

RDGP evidence is organized for reasoning at the `(sample_id, gene_id)` level after VDB-derived variant evidence has been aggregated. Evidence taxonomy should not imply that RDGP directly owns raw variant calling, persistent storage, GSC generation, or RSP analysis.

Evidence category, scope, role, strength, confidence, directionality, provenance, quality, and missingness are independent dimensions. DEX-RDGP should not encode them as one mutually exclusive enum.

---

# Core Taxonomy Philosophy

RDGP evidence taxonomy prioritizes:

```text
biological semantics
over
implementation convenience
```

The taxonomy exists to preserve:

- explainability
- provenance
- biological interpretability
- scope awareness
- uncertainty visibility
- convergence reasoning

The taxonomy is NOT intended to:

- collapse evidence into opaque numerical categories
- replace biological reasoning with implementation shortcuts
- optimize solely for engineering simplicity

---

# Biological Evidence vs Computational Convenience

Implementation simplifications must not silently redefine biological meaning.

Examples of unacceptable semantic collapse include:

- treating all evidence channels as equivalent
- collapsing all evidence into weak/moderate/strong labels
- treating missingness as zero evidence
- treating uncertainty as automatic contradiction
- allowing schema convenience to determine biological interpretation

Where simplification becomes necessary, simplification should remain:

- explicit
- documented
- explainable
- scientifically defensible

---

# Core Taxonomy Design Principles

RDGP evidence taxonomy should remain:

- biologically meaningful
- operationally tractable
- explainable
- provenance-preserving
- scope-aware
- uncertainty-aware
- extensible
- implementation-compatible

RDGP v1 intentionally avoids:

- ontology explosion
- excessively granular mechanistic subclassing
- premature disease-specific branching
- deep transcript-level ontology hierarchies
- uncontrolled evidence subtype proliferation

---

# Core Taxonomy Dimensions

RDGP evidence taxonomy is organized across multiple conceptual dimensions.

These dimensions should remain semantically distinct.

---

# 1. Evidence Category

Evidence category represents:

```text
what kind of biological or interpretive evidence exists
```

Examples include:

- variant consequence evidence
- pathogenicity assertion evidence
- phenotype prior evidence
- inheritance evidence
- transcriptomic convergence evidence
- network convergence evidence
- QC/reliability evidence
- functional evidence
- prediction-system evidence

Evidence category is intended to preserve biological meaning rather than merely evidence strength.

---

# 2. Evidence Scope

Evidence scope represents:

```text
the contextual identity-space in which evidence exists
```

Scope is a first-class taxonomy dimension.

---

## Example Evidence Scopes

| Evidence Type | Scope |
|---|---|
| pathogenic LOF | sample-specific |
| inheritance consistency | sample-specific |
| GSC support | phenotype-scoped |
| transcriptomic convergence | cohort-scoped |
| network convergence | functional/system-level |
| ClinVar assertion | external curated |
| QC evidence | pipeline/system-level |

---

# 3. Evidence Role

Evidence role represents:

```text
the biological or interpretive function
performed by the evidence
```

---

## Example Evidence Roles

| Evidence | Role |
|---|---|
| LOF variant | direct biological evidence |
| ClinVar pathogenic assertion | curated interpretive evidence |
| GSC support | contextual prior evidence |
| transcriptomic convergence | functional support evidence |
| inheritance consistency | coherence evidence |
| QC failure | reliability-modifying evidence |

---

# 4. Evidence Strength

Evidence strength represents:

```text
the estimated biological importance or prioritization relevance
of an evidence signal
```

Evidence strength does NOT represent certainty or reliability.

---

# 5. Evidence Confidence

Evidence confidence represents:

```text
the reliability, stability, or trustworthiness
of an evidence signal
```

Confidence and strength must remain fully separated.

---

## Examples

| Evidence | Strength | Confidence |
|---|---|---|
| novel LOF | strong | moderate |
| ClinVar pathogenic | strong | high |
| weak network convergence | weak | high |
| ambiguous splice prediction | moderate | low |

---

# 6. Evidence Directionality

Evidence directionality represents:

```text
whether evidence supports, contextualizes,
or contradicts biological plausibility
```

---

## Positive Evidence

Supports plausibility.

Examples:

- pathogenic LOF
- strong convergence
- phenotype overlap
- inheritance consistency

---

## Neutral / Contextual Evidence

Provides contextual information without strongly altering plausibility.

---

## Reliability-Reducing Evidence

Reduces interpretive confidence rather than directly contradicting plausibility.

Examples:

- poor QC
- low coverage
- unstable transcript support
- conflicting assertions
- ambiguous mapping

---

## Strong Contradictory Evidence

Should be used conservatively in RDGP v1.

## Negative vs Reliability-Reducing Evidence

RDGP must distinguish evidence that argues against biological plausibility from evidence that reduces trust in the available data.

Examples:

| Evidence state | Recommended interpretation |
|---|---|
| high-confidence benign assertion | potential plausibility-reducing evidence or down-weighting evidence |
| inheritance impossibility | potential plausibility-reducing evidence evidence |
| impossible zygosity model | potential plausibility-reducing evidence evidence |
| poor QC | reliability-reducing evidence |
| low coverage | reliability-reducing evidence |
| ambiguous gene mapping | reliability-reducing evidence |
| conflicting assertions | reliability-reducing or conflict evidence |
| missing ClinVar record | missingness, not contradiction |
| no GSC match | missing/unsupported prior, not contradiction |

This distinction is required to prevent missing or low-quality information from being incorrectly treated as biological evidence against a gene.

---

# 7. Evidence Provenance

Evidence provenance represents:

```text
where evidence originated
```

Provenance is a first-class taxonomy dimension.

---

## Example Provenance Sources

Examples may include:

- ClinVar
- GSC
- RSP
- AlphaMissense
- SpliceAI
- VEP
- inheritance inference systems
- QC systems
- external curated resources

---

# 8. Evidence Quality

Evidence quality represents:

```text
technical or interpretive reliability modifiers
```

Evidence quality is distinct from:

- evidence strength
- evidence confidence
- evidence scope
- evidence category

---

# 9. Evidence Missingness and Null Semantics

RDGP should avoid introducing implicit negative priors through absent databases, unsupported overlays, unavailable transcriptomic evidence, or missing annotations.

RDGP must preserve semantic distinctions between:

```text
missing
unknown
not evaluated
unsupported
conflicting
low quality
negative evidence
zero observed evidence
```

These states must not collapse into identical evidence representations.

---

## Discovery Preservation Principle

Genes lacking:

- GSC support
- ClinVar support
- transcriptomic support
- literature support

must remain eligible for prioritization.

---

# 10. Core Evidence Categories (Recommended v1)

## Variant Consequence Evidence

**Biological meaning:**  
Evidence that an observed variant may alter gene or transcript function through its predicted molecular consequence.

**Scope:**  
Primarily sample-specific, derived from VDB/VAP variant annotations after aggregation to `(sample_id, gene_id)`.

**Typical directionality:**  
Usually positive when consequence is plausibly damaging; neutral/contextual for weak or low-specificity consequences; reliability-reducing when consequence assignment is ambiguous.

**Strength behavior:**  
High-confidence LOF, frameshift, canonical splice disruption, and severe coding consequences may provide strong evidence. Missense and noncoding assignments are generally more context-dependent. Synonymous variants usually contribute weak or neutral evidence unless splice/regulatory impact is supported.

**Confidence caveats:**  
Confidence depends on annotation source, transcript choice, mapping quality, consequence consistency, and variant normalization.

**Known failure modes:**  
Transcript ambiguity, multi-transcript consequence disagreement, gene mapping ambiguity, overinterpreting noncoding nearest-gene assignments, and treating predicted consequence as proven biological effect.

**Implementation note:**  
DEX-RDGP should preserve consequence subtype, annotation source, transcript context if available, gene mapping status, and confidence/quality modifiers separately.

---

## Pathogenicity Assertion Evidence

**Scope clarification:**  
External curated pathogenicity assertions are not sample-specific evidence by themselves. A ClinVar pathogenic assertion may annotate a variant observed in the sample, but the assertion itself remains external curated evidence. RDGP should preserve the distinction between:

- the variant being observed in this sample
- the external source asserting pathogenicity for that variant
- the confidence and review status of that assertion

A pathogenic assertion can strengthen interpretation of a sample variant, but it should not be treated as equivalent to a newly generated sample-specific observation.

**Biological meaning:**  
Curated interpretive evidence describing whether a variant has been previously assessed for disease relevance by external expert or community resources.

**Scope:**  
External curated evidence associated with a variant observed in the sample.

**Typical directionality:**  
May be positive, neutral, or contradictory depending on assertion class and review confidence.

**Strength behavior:**  
Pathogenic and likely pathogenic assertions may provide strong support when concordant with sample evidence and phenotype context. VUS assertions generally provide limited standalone support. Benign assertions may function as contradictory or down-weighting evidence.

**Confidence caveats:**  
Confidence depends on review status, assertion conflicts, provenance quality, curation recency, and source reliability.

**Known failure modes:**  
Conflicting assertions, stale classifications, phenotype mismatch, overreliance on external assertions, and assuming curated assertions are equivalent to direct biological proof.

**Implementation note:**  
DEX-RDGP should preserve assertion class, review status, conflict state, source identity, and provenance separately from sample-specific evidence.

---

## Inheritance Evidence

**Biological meaning:**  
Evidence describing whether observed variant configurations are compatible with expected inheritance behavior for a disease mechanism or phenotype context.

**Scope:**  
Primarily sample-specific, potentially family-aware when pedigree information exists.

**Typical directionality:**  
Usually positive when inheritance configuration supports plausibility; potentially contradictory when inheritance assumptions are violated.

**Strength behavior:**  
Inheritance consistency may substantially strengthen plausibility when combined with damaging variants and phenotype relevance. Inheritance evidence rarely functions as strong standalone evidence without additional biological support.

**Confidence caveats:**  
Confidence depends on pedigree completeness, phasing accuracy, zygosity quality, family structure, and inheritance model assumptions.

**Known failure modes:**  
Incorrect phasing, incomplete pedigree data, false de novo calls, zygosity errors, phenotype heterogeneity, and oversimplified inheritance assumptions.

**Implementation note:**  
DEX-RDGP should preserve inheritance model assumptions, zygosity state, pedigree availability, phasing confidence, and family-context provenance separately.

---

## Phenotype Prior Evidence

**Biological meaning:**  
Contextual prior evidence indicating that a gene has previously been associated with a phenotype-relevant disease context or biologically related gene set.

**Scope:**  
Phenotype-scoped rather than sample-specific.

**Typical directionality:**  
Usually positive or contextual; absence of phenotype-prior support should remain neutral rather than contradictory.

**Strength behavior:**  
Strong phenotype-relevant overlap may stabilize prioritization and improve interpretability but should not dominate sample-derived biological evidence.

**Confidence caveats:**  
Confidence depends on phenotype specificity, overlay provenance, source quality, curation strategy, and ontology resolution quality.

**Known failure modes:**  
Literature circularity, phenotype overgeneralization, ontology mismatch, rediscovery bias, and treating absence of overlap as negative evidence.

**Implementation note:**  
DEX-RDGP should preserve selected phenotype context, overlay provenance, phenotype ontology mapping, and overlap source independently from sample evidence.

---

## Functional / Transcriptomic Evidence

Orthogonal convergence across independent evidence layers is generally more biologically informative than repeated support from a single evidence source.

**Biological meaning:**  
Evidence describing functional perturbation, expression alteration, network convergence, or pathway-level biological behavior associated with a gene or disease context.

**Scope:**  
Usually cohort-scoped or dataset-scoped rather than directly patient-specific.

**Typical directionality:**  
Usually positive or contextual; may increase plausibility through orthogonal biological convergence.

**Strength behavior:**  
Functional convergence may strengthen prioritization when aligned with damaging sample-specific evidence and phenotype relevance. Weak isolated convergence should generally remain supportive rather than dominant.

**Confidence caveats:**  
Confidence depends on cohort quality, statistical robustness, dataset reproducibility, tissue relevance, experimental design, and network methodology.

**Known failure modes:**  
Batch effects, tissue mismatch, unstable network inference, cohort bias, pathway overinterpretation, and treating cohort-derived signals as patient-specific observations.

**Implementation note:**  
DEX-RDGP should preserve dataset provenance, cohort identity, tissue context, convergence methodology, statistical metadata, and cohort-vs-patient distinction explicitly.

---

## Prediction-System Evidence

**Biological meaning:**  
Computationally inferred evidence estimating potential functional impact, pathogenicity, conservation disruption, or splice alteration.

**Scope:**  
Usually variant-associated computational inference rather than experimentally validated biological evidence.

**Typical directionality:**  
Usually positive or contextual depending on prediction severity and model agreement.

**Strength behavior:**  
Prediction systems may provide useful supporting evidence but should rarely dominate prioritization independently without orthogonal biological support.

**Confidence caveats:**  
Confidence depends on model calibration, training bias, feature space limitations, prediction agreement, and applicability to variant context.

**Known failure modes:**  
Model overconfidence, training-data circularity, predictor disagreement, overinterpretation of probabilistic scores, and treating computational inference as biological confirmation.

**Implementation note:**  
DEX-RDGP should preserve predictor identity, predictor version, score normalization metadata, threshold assumptions, and agreement/disagreement between systems.

---

## QC / Reliability Evidence

**Biological meaning:**  
Technical or analytical evidence affecting confidence in interpretation reliability rather than directly indicating biological plausibility.

**Scope:**  
Usually pipeline-level, sample-level, or analysis-level.

**Typical directionality:**  
Primarily reliability-reducing rather than biologically contradictory.

**Strength behavior:**  
QC evidence should generally modify confidence, interpretability, or review priority rather than functioning as direct biological support.

**Confidence caveats:**  
QC interpretation depends on platform behavior, sequencing characteristics, pipeline thresholds, contamination detection methods, and analytical reproducibility.

**Known failure modes:**  
False-positive QC flags, over-filtering, hidden pipeline assumptions, silent QC exclusion, and treating low-quality evidence as biological contradiction.

**Implementation note:**  
DEX-RDGP should preserve QC source identity, threshold definitions, filter rationale, and explicit distinction between excluded, flagged, and reviewable evidence states.

---

# 11. Scope-Aware Evidence Architecture

RDGP should preserve distinctions between:

- sample-specific evidence
- phenotype-scoped evidence
- cohort-scoped evidence
- external curated evidence
- functional/system-level evidence

These evidence scopes should remain explainable and independently auditable.

---

# 12. Explainability Requirements

Each evidence signal should remain explainable in terms of:

- biological meaning
- scope
- provenance
- role
- confidence
- strength
- uncertainty
- quality
- directionality

# 12A. Known Failure Modes and Edge Cases

RDGP evidence taxonomy must explicitly anticipate edge cases that can cause semantic drift during implementation.

## Ambiguous Gene Mapping

Variants may map to multiple genes or lack stable gene assignment. RDGP should preserve mapping ambiguity and avoid silently assigning evidence to one gene without recording the mapping basis.

Examples:

- transcript-to-gene ambiguity
- unresolved gene identifiers
- conflicting gene symbol mappings
- nearest-gene assignment for noncoding variants
- multi-gene structural variant overlap

## Conflicting Transcript Consequences

A single variant may have different predicted consequences across transcripts. RDGP should preserve transcript context where available and avoid treating one consequence as globally authoritative without a documented precedence rule.

## Multiple Annotations for One Variant

One variant may have multiple annotations from different tools or databases. RDGP should not naïvely count each annotation as independent evidence. Annotation provenance and source identity must remain visible.

## Multi-Gene and Noncoding Assignments

Noncoding or structural variants may be assigned to genes using nearest-gene, regulatory-feature, enhancer-target, or locus-window logic. These mappings are not equivalent to direct coding disruption and must remain explicitly labeled.

## Missing Source Database

If an evidence source is unavailable, not queried, or missing from a run, RDGP should preserve this as source missingness rather than interpreting lack of evidence as biological absence.

## Low-Quality Variant Evidence

Low-quality variants should not be silently discarded unless configured. They may be excluded, penalized, flagged, or reported separately, but the behavior must be explicit.

## Cohort-Derived Functional Evidence Mistaken as Patient-Specific

RSP or transcriptomic convergence evidence may derive from cohort-level or dataset-level analyses. RDGP must not treat cohort-derived evidence as direct patient-specific evidence unless a future interface explicitly supports patient-specific functional inputs.

## No GSC Match Mistaken as Negative Evidence

`no_gsc_match` means no phenotype-prior support was identified for the selected phenotype context. It does not mean the gene is biologically irrelevant, contradicted, or excluded.

---

# 12B. Implementation-Facing Recommended Evidence Fields

Numeric weighting systems should be treated as implementation mechanisms rather than replacements for biological semantics.

Evidence meaning must remain recoverable independently from numerical weighting behavior.

This taxonomy does not prescribe a final database schema, but DEX-RDGP should preserve enough structured fields to represent the taxonomy dimensions without semantic collapse.

Recommended evidence-level fields include:

| Field | Purpose |
|---|---|
| `evidence_id` | stable evidence record identifier |
| `sample_id` | sample context when evidence is sample-associated |
| `gene_id` | stable gene identifier when available |
| `gene_symbol` | human-readable gene label |
| `evidence_category` | top-level evidence class |
| `evidence_subtype` | more specific evidence type |
| `evidence_scope` | sample-specific, phenotype-scoped, cohort-scoped, external-curated, functional/system-level, pipeline/system-level |
| `evidence_role` | direct biological, curated interpretive, contextual prior, functional support, coherence, reliability-modifying |
| `evidence_direction` | positive, neutral/contextual, reliability-reducing, contradictory |
| `evidence_strength` | qualitative or calibrated strength tier |
| `evidence_confidence` | reliability/confidence tier independent of strength |
| `evidence_quality` | QC/reliability status |
| `evidence_status` | present, missing, not evaluated, unsupported, conflicting, low quality, zero observed |
| `source_name` | source system or database |
| `source_version` | source version when available |
| `source_record_id` | upstream identifier when available |
| `provenance_id` | internal provenance reference when available |
| `run_id` | pipeline or integration run provenance |
| `selected_phenotype` | phenotype context when evidence is phenotype-scoped |
| `gene_mapping_status` | stable, fallback, ambiguous, missing |
| `notes` | human-readable explanation or caveat |

## Implementation Constraint

DEX-RDGP should not encode all taxonomy dimensions into one mutually exclusive enum. Evidence category, scope, role, direction, confidence, quality, and status should remain independently representable.

## Minimal v1 Requirement

At minimum, RDGP evidence records should preserve:

```text
evidence_category
evidence_scope
evidence_direction
evidence_strength
evidence_confidence
evidence_status
source_name
run_id
gene_mapping_status
```

---

# 13. Validation Implications

Evidence taxonomy validation should assess:

- taxonomy consistency
- provenance preservation
- explainability retention
- uncertainty preservation
- scope preservation
- semantic stability
- resistance to evidence collapse
- extensibility

---

# 14. Forward Compatibility

This taxonomy is intended to remain compatible with future:

- probabilistic reasoning
- inheritance-aware models
- noncoding interpretation
- transcript-aware scoring
- heteroplasmy-aware modeling
- multi-omics convergence
- ontology extension
- machine-learning augmentation

---

# 15. Summary Principles

## Core Taxonomy Principle

```text
RDGP evidence taxonomy exists to preserve
biological meaning across heterogeneous evidence layers.
```

---

## Core Scope Principle

```text
Evidence from different identity-spaces
must remain distinguishable.
```

---

## Core Provenance Principle

```text
All evidence should remain traceable to origin.
```

---

## Core Uncertainty Principle

```text
Uncertainty must remain explicit rather than silently collapsed.
```

---

## Core Explainability Principle

```text
RDGP evidence taxonomy should explain
why evidence matters biologically,
not merely how it affects ranking.
```

---

# End of evidence_taxonomy.md