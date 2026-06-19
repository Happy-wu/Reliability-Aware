# Expert Fusion Preliminary Analysis

- Edge protocol: target_to_source
- Runs: 10
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_050, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3526 | 0.3207 | 0.0124 | 0.000 |
| Actor | fixed_alpha_000 | 0.3526 | 0.3207 | 0.0124 | 0.000 |
| Actor | fixed_alpha_050 | 0.3480 | 0.3062 | 0.0099 | 0.500 |
| Actor | fixed_alpha_100 | 0.2748 | 0.1944 | 0.0142 | 1.000 |
| Actor | gcn_pyg | 0.2748 | 0.1944 | 0.0142 | n/a |
| Actor | global_only | 0.3526 | 0.3207 | 0.0124 | n/a |
| Actor | ordinary_gate | 0.3518 | 0.3180 | 0.0125 | n/a |
| Actor | reliability_gate | 0.3524 | 0.3185 | 0.0130 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.6643 | 0.6652 | 0.0186 | 1.000 |
| Chameleon | fixed_alpha_000 | 0.4750 | 0.4634 | 0.0216 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.5932 | 0.5881 | 0.0394 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.6643 | 0.6652 | 0.0186 | 1.000 |
| Chameleon | gcn_pyg | 0.6643 | 0.6652 | 0.0186 | n/a |
| Chameleon | global_only | 0.4750 | 0.4634 | 0.0216 | n/a |
| Chameleon | ordinary_gate | 0.5928 | 0.5876 | 0.0393 | n/a |
| Chameleon | reliability_gate | 0.5901 | 0.5854 | 0.0364 | n/a |
| Squirrel | best_fixed_alpha_by_val | 0.5193 | 0.5129 | 0.0085 | 1.000 |
| Squirrel | fixed_alpha_000 | 0.3096 | 0.2999 | 0.0184 | 0.000 |
| Squirrel | fixed_alpha_050 | 0.3744 | 0.3645 | 0.0399 | 0.500 |
| Squirrel | fixed_alpha_100 | 0.5193 | 0.5129 | 0.0085 | 1.000 |
| Squirrel | gcn_pyg | 0.5193 | 0.5129 | 0.0085 | n/a |
| Squirrel | global_only | 0.3096 | 0.2999 | 0.0184 | n/a |
| Squirrel | ordinary_gate | 0.3714 | 0.3629 | 0.0367 | n/a |
| Squirrel | reliability_gate | 0.3737 | 0.3652 | 0.0392 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | fixed_alpha_050 | 0.275 | 0.353 | 0.125 | 0.203 | 0.280 |
| Actor | ordinary_gate | 0.275 | 0.353 | 0.125 | 0.203 | 0.280 |
| Actor | reliability_gate | 0.275 | 0.353 | 0.125 | 0.203 | 0.280 |
| Chameleon | fixed_alpha_050 | 0.664 | 0.475 | 0.287 | 0.097 | 0.290 |
| Chameleon | ordinary_gate | 0.664 | 0.475 | 0.287 | 0.097 | 0.290 |
| Chameleon | reliability_gate | 0.664 | 0.475 | 0.287 | 0.097 | 0.290 |
| Squirrel | fixed_alpha_050 | 0.519 | 0.310 | 0.322 | 0.113 | 0.234 |
| Squirrel | ordinary_gate | 0.519 | 0.310 | 0.322 | 0.113 | 0.234 |
| Squirrel | reliability_gate | 0.519 | 0.310 | 0.322 | 0.113 | 0.234 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Chameleon | Reliability gate - ordinary gate | -0.0026 | [-0.0076, +0.0023] | 0/8/2 | +0.2598 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0715 | [-0.0978, -0.0452] | 1/0/9 | +0.0002 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0741 | [-0.0969, -0.0513] | 0/0/10 | +0.0000 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | ordinary_gate - GCN | -0.0715 | [-0.0978, -0.0452] | 1/0/9 | +0.0002 |
| Chameleon | reliability_gate - GCN | -0.0741 | [-0.0969, -0.0513] | 0/0/10 | +0.0000 |
| Chameleon | ordinary_gate - fixed_alpha_000 | +0.1178 | [+0.0944, +0.1411] | 10/0/0 | +0.0000 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0004 | [-0.0014, +0.0006] | 0/9/1 | +0.3434 |
| Chameleon | ordinary_gate - fixed_alpha_100 | -0.0715 | [-0.0978, -0.0452] | 1/0/9 | +0.0002 |
| Chameleon | reliability_gate - fixed_alpha_000 | +0.1151 | [+0.0923, +0.1380] | 10/0/0 | +0.0000 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0031 | [-0.0082, +0.0021] | 0/8/2 | +0.2091 |
| Chameleon | reliability_gate - fixed_alpha_100 | -0.0741 | [-0.0969, -0.0513] | 0/0/10 | +0.0000 |
| Squirrel | Reliability gate - ordinary gate | +0.0023 | [-0.0012, +0.0058] | 2/8/0 | +0.1695 |
| Squirrel | ordinary_gate - validation-selected fixed alpha | -0.1479 | [-0.1706, -0.1253] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - validation-selected fixed alpha | -0.1456 | [-0.1704, -0.1209] | 0/0/10 | +0.0000 |
| Squirrel | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | ordinary_gate - GCN | -0.1479 | [-0.1706, -0.1253] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - GCN | -0.1456 | [-0.1704, -0.1209] | 0/0/10 | +0.0000 |
| Squirrel | ordinary_gate - fixed_alpha_000 | +0.0618 | [+0.0416, +0.0819] | 10/0/0 | +0.0001 |
| Squirrel | ordinary_gate - fixed_alpha_050 | -0.0031 | [-0.0079, +0.0017] | 0/8/2 | +0.1825 |
| Squirrel | ordinary_gate - fixed_alpha_100 | -0.1479 | [-0.1706, -0.1253] | 0/0/10 | +0.0000 |
| Squirrel | reliability_gate - fixed_alpha_000 | +0.0641 | [+0.0413, +0.0868] | 10/0/0 | +0.0001 |
| Squirrel | reliability_gate - fixed_alpha_050 | -0.0008 | [-0.0028, +0.0012] | 1/8/1 | +0.4054 |
| Squirrel | reliability_gate - fixed_alpha_100 | -0.1456 | [-0.1704, -0.1209] | 0/0/10 | +0.0000 |
| Actor | Reliability gate - ordinary gate | +0.0006 | [-0.0006, +0.0018] | 4/5/1 | +0.2869 |
| Actor | ordinary_gate - validation-selected fixed alpha | -0.0008 | [-0.0038, +0.0023] | 4/1/5 | +0.5724 |
| Actor | reliability_gate - validation-selected fixed alpha | -0.0002 | [-0.0025, +0.0021] | 4/1/5 | +0.8528 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0770 | [+0.0653, +0.0888] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - GCN | +0.0776 | [+0.0657, +0.0895] | 10/0/0 | +0.0000 |
| Actor | ordinary_gate - fixed_alpha_000 | -0.0008 | [-0.0038, +0.0023] | 4/1/5 | +0.5724 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0038 | [-0.0002, +0.0079] | 6/0/4 | +0.0611 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0770 | [+0.0653, +0.0888] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - fixed_alpha_000 | -0.0002 | [-0.0025, +0.0021] | 4/1/5 | +0.8528 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0044 | [-0.0002, +0.0090] | 6/0/4 | +0.0579 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0776 | [+0.0657, +0.0895] | 10/0/0 | +0.0000 |
