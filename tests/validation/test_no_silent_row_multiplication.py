import pandas as pd
import pytest
from rdgp.io import read_tsv
from rdgp.gsc_overlay import attach_gsc_overlay

def test_gsc_overlay_preserves_row_count_for_edge_cases():
    gene_df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_edge_cases.tsv")
    out=attach_gsc_overlay(gene_df,gsc_df,"mitochondrial_disease")
    assert len(out)==len(gene_df)

def test_duplicate_gsc_rows_do_not_silently_multiply_gene_rows():
    gene_df=read_tsv("tests/fixtures/gene_evidence_minimal.tsv")
    gsc_df=read_tsv("tests/fixtures/gsc_overlay_minimal.tsv")
    duplicated=pd.concat([gsc_df,gsc_df.iloc[[0]]],ignore_index=True)
    with pytest.raises(ValueError,match="row multiplication"):
        attach_gsc_overlay(gene_df,duplicated,"mitochondrial_disease")
