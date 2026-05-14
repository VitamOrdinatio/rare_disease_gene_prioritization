from pathlib import Path
import pytest
from rdgp.config import load_config

def test_load_default_config():
    cfg=load_config("config/config.yaml")
    assert cfg.strict_mode is True
    assert cfg.enable_gsc_overlay is True
    assert cfg.selected_phenotype=="mitochondrial_disease"
    assert cfg.scoring_profile=="default_v1"
    assert cfg.validation_profile=="default_v1"
    assert cfg.gene_evidence_table.exists()
    assert cfg.gsc_overlay_table is not None
    assert cfg.gsc_overlay_table.exists()

def test_gsc_requires_selected_phenotype(tmp_path):
    config=tmp_path/"config.yaml"
    config.write_text(
        "run:\n  run_id: test\n  strict_mode: true\n"
        "inputs:\n  gene_evidence_table: tests/fixtures/gene_evidence_minimal.tsv\n  gsc_overlay_table: tests/fixtures/gsc_overlay_minimal.tsv\n  functional_evidence_table: null\n"
        "analysis:\n  selected_phenotype: null\n  enable_gsc_overlay: true\n  enable_functional_evidence: false\n"
        "scoring:\n  profile: default_v1\n"
        "validation:\n  profile: default_v1\n"
        "outputs:\n  output_root: results/runs\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError,match="selected_phenotype"):
        load_config(config)
