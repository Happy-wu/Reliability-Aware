# Reliability Suite Preliminary Analysis

- Generated: 2026-06-18T14:04:37.765014+00:00
- Seeds: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- Graphs: heterophily, homophily, noisy
- Device: cuda
- Delta definition: left model minus right/baseline model using matched seeds.
- A 95% CI excluding zero is treated as preliminary evidence, not a final claim.

## Branch-Specific Encoder Comparisons

| Graph | Comparison | Left | Right | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|---:|---:|
| heterophily | gate encoded - static | 0.8419 | 0.8411 | +0.0008 | [-0.0220, +0.0235] | 5/0/5 | 0.9388 |
| heterophily | qk encoded - static | 0.8189 | 0.8203 | -0.0014 | [-0.0240, +0.0211] | 5/0/5 | 0.8892 |
| heterophily | reliability encoded - static | 0.8554 | 0.8637 | -0.0083 | [-0.0336, +0.0171] | 3/0/7 | 0.4795 |
| heterophily | static reliability - static gate | 0.8637 | 0.8411 | +0.0225 | [-0.0056, +0.0507] | 8/0/2 | 0.1037 |
| heterophily | encoded reliability - encoded gate | 0.8554 | 0.8419 | +0.0135 | [-0.0101, +0.0371] | 6/0/4 | 0.2282 |
| homophily | gate encoded - static | 0.9706 | 0.9686 | +0.0021 | [-0.0035, +0.0076] | 6/1/3 | 0.4232 |
| homophily | qk encoded - static | 0.9206 | 0.9256 | -0.0049 | [-0.0199, +0.0101] | 5/0/5 | 0.4770 |
| homophily | reliability encoded - static | 0.9668 | 0.9683 | -0.0014 | [-0.0063, +0.0035] | 5/0/5 | 0.5276 |
| homophily | static reliability - static gate | 0.9683 | 0.9686 | -0.0003 | [-0.0051, +0.0044] | 3/1/6 | 0.8832 |
| homophily | encoded reliability - encoded gate | 0.9668 | 0.9706 | -0.0038 | [-0.0070, -0.0006] | 2/2/6 | 0.0239 |
| noisy | gate encoded - static | 0.5898 | 0.6071 | -0.0173 | [-0.0379, +0.0033] | 2/0/8 | 0.0897 |
| noisy | qk encoded - static | 0.6013 | 0.5967 | +0.0046 | [-0.0133, +0.0226] | 5/0/5 | 0.5761 |
| noisy | reliability encoded - static | 0.5921 | 0.6117 | -0.0197 | [-0.0417, +0.0024] | 3/0/7 | 0.0742 |
| noisy | static reliability - static gate | 0.6117 | 0.6071 | +0.0046 | [-0.0253, +0.0345] | 6/0/4 | 0.7357 |
| noisy | encoded reliability - encoded gate | 0.5921 | 0.5898 | +0.0022 | [-0.0172, +0.0216] | 6/1/3 | 0.8014 |

## Component Ablation

Each row is compared with the same static model using the full reliability basis from `batch_reliability_encoder_compare`.
Local similarity and neighbor variance are gate-only components; when selected alone, the Q/K reliability input is zero.

### heterophily / gate_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Without RWSE | 0.8576 | +0.0165 | [+0.0007, +0.0323] | 9/1/0 | 0.0421 |
| Only local similarity | 0.8575 | +0.0163 | [+0.0062, +0.0265] | 9/0/1 | 0.0053 |
| Only neighbor variance | 0.8560 | +0.0149 | [+0.0016, +0.0283] | 9/0/1 | 0.0323 |
| Without degree | 0.8533 | +0.0122 | [+0.0029, +0.0216] | 8/0/2 | 0.0160 |
| Only RWSE | 0.8532 | +0.0121 | [-0.0002, +0.0243] | 8/0/2 | 0.0532 |
| Without neighbor variance | 0.8530 | +0.0119 | [-0.0056, +0.0294] | 6/0/4 | 0.1583 |
| Only degree | 0.8530 | +0.0119 | [-0.0041, +0.0279] | 9/0/1 | 0.1266 |
| Without local similarity | 0.8451 | +0.0040 | [-0.0050, +0.0130] | 5/0/5 | 0.3442 |

