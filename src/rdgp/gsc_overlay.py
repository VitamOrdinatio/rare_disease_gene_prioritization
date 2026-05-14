"""Phenotype-scoped GSC overlay helpers for RDGP."""
from __future__ import annotations
import pandas as pd

GSC_STATUS_MATCHED_GENE_ID="matched_gene_id"
GSC_STATUS_MATCHED_GENE_SYMBOL="matched_gene_symbol"
GSC_STATUS_NO_MATCH="no_gsc_match"
GSC_STATUS_AMBIGUOUS="ambiguous_gene_mapping"
GSC_STATUS_UNSUPPORTED_PHENOTYPE="unsupported_phenotype_context"

GSC_OVERLAY_COLUMNS=[
"gsc_overlay_status",
"gsc_consensus_score",
"gsc_semantic_consensus_score",
"gsc_source_count",
"gsc_weighted_source_sum",
"gsc_semantic_channel_summary",
"gsc_source_list",
"gsc_active_score",
"gsc_scoring_profile",
"gsc_version",
"gsc_release_id",
"gsc_run_id",
"gsc_provenance_id",
]

def _empty_overlay_values(status:str)->dict[str,str]:
    values={col:"" for col in GSC_OVERLAY_COLUMNS}
    values["gsc_overlay_status"]=status
    return values

def _validate_selected_phenotype(selected_phenotype:str|None)->str:
    if selected_phenotype is None or str(selected_phenotype).strip()=="":
        raise ValueError("selected_phenotype is required for GSC overlay")
    return str(selected_phenotype)

def _phenotype_subset(gsc_df:pd.DataFrame,selected_phenotype:str)->pd.DataFrame:
    if "phenotype" not in gsc_df.columns:
        raise ValueError("gsc_overlay missing required column: phenotype")
    return gsc_df[gsc_df["phenotype"].astype(str)==selected_phenotype].copy()

def _ensure_unique_key(df:pd.DataFrame,key:str,context:str)->None:
    if key not in df.columns:
        raise ValueError(f"{context} missing required column: {key}")
    nonempty=df[df[key].fillna("").astype(str).str.strip()!=""]
    duplicated=nonempty[key].duplicated(keep=False)
    if duplicated.any():
        dupes=sorted(nonempty.loc[duplicated,key].astype(str).unique())
        raise ValueError(f"{context} contains duplicate {key} values that would cause row multiplication: {dupes}")

def _overlay_from_row(row:pd.Series,status:str)->dict[str,str]:
    return {
        "gsc_overlay_status":status,
        "gsc_consensus_score":str(row.get("consensus_score","")),
        "gsc_semantic_consensus_score":str(row.get("semantic_consensus_score","")),
        "gsc_source_count":str(row.get("source_count","")),
        "gsc_weighted_source_sum":str(row.get("weighted_source_sum","")),
        "gsc_semantic_channel_summary":str(row.get("semantic_channel_summary","")),
        "gsc_source_list":str(row.get("source_list","")),
        "gsc_active_score":str(row.get("active_score","")),
        "gsc_scoring_profile":str(row.get("scoring_profile","")),
        "gsc_version":str(row.get("gsc_version","")),
        "gsc_release_id":str(row.get("release_id","")),
        "gsc_run_id":str(row.get("run_id","")),
        "gsc_provenance_id":str(row.get("provenance_id","")),
    }

def attach_gsc_overlay(gene_df:pd.DataFrame,gsc_df:pd.DataFrame,selected_phenotype:str|None,allow_symbol_fallback:bool=False)->pd.DataFrame:
    """Attach phenotype-scoped GSC evidence without changing RDGP row identity."""
    selected_phenotype=_validate_selected_phenotype(selected_phenotype)
    original_rows=len(gene_df)
    phenotype_gsc=_phenotype_subset(gsc_df,selected_phenotype)
    result=gene_df.copy()
    result["selected_phenotype"]=selected_phenotype
    for col in GSC_OVERLAY_COLUMNS:
        result[col]=""
    if phenotype_gsc.empty:
        for idx in result.index:
            values=_empty_overlay_values(GSC_STATUS_UNSUPPORTED_PHENOTYPE)
            for col,val in values.items():
                result.at[idx,col]=val
        return result
    _ensure_unique_key(phenotype_gsc,"gene_id","gsc_overlay phenotype subset")
    gsc_by_gene_id={str(row["gene_id"]).strip():row for _,row in phenotype_gsc.iterrows() if str(row.get("gene_id","")).strip()!=""}
    gsc_by_symbol={}
    if allow_symbol_fallback:
        _ensure_unique_key(phenotype_gsc,"gene_symbol","gsc_overlay phenotype subset")
        gsc_by_symbol={str(row["gene_symbol"]).strip():row for _,row in phenotype_gsc.iterrows() if str(row.get("gene_symbol","")).strip()!=""}
    for idx,row in result.iterrows():
        gene_id=str(row.get("gene_id","")).strip()
        gene_symbol=str(row.get("gene_symbol","")).strip()
        gene_mapping_status=str(row.get("gene_mapping_status","")).strip()
        overlay_values=None
        if gene_id and gene_id in gsc_by_gene_id:
            overlay_values=_overlay_from_row(gsc_by_gene_id[gene_id],GSC_STATUS_MATCHED_GENE_ID)
        elif allow_symbol_fallback and gene_symbol and gene_symbol in gsc_by_symbol:
            overlay_values=_overlay_from_row(gsc_by_symbol[gene_symbol],GSC_STATUS_MATCHED_GENE_SYMBOL)
        elif gene_mapping_status in {"ambiguous","missing","unresolved"}:
            overlay_values=_empty_overlay_values(GSC_STATUS_AMBIGUOUS)
        else:
            overlay_values=_empty_overlay_values(GSC_STATUS_NO_MATCH)
        for col,val in overlay_values.items():
            result.at[idx,col]=val
    if len(result)!=original_rows:
        raise RuntimeError("GSC overlay changed row count; this violates RDGP no-silent-row-multiplication invariant")
    return result
