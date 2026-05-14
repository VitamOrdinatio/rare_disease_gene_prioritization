from rdgp.inheritance import (
    normalize_inheritance_mode,
    normalize_zygosity_context,
    evaluate_inheritance_context,
)

def test_normalize_inheritance_mode():
    assert normalize_inheritance_mode("AUTOSOMAL_DOMINANT")=="autosomal_dominant"
    assert normalize_inheritance_mode("weird_mode")=="unresolved"

def test_normalize_zygosity_context():
    assert normalize_zygosity_context("HOMOZYGOUS")=="homozygous"
    assert normalize_zygosity_context("bad_value")=="unknown"

def test_recessive_homozygous_support():
    result=evaluate_inheritance_context("autosomal_recessive","homozygous")
    assert result["inheritance_support"]=="compatible"
    assert result["inheritance_conflict"]=="none"

def test_recessive_heterozygous_partial():
    result=evaluate_inheritance_context("autosomal_recessive","heterozygous")
    assert result["inheritance_support"]=="partial"
    assert result["inheritance_conflict"]=="possible"

def test_dominant_heterozygous_support():
    result=evaluate_inheritance_context("autosomal_dominant","heterozygous")
    assert result["inheritance_support"]=="compatible"

def test_mitochondrial_heteroplasmic_support():
    result=evaluate_inheritance_context("mitochondrial","heteroplasmic")
    assert result["inheritance_support"]=="compatible"

def test_unknown_inheritance_remains_unresolved():
    result=evaluate_inheritance_context("unknown","heterozygous")
    assert result["inheritance_support"]=="unresolved"
