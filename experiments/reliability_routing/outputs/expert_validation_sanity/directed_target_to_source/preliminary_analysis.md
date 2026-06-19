# Expert Fusion Preliminary Analysis

- Edge protocol: target_to_source
- Runs: 3
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_050, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3616 | 0.3314 | 0.0067 | 0.000 |
| Actor | fixed_alpha_000 | 0.3616 | 0.3314 | 0.0067 | 0.000 |
| Actor | fixed_alpha_050 | 0.3498 | 0.3076 | 0.0040 | 0.500 |
| Actor | fixed_alpha_100 | 0.2750 | 0.1951 | 0.0048 | 1.000 |
| Actor | gcn_pyg | 0.2750 | 0.1951 | 0.0048 | n/a |
| Actor | global_only | 0.3616 | 0.3314 | 0.0067 | n/a |
| Actor | ordinary_gate | 0.3599 | 0.3256 | 0.0065 | n/a |
| Actor | reliability_gate | 0.3625 | 0.3306 | 0.0054 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.5607 | 0.5510 | 0.0238 | 1.000 |
| Chameleon | fixed_alpha_000 | 0.4737 | 0.4563 | 0.0082 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.5234 | 0.5141 | 0.0055 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.5607 | 0.5510 | 0.0238 | 1.000 |
| Chameleon | gcn_pyg | 0.5607 | 0.5510 | 0.0238 | n/a |
| Chameleon | global_only | 0.4737 | 0.4563 | 0.0082 | n/a |
| Chameleon | ordinary_gate | 0.5161 | 0.5046 | 0.0055 | n/a |
| Chameleon | reliability_gate | 0.5168 | 0.5060 | 0.0058 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | fixed_alpha_050 | 0.275 | 0.362 | 0.120 | 0.207 | 0.285 |
| Actor | ordinary_gate | 0.275 | 0.362 | 0.120 | 0.207 | 0.285 |
| Actor | reliability_gate | 0.275 | 0.362 | 0.120 | 0.207 | 0.285 |
| Chameleon | fixed_alpha_050 | 0.561 | 0.474 | 0.233 | 0.146 | 0.332 |
| Chameleon | ordinary_gate | 0.561 | 0.474 | 0.233 | 0.146 | 0.332 |
| Chameleon | reliability_gate | 0.561 | 0.474 | 0.233 | 0.146 | 0.332 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Chameleon | Reliability gate - ordinary gate | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0446 | [-0.1171, +0.0280] | 0/0/3 | +0.1182 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0439 | [-0.1195, +0.0318] | 0/0/3 | +0.1302 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | ordinary_gate - GCN | -0.0446 | [-0.1171, +0.0280] | 0/0/3 | +0.1182 |
| Chameleon | reliability_gate - GCN | -0.0439 | [-0.1195, +0.0318] | 0/0/3 | +0.1302 |
| Chameleon | ordinary_gate - fixed_alpha_000 | +0.0424 | [+0.0204, +0.0644] | 3/0/0 | +0.0143 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0073 | [-0.0240, +0.0093] | 0/1/2 | +0.1994 |
| Chameleon | ordinary_gate - fixed_alpha_100 | -0.0446 | [-0.1171, +0.0280] | 0/0/3 | +0.1182 |
| Chameleon | reliability_gate - fixed_alpha_000 | +0.0431 | [+0.0180, +0.0683] | 3/0/0 | +0.0179 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0066 | [-0.0262, +0.0131] | 1/0/2 | +0.2863 |
| Chameleon | reliability_gate - fixed_alpha_100 | -0.0439 | [-0.1195, +0.0318] | 0/0/3 | +0.1302 |
| Actor | Reliability gate - ordinary gate | +0.0026 | [-0.0087, +0.0140] | 1/2/0 | +0.4226 |
| Actor | ordinary_gate - validation-selected fixed alpha | -0.0018 | [-0.0059, +0.0024] | 0/1/2 | +0.2079 |
| Actor | reliability_gate - validation-selected fixed alpha | +0.0009 | [-0.0075, +0.0093] | 1/1/1 | +0.6968 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0849 | [+0.0509, +0.1189] | 3/0/0 | +0.0086 |
| Actor | reliability_gate - GCN | +0.0875 | [+0.0570, +0.1180] | 3/0/0 | +0.0065 |
| Actor | ordinary_gate - fixed_alpha_000 | -0.0018 | [-0.0059, +0.0024] | 0/1/2 | +0.2079 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0101 | [+0.0020, +0.0181] | 3/0/0 | +0.0328 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0849 | [+0.0509, +0.1189] | 3/0/0 | +0.0086 |
| Actor | reliability_gate - fixed_alpha_000 | +0.0009 | [-0.0075, +0.0093] | 1/1/1 | +0.6968 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0127 | [+0.0018, +0.0236] | 3/0/0 | +0.0373 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0875 | [+0.0570, +0.1180] | 3/0/0 | +0.0065 |
