# Current Evidence Matrix

This document consolidates the current evidence for whether structural reliability can control local/global representation correction.

## Current Best Representation-Control Configuration

| Parameter | Value |
|---|---|
| reliability_encoder_mode | component_concat |
| reliability_component_dim | 32 |
| component_missing_mode | zero_slot |
| rw_steps | 8 |
| alpha_type | channel |
| relation_steps | 1 |
| hidden_dim | 64 |
| num_layers | 2 |
| num_heads | 4 |
| max_adjustment | 0.1 |
| lambda_init | 0.001 |

## Current Main Evidence Table

| Dataset | Runs | Source | Config tag | Protocol level | Metric | Fixed | Reliability | Combined | Shuffled | Constant | Local GraphGPS Repro | Best | True-Fixed | True-Shuffled | True-Constant | Rel Pref AUC | Feature Pref AUC | Combined Pref AUC | Oracle Gap | Reliability-specific? | Paper Use | Verdict |
|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| Roman-empire | 10 | phaseC_rw8_dim32_confirm_r10 | dim32-rw8-channel | main 10-run current best | accuracy | 82.48 | 84.52 | **84.59** | 82.27 | 82.57 | 84.15 | combined 84.59 | +2.03 | +2.25 | +1.95 | 0.6997 | 0.7674 | 0.8379 | +3.73 | yes | main positive | strong positive |
| Arxiv-year, source_to_target | 10 | arxiv_year_directed_component_concat_confirm_r10 | dim32-rw8-channel-component_concat | directed 10-run confirmation | accuracy | 43.07 | 47.47 | **47.49** | 43.21 | 43.22 |  | combined 47.49 | +4.40 | +4.26 | +4.25 |  |  |  |  | yes | second mechanism positive | strong mechanism-positive, low absolute accuracy |
| Arxiv-year, undirected | 10 | arxiv_year_undirected_component_concat_confirm_r10 | dim32-rw8-channel-component_concat | undirected 10-run confirmation | accuracy | 45.39 | 46.69 | **46.76** | 45.41 | 45.45 |  | combined 46.76 | +1.30 | +1.28 | +1.24 |  |  |  |  | yes | second mechanism positive, weaker protocol | clean positive but weaker than directed |
| OGBN-Arxiv original, undirected | 10 | ogbn_arxiv_full_controls_h128_l3_drop03_lr003_r10 | h128-l3-rw8-channel-component_concat | original OGB task 10-run confirmation | accuracy | 69.83 | **70.35** | 70.24 | 69.90 | 69.99 | 69.07 | reliability_only 70.35 | +0.52 | +0.45 | +0.36 |  |  |  |  | yes | confirmed mechanism positive | stable frozen reliability controller gain; h256-l2 was unstable and is not used |
| Questions | 10 | phaseC1_questions_bestparams_channel_r10 | dim32-rw8-channel | supplemental 10-run | roc_auc | 77.63 | **77.85** | 77.76 | 77.63 | 77.70 | 73.41 | reliability_only 77.85 | +0.22 | +0.23 | +0.15 |  |  |  |  | weak yes, finetune-only | supplemental weak evidence | weak / inconclusive positive |
| Amazon-ratings | 10 | phaseC_rw8_dim32_confirm_r10 | dim32-rw8-channel | main negative 10-run | accuracy | 46.78 | 46.76 | **46.91** | 46.76 | 46.73 |  | combined 46.91 | -0.01 | +0.01 | +0.03 | 0.5580 | 0.5346 | 0.5620 | +13.30 | no | negative boundary | negative / signal failure |
| Minesweeper | 3 | phaseC0_existing_datasets_channel_screen | phaseC0-channel-screen | negative diagnostic 3-run | roc_auc | **90.65** | 90.65 | 90.65 | 90.65 | 90.65 |  | fixed 90.65 | +0.00 | +0.00 | +0.00 | 0.5911 | 0.5289 | 0.5071 |  | no | negative boundary | negative |
| Tolokers | 3 | iterative_relation_binary_k1_screen | binary-k1-screen | binary ROC-AUC screening 3-run | roc_auc | 85.38 | 85.19 |  | 84.78 | **85.42** |  | constant 85.42 | -0.19 | +0.41 | -0.23 |  |  |  |  | no, constant higher | negative boundary | non-specific / weak |
| Texas | 3 | webkb_best_config_screen | webkb-best-config-screen | screening negative 3-run | accuracy | **76.58** | 74.77 | 74.77 | 74.77 | 74.77 |  | fixed 76.58 | -1.80 | +0.00 | +0.00 |  |  |  |  | no | negative boundary | negative |
| Cornell | 3 | webkb_best_config_screen | webkb-best-config-screen | screening negative 3-run | accuracy | 75.68 | **77.48** | 76.58 | 77.48 | 77.48 |  | reliability_only 77.48 | +1.80 | +0.00 | +0.00 |  |  |  |  | no, copied by shuffled/constant | negative boundary | non-specific controller effect |
| Wisconsin | 3 | webkb_best_config_screen | webkb-best-config-screen | screening negative 3-run | accuracy | 83.01 | **83.66** | 83.66 | 83.66 | 83.66 |  | reliability_only 83.66 | +0.65 | +0.00 | +0.00 |  |  |  |  | no, copied by shuffled/constant | negative boundary | non-specific / negative |
| Actor | 3 | phaseC0_existing_datasets_channel_screen | phaseC0-channel-screen | negative diagnostic 3-run | accuracy | **36.23** | 36.23 | 36.23 | 36.23 | 36.23 |  | fixed 36.23 | +0.00 | +0.00 | +0.00 | 0.5279 | 0.5276 | 0.5392 |  | no | negative boundary | negative |

