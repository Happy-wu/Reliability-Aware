# Preference Routing Diagnostic

Primary question: can reliability predict which frozen expert is correct?

## Summary

| Dataset | Router | Valid/Total | Status | Preference nodes | AUC [95% CI] | Threshold | Balanced acc | Routing acc | Majority routing | Routed node acc | Majority node acc |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Actor | reliability_only | 10/10 | ok:10 | 440.8 | 0.5279 [0.5098, 0.5460] | 0.5215 | 0.5171 | 0.5166 | 0.5846 | 0.3330 | 0.3526 |
| Actor | node_feature_only | 10/10 | ok:10 | 440.8 | 0.5276 [0.4988, 0.5563] | 0.5231 | 0.5175 | 0.5142 | 0.5846 | 0.3322 | 0.3526 |
| Actor | combined | 10/10 | ok:10 | 440.8 | 0.5392 [0.5261, 0.5522] | 0.4973 | 0.5209 | 0.5109 | 0.5846 | 0.3311 | 0.3526 |
| Amazon-ratings | reliability_only | 10/10 | ok:10 | 1834.0 | 0.5580 [0.5377, 0.5783] | 0.4706 | 0.5415 | 0.5389 | 0.5134 | 0.4205 | 0.4142 |
| Amazon-ratings | node_feature_only | 10/10 | ok:10 | 1834.0 | 0.5346 [0.5108, 0.5585] | 0.3996 | 0.5318 | 0.5294 | 0.5134 | 0.4179 | 0.4142 |
| Amazon-ratings | combined | 10/10 | ok:10 | 1834.0 | 0.5620 [0.5436, 0.5805] | 0.4715 | 0.5473 | 0.5452 | 0.5134 | 0.4225 | 0.4142 |
| Chameleon | reliability_only | 10/10 | ok:10 | 168.3 | 0.6606 [0.6219, 0.6994] | 0.5273 | 0.6185 | 0.5931 | 0.7286 | 0.5941 | 0.6436 |
| Chameleon | node_feature_only | 10/10 | ok:10 | 168.3 | 0.5791 [0.5508, 0.6073] | 0.6967 | 0.5634 | 0.4936 | 0.7286 | 0.5577 | 0.6436 |
| Chameleon | combined | 10/10 | ok:10 | 168.3 | 0.6391 [0.6041, 0.6740] | 0.5669 | 0.6018 | 0.5905 | 0.7286 | 0.5928 | 0.6436 |
| Minesweeper | reliability_only | 7/10 | insufficient_validation_labels:3;ok:7 | 19.1 | 0.5911 [0.5128, 0.6695] | 0.3910 | 0.6114 | 0.6030 | 0.6336 | 0.8015 | 0.8004 |
| Minesweeper | node_feature_only | 7/10 | insufficient_validation_labels:3;ok:7 | 19.1 | 0.5289 [0.3714, 0.6863] | 0.4897 | 0.5271 | 0.5161 | 0.6336 | 0.8006 | 0.8004 |
| Minesweeper | combined | 7/10 | insufficient_validation_labels:3;ok:7 | 19.1 | 0.5071 [0.3303, 0.6838] | 0.4247 | 0.5141 | 0.5327 | 0.6336 | 0.8009 | 0.8004 |
| Roman-empire | reliability_only | 10/10 | ok:10 | 2340.3 | 0.6997 [0.6899, 0.7094] | 0.5157 | 0.6472 | 0.6240 | 0.8325 | 0.5738 | 0.6599 |
| Roman-empire | node_feature_only | 10/10 | ok:10 | 2340.3 | 0.7674 [0.7563, 0.7785] | 0.4095 | 0.7052 | 0.6285 | 0.8325 | 0.5757 | 0.6599 |
| Roman-empire | combined | 10/10 | ok:10 | 2340.3 | 0.8379 [0.8280, 0.8479] | 0.2526 | 0.7571 | 0.7340 | 0.8325 | 0.6192 | 0.6599 |
| Squirrel | reliability_only | 10/10 | ok:10 | 425.1 | 0.6098 [0.5864, 0.6331] | 0.4836 | 0.5762 | 0.5955 | 0.7008 | 0.4305 | 0.4736 |
| Squirrel | node_feature_only | 10/10 | ok:10 | 425.1 | 0.5242 [0.5107, 0.5377] | 0.6147 | 0.5131 | 0.5570 | 0.7008 | 0.4150 | 0.4736 |
| Squirrel | combined | 10/10 | ok:10 | 425.1 | 0.5885 [0.5614, 0.6155] | 0.6680 | 0.5646 | 0.5586 | 0.7008 | 0.4157 | 0.4736 |

## Paired Comparisons

