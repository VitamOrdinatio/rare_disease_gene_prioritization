from rdgp.mechanism import (
    normalize_mechanism_context,
    evaluate_mechanism_context,
)

def test_normalize_mechanism_context():
    assert normalize_mechanism_context("LOSS_OF_FUNCTION")=="loss_of_function"

def test_unknown_mechanism_context():
    assert normalize_mechanism_context("weird_context")=="unresolved"

def test_lof_mechanism_support():
    result=evaluate_mechanism_context("loss_of_function")

    assert result["mechanism_support"]=="compatible"
    assert "loss-of-function" in result["mechanism_explanation"].lower()

def test_unknown_mechanism_remains_unresolved():
    result=evaluate_mechanism_context("unknown")

    assert result["mechanism_support"]=="contextual"
    assert "unresolved" in result["mechanism_explanation"].lower()
