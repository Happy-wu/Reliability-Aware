# Expert Fusion Preliminary Analysis

- Edge protocol: undirected
- Runs: 10
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_025, fixed_alpha_050, fixed_alpha_075, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3535 | 0.3214 | 0.0118 | 0.100 |
| Actor | fixed_alpha_000 | 0.3526 | 0.3207 | 0.0124 | 0.000 |
| Actor | fixed_alpha_025 | 0.3533 | 0.3201 | 0.0112 | 0.250 |
| Actor | fixed_alpha_050 | 0.3507 | 0.3120 | 0.0110 | 0.500 |
| Actor | fixed_alpha_075 | 0.3456 | 0.2946 | 0.0122 | 0.750 |
| Actor | fixed_alpha_100 | 0.3036 | 0.2359 | 0.0092 | 1.000 |
| Actor | gcn_pyg | 0.3036 | 0.2359 | 0.0092 | n/a |
| Actor | global_only | 0.3526 | 0.3207 | 0.0124 | n/a |
| Actor | ordinary_gate | 0.3528 | 0.3200 | 0.0109 | n/a |
| Actor | reliability_gate | 0.3541 | 0.3223 | 0.0116 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.6456 | 0.6453 | 0.0134 | 0.975 |
| Chameleon | fixed_alpha_000 | 0.4750 | 0.4634 | 0.0216 | 0.000 |
| Chameleon | fixed_alpha_025 | 0.5235 | 0.5159 | 0.0270 | 0.250 |
| Chameleon | fixed_alpha_050 | 0.5743 | 0.5695 | 0.0356 | 0.500 |
| Chameleon | fixed_alpha_075 | 0.6333 | 0.6312 | 0.0251 | 0.750 |
| Chameleon | fixed_alpha_100 | 0.6436 | 0.6435 | 0.0132 | 1.000 |
| Chameleon | gcn_pyg | 0.6436 | 0.6435 | 0.0132 | n/a |
| Chameleon | global_only | 0.4750 | 0.4634 | 0.0216 | n/a |
| Chameleon | ordinary_gate | 0.5737 | 0.5691 | 0.0347 | n/a |
| Chameleon | reliability_gate | 0.5763 | 0.5718 | 0.0386 | n/a |
| Citeseer | best_fixed_alpha_by_val | 0.6929 | 0.6517 | 0.0048 | 0.975 |
| Citeseer | fixed_alpha_000 | 0.5174 | 0.4841 | 0.0140 | 0.000 |
| Citeseer | fixed_alpha_025 | 0.5383 | 0.5056 | 0.0339 | 0.250 |
| Citeseer | fixed_alpha_050 | 0.5564 | 0.5233 | 0.0485 | 0.500 |
| Citeseer | fixed_alpha_075 | 0.5903 | 0.5568 | 0.0543 | 0.750 |
| Citeseer | fixed_alpha_100 | 0.6931 | 0.6524 | 0.0047 | 1.000 |
| Citeseer | gcn_pyg | 0.6931 | 0.6524 | 0.0047 | n/a |
| Citeseer | global_only | 0.5174 | 0.4841 | 0.0140 | n/a |
| Citeseer | ordinary_gate | 0.5575 | 0.5252 | 0.0513 | n/a |
| Citeseer | reliability_gate | 0.5564 | 0.5233 | 0.0485 | n/a |
| Cora | best_fixed_alpha_by_val | 0.8121 | 0.8027 | 0.0029 | 1.000 |
| Cora | fixed_alpha_000 | 0.5450 | 0.5214 | 0.0088 | 0.000 |
| Cora | fixed_alpha_025 | 0.5790 | 0.5564 | 0.0351 | 0.250 |
| Cora | fixed_alpha_050 | 0.6349 | 0.6150 | 0.0516 | 0.500 |
| Cora | fixed_alpha_075 | 0.7180 | 0.7006 | 0.0444 | 0.750 |
| Cora | fixed_alpha_100 | 0.8121 | 0.8027 | 0.0029 | 1.000 |
| Cora | gcn_pyg | 0.8121 | 0.8027 | 0.0029 | n/a |
| Cora | global_only | 0.5450 | 0.5214 | 0.0088 | n/a |
| Cora | ordinary_gate | 0.6389 | 0.6201 | 0.0624 | n/a |
| Cora | reliability_gate | 0.6389 | 0.6201 | 0.0624 | n/a |
| Pubmed | best_fixed_alpha_by_val | 0.7687 | 0.7663 | 0.0031 | 1.000 |
| Pubmed | fixed_alpha_000 | 0.7040 | 0.7069 | 0.0115 | 0.000 |
| Pubmed | fixed_alpha_025 | 0.7185 | 0.7203 | 0.0133 | 0.250 |
| Pubmed | fixed_alpha_050 | 0.7351 | 0.7367 | 0.0129 | 0.500 |
| Pubmed | fixed_alpha_075 | 0.7575 | 0.7573 | 0.0097 | 0.750 |
| Pubmed | fixed_alpha_100 | 0.7687 | 0.7663 | 0.0031 | 1.000 |
| Pubmed | gcn_pyg | 0.7687 | 0.7663 | 0.0031 | n/a |
| Pubmed | global_only | 0.7040 | 0.7069 | 0.0115 | n/a |
| Pubmed | ordinary_gate | 0.7324 | 0.7343 | 0.0127 | n/a |
| Pubmed | reliability_gate | 0.7351 | 0.7367 | 0.0129 | n/a |
| Squirrel | best_fixed_alpha_by_val | 0.4736 | 0.4668 | 0.0189 | 1.000 |
| Squirrel | fixed_alpha_000 | 0.3096 | 0.2999 | 0.0184 | 0.000 |
| Squirrel | fixed_alpha_025 | 0.3240 | 0.3145 | 0.0228 | 0.250 |
| Squirrel | fixed_alpha_050 | 0.3555 | 0.3466 | 0.0289 | 0.500 |
| Squirrel | fixed_alpha_075 | 0.4186 | 0.4124 | 0.0355 | 0.750 |
| Squirrel | fixed_alpha_100 | 0.4736 | 0.4668 | 0.0189 | 1.000 |
| Squirrel | gcn_pyg | 0.4736 | 0.4668 | 0.0189 | n/a |
| Squirrel | global_only | 0.3096 | 0.2999 | 0.0184 | n/a |
| Squirrel | ordinary_gate | 0.3549 | 0.3461 | 0.0288 | n/a |
| Squirrel | reliability_gate | 0.3554 | 0.3465 | 0.0290 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.304 | 0.353 | 0.127 | 0.170 | 0.244 |
| Actor | fixed_alpha_025 | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Actor | fixed_alpha_050 | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Actor | fixed_alpha_075 | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Actor | ordinary_gate | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Actor | reliability_gate | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Chameleon | best_fixed_alpha_by_val | 0.644 | 0.518 | 0.248 | 0.129 | 0.355 |
| Chameleon | fixed_alpha_025 | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Chameleon | fixed_alpha_050 | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Chameleon | fixed_alpha_075 | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Chameleon | ordinary_gate | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Chameleon | reliability_gate | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Citeseer | best_fixed_alpha_by_val | 0.693 | 0.522 | 0.250 | 0.080 | 0.260 |
| Citeseer | fixed_alpha_025 | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Citeseer | fixed_alpha_050 | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Citeseer | fixed_alpha_075 | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Citeseer | ordinary_gate | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Citeseer | reliability_gate | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Cora | fixed_alpha_025 | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Cora | fixed_alpha_050 | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Cora | fixed_alpha_075 | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Cora | ordinary_gate | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Cora | reliability_gate | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Pubmed | fixed_alpha_025 | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Pubmed | fixed_alpha_050 | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Pubmed | fixed_alpha_075 | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Pubmed | ordinary_gate | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Pubmed | reliability_gate | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Squirrel | fixed_alpha_025 | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |
| Squirrel | fixed_alpha_050 | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |
| Squirrel | fixed_alpha_075 | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |
| Squirrel | ordinary_gate | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |
| Squirrel | reliability_gate | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Cora | Reliability gate - ordinary gate | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | ordinary_gate - validation-selected fixed alpha | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Cora | reliability_gate - validation-selected fixed alpha | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Cora | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | ordinary_gate - GCN | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Cora | reliability_gate - GCN | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Cora | ordinary_gate - fixed_alpha_000 | +0.0939 | [+0.0469, +0.1409] | 10/0/0 | +0.0014 |
| Cora | ordinary_gate - fixed_alpha_025 | +0.0599 | [+0.0368, +0.0830] | 10/0/0 | +0.0002 |
| Cora | ordinary_gate - fixed_alpha_050 | +0.0040 | [-0.0050, +0.0130] | 1/9/0 | +0.3434 |
| Cora | ordinary_gate - fixed_alpha_075 | -0.0791 | [-0.1011, -0.0571] | 1/0/9 | +0.0000 |
| Cora | ordinary_gate - fixed_alpha_100 | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Cora | reliability_gate - fixed_alpha_000 | +0.0939 | [+0.0469, +0.1409] | 10/0/0 | +0.0014 |
| Cora | reliability_gate - fixed_alpha_025 | +0.0599 | [+0.0368, +0.0830] | 10/0/0 | +0.0002 |
| Cora | reliability_gate - fixed_alpha_050 | +0.0040 | [-0.0050, +0.0130] | 1/9/0 | +0.3434 |
| Cora | reliability_gate - fixed_alpha_075 | -0.0791 | [-0.1011, -0.0571] | 1/0/9 | +0.0000 |
| Cora | reliability_gate - fixed_alpha_100 | -0.1732 | [-0.2205, -0.1259] | 0/1/9 | +0.0000 |
| Citeseer | Reliability gate - ordinary gate | -0.0011 | [-0.0036, +0.0014] | 0/9/1 | +0.3434 |
| Citeseer | ordinary_gate - validation-selected fixed alpha | -0.1354 | [-0.1756, -0.0952] | 0/0/10 | +0.0000 |
| Citeseer | reliability_gate - validation-selected fixed alpha | -0.1365 | [-0.1747, -0.0983] | 0/0/10 | +0.0000 |
| Citeseer | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Citeseer | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Citeseer | ordinary_gate - GCN | -0.1356 | [-0.1755, -0.0957] | 0/0/10 | +0.0000 |
| Citeseer | reliability_gate - GCN | -0.1367 | [-0.1745, -0.0989] | 0/0/10 | +0.0000 |
| Citeseer | ordinary_gate - fixed_alpha_000 | +0.0401 | [+0.0052, +0.0750] | 10/0/0 | +0.0287 |
| Citeseer | ordinary_gate - fixed_alpha_025 | +0.0192 | [+0.0052, +0.0332] | 10/0/0 | +0.0125 |
| Citeseer | ordinary_gate - fixed_alpha_050 | +0.0011 | [-0.0014, +0.0036] | 1/9/0 | +0.3434 |
| Citeseer | ordinary_gate - fixed_alpha_075 | -0.0328 | [-0.0494, -0.0162] | 0/0/10 | +0.0015 |
| Citeseer | ordinary_gate - fixed_alpha_100 | -0.1356 | [-0.1755, -0.0957] | 0/0/10 | +0.0000 |
| Citeseer | reliability_gate - fixed_alpha_000 | +0.0390 | [+0.0064, +0.0716] | 10/0/0 | +0.0243 |
| Citeseer | reliability_gate - fixed_alpha_025 | +0.0181 | [+0.0060, +0.0302] | 10/0/0 | +0.0081 |
| Citeseer | reliability_gate - fixed_alpha_050 | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Citeseer | reliability_gate - fixed_alpha_075 | -0.0339 | [-0.0494, -0.0184] | 0/0/10 | +0.0008 |
| Citeseer | reliability_gate - fixed_alpha_100 | -0.1367 | [-0.1745, -0.0989] | 0/0/10 | +0.0000 |
| Pubmed | Reliability gate - ordinary gate | +0.0027 | [-0.0034, +0.0088] | 1/9/0 | +0.3434 |
| Pubmed | ordinary_gate - validation-selected fixed alpha | -0.0363 | [-0.0460, -0.0266] | 0/0/10 | +0.0000 |
| Pubmed | reliability_gate - validation-selected fixed alpha | -0.0336 | [-0.0437, -0.0235] | 0/0/10 | +0.0000 |
| Pubmed | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Pubmed | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Pubmed | ordinary_gate - GCN | -0.0363 | [-0.0460, -0.0266] | 0/0/10 | +0.0000 |
| Pubmed | reliability_gate - GCN | -0.0336 | [-0.0437, -0.0235] | 0/0/10 | +0.0000 |
| Pubmed | ordinary_gate - fixed_alpha_000 | +0.0284 | [+0.0217, +0.0351] | 10/0/0 | +0.0000 |
| Pubmed | ordinary_gate - fixed_alpha_025 | +0.0139 | [+0.0076, +0.0202] | 9/0/1 | +0.0008 |
| Pubmed | ordinary_gate - fixed_alpha_050 | -0.0027 | [-0.0088, +0.0034] | 0/9/1 | +0.3434 |
| Pubmed | ordinary_gate - fixed_alpha_075 | -0.0251 | [-0.0329, -0.0173] | 0/0/10 | +0.0000 |
| Pubmed | ordinary_gate - fixed_alpha_100 | -0.0363 | [-0.0460, -0.0266] | 0/0/10 | +0.0000 |
| Pubmed | reliability_gate - fixed_alpha_000 | +0.0311 | [+0.0224, +0.0398] | 10/0/0 | +0.0000 |
| Pubmed | reliability_gate - fixed_alpha_025 | +0.0166 | [+0.0115, +0.0217] | 10/0/0 | +0.0000 |
| Pubmed | reliability_gate - fixed_alpha_050 | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Pubmed | reliability_gate - fixed_alpha_075 | -0.0224 | [-0.0283, -0.0165] | 0/0/10 | +0.0000 |
| Pubmed | reliability_gate - fixed_alpha_100 | -0.0336 | [-0.0437, -0.0235] | 0/0/10 | +0.0000 |
| Chameleon | Reliability gate - ordinary gate | +0.0026 | [-0.0033, +0.0086] | 1/9/0 | +0.3434 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0719 | [-0.0953, -0.0486] | 0/0/10 | +0.0001 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0693 | [-0.0954, -0.0432] | 0/0/10 | +0.0002 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | ordinary_gate - GCN | -0.0700 | [-0.0952, -0.0447] | 0/0/10 | +0.0001 |
| Chameleon | reliability_gate - GCN | -0.0673 | [-0.0960, -0.0386] | 1/0/9 | +0.0005 |
| Chameleon | ordinary_gate - fixed_alpha_000 | +0.0987 | [+0.0763, +0.1211] | 10/0/0 | +0.0000 |
| Chameleon | ordinary_gate - fixed_alpha_025 | +0.0502 | [+0.0343, +0.0661] | 10/0/0 | +0.0001 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0007 | [-0.0021, +0.0008] | 0/9/1 | +0.3434 |
| Chameleon | ordinary_gate - fixed_alpha_075 | -0.0596 | [-0.0727, -0.0466] | 0/0/10 | +0.0000 |
| Chameleon | ordinary_gate - fixed_alpha_100 | -0.0700 | [-0.0952, -0.0447] | 0/0/10 | +0.0001 |
| Chameleon | reliability_gate - fixed_alpha_000 | +0.1013 | [+0.0782, +0.1245] | 10/0/0 | +0.0000 |
| Chameleon | reliability_gate - fixed_alpha_025 | +0.0529 | [+0.0360, +0.0697] | 10/0/0 | +0.0001 |
| Chameleon | reliability_gate - fixed_alpha_050 | +0.0020 | [-0.0025, +0.0064] | 1/9/0 | +0.3434 |
| Chameleon | reliability_gate - fixed_alpha_075 | -0.0570 | [-0.0733, -0.0407] | 0/0/10 | +0.0000 |
| Chameleon | reliability_gate - fixed_alpha_100 | -0.0673 | [-0.0960, -0.0386] | 1/0/9 | +0.0005 |
| Squirrel | Reliability gate - ordinary gate | +0.0005 | [-0.0006, +0.0016] | 1/9/0 | +0.3434 |
| Squirrel | ordinary_gate - validation-selected fixed alpha | -0.1186 | [-0.1333, -0.1039] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - validation-selected fixed alpha | -0.1182 | [-0.1332, -0.1032] | 0/0/10 | +0.0000 |
| Squirrel | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | ordinary_gate - GCN | -0.1186 | [-0.1333, -0.1039] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - GCN | -0.1182 | [-0.1332, -0.1032] | 0/0/10 | +0.0000 |
| Squirrel | ordinary_gate - fixed_alpha_000 | +0.0453 | [+0.0313, +0.0593] | 10/0/0 | +0.0000 |
| Squirrel | ordinary_gate - fixed_alpha_025 | +0.0309 | [+0.0222, +0.0397] | 10/0/0 | +0.0000 |
| Squirrel | ordinary_gate - fixed_alpha_050 | -0.0006 | [-0.0017, +0.0005] | 0/8/2 | +0.2598 |
| Squirrel | ordinary_gate - fixed_alpha_075 | -0.0637 | [-0.0736, -0.0538] | 0/0/10 | +0.0000 |
| Squirrel | ordinary_gate - fixed_alpha_100 | -0.1186 | [-0.1333, -0.1039] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - fixed_alpha_000 | +0.0458 | [+0.0314, +0.0602] | 10/0/0 | +0.0001 |
| Squirrel | reliability_gate - fixed_alpha_025 | +0.0314 | [+0.0223, +0.0405] | 10/0/0 | +0.0000 |
| Squirrel | reliability_gate - fixed_alpha_050 | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Squirrel | reliability_gate - fixed_alpha_075 | -0.0632 | [-0.0724, -0.0540] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - fixed_alpha_100 | -0.1182 | [-0.1332, -0.1032] | 0/0/10 | +0.0000 |
| Actor | Reliability gate - ordinary gate | +0.0014 | [-0.0003, +0.0030] | 6/3/1 | +0.0911 |
| Actor | ordinary_gate - validation-selected fixed alpha | -0.0007 | [-0.0027, +0.0013] | 4/0/6 | +0.4319 |
| Actor | reliability_gate - validation-selected fixed alpha | +0.0007 | [-0.0008, +0.0021] | 7/0/3 | +0.3330 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0492 | [+0.0424, +0.0561] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - GCN | +0.0506 | [+0.0428, +0.0584] | 10/0/0 | +0.0000 |
| Actor | ordinary_gate - fixed_alpha_000 | +0.0001 | [-0.0017, +0.0019] | 6/0/4 | +0.8732 |
| Actor | ordinary_gate - fixed_alpha_025 | -0.0005 | [-0.0033, +0.0022] | 5/0/5 | +0.6754 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0020 | [-0.0020, +0.0061] | 6/0/4 | +0.2835 |
| Actor | ordinary_gate - fixed_alpha_075 | +0.0072 | [+0.0002, +0.0142] | 9/0/1 | +0.0460 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0492 | [+0.0424, +0.0561] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - fixed_alpha_000 | +0.0015 | [+0.0006, +0.0025] | 9/0/1 | +0.0055 |
| Actor | reliability_gate - fixed_alpha_025 | +0.0009 | [-0.0011, +0.0028] | 6/1/3 | +0.3523 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0034 | [+0.0001, +0.0068] | 9/0/1 | +0.0458 |
| Actor | reliability_gate - fixed_alpha_075 | +0.0086 | [+0.0010, +0.0162] | 9/0/1 | +0.0314 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0506 | [+0.0428, +0.0584] | 10/0/0 | +0.0000 |
