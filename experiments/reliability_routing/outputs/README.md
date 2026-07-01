# Reliability Routing Outputs

Last organized: 2026-07-01.

This directory stores experiment outputs for the reliability-routing project. The top level is intentionally kept shallow: active experiment folders stay in place, while loose validation reports and old exported summaries are collected under `_reports/`.

## Top-Level Layout

```text
outputs/
  README.md
  README_INDEX.md
  experiment_index.csv
  archive_manifest.csv
  _reports/
    dataset_validation/
    legacy_strength_sweep/
  evidence_matrix/
  archive/
  <experiment-output-directories>/
```

## Current Main Evidence

### Roman-Empire

The main positive result remains the component-concat iterative-relation controller on Roman-empire.

Recommended reference folders:

```text
phaseC_rw8_dim32_confirm_r10/
phaseB_alpha_channel_confirm_r10/
evidence_matrix/
```

Best remembered configuration:

```text
reliability_encoder_mode = component_concat
reliability_component_dim = 32
component_missing_mode = zero_slot
rw_steps = 8
alpha_type = channel
relation_steps = 1
```

### Arxiv-Year

Arxiv-year is now the strongest second mechanism-positive candidate.

Primary confirmation folders:

```text
arxiv_year_directed_component_concat_confirm_r10/
arxiv_year_undirected_component_concat_confirm_r10/
```

Directed/source-to-target is stronger and should be treated as the main Arxiv-year result:

```text
finetune fixed            43.07%
finetune reliability_only 47.47%
finetune combined         47.49%
```

Key directed 10-run deltas:

```text
reliability_only - fixed       +4.40 pp
reliability_only - shuffled    +4.26 pp
reliability_only - constant    +4.25 pp
combined - fixed               +4.42 pp
combined - combined_shuffled   +4.37 pp
combined - combined_constant   +4.28 pp
```

Undirected is also positive but weaker:

```text
finetune fixed            45.39%
finetune reliability_only 46.69%
finetune combined         46.76%
```

Interpretation: Arxiv-year is a mechanism-positive dataset, not yet a strong absolute-performance result against LINKX or a tuned GraphGPS-style baseline.

### PascalVOC-SP

The current PascalVOC-SP run is incomplete:

```text
lrgb_pascalvocsp_screen_v3/
```

It contains only seed 0 for all controls plus seed 1 for `fixed`. Do not use it as a formal comparison. The partial seed-0 signal is not favorable to reliability, so this branch should not consume more compute until the runner/protocol is revisited.

## New Candidate Data

Validation reports were moved to:

```text
_reports/dataset_validation/
```

Current validated candidates:

```text
Genius
Arxiv-year
WikiCS
```

LINKX Wiki is not downloaded. The expected manual file location is:

```text
data/linkx/wiki/wiki_features2M.pt
data/linkx/wiki/wiki_edges2M.pt
data/linkx/wiki/wiki_views2M.pt
```

## Report Folders

`_reports/dataset_validation/` contains one-off validation JSON files, including new-candidate checks and LRGB staging checks.

`_reports/legacy_strength_sweep/` contains the older representation-control strength sweep exports that were previously loose in the top-level `outputs/` directory.

## Historical Archive

Older early-stage outputs are kept under:

```text
archive/
archive_manifest.csv
```

The archive is retained for provenance only. Current conclusions should come from the phase folders, Arxiv-year confirmation folders, and `evidence_matrix/`.

## Reading Order

1. `evidence_matrix/`
2. `phaseC_rw8_dim32_confirm_r10/`
3. `arxiv_year_directed_component_concat_confirm_r10/`
4. `arxiv_year_undirected_component_concat_confirm_r10/`
5. `unified_diagnostics_v1/`
6. `webkb_best_config_screen/`
7. `lrgb_pascalvocsp_screen_v3/` only as an incomplete smoke result

## Caution

Do not compare Arxiv-year accuracy directly with OGB `ogbn-arxiv` results. They are different tasks:

```text
ogbn-arxiv: subject classification
Arxiv-year: year-bin classification
```

For Arxiv-year, the current result is best used to support reliability-specific controlled gains rather than SOTA-level absolute accuracy.
