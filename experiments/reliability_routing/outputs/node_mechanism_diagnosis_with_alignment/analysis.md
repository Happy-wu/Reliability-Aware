# Node Mechanism Diagnosis

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Controls: reliability_only, combined, fixed
- Node diagnostics dir: `outputs/iter_relation_mechanism_v1/_node_diagnostics`

## Group Summary

| Dataset | Family | Control | n | Align avail | Alpha AUC | Alpha corr(local advantage) | Alpha gap(local-global) | High-alpha local pref rate | Low-alpha global pref rate | Alpha corr degree | Alpha corr variance | Alpha corr rwse |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 10 | 1.0000 | 0.4941 | 0.0370 | -0.0000 | 0.6421 | 0.3610 | -0.2401 | 0.1275 | -0.5900 |
| Amazon-ratings | iterative_relation_finetune | fixed | 10 | 1.0000 | 0.5000 | n/a | 0.0000 | 0.6617 | 0.3383 | n/a | n/a | n/a |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 10 | 1.0000 | 0.5238 | 0.0218 | 0.0006 | 0.7049 | 0.3301 | -0.1663 | 0.1276 | -0.5889 |
| Amazon-ratings | iterative_relation_frozen | combined | 10 | 1.0000 | 0.4801 | 0.0871 | -0.0000 | 0.6690 | 0.3391 | -0.1018 | 0.2179 | -0.1714 |
| Amazon-ratings | iterative_relation_frozen | fixed | 10 | 1.0000 | 0.5000 | n/a | 0.0000 | 0.6617 | 0.3383 | n/a | n/a | n/a |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 10 | 1.0000 | 0.5095 | 0.0973 | -0.0000 | 0.6643 | 0.3274 | -0.1300 | 0.1436 | -0.1984 |
| Roman-empire | iterative_relation_finetune | combined | 10 | 1.0000 | 0.5832 | 0.0810 | 0.0010 | 0.1972 | 0.8966 | 0.2905 | 0.1840 | 0.0635 |
| Roman-empire | iterative_relation_finetune | fixed | 10 | 1.0000 | 0.5000 | n/a | 0.0000 | 0.1455 | 0.8545 | n/a | n/a | n/a |
| Roman-empire | iterative_relation_finetune | reliability_only | 10 | 1.0000 | 0.5439 | 0.0229 | 0.0005 | 0.1716 | 0.8809 | 0.2977 | 0.0908 | 0.0043 |
| Roman-empire | iterative_relation_frozen | combined | 10 | 1.0000 | 0.5620 | 0.0747 | 0.0013 | 0.1805 | 0.8883 | 0.2915 | 0.2569 | 0.0816 |
| Roman-empire | iterative_relation_frozen | fixed | 10 | 1.0000 | 0.5000 | n/a | 0.0000 | 0.1455 | 0.8545 | n/a | n/a | n/a |
| Roman-empire | iterative_relation_frozen | reliability_only | 10 | 1.0000 | 0.5251 | 0.0266 | 0.0004 | 0.1669 | 0.8617 | 0.2319 | 0.1370 | 0.0159 |

## Takeaways

- Interpret `Roman-empire` and `Amazon-ratings` side by side using the chain `headroom -> separability -> alpha alignment -> accuracy gain`.
- `Align avail` reports whether external local/global expert logits were successfully recovered for the group.
- If `Align avail` is below 1.0000, treat preference-alignment metrics as partially observed for that group.
- `alpha_auc_for_local_preference` and `alpha_corr_local_advantage` are the primary node-level alignment metrics.
- `high_alpha_local_preference_rate` and `low_alpha_global_preference_rate` summarize whether extreme alpha buckets match expert preference.
- `alpha_corr_degree_test`, `alpha_corr_neighbor_variance_test`, and `alpha_corr_rwse_test` summarize structural association on test nodes.
- Treat `fixed` mainly as a sanity baseline: its constant alpha is useful for confirming the absence of node-level routing information, not as mechanism evidence.
- Extremely large `relation_to_base_norm` values should be treated as unstable ratio diagnostics rather than publication-ready evidence.
