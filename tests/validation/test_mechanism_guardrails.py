from rdgp.mechanism import evaluate_mechanism_context

def test_mechanism_not_collapsed_into_score():
    result=evaluate_mechanism_context("loss_of_function")

    assert "mechanism_support" in result
    assert "mechanism_conflict" in result

def test_mechanism_unknown_remains_visible():
    result=evaluate_mechanism_context("unknown")

    assert "unresolved" in result["mechanism_explanation"].lower()

def test_mechanism_not_diagnostic():
    result=evaluate_mechanism_context("dominant_negative")

    assert result["mechanism_support"]=="contextual"
