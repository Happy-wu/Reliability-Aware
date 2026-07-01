# Preference Routing Diagnostic

Primary question: can reliability predict which frozen expert is correct?

`P/H/U/Total` denotes preference-valid, post-hoc-utility-valid, utility-checkpoint-valid, and total runs.

## Summary

| Dataset | Router | P/H/U/Total | Status | AUC [95% CI] | Fixed-0.5 routed acc | Pref-threshold routed acc | Post-hoc utility acc | Utility-checkpoint acc | Best expert | Fixed alpha | Oracle | Utility switch |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Chameleon | reliability_only | 1/1/1/1 | ok:1 | 0.6161 [n/a, n/a] | 0.5482 | 0.5439 | 0.5461 | 0.5461 | 0.5482 | 0.5395 (a=0.75) | 0.7018 | 0.4518 |
| Chameleon | node_feature_only | 1/1/1/1 | ok:1 | 0.5094 [n/a, n/a] | 0.5088 | 0.5088 | 0.5088 | 0.5329 | 0.5482 | 0.5395 (a=0.75) | 0.7018 | 0.5395 |
| Chameleon | combined | 1/1/1/1 | ok:1 | 0.5965 [n/a, n/a] | 0.5307 | 0.5241 | 0.5219 | 0.5329 | 0.5482 | 0.5395 (a=0.75) | 0.7018 | 0.5022 |
| Cora | reliability_only | 1/1/1/1 | ok:1 | 0.5356 [n/a, n/a] | 0.7560 | 0.6020 | 0.8110 | 0.8110 | 0.8110 | 0.8110 (a=1.00) | 0.8570 | 0.0000 |
| Cora | node_feature_only | 1/1/1/1 | ok:1 | 0.4719 [n/a, n/a] | 0.8110 | 0.7660 | 0.8110 | 0.8110 | 0.8110 | 0.8110 (a=1.00) | 0.8570 | 0.0000 |
| Cora | combined | 1/1/1/1 | ok:1 | 0.5224 [n/a, n/a] | 0.7450 | 0.5870 | 0.8110 | 0.8110 | 0.8110 | 0.8110 (a=1.00) | 0.8570 | 0.0000 |
| Minesweeper | reliability_only | 0/0/0/1 | insufficient_preference_labels:1 | n/a [n/a, n/a] | n/a | n/a | n/a | n/a | 0.8000 | 0.8000 (a=1.00) | 0.8000 | n/a |
| Minesweeper | node_feature_only | 0/0/0/1 | insufficient_preference_labels:1 | n/a [n/a, n/a] | n/a | n/a | n/a | n/a | 0.8000 | 0.8000 (a=1.00) | 0.8000 | n/a |
| Minesweeper | combined | 0/0/0/1 | insufficient_preference_labels:1 | n/a [n/a, n/a] | n/a | n/a | n/a | n/a | 0.8000 | 0.8000 (a=1.00) | 0.8000 | n/a |
| Roman-empire | reliability_only | 1/1/1/1 | ok:1 | 0.7953 [n/a, n/a] | 0.4158 | 0.5501 | 0.6470 | 0.6468 | 0.6470 | 0.6445 (a=0.75) | 0.6647 | 0.0000 |
| Roman-empire | node_feature_only | 1/1/1/1 | ok:1 | 0.8417 [n/a, n/a] | 0.5724 | 0.5252 | 0.6470 | 0.6472 | 0.6470 | 0.6445 (a=0.75) | 0.6647 | 0.0000 |
| Roman-empire | combined | 1/1/1/1 | ok:1 | 0.8774 [n/a, n/a] | 0.5980 | 0.5660 | 0.6470 | 0.6470 | 0.6470 | 0.6445 (a=0.75) | 0.6647 | 0.0000 |

## Paired Comparisons

| Dataset | Comparison | Metric | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Cora | reliability_only - node_feature_only | test_preference_auc | 1 | 0.0637 | [n/a, n/a] | 1/0/0 |
| Cora | reliability_only - node_feature_only | test_balanced_accuracy | 1 | 0.0841 | [n/a, n/a] | 1/0/0 |
| Cora | reliability_only - node_feature_only | test_routing_accuracy | 1 | -0.4530 | [n/a, n/a] | 0/0/1 |
| Cora | combined - node_feature_only | test_preference_auc | 1 | 0.0504 | [n/a, n/a] | 1/0/0 |
| Cora | combined - node_feature_only | test_balanced_accuracy | 1 | 0.0418 | [n/a, n/a] | 1/0/0 |
| Cora | combined - node_feature_only | test_routing_accuracy | 1 | -0.4945 | [n/a, n/a] | 0/0/1 |
| Chameleon | reliability_only - node_feature_only | test_preference_auc | 1 | 0.1067 | [n/a, n/a] | 1/0/0 |
| Chameleon | reliability_only - node_feature_only | test_balanced_accuracy | 1 | 0.0738 | [n/a, n/a] | 1/0/0 |
| Chameleon | reliability_only - node_feature_only | test_routing_accuracy | 1 | 0.0914 | [n/a, n/a] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_preference_auc | 1 | 0.0871 | [n/a, n/a] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_balanced_accuracy | 1 | 0.0381 | [n/a, n/a] | 1/0/0 |
| Chameleon | combined - node_feature_only | test_routing_accuracy | 1 | 0.0400 | [n/a, n/a] | 1/0/0 |
| Roman-empire | reliability_only - node_feature_only | test_preference_auc | 1 | -0.0464 | [n/a, n/a] | 0/0/1 |
| Roman-empire | reliability_only - node_feature_only | test_balanced_accuracy | 1 | -0.0961 | [n/a, n/a] | 0/0/1 |
| Roman-empire | reliability_only - node_feature_only | test_routing_accuracy | 1 | 0.0474 | [n/a, n/a] | 1/0/0 |
| Roman-empire | combined - node_feature_only | test_preference_auc | 1 | 0.0357 | [n/a, n/a] | 1/0/0 |
| Roman-empire | combined - node_feature_only | test_balanced_accuracy | 1 | 0.0016 | [n/a, n/a] | 1/0/0 |
| Roman-empire | combined - node_feature_only | test_routing_accuracy | 1 | 0.0777 | [n/a, n/a] | 1/0/0 |
| Minesweeper | reliability_only - node_feature_only | test_preference_auc | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only - node_feature_only | test_balanced_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only - node_feature_only | test_routing_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_preference_auc | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_balanced_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_routing_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |

