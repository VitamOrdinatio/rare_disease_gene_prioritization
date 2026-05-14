"""Human-readable explainability helpers for RDGP v1."""
from __future__ import annotations
import pandas as pd

def _join_nonempty(parts:list[str])->str:
    return " ".join([part for part in parts if part and str(part).strip()])

def build_evidence_summary(row)->str:
    parts=[
        f"Gene {row.get('gene_symbol','')} ranked with priority_score={row.get('priority_score','')}.",
        f"Variant evidence score={row.get('variant_evidence_score','')} based on max_variant_severity={row.get('max_variant_severity','')}.",
        f"GSC overlay status={row.get('gsc_overlay_status','')} with gsc_prior_score={row.get('gsc_prior_score','')}.",
        f"Functional evidence status={row.get('functional_evidence_score','')}.",
        f"Confidence tier={row.get('confidence_tier','')} ({row.get('confidence_state','')}).",
    ]
    return _join_nonempty(parts)

def build_provenance_summary(row)->str:
    parts=[
        f"Variant provenance={row.get('variant_provenance_summary','')}.",
        f"Source pipeline={row.get('source_pipeline','')}.",
        f"Input run_id={row.get('run_id','')}.",
    ]
    if str(row.get("gsc_overlay_status","")) in {"matched_gene_id","matched_gene_symbol"}:
        parts.append(f"GSC provenance={row.get('gsc_provenance_id','')} from gsc_run_id={row.get('gsc_run_id','')} using profile={row.get('gsc_scoring_profile','')}.")
    else:
        parts.append(f"GSC provenance unavailable because overlay status={row.get('gsc_overlay_status','')}.")
    return _join_nonempty(parts)

def build_status_summary(row)->str:
    states=[]
    if str(row.get("gsc_overlay_status","")):
        states.append(f"gsc:{row.get('gsc_overlay_status')}")
    if str(row.get("gene_mapping_status","")):
        states.append(f"mapping:{row.get('gene_mapping_status')}")
    if str(row.get("quality_summary","")):
        states.append(f"quality:{row.get('quality_summary')}")
    if str(row.get("confidence_flags","")):
        states.append(f"confidence_flags:{row.get('confidence_flags')}")
    return ";".join(states)

def add_explanations(df:pd.DataFrame)->pd.DataFrame:
    """Add human-readable explanation columns without changing scores or ranks."""
    result=df.copy()
    result["evidence_summary"]=[build_evidence_summary(row) for _,row in result.iterrows()]
    result["provenance_summary"]=[build_provenance_summary(row) for _,row in result.iterrows()]
    result["evidence_status_summary"]=[build_status_summary(row) for _,row in result.iterrows()]
    return result

def build_inheritance_explanation(inheritance_result:dict)->str:
    support=inheritance_result.get("inheritance_support","unresolved")
    conflict=inheritance_result.get("inheritance_conflict","none")
    uncertainty=inheritance_result.get("inheritance_uncertainty","visible")
    explanation=inheritance_result.get("inheritance_explanation","")

    components=[
        f"inheritance_support={support}",
        f"inheritance_conflict={conflict}",
        f"inheritance_uncertainty={uncertainty}",
    ]

    if explanation:
        components.append(explanation)

    return "; ".join(components)
