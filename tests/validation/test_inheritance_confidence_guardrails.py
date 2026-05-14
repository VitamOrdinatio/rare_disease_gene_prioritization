from rdgp.inheritance import evaluate_inheritance_context
from rdgp.confidence import apply_inheritance_confidence_context

def test_inheritance_conflict_does_not_zero_confidence():
    inheritance=evaluate_inheritance_context(
        "autosomal_recessive",
        "heterozygous",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="high",
        inheritance_result=inheritance,
    )

    assert result["confidence_tier"]!="none"

def test_inheritance_uncertainty_remains_explainable():
    inheritance=evaluate_inheritance_context(
        "unknown",
        "unknown",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="moderate",
        inheritance_result=inheritance,
    )

    assert result["confidence_reason"]!=""

def test_inheritance_behavior_not_collapsed_into_score():
    inheritance=evaluate_inheritance_context(
        "mitochondrial",
        "heteroplasmic",
    )

    result=apply_inheritance_confidence_context(
        confidence_tier="high",
        inheritance_result=inheritance,
    )

    assert "confidence_tier" in result
    assert "inheritance_confidence" in result
