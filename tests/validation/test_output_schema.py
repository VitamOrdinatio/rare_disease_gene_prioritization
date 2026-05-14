from pathlib import Path
import os
import subprocess
import pandas as pd
from rdgp.schemas import PRIORITIZED_GENES_COLUMNS

def test_prioritized_genes_output_schema_and_order():
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

    df=pd.read_csv(
        prioritized,
        sep="\t",
        dtype=str,
        keep_default_na=False,
    )

    assert list(df.columns)==PRIORITIZED_GENES_COLUMNS

def test_gene_evidence_matrix_contains_primary_schema_columns():
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

    df=pd.read_csv(
        matrix,
        sep="\t",
        dtype=str,
        keep_default_na=False,
    )

    assert set(PRIORITIZED_GENES_COLUMNS).issubset(df.columns)
