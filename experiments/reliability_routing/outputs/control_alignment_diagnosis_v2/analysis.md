# Control Alignment Diagnosis

This report replays trained representation-control runs and checks whether
node-wise alpha aligns with frozen external local/global expert preference.

Important scope note: these alignment targets come from cached external
local/global experts, not from the representation model's internal
branch-level counterfactual utility.

## Summary

| Dataset | Family | Control | Runs | Suspect | Pref count | Local frac | Reprod delta | Max | Alpha std | Alpha AUC(local pref) | Alpha corr(pref) | Alpha corr(correct) | Alpha corr(local advantage) | Alpha gap(local-global) | Rel/Base | Update gate |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 3 | 3 | 2013.6667 | 0.4800 | -0.0142 | 0.0271 | 0.0015 | 0.5086 | 0.0552 | 0.0304 | -0.0373 | 0.0002 | 0.1823 | 0.4789 |
| Amazon-ratings | iterative_relation_finetune | feature_only | 3 | 3 | 2013.6667 | 0.4800 | -0.0032 | 0.0171 | 0.0027 | 0.4957 | 0.0144 | 0.0028 | -0.0154 | 0.0001 | 0.4051 | 0.5171 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 3 | 2 | 2013.6667 | 0.4800 | -0.0032 | 0.0080 | 0.0017 | 0.5018 | 0.0219 | 0.0123 | -0.0516 | 0.0001 | 0.1852 | 0.5006 |
| Amazon-ratings | iterative_relation_frozen | combined | 3 | 2 | 2013.6667 | 0.4800 | -0.0036 | 0.0069 | 0.0000 | 0.5000 | n/a | n/a | n/a | 0.0000 | 0.0000 | 0.4977 |
| Amazon-ratings | iterative_relation_frozen | feature_only | 3 | 2 | 2013.6667 | 0.4800 | -0.0029 | 0.0054 | 0.0000 | 0.5000 | n/a | n/a | n/a | 0.0000 | 0.0000 | 0.4967 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 3 | 3 | 2013.6667 | 0.4800 | -0.0022 | 0.0056 | 0.0005 | 0.4946 | -0.0432 | -0.0237 | -0.0062 | -0.0000 | 0.1524 | 0.4697 |
| Roman-empire | iterative_relation_finetune | combined | 3 | 3 | 2352.6667 | 0.1710 | 0.0007 | 0.0051 | 0.0048 | 0.5070 | 0.0224 | 0.0337 | 0.0353 | 0.0003 | 0.5377 | 0.5300 |
| Roman-empire | iterative_relation_finetune | feature_only | 3 | 3 | 2352.6667 | 0.1710 | -0.0082 | 0.0155 | 0.0002 | 0.4446 | -0.0854 | -0.0011 | 0.0248 | -0.0001 | 0.1846 | 0.4624 |
| Roman-empire | iterative_relation_finetune | reliability_only | 3 | 2 | 2352.6667 | 0.1710 | -0.0024 | 0.0049 | 0.0045 | 0.4735 | -0.0328 | -0.0063 | -0.0288 | -0.0005 | 0.5491 | 0.5130 |
| Roman-empire | iterative_relation_frozen | combined | 3 | 3 | 2352.6667 | 0.1710 | -0.0031 | 0.0042 | 0.0068 | 0.5787 | 0.1075 | 0.0594 | 0.1191 | 0.0020 | 0.6740 | 0.4830 |
| Roman-empire | iterative_relation_frozen | feature_only | 3 | 3 | 2352.6667 | 0.1710 | 0.0017 | 0.0056 | 0.0012 | 0.3807 | -0.1747 | -0.0946 | -0.0520 | -0.0005 | 0.4520 | 0.4314 |
| Roman-empire | iterative_relation_frozen | reliability_only | 3 | 1 | 2352.6667 | 0.1710 | -0.0009 | 0.0026 | 0.0060 | 0.5014 | -0.0049 | -0.0044 | 0.0362 | 0.0001 | 0.6823 | 0.4804 |
