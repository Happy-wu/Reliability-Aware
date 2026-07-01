# Real Dataset Preliminary Analysis

- Generated: 2026-06-18T18:48:57.587844+00:00
- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor
- Models: gcn, gcn_pyg, local_only_gt, gate_gt, reliability_gt
- Runs per dataset/model: 10
- Planetoid uses its public split with repeated training seeds.
- Chameleon, Squirrel, and Actor cycle through official Geom-GCN splits.

## Accuracy Summary

| Dataset | Model | Mean | Std |
|---|---|---:|---:|
| Actor | gate_gt | 0.3592 | 0.0085 |
| Actor | gcn | 0.2745 | 0.0132 |
| Actor | gcn_pyg | 0.2841 | 0.0103 |
| Actor | local_only_gt | 0.3455 | 0.0057 |
| Actor | reliability_gt | 0.3518 | 0.0069 |
| Chameleon | gate_gt | 0.5814 | 0.0210 |
| Chameleon | gcn | 0.6474 | 0.0222 |
| Chameleon | gcn_pyg | 0.4268 | 0.0183 |
| Chameleon | local_only_gt | 0.6024 | 0.0208 |
| Chameleon | reliability_gt | 0.5800 | 0.0111 |
| Citeseer | gate_gt | 0.6272 | 0.0193 |
| Citeseer | gcn | 0.6842 | 0.0174 |
| Citeseer | gcn_pyg | 0.6931 | 0.0047 |
| Citeseer | local_only_gt | 0.6488 | 0.0134 |
| Citeseer | reliability_gt | 0.6211 | 0.0112 |
| Cora | gate_gt | 0.6986 | 0.0198 |
| Cora | gcn | 0.8088 | 0.0050 |
| Cora | gcn_pyg | 0.8121 | 0.0029 |
| Cora | local_only_gt | 0.7398 | 0.0114 |
| Cora | reliability_gt | 0.7002 | 0.0073 |
| Pubmed | gate_gt | 0.7309 | 0.0101 |
| Pubmed | gcn | 0.7642 | 0.0028 |
| Pubmed | gcn_pyg | 0.7687 | 0.0031 |
| Pubmed | local_only_gt | 0.7348 | 0.0176 |
| Pubmed | reliability_gt | 0.7340 | 0.0129 |
| Squirrel | gate_gt | 0.4191 | 0.0150 |
| Squirrel | gcn | 0.4688 | 0.0138 |
| Squirrel | gcn_pyg | 0.2891 | 0.0169 |
| Squirrel | local_only_gt | 0.4346 | 0.0197 |
| Squirrel | reliability_gt | 0.4273 | 0.0186 |

## Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Cora | PyG-GCN - custom GCN | +0.0033 | [-0.0009, +0.0075] | 6/1/3 | +0.1101 |
| Cora | Local-only GT - PyG-GCN | -0.0723 | [-0.0824, -0.0622] | 0/0/10 | +0.0000 |
| Cora | Reliability-GT - Gate-GT | +0.0016 | [-0.0159, +0.0191] | 5/0/5 | +0.8408 |
| Citeseer | PyG-GCN - custom GCN | +0.0089 | [-0.0037, +0.0215] | 8/0/2 | +0.1438 |
| Citeseer | Local-only GT - PyG-GCN | -0.0443 | [-0.0546, -0.0340] | 0/0/10 | +0.0000 |
| Citeseer | Reliability-GT - Gate-GT | -0.0061 | [-0.0257, +0.0135] | 4/0/6 | +0.4983 |
| Pubmed | PyG-GCN - custom GCN | +0.0045 | [+0.0005, +0.0085] | 6/3/1 | +0.0322 |
| Pubmed | Local-only GT - PyG-GCN | -0.0339 | [-0.0469, -0.0209] | 0/0/10 | +0.0002 |
| Pubmed | Reliability-GT - Gate-GT | +0.0031 | [-0.0091, +0.0153] | 4/1/5 | +0.5793 |
| Chameleon | PyG-GCN - custom GCN | -0.2206 | [-0.2393, -0.2019] | 0/0/10 | +0.0000 |
| Chameleon | Local-only GT - PyG-GCN | +0.1757 | [+0.1565, +0.1948] | 10/0/0 | +0.0000 |
| Chameleon | Reliability-GT - Gate-GT | -0.0013 | [-0.0145, +0.0119] | 5/0/5 | +0.8265 |
| Squirrel | PyG-GCN - custom GCN | -0.1796 | [-0.1920, -0.1673] | 0/0/10 | +0.0000 |
| Squirrel | Local-only GT - PyG-GCN | +0.1454 | [+0.1301, +0.1608] | 10/0/0 | +0.0000 |
| Squirrel | Reliability-GT - Gate-GT | +0.0082 | [-0.0055, +0.0218] | 7/0/3 | +0.2096 |
| Actor | PyG-GCN - custom GCN | +0.0097 | [-0.0009, +0.0203] | 8/0/2 | +0.0695 |
| Actor | Local-only GT - PyG-GCN | +0.0614 | [+0.0530, +0.0698] | 10/0/0 | +0.0000 |
| Actor | Reliability-GT - Gate-GT | -0.0074 | [-0.0102, -0.0046] | 0/0/10 | +0.0002 |

