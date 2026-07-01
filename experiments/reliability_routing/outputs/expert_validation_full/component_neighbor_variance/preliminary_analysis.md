# Expert Fusion Preliminary Analysis

- Edge protocol: undirected
- Runs: 10
- Models: reliability_gate

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | reliability_gate | 0.3539 | 0.3211 | 0.0117 | n/a |
| Chameleon | reliability_gate | 0.5730 | 0.5687 | 0.0343 | n/a |
| Citeseer | reliability_gate | 0.5577 | 0.5254 | 0.0518 | n/a |
| Cora | reliability_gate | 0.6389 | 0.6201 | 0.0624 | n/a |
| Pubmed | reliability_gate | 0.7324 | 0.7343 | 0.0127 | n/a |
| Squirrel | reliability_gate | 0.3554 | 0.3465 | 0.0290 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | reliability_gate | 0.304 | 0.353 | 0.120 | 0.170 | 0.243 |
| Chameleon | reliability_gate | 0.644 | 0.475 | 0.269 | 0.100 | 0.281 |
| Citeseer | reliability_gate | 0.693 | 0.517 | 0.252 | 0.077 | 0.249 |
| Cora | reliability_gate | 0.812 | 0.545 | 0.317 | 0.050 | 0.267 |
| Pubmed | reliability_gate | 0.769 | 0.704 | 0.138 | 0.073 | 0.317 |
| Squirrel | reliability_gate | 0.474 | 0.310 | 0.286 | 0.122 | 0.232 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
