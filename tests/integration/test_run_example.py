from pathlib import Path
import os
import subprocess
import pandas as pd

def test_run_pipeline_end_to_end():
    results_root=Path("results/runs")
    logs_root=Path("logs")
    before_results={p.name for p in results_root.iterdir()} if results_root.exists() else set()
    before_logs={p.name for p in logs_root.iterdir()} if logs_root.exists() else set()
    env=os.environ.copy()
    env["PYTHONPATH"]="src"
    completed=subprocess.run(
        ["python","scripts/run_pipeline.py"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert completed.returncode==0
    after_results={p.name for p in results_root.iterdir()}
    new_runs=sorted(after_results-before_results)
    assert new_runs
    run_dir=results_root/new_runs[-1]
    prioritized=run_dir/"tables"/"prioritized_genes.tsv"
    manifest=run_dir/"run_manifest.yaml"
    validation=run_dir/"reports"/"validation_report.md"
    assert prioritized.exists()
    assert manifest.exists()
    assert validation.exists()
    df=pd.read_csv(prioritized,sep="\t",dtype=str,keep_default_na=False)
    required_columns={
        "sample_id",
        "gene_symbol",
        "priority_score",
        "confidence_tier",
        "rank",
        "evidence_summary",
        "provenance_summary",
    }
    assert required_columns.issubset(df.columns)
    after_logs={p.name for p in logs_root.iterdir()}
    new_logs=sorted(after_logs-before_logs)
    assert new_logs
    log_dir=logs_root/new_logs[-1]
    log_file=log_dir/"pipeline.log"
    assert log_file.exists()
