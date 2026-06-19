# Preference Routing Diagnostic

Primary question: can reliability predict which frozen expert is correct?

`P/H/U/Total` denotes preference-valid, post-hoc-utility-valid, utility-checkpoint-valid, and total runs.

## Summary

| Dataset | Router | P/H/U/Total | Status | AUC [95% CI] | Fixed-0.5 routed acc | Pref-threshold routed acc | Post-hoc utility acc | Utility-checkpoint acc | Best expert | Fixed alpha | Oracle | Utility switch |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Actor | reliability_only | 10/10/10/10 | ok:10 | 0.5283 [0.5098, 0.5467] | 0.3281 | 0.3352 | 0.3516 | 0.3511 | 0.3526 | 0.3535 (a=0.10) | 0.4731 | 0.0422 |
| Actor | node_feature_only | 10/10/10/10 | ok:10 | 0.5277 [0.4989, 0.5564] | 0.3305 | 0.3320 | 0.3529 | 0.3522 | 0.3526 | 0.3535 (a=0.10) | 0.4731 | 0.0785 |
| Actor | combined | 10/10/10/10 | ok:10 | 0.5362 [0.5231, 0.5493] | 0.3395 | 0.3291 | 0.3526 | 0.3507 | 0.3526 | 0.3535 (a=0.10) | 0.4731 | 0.0578 |
| Amazon-ratings | reliability_only | 10/10/10/10 | ok:10 | 0.5231 [0.4501, 0.5962] | 0.3683 | 0.3686 | 0.3689 | 0.3687 | 0.3686 | 0.3686 (a=1.00) | 0.3791 | 0.0990 |
| Amazon-ratings | node_feature_only | 10/10/10/10 | ok:10 | 0.4839 [0.3965, 0.5712] | 0.3692 | 0.3690 | 0.3697 | 0.3693 | 0.3686 | 0.3686 (a=1.00) | 0.3791 | 0.2132 |
| Amazon-ratings | combined | 10/10/10/10 | ok:10 | 0.5695 [0.5286, 0.6105] | 0.3687 | 0.3684 | 0.3687 | 0.3688 | 0.3686 | 0.3686 (a=1.00) | 0.3791 | 0.1180 |
| Chameleon | reliability_only | 10/10/10/10 | ok:10 | 0.6614 [0.6347, 0.6881] | 0.5853 | 0.5882 | 0.6254 | 0.6257 | 0.6296 | 0.6307 (a=0.95) | 0.7371 | 0.0292 |
| Chameleon | node_feature_only | 10/10/10/10 | ok:10 | 0.5781 [0.5495, 0.6068] | 0.5577 | 0.5627 | 0.6272 | 0.6276 | 0.6296 | 0.6307 (a=0.95) | 0.7371 | 0.0197 |
| Chameleon | combined | 10/10/10/10 | ok:10 | 0.6388 [0.6088, 0.6688] | 0.6013 | 0.5866 | 0.6252 | 0.6235 | 0.6296 | 0.6307 (a=0.95) | 0.7371 | 0.0476 |
| Citeseer | reliability_only | 10/10/10/10 | ok:10 | 0.5096 [0.4805, 0.5387] | 0.6421 | 0.6329 | 0.6915 | 0.6907 | 0.6931 | 0.6929 (a=0.97) | 0.7695 | 0.0102 |
| Citeseer | node_feature_only | 10/10/10/10 | ok:10 | 0.5342 [0.5023, 0.5661] | 0.6441 | 0.6258 | 0.6931 | 0.6931 | 0.6931 | 0.6929 (a=0.97) | 0.7695 | 0.0000 |
| Citeseer | combined | 10/10/10/10 | ok:10 | 0.5241 [0.4915, 0.5568] | 0.6373 | 0.6347 | 0.6915 | 0.6908 | 0.6931 | 0.6929 (a=0.97) | 0.7695 | 0.0078 |
| Cora | reliability_only | 10/10/10/10 | ok:10 | 0.5567 [0.5187, 0.5947] | 0.7383 | 0.7028 | 0.8068 | 0.8072 | 0.8082 | 0.8082 (a=1.00) | 0.8594 | 0.0062 |
| Cora | node_feature_only | 10/10/10/10 | ok:10 | 0.5139 [0.4865, 0.5414] | 0.7522 | 0.6771 | 0.8082 | 0.8082 | 0.8082 | 0.8082 (a=1.00) | 0.8594 | 0.0000 |
| Cora | combined | 10/10/10/10 | ok:10 | 0.5657 [0.5347, 0.5967] | 0.7525 | 0.7259 | 0.8082 | 0.8084 | 0.8082 | 0.8082 (a=1.00) | 0.8594 | 0.0000 |
| Minesweeper | reliability_only | 0/10/10/10 | ok_utility_only:10 | n/a [n/a, n/a] | 0.8000 | n/a | 0.8000 | 0.8000 | 0.8000 | 0.8000 (a=1.00) | 0.8000 | 0.0000 |
| Minesweeper | node_feature_only | 0/10/10/10 | ok_utility_only:10 | n/a [n/a, n/a] | 0.8000 | n/a | 0.8000 | 0.8000 | 0.8000 | 0.8000 (a=1.00) | 0.8000 | 0.0000 |
| Minesweeper | combined | 0/10/10/10 | ok_utility_only:10 | n/a [n/a, n/a] | 0.8000 | n/a | 0.8000 | 0.8000 | 0.8000 | 0.8000 (a=1.00) | 0.8000 | 0.0000 |
| Pubmed | reliability_only | 10/10/10/10 | ok:10 | 0.5217 [0.4906, 0.5527] | 0.7466 | 0.7354 | 0.7684 | 0.7683 | 0.7687 | 0.7696 (a=0.97) | 0.8418 | 0.0095 |
| Pubmed | node_feature_only | 10/10/10/10 | ok:10 | 0.4955 [0.4628, 0.5282] | 0.7474 | 0.7467 | 0.7683 | 0.7667 | 0.7687 | 0.7696 (a=0.97) | 0.8418 | 0.0056 |
| Pubmed | combined | 10/10/10/10 | ok:10 | 0.5074 [0.4779, 0.5370] | 0.7347 | 0.7255 | 0.7687 | 0.7677 | 0.7687 | 0.7696 (a=0.97) | 0.8418 | 0.0000 |
| Roman-empire | reliability_only | 10/10/10/10 | ok:10 | 0.7223 [0.7144, 0.7301] | 0.5419 | 0.5444 | 0.6603 | 0.6599 | 0.6599 | 0.6743 (a=0.45) | 0.7265 | 0.0093 |
| Roman-empire | node_feature_only | 10/10/10/10 | ok:10 | 0.7906 [0.7825, 0.7987] | 0.5833 | 0.5553 | 0.6597 | 0.6599 | 0.6599 | 0.6743 (a=0.45) | 0.7265 | 0.0026 |
| Roman-empire | combined | 10/10/10/10 | ok:10 | 0.8522 [0.8436, 0.8608] | 0.6168 | 0.6057 | 0.6662 | 0.6664 | 0.6599 | 0.6743 (a=0.45) | 0.7265 | 0.0564 |
| Squirrel | reliability_only | 10/10/10/10 | ok:10 | 0.5872 [0.5627, 0.6117] | 0.4061 | 0.4127 | 0.4451 | 0.4437 | 0.4449 | 0.4449 (a=1.00) | 0.5780 | 0.0179 |
| Squirrel | node_feature_only | 10/10/10/10 | ok:10 | 0.5268 [0.5062, 0.5474] | 0.3997 | 0.3945 | 0.4445 | 0.4439 | 0.4449 | 0.4449 (a=1.00) | 0.5780 | 0.0019 |
| Squirrel | combined | 10/10/10/10 | ok:10 | 0.5786 [0.5467, 0.6106] | 0.4148 | 0.4078 | 0.4449 | 0.4444 | 0.4449 | 0.4449 (a=1.00) | 0.5780 | 0.0247 |

