# RDGP Phase 1 Plan: From Scientific Governance to DEX Contracts

## Repository

`rare_disease_gene_prioritization` (`RDGP`)

## Purpose of This Phase

This phase converts the first SAGE-RDGP scientific governance deliverables into DEX-RDGP engineering control artifacts.

The goal is to move RDGP from design maturity into implementation readiness without prematurely coding around unstable semantics.

## Current Status

SAGE-RDGP has produced the four immediate scientific governance documents needed to ground DEX-RDGP work:

1. `scoring_rationale.md`
2. `evidence_taxonomy.md`
3. `uncertainty_and_null_semantics.md`
4. `validation_strategy.md`

DEX-RDGP inspection concluded that these documents are sufficiently mature to begin RDGP-specific system contract and implementation planning.

## Key Development Principle

RDGP v1 should be an explainable, deterministic, sample-scoped gene prioritization framework.

It should not become:

- a black-box predictor
- a diagnostic engine
- a known-gene rediscovery tool
- a raw variant annotation pipeline
- a persistent database replacement
- a transcriptomics pipeline

RDGP owns the reasoning layer.

## RDGP Core Identity

RDGP’s primary reasoning unit is:

```text
(sample_id, gene_id)
```

Each row should represent one gene evaluated within one biological sample.

## Ecosystem Boundary Reminder

| Repository | Primary Role | Identity Space |
|---|---|---|
| VAP | variant calling and annotation | `(sample_id, variant_id)` |
| VDB | persistent variant/sample/gene/annotation storage | variant/sample/database entities |
| GSC | phenotype-scoped gene priors | `(phenotype, gene_id)` |
| RSP | transcriptomic and network evidence | `(dataset_id, contrast_id, gene_id)` |
| RDGP | sample-scoped gene reasoning | `(sample_id, gene_id)` |

RDGP must preserve these identity spaces and join only through explicit interfaces.

---

# Recommendation on Confidence Modeling

DEX-RDGP recommends asking SAGE-RDGP to produce a focused confidence modeling document.

## Proposed New SAGE-RDGP Deliverable

`confidence_modeling_framework.md`

## Why This Is Needed

The first four SAGE-RDGP documents already distinguish:

- score
- confidence
- uncertainty
- evidence strength
- evidence quality
- evidence scope
- provenance

However, the next scientific-governance question is how confidence should be represented and propagated.

This document should define confidence as interpretive reliability, not as disease probability.

## Confidence Modeling Should Address

- What confidence means in RDGP
- How confidence differs from score
- How confidence differs from evidence strength
- How uncertainty modifies confidence
- How QC modifies confidence
- How conflicting evidence modifies confidence
- How missing evidence affects confidence or completeness
- How provenance affects confidence
- Whether confidence should be categorical, numeric, or hybrid
- Whether confidence should be reported per evidence item, per evidence channel, and/or per `(sample_id, gene_id)` row
- How confidence should be exposed in final outputs
- What confidence behaviors should be validated

## Important Constraint

Confidence modeling should not block DEX-RDGP from drafting the initial system contract and implementation plan.

Recommended approach:

```text
DEX begins architecture using current score/confidence separation.
SAGE develops confidence_modeling_framework.md in parallel.
DEX then integrates confidence modeling into contracts before implementation freeze.
```

---

# Phase 1 Plan of Attack

## Phase 1A — Scientific Governance Ingestion

- [ ] Read `scoring_rationale.md` as the authoritative scoring philosophy.
- [ ] Read `evidence_taxonomy.md` as the authoritative evidence semantics layer.
- [ ] Read `uncertainty_and_null_semantics.md` as the authoritative null/uncertainty behavior layer.
- [ ] Read `validation_strategy.md` as the authoritative validation philosophy.
- [ ] Identify all implementation-relevant invariants.
- [ ] Extract must-preserve semantic distinctions.
- [ ] Extract must-pass validation behaviors.
- [ ] Extract fields implied by taxonomy and uncertainty semantics.
- [ ] Identify open design questions requiring SAGE-RDGP follow-up.

## Phase 1B — DEX-RDGP Contract Drafting

Primary artifact:

`docs/contracts/system_contract.md`

Tasks:

- [ ] Define RDGP repository role and boundaries.
- [ ] Define RDGP primary identity: `(sample_id, gene_id)`.
- [ ] Define upstream interface assumptions for VDB-like inputs.
- [ ] Define GSC overlay assumptions and selected phenotype requirements.
- [ ] Define optional RSP/functional evidence extension boundary.
- [ ] Define required input tables or fixture schemas.
- [ ] Define required output tables.
- [ ] Define provenance requirements.
- [ ] Define null/uncertainty invariants.
- [ ] Define score/confidence separation as a system invariant.
- [ ] Define no-silent-row-multiplication rules.
- [ ] Define failure modes and required validation responses.

## Phase 1C — DEX-RDGP Implementation Planning

Primary artifact:

`docs/plans/implementation_plan.md`

Tasks:

