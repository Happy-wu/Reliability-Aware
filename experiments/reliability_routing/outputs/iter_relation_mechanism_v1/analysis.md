# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 10
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4726 | 0.4665 | +0.0062 | 0.0104 | 0.4726 | 0.8181 | 0.0273 | 0.2356 | 0.5040 | 166144 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4715 | 0.4665 | +0.0050 | 0.0100 | 0.4715 | 0.8248 | 0.0378 | 0.2980 | 0.5275 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | feature_only | 0.4725 | 0.4665 | +0.0061 | 0.0104 | 0.4725 | 0.8180 | 0.0290 | 0.2244 | 0.5333 | 156544 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4703 | 0.4665 | +0.0039 | 0.0089 | 0.4703 | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4727 | 0.4665 | +0.0063 | 0.0128 | 0.4727 | 0.8238 | 0.0340 | 0.2921 | 0.5098 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4733 | 0.4665 | +0.0068 | 0.0105 | 0.4733 | 0.8294 | 0.0424 | 0.3451 | 0.5315 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4656 | 0.4665 | -0.0008 | 0.0083 | 0.4656 | 0.7982 | 0.0044 | 29752833.3248 | 0.4913 | 166144 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4664 | 0.4665 | -0.0000 | 0.0083 | 0.4664 | 0.7998 | 0.0037 | 0.0333 | 0.4917 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | feature_only | 0.4660 | 0.4665 | -0.0005 | 0.0081 | 0.4660 | 0.7974 | 0.0049 | 24321734.3564 | 0.4954 | 156544 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4665 | 0.4665 | +0.0000 | 0.0083 | 0.4665 | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4657 | 0.4665 | -0.0007 | 0.0083 | 0.4657 | 0.7979 | 0.0057 | 25320328.0366 | 0.4949 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4667 | 0.4665 | +0.0002 | 0.0086 | 0.4667 | 0.7999 | 0.0035 | 0.0331 | 0.4935 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8436 | 0.8169 | +0.0267 | 0.0049 | 0.8436 | 0.8004 | 0.0474 | 165696.8727 | 0.5052 | 166144 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8248 | 0.8169 | +0.0078 | 0.0076 | 0.8248 | 0.8079 | 0.0516 | 148059.8611 | 0.5057 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | feature_only | 0.8257 | 0.8169 | +0.0088 | 0.0079 | 0.8257 | 0.8055 | 0.0519 | 47201.9905 | 0.5194 | 156544 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8209 | 0.8169 | +0.0040 | 0.0088 | 0.8209 | 0.7750 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8442 | 0.8169 | +0.0273 | 0.0050 | 0.8442 | 0.7978 | 0.0474 | 56652.8223 | 0.5243 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8236 | 0.8169 | +0.0067 | 0.0072 | 0.8236 | 0.8049 | 0.0513 | 41285.9710 | 0.5073 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8307 | 0.8169 | +0.0138 | 0.0062 | 0.8307 | 0.7828 | 0.0523 | 816619.5761 | 0.4677 | 166144 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8231 | 0.8169 | +0.0062 | 0.0064 | 0.8231 | 0.7948 | 0.0507 | 370.8278 | 0.4223 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | feature_only | 0.8188 | 0.8169 | +0.0019 | 0.0055 | 0.8188 | 0.7897 | 0.0362 | 242695.1833 | 0.4399 | 156544 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8169 | 0.8169 | +0.0000 | 0.0056 | 0.8169 | 0.7750 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8329 | 0.8169 | +0.0160 | 0.0067 | 0.8329 | 0.7822 | 0.0534 | 525195.5811 | 0.4832 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8189 | 0.8169 | +0.0020 | 0.0056 | 0.8189 | 0.7878 | 0.0271 | 958.5380 | 0.4506 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | feature_only - fixed | +0.0019 | [-0.0002, +0.0040] | 6/2/2 | +0.0716 |
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0160 | [+0.0130, +0.0189] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0138 | [+0.0121, +0.0154] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0020 | [-0.0001, +0.0040] | 6/2/2 | +0.0562 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0062 | [+0.0034, +0.0089] | 9/1/0 | +0.0007 |
| Roman-empire | iterative_relation_frozen | reliability_only - feature_only | +0.0141 | [+0.0115, +0.0167] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0140 | [+0.0114, +0.0166] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0098 | [+0.0077, +0.0118] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | combined - feature_only | +0.0119 | [+0.0094, +0.0143] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | feature_only - fixed | +0.0047 | [+0.0004, +0.0091] | 8/1/1 | +0.0346 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0233 | [+0.0170, +0.0296] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0227 | [+0.0168, +0.0285] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0027 | [-0.0000, +0.0054] | 7/1/2 | +0.0514 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | +0.0038 | [+0.0009, +0.0068] | 7/1/2 | +0.0159 |
| Roman-empire | iterative_relation_finetune | reliability_only - feature_only | +0.0185 | [+0.0145, +0.0226] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0206 | [+0.0162, +0.0250] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0195 | [+0.0145, +0.0245] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | combined - feature_only | +0.0179 | [+0.0143, +0.0215] | 10/0/0 | +0.0000 |
| Amazon-ratings | iterative_relation_frozen | feature_only - fixed | -0.0005 | [-0.0020, +0.0011] | 2/6/2 | +0.4997 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | -0.0007 | [-0.0026, +0.0011] | 2/5/3 | +0.3918 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | -0.0008 | [-0.0034, +0.0017] | 3/5/2 | +0.4736 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0002 | [-0.0008, +0.0012] | 2/7/1 | +0.6427 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | -0.0000 | [-0.0003, +0.0002] | 2/7/1 | +0.6637 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - feature_only | -0.0003 | [-0.0010, +0.0005] | 1/5/4 | +0.4319 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0009 | [-0.0025, +0.0006] | 0/5/5 | +0.1996 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0007 | [-0.0025, +0.0011] | 1/5/4 | +0.4058 |
| Amazon-ratings | iterative_relation_frozen | combined - feature_only | -0.0004 | [-0.0015, +0.0007] | 2/5/3 | +0.4635 |
| Amazon-ratings | iterative_relation_finetune | feature_only - fixed | +0.0022 | [-0.0025, +0.0069] | 4/5/1 | +0.3126 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | +0.0024 | [-0.0030, +0.0078] | 5/4/1 | +0.3405 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0023 | [-0.0025, +0.0071] | 4/5/1 | +0.3010 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | +0.0030 | [+0.0001, +0.0058] | 5/4/1 | +0.0433 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | +0.0012 | [-0.0029, +0.0052] | 5/4/1 | +0.5337 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - feature_only | +0.0002 | [-0.0064, +0.0068] | 4/4/2 | +0.9521 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | -0.0006 | [-0.0062, +0.0050] | 2/4/4 | +0.8230 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0012 | [-0.0052, +0.0077] | 3/4/3 | +0.6721 |
| Amazon-ratings | iterative_relation_finetune | combined - feature_only | +0.0001 | [-0.0006, +0.0008] | 2/6/2 | +0.7493 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0040 | [+0.0013, +0.0067] | 7/3/0 | +0.0082 |
| Roman-empire | iterative_relation_protocol | feature_only: finetune - frozen | +0.0069 | [+0.0019, +0.0118] | 9/0/1 | +0.0118 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0113 | [+0.0056, +0.0171] | 10/0/0 | +0.0015 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0129 | [+0.0085, +0.0173] | 10/0/0 | +0.0001 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0047 | [+0.0015, +0.0080] | 8/0/2 | +0.0090 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0016 | [-0.0028, +0.0061] | 6/0/4 | +0.4228 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0039 | [-0.0001, +0.0079] | 4/6/0 | +0.0557 |
| Amazon-ratings | iterative_relation_protocol | feature_only: finetune - frozen | +0.0066 | [+0.0008, +0.0123] | 6/3/1 | +0.0296 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0070 | [+0.0019, +0.0121] | 6/3/1 | +0.0130 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0070 | [+0.0011, +0.0130] | 6/3/1 | +0.0252 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0066 | [+0.0011, +0.0122] | 6/4/0 | +0.0241 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0051 | [+0.0007, +0.0095] | 5/4/1 | +0.0286 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
