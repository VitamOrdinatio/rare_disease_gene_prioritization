from pathlib import Path
import os
import subprocess
import pandas as pd

def test_pipeline_gene_evidence_matrix_contains_inheritance_fields():
    results_root=Path("results/runs")
    before={p.name for p in results_root.iterdir()} if results_root.exists() else set()
    env=os.environ.copy()
    env["PYTHONPATH"]="src"

    subprocess.run(
        ["python","scripts/run_pipeline.py"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    after={p.name for p in results_root.iterdir()}
    new_runs=sorted(after-before)
    assert new_runs

    matrix=results_root/new_runs[-1]/"tables"/"gene_evidence_matrix.tsv"
    df=pd.read_csv(matrix,sep="\t",dtype=str,keep_default_na=False)

    required={
        "inheritance_mode",
        "zygosity_context",
        "inheritance_support",
        "inheritance_conflict",
        "inheritance_explanation",
        "inheritance_uncertainty",
    }

    assert required.issubset(df.columns)

def test_prioritized_genes_schema_remains_stable_without_promoting_inheritance():
    results_root=Path("results/runs")
    before={p.name for p in results_root.iterdir()} if results_root.exists() else set()
    env=os.environ.copy()
    env["PYTHONPATH"]="src"

    subprocess.run(
        ["python","scripts/run_pipeline.py"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    after={p.name for p in results_root.iterdir()}
    new_runs=sorted(after-before)
    assert new_runs

    prioritized=results_root/new_runs[-1]/"tables"/"prioritized_genes.tsv"
    df=pd.read_csv(prioritized,sep="\t",dtype=str,keep_default_na=False)

    assert "inheritance_support" not in df.columns
    assert "inheritance_explanation" not in df.columns
