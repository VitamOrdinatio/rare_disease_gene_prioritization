from rdgp.inheritance import evaluate_inheritance_context

def test_inheritance_conflict_does_not_become_exclusion():
    result=evaluate_inheritance_context("autosomal_recessive","heterozygous")
    assert result["inheritance_conflict"]=="possible"
    assert result["inheritance_support"]!="excluded"

def test_unknown_zygosity_remains_visible():
    result=evaluate_inheritance_context("autosomal_dominant","unknown")
    assert result["inheritance_uncertainty"]=="visible"

def test_mitochondrial_context_not_collapsed_into_mendelian_logic():
    result=evaluate_inheritance_context("mitochondrial","heteroplasmic")
    assert "mitochondrial" in result["inheritance_explanation"].lower()

def test_unresolved_inheritance_remains_explicit():
    result=evaluate_inheritance_context("unresolved","heterozygous")
    assert result["inheritance_support"]=="unresolved"
