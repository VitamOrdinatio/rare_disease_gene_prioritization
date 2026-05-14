"""Semantic evidence-context substrate for RDGP."""

REQUIRED_EVIDENCE_FIELDS=[
    "evidence_id",
    "gene_id",
    "evidence_category",
    "evidence_direction",
    "evidence_scope",
    "evidence_status",
    "confidence_context",
    "uncertainty_context",
    "provenance_id",
]

DEFAULT_EVIDENCE_ITEM={
    "evidence_id":"unknown",
    "sample_id":"unknown",
    "gene_id":"unknown",
    "gene_symbol":"unknown",
    "evidence_category":"unknown",
    "evidence_direction":"unresolved",
    "evidence_scope":"unknown",
    "evidence_status":"unresolved",
    "biological_context":"unknown",
    "mechanism_context":"unknown",
    "tissue_context":"unknown",
    "temporal_context":"unknown",
    "transcript_context":"unknown",
    "interaction_context":"unknown",
    "confidence_context":"unresolved_confidence",
    "uncertainty_context":"unresolved",
    "provenance_id":"unknown",
    "source_name":"unknown",
    "source_version":"unknown",
    "run_id":"unknown",
    "evidence_description":"",
}

VALID_EVIDENCE_DIRECTIONS={
    "supportive",
    "contradictory",
    "reliability_reducing",
    "context_modifying",
    "uncertainty_preserving",
    "unresolved",
}

VALID_EVIDENCE_STATUSES={
    "present",
    "missing",
    "not_evaluated",
    "unsupported",
    "unresolved",
    "ambiguous",
    "conflicting",
    "low_quality",
}

def normalize_token(value:str|None,allowed:set[str],default:str)->str:
    if value is None:
        return default
    token=str(value).strip().lower().replace(" ","_").replace("-","_")
    if token in allowed:
        return token
    return default

def normalize_evidence_direction(value:str|None)->str:
    return normalize_token(value,VALID_EVIDENCE_DIRECTIONS,"unresolved")

def normalize_evidence_status(value:str|None)->str:
    return normalize_token(value,VALID_EVIDENCE_STATUSES,"unresolved")

def build_evidence_item(values:dict)->dict:
    item=DEFAULT_EVIDENCE_ITEM.copy()
    for key,value in values.items():
        if key in item:
            item[key]="" if value is None else str(value)
    item["evidence_direction"]=normalize_evidence_direction(item["evidence_direction"])
    item["evidence_status"]=normalize_evidence_status(item["evidence_status"])
    return item

def validate_evidence_item(item:dict)->list[str]:
    errors=[]
    for field in REQUIRED_EVIDENCE_FIELDS:
        if field not in item or item[field] in {"","unknown"}:
            errors.append(f"missing_required_evidence_field:{field}")
    if item.get("evidence_direction") not in VALID_EVIDENCE_DIRECTIONS:
        errors.append("invalid_evidence_direction")
    if item.get("evidence_status") not in VALID_EVIDENCE_STATUSES:
        errors.append("invalid_evidence_status")
    return errors

def summarize_evidence_item(item:dict)->str:
    return (
        f"{item.get('evidence_category','unknown')} evidence "
        f"for gene_id={item.get('gene_id','unknown')} "
        f"direction={item.get('evidence_direction','unresolved')} "
        f"status={item.get('evidence_status','unresolved')} "
        f"scope={item.get('evidence_scope','unknown')} "
        f"provenance={item.get('provenance_id','unknown')}"
    )
