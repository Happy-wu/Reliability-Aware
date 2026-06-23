# Internal Branch Diagnosis

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Controls: feature_only, shuffled_reliability, constant_reliability

## Group Summary

| Dataset | Family | Control | Acc delta (pp) | Corrected | Harmed | Alpha abs | Channel std | Relation/base | Weighted shift AUC | Changed-pred AUC |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | constant_reliability | 0.1160 | 0.0320 | 0.0308 | 0.0378 | 0.0319 | 0.1444 | n/a | 0.5349 |
| Amazon-ratings | iterative_relation_finetune | feature_only | 0.2221 | 0.0255 | 0.0233 | 0.0290 | 0.0260 | 0.1043 | n/a | 0.5088 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability | 0.2972 | 0.0328 | 0.0298 | 0.0424 | 0.0360 | 0.1574 | n/a | 0.5206 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability | -0.0049 | 0.0036 | 0.0037 | 0.0037 | 0.0041 | 0.0312 | n/a | 0.5430 |
| Amazon-ratings | iterative_relation_frozen | feature_only | -0.0474 | 0.0058 | 0.0063 | 0.0049 | 0.0068 | 0.0298 | n/a | 0.5245 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability | 0.0212 | 0.0033 | 0.0031 | 0.0035 | 0.0040 | 0.0288 | n/a | 0.5422 |
| Roman-empire | iterative_relation_finetune | constant_reliability | 0.3830 | 0.0159 | 0.0121 | 0.0516 | 0.0451 | 0.3821 | n/a | 0.4888 |
| Roman-empire | iterative_relation_finetune | feature_only | 0.4748 | 0.0177 | 0.0129 | 0.0519 | 0.0466 | 0.4140 | n/a | 0.4978 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability | 0.2700 | 0.0166 | 0.0139 | 0.0512 | 0.0456 | 0.4167 | n/a | 0.5052 |
| Roman-empire | iterative_relation_frozen | constant_reliability | 0.6195 | 0.0215 | 0.0153 | 0.0507 | 0.0540 | 0.4302 | n/a | 0.5414 |
| Roman-empire | iterative_relation_frozen | feature_only | 0.1888 | 0.0153 | 0.0134 | 0.0362 | 0.0386 | 0.2986 | n/a | 0.5519 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability | 0.1977 | 0.0126 | 0.0107 | 0.0271 | 0.0288 | 0.2436 | n/a | 0.5351 |

## Interpretation Notes

- `Weighted shift AUC` preserves channel importance by weighting the local/global direction with branch disagreement energy.
- `Changed-pred AUC` asks whether large channel-wise adjustment identifies nodes whose final prediction differs from the fixed model.
- Association with corrected nodes is descriptive and does not establish a causal channel attribution.
