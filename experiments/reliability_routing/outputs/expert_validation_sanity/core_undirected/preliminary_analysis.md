# Expert Fusion Preliminary Analysis

- Edge protocol: undirected
- Runs: 3
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_050, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3616 | 0.3314 | 0.0067 | 0.000 |
| Actor | fixed_alpha_000 | 0.3616 | 0.3314 | 0.0067 | 0.000 |
| Actor | fixed_alpha_050 | 0.3559 | 0.3165 | 0.0046 | 0.500 |
| Actor | fixed_alpha_100 | 0.2879 | 0.1960 | 0.0103 | 1.000 |
| Actor | gcn_pyg | 0.2879 | 0.1960 | 0.0103 | n/a |
| Actor | global_only | 0.3616 | 0.3314 | 0.0067 | n/a |
| Actor | ordinary_gate | 0.3605 | 0.3296 | 0.0043 | n/a |
| Actor | reliability_gate | 0.3601 | 0.3303 | 0.0042 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.5417 | 0.5319 | 0.0602 | 0.667 |
| Chameleon | fixed_alpha_000 | 0.4737 | 0.4563 | 0.0082 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.4978 | 0.4841 | 0.0233 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.5329 | 0.5124 | 0.0716 | 1.000 |
| Chameleon | gcn_pyg | 0.5329 | 0.5124 | 0.0716 | n/a |
| Chameleon | global_only | 0.4737 | 0.4563 | 0.0082 | n/a |
| Chameleon | ordinary_gate | 0.4868 | 0.4713 | 0.0189 | n/a |
| Chameleon | reliability_gate | 0.4868 | 0.4717 | 0.0164 | n/a |
| Cora | best_fixed_alpha_by_val | 0.8023 | 0.7934 | 0.0116 | 1.000 |
| Cora | fixed_alpha_000 | 0.5480 | 0.5251 | 0.0054 | 0.000 |
| Cora | fixed_alpha_050 | 0.6030 | 0.5795 | 0.0278 | 0.500 |
| Cora | fixed_alpha_100 | 0.8023 | 0.7934 | 0.0116 | 1.000 |
| Cora | gcn_pyg | 0.8023 | 0.7934 | 0.0116 | n/a |
| Cora | global_only | 0.5480 | 0.5251 | 0.0054 | n/a |
| Cora | ordinary_gate | 0.5693 | 0.5463 | 0.0118 | n/a |
| Cora | reliability_gate | 0.5707 | 0.5474 | 0.0123 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | fixed_alpha_050 | 0.288 | 0.362 | 0.108 | 0.182 | 0.255 |
| Actor | ordinary_gate | 0.288 | 0.362 | 0.108 | 0.182 | 0.255 |
| Actor | reliability_gate | 0.288 | 0.362 | 0.108 | 0.182 | 0.255 |
| Chameleon | fixed_alpha_050 | 0.533 | 0.474 | 0.207 | 0.148 | 0.317 |
| Chameleon | ordinary_gate | 0.533 | 0.474 | 0.207 | 0.148 | 0.317 |
| Chameleon | reliability_gate | 0.533 | 0.474 | 0.207 | 0.148 | 0.317 |
| Cora | fixed_alpha_050 | 0.802 | 0.548 | 0.309 | 0.055 | 0.276 |
| Cora | ordinary_gate | 0.802 | 0.548 | 0.309 | 0.055 | 0.276 |
| Cora | reliability_gate | 0.802 | 0.548 | 0.309 | 0.055 | 0.276 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Cora | Reliability gate - ordinary gate | +0.0013 | [-0.0015, +0.0042] | 2/1/0 | +0.1835 |
| Cora | ordinary_gate - validation-selected fixed alpha | -0.2330 | [-0.2717, -0.1943] | 0/0/3 | +0.0015 |
| Cora | reliability_gate - validation-selected fixed alpha | -0.2317 | [-0.2690, -0.1943] | 0/0/3 | +0.0014 |
| Cora | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | ordinary_gate - GCN | -0.2330 | [-0.2717, -0.1943] | 0/0/3 | +0.0015 |
| Cora | reliability_gate - GCN | -0.2317 | [-0.2690, -0.1943] | 0/0/3 | +0.0014 |
| Cora | ordinary_gate - fixed_alpha_000 | +0.0213 | [-0.0028, +0.0455] | 3/0/0 | +0.0627 |
| Cora | ordinary_gate - fixed_alpha_050 | -0.0337 | [-0.0976, +0.0303] | 0/0/3 | +0.1517 |
| Cora | ordinary_gate - fixed_alpha_100 | -0.2330 | [-0.2717, -0.1943] | 0/0/3 | +0.0015 |
| Cora | reliability_gate - fixed_alpha_000 | +0.0227 | [-0.0037, +0.0490] | 3/0/0 | +0.0658 |
| Cora | reliability_gate - fixed_alpha_050 | -0.0323 | [-0.0934, +0.0287] | 0/0/3 | +0.1504 |
| Cora | reliability_gate - fixed_alpha_100 | -0.2317 | [-0.2690, -0.1943] | 0/0/3 | +0.0014 |
| Chameleon | Reliability gate - ordinary gate | -0.0000 | [-0.0163, +0.0163] | 1/1/1 | +1.0000 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0548 | [-0.1815, +0.0719] | 0/1/2 | +0.2037 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0548 | [-0.1884, +0.0787] | 0/1/2 | +0.2194 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | ordinary_gate - GCN | -0.0461 | [-0.2085, +0.1164] | 1/0/2 | +0.3468 |
| Chameleon | reliability_gate - GCN | -0.0461 | [-0.2139, +0.1218] | 1/0/2 | +0.3591 |
| Chameleon | ordinary_gate - fixed_alpha_000 | +0.0132 | [-0.0195, +0.0458] | 2/1/0 | +0.2254 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0110 | [-0.0535, +0.0316] | 0/1/2 | +0.3830 |
| Chameleon | ordinary_gate - fixed_alpha_100 | -0.0461 | [-0.2085, +0.1164] | 1/0/2 | +0.3468 |
| Chameleon | reliability_gate - fixed_alpha_000 | +0.0132 | [-0.0151, +0.0415] | 2/1/0 | +0.1835 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0110 | [-0.0413, +0.0194] | 0/1/2 | +0.2601 |
| Chameleon | reliability_gate - fixed_alpha_100 | -0.0461 | [-0.2139, +0.1218] | 1/0/2 | +0.3591 |
| Actor | Reliability gate - ordinary gate | -0.0004 | [-0.0014, +0.0005] | 0/1/2 | +0.1835 |
| Actor | ordinary_gate - validation-selected fixed alpha | -0.0011 | [-0.0086, +0.0065] | 2/0/1 | +0.5958 |
| Actor | reliability_gate - validation-selected fixed alpha | -0.0015 | [-0.0096, +0.0065] | 1/1/1 | +0.4987 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0726 | [+0.0476, +0.0976] | 3/0/0 | +0.0064 |
| Actor | reliability_gate - GCN | +0.0721 | [+0.0462, +0.0981] | 3/0/0 | +0.0069 |
| Actor | ordinary_gate - fixed_alpha_000 | -0.0011 | [-0.0086, +0.0065] | 2/0/1 | +0.5958 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0046 | [+0.0013, +0.0079] | 3/0/0 | +0.0261 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0726 | [+0.0476, +0.0976] | 3/0/0 | +0.0064 |
| Actor | reliability_gate - fixed_alpha_000 | -0.0015 | [-0.0096, +0.0065] | 1/1/1 | +0.4987 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0042 | [+0.0017, +0.0067] | 3/0/0 | +0.0188 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0721 | [+0.0462, +0.0981] | 3/0/0 | +0.0069 |