## Paired Comparisons

| Dataset | Comparison | Metric | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Cora | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0428 | [-0.0112, 0.0967] | 7/0/3 |
| Cora | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0322 | [-0.0031, 0.0674] | 8/0/2 |
| Cora | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0698 | [-0.0238, 0.1634] | 7/0/3 |
| Cora | combined - node_feature_only | test_preference_auc | 10 | 0.0518 | [0.0087, 0.0949] | 7/0/3 |
| Cora | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0240 | [0.0006, 0.0475] | 7/0/3 |
| Cora | combined - node_feature_only | test_routing_accuracy | 10 | 0.1328 | [0.0528, 0.2129] | 8/0/2 |
| Citeseer | reliability_only - node_feature_only | test_preference_auc | 10 | -0.0246 | [-0.0639, 0.0147] | 3/0/7 |
| Citeseer | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0180 | [-0.0440, 0.0081] | 4/0/6 |
| Citeseer | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0206 | [-0.0549, 0.0961] | 4/0/6 |
| Citeseer | combined - node_feature_only | test_preference_auc | 10 | -0.0100 | [-0.0424, 0.0223] | 3/0/7 |
| Citeseer | combined - node_feature_only | test_balanced_accuracy | 10 | -0.0115 | [-0.0310, 0.0080] | 5/0/5 |
| Citeseer | combined - node_feature_only | test_routing_accuracy | 10 | 0.0256 | [-0.0663, 0.1174] | 5/0/5 |
| Pubmed | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0262 | [-0.0276, 0.0800] | 5/0/5 |
| Pubmed | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0050 | [-0.0294, 0.0193] | 4/0/6 |
| Pubmed | reliability_only - node_feature_only | test_routing_accuracy | 10 | -0.0518 | [-0.1490, 0.0453] | 4/0/6 |
| Pubmed | combined - node_feature_only | test_preference_auc | 10 | 0.0120 | [-0.0389, 0.0629] | 6/0/4 |
| Pubmed | combined - node_feature_only | test_balanced_accuracy | 10 | -0.0064 | [-0.0458, 0.0329] | 6/0/4 |
| Pubmed | combined - node_feature_only | test_routing_accuracy | 10 | -0.0986 | [-0.1528, -0.0444] | 1/0/9 |
| Chameleon | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0833 | [0.0459, 0.1207] | 10/0/0 |
| Chameleon | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0707 | [0.0429, 0.0984] | 9/0/1 |
| Chameleon | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0676 | [0.0226, 0.1127] | 9/0/1 |
| Chameleon | combined - node_feature_only | test_preference_auc | 10 | 0.0607 | [0.0337, 0.0877] | 10/0/0 |
| Chameleon | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0554 | [0.0294, 0.0813] | 9/0/1 |
| Chameleon | combined - node_feature_only | test_routing_accuracy | 10 | 0.0652 | [0.0275, 0.1029] | 9/0/1 |
| Squirrel | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0604 | [0.0334, 0.0875] | 10/0/0 |
| Squirrel | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0408 | [0.0115, 0.0701] | 10/0/0 |
| Squirrel | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0458 | [0.0068, 0.0848] | 8/0/2 |
| Squirrel | combined - node_feature_only | test_preference_auc | 10 | 0.0519 | [0.0165, 0.0872] | 9/0/1 |
| Squirrel | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0412 | [0.0126, 0.0697] | 8/0/2 |
| Squirrel | combined - node_feature_only | test_routing_accuracy | 10 | 0.0334 | [-0.0284, 0.0953] | 6/0/4 |
| Actor | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0006 | [-0.0271, 0.0283] | 4/0/6 |
| Actor | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0015 | [-0.0288, 0.0258] | 5/0/5 |
| Actor | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0114 | [-0.0274, 0.0502] | 7/0/3 |
| Actor | combined - node_feature_only | test_preference_auc | 10 | 0.0085 | [-0.0263, 0.0433] | 4/0/6 |
| Actor | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0033 | [-0.0291, 0.0357] | 2/0/8 |
| Actor | combined - node_feature_only | test_routing_accuracy | 10 | -0.0094 | [-0.0585, 0.0398] | 3/0/7 |
| Roman-empire | reliability_only - node_feature_only | test_preference_auc | 10 | -0.0683 | [-0.0786, -0.0581] | 0/0/10 |
| Roman-empire | reliability_only - node_feature_only | test_balanced_accuracy | 10 | -0.0570 | [-0.0685, -0.0455] | 0/0/10 |
| Roman-empire | reliability_only - node_feature_only | test_routing_accuracy | 10 | -0.0234 | [-0.0441, -0.0027] | 2/0/8 |
| Roman-empire | combined - node_feature_only | test_preference_auc | 10 | 0.0616 | [0.0551, 0.0681] | 10/0/0 |
| Roman-empire | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0487 | [0.0369, 0.0605] | 10/0/0 |
| Roman-empire | combined - node_feature_only | test_routing_accuracy | 10 | 0.1083 | [0.0938, 0.1227] | 10/0/0 |
| Amazon-ratings | reliability_only - node_feature_only | test_preference_auc | 10 | 0.0393 | [-0.0538, 0.1323] | 5/0/5 |
| Amazon-ratings | reliability_only - node_feature_only | test_balanced_accuracy | 10 | 0.0381 | [-0.0569, 0.1331] | 5/0/5 |
| Amazon-ratings | reliability_only - node_feature_only | test_routing_accuracy | 10 | 0.0760 | [-0.0569, 0.2088] | 5/1/4 |
| Amazon-ratings | combined - node_feature_only | test_preference_auc | 10 | 0.0856 | [-0.0322, 0.2035] | 6/0/4 |
| Amazon-ratings | combined - node_feature_only | test_balanced_accuracy | 10 | 0.0350 | [-0.0485, 0.1184] | 5/1/4 |
| Amazon-ratings | combined - node_feature_only | test_routing_accuracy | 10 | 0.0432 | [-0.0421, 0.1286] | 7/0/3 |
| Minesweeper | reliability_only - node_feature_only | test_preference_auc | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only - node_feature_only | test_balanced_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | reliability_only - node_feature_only | test_routing_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_preference_auc | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_balanced_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |
| Minesweeper | combined - node_feature_only | test_routing_accuracy | 0 | n/a | [n/a, n/a] | 0/0/0 |

