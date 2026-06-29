# Outputs Index

This directory stores experiment outputs for `experiments/reliability_routing`.

## Active Folder

- Keep as-is: `iter_relation_mechanism_v1`
  - Current active mechanism run with node-level diagnostics.
  - Large on disk because it stores per-run tensor payloads.

## Category Index

### Expert Validation

- `expert_fusion_gate_init_sanity`
- `expert_validation_sanity`
- `expert_validation_full`
- `real_gcn_diagnostic`

### Routing and Preference

- `preference_routing_sanity_v2`
- `preference_routing_full_v3`
- `utility_routing_sanity_v2`
- `utility_routing_full_v3`

### Mechanism Diagnosis

- `expert_headroom_diagnosis_v1`
- `control_alignment_diagnosis_v2`
- `mechanism_diagnosis`
- `mechanism_diagnosis_smoke`
- `mechanism_diagnosis_smoke_v2`

### Representation Control

- `representation_control_screen_v3`
- `representation_control_confirm_s010_r10`
- `representation_control_strength_0.05`
- `representation_control_strength_0.10`
- `representation_control_strength_0.20`
- `representation_control_strength_combined_summary.csv`
- `representation_control_strength_key_comparisons.csv`
- `iterative_relation_k1_screen`
- `iterative_relation_k2_screen`
- `iterative_relation_k3_screen`
- `iterative_relation_binary_k1_screen`
- `iterative_relation_binary_shared_backbone`
- `phaseA_raw_concat_screen`
  - Phase A input-side screening baseline with `reliability_encoder_mode=raw_concat`.
- `phaseA_component_aligned_screen`
  - Historical component mean/aligned encoder screening; not selected as the main baseline.
- `phaseA2_raw_concat_screen`
  - Phase A2 baseline rerun for direct comparison with component concat.
- `phaseA2_component_concat_screen`
  - Current recommended reliability encoder baseline.
  - Uses component-wise encoders followed by direct concat:
    `reliability_encoder_mode=component_concat`,
    `reliability_component_dim=16`,
    `component_missing_mode=zero_slot`.
- `phaseA2_shared_cache`
  - Shared expert/backbone cache used by Phase A2 raw concat and component concat runs.

### Historical Archive

- `archive`
- `archive_manifest.csv`

## Suggested Reading Order

1. `iter_relation_mechanism_v1`
2. `control_alignment_diagnosis_v2`
3. `expert_headroom_diagnosis_v1`
4. `preference_routing_full_v3`
5. `utility_routing_full_v3`
6. `expert_validation_full`
7. `phaseA2_component_concat_screen`

## Notes

- No existing result directory was modified by this indexing update.
- The current active folder was intentionally left untouched.
- Folder grouping is recorded in `experiment_index.csv`.
