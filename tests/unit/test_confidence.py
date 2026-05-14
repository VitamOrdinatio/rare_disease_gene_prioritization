from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes
from rdgp.confidence import compute_confidence

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def _scored_edge_cases():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    return score_genes(merged,profile)

def test_confidence_adds_required_fields():
    out=compute_confidence(_scored_edge_cases())
    required={
        "confidence_tier",
        "confidence_state",
        "confidence_sources",
        "confidence_modifiers",
        "confidence_flags",
        "confidence_explanation",
        "confidence_completeness",
        "confidence_limitations",
    }
    assert required.issubset(out.columns)

def test_strong_variant_and_gsc_support_can_be_high_confidence():
    out=compute_confidence(_scored_edge_cases())
    polg=out[out["gene_symbol"]=="POLG"].iloc[0]
    assert polg["confidence_tier"]=="high"
    assert "strong_variant_evidence" in polg["confidence_sources"]
    assert "phenotype_scoped_gsc_support" in polg["confidence_sources"]

def test_ambiguous_mapping_is_unresolved_confidence():
    out=compute_confidence(_scored_edge_cases())
    ambig=out[out["gene_symbol"]=="AMBIG1"].iloc[0]
    assert ambig["confidence_tier"]=="unresolved"
    assert "mapping_limited" in ambig["confidence_flags"]

def test_low_quality_evidence_reduces_confidence_not_score_directly():
    scored=_scored_edge_cases()
    before=scored[scored["gene_symbol"]=="LOWQC1"]["priority_score"].iloc[0]
    out=compute_confidence(scored)
    after=out[out["gene_symbol"]=="LOWQC1"]["priority_score"].iloc[0]
    lowqc=out[out["gene_symbol"]=="LOWQC1"].iloc[0]
    assert before==after
    assert lowqc["confidence_tier"]=="low"
    assert "quality_limited" in lowqc["confidence_flags"]
