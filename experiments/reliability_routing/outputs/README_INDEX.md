# Outputs Index

Last updated: 2026-07-01.

This index groups result folders by purpose. Experiment directories are not moved after creation unless they are clearly one-off reports; this keeps command histories and cached paths reproducible.

## Current Main Results

### Roman-Empire Main Line

- `phaseC_rw8_dim32_confirm_r10`
  - Current strongest Roman configuration.
  - `component_concat`, `component_dim=32`, `rw_steps=8`, `alpha_type=channel`.
- `phaseB_alpha_channel_confirm_r10`
  - Channel-wise alpha confirmation.
- `phaseB_alpha_group8_confirm_r10`
  - Lightweight/interpretable group-wise alpha confirmation.
- `evidence_matrix`
  - Current evidence map, including GraphGPS local comparison where available.

### Arxiv-Year Second Positive Candidate

- `new_candidate_arxiv_year_directed_prescreen_v1`
  - Preference/headroom prescreen for source-to-target directed Arxiv-year.
- `new_candidate_prescreen_v1`
  - Mixed new-candidate prescreen; includes Arxiv-year undirected and WikiCS.
- `arxiv_year_directed_component_concat_screen_r3`
  - 3-run representation-control screen, source-to-target.
- `arxiv_year_undirected_component_concat_screen_r3`
  - 3-run representation-control screen, undirected.
- `arxiv_year_directed_component_concat_confirm_r10`
  - Main Arxiv-year confirmation.
  - Strongest second mechanism-positive result.
- `arxiv_year_undirected_component_concat_confirm_r10`
  - Directed-sensitivity counterpart; positive but weaker than directed.

### New Candidate Screens

- `new_candidate_genius_prescreen_v1`
  - Genius has large oracle headroom but weak current reliability separability.
- `new_candidate_prescreen_drycheck`
  - Wrapper dry-check; not a scientific result.
- `lrgb_pascalvocsp_screen_v3`
  - Incomplete PascalVOC-SP smoke/screening run.
  - Only seed 0 is complete for all controls; seed 1 contains fixed only.

## Diagnostics

- `unified_diagnostics_v1`
  - Cross-dataset diagnostic table.
- `second_positive_prescreen_v1`
  - Prescreen rule calibration / earlier candidate pass.
- `webkb_best_config_screen`
  - WebKB negative-family screen.
- `expert_headroom_diagnosis_v1`
  - Local/global headroom diagnosis.
- `control_alignment_diagnosis_v2`
  - Alpha/control alignment diagnosis.
- `node_mechanism_diagnosis`
- `node_mechanism_diagnosis_with_alignment`
- `mechanism_diagnosis`
- `mechanism_diagnosis_smoke`
- `mechanism_diagnosis_smoke_v2`

## Representation-Control Development History

### Early Representation Control

- `representation_control_screen_v3`
- `representation_control_confirm_s010_r10`
- `representation_control_strength_0.05`
- `representation_control_strength_0.10`
- `representation_control_strength_0.20`
- `_reports/legacy_strength_sweep`
  - Moved top-level strength-sweep CSV exports.

### Iterative Relation

- `iterative_relation_k1_screen`
- `iterative_relation_k2_screen`
- `iterative_relation_k3_screen`
- `iterative_relation_binary_k1_screen`
- `iterative_relation_binary_shared_backbone`
- `iter_relation_mechanism_v1`
  - Large active mechanism diagnostics folder with tensor payloads.
- `iter_relation_causal_v2`
  - Causal intervention/control experiment outputs.

### Phase A: Reliability Encoder

- `phaseA_raw_concat_screen`
- `phaseA_component_aligned_screen`
- `phaseA2_raw_concat_screen`
- `phaseA2_component_concat_screen`
- `phaseA_shared_cache`
- `phaseA2_shared_cache`

### Phase B: Alpha Type

- `phaseB_alpha_channel_screen`
- `phaseB_alpha_group4_screen`
- `phaseB_alpha_node_screen`
- `phaseB_alpha_group8_screen`
- `phaseB_alpha_channel_confirm_r10`
- `phaseB_alpha_group4_confirm_r10`
- `phaseB_alpha_group8_confirm_r10`
- `phaseB_alpha_shared_cache`

### Phase C: RWSE and Component Dim

- `phaseC_component_dim8_screen`
- `phaseC_component_dim16_screen`
- `phaseC_component_dim32_screen`
- `phaseC_component_dim32_confirm_r10`
- `phaseC_rw8_dim16_screen`
- `phaseC_rw16_dim16_screen`
- `phaseC_rw8_dim32_screen`
- `phaseC_rw16_dim32_screen`
- `phaseC_rw8_dim32_confirm_r10`
- `phaseC_component_dim_shared_cache`
- `phaseC0_existing_datasets_channel_screen`
- `phaseC0_existing_datasets_group8_screen`
- `phaseC0_existing_datasets_shared_cache`
- `phaseC1_questions_bestparams_channel_r10`
- `phaseC1_squirrel_bestparams_channel_r10`

## Routing and Expert Fusion History

- `expert_fusion_gate_init_sanity`
- `expert_validation_sanity`
- `expert_validation_full`
- `real_gcn_diagnostic`
- `preference_routing_sanity_v2`
- `preference_routing_full_v3`
- `utility_routing_sanity_v2`
- `utility_routing_full_v3`
- `expert_validation_sanity`
- `expert_validation_full`

## Reports and Validation Files

- `_reports/dataset_validation`
  - One-off validation JSON files.
  - Includes new-candidate validation for Genius, Arxiv-year, WikiCS, LINKX Wiki missing checks, and LRGB staging checks.
- `_reports/legacy_strength_sweep`
  - Older top-level strength sweep summary CSV files.

## Historical Archive

- `archive`
- `archive_manifest.csv`

These preserve early synthetic and first real-data experiments. They are useful for provenance, not for the latest conclusions.

## Top-Level Files

- `README.md`
  - Human-oriented overview and current conclusions.
- `README_INDEX.md`
  - This categorized folder index.
- `experiment_index.csv`
  - Older machine-readable index; may not include the latest folders.
- `archive_manifest.csv`
  - Manifest for `archive/`.

## Current Interpretation Snapshot

- Roman-empire remains the strongest performance and mechanism-positive dataset.
- Arxiv-year directed is now a confirmed second mechanism-positive dataset.
- Arxiv-year undirected is also positive but weaker.
- WikiCS and Genius have headroom but do not currently show reliable handcrafted-reliability separability.
- PascalVOC-SP is incomplete and should not be used as a formal result.
