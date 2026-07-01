# Expert Fusion Preliminary Analysis

- Edge protocol: undirected
- Runs: 10
- Models: reliability_gate

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | reliability_gate | 0.3541 | 0.3226 | 0.0123 | n/a |
| Chameleon | reliability_gate | 0.5759 | 0.5711 | 0.0379 | n/a |
| Citeseer | reliability_gate | 0.5575 | 0.5246 | 0.0513 | n/a |
| Cora | reliability_gate | 0.6389 | 0.6201 | 0.0624 | n/a |
| Pubmed | reliability_gate | 0.7331 | 0.7351 | 0.0123 | n/a |
| Squirrel | reliability_gate | 0.3566 | 0.3480 | 0.0307 | n/a |

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
