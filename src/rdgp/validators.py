"""Validation helpers for RDGP v1 fixture-first implementation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import pandas as pd
from rdgp.schemas import GENE_EVIDENCE_REQUIRED_COLUMNS,GSC_OVERLAY_REQUIRED_COLUMNS,NULL_STATES,GENE_MAPPING_STATUSES

@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    errors: list[str]
    warnings: list[str]

def _missing_columns(df:pd.DataFrame,required:Iterable[str])->list[str]:
    return [col for col in required if col not in df.columns]

def validate_required_columns(df:pd.DataFrame,required:Iterable[str],table_name:str)->ValidationResult:
    missing=_missing_columns(df,required)
    errors=[f"{table_name} missing required column: {col}" for col in missing]
    return ValidationResult(passed=not errors,errors=errors,warnings=[])

def validate_gene_evidence_schema(df:pd.DataFrame)->ValidationResult:
    result=validate_required_columns(df,GENE_EVIDENCE_REQUIRED_COLUMNS,"gene_evidence")
    errors=list(result.errors)
    warnings=[]
    if "sample_id" in df.columns and df["sample_id"].isna().any():
        errors.append("gene_evidence contains missing sample_id values")
    if "gene_symbol" in df.columns and df["gene_symbol"].isna().any():
        errors.append("gene_evidence contains missing gene_symbol values")
    if {"gene_id","gene_mapping_status"}.issubset(df.columns):
        for idx,row in df.iterrows():
            gene_id=str(row["gene_id"]).strip() if not pd.isna(row["gene_id"]) else ""
            status=str(row["gene_mapping_status"]).strip()
            if status not in GENE_MAPPING_STATUSES:
                errors.append(f"row {idx}: invalid gene_mapping_status '{status}'")
            if not gene_id and status not in {"fallback","ambiguous","missing","unresolved"}:
                errors.append(f"row {idx}: missing gene_id requires fallback/ambiguous/missing/unresolved gene_mapping_status")
    return ValidationResult(passed=not errors,errors=errors,warnings=warnings)

def validate_gsc_overlay_schema(df:pd.DataFrame)->ValidationResult:
    result=validate_required_columns(df,GSC_OVERLAY_REQUIRED_COLUMNS,"gsc_overlay")
    errors=list(result.errors)
    warnings=[]
    if "phenotype" in df.columns and df["phenotype"].isna().any():
        errors.append("gsc_overlay contains missing phenotype values")
    if "gene_id" in df.columns and "gene_symbol" in df.columns:
        both_missing=df["gene_id"].fillna("").astype(str).str.strip().eq("") & df["gene_symbol"].fillna("").astype(str).str.strip().eq("")
        if both_missing.any():
            errors.append("gsc_overlay contains rows missing both gene_id and gene_symbol")
    return ValidationResult(passed=not errors,errors=errors,warnings=warnings)

def validate_semantic_state_distinction()->ValidationResult:
    errors=[]
    if "missing"=="zero_observed":
        errors.append("semantic collapse: missing equals zero_observed")
    if "unsupported"=="contradictory":
        errors.append("semantic collapse: unsupported equals contradictory")
    if "unresolved"=="low_quality":
        errors.append("semantic collapse: unresolved equals low_quality")
    required={"missing","zero_observed","unsupported","contradictory","unresolved","low_quality"}
    absent=required-NULL_STATES
    for state in sorted(absent):
        errors.append(f"required semantic state absent: {state}")
    return ValidationResult(passed=not errors,errors=errors,warnings=[])

def validation_result_to_dict(result:ValidationResult,label:str)->dict:
    return {
        "label":label,
        "passed":result.passed,
        "errors":result.errors,
        "warnings":result.warnings,
    }

def summarize_validation_results(results:list[dict])->dict:
    passed=all(item["passed"] for item in results)
    return {
        "passed":passed,
        "results":results,
        "error_count":sum(len(item.get("errors",[])) for item in results),
        "warning_count":sum(len(item.get("warnings",[])) for item in results),
    }
