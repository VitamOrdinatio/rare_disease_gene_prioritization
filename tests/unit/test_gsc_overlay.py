import pandas as pd
import pytest
from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay

def test_attach_gsc_overlay_matches_by_gene_id():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    out=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    assert len(out)==len(gene_df)
    assert set(out["gsc_overlay_status"])=={"matched_gene_id"}
    polg=out[out["gene_symbol"]=="POLG"].iloc[0]
    assert polg["gsc_semantic_consensus_score"]=="0.88"
    assert polg["selected_phenotype"]=="mitochondrial_disease"

def test_attach_gsc_overlay_requires_selected_phenotype():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    with pytest.raises(ValueError,match="selected_phenotype"):
        attach_gsc_overlay(gene_df,gsc_df,None)

def test_unsupported_phenotype_context_is_explicit():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    out=attach_gsc_overlay(gene_df,gsc_df,"unsupported_phenotype")
    assert set(out["gsc_overlay_status"])=={"unsupported_phenotype_context"}

def test_duplicate_gsc_gene_id_fails_before_join():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    duplicated=pd.concat([gsc_df,gsc_df.iloc[[0]]],ignore_index=True)
    with pytest.raises(ValueError,match="duplicate gene_id"):
        attach_gsc_overlay(gene_df,duplicated,"mitochondrial_disease")
