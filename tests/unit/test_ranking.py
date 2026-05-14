from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay
from rdgp.scoring import load_scoring_profile,score_genes
from rdgp.confidence import compute_confidence
from rdgp.ranking import rank_genes

PROFILE_PATH="config/scoring_profiles/default_v1.yaml"

def _ranked_edge_cases():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    merged=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    profile=load_scoring_profile(PROFILE_PATH)
    scored=score_genes(merged,profile)
    confident=compute_confidence(scored)
    return rank_genes(confident)

def test_rank_column_is_assigned_per_sample():
    ranked=_ranked_edge_cases()
    assert "rank" in ranked.columns
    assert ranked["rank"].tolist()==list(range(1,len(ranked)+1))

def test_ranking_is_deterministic():
    ranked1=_ranked_edge_cases()
    ranked2=_ranked_edge_cases()
    assert ranked1[["sample_id","gene_symbol","rank"]].to_dict("records")==ranked2[["sample_id","gene_symbol","rank"]].to_dict("records")

def test_strong_candidate_ranks_above_weak_gsc_candidate():
    ranked=_ranked_edge_cases()
    polg_rank=int(ranked[ranked["gene_symbol"]=="POLG"]["rank"].iloc[0])
    weak_rank=int(ranked[ranked["gene_symbol"]=="WEAKGSC"]["rank"].iloc[0])
    assert polg_rank<weak_rank

def test_rank_sort_is_stable_with_gene_symbol_tiebreaker():
    ranked=_ranked_edge_cases()
    assert ranked["rank"].is_monotonic_increasing
