# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: component_concat
- Reliability component dim: 16
- Component missing mode: zero_slot
- Iterative alpha type: channel
- Iterative alpha groups: n/a
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4997 | 159328 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4996 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4751 | 0.4713 | +0.0038 | 0.0073 | 0.4751 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4755 | 0.4713 | +0.0042 | 0.0078 | 0.4755 | 0.7639 | 0.0199 | 0.0114 | 0.0120 | 0.4915 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4978 | 150752 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4997 | 159328 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4996 | 150752 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4710 | 0.4713 | -0.0003 | 0.0035 | 0.4710 | 0.7495 | 0.0005 | 0.0015 | 0.0017 | 0.4995 | 150752 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4978 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8436 | 0.8195 | +0.0241 | 0.0023 | 0.8436 | 0.7827 | 0.0509 | 0.0357 | 0.0368 | 0.4859 | 159328 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8259 | 0.8195 | +0.0064 | 0.0051 | 0.8259 | 0.7952 | 0.0619 | 0.0351 | 0.0359 | 0.4996 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8236 | 0.8195 | +0.0041 | 0.0066 | 0.8236 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8441 | 0.8195 | +0.0246 | 0.0016 | 0.8441 | 0.7786 | 0.0483 | 0.0365 | 0.0377 | 0.5088 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8264 | 0.8195 | +0.0069 | 0.0037 | 0.8264 | 0.7945 | 0.0600 | 0.0355 | 0.0364 | 0.4937 | 150752 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8310 | 0.8195 | +0.0115 | 0.0041 | 0.8310 | 0.7668 | 0.0591 | 0.0571 | 0.0587 | 0.4902 | 159328 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8257 | 0.8195 | +0.0062 | 0.0068 | 0.8257 | 0.7789 | 0.0610 | 0.0520 | 0.0534 | 0.4731 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8195 | 0.8195 | +0.0000 | 0.0035 | 0.8195 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8337 | 0.8195 | +0.0142 | 0.0043 | 0.8337 | 0.7677 | 0.0622 | 0.0565 | 0.0581 | 0.5228 | 150752 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8237 | 0.8195 | +0.0042 | 0.0067 | 0.8237 | 0.7747 | 0.0515 | 0.0484 | 0.0498 | 0.4914 | 150752 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0142 | [+0.0081, +0.0204] | 3/0/0 | +0.0100 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0115 | [+0.0096, +0.0135] | 3/0/0 | +0.0016 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0042 | [-0.0074, +0.0158] | 2/0/1 | +0.2567 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0062 | [-0.0083, +0.0206] | 2/0/1 | +0.2068 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0100 | [+0.0024, +0.0176] | 3/0/0 | +0.0295 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0081 | [-0.0004, +0.0166] | 3/0/0 | +0.0552 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0205 | [+0.0052, +0.0359] | 3/0/0 | +0.0289 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0200 | [+0.0016, +0.0384] | 3/0/0 | +0.0427 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0028 | [-0.0101, +0.0158] | 2/0/1 | +0.4473 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | +0.0023 | [-0.0048, +0.0094] | 2/0/1 | +0.2967 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0177 | [+0.0105, +0.0249] | 3/0/0 | +0.0088 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0182 | [+0.0076, +0.0288] | 3/0/0 | +0.0178 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | -0.0003 | [-0.0014, +0.0009] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0003 | [-0.0014, +0.0009] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0003 | [-0.0014, +0.0009] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | +0.0004 | [-0.0013, +0.0020] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | -0.0038 | [-0.0202, +0.0126] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0038 | [-0.0202, +0.0126] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0038 | [-0.0202, +0.0126] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0042 | [-0.0138, +0.0222] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0042 | [-0.0138, +0.0222] | 1/2/0 | +0.4226 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0041 | [-0.0060, +0.0141] | 2/1/0 | +0.2254 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0104 | [+0.0022, +0.0185] | 3/0/0 | +0.0318 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0125 | [-0.0000, +0.0251] | 3/0/0 | +0.0501 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0026 | [-0.0088, +0.0140] | 2/0/1 | +0.4229 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0002 | [-0.0060, +0.0064] | 1/0/2 | +0.9139 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0038 | [-0.0126, +0.0202] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0045 | [-0.0130, +0.0219] | 2/1/0 | +0.3865 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