## Utility Comparisons

| Dataset | Router | Comparison | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Cora | reliability_only | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | reliability_only | utility-checkpoint routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | reliability_only | utility routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | node_feature_only | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | node_feature_only | utility-checkpoint routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | node_feature_only | utility routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | combined | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | combined | utility-checkpoint routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | combined | utility routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Cora | combined | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Chameleon | reliability_only | utility routing - validation-selected best expert | 1 | -0.0022 | [n/a, n/a] | 0/0/1 |
| Chameleon | reliability_only | utility-checkpoint routing - validation-selected best expert | 1 | -0.0022 | [n/a, n/a] | 0/0/1 |
| Chameleon | reliability_only | utility routing - validation-selected fixed alpha | 1 | 0.0066 | [n/a, n/a] | 1/0/0 |
| Chameleon | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0066 | [n/a, n/a] | 1/0/0 |
| Chameleon | node_feature_only | utility routing - validation-selected best expert | 1 | -0.0395 | [n/a, n/a] | 0/0/1 |
| Chameleon | node_feature_only | utility-checkpoint routing - validation-selected best expert | 1 | -0.0154 | [n/a, n/a] | 0/0/1 |
| Chameleon | node_feature_only | utility routing - validation-selected fixed alpha | 1 | -0.0307 | [n/a, n/a] | 0/0/1 |
| Chameleon | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | -0.0066 | [n/a, n/a] | 0/0/1 |
| Chameleon | combined | utility routing - validation-selected best expert | 1 | -0.0263 | [n/a, n/a] | 0/0/1 |
| Chameleon | combined | utility-checkpoint routing - validation-selected best expert | 1 | -0.0154 | [n/a, n/a] | 0/0/1 |
| Chameleon | combined | utility routing - validation-selected fixed alpha | 1 | -0.0175 | [n/a, n/a] | 0/0/1 |
| Chameleon | combined | utility-checkpoint routing - validation-selected fixed alpha | 1 | -0.0066 | [n/a, n/a] | 0/0/1 |
| Roman-empire | reliability_only | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Roman-empire | reliability_only | utility-checkpoint routing - validation-selected best expert | 1 | -0.0002 | [n/a, n/a] | 0/0/1 |
| Roman-empire | reliability_only | utility routing - validation-selected fixed alpha | 1 | 0.0025 | [n/a, n/a] | 1/0/0 |
| Roman-empire | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0023 | [n/a, n/a] | 1/0/0 |
| Roman-empire | node_feature_only | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Roman-empire | node_feature_only | utility-checkpoint routing - validation-selected best expert | 1 | 0.0002 | [n/a, n/a] | 1/0/0 |
| Roman-empire | node_feature_only | utility routing - validation-selected fixed alpha | 1 | 0.0025 | [n/a, n/a] | 1/0/0 |
| Roman-empire | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0026 | [n/a, n/a] | 1/0/0 |
| Roman-empire | combined | utility routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Roman-empire | combined | utility-checkpoint routing - validation-selected best expert | 1 | 0.0000 | [n/a, n/a] | 0/1/0 |
| Roman-empire | combined | utility routing - validation-selected fixed alpha | 1 | 0.0025 | [n/a, n/a] | 1/0/0 |
| Roman-empire | combined | utility-checkpoint routing - validation-selected fixed alpha | 1 | 0.0025 | [n/a, n/a] | 1/0/0 |
| Minesweeper | reliability_only | utility routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only | utility-checkpoint routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only | utility routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | node_feature_only | utility routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | node_feature_only | utility-checkpoint routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | node_feature_only | utility routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined | utility routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined | utility-checkpoint routing - validation-selected best expert | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined | utility routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined | utility-checkpoint routing - validation-selected fixed alpha | 0 | n/a | [n/a, n/a] | 0/0/0 |

## Decision Rule

- Preference evidence: reliability-only AUC should be clearly above 0.5 and combined should exceed node-feature-only.
- Utility evidence: utility-threshold routing should exceed the validation-selected best expert or fixed-alpha baseline with a paired CI above zero.
- Training preference labels are generated from out-of-fold expert predictions to avoid in-sample expert leakage.
- Post-hoc utility uses a preference-selected checkpoint; utility-checkpoint routing separately selects the epoch by validation routed accuracy.
- Utility thresholds are conservative: near-optimal thresholds prefer fewer switches away from the stronger validation expert.
