# Expert Fusion Preliminary Analysis

- Edge protocol: undirected
- Runs: 3
- Models: reliability_gate

## Accuracy Summary

| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |
|---|---|---:|---:|---:|---:|
| Actor | reliability_gate | 0.3603 | 0.3289 | 0.0050 | n/a |
| Chameleon | reliability_gate | 0.4854 | 0.4696 | 0.0204 | n/a |
| Cora | reliability_gate | 0.5697 | 0.5467 | 0.0123 | n/a |

## Expert Complementarity

| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |
|---|---|---:|---:|---:|---:|---:|
| Actor | reliability_gate | 0.288 | 0.362 | 0.108 | 0.182 | 0.255 |
| Chameleon | reliability_gate | 0.533 | 0.474 | 0.207 | 0.148 | 0.317 |
| Cora | reliability_gate | 0.802 | 0.548 | 0.309 | 0.055 | 0.276 |

## Key Paired Comparisons

| Dataset | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---:|---:|---:|---:|
