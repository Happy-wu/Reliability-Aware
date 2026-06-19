# Expert Fusion Preliminary Analysis

- Edge protocol: source_to_target
- Runs: 10
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_050, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3539 | 0.3211 | 0.0122 | 0.050 |
| Actor | fixed_alpha_000 | 0.3526 | 0.3207 | 0.0124 | 0.000 |
| Actor | fixed_alpha_050 | 0.3512 | 0.3121 | 0.0124 | 0.500 |
| Actor | fixed_alpha_100 | 0.2844 | 0.2293 | 0.0107 | 1.000 |
| Actor | gcn_pyg | 0.2844 | 0.2293 | 0.0107 | n/a |
| Actor | global_only | 0.3526 | 0.3207 | 0.0124 | n/a |
| Actor | ordinary_gate | 0.3526 | 0.3204 | 0.0127 | n/a |
| Actor | reliability_gate | 0.3553 | 0.3223 | 0.0117 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.4759 | 0.4638 | 0.0197 | 0.400 |
| Chameleon | fixed_alpha_000 | 0.4750 | 0.4634 | 0.0216 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.4750 | 0.4628 | 0.0213 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.4268 | 0.4144 | 0.0183 | 1.000 |
| Chameleon | gcn_pyg | 0.4268 | 0.4144 | 0.0183 | n/a |
| Chameleon | global_only | 0.4750 | 0.4634 | 0.0216 | n/a |
| Chameleon | ordinary_gate | 0.4748 | 0.4625 | 0.0203 | n/a |
| Chameleon | reliability_gate | 0.4746 | 0.4624 | 0.0200 | n/a |
| Squirrel | best_fixed_alpha_by_val | 0.3091 | 0.3004 | 0.0189 | 0.400 |
| Squirrel | fixed_alpha_000 | 0.3096 | 0.2999 | 0.0184 | 0.000 |
| Squirrel | fixed_alpha_050 | 0.3110 | 0.3018 | 0.0201 | 0.500 |
| Squirrel | fixed_alpha_100 | 0.2891 | 0.2840 | 0.0169 | 1.000 |
| Squirrel | gcn_pyg | 0.2891 | 0.2840 | 0.0169 | n/a |
| Squirrel | global_only | 0.3096 | 0.2999 | 0.0184 | n/a |
| Squirrel | ordinary_gate | 0.3102 | 0.3009 | 0.0189 | n/a |
| Squirrel | reliability_gate | 0.3102 | 0.3009 | 0.0191 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.276 | 0.353 | 0.119 | 0.188 | 0.259 |
| Actor | fixed_alpha_050 | 0.284 | 0.353 | 0.122 | 0.190 | 0.266 |
| Actor | ordinary_gate | 0.284 | 0.353 | 0.122 | 0.190 | 0.266 |
| Actor | reliability_gate | 0.284 | 0.353 | 0.122 | 0.190 | 0.266 |
| Chameleon | best_fixed_alpha_by_val | 0.428 | 0.475 | 0.161 | 0.212 | 0.371 |
| Chameleon | fixed_alpha_050 | 0.427 | 0.475 | 0.163 | 0.211 | 0.368 |
| Chameleon | ordinary_gate | 0.427 | 0.475 | 0.163 | 0.211 | 0.368 |
| Chameleon | reliability_gate | 0.427 | 0.475 | 0.163 | 0.211 | 0.368 |
| Squirrel | best_fixed_alpha_by_val | 0.285 | 0.309 | 0.141 | 0.168 | 0.233 |
| Squirrel | fixed_alpha_050 | 0.289 | 0.310 | 0.146 | 0.167 | 0.234 |
| Squirrel | ordinary_gate | 0.289 | 0.310 | 0.146 | 0.167 | 0.234 |
| Squirrel | reliability_gate | 0.289 | 0.310 | 0.146 | 0.167 | 0.234 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Chameleon | Reliability gate - ordinary gate | -0.0002 | [-0.0011, +0.0007] | 1/7/2 | +0.5911 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0011 | [-0.0037, +0.0015] | 1/7/2 | +0.3629 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0013 | [-0.0038, +0.0012] | 0/8/2 | +0.2598 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Chameleon | ordinary_gate - GCN | +0.0480 | [+0.0304, +0.0656] | 10/0/0 | +0.0002 |
| Chameleon | reliability_gate - GCN | +0.0478 | [+0.0308, +0.0648] | 10/0/0 | +0.0001 |
| Chameleon | ordinary_gate - fixed_alpha_000 | -0.0002 | [-0.0049, +0.0045] | 4/2/4 | +0.9183 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0002 | [-0.0035, +0.0030] | 2/6/2 | +0.8825 |
| Chameleon | ordinary_gate - fixed_alpha_100 | +0.0480 | [+0.0304, +0.0656] | 10/0/0 | +0.0002 |
| Chameleon | reliability_gate - fixed_alpha_000 | -0.0004 | [-0.0050, +0.0041] | 3/2/5 | +0.8321 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0004 | [-0.0036, +0.0027] | 2/6/2 | +0.7577 |
| Chameleon | reliability_gate - fixed_alpha_100 | +0.0478 | [+0.0308, +0.0648] | 10/0/0 | +0.0001 |
| Squirrel | Reliability gate - ordinary gate | +0.0000 | [-0.0003, +0.0003] | 1/8/1 | +1.0000 |
| Squirrel | ordinary_gate - validation-selected fixed alpha | +0.0011 | [-0.0026, +0.0047] | 2/5/3 | +0.5328 |
| Squirrel | reliability_gate - validation-selected fixed alpha | +0.0011 | [-0.0026, +0.0048] | 3/3/4 | +0.5344 |
| Squirrel | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Squirrel | ordinary_gate - GCN | +0.0210 | [+0.0050, +0.0371] | 7/0/3 | +0.0159 |
| Squirrel | reliability_gate - GCN | +0.0210 | [+0.0048, +0.0373] | 7/0/3 | +0.0167 |
| Squirrel | ordinary_gate - fixed_alpha_000 | +0.0006 | [-0.0015, +0.0026] | 4/3/3 | +0.5414 |
| Squirrel | ordinary_gate - fixed_alpha_050 | -0.0008 | [-0.0021, +0.0006] | 2/5/3 | +0.2229 |
| Squirrel | ordinary_gate - fixed_alpha_100 | +0.0210 | [+0.0050, +0.0371] | 7/0/3 | +0.0159 |
| Squirrel | reliability_gate - fixed_alpha_000 | +0.0006 | [-0.0015, +0.0027] | 5/1/4 | +0.5462 |
| Squirrel | reliability_gate - fixed_alpha_050 | -0.0008 | [-0.0019, +0.0003] | 1/6/3 | +0.1527 |
| Squirrel | reliability_gate - fixed_alpha_100 | +0.0210 | [+0.0048, +0.0373] | 7/0/3 | +0.0167 |
| Actor | Reliability gate - ordinary gate | +0.0027 | [-0.0004, +0.0058] | 7/1/2 | +0.0800 |
| Actor | ordinary_gate - validation-selected fixed alpha | -0.0013 | [-0.0029, +0.0003] | 1/2/7 | +0.0985 |
| Actor | reliability_gate - validation-selected fixed alpha | +0.0014 | [-0.0009, +0.0036] | 5/1/4 | +0.1974 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0682 | [+0.0624, +0.0740] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - GCN | +0.0709 | [+0.0641, +0.0777] | 10/0/0 | +0.0000 |
| Actor | ordinary_gate - fixed_alpha_000 | +0.0000 | [-0.0021, +0.0021] | 2/2/6 | +1.0000 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0014 | [-0.0016, +0.0045] | 6/0/4 | +0.3143 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0682 | [+0.0624, +0.0740] | 10/0/0 | +0.0000 |
| Actor | reliability_gate - fixed_alpha_000 | +0.0027 | [-0.0004, +0.0058] | 6/1/3 | +0.0840 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0041 | [-0.0003, +0.0086] | 7/0/3 | +0.0635 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0709 | [+0.0641, +0.0777] | 10/0/0 | +0.0000 |
