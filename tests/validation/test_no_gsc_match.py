from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay

def test_no_gsc_match_is_not_contradictory():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    out=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    novel=out[out["gene_symbol"]=="NOVEL1"].iloc[0]
    assert novel["gsc_overlay_status"]=="no_gsc_match"
    assert novel["gsc_overlay_status"]!="contradictory"
    assert novel["gsc_consensus_score"]==""

def test_ambiguous_gene_mapping_is_not_no_match():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    out=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    ambig=out[out["gene_symbol"]=="AMBIG1"].iloc[0]
    assert ambig["gsc_overlay_status"]=="ambiguous_gene_mapping"
    assert ambig["gsc_overlay_status"]!="no_gsc_match"
