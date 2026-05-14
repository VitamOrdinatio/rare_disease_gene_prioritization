from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes
from rdgp.confidence import compute_confidence
from rdgp.ranking import rank_genes
from rdgp.explainability import add_explanations

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def _explained_edge_cases():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    confident=compute_confidence(scored)
    ranked=rank_genes(confident)
    return add_explanations(ranked)

def test_explanations_add_required_columns():
    out=_explained_edge_cases()
    assert {"evidence_summary","provenance_summary","evidence_status_summary"}.issubset(out.columns)

def test_evidence_summary_explains_ranking_components():
    out=_explained_edge_cases()
    polg=out[out["gene_symbol"]=="POLG"].iloc[0]
    assert "priority_score=" in polg["evidence_summary"]
    assert "Variant evidence score=" in polg["evidence_summary"]
    assert "GSC overlay status=" in polg["evidence_summary"]
    assert "Confidence tier=" in polg["evidence_summary"]

def test_provenance_summary_preserves_sources():
    out=_explained_edge_cases()
    polg=out[out["gene_symbol"]=="POLG"].iloc[0]
    assert "Variant provenance=" in polg["provenance_summary"]
    assert "Source pipeline=" in polg["provenance_summary"]
    assert "GSC provenance=" in polg["provenance_summary"]

def test_no_gsc_match_remains_visible_in_explanation():
    out=_explained_edge_cases()
    novel=out[out["gene_symbol"]=="NOVEL1"].iloc[0]
    assert "no_gsc_match" in novel["evidence_summary"]
    assert "no_gsc_match" in novel["evidence_status_summary"]
