# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: component_concat
- Reliability component dim: 16
- Component missing mode: zero_slot
- Max adjustment: 0.1
- Initial scalar-alpha adjustment: n/a
- Iterative relation steps: 1
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.
- External local/global expert logits are not embedded; node diagnostics support internal branch analysis but do not by themselves guarantee preference-alignment availability.
- `relation_relative_strength` and `relation_to_branch_disagreement` are the stable relation-magnitude diagnostics. Per-node `relation_to_base_norm` is retained only as an auxiliary diagnostic because small base norms can inflate it.
- `iterative_relation_frozen/fixed` is the same selected hidden baseline with zero relation correction.
- `iterative_relation_finetune/fixed` fine-tunes the fixed mixing architecture without a relation controller.

## Summary

| Dataset | Metric | Family | Control | Primary | Baseline | Delta | Std | Accuracy | Alpha | Adjustment | Relation strength | Relation/disagreement | Update gate | Active ctrl params | Backbone params |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4778 | 0.4716 | +0.0062 | 0.0098 | 0.4778 | 0.6935 | 0.0456 | 0.0331 | 0.0346 | 0.5033 | 159328 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4745 | 0.4716 | +0.0029 | 0.0061 | 0.4745 | 0.6940 | 0.0509 | 0.0410 | 0.0430 | 0.5592 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4771 | 0.4716 | +0.0054 | 0.0088 | 0.4771 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4740 | 0.4716 | +0.0024 | 0.0060 | 0.4740 | 0.6912 | 0.0470 | 0.0375 | 0.0392 | 0.5566 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4762 | 0.4716 | +0.0046 | 0.0089 | 0.4762 | 0.6953 | 0.0481 | 0.0362 | 0.0379 | 0.5384 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4724 | 0.4716 | +0.0008 | 0.0035 | 0.4724 | 0.6667 | 0.0016 | 0.0022 | 0.0023 | 0.4928 | 159328 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4723 | 0.4716 | +0.0007 | 0.0036 | 0.4723 | 0.6666 | 0.0015 | 0.0022 | 0.0023 | 0.4934 | 150752 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4716 | 0.4716 | +0.0000 | 0.0045 | 0.4716 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4724 | 0.4716 | +0.0008 | 0.0035 | 0.4724 | 0.6666 | 0.0015 | 0.0022 | 0.0023 | 0.4916 | 150752 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4723 | 0.4716 | +0.0007 | 0.0037 | 0.4723 | 0.6666 | 0.0015 | 0.0022 | 0.0023 | 0.4916 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8441 | 0.8199 | +0.0242 | 0.0057 | 0.8441 | 0.7816 | 0.0529 | 0.0416 | 0.0429 | 0.5010 | 159328 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8212 | 0.8199 | +0.0012 | 0.0068 | 0.8212 | 0.7665 | 0.0218 | 0.0116 | 0.0118 | 0.4930 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8237 | 0.8199 | +0.0038 | 0.0074 | 0.8237 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8451 | 0.8199 | +0.0252 | 0.0048 | 0.8451 | 0.7763 | 0.0491 | 0.0407 | 0.0420 | 0.5000 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8211 | 0.8199 | +0.0012 | 0.0067 | 0.8211 | 0.7639 | 0.0195 | 0.0121 | 0.0124 | 0.4844 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8310 | 0.8199 | +0.0111 | 0.0038 | 0.8310 | 0.7638 | 0.0584 | 0.0582 | 0.0597 | 0.4824 | 159328 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8255 | 0.8199 | +0.0056 | 0.0059 | 0.8255 | 0.7784 | 0.0613 | 0.0520 | 0.0534 | 0.4413 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8199 | 0.8199 | +0.0000 | 0.0051 | 0.8199 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8370 | 0.8199 | +0.0171 | 0.0034 | 0.8370 | 0.7682 | 0.0609 | 0.0547 | 0.0562 | 0.5066 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8224 | 0.8199 | +0.0025 | 0.0063 | 0.8224 | 0.7745 | 0.0499 | 0.0448 | 0.0460 | 0.4757 | 150752 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0171 | [+0.0119, +0.0223] | 3/0/0 | +0.0050 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0111 | [+0.0031, +0.0192] | 3/0/0 | +0.0272 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0025 | [-0.0070, +0.0120] | 2/0/1 | +0.3789 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0056 | [-0.0028, +0.0140] | 3/0/0 | +0.1040 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0146 | [+0.0029, +0.0263] | 3/0/0 | +0.0329 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0115 | [+0.0011, +0.0218] | 3/0/0 | +0.0414 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0214 | [+0.0130, +0.0298] | 3/0/0 | +0.0083 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0204 | [+0.0133, +0.0275] | 3/0/0 | +0.0065 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | -0.0026 | [-0.0088, +0.0035] | 0/1/2 | +0.2069 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0026 | [-0.0087, +0.0036] | 0/1/2 | +0.2123 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0240 | [+0.0148, +0.0332] | 3/0/0 | +0.0079 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0239 | [+0.0145, +0.0334] | 3/0/0 | +0.0083 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0008 | [-0.0025, +0.0040] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0008 | [-0.0025, +0.0040] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0007 | [-0.0023, +0.0038] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | +0.0001 | [-0.0004, +0.0006] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | +0.0001 | [-0.0002, +0.0003] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0030 | [-0.0217, +0.0156] | 1/1/1 | +0.5545 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0007 | [-0.0034, +0.0049] | 1/1/1 | +0.5389 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0009 | [-0.0053, +0.0036] | 1/1/1 | +0.4899 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0026 | [-0.0139, +0.0088] | 1/1/1 | +0.4348 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | -0.0022 | [-0.0242, +0.0198] | 1/1/1 | +0.7117 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | -0.0005 | [-0.0081, +0.0071] | 1/1/1 | +0.8070 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0038 | [-0.0046, +0.0123] | 2/1/0 | +0.1912 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0081 | [+0.0020, +0.0142] | 3/0/0 | +0.0291 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0131 | [+0.0036, +0.0225] | 3/0/0 | +0.0273 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | -0.0013 | [-0.0109, +0.0083] | 1/1/1 | +0.6211 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0044 | [-0.0136, +0.0049] | 0/0/3 | +0.1805 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0054 | [-0.0076, +0.0185] | 2/1/0 | +0.2137 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0016 | [-0.0128, +0.0161] | 1/0/2 | +0.6753 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0054 | [-0.0137, +0.0245] | 2/0/1 | +0.3480 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0039 | [-0.0120, +0.0199] | 2/0/1 | +0.4015 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0022 | [-0.0080, +0.0124] | 2/0/1 | +0.4548 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
