# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: component_aligned
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4767 | 0.4685 | +0.0082 | 0.0088 | 0.4767 | 0.8641 | 0.0461 | 0.0311 | 0.0325 | 0.5320 | 209152 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.5117 | 200576 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4741 | 0.4685 | +0.0056 | 0.0087 | 0.4741 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4737 | 0.4685 | +0.0052 | 0.0074 | 0.4737 | 0.8638 | 0.0463 | 0.0314 | 0.0327 | 0.5601 | 200576 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4717 | 0.4685 | +0.0032 | 0.0076 | 0.4717 | 0.8501 | 0.0233 | 0.0127 | 0.0132 | 0.5395 | 200576 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.5150 | 209152 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4678 | 0.4685 | -0.0007 | 0.0043 | 0.4678 | 0.8328 | 0.0006 | 0.0020 | 0.0024 | 0.5121 | 200576 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.5120 | 200576 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.5121 | 200576 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8400 | 0.8174 | +0.0226 | 0.0073 | 0.8400 | 0.7863 | 0.0579 | 0.0417 | 0.0431 | 0.4727 | 209152 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8266 | 0.8174 | +0.0092 | 0.0070 | 0.8266 | 0.7934 | 0.0635 | 0.0433 | 0.0445 | 0.4795 | 200576 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8224 | 0.8174 | +0.0050 | 0.0004 | 0.8224 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8400 | 0.8174 | +0.0226 | 0.0060 | 0.8400 | 0.7833 | 0.0561 | 0.0422 | 0.0436 | 0.4647 | 200576 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8255 | 0.8174 | +0.0081 | 0.0072 | 0.8255 | 0.7907 | 0.0608 | 0.0415 | 0.0427 | 0.4746 | 200576 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8342 | 0.8174 | +0.0168 | 0.0049 | 0.8342 | 0.7677 | 0.0599 | 0.0582 | 0.0598 | 0.5068 | 209152 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8267 | 0.8174 | +0.0093 | 0.0070 | 0.8267 | 0.7795 | 0.0623 | 0.0517 | 0.0531 | 0.4689 | 200576 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8174 | 0.8174 | +0.0000 | 0.0035 | 0.8174 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8361 | 0.8174 | +0.0187 | 0.0041 | 0.8361 | 0.7682 | 0.0620 | 0.0554 | 0.0569 | 0.5084 | 200576 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8230 | 0.8174 | +0.0056 | 0.0073 | 0.8230 | 0.7768 | 0.0461 | 0.0410 | 0.0422 | 0.5003 | 200576 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0187 | [+0.0142, +0.0233] | 3/0/0 | +0.0032 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0168 | [+0.0094, +0.0243] | 3/0/0 | +0.0104 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0056 | [-0.0060, +0.0173] | 3/0/0 | +0.1717 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0093 | [-0.0015, +0.0201] | 3/0/0 | +0.0654 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0131 | [+0.0007, +0.0254] | 3/0/0 | +0.0450 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0094 | [-0.0020, +0.0208] | 3/0/0 | +0.0713 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0176 | [-0.0011, +0.0363] | 3/0/0 | +0.0561 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0176 | [-0.0053, +0.0405] | 3/0/0 | +0.0807 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0031 | [-0.0196, +0.0257] | 2/0/1 | +0.6204 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | +0.0042 | [-0.0179, +0.0264] | 1/1/1 | +0.4968 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0145 | [+0.0078, +0.0212] | 3/0/0 | +0.0113 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0134 | [+0.0094, +0.0173] | 3/0/0 | +0.0047 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | -0.0007 | [-0.0038, +0.0023] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | +0.0007 | [-0.0023, +0.0038] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0004 | [-0.0063, +0.0056] | 1/1/1 | +0.8084 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0027 | [-0.0167, +0.0220] | 1/1/1 | +0.6129 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0023 | [-0.0354, +0.0307] | 1/1/1 | +0.7893 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0056 | [-0.0294, +0.0183] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0020 | [-0.0251, +0.0291] | 1/1/1 | +0.7852 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0052 | [-0.0134, +0.0237] | 2/1/0 | +0.3526 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0050 | [-0.0065, +0.0165] | 2/1/0 | +0.2032 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0039 | [-0.0018, +0.0096] | 3/0/0 | +0.0994 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0058 | [-0.0113, +0.0229] | 2/0/1 | +0.2839 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0024 | [-0.0014, +0.0062] | 3/0/0 | +0.1135 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0001 | [-0.0071, +0.0069] | 2/0/1 | +0.9744 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0056 | [-0.0183, +0.0294] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0052 | [-0.0134, +0.0237] | 2/1/0 | +0.3526 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0082 | [-0.0096, +0.0260] | 2/1/0 | +0.1857 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0032 | [-0.0106, +0.0170] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0007 | [-0.0023, +0.0038] | 1/2/0 | +0.4226 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
