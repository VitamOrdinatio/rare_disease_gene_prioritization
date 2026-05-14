from rdgp.evidence import build_evidence_item, validate_evidence_item

def test_evidence_context_axes_remain_decomposed():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"mechanistic",
        "evidence_direction":"supportive",
        "evidence_scope":"sample_specific",
        "evidence_status":"present",
        "mechanism_context":"loss_of_function",
        "tissue_context":"CNS",
        "temporal_context":"developmental",
        "confidence_context":"moderate_confidence",
        "uncertainty_context":"unresolved",
        "provenance_id":"prov1",
    })

    assert item["mechanism_context"]!="unknown"
    assert item["tissue_context"]!="unknown"
    assert item["temporal_context"]!="unknown"
    assert item["mechanism_context"]!=item["confidence_context"]

def test_direction_not_collapsed_into_confidence_or_score():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"phenotype",
        "evidence_direction":"contradictory",
        "evidence_scope":"phenotype_specific",
        "evidence_status":"conflicting",
        "confidence_context":"limited_confidence",
        "uncertainty_context":"conflicting",
        "provenance_id":"prov1",
    })

    assert item["evidence_direction"]=="contradictory"
    assert item["confidence_context"]=="limited_confidence"
    assert "priority_score" not in item

def test_missing_required_identity_is_reported():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "evidence_category":"variant",
        "evidence_direction":"supportive",
        "evidence_status":"present",
        "confidence_context":"moderate_confidence",
        "uncertainty_context":"unresolved",
        "provenance_id":"prov1",
    })

    errors=validate_evidence_item(item)
    assert "missing_required_evidence_field:gene_id" in errors

def test_evidence_item_does_not_require_probabilistic_fields():
    item=build_evidence_item({
        "evidence_id":"ev1",
        "gene_id":"GENE1",
        "evidence_category":"mechanistic",
        "evidence_direction":"context_modifying",
        "evidence_scope":"sample_specific",
        "evidence_status":"present",
        "confidence_context":"moderate_confidence",
        "uncertainty_context":"unresolved",
        "provenance_id":"prov1",
    })

    assert validate_evidence_item(item)==[]
    assert "posterior_probability" not in item
