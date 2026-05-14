from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def test_no_gsc_match_is_not_negative_evidence():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    novel=scored[scored["gene_symbol"]=="NOVEL1"].iloc[0]
    assert novel["gsc_overlay_status"]=="no_gsc_match"
    assert float(novel["gsc_prior_score"])==0.0
    assert float(novel["priority_score"])>0.0

def test_gsc_only_support_does_not_dominate_priority_score():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    weak=scored[scored["gene_symbol"]=="WEAKGSC"]["priority_score"].iloc[0]
    polg=scored[scored["gene_symbol"]=="POLG"]["priority_score"].iloc[0]
    assert float(polg)>float(weak)

def test_repeated_weak_support_is_bounded():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    weak=scored[scored["gene_symbol"]=="WEAKGSC"].iloc[0]
    assert float(weak["variant_support_score"])<=6.0

def test_priority_score_remains_inspectable():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    row=scored.iloc[0]
    reconstructed=(
        float(row["variant_evidence_score"])+
        float(row["gsc_prior_score"])
    )
    assert abs(reconstructed-float(row["priority_score"]))<0.0001
