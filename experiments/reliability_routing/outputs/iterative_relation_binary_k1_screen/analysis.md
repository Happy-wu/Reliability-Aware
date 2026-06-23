# Representation Control Screening

- Datasets: Minesweeper, Tolokers, Questions
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial scalar-alpha adjustment: n/a
- Iterative relation steps: 1
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.
- `iterative_relation_frozen/fixed` is the same selected hidden baseline with zero relation correction.
- `iterative_relation_finetune/fixed` fine-tunes the fixed mixing architecture without a relation controller.

## Summary

| Dataset | Metric | Family | Control | Primary | Baseline | Delta | Std | Accuracy | Alpha | Adjustment | Relation/Base | Update gate | Active ctrl params | Backbone params |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Minesweeper | roc_auc | iterative_relation_finetune | constant_reliability | 0.9069 | 0.9069 | -0.0000 | 0.0014 | 0.8608 | 0.6667 | 0.0000 | 0.0000 | 0.4954 | 157568 | 75906 |
| Minesweeper | roc_auc | iterative_relation_finetune | feature_only | 0.9069 | 0.9069 | +0.0000 | 0.0014 | 0.8608 | 0.6667 | 0.0000 | 0.0000 | 0.4960 | 156544 | 75906 |
| Minesweeper | roc_auc | iterative_relation_finetune | fixed | 0.9070 | 0.9069 | +0.0000 | 0.0013 | 0.8609 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 75906 |
| Minesweeper | roc_auc | iterative_relation_finetune | reliability_only | 0.9069 | 0.9069 | +0.0000 | 0.0014 | 0.8608 | 0.6667 | 0.0000 | 0.0000 | 0.4960 | 157568 | 75906 |
| Minesweeper | roc_auc | iterative_relation_finetune | shuffled_reliability | 0.9069 | 0.9069 | +0.0000 | 0.0014 | 0.8608 | 0.6667 | 0.0000 | 0.0000 | 0.4960 | 157568 | 75906 |
| Minesweeper | roc_auc | iterative_relation_frozen | constant_reliability | 0.9074 | 0.9069 | +0.0005 | 0.0028 | 0.8613 | 0.6715 | 0.0254 | 0.1351 | 0.4942 | 157568 | 0 |
| Minesweeper | roc_auc | iterative_relation_frozen | feature_only | 0.9073 | 0.9069 | +0.0004 | 0.0022 | 0.8597 | 0.6712 | 0.0186 | 0.0997 | 0.5007 | 156544 | 0 |
| Minesweeper | roc_auc | iterative_relation_frozen | fixed | 0.9069 | 0.9069 | +0.0000 | 0.0014 | 0.8608 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Minesweeper | roc_auc | iterative_relation_frozen | reliability_only | 0.9073 | 0.9069 | +0.0003 | 0.0020 | 0.8604 | 0.6676 | 0.0050 | 0.0286 | 0.4871 | 157568 | 0 |
| Minesweeper | roc_auc | iterative_relation_frozen | shuffled_reliability | 0.9069 | 0.9069 | -0.0000 | 0.0018 | 0.8611 | 0.6682 | 0.0063 | 0.0370 | 0.4827 | 157568 | 0 |
| Questions | roc_auc | iterative_relation_finetune | constant_reliability | 0.7777 | 0.7777 | +0.0000 | 0.0094 | 0.9716 | 0.7500 | 0.0000 | 0.0000 | 0.5035 | 157568 | 94722 |
| Questions | roc_auc | iterative_relation_finetune | feature_only | 0.7777 | 0.7777 | -0.0000 | 0.0094 | 0.9716 | 0.7500 | 0.0000 | 0.0000 | 0.5050 | 156544 | 94722 |
| Questions | roc_auc | iterative_relation_finetune | fixed | 0.7781 | 0.7777 | +0.0003 | 0.0098 | 0.9708 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 94722 |
| Questions | roc_auc | iterative_relation_finetune | reliability_only | 0.7792 | 0.7777 | +0.0015 | 0.0090 | 0.9716 | 0.7463 | 0.0037 | 0.1096 | 0.5227 | 157568 | 94722 |
| Questions | roc_auc | iterative_relation_finetune | shuffled_reliability | 0.7777 | 0.7777 | -0.0000 | 0.0094 | 0.9716 | 0.7500 | 0.0000 | 0.0000 | 0.5031 | 157568 | 94722 |
| Questions | roc_auc | iterative_relation_frozen | constant_reliability | 0.7771 | 0.7777 | -0.0006 | 0.0100 | 0.9715 | 0.7489 | 0.0042 | 0.0226 | 0.5042 | 157568 | 0 |
| Questions | roc_auc | iterative_relation_frozen | feature_only | 0.7766 | 0.7777 | -0.0012 | 0.0106 | 0.9714 | 0.7482 | 0.0069 | 0.0364 | 0.5077 | 156544 | 0 |
| Questions | roc_auc | iterative_relation_frozen | fixed | 0.7777 | 0.7777 | +0.0000 | 0.0094 | 0.9716 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Questions | roc_auc | iterative_relation_frozen | reliability_only | 0.7779 | 0.7777 | +0.0002 | 0.0098 | 0.9712 | 0.7409 | 0.0115 | 0.2171 | 0.5301 | 157568 | 0 |
| Questions | roc_auc | iterative_relation_frozen | shuffled_reliability | 0.7767 | 0.7777 | -0.0010 | 0.0104 | 0.9714 | 0.7480 | 0.0069 | 0.0365 | 0.5032 | 157568 | 0 |
| Tolokers | roc_auc | iterative_relation_finetune | constant_reliability | 0.8542 | 0.8470 | +0.0072 | 0.0049 | 0.8263 | 0.9269 | 0.0172 | 0.1379 | 0.4873 | 157568 | 76098 |
| Tolokers | roc_auc | iterative_relation_finetune | feature_only | 0.8538 | 0.8470 | +0.0068 | 0.0051 | 0.8274 | 0.9203 | 0.0139 | 0.1480 | 0.4349 | 156544 | 76098 |
| Tolokers | roc_auc | iterative_relation_finetune | fixed | 0.8538 | 0.8470 | +0.0067 | 0.0053 | 0.8252 | 0.9167 | 0.0000 | 0.0000 | 0.0000 | 0 | 76098 |
| Tolokers | roc_auc | iterative_relation_finetune | reliability_only | 0.8519 | 0.8470 | +0.0049 | 0.0052 | 0.8231 | 0.9130 | 0.0146 | 0.2039 | 0.4858 | 157568 | 76098 |
| Tolokers | roc_auc | iterative_relation_finetune | shuffled_reliability | 0.8478 | 0.8470 | +0.0008 | 0.0040 | 0.8214 | 0.9040 | 0.0216 | 0.3628 | 0.5029 | 157568 | 76098 |
| Tolokers | roc_auc | iterative_relation_frozen | constant_reliability | 0.8470 | 0.8470 | -0.0001 | 0.0073 | 0.8201 | 0.9136 | 0.0269 | 0.1274 | 0.5078 | 157568 | 0 |
| Tolokers | roc_auc | iterative_relation_frozen | feature_only | 0.8467 | 0.8470 | -0.0004 | 0.0064 | 0.8205 | 0.9026 | 0.0379 | 0.1837 | 0.5278 | 156544 | 0 |
| Tolokers | roc_auc | iterative_relation_frozen | fixed | 0.8470 | 0.8470 | +0.0000 | 0.0075 | 0.8210 | 0.9167 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Tolokers | roc_auc | iterative_relation_frozen | reliability_only | 0.8465 | 0.8470 | -0.0005 | 0.0079 | 0.8204 | 0.9053 | 0.0341 | 0.1674 | 0.4940 | 157568 | 0 |
| Tolokers | roc_auc | iterative_relation_frozen | shuffled_reliability | 0.8466 | 0.8470 | -0.0004 | 0.0080 | 0.8203 | 0.9005 | 0.0287 | 0.1355 | 0.4977 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Minesweeper | iterative_relation_frozen | feature_only - fixed | +0.0004 | [-0.0025, +0.0033] | 1/1/1 | +0.6269 |
| Minesweeper | iterative_relation_frozen | reliability_only - fixed | +0.0003 | [-0.0018, +0.0025] | 1/0/2 | +0.5719 |
| Minesweeper | iterative_relation_frozen | shuffled_reliability - fixed | -0.0000 | [-0.0020, +0.0020] | 1/0/2 | +0.9705 |
| Minesweeper | iterative_relation_frozen | constant_reliability - fixed | +0.0005 | [-0.0048, +0.0057] | 1/0/2 | +0.7394 |
| Minesweeper | iterative_relation_frozen | reliability_only - feature_only | -0.0000 | [-0.0009, +0.0008] | 1/0/2 | +0.8250 |
| Minesweeper | iterative_relation_frozen | true reliability - shuffled reliability | +0.0004 | [-0.0003, +0.0010] | 3/0/0 | +0.1303 |
| Minesweeper | iterative_relation_frozen | true reliability - constant reliability | -0.0001 | [-0.0032, +0.0030] | 2/0/1 | +0.8797 |
| Minesweeper | iterative_relation_finetune | feature_only - fixed | -0.0000 | [-0.0002, +0.0001] | 0/2/1 | +0.4226 |
| Minesweeper | iterative_relation_finetune | reliability_only - fixed | -0.0000 | [-0.0002, +0.0001] | 0/2/1 | +0.4226 |
| Minesweeper | iterative_relation_finetune | shuffled_reliability - fixed | -0.0000 | [-0.0002, +0.0001] | 0/2/1 | +0.4226 |
| Minesweeper | iterative_relation_finetune | constant_reliability - fixed | -0.0000 | [-0.0002, +0.0001] | 0/2/1 | +0.4226 |
| Minesweeper | iterative_relation_finetune | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Minesweeper | iterative_relation_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Minesweeper | iterative_relation_finetune | true reliability - constant reliability | +0.0000 | [-0.0000, +0.0000] | 1/2/0 | +0.4226 |
| Tolokers | iterative_relation_frozen | feature_only - fixed | -0.0004 | [-0.0045, +0.0038] | 2/0/1 | +0.7507 |
| Tolokers | iterative_relation_frozen | reliability_only - fixed | -0.0005 | [-0.0025, +0.0014] | 1/0/2 | +0.3660 |
| Tolokers | iterative_relation_frozen | shuffled_reliability - fixed | -0.0004 | [-0.0048, +0.0040] | 1/1/1 | +0.7275 |
| Tolokers | iterative_relation_frozen | constant_reliability - fixed | -0.0001 | [-0.0017, +0.0016] | 1/1/1 | +0.8958 |
| Tolokers | iterative_relation_frozen | reliability_only - feature_only | -0.0002 | [-0.0048, +0.0044] | 1/0/2 | +0.8836 |
| Tolokers | iterative_relation_frozen | true reliability - shuffled reliability | -0.0001 | [-0.0061, +0.0059] | 1/0/2 | +0.9398 |
| Tolokers | iterative_relation_frozen | true reliability - constant reliability | -0.0005 | [-0.0023, +0.0013] | 1/0/2 | +0.3725 |
| Tolokers | iterative_relation_finetune | feature_only - fixed | +0.0000 | [-0.0009, +0.0009] | 1/1/1 | +0.8901 |
| Tolokers | iterative_relation_finetune | reliability_only - fixed | -0.0019 | [-0.0070, +0.0033] | 0/1/2 | +0.2575 |
| Tolokers | iterative_relation_finetune | shuffled_reliability - fixed | -0.0059 | [-0.0202, +0.0083] | 1/0/2 | +0.2146 |
| Tolokers | iterative_relation_finetune | constant_reliability - fixed | +0.0004 | [-0.0031, +0.0039] | 1/1/1 | +0.6658 |
| Tolokers | iterative_relation_finetune | reliability_only - feature_only | -0.0019 | [-0.0077, +0.0039] | 0/1/2 | +0.2931 |
| Tolokers | iterative_relation_finetune | true reliability - shuffled reliability | +0.0041 | [-0.0061, +0.0143] | 2/0/1 | +0.2271 |
| Tolokers | iterative_relation_finetune | true reliability - constant reliability | -0.0023 | [-0.0105, +0.0059] | 0/1/2 | +0.3551 |
| Questions | iterative_relation_frozen | feature_only - fixed | -0.0012 | [-0.0062, +0.0038] | 1/0/2 | +0.4227 |
| Questions | iterative_relation_frozen | reliability_only - fixed | +0.0002 | [-0.0055, +0.0059] | 1/0/2 | +0.8862 |
| Questions | iterative_relation_frozen | shuffled_reliability - fixed | -0.0010 | [-0.0054, +0.0034] | 1/0/2 | +0.4227 |
| Questions | iterative_relation_frozen | constant_reliability - fixed | -0.0006 | [-0.0034, +0.0021] | 1/0/2 | +0.4227 |
| Questions | iterative_relation_frozen | reliability_only - feature_only | +0.0014 | [-0.0019, +0.0046] | 2/1/0 | +0.2093 |
| Questions | iterative_relation_frozen | true reliability - shuffled reliability | +0.0012 | [-0.0020, +0.0045] | 2/1/0 | +0.2427 |
| Questions | iterative_relation_frozen | true reliability - constant reliability | +0.0009 | [-0.0029, +0.0046] | 1/1/1 | +0.4309 |
| Questions | iterative_relation_finetune | feature_only - fixed | -0.0003 | [-0.0017, +0.0011] | 0/2/1 | +0.4226 |
| Questions | iterative_relation_finetune | reliability_only - fixed | +0.0011 | [-0.0060, +0.0082] | 1/0/2 | +0.5639 |
| Questions | iterative_relation_finetune | shuffled_reliability - fixed | -0.0003 | [-0.0017, +0.0011] | 0/1/2 | +0.4225 |
| Questions | iterative_relation_finetune | constant_reliability - fixed | -0.0003 | [-0.0017, +0.0011] | 1/0/2 | +0.4226 |
| Questions | iterative_relation_finetune | reliability_only - feature_only | +0.0015 | [-0.0048, +0.0077] | 2/0/1 | +0.4227 |
| Questions | iterative_relation_finetune | true reliability - shuffled reliability | +0.0015 | [-0.0048, +0.0077] | 2/1/0 | +0.4226 |
| Questions | iterative_relation_finetune | true reliability - constant reliability | +0.0015 | [-0.0048, +0.0077] | 1/1/1 | +0.4226 |
| Minesweeper | iterative_relation_protocol | fixed: finetune - frozen | +0.0000 | [-0.0001, +0.0002] | 1/2/0 | +0.4226 |
| Minesweeper | iterative_relation_protocol | feature_only: finetune - frozen | -0.0004 | [-0.0033, +0.0025] | 1/1/1 | +0.6269 |
| Minesweeper | iterative_relation_protocol | reliability_only: finetune - frozen | -0.0003 | [-0.0025, +0.0018] | 2/0/1 | +0.5719 |
| Minesweeper | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0000 | [-0.0020, +0.0020] | 2/0/1 | +0.9705 |
| Minesweeper | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0005 | [-0.0057, +0.0048] | 2/0/1 | +0.7394 |
| Tolokers | iterative_relation_protocol | fixed: finetune - frozen | +0.0067 | [-0.0126, +0.0260] | 2/1/0 | +0.2716 |
| Tolokers | iterative_relation_protocol | feature_only: finetune - frozen | +0.0071 | [-0.0120, +0.0262] | 2/0/1 | +0.2498 |
| Tolokers | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0054 | [-0.0107, +0.0215] | 2/0/1 | +0.2847 |
| Tolokers | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0012 | [-0.0116, +0.0140] | 2/0/1 | +0.7231 |
| Tolokers | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0072 | [-0.0154, +0.0298] | 2/0/1 | +0.3038 |
| Questions | iterative_relation_protocol | fixed: finetune - frozen | +0.0003 | [-0.0011, +0.0017] | 1/2/0 | +0.4226 |
| Questions | iterative_relation_protocol | feature_only: finetune - frozen | +0.0012 | [-0.0038, +0.0062] | 1/1/1 | +0.4227 |
| Questions | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0012 | [-0.0014, +0.0039] | 3/0/0 | +0.1843 |
| Questions | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0010 | [-0.0034, +0.0054] | 1/1/1 | +0.4227 |
| Questions | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0006 | [-0.0021, +0.0034] | 2/1/0 | +0.4226 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