### heterophily / reliability_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Without neighbor variance | 0.8768 | +0.0132 | [+0.0018, +0.0245] | 8/0/2 | 0.0275 |
| Only degree | 0.8729 | +0.0092 | [-0.0073, +0.0257] | 8/0/2 | 0.2387 |
| Without degree | 0.8683 | +0.0046 | [-0.0079, +0.0171] | 7/0/3 | 0.4256 |
| Only local similarity | 0.8665 | +0.0029 | [-0.0135, +0.0192] | 7/0/3 | 0.7018 |
| Only neighbor variance | 0.8646 | +0.0010 | [-0.0122, +0.0141] | 6/0/4 | 0.8731 |
| Without local similarity | 0.8637 | +0.0000 | [-0.0154, +0.0154] | 6/0/4 | 1.0000 |
| Only RWSE | 0.8635 | -0.0002 | [-0.0151, +0.0148] | 5/0/5 | 0.9814 |
| Without RWSE | 0.8613 | -0.0024 | [-0.0203, +0.0156] | 6/0/4 | 0.7711 |

### homophily / gate_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Only RWSE | 0.9714 | +0.0029 | [-0.0031, +0.0088] | 6/3/1 | 0.3060 |
| Without neighbor variance | 0.9708 | +0.0022 | [-0.0005, +0.0049] | 5/4/1 | 0.0942 |
| Without local similarity | 0.9702 | +0.0016 | [-0.0028, +0.0059] | 4/3/3 | 0.4303 |
| Only local similarity | 0.9692 | +0.0006 | [-0.0050, +0.0063] | 4/1/5 | 0.8049 |
| Without degree | 0.9687 | +0.0002 | [-0.0046, +0.0050] | 3/4/3 | 0.9420 |
| Only neighbor variance | 0.9681 | -0.0005 | [-0.0066, +0.0057] | 4/2/4 | 0.8649 |
| Without RWSE | 0.9681 | -0.0005 | [-0.0050, +0.0040] | 4/1/5 | 0.8166 |
| Only degree | 0.9663 | -0.0022 | [-0.0095, +0.0051] | 5/1/4 | 0.5075 |

### homophily / reliability_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Only local similarity | 0.9716 | +0.0033 | [+0.0006, +0.0060] | 7/1/2 | 0.0210 |
| Without RWSE | 0.9716 | +0.0033 | [-0.0021, +0.0088] | 6/1/3 | 0.2014 |
| Only degree | 0.9710 | +0.0027 | [-0.0015, +0.0069] | 8/0/2 | 0.1816 |
| Without neighbor variance | 0.9705 | +0.0022 | [-0.0019, +0.0063] | 6/3/1 | 0.2495 |
| Without degree | 0.9690 | +0.0008 | [-0.0033, +0.0049] | 4/5/1 | 0.6733 |
| Only neighbor variance | 0.9681 | -0.0002 | [-0.0050, +0.0047] | 2/2/6 | 0.9424 |
| Only RWSE | 0.9679 | -0.0003 | [-0.0059, +0.0053] | 4/0/6 | 0.9009 |
| Without local similarity | 0.9659 | -0.0024 | [-0.0059, +0.0011] | 2/3/5 | 0.1604 |

