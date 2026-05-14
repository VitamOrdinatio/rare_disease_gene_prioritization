from pathlib import Path
import os
import subprocess
import yaml

def test_run_manifest_records_inheritance_reasoning():
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

    manifest_path=results_root/new_runs[-1]/"run_manifest.yaml"

    manifest=yaml.safe_load(manifest_path.read_text())

    assert manifest["reasoning_layers"]["inheritance_reasoning_enabled"] is True
