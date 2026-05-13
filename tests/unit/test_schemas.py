from rdgp.schemas import GENE_EVIDENCE_REQUIRED_COLUMNS,GSC_OVERLAY_REQUIRED_COLUMNS,NULL_STATES,GENE_MAPPING_STATUSES,CONFIDENCE_TIERS

def test_gene_evidence_schema_contains_identity_fields():
    assert "sample_id" in GENE_EVIDENCE_REQUIRED_COLUMNS
    assert "gene_id" in GENE_EVIDENCE_REQUIRED_COLUMNS
    assert "gene_symbol" in GENE_EVIDENCE_REQUIRED_COLUMNS

def test_gsc_overlay_schema_contains_phenotype_fields():
    assert "phenotype" in GSC_OVERLAY_REQUIRED_COLUMNS
    assert "gene_id" in GSC_OVERLAY_REQUIRED_COLUMNS
    assert "consensus_score" in GSC_OVERLAY_REQUIRED_COLUMNS

def test_semantic_states_preserve_anti_collapse_terms():
    assert {"missing","zero_observed","unsupported","contradictory","unresolved","low_quality"}.issubset(NULL_STATES)

def test_gene_mapping_statuses_allow_controlled_fallback():
    assert {"stable","fallback","ambiguous","missing","unresolved"}.issubset(GENE_MAPPING_STATUSES)

def test_confidence_tiers_are_qualitative_first():
    assert {"high","moderate","limited","low","unresolved"}.issubset(CONFIDENCE_TIERS)
