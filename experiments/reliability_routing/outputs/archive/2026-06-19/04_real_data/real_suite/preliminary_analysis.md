# Real Dataset Preliminary Analysis

- Generated: 2026-06-18T18:11:23.510852+00:00
- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor
- Models: mlp, gcn, linear_gt, qk_gt, gate_gt, reliability_gt
- Runs per dataset/model: 10
- Planetoid uses its public split with repeated training seeds.
- Chameleon, Squirrel, and Actor cycle through official Geom-GCN splits.

## Accuracy Summary

| Dataset | Model | Mean | Std |
|---|---|---:|---:|
| Actor | gate_gt | 0.3593 | 0.0084 |
| Actor | gcn | 0.2745 | 0.0132 |
| Actor | linear_gt | 0.3512 | 0.0053 |
| Actor | mlp | 0.3536 | 0.0105 |
| Actor | qk_gt | 0.3547 | 0.0069 |
| Actor | reliability_gt | 0.3527 | 0.0071 |
| Chameleon | gate_gt | 0.5833 | 0.0197 |
| Chameleon | gcn | 0.6474 | 0.0222 |
| Chameleon | linear_gt | 0.5682 | 0.0196 |
| Chameleon | mlp | 0.4838 | 0.0223 |
| Chameleon | qk_gt | 0.5759 | 0.0205 |
| Chameleon | reliability_gt | 0.5816 | 0.0142 |
| Citeseer | gate_gt | 0.6272 | 0.0193 |
| Citeseer | gcn | 0.6842 | 0.0174 |
| Citeseer | linear_gt | 0.6149 | 0.0137 |
| Citeseer | mlp | 0.5125 | 0.0125 |
| Citeseer | qk_gt | 0.6225 | 0.0112 |
| Citeseer | reliability_gt | 0.6211 | 0.0112 |
| Cora | gate_gt | 0.6978 | 0.0211 |
| Cora | gcn | 0.8088 | 0.0050 |
| Cora | linear_gt | 0.6793 | 0.0083 |
| Cora | mlp | 0.5255 | 0.0070 |
| Cora | qk_gt | 0.6875 | 0.0147 |
| Cora | reliability_gt | 0.6998 | 0.0078 |
| Pubmed | gate_gt | 0.7309 | 0.0101 |
| Pubmed | gcn | 0.7642 | 0.0028 |
| Pubmed | linear_gt | 0.7254 | 0.0125 |
| Pubmed | mlp | 0.6977 | 0.0063 |
| Pubmed | qk_gt | 0.7284 | 0.0087 |
| Pubmed | reliability_gt | 0.7371 | 0.0079 |
| Squirrel | gate_gt | 0.4124 | 0.0154 |
| Squirrel | gcn | 0.4688 | 0.0138 |
| Squirrel | linear_gt | 0.4014 | 0.0179 |
| Squirrel | mlp | 0.3016 | 0.0155 |
| Squirrel | qk_gt | 0.3989 | 0.0235 |
| Squirrel | reliability_gt | 0.4237 | 0.0164 |

## Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Cora | QK-GT - LinearGT | +0.0082 | [-0.0069, +0.0233] | 6/0/4 | +0.2491 |
| Cora | Gate-GT - LinearGT | +0.0185 | [+0.0001, +0.0369] | 8/0/2 | +0.0488 |
| Cora | Reliability-GT - LinearGT | +0.0205 | [+0.0117, +0.0293] | 10/0/0 | +0.0005 |
| Cora | Reliability-GT - Gate-GT | +0.0020 | [-0.0165, +0.0205] | 5/0/5 | +0.8120 |
| Citeseer | QK-GT - LinearGT | +0.0076 | [-0.0037, +0.0189] | 5/1/4 | +0.1637 |
| Citeseer | Gate-GT - LinearGT | +0.0123 | [-0.0062, +0.0308] | 6/1/3 | +0.1676 |
| Citeseer | Reliability-GT - LinearGT | +0.0062 | [-0.0092, +0.0216] | 6/0/4 | +0.3854 |
| Citeseer | Reliability-GT - Gate-GT | -0.0061 | [-0.0257, +0.0135] | 4/0/6 | +0.4983 |
| Pubmed | QK-GT - LinearGT | +0.0030 | [-0.0072, +0.0132] | 5/0/5 | +0.5230 |
| Pubmed | Gate-GT - LinearGT | +0.0055 | [-0.0039, +0.0149] | 5/1/4 | +0.2202 |
| Pubmed | Reliability-GT - LinearGT | +0.0117 | [+0.0021, +0.0213] | 8/0/2 | +0.0225 |
| Pubmed | Reliability-GT - Gate-GT | +0.0062 | [-0.0028, +0.0152] | 5/1/4 | +0.1540 |
| Chameleon | QK-GT - LinearGT | +0.0077 | [-0.0008, +0.0161] | 7/0/3 | +0.0698 |
| Chameleon | Gate-GT - LinearGT | +0.0151 | [+0.0008, +0.0295] | 6/2/2 | +0.0406 |
| Chameleon | Reliability-GT - LinearGT | +0.0134 | [+0.0018, +0.0249] | 8/0/2 | +0.0279 |
| Chameleon | Reliability-GT - Gate-GT | -0.0018 | [-0.0156, +0.0121] | 5/0/5 | +0.7810 |
| Squirrel | QK-GT - LinearGT | -0.0025 | [-0.0175, +0.0125] | 5/0/5 | +0.7154 |
| Squirrel | Gate-GT - LinearGT | +0.0110 | [-0.0022, +0.0241] | 7/0/3 | +0.0914 |
| Squirrel | Reliability-GT - LinearGT | +0.0223 | [+0.0077, +0.0369] | 9/0/1 | +0.0071 |
| Squirrel | Reliability-GT - Gate-GT | +0.0113 | [+0.0008, +0.0218] | 8/0/2 | +0.0373 |
| Actor | QK-GT - LinearGT | +0.0035 | [-0.0007, +0.0077] | 7/0/3 | +0.0926 |
| Actor | Gate-GT - LinearGT | +0.0082 | [+0.0035, +0.0128] | 8/0/2 | +0.0032 |
| Actor | Reliability-GT - LinearGT | +0.0015 | [-0.0024, +0.0055] | 6/0/4 | +0.4101 |
| Actor | Reliability-GT - Gate-GT | -0.0066 | [-0.0105, -0.0028] | 1/0/9 | +0.0036 |

## Decision Rule

- If Reliability-GT consistently exceeds Gate-GT, Q/K remains a candidate contribution.
- If Reliability-GT is approximately equal to Gate-GT, routing is the primary contribution.
- If Gate-GT does not exceed LinearGT, inspect reliability transfer and tuning before adding architecture.
- These p-values are exploratory and uncorrected across datasets.