## Historical / Protocol-Caution Table

| Dataset | Group | Runs | Source | Config tag | Protocol level | Metric | Fixed / Baseline | Reliability | Combined | Shuffled | Constant | Best | Reliability-specific? | Paper Use | Note |
|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| Cora | homophily fallback | 10 | archive/2026-06-19/04_real_data/real_suite | old-real-suite | historical old-architecture 10-run | accuracy | **80.88** | 69.98 | 69.78 |  |  | fixed 80.88 | not comparable | historical diagnostic only | checks whether earlier GT-style modules damage homophily baselines |
| Citeseer | homophily fallback | 10 | archive/2026-06-19/04_real_data/real_suite | old-real-suite | historical old-architecture 10-run | accuracy | **68.42** | 62.11 | 62.72 |  |  | fixed 68.42 | not comparable | historical diagnostic only | checks whether earlier GT-style modules damage homophily baselines |
| Pubmed | homophily fallback | 10 | archive/2026-06-19/04_real_data/real_suite | old-real-suite | historical old-architecture 10-run | accuracy | **76.42** | 73.71 | 73.09 |  |  | fixed 76.42 | not comparable | historical diagnostic only | checks whether earlier GT-style modules damage homophily baselines |
| Chameleon | protocol-sensitive stress test | 3 | phaseC0_existing_datasets_channel_screen | phaseC0-channel-screen | protocol caution 3-run | accuracy | 53.22 | 52.92 | 53.65 | **53.95** | 53.29 | shuffled 53.95 | failed control | protocol caution only | available channel-screen run shows shuffled reliability above true reliability |
| Squirrel | protocol-sensitive stress test | 10 | phaseC1_squirrel_bestparams_channel_r10 | dim32-rw8-channel | protocol caution 10-run | accuracy | 34.22 | 34.38 | 34.21 | **34.44** | 34.44 | shuffled 34.44 | failed control | protocol caution only | preference signal exists, but utility control does not beat shuffled/constant |

## Broader Benchmark Table

| Dataset | Metric | Status | Protocol note | Paper Use |
|---|---|---|---|---|
| PascalVOC-SP | weighted F1 | not yet summarized | edge-index-only adaptation; edge_attr ignored | broader benchmark pending |

## Local GraphGPS Reproduction Table

These are local reproductions under available configs, not values copied from the original GraphGPS paper.

| Dataset | Metric | Best Local GraphGPS Repro | Source |
|---|---|---:|---|
| Roman-empire | accuracy | 84.15 | results_lappe_rwse_gatedgcn_performer\roman-empire-GPS\agg\test\best.json |
| Questions | roc_auc | 73.41 | results_questions_nope_gcn_performer\questions-GPS\agg\test\best.json |