## Routing Diagnostics

| Dataset | Model | Gate mean | Gate std | Local norm | Global norm | Mixed norm | Local/global cosine |
|---|---|---:|---:|---:|---:|---:|---:|
| Actor | gate_gt | 0.4712 | 0.0749 | 2.1776 | 1.3606 | 1.0230 | -0.3509 |
| Actor | local_only_gt | n/a | n/a | 1.7306 | 1.1117 | 1.7306 | 0.0455 |
| Actor | reliability_gt | 0.4595 | 0.0401 | 2.1803 | 1.1444 | 1.1376 | -0.2967 |
| Chameleon | gate_gt | 0.5517 | 0.1483 | 2.1476 | 0.9964 | 1.2349 | -0.4804 |
| Chameleon | local_only_gt | n/a | n/a | 1.6407 | 0.9453 | 1.6407 | 0.0572 |
| Chameleon | reliability_gt | 0.5393 | 0.1484 | 2.1896 | 1.2305 | 1.3629 | -0.4232 |
| Citeseer | gate_gt | 0.6067 | 0.1303 | 3.0923 | 1.2319 | 1.7701 | -0.4871 |
| Citeseer | local_only_gt | n/a | n/a | 3.0790 | 1.1989 | 3.0790 | 0.0177 |
| Citeseer | reliability_gt | 0.5835 | 0.1178 | 2.9559 | 1.2642 | 1.6751 | -0.4427 |
| Cora | gate_gt | 0.6261 | 0.1186 | 2.7980 | 1.0492 | 1.6957 | -0.4837 |
| Cora | local_only_gt | n/a | n/a | 3.0414 | 0.9637 | 3.0414 | -0.0105 |
| Cora | reliability_gt | 0.6320 | 0.1266 | 2.8514 | 0.9851 | 1.7686 | -0.4832 |
| Pubmed | gate_gt | 0.6386 | 0.1628 | 2.9331 | 1.3720 | 1.8969 | -0.3769 |
| Pubmed | local_only_gt | n/a | n/a | 3.0302 | 1.1548 | 3.0302 | -0.0012 |
| Pubmed | reliability_gt | 0.6313 | 0.1843 | 3.2050 | 1.5316 | 2.1111 | -0.3239 |
| Squirrel | gate_gt | 0.5432 | 0.1466 | 1.5465 | 1.7382 | 1.2231 | -0.6611 |
| Squirrel | local_only_gt | n/a | n/a | 1.2119 | 1.0031 | 1.2119 | -0.0976 |
| Squirrel | reliability_gt | 0.6402 | 0.1261 | 1.3869 | 1.5936 | 1.0655 | -0.6106 |

## Decision Rule

- If Reliability-GT consistently exceeds Gate-GT, Q/K remains a candidate contribution.
- If Reliability-GT is approximately equal to Gate-GT, routing is the primary contribution.
- If Gate-GT does not exceed LinearGT, inspect reliability transfer and tuning before adding architecture.
- These p-values are exploratory and uncorrected across datasets.
