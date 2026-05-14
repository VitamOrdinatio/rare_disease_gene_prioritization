from rdgp.inheritance import evaluate_inheritance_context
from rdgp.explainability import build_inheritance_explanation

def test_inheritance_explanation_preserves_conflict_visibility():
    inheritance=evaluate_inheritance_context(
        "autosomal_recessive",
        "heterozygous",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "possible" in explanation.lower()

def test_inheritance_explanation_preserves_uncertainty_visibility():
    inheritance=evaluate_inheritance_context(
        "unknown",
        "heterozygous",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "visible" in explanation.lower() or "unresolved" in explanation.lower()

def test_inheritance_explanation_not_reduced_to_scalar():
    inheritance=evaluate_inheritance_context(
        "mitochondrial",
        "heteroplasmic",
    )
    explanation=build_inheritance_explanation(inheritance)

    assert "inheritance_support" in explanation
    assert "inheritance_conflict" in explanation
    assert "inheritance_uncertainty" in explanation
