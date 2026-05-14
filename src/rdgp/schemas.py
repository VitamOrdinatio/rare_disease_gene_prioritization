"""Schema constants and semantic states for RDGP v1."""
GENE_EVIDENCE_REQUIRED_COLUMNS=[
"sample_id","gene_id","gene_symbol","variant_count","rare_variant_count","high_impact_variant_count","pathogenic_variant_count","likely_pathogenic_variant_count","vus_variant_count","likely_benign_variant_count","benign_variant_count","max_variant_severity","quality_summary","variant_provenance_summary","gene_mapping_status","source_pipeline","run_id"]
GSC_OVERLAY_REQUIRED_COLUMNS=[
"phenotype","gene_id","gene_symbol","consensus_score","semantic_consensus_score","source_count","weighted_source_sum","semantic_channel_summary","source_list","active_score","scoring_profile","gsc_version","release_id","run_id","provenance_id"]
NULL_STATES={"missing","unknown","not_evaluated","unsupported","unresolved","ambiguous","conflicting","contradictory","low_quality","zero_observed"}
GENE_MAPPING_STATUSES={"stable","fallback","ambiguous","missing","unresolved"}
GSC_OVERLAY_STATUSES={"matched_gene_id","matched_gene_symbol","no_gsc_match","ambiguous_gene_mapping","unsupported_phenotype_context"}
CONFIDENCE_TIERS={"high","moderate","limited","low","unresolved"}

PRIORITIZED_GENES_COLUMNS=[
"sample_id","gene_id","gene_symbol","selected_phenotype","rank","priority_score",
"confidence_tier","confidence_state","confidence_explanation","confidence_flags",
"variant_evidence_score","gsc_prior_score","functional_evidence_score",
"uncertainty_state","evidence_status_summary","quality_flag","gsc_overlay_status",
"gene_mapping_status","evidence_summary","provenance_summary","run_id"]
