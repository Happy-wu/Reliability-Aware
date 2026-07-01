# Reports Folder

This folder collects loose one-off report files that used to sit directly under `outputs/`.

## dataset_validation

Contains validation and staging reports:

- `new_candidate_dataset_validation*.json`
- `new_candidate_prepare_real_smoke.json`
- `lrgb_manual_stage_only.json`

These files record data integrity checks and are not experiment result folders.

## legacy_strength_sweep

Contains older exported CSV summaries:

- `representation_control_strength_combined_summary.csv`
- `representation_control_strength_key_comparisons.csv`

The corresponding experiment directories remain at top level:

- `representation_control_strength_0.05`
- `representation_control_strength_0.10`
- `representation_control_strength_0.20`
