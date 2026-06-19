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
| Actor | ordinary_gate | 0.3616 | 0.3307 | 0.0045 | n/a |
| Actor | reliability_gate | 0.3612 | 0.3313 | 0.0048 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.5417 | 0.5319 | 0.0602 | 0.667 |
| Chameleon | fixed_alpha_000 | 0.4737 | 0.4563 | 0.0082 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.4978 | 0.4841 | 0.0233 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.5329 | 0.5124 | 0.0716 | 1.000 |
| Chameleon | gcn_pyg | 0.5329 | 0.5124 | 0.0716 | n/a |
| Chameleon | global_only | 0.4737 | 0.4563 | 0.0082 | n/a |
| Chameleon | ordinary_gate | 0.4949 | 0.4806 | 0.0217 | n/a |
| Chameleon | reliability_gate | 0.4949 | 0.4806 | 0.0217 | n/a |
| Cora | best_fixed_alpha_by_val | 0.8023 | 0.7934 | 0.0116 | 1.000 |
| Cora | fixed_alpha_000 | 0.5480 | 0.5251 | 0.0054 | 0.000 |
| Cora | fixed_alpha_050 | 0.6030 | 0.5795 | 0.0278 | 0.500 |
| Cora | fixed_alpha_100 | 0.8023 | 0.7934 | 0.0116 | 1.000 |
| Cora | gcn_pyg | 0.8023 | 0.7934 | 0.0116 | n/a |
| Cora | global_only | 0.5480 | 0.5251 | 0.0054 | n/a |
| Cora | ordinary_gate | 0.6030 | 0.5795 | 0.0278 | n/a |
| Cora | reliability_gate | 0.6030 | 0.5795 | 0.0278 | n/a |

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
| Cora | Reliability gate - ordinary gate | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | ordinary_gate - validation-selected fixed alpha | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Cora | reliability_gate - validation-selected fixed alpha | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Cora | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | ordinary_gate - GCN | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Cora | reliability_gate - GCN | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Cora | ordinary_gate - fixed_alpha_000 | +0.0550 | [-0.0277, +0.1377] | 3/0/0 | +0.1035 |
| Cora | ordinary_gate - fixed_alpha_050 | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | ordinary_gate - fixed_alpha_100 | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Cora | reliability_gate - fixed_alpha_000 | +0.0550 | [-0.0277, +0.1377] | 3/0/0 | +0.1035 |
| Cora | reliability_gate - fixed_alpha_050 | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | reliability_gate - fixed_alpha_100 | -0.1993 | [-0.2529, -0.1458] | 0/0/3 | +0.0039 |
| Chameleon | Reliability gate - ordinary gate | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0468 | [-0.1836, +0.0900] | 0/1/2 | +0.2789 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0468 | [-0.1836, +0.0900] | 0/1/2 | +0.2789 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | ordinary_gate - GCN | -0.0380 | [-0.2045, +0.1285] | 1/0/2 | +0.4296 |
| Chameleon | reliability_gate - GCN | -0.0380 | [-0.2045, +0.1285] | 1/0/2 | +0.4296 |
| Chameleon | ordinary_gate - fixed_alpha_000 | +0.0212 | [-0.0334, +0.0758] | 2/1/0 | +0.2366 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0029 | [-0.0155, +0.0097] | 0/2/1 | +0.4226 |
| Chameleon | ordinary_gate - fixed_alpha_100 | -0.0380 | [-0.2045, +0.1285] | 1/0/2 | +0.4296 |
| Chameleon | reliability_gate - fixed_alpha_000 | +0.0212 | [-0.0334, +0.0758] | 2/1/0 | +0.2366 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0029 | [-0.0155, +0.0097] | 0/2/1 | +0.4226 |
| Chameleon | reliability_gate - fixed_alpha_100 | -0.0380 | [-0.2045, +0.1285] | 1/0/2 | +0.4296 |
| Actor | Reliability gate - ordinary gate | -0.0004 | [-0.0014, +0.0005] | 0/1/2 | +0.1835 |
| Actor | ordinary_gate - validation-selected fixed alpha | +0.0000 | [-0.0071, +0.0071] | 2/0/1 | +1.0000 |
| Actor | reliability_gate - validation-selected fixed alpha | -0.0004 | [-0.0066, +0.0057] | 2/0/1 | +0.7892 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0737 | [+0.0482, +0.0992] | 3/0/0 | +0.0064 |
| Actor | reliability_gate - GCN | +0.0732 | [+0.0481, +0.0984] | 3/0/0 | +0.0063 |
| Actor | ordinary_gate - fixed_alpha_000 | +0.0000 | [-0.0071, +0.0071] | 2/0/1 | +1.0000 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0057 | [+0.0032, +0.0082] | 3/0/0 | +0.0102 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0737 | [+0.0482, +0.0992] | 3/0/0 | +0.0064 |
| Actor | reliability_gate - fixed_alpha_000 | -0.0004 | [-0.0066, +0.0057] | 2/0/1 | +0.7892 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0053 | [+0.0024, +0.0081] | 3/0/0 | +0.0153 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0732 | [+0.0481, +0.0984] | 3/0/0 | +0.0063 |