## Utility Comparisons

| Dataset | Router | Comparison | N | Delta | 95% CI | W/T/L |
|---|---|---|---:|---:|---:|---:|
| Cora | reliability_only | utility routing - validation-selected best expert | 10 | -0.0014 | [-0.0028, -0.0000] | 0/6/4 |
| Cora | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0010 | [-0.0021, 0.0001] | 0/5/5 |
| Cora | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0014 | [-0.0028, -0.0000] | 0/6/4 |
| Cora | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0010 | [-0.0021, 0.0001] | 0/5/5 |
| Cora | node_feature_only | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | node_feature_only | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | combined | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | combined | utility-checkpoint routing - validation-selected best expert | 10 | 0.0002 | [-0.0003, 0.0007] | 1/9/0 |
| Cora | combined | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Cora | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0002 | [-0.0003, 0.0007] | 1/9/0 |
| Citeseer | reliability_only | utility routing - validation-selected best expert | 10 | -0.0016 | [-0.0047, 0.0015] | 0/7/3 |
| Citeseer | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0024 | [-0.0057, 0.0009] | 0/7/3 |
| Citeseer | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0014 | [-0.0046, 0.0018] | 1/6/3 |
| Citeseer | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0022 | [-0.0056, 0.0012] | 1/6/3 |
| Citeseer | node_feature_only | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Citeseer | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [-0.0015, 0.0015] | 1/7/2 |
| Citeseer | node_feature_only | utility routing - validation-selected fixed alpha | 10 | 0.0002 | [-0.0003, 0.0007] | 1/9/0 |
| Citeseer | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0002 | [-0.0011, 0.0015] | 1/7/2 |
| Citeseer | combined | utility routing - validation-selected best expert | 10 | -0.0016 | [-0.0052, 0.0020] | 0/9/1 |
| Citeseer | combined | utility-checkpoint routing - validation-selected best expert | 10 | -0.0023 | [-0.0061, 0.0015] | 1/6/3 |
| Citeseer | combined | utility routing - validation-selected fixed alpha | 10 | -0.0014 | [-0.0051, 0.0023] | 1/8/1 |
| Citeseer | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0021 | [-0.0060, 0.0018] | 2/6/2 |
| Pubmed | reliability_only | utility routing - validation-selected best expert | 10 | -0.0003 | [-0.0013, 0.0007] | 1/8/1 |
| Pubmed | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0004 | [-0.0014, 0.0006] | 1/7/2 |
| Pubmed | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0012 | [-0.0034, 0.0010] | 1/7/2 |
| Pubmed | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0013 | [-0.0035, 0.0009] | 1/6/3 |
| Pubmed | node_feature_only | utility routing - validation-selected best expert | 10 | -0.0004 | [-0.0014, 0.0006] | 1/7/2 |
| Pubmed | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0020 | [-0.0048, 0.0008] | 0/7/3 |
| Pubmed | node_feature_only | utility routing - validation-selected fixed alpha | 10 | -0.0013 | [-0.0037, 0.0011] | 1/7/2 |
| Pubmed | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0029 | [-0.0066, 0.0008] | 0/7/3 |
| Pubmed | combined | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Pubmed | combined | utility-checkpoint routing - validation-selected best expert | 10 | -0.0010 | [-0.0028, 0.0008] | 0/7/3 |
| Pubmed | combined | utility routing - validation-selected fixed alpha | 10 | -0.0009 | [-0.0029, 0.0011] | 0/9/1 |
| Pubmed | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0019 | [-0.0044, 0.0006] | 0/6/4 |
| Chameleon | reliability_only | utility routing - validation-selected best expert | 10 | -0.0042 | [-0.0104, 0.0020] | 1/5/4 |
| Chameleon | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0039 | [-0.0117, 0.0038] | 3/3/4 |
| Chameleon | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0053 | [-0.0113, 0.0008] | 1/3/6 |
| Chameleon | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0050 | [-0.0128, 0.0027] | 3/3/4 |
| Chameleon | node_feature_only | utility routing - validation-selected best expert | 10 | -0.0024 | [-0.0065, 0.0017] | 0/8/2 |
| Chameleon | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0020 | [-0.0059, 0.0020] | 0/8/2 |
| Chameleon | node_feature_only | utility routing - validation-selected fixed alpha | 10 | -0.0035 | [-0.0081, 0.0011] | 0/7/3 |
| Chameleon | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0031 | [-0.0071, 0.0009] | 0/6/4 |
| Chameleon | combined | utility routing - validation-selected best expert | 10 | -0.0044 | [-0.0090, 0.0002] | 0/5/5 |
| Chameleon | combined | utility-checkpoint routing - validation-selected best expert | 10 | -0.0061 | [-0.0118, -0.0005] | 1/2/7 |
| Chameleon | combined | utility routing - validation-selected fixed alpha | 10 | -0.0055 | [-0.0108, -0.0001] | 0/4/6 |
| Chameleon | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0072 | [-0.0129, -0.0016] | 0/3/7 |
| Squirrel | reliability_only | utility routing - validation-selected best expert | 10 | 0.0002 | [-0.0002, 0.0006] | 1/9/0 |
| Squirrel | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0012 | [-0.0025, 0.0002] | 2/1/7 |
| Squirrel | reliability_only | utility routing - validation-selected fixed alpha | 10 | 0.0002 | [-0.0002, 0.0006] | 1/9/0 |
| Squirrel | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0012 | [-0.0025, 0.0002] | 2/1/7 |
| Squirrel | node_feature_only | utility routing - validation-selected best expert | 10 | -0.0004 | [-0.0014, 0.0007] | 1/7/2 |
| Squirrel | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0010 | [-0.0026, 0.0007] | 2/4/4 |
| Squirrel | node_feature_only | utility routing - validation-selected fixed alpha | 10 | -0.0004 | [-0.0014, 0.0007] | 1/7/2 |
| Squirrel | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0010 | [-0.0026, 0.0007] | 2/4/4 |
| Squirrel | combined | utility routing - validation-selected best expert | 10 | 0.0000 | [-0.0017, 0.0017] | 3/4/3 |
| Squirrel | combined | utility-checkpoint routing - validation-selected best expert | 10 | -0.0005 | [-0.0033, 0.0024] | 5/1/4 |
| Squirrel | combined | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [-0.0017, 0.0017] | 3/4/3 |
| Squirrel | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0005 | [-0.0033, 0.0024] | 5/1/4 |
| Actor | reliability_only | utility routing - validation-selected best expert | 10 | -0.0010 | [-0.0030, 0.0011] | 1/6/3 |
| Actor | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0016 | [-0.0029, -0.0003] | 0/3/7 |
| Actor | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0018 | [-0.0040, 0.0004] | 1/3/6 |
| Actor | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0024 | [-0.0039, -0.0010] | 0/2/8 |
| Actor | node_feature_only | utility routing - validation-selected best expert | 10 | 0.0003 | [-0.0022, 0.0028] | 4/3/3 |
| Actor | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | -0.0004 | [-0.0035, 0.0027] | 3/1/6 |
| Actor | node_feature_only | utility routing - validation-selected fixed alpha | 10 | -0.0006 | [-0.0036, 0.0024] | 4/1/5 |
| Actor | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0012 | [-0.0042, 0.0017] | 3/2/5 |
| Actor | combined | utility routing - validation-selected best expert | 10 | -0.0001 | [-0.0017, 0.0016] | 4/4/2 |
| Actor | combined | utility-checkpoint routing - validation-selected best expert | 10 | -0.0020 | [-0.0040, 0.0000] | 2/0/8 |
| Actor | combined | utility routing - validation-selected fixed alpha | 10 | -0.0009 | [-0.0039, 0.0021] | 4/3/3 |
| Actor | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0028 | [-0.0058, 0.0001] | 2/0/8 |
| Roman-empire | reliability_only | utility routing - validation-selected best expert | 10 | 0.0004 | [-0.0003, 0.0010] | 6/2/2 |
| Roman-empire | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [-0.0006, 0.0007] | 5/0/5 |
| Roman-empire | reliability_only | utility routing - validation-selected fixed alpha | 10 | -0.0140 | [-0.0174, -0.0107] | 0/0/10 |
| Roman-empire | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0144 | [-0.0175, -0.0112] | 0/0/10 |
| Roman-empire | node_feature_only | utility routing - validation-selected best expert | 10 | -0.0002 | [-0.0004, 0.0000] | 0/7/3 |
| Roman-empire | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [-0.0008, 0.0008] | 5/0/5 |
| Roman-empire | node_feature_only | utility routing - validation-selected fixed alpha | 10 | -0.0146 | [-0.0177, -0.0116] | 0/0/10 |
| Roman-empire | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0144 | [-0.0175, -0.0114] | 0/0/10 |
| Roman-empire | combined | utility routing - validation-selected best expert | 10 | 0.0063 | [0.0041, 0.0085] | 10/0/0 |
| Roman-empire | combined | utility-checkpoint routing - validation-selected best expert | 10 | 0.0065 | [0.0046, 0.0085] | 10/0/0 |
| Roman-empire | combined | utility routing - validation-selected fixed alpha | 10 | -0.0081 | [-0.0112, -0.0051] | 0/0/10 |
| Roman-empire | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | -0.0079 | [-0.0114, -0.0044] | 0/0/10 |
| Amazon-ratings | reliability_only | utility routing - validation-selected best expert | 10 | 0.0003 | [-0.0002, 0.0008] | 3/6/1 |
| Amazon-ratings | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [-0.0002, 0.0003] | 2/6/2 |
| Amazon-ratings | reliability_only | utility routing - validation-selected fixed alpha | 10 | 0.0003 | [-0.0002, 0.0008] | 3/6/1 |
| Amazon-ratings | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0000 | [-0.0002, 0.0003] | 2/6/2 |
| Amazon-ratings | node_feature_only | utility routing - validation-selected best expert | 10 | 0.0010 | [-0.0010, 0.0031] | 2/6/2 |
| Amazon-ratings | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0006 | [-0.0007, 0.0019] | 2/6/2 |
| Amazon-ratings | node_feature_only | utility routing - validation-selected fixed alpha | 10 | 0.0010 | [-0.0010, 0.0031] | 2/6/2 |
| Amazon-ratings | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0006 | [-0.0007, 0.0019] | 2/6/2 |
| Amazon-ratings | combined | utility routing - validation-selected best expert | 10 | 0.0000 | [-0.0007, 0.0008] | 1/4/5 |
| Amazon-ratings | combined | utility-checkpoint routing - validation-selected best expert | 10 | 0.0002 | [-0.0006, 0.0009] | 1/6/3 |
| Amazon-ratings | combined | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [-0.0007, 0.0008] | 1/4/5 |
| Amazon-ratings | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0002 | [-0.0006, 0.0009] | 1/6/3 |
| Minesweeper | reliability_only | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | reliability_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | reliability_only | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | reliability_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | node_feature_only | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | node_feature_only | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | node_feature_only | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | node_feature_only | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | combined | utility routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | combined | utility-checkpoint routing - validation-selected best expert | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | combined | utility routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |
| Minesweeper | combined | utility-checkpoint routing - validation-selected fixed alpha | 10 | 0.0000 | [0.0000, 0.0000] | 0/10/0 |

## Decision Rule

- Preference evidence: reliability-only AUC should be clearly above 0.5 and combined should exceed node-feature-only.
- Utility evidence: utility-threshold routing should exceed the validation-selected best expert or fixed-alpha baseline with a paired CI above zero.
- Training preference labels are generated from out-of-fold expert predictions to avoid in-sample expert leakage.
- Post-hoc utility uses a preference-selected checkpoint; utility-checkpoint routing separately selects the epoch by validation routed accuracy.
- Utility thresholds are conservative: near-optimal thresholds prefer fewer switches away from the stronger validation expert.