### noisy / gate_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Only degree | 0.6278 | +0.0206 | [+0.0045, +0.0368] | 9/0/1 | 0.0179 |
| Only neighbor variance | 0.6229 | +0.0157 | [-0.0023, +0.0337] | 6/1/3 | 0.0801 |
| Without local similarity | 0.6192 | +0.0121 | [-0.0058, +0.0299] | 6/1/3 | 0.1607 |
| Only local similarity | 0.6165 | +0.0094 | [-0.0140, +0.0327] | 7/1/2 | 0.3872 |
| Only RWSE | 0.6162 | +0.0090 | [+0.0002, +0.0179] | 8/0/2 | 0.0466 |
| Without neighbor variance | 0.6106 | +0.0035 | [-0.0094, +0.0164] | 4/1/5 | 0.5561 |
| Without RWSE | 0.6068 | -0.0003 | [-0.0229, +0.0223] | 5/0/5 | 0.9753 |
| Without degree | 0.6054 | -0.0017 | [-0.0105, +0.0070] | 3/0/7 | 0.6619 |

### noisy / reliability_gt

| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |
|---|---:|---:|---:|---:|---:|
| Only RWSE | 0.6260 | +0.0143 | [-0.0023, +0.0309] | 7/0/3 | 0.0829 |
| Only local similarity | 0.6205 | +0.0087 | [-0.0085, +0.0260] | 7/1/2 | 0.2822 |
| Only degree | 0.6200 | +0.0083 | [-0.0041, +0.0206] | 7/1/2 | 0.1654 |
| Only neighbor variance | 0.6195 | +0.0078 | [-0.0038, +0.0194] | 6/1/3 | 0.1632 |
| Without RWSE | 0.6152 | +0.0035 | [-0.0149, +0.0219] | 6/0/4 | 0.6778 |
| Without local similarity | 0.6138 | +0.0021 | [-0.0161, +0.0202] | 4/0/6 | 0.8031 |
| Without neighbor variance | 0.6127 | +0.0010 | [-0.0164, +0.0183] | 5/0/5 | 0.9038 |
| Without degree | 0.6089 | -0.0029 | [-0.0229, +0.0172] | 5/0/5 | 0.7546 |

## Automatic Preliminary Findings

- No branch-specific encoder comparison has a 95% CI excluding zero.
- Best single component for heterophily/gate_gt: Only local similarity (mean=0.8575, delta vs full=+0.0163).
- Best single component for heterophily/reliability_gt: Only degree (mean=0.8729, delta vs full=+0.0092).
- Best single component for homophily/gate_gt: Only RWSE (mean=0.9714, delta vs full=+0.0029).
- Best single component for homophily/reliability_gt: Only local similarity (mean=0.9716, delta vs full=+0.0033).
- Best single component for noisy/gate_gt: Only degree (mean=0.6278, delta vs full=+0.0206).
- Best single component for noisy/reliability_gt: Only RWSE (mean=0.6260, delta vs full=+0.0143).
- Gamma Q mean absolute deviation for heterophily/qk_gt: 0.000642.
- Gamma Q mean absolute deviation for heterophily/qk_gt_encoded: 0.001495.
- Gamma Q mean absolute deviation for heterophily/reliability_gt: 0.000451.
- Gamma Q mean absolute deviation for heterophily/reliability_gt_encoded: 0.001241.
- Gamma Q mean absolute deviation for homophily/qk_gt: 0.000508.
- Gamma Q mean absolute deviation for homophily/qk_gt_encoded: 0.001203.
- Gamma Q mean absolute deviation for homophily/reliability_gt: 0.000262.
- Gamma Q mean absolute deviation for homophily/reliability_gt_encoded: 0.000873.
- Gamma Q mean absolute deviation for noisy/qk_gt: 0.000542.
- Gamma Q mean absolute deviation for noisy/qk_gt_encoded: 0.001345.
- Gamma Q mean absolute deviation for noisy/reliability_gt: 0.000481.
- Gamma Q mean absolute deviation for noisy/reliability_gt_encoded: 0.001351.
- Component batches are compared with a baseline trained in a separate run. Use the paired deltas as screening evidence and re-run finalists in one combined batch.
- Multiple comparisons are exploratory; p-values are uncorrected.
