"""Run manifest helpers for RDGP v1."""
from __future__ import annotations
from pathlib import Path
import datetime as dt
import platform
import yaml

def build_manifest(config)->dict:
    return {
        "rdgp_version":"v1_pre_release",
        "generated_at":dt.datetime.now().isoformat(),
        "run_id":config.run_id,
        "selected_phenotype":config.selected_phenotype,
        "strict_mode":config.strict_mode,
        "inputs":{
            "gene_evidence_table":str(config.gene_evidence_table),
            "gsc_overlay_table":str(config.gsc_overlay_table) if config.gsc_overlay_table else None,
            "functional_evidence_table":str(config.functional_evidence_table) if config.functional_evidence_table else None,
        },
        "profiles":{
            "scoring_profile":config.scoring_profile,
            "validation_profile":config.validation_profile,
        },
        "reasoning_layers":{
            "inheritance_reasoning_enabled":True,
        },
        "environment":{
            "python_platform":platform.platform(),
            "python_version":platform.python_version(),
        },
    }

def write_manifest(manifest:dict,path:str|Path)->Path:
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as handle:
        yaml.safe_dump(manifest,handle,sort_keys=False)
    return path
