import pandas as pd
from pathlib import Path
from rdgp.validators import validate_gene_evidence_schema,validate_gsc_overlay_schema,validate_semantic_state_distinction

FIXTURES=Path("tests/fixtures")

def test_gene_evidence_minimal_schema_passes():
    df=pd.read_csv(FIXTURES/"gene_evidence_minimal.tsv",sep="\t",keep_default_na=False)
    result=validate_gene_evidence_schema(df)
    assert result.passed,result.errors

def test_gsc_overlay_minimal_schema_passes():
    df=pd.read_csv(FIXTURES/"gsc_overlay_minimal.tsv",sep="\t",keep_default_na=False)
    result=validate_gsc_overlay_schema(df)
    assert result.passed,result.errors

def test_gene_evidence_edge_case_schema_passes_with_explicit_statuses():
    df=pd.read_csv(FIXTURES/"gene_evidence_edge_cases.tsv",sep="\t",keep_default_na=False)
    result=validate_gene_evidence_schema(df)
    assert result.passed,result.errors

def test_semantic_state_distinctions_do_not_collapse():
    result=validate_semantic_state_distinction()
    assert result.passed,result.errors
