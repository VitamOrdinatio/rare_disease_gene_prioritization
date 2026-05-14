"""Qualitative confidence engine for RDGP v1."""
from __future__ import annotations
import pandas as pd

CONFIDENCE_HIGH="high"
CONFIDENCE_MODERATE="moderate"
CONFIDENCE_LIMITED="limited"
CONFIDENCE_LOW="low"
CONFIDENCE_UNRESOLVED="unresolved"

def _split_flags(value)->set[str]:
    text=str(value or "").strip()
    if not text:
        return set()
    return {part.strip() for part in text.replace(";",",").split(",") if part.strip()}

def _has_positive_gsc(row)->bool:
    return str(row.get("gsc_overlay_status","")) in {"matched_gene_id","matched_gene_symbol"}

def _has_strong_variant_evidence(row)->bool:
    try:
        return float(row.get("variant_evidence_score",0))>=8
    except ValueError:
        return False

def _has_moderate_variant_evidence(row)->bool:
    try:
        return float(row.get("variant_evidence_score",0))>=5
    except ValueError:
        return False

def _confidence_for_row(row)->dict[str,str]:
    flags=[]
    limitations=[]
    sources=[]
    mapping=str(row.get("gene_mapping_status","")).strip()
    quality=str(row.get("quality_summary","")).strip()
    provenance=str(row.get("variant_provenance_summary","")).strip()
    gsc_status=str(row.get("gsc_overlay_status","")).strip()
    max_severity=str(row.get("max_variant_severity","")).strip()
    if mapping in {"ambiguous","missing","unresolved"}:
        flags.append("mapping_limited")
        limitations.append("gene mapping unresolved or ambiguous")
    if quality in {"low_quality","failed_qc"}:
        flags.append("quality_limited")
        limitations.append("variant evidence quality is limited")
    if "conflict" in provenance.lower() or "conflicting" in provenance.lower():
        flags.append("conflict_limited")
        limitations.append("conflicting annotation evidence present")
    if gsc_status in {"no_gsc_match","unsupported_phenotype_context"}:
        flags.append("prior_limited")
        limitations.append("phenotype-prior support is unavailable or unsupported")
    if str(row.get("functional_evidence_score","")) in {"not_evaluated","missing",""}:
        flags.append("functional_not_evaluated")
    if _has_strong_variant_evidence(row):
        sources.append("strong_variant_evidence")
    elif _has_moderate_variant_evidence(row):
        sources.append("moderate_variant_evidence")
    if _has_positive_gsc(row):
        sources.append("phenotype_scoped_gsc_support")
    if mapping in {"ambiguous","missing","unresolved"}:
        tier=CONFIDENCE_UNRESOLVED
        state="confidence_limited_by_mapping"
    elif quality in {"low_quality","failed_qc"} or "conflict_limited" in flags:
        tier=CONFIDENCE_LOW
        state="confidence_limited_by_quality_or_conflict"
    elif _has_strong_variant_evidence(row) and _has_positive_gsc(row) and quality=="pass":
        tier=CONFIDENCE_HIGH
        state="high_confidence_interpretive_reliability"
    elif _has_strong_variant_evidence(row) and quality=="pass":
        tier=CONFIDENCE_MODERATE
        state="moderate_confidence_strong_sample_evidence"
    elif _has_moderate_variant_evidence(row) or _has_positive_gsc(row):
        tier=CONFIDENCE_LIMITED
        state="limited_confidence_partial_support"
    else:
        tier=CONFIDENCE_LIMITED
        state="limited_confidence_sparse_evidence"
    explanation_parts=[]
    if sources:
        explanation_parts.append("Confidence supported by "+", ".join(sources)+".")
    else:
        explanation_parts.append("Confidence is limited by sparse supporting evidence.")
    if limitations:
        explanation_parts.append("Limitations: "+", ".join(limitations)+".")
    if "functional_not_evaluated" in flags:
        explanation_parts.append("Functional evidence was not evaluated and is treated as completeness context, not negative evidence.")
    if gsc_status=="no_gsc_match":
        explanation_parts.append("No GSC match is treated as absent prior support, not contradiction.")
    return {
        "confidence_tier":tier,
        "confidence_state":state,
        "confidence_sources":";".join(sources),
        "confidence_modifiers":";".join(flags),
        "confidence_flags":";".join(flags),
        "confidence_explanation":" ".join(explanation_parts),
        "confidence_completeness":"limited" if flags else "complete_for_enabled_channels",
        "confidence_limitations":";".join(limitations),
    }

def compute_confidence(df:pd.DataFrame)->pd.DataFrame:
    """Compute qualitative confidence fields without modifying priority_score."""
    result=df.copy()
    records=[_confidence_for_row(row) for _,row in result.iterrows()]
    confidence_df=pd.DataFrame(records,index=result.index)
    for col in confidence_df.columns:
        result[col]=confidence_df[col]
    return result