- [ ] Define minimal v1 pipeline shape.
- [ ] Define internal package/module structure.
- [ ] Define fixture-first development strategy.
- [ ] Define configuration files needed for scoring behavior.
- [ ] Define Makefile targets.
- [ ] Define required tests by layer.
- [ ] Define minimal example input files.
- [ ] Define minimal example output files.
- [ ] Define logging and run manifest strategy.
- [ ] Define deterministic run behavior.
- [ ] Define development order by commit-sized units.

## Phase 1D — Scoring Contract / Scoring Interface Design

Possible artifact:

`docs/contracts/scoring_contract.md`

Tasks:

- [ ] Translate SAGE scoring philosophy into implementation-facing scoring behavior.
- [ ] Define scoring components without prematurely hard-coding final weights.
- [ ] Define strongest-hit anchoring behavior.
- [ ] Define bounded additive support behavior.
- [ ] Define GSC influence guardrails.
- [ ] Define optional functional evidence guardrails.
- [ ] Define calibration and scale-normalization requirements.
- [ ] Define score vs confidence vs uncertainty separation.
- [ ] Define required intermediate output fields.
- [ ] Define scoring profile concept.

## Phase 1E — Validation Harness Design

Possible artifact:

`docs/validation/validation_plan.md` or section within `implementation_plan.md`

Tasks:

- [ ] Define schema validation tests.
- [ ] Define interface validation tests.
- [ ] Define semantic anti-collapse tests.
- [ ] Define scoring behavior tests.
- [ ] Define score/confidence separation tests.
- [ ] Define GSC no-match tests.
- [ ] Define missing RSP evidence tests.
- [ ] Define ambiguity and conflict tests.
- [ ] Define provenance retention tests.
- [ ] Define deterministic reproducibility tests.
- [ ] Define discovery-preservation toy case.
- [ ] Define known-gene recovery toy case.

## Phase 1F — Repo Scaffold Alignment

Tasks:

- [ ] Review current RDGP scaffold.
- [ ] Confirm required docs folders exist.
- [ ] Add or plan missing folders if needed:
  - `config/`
  - `docs/contracts/`
  - `docs/plans/`
  - `docs/validation/`
  - `tests/unit/`
  - `tests/integration/`
  - `tests/validation/`
  - `tests/fixtures/`
- [ ] Confirm `.venv/` remains untracked.
- [ ] Plan `.gitignore` updates.
- [ ] Plan `requirements.txt` or `environment/requirements.txt` placement.
- [ ] Plan `Makefile` targets.
- [ ] Plan example data policy.

---

# Immediate DEX-RDGP Deliverables

After ingesting the four SAGE-RDGP documents, DEX-RDGP should produce, in order:

1. `docs/contracts/system_contract.md`
2. `docs/plans/implementation_plan.md`
3. optionally `docs/contracts/scoring_contract.md`
4. optionally `docs/validation/validation_plan.md`

Recommended order:

```text
system_contract.md
→ implementation_plan.md
→ scoring_contract.md
→ validation_plan.md
```

If the documents become too large, split them. If they remain readable, keep validation and scoring sections inside the first two DEX artifacts initially.

---

# Immediate SAGE-RDGP Follow-Up

Recommended next SAGE-RDGP assignment:

`confidence_modeling_framework.md`

This should be treated as a high-value refinement, not a blocker for initial DEX contract drafting.

## Suggested SAGE Prompt

```text
SAGE-RDGP, please produce confidence_modeling_framework.md for RDGP.

Use the existing four design documents as governing context:
- scoring_rationale.md
- evidence_taxonomy.md
- uncertainty_and_null_semantics.md
- validation_strategy.md

Define confidence as interpretive reliability, distinct from prioritization score, evidence strength, and uncertainty state.

Please specify how confidence should be represented, propagated, reported, and validated in RDGP v1 without turning RDGP into a probabilistic diagnostic system.
```

---

# Implementation Gate

DEX-RDGP should not begin coding until the following are complete:

- [ ] Four SAGE-RDGP documents ingested.
- [ ] `system_contract.md` drafted and reviewed.
- [ ] `implementation_plan.md` drafted and reviewed.
- [ ] Minimal scoring interface agreed.
- [ ] Minimal validation expectations agreed.
- [ ] User approves transition from design to implementation.

---

# Definition of Success for This Phase

This phase succeeds when RDGP has:

- clear repository boundaries
- explicit identity-space discipline
- defined input/output expectations
- explainable scoring architecture
- null/uncertainty behavior constraints
- validation invariants
- implementation sequencing
- fixture-first development path
- no ambiguity about DEX vs SAGE ownership

At the end of this phase, RDGP should be ready for controlled, deterministic implementation.

---

# DEX-RDGP Position

DEX-RDGP can now proceed with contract and implementation-plan drafting based on the four immediate SAGE-RDGP documents.

SAGE-RDGP should next refine confidence modeling in parallel.

The correct sequence is:

```text
scientific governance
→ engineering contracts
→ implementation plan
→ controlled implementation
→ validation harness
→ real upstream integration
```

This preserves the design-first development culture that RDGP requires.
