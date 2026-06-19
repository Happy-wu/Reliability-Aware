# Preference Routing Diagnostic

Primary question: can reliability predict which frozen expert is correct?

## Summary

| Dataset | Router | Valid/Total | Status | Preference nodes | AUC [95% CI] | Balanced acc | Routing acc | Routed node acc |
|---|---|---:|---|---:|---:|---:|---:|---:|
| Actor | reliability_only | 1/1 | ok:1 | 461.0 | 0.5414 [0.5414, 0.5414] | 0.5269 | 0.5813 | 0.3408 |
| Actor | node_feature_only | 1/1 | ok:1 | 461.0 | 0.5605 [0.5605, 0.5605] | 0.5595 | 0.5965 | 0.3454 |
| Actor | combined | 1/1 | ok:1 | 461.0 | 0.5408 [0.5408, 0.5408] | 0.5280 | 0.5597 | 0.3342 |
| Chameleon | reliability_only | 1/1 | ok:1 | 175.0 | 0.6161 [0.6161, 0.6161] | 0.5857 | 0.6000 | 0.5482 |
| Chameleon | node_feature_only | 1/1 | ok:1 | 175.0 | 0.5224 [0.5224, 0.5224] | 0.5143 | 0.5086 | 0.5132 |
| Chameleon | combined | 1/1 | ok:1 | 175.0 | 0.5751 [0.5751, 0.5751] | 0.5571 | 0.5657 | 0.5351 |
| Roman-empire | reliability_only | 1/1 | ok:1 | 2974.0 | 0.8049 [0.8049, 0.8049] | 0.7071 | 0.5646 | 0.4361 |
| Roman-empire | node_feature_only | 1/1 | ok:1 | 2974.0 | 0.8388 [0.8388, 0.8388] | 0.6971 | 0.8157 | 0.5679 |
| Roman-empire | combined | 1/1 | ok:1 | 2974.0 | 0.8683 [0.8683, 0.8683] | 0.7817 | 0.8393 | 0.5803 |

## Paired Comparisons

| Dataset | Comparison | Metric | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Chameleon | reliability_only - node_feature_only | test_preference_auc | 1 | 0.0936 | [0.0936, 0.0936] | 1/0/0 |
| Chameleon | reliability_only - node_feature_only | test_balanced_accuracy | 1 | 0.0714 | [0.0714, 0.0714] | 1/0/0 |
| Chameleon | reliability_only - node_feature_only | test_routing_accuracy | 1 | 0.0914 | [0.0914, 0.0914] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_preference_auc | 1 | 0.0527 | [0.0527, 0.0527] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_balanced_accuracy | 1 | 0.0429 | [0.0429, 0.0429] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_routing_accuracy | 1 | 0.0571 | [0.0571, 0.0571] | 1/0/0 |
| Actor | reliability_only - node_feature_only | test_preference_auc | 1 | -0.0192 | [-0.0192, -0.0192] | 0/0/1 |
| Actor | reliability_only - node_feature_only | test_balanced_accuracy | 1 | -0.0326 | [-0.0326, -0.0326] | 0/0/1 |
| Actor | reliability_only - node_feature_only | test_routing_accuracy | 1 | -0.0152 | [-0.0152, -0.0152] | 0/0/1 |
| Actor | combined - node_feature_only | test_preference_auc | 1 | -0.0197 | [-0.0197, -0.0197] | 0/0/1 |
| Actor | combined - node_feature_only | test_balanced_accuracy | 1 | -0.0315 | [-0.0315, -0.0315] | 0/0/1 |
| Actor | combined - node_feature_only | test_routing_accuracy | 1 | -0.0369 | [-0.0369, -0.0369] | 0/0/1 |
| Roman-empire | reliability_only - node_feature_only | test_preference_auc | 1 | -0.0340 | [-0.0340, -0.0340] | 0/0/1 |
| Roman-empire | reliability_only - node_feature_only | test_balanced_accuracy | 1 | 0.0100 | [0.0100, 0.0100] | 1/0/0 |
| Roman-empire | reliability_only - node_feature_only | test_routing_accuracy | 1 | -0.2512 | [-0.2512, -0.2512] | 0/0/1 |
| Roman-empire | combined - node_feature_only | test_preference_auc | 1 | 0.0295 | [0.0295, 0.0295] | 1/0/0 |
| Roman-empire | combined - node_feature_only | test_balanced_accuracy | 1 | 0.0846 | [0.0846, 0.0846] | 1/0/0 |
| Roman-empire | combined - node_feature_only | test_routing_accuracy | 1 | 0.0235 | [0.0235, 0.0235] | 1/0/0 |

## Decision Rule

- Continue reliability routing only if reliability-only AUC is clearly above 0.5 and combined reliably exceeds node-feature-only on at least two undirected heterophilous datasets.
- Treat routed node accuracy as secondary; preference AUC and balanced accuracy diagnose whether the routing signal exists.
- Training preference labels are generated from out-of-fold expert predictions to avoid in-sample expert leakage.
