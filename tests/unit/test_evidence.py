from rdgp.evidence import (
    build_evidence_item,
    normalize_evidence_direction,
    normalize_evidence_status,
    summarize_evidence_item,
    validate_evidence_item,
)

def test_normalize_evidence_direction():
    assert normalize_evidence_direction("Reliability Reducing")=="reliability_reducing"
    assert normalize_evidence_direction("bad")=="unresolved"

def test_normalize_evidence_status():
    assert normalize_evidence_status("not-evaluated")=="not_evaluated"
    assert normalize_evidence_status("bad")=="unresolved"

def test_build_evidence_item_preserves_context_fields():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"mechanistic",
        "evidence_direction":"supportive",
        "evidence_scope":"sample-specific",
        "mechanism_context":"loss_of_function",
        "temporal_context":"developmental",
        "provenance_id":"prov1",
    })

    assert item["mechanism_context"]=="loss_of_function"
    assert item["temporal_context"]=="developmental"
    assert item["evidence_direction"]=="supportive"

def test_validate_complete_evidence_item():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"variant",
        "evidence_direction":"supportive",
        "evidence_scope":"sample_specific",
        "evidence_status":"present",
        "confidence_context":"moderate_confidence",
        "uncertainty_context":"unresolved",
        "provenance_id":"prov1",
    })

    assert validate_evidence_item(item)==[]

def test_summarize_evidence_item():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"inheritance",
        "evidence_direction":"context_modifying",
        "evidence_status":"present",
        "evidence_scope":"sample_specific",
        "provenance_id":"prov1",
    })

    summary=summarize_evidence_item(item)
    assert "inheritance evidence" in summary
    assert "GENE1" in summary
    assert "context_modifying" in summary
