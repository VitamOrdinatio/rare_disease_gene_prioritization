"""Future-facing mechanistic reasoning scaffolding for RDGP."""

VALID_MECHANISM_CONTEXTS={
    "loss_of_function",
    "gain_of_function",
    "dominant_negative",
    "haploinsufficiency",
    "dosage_sensitive",
    "unknown",
    "unresolved",
}

def normalize_mechanism_context(value:str|None)->str:
    if value is None:
        return "unknown"

    value=value.strip().lower()

    if value in VALID_MECHANISM_CONTEXTS:
        return value

    return "unresolved"

def evaluate_mechanism_context(mechanism_context:str|None)->dict:
    mechanism_context=normalize_mechanism_context(mechanism_context)

    result={
        "mechanism_context":mechanism_context,
        "mechanism_support":"contextual",
        "mechanism_conflict":"none",
        "mechanism_explanation":"",
    }

    if mechanism_context in {"unknown","unresolved"}:
        result["mechanism_explanation"]="Mechanistic interpretation unresolved or unavailable."
        return result

    if mechanism_context=="loss_of_function":
        result["mechanism_support"]="compatible"
        result["mechanism_explanation"]="Loss-of-function mechanism context preserved."

    elif mechanism_context=="gain_of_function":
        result["mechanism_support"]="compatible"
        result["mechanism_explanation"]="Gain-of-function mechanism context preserved."

    elif mechanism_context=="dominant_negative":
        result["mechanism_support"]="contextual"
        result["mechanism_explanation"]="Dominant-negative interpretation requires biological context."

    elif mechanism_context=="haploinsufficiency":
        result["mechanism_support"]="contextual"
        result["mechanism_explanation"]="Haploinsufficiency interpretation remains context-dependent."

    elif mechanism_context=="dosage_sensitive":
        result["mechanism_support"]="contextual"
        result["mechanism_explanation"]="Dosage-sensitive interpretation remains context-dependent."

    return result
