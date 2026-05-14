#!/usr/bin/env python3
"""Validate RDGP configured inputs and write validation reports."""
from __future__ import annotations
from pathlib import Path
import yaml
from rdgp.config import load_config
from rdgp.io import read_tsv
from rdgp.validators import (
    validate_gene_evidence_schema,
    validate_gsc_overlay_schema,
    validate_semantic_state_distinction,
    validation_result_to_dict,
    summarize_validation_results,
)

def write_validation_markdown(summary:dict,path:Path)->Path:
    path.parent.mkdir(parents=True,exist_ok=True)
    lines=["# RDGP Validation Report",""]
    lines.append(f"- overall_passed: {summary['passed']}")
    lines.append(f"- error_count: {summary['error_count']}")
    lines.append(f"- warning_count: {summary['warning_count']}")
    lines.append("")
    for item in summary["results"]:
        lines.append(f"## {item['label']}")
        lines.append("")
        lines.append(f"- passed: {item['passed']}")
        if item["errors"]:
            lines.append("- errors:")
            for err in item["errors"]:
                lines.append(f"  - {err}")
        if item["warnings"]:
            lines.append("- warnings:")
            for warn in item["warnings"]:
                lines.append(f"  - {warn}")
        lines.append("")
    path.write_text("\n".join(lines),encoding="utf-8")
    return path

def write_validation_yaml(summary:dict,path:Path)->Path:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as handle:
        yaml.safe_dump(summary,handle,sort_keys=False)
    return path

def main()->None:
    config=load_config("config/config.yaml")
    run_root=Path(config.output_root)/config.run_id
    report_dir=run_root/"reports"
    gene_df=read_tsv(config.gene_evidence_table)
    results=[
        validation_result_to_dict(validate_gene_evidence_schema(gene_df),"gene_evidence_schema"),
        validation_result_to_dict(validate_semantic_state_distinction(),"semantic_state_distinction"),
    ]
    if config.enable_gsc_overlay and config.gsc_overlay_table:
        gsc_df=read_tsv(config.gsc_overlay_table)
        results.append(validation_result_to_dict(validate_gsc_overlay_schema(gsc_df),"gsc_overlay_schema"))
    summary=summarize_validation_results(results)
    write_validation_markdown(summary,report_dir/"validation_report.md")
    write_validation_yaml(summary,report_dir/"validation_summary.yaml")
    if not summary["passed"]:
        raise SystemExit(1)

if __name__=="__main__":
    main()
