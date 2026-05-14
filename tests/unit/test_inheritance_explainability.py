from rdgp.inheritance import evaluate_inheritance_context
from rdgp.explainability import build_inheritance_explanation

def test_build_inheritance_explanation_supportive():
    inheritance=evaluate_inheritance_context(
        "autosomal_dominant",
        "heterozygous",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "compatible" in explanation.lower()
    assert "dominant" in explanation.lower()

def test_build_inheritance_explanation_partial():
    inheritance=evaluate_inheritance_context(
        "autosomal_recessive",
        "heterozygous",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "incomplete" in explanation.lower() or "partial" in explanation.lower()

def test_build_inheritance_explanation_unresolved():
    inheritance=evaluate_inheritance_context(
        "unknown",
        "unknown",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "unresolved" in explanation.lower() or "unavailable" in explanation.lower()
