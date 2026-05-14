from rdgp.inheritance import evaluate_inheritance_context
from rdgp.confidence import apply_inheritance_confidence_context

def test_recessive_partial_support_reduces_confidence():
    inheritance=evaluate_inheritance_context(
        "autosomal_recessive",
        "heterozygous",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="high",
        inheritance_result=inheritance,
    )

    assert result["confidence_tier"] in {"moderate","limited"}
    assert "inheritance" in result["confidence_reason"].lower()

def test_unknown_inheritance_preserves_visibility():
    inheritance=evaluate_inheritance_context(
        "unknown",
        "unknown",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="moderate",
        inheritance_result=inheritance,
    )

    assert result["inheritance_confidence"]=="limited"

def test_compatible_dominant_preserves_confidence():
    inheritance=evaluate_inheritance_context(
        "autosomal_dominant",
        "heterozygous",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="high",
        inheritance_result=inheritance,
    )

    assert result["confidence_tier"]=="high"
