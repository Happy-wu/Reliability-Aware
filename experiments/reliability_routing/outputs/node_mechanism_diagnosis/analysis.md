# Node Mechanism Diagnosis

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Controls: reliability_only, combined, fixed
- Node diagnostics dir: `outputs/iter_relation_mechanism_v1/_node_diagnostics`

## Group Summary

| Dataset | Family | Control | n | Align avail | Alpha AUC | Alpha corr(local advantage) | Alpha gap(local-global) | High-alpha local pref rate | Low-alpha global pref rate | Alpha corr degree | Alpha corr variance | Alpha corr rwse |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | -0.2401 | 0.1275 | -0.5900 |
| Amazon-ratings | iterative_relation_finetune | fixed | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | -0.1663 | 0.1276 | -0.5889 |
| Amazon-ratings | iterative_relation_frozen | combined | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | -0.1018 | 0.2179 | -0.1714 |
| Amazon-ratings | iterative_relation_frozen | fixed | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | -0.1300 | 0.1436 | -0.1984 |
| Roman-empire | iterative_relation_finetune | combined | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | 0.2905 | 0.1840 | 0.0635 |
| Roman-empire | iterative_relation_finetune | fixed | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Roman-empire | iterative_relation_finetune | reliability_only | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | 0.2977 | 0.0908 | 0.0043 |
| Roman-empire | iterative_relation_frozen | combined | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | 0.2915 | 0.2569 | 0.0816 |
| Roman-empire | iterative_relation_frozen | fixed | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Roman-empire | iterative_relation_frozen | reliability_only | 10 | 0.0000 | n/a | n/a | n/a | n/a | n/a | 0.2319 | 0.1370 | 0.0159 |

## Takeaways

- Interpret `Roman-empire` and `Amazon-ratings` side by side using the chain `headroom -> separability -> alpha alignment -> accuracy gain`.
- `Align avail` reports whether external local/global expert logits were successfully recovered for the group.
- If `Align avail` is below 1.0000, treat preference-alignment metrics as partially observed for that group.
- `alpha_auc_for_local_preference` and `alpha_corr_local_advantage` are the primary node-level alignment metrics.
- `high_alpha_local_preference_rate` and `low_alpha_global_preference_rate` summarize whether extreme alpha buckets match expert preference.
- `alpha_corr_degree_test`, `alpha_corr_neighbor_variance_test`, and `alpha_corr_rwse_test` summarize structural association on test nodes.
- Treat `fixed` mainly as a sanity baseline: its constant alpha is useful for confirming the absence of node-level routing information, not as mechanism evidence.
- Extremely large `relation_to_base_norm` values should be treated as unstable ratio diagnostics rather than publication-ready evidence.
