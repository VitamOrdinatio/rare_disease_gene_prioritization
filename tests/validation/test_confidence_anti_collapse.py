from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes
from rdgp.confidence import compute_confidence

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def _confidence_edge_cases():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    return compute_confidence(scored)

def test_high_score_can_coexist_with_reduced_confidence():
    out=_confidence_edge_cases()
    lowqc=out[out["gene_symbol"]=="LOWQC1"].iloc[0]
    assert float(lowqc["priority_score"])>0
    assert lowqc["confidence_tier"]=="low"

def test_no_gsc_match_does_not_create_low_confidence_by_default():
    out=_confidence_edge_cases()
    novel=out[out["gene_symbol"]=="NOVEL1"].iloc[0]
    assert novel["gsc_overlay_status"]=="no_gsc_match"
    assert novel["confidence_tier"] in {"moderate","limited"}
    assert novel["confidence_tier"]!="low"
    assert "not contradiction" in novel["confidence_explanation"]

def test_missing_functional_evidence_is_completeness_context_not_penalty():
    out=_confidence_edge_cases()
    assert "functional_not_evaluated" in set(";".join(out["confidence_flags"]).split(";"))
    for _,row in out.iterrows():
        assert row["functional_evidence_score"]=="not_evaluated"

def test_confidence_does_not_overwrite_priority_score():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    before=scored["priority_score"].tolist()
    out=compute_confidence(scored)
    after=out["priority_score"].tolist()
    assert before==after

def test_confidence_explanations_are_reconstructable():
    out=_confidence_edge_cases()
    assert out["confidence_explanation"].str.len().min()>20
    assert out["confidence_state"].str.len().min()>0
