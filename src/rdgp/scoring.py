"""Transparent scoring engine for RDGP v1."""
from __future__ import annotations
from pathlib import Path
import math
import pandas as pd
import yaml

DEFAULT_SEVERITY_WEIGHTS={
"LOF":8,
"splice":7,
"missense":5,
"synonymous":1,
"none":0,
"unknown":0,
}

def load_scoring_profile(path:str|Path)->dict:
    with Path(path).open("r",encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}

def _safe_float(value)->float:
    if value is None:
        return 0.0
    text=str(value).strip()
    if text in {"","missing","unknown","not_evaluated","unsupported","unresolved"}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0

def _severity_anchor(severity:str,weights:dict[str,float])->float:
    return float(weights.get(str(severity),weights.get("unknown",0)))

def compute_variant_evidence_score(df:pd.DataFrame,profile:dict)->pd.DataFrame:
    result=df.copy()
    severity_weights=profile.get("variant_scoring",{}).get("severity_weights",DEFAULT_SEVERITY_WEIGHTS)
    component_weights=profile.get("variant_scoring",{}).get("component_weights",{})
    support_cap=float(profile.get("variant_scoring",{}).get("caps",{}).get("additive_support_cap",6))
    variant_scores=[]
    support_scores=[]
    for _,row in result.iterrows():
        anchor=_severity_anchor(str(row.get("max_variant_severity","unknown")),severity_weights)
        support=0.0
        for field,weight in component_weights.items():
            support+=_safe_float(row.get(field))*float(weight)
        support=min(support,support_cap)
        variant_score=anchor+support
        variant_scores.append(round(variant_score,3))
        support_scores.append(round(support,3))
    result["variant_anchor_score"]=variant_scores
    result["variant_support_score"]=support_scores
    result["variant_evidence_score"]=variant_scores
    return result

def compute_gsc_prior_score(df:pd.DataFrame,profile:dict)->pd.DataFrame:
    result=df.copy()
    gsc_cfg=profile.get("gsc_scoring",{})
    enabled=bool(gsc_cfg.get("enabled",True))
    max_contribution=float(gsc_cfg.get("max_contribution",4))
    gsc_scores=[]
    for _,row in result.iterrows():
        if not enabled:
            gsc_scores.append(0.0)
            continue
        status=str(row.get("gsc_overlay_status",""))
        if status not in {"matched_gene_id","matched_gene_symbol"}:
            gsc_scores.append(0.0)
            continue
        semantic_score=_safe_float(row.get("gsc_semantic_consensus_score"))
        bounded=min(semantic_score*max_contribution,max_contribution)
        gsc_scores.append(round(bounded,3))
    result["gsc_prior_score"]=gsc_scores
    return result

def compute_functional_evidence_score(df:pd.DataFrame)->pd.DataFrame:
    result=df.copy()
    result["functional_evidence_score"]="not_evaluated"
    return result

def compute_priority_score(df:pd.DataFrame,profile:dict)->pd.DataFrame:
    result=df.copy()
    rounding=int(profile.get("composite_scoring",{}).get("rounding_digits",3))
    scores=[]
    for _,row in result.iterrows():
        variant_score=_safe_float(row.get("variant_evidence_score"))
        gsc_score=_safe_float(row.get("gsc_prior_score"))
        functional_score=_safe_float(row.get("functional_evidence_score"))
        total=variant_score+gsc_score+functional_score
        scores.append(round(total,rounding))
    result["priority_score"]=scores
    return result

def score_genes(df:pd.DataFrame,profile:dict)->pd.DataFrame:
    result=compute_variant_evidence_score(df,profile)
    result=compute_gsc_prior_score(result,profile)
    result=compute_functional_evidence_score(result)
    result=compute_priority_score(result,profile)
    return result
