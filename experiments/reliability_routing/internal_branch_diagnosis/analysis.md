# Internal Branch Diagnosis

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Controls: reliability_only, combined

## Group Summary

| Dataset | Family | Control | Acc delta (pp) | Corrected | Harmed | Alpha abs | Channel std | Relation/base | Weighted shift AUC | Changed-pred AUC |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 0.2319 | 0.0275 | 0.0252 | 0.0272 | 0.0240 | 0.1111 | n/a | 0.4967 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 0.2401 | 0.0361 | 0.0337 | 0.0340 | 0.0291 | 0.1355 | n/a | 0.4926 |
| Amazon-ratings | iterative_relation_frozen | combined | -0.0849 | 0.0075 | 0.0083 | 0.0044 | 0.0059 | 0.0286 | n/a | 0.4948 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | -0.0735 | 0.0064 | 0.0072 | 0.0057 | 0.0078 | 0.0407 | n/a | 0.5030 |
| Roman-empire | iterative_relation_finetune | combined | 2.2661 | 0.0404 | 0.0177 | 0.0474 | 0.0459 | 0.4266 | n/a | 0.4685 |
| Roman-empire | iterative_relation_finetune | reliability_only | 2.3297 | 0.0412 | 0.0179 | 0.0474 | 0.0474 | 0.4431 | n/a | 0.4867 |
| Roman-empire | iterative_relation_frozen | combined | 1.3766 | 0.0363 | 0.0225 | 0.0523 | 0.0575 | 0.4436 | n/a | 0.5448 |
| Roman-empire | iterative_relation_frozen | reliability_only | 1.5955 | 0.0363 | 0.0204 | 0.0534 | 0.0599 | 0.4457 | n/a | 0.5361 |

## Interpretation Notes

- `Weighted shift AUC` preserves channel importance by weighting the local/global direction with branch disagreement energy.
- `Changed-pred AUC` asks whether large channel-wise adjustment identifies nodes whose final prediction differs from the fixed model.
- Association with corrected nodes is descriptive and does not establish a causal channel attribution.
