# Expert Fusion Preliminary Analysis

- Edge protocol: source_to_target
- Runs: 3
- Models: gcn_pyg, global_only, ordinary_gate, reliability_gate, fixed_alpha_000, fixed_alpha_050, fixed_alpha_100, best_fixed_alpha_by_val

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.3592 | 0.3268 | 0.0092 | 0.167 |
| Actor | fixed_alpha_000 | 0.3616 | 0.3314 | 0.0067 | 0.000 |
| Actor | fixed_alpha_050 | 0.3583 | 0.3165 | 0.0098 | 0.500 |
| Actor | fixed_alpha_100 | 0.2888 | 0.2173 | 0.0107 | 1.000 |
| Actor | gcn_pyg | 0.2888 | 0.2173 | 0.0107 | n/a |
| Actor | global_only | 0.3616 | 0.3314 | 0.0067 | n/a |
| Actor | ordinary_gate | 0.3607 | 0.3295 | 0.0069 | n/a |
| Actor | reliability_gate | 0.3612 | 0.3302 | 0.0070 | n/a |
| Chameleon | best_fixed_alpha_by_val | 0.4751 | 0.4564 | 0.0072 | 0.333 |
| Chameleon | fixed_alpha_000 | 0.4737 | 0.4563 | 0.0082 | 0.000 |
| Chameleon | fixed_alpha_050 | 0.4744 | 0.4553 | 0.0063 | 0.500 |
| Chameleon | fixed_alpha_100 | 0.4306 | 0.4110 | 0.0166 | 1.000 |
| Chameleon | gcn_pyg | 0.4306 | 0.4110 | 0.0166 | n/a |
| Chameleon | global_only | 0.4737 | 0.4563 | 0.0082 | n/a |
| Chameleon | ordinary_gate | 0.4715 | 0.4534 | 0.0117 | n/a |
| Chameleon | reliability_gate | 0.4722 | 0.4538 | 0.0109 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | best_fixed_alpha_by_val | 0.282 | 0.362 | 0.121 | 0.195 | 0.271 |
| Actor | fixed_alpha_050 | 0.289 | 0.362 | 0.120 | 0.193 | 0.271 |
| Actor | ordinary_gate | 0.289 | 0.362 | 0.120 | 0.193 | 0.271 |
| Actor | reliability_gate | 0.289 | 0.362 | 0.120 | 0.193 | 0.271 |
| Chameleon | best_fixed_alpha_by_val | 0.435 | 0.474 | 0.157 | 0.190 | 0.335 |
| Chameleon | fixed_alpha_050 | 0.431 | 0.474 | 0.149 | 0.192 | 0.337 |
| Chameleon | ordinary_gate | 0.431 | 0.474 | 0.149 | 0.192 | 0.337 |
| Chameleon | reliability_gate | 0.431 | 0.474 | 0.149 | 0.192 | 0.337 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
| Chameleon | Reliability gate - ordinary gate | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | ordinary_gate - validation-selected fixed alpha | -0.0037 | [-0.0288, +0.0215] | 2/0/1 | +0.5958 |
| Chameleon | reliability_gate - validation-selected fixed alpha | -0.0029 | [-0.0249, +0.0191] | 2/0/1 | +0.6254 |
| Chameleon | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | ordinary_gate - GCN | +0.0409 | [-0.0217, +0.1036] | 3/0/0 | +0.1067 |
| Chameleon | reliability_gate - GCN | +0.0417 | [-0.0212, +0.1045] | 3/0/0 | +0.1040 |
| Chameleon | ordinary_gate - fixed_alpha_000 | -0.0022 | [-0.0131, +0.0087] | 1/0/2 | +0.4778 |
| Chameleon | ordinary_gate - fixed_alpha_050 | -0.0029 | [-0.0298, +0.0239] | 2/0/1 | +0.6857 |
| Chameleon | ordinary_gate - fixed_alpha_100 | +0.0409 | [-0.0217, +0.1036] | 3/0/0 | +0.1067 |
| Chameleon | reliability_gate - fixed_alpha_000 | -0.0015 | [-0.0098, +0.0069] | 1/0/2 | +0.5286 |
| Chameleon | reliability_gate - fixed_alpha_050 | -0.0022 | [-0.0259, +0.0216] | 2/0/1 | +0.7295 |
| Chameleon | reliability_gate - fixed_alpha_100 | +0.0417 | [-0.0212, +0.1045] | 3/0/0 | +0.1040 |
| Actor | Reliability gate - ordinary gate | +0.0004 | [-0.0005, +0.0014] | 2/1/0 | +0.1835 |
| Actor | ordinary_gate - validation-selected fixed alpha | +0.0015 | [-0.0079, +0.0110] | 1/0/2 | +0.5564 |
| Actor | reliability_gate - validation-selected fixed alpha | +0.0020 | [-0.0080, +0.0119] | 1/1/1 | +0.4830 |
| Actor | alpha=0 fallback - global expert | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | alpha=1 fallback - GCN | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Actor | ordinary_gate - GCN | +0.0719 | [+0.0588, +0.0850] | 3/0/0 | +0.0018 |
| Actor | reliability_gate - GCN | +0.0724 | [+0.0600, +0.0847] | 3/0/0 | +0.0016 |
| Actor | ordinary_gate - fixed_alpha_000 | -0.0009 | [-0.0018, +0.0001] | 0/0/3 | +0.0572 |
| Actor | ordinary_gate - fixed_alpha_050 | +0.0024 | [-0.0066, +0.0114] | 2/0/1 | +0.3681 |
| Actor | ordinary_gate - fixed_alpha_100 | +0.0719 | [+0.0588, +0.0850] | 3/0/0 | +0.0018 |
| Actor | reliability_gate - fixed_alpha_000 | -0.0004 | [-0.0014, +0.0005] | 0/1/2 | +0.1835 |
| Actor | reliability_gate - fixed_alpha_050 | +0.0029 | [-0.0062, +0.0119] | 2/0/1 | +0.3061 |
| Actor | reliability_gate - fixed_alpha_100 | +0.0724 | [+0.0600, +0.0847] | 3/0/0 | +0.0016 |