## Interpretation By Category

### Strong Positive

- Roman-empire is the cleanest strong positive so far. True reliability beats fixed, shuffled, and constant controls by about 2 pp under the current best configuration.
- Roman values in this table use the current best `dim32-rw8-channel` configuration, not the earlier strength=0.10 formal confirm table.
- Roman-empire also has strong preference separability when reliability is combined with node/features: Rel AUC 0.6997, Feature AUC 0.7674, Combined AUC 0.8379.
- Local GraphGPS reproduction is integrated when a completed `agg/test/best.json` exists. Roman-empire local GraphGPS best is 84.15 accuracy, while our best current combined controller is 84.59.
- Arxiv-year is now a second clean mechanism-positive dataset under 10 runs. The `source_to_target` protocol has the strongest effect: finetune combined reaches 47.49 accuracy, with true reliability beating fixed, shuffled, and constant controls by more than 4 pp. The undirected protocol is also positive, but weaker.
- Arxiv-year should be interpreted as mechanism-positive rather than absolute-performance-positive until GraphGPS/LINKX-style baselines are reproduced under the same split and preprocessing protocol.
- OGBN-Arxiv original subject classification has now passed 10-run confirmation under the stable `h128-l3-drop0.3-lr0.003` backbone. Frozen `reliability_only` reaches 70.35 accuracy versus fixed 69.83, shuffled 69.90, and constant 69.99. The paired gains are positive over fixed, feature-only, shuffled, and constant controls, so this is a confirmed mechanism-positive original OGB task result.

### Weak Or Inconclusive Positive

- Questions shows a small 10-run ROC-AUC gain (+0.22 pp over fixed, +0.23 pp over shuffled), but the effect is small and headroom/preference diagnostics are missing. It is supplemental, not a second main positive yet.
- Questions is therefore labeled `weak yes, finetune-only`, not a clean mechanism-positive dataset.
- Questions local GraphGPS reproductions currently have lower ROC-AUC than our current best configuration, but this comparison should still be treated as local reproduction rather than an official benchmark claim.

### Negative Or Non-Specific Evidence

- Amazon-ratings has large oracle headroom, but current reliability preference AUC is weak and final utility does not improve.
- Texas/Cornell/Wisconsin do not provide Roman-like evidence. Cornell/Wisconsin gains are copied by shuffled/constant controls, so they are non-specific controller effects.
- WebKB should be treated as a family-level negative result: web/text/hyperlink structure alone is insufficient. This rules out the simple explanation that Roman works merely because it is a text/web graph.
- Tolokers and Chameleon now have available run values in the table. Tolokers is from binary ROC-AUC screening with combined not summarized in that source; Chameleon is a protocol/control caution case. Neither is a clean second positive under the displayed controls.
- Minesweeper, Actor, and the homophily fallback datasets do not currently support the main mechanism.

### Protocol-Sensitive Stress Tests

- Chameleon and Squirrel should not be treated as core evidence because edge protocol sensitivity and shuffled/constant controls make the story less clean.

### Broader Benchmark

- PascalVOC-SP is useful for checking whether the controller can be adapted to LRGB-style tasks, but it should not be used as Roman-like evidence unless the same reliability-specific controls pass.

## Current Decision

The prescreen wrapper should remain a utility, not a research centerpiece. Arxiv-year has passed full 10-run representation-control confirmation and should be kept as a mechanism-positive dataset. OGBN-Arxiv original has also passed 10-run confirmation under the stable `h128-l3` backbone, with frozen reliability-specific gains that shuffled and constant controls cannot copy. The next research-relevant step is to add Arxiv-year/OGBN-Arxiv headroom, preference, node-level diagnostics, and strong local baselines.

## Candidate Dataset Direction

Priority candidates still worth checking: LINKX wiki / Non-Homophily-Large-Scale wiki, Wiki-CS, and genius. Arxiv-year and OGBN-Arxiv original have moved from candidate/screening status to confirmed mechanism-positive evidence, but both still need stronger same-protocol baseline comparison and node-level mechanism diagnostics.
