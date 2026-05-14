import pandas as pd
from pathlib import Path
from rdgp.io import read_tsv,write_tsv

def test_read_tsv_preserves_explicit_missing_string():
    df=read_tsv("tests/fixtures/gene_evidence_edge_cases.tsv")
    row=df[df["gene_symbol"]=="MISSING1"].iloc[0]
    assert row["variant_count"]=="missing"
    assert row["quality_summary"]=="not_evaluated"

def test_write_tsv_roundtrip_preserves_strings(tmp_path):
    df=pd.DataFrame({"state":["missing","zero_observed","not_evaluated"],"value":["","0","unknown"]})
    path=tmp_path/"roundtrip.tsv"
    write_tsv(df,path)
    loaded=read_tsv(path)
    assert loaded["state"].tolist()==["missing","zero_observed","not_evaluated"]
    assert loaded["value"].tolist()==["","0","unknown"]
