"""Configuration loading for RDGP."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import datetime as dt
import yaml

@dataclass(frozen=True)
class RDGPConfig:
    config_path: Path
    run_id: str
    strict_mode: bool
    gene_evidence_table: Path
    gsc_overlay_table: Path | None
    functional_evidence_table: Path | None
    selected_phenotype: str | None
    enable_gsc_overlay: bool
    enable_functional_evidence: bool
    scoring_profile: str
    validation_profile: str
    output_root: Path

def _require_section(data:dict[str,Any],section:str)->dict[str,Any]:
    if section not in data or not isinstance(data[section],dict):
        raise ValueError(f"Missing required config section: {section}")
    return data[section]

def _resolve_optional_path(value:Any,base:Path)->Path|None:
    if value is None:
        return None
    if isinstance(value,str) and value.strip().lower() in {"","null","none"}:
        return None
    path=Path(str(value))
    return path if path.is_absolute() else base/path

def _make_run_id()->str:
    return "run_"+dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def load_config(config_path:str|Path)->RDGPConfig:
    config_path=Path(config_path)
    base=config_path.parent.parent if config_path.parent.name=="config" else Path.cwd()
    with config_path.open("r",encoding="utf-8") as handle:
        data=yaml.safe_load(handle) or {}
    run=_require_section(data,"run")
    inputs=_require_section(data,"inputs")
    analysis=_require_section(data,"analysis")
    scoring=_require_section(data,"scoring")
    validation=_require_section(data,"validation")
    outputs=_require_section(data,"outputs")
    run_id=str(run.get("run_id","auto"))
    if run_id=="auto":
        run_id=_make_run_id()
    enable_gsc=bool(analysis.get("enable_gsc_overlay",False))
    selected_phenotype=analysis.get("selected_phenotype")
    if enable_gsc and not selected_phenotype:
        raise ValueError("analysis.selected_phenotype is required when enable_gsc_overlay=true")
    gene_evidence=_resolve_optional_path(inputs.get("gene_evidence_table"),base)
    if gene_evidence is None:
        raise ValueError("inputs.gene_evidence_table is required")
    return RDGPConfig(
        config_path=config_path,
        run_id=run_id,
        strict_mode=bool(run.get("strict_mode",True)),
        gene_evidence_table=gene_evidence,
        gsc_overlay_table=_resolve_optional_path(inputs.get("gsc_overlay_table"),base),
        functional_evidence_table=_resolve_optional_path(inputs.get("functional_evidence_table"),base),
        selected_phenotype=str(selected_phenotype) if selected_phenotype is not None else None,
        enable_gsc_overlay=enable_gsc,
        enable_functional_evidence=bool(analysis.get("enable_functional_evidence",False)),
        scoring_profile=str(scoring.get("profile","default_v1")),
        validation_profile=str(validation.get("profile","default_v1")),
        output_root=_resolve_optional_path(outputs.get("output_root","results/runs"),base) or base/"results/runs",
    )
