from pathlib import Path
import os
import subprocess
import yaml

def test_validate_inputs_writes_markdown_and_yaml_reports():
    results_root=Path("results/runs")
    before={p.name for p in results_root.iterdir()} if results_root.exists() else set()
    env=os.environ.copy()
    env["PYTHONPATH"]="src"
    completed=subprocess.run(
        ["python","scripts/validate_inputs.py"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert completed.returncode==0
    after={p.name for p in results_root.iterdir()}
    new_runs=sorted(after-before)
    assert new_runs
    report_dir=results_root/new_runs[-1]/"reports"
    md=report_dir/"validation_report.md"
    yml=report_dir/"validation_summary.yaml"
    assert md.exists()
    assert yml.exists()
    text=md.read_text(encoding="utf-8")
    assert "overall_passed: True" in text
    summary=yaml.safe_load(yml.read_text(encoding="utf-8"))
    assert summary["passed"] is True
    assert summary["error_count"]==0

def test_run_pipeline_writes_validation_summary_yaml():
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
    yml=results_root/new_runs[-1]/"reports"/"validation_summary.yaml"
    assert yml.exists()
    summary=yaml.safe_load(yml.read_text(encoding="utf-8"))
    assert summary["passed"] is True
