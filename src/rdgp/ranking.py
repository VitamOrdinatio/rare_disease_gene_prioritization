"""Deterministic ranking helpers for RDGP v1."""
from __future__ import annotations
import pandas as pd

CONFIDENCE_ORDER={"high":4,"moderate":3,"limited":2,"low":1,"unresolved":0}

def rank_genes(df:pd.DataFrame)->pd.DataFrame:
    """Assign deterministic ranks using documented tie-breakers."""
    result=df.copy()
    result["_confidence_order"]=result["confidence_tier"].map(CONFIDENCE_ORDER).fillna(-1)
    result["_priority_score_num"]=pd.to_numeric(result["priority_score"],errors="coerce").fillna(0)
    result["_variant_score_num"]=pd.to_numeric(result["variant_evidence_score"],errors="coerce").fillna(0)
    result["_gsc_score_num"]=pd.to_numeric(result["gsc_prior_score"],errors="coerce").fillna(0)
    result=result.sort_values(
        by=["sample_id","_priority_score_num","_confidence_order","_variant_score_num","_gsc_score_num","gene_symbol","gene_id"],
        ascending=[True,False,False,False,False,True,True],
        kind="mergesort",
    ).reset_index(drop=True)
    result["rank"]=result.groupby("sample_id").cumcount()+1
    result=result.drop(columns=["_confidence_order","_priority_score_num","_variant_score_num","_gsc_score_num"])
    return result
