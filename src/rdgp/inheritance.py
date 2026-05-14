"""Inheritance-aware compatibility reasoning for RDGP."""

VALID_INHERITANCE_MODES={
    "autosomal_recessive",
    "autosomal_dominant",
    "x_linked",
    "mitochondrial",
    "unknown",
    "unresolved",
}

VALID_ZYGOSITY_CONTEXTS={
    "heterozygous",
    "homozygous",
    "hemizygous",
    "heteroplasmic",
    "unknown",
}

def normalize_inheritance_mode(value:str|None)->str:
    if value is None:
        return "unknown"
    value=value.strip().lower()
    if value in VALID_INHERITANCE_MODES:
        return value
    return "unresolved"

def normalize_zygosity_context(value:str|None)->str:
    if value is None:
        return "unknown"
    value=value.strip().lower()
    if value in VALID_ZYGOSITY_CONTEXTS:
        return value
    return "unknown"

def evaluate_inheritance_context(inheritance_mode:str|None,zygosity_context:str|None)->dict:
    inheritance_mode=normalize_inheritance_mode(inheritance_mode)
    zygosity_context=normalize_zygosity_context(zygosity_context)

    result={
        "inheritance_mode":inheritance_mode,
        "zygosity_context":zygosity_context,
        "inheritance_support":"unresolved",
        "inheritance_conflict":"none",
        "inheritance_uncertainty":"visible",
        "inheritance_explanation":"",
    }

    if inheritance_mode in {"unknown","unresolved"}:
        result["inheritance_explanation"]="Inheritance mode unresolved or unavailable."
        return result

    if zygosity_context=="unknown":
        result["inheritance_explanation"]="Zygosity context unavailable."
        return result

    if inheritance_mode=="autosomal_recessive":
        if zygosity_context=="homozygous":
            result["inheritance_support"]="compatible"
            result["inheritance_uncertainty"]="limited"
            result["inheritance_explanation"]="Homozygous context compatible with recessive inheritance."
        elif zygosity_context=="heterozygous":
            result["inheritance_support"]="partial"
            result["inheritance_conflict"]="possible"
            result["inheritance_explanation"]="Single heterozygous context may be incomplete for recessive inheritance."
        else:
            result["inheritance_explanation"]="Inheritance interpretation remains unresolved."

    elif inheritance_mode=="autosomal_dominant":
        if zygosity_context=="heterozygous":
            result["inheritance_support"]="compatible"
            result["inheritance_uncertainty"]="limited"
            result["inheritance_explanation"]="Heterozygous context compatible with dominant inheritance."
        else:
            result["inheritance_support"]="contextual"
            result["inheritance_explanation"]="Dominant inheritance interpretation requires biological context."

    elif inheritance_mode=="x_linked":
        if zygosity_context=="hemizygous":
            result["inheritance_support"]="compatible"
            result["inheritance_uncertainty"]="limited"
            result["inheritance_explanation"]="Hemizygous context compatible with X-linked inheritance."
        else:
            result["inheritance_support"]="contextual"
            result["inheritance_explanation"]="X-linked interpretation may depend on sex-specific biological context."

    elif inheritance_mode=="mitochondrial":
        if zygosity_context=="heteroplasmic":
            result["inheritance_support"]="compatible"
            result["inheritance_uncertainty"]="visible"
            result["inheritance_explanation"]="Heteroplasmic context compatible with mitochondrial inheritance."
        else:
            result["inheritance_support"]="contextual"
            result["inheritance_explanation"]="Mitochondrial inheritance interpretation may depend on heteroplasmy context."

    return result
