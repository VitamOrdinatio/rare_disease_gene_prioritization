from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def test_scoring_produces_required_score_fields():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    required={
        "variant_anchor_score",
        "variant_support_score",
        "variant_evidence_score",
        "gsc_prior_score",
        "functional_evidence_score",
        "priority_score",
    }
    assert required.issubset(scored.columns)

def test_lof_candidate_scores_higher_than_missense_candidate():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    polg=float(scored[scored["gene_symbol"]=="POLG"]["priority_score"].iloc[0])
    mtnd2=float(scored[scored["gene_symbol"]=="MT-ND2"]["priority_score"].iloc[0])
    assert polg>mtnd2

def test_missing_functional_evidence_is_not_penalized():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    assert set(scored["functional_evidence_score"])=={"not_evaluated"}

def test_gsc_only_support_is_bounded():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    gsc_only=scored[scored["gene_symbol"]=="WEAKGSC"].iloc[0]
    assert float(gsc_only["gsc_prior_score"])<=4.0