| Dataset | Comparison | Metric | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Chameleon | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0816 | [0.0477, 0.1154] | 10/0/0 |
| Chameleon | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0550 | [0.0200, 0.0901] | 9/0/1 |
| Chameleon | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0996 | [0.0613, 0.1378] | 10/0/0 |
| Chameleon | combined - node_feature_only | test_preference_auc | 10 | 0.0600 | [0.0316, 0.0884] | 9/0/1 |
| Chameleon | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0384 | [0.0149, 0.0618] | 9/0/1 |
| Chameleon | combined - node_feature_only | test_routing_accuracy | 10 | 0.0970 | [0.0470, 0.1469] | 9/0/1 |
| Squirrel | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0856 | [0.0599, 0.1112] | 10/0/0 |
| Squirrel | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0630 | [0.0358, 0.0903] | 10/0/0 |
| Squirrel | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0384 | [-0.0095, 0.0863] | 6/0/4 |
| Squirrel | combined - node_feature_only | test_preference_auc | 10 | 0.0643 | [0.0367, 0.0918] | 10/0/0 |
| Squirrel | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0515 | [0.0281, 0.0749] | 9/0/1 |
| Squirrel | combined - node_feature_only | test_routing_accuracy | 10 | 0.0016 | [-0.0251, 0.0283] | 4/0/6 |
| Actor | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0003 | [-0.0272, 0.0278] | 4/0/6 |
| Actor | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0004 | [-0.0274, 0.0266] | 5/0/5 |
| Actor | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0024 | [-0.0402, 0.0451] | 6/0/4 |
| Actor | combined - node_feature_only | test_preference_auc | 10 | 0.0116 | [-0.0229, 0.0460] | 5/0/5 |
| Actor | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0034 | [-0.0290, 0.0358] | 2/0/8 |
| Actor | combined - node_feature_only | test_routing_accuracy | 10 | -0.0032 | [-0.0500, 0.0435] | 3/0/7 |
| Roman-empire | reliability_only - node_feature_only | test_preference_auc | 10 | -0.0677 | [-0.0809, -0.0546] | 0/0/10 |
| Roman-empire | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0580 | [-0.0708, -0.0451] | 0/0/10 |
| Roman-empire | reliability_only - node_feature_only | test_routing_accuracy | 10 | -0.0044 | [-0.0188, 0.0099] | 4/0/6 |
| Roman-empire | combined - node_feature_only | test_preference_auc | 10 | 0.0705 | [0.0594, 0.0816] | 10/0/0 |
| Roman-empire | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0519 | [0.0417, 0.0622] | 10/0/0 |
| Roman-empire | combined - node_feature_only | test_routing_accuracy | 10 | 0.1055 | [0.0801, 0.1309] | 10/0/0 |
| Amazon-ratings | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0234 | [0.0050, 0.0417] | 8/0/2 |
| Amazon-ratings | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0098 | [-0.0048, 0.0243] | 7/0/3 |
| Amazon-ratings | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0095 | [-0.0036, 0.0226] | 6/0/4 |
| Amazon-ratings | combined - node_feature_only | test_preference_auc | 10 | 0.0274 | [0.0083, 0.0465] | 8/0/2 |
| Amazon-ratings | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0156 | [0.0006, 0.0305] | 8/0/2 |
| Amazon-ratings | combined - node_feature_only | test_routing_accuracy | 10 | 0.0158 | [0.0010, 0.0305] | 7/0/3 |
| Minesweeper | reliability_only - node_feature_only | test_preference_auc | 7 | 0.0623 | [-0.1329, 0.2575] | 5/0/2 |
| Minesweeper | reliability_only - node_feature_only | test_balanced_accuracy | 7 | 0.0843 | [-0.0020, 0.1706] | 5/0/2 |
| Minesweeper | reliability_only - node_feature_only | test_routing_accuracy | 7 | 0.0868 | [-0.0085, 0.1822] | 5/0/2 |
| Minesweeper | combined - node_feature_only | test_preference_auc | 7 | -0.0218 | [-0.0898, 0.0462] | 3/1/3 |
| Minesweeper | combined - node_feature_only | test_balanced_accuracy | 7 | -0.0131 | [-0.0959, 0.0698] | 4/0/3 |
| Minesweeper | combined - node_feature_only | test_routing_accuracy | 7 | 0.0166 | [-0.0715, 0.1047] | 4/2/1 |

## Decision Rule

- Continue reliability routing only if reliability-only AUC is clearly above 0.5 and combined reliably exceeds node-feature-only on at least two undirected heterophilous datasets.
- Treat routed node accuracy as secondary; preference AUC and balanced accuracy diagnose whether the routing signal exists.
- Training preference labels are generated from out-of-fold expert predictions to avoid in-sample expert leakage.
