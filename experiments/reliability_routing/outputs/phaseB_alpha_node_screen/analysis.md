# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: component_concat
- Reliability component dim: 16
- Component missing mode: zero_slot
- Iterative alpha type: node
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.5181 | 151138 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.5169 | 142562 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4722 | 0.4713 | +0.0009 | 0.0038 | 0.4722 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.5162 | 142562 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.5162 | 142562 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4714 | 0.4718 | -0.0003 | 0.0038 | 0.4714 | 0.7471 | 0.0042 | 0.0060 | 0.0068 | 0.5187 | 151138 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.5169 | 142562 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4680 | 0.4680 | +0.0000 | 0.0055 | 0.4680 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4717 | 0.4718 | -0.0001 | 0.0036 | 0.4717 | 0.7442 | 0.0067 | 0.0103 | 0.0119 | 0.5161 | 142562 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4712 | 0.4713 | -0.0001 | 0.0032 | 0.4712 | 0.7451 | 0.0049 | 0.0078 | 0.0093 | 0.5169 | 142562 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8357 | 0.8195 | +0.0162 | 0.0054 | 0.8357 | 0.7973 | 0.0548 | 0.0322 | 0.0330 | 0.5117 | 151138 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8250 | 0.8195 | +0.0055 | 0.0048 | 0.8250 | 0.8087 | 0.0589 | 0.0210 | 0.0215 | 0.5838 | 142562 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8235 | 0.8195 | +0.0040 | 0.0058 | 0.8235 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8351 | 0.8195 | +0.0156 | 0.0048 | 0.8351 | 0.7875 | 0.0462 | 0.0282 | 0.0289 | 0.4569 | 142562 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8263 | 0.8195 | +0.0068 | 0.0037 | 0.8263 | 0.8089 | 0.0594 | 0.0222 | 0.0228 | 0.5630 | 142562 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8278 | 0.8195 | +0.0083 | 0.0047 | 0.8278 | 0.7666 | 0.0404 | 0.0574 | 0.0590 | 0.4969 | 151138 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8226 | 0.8195 | +0.0031 | 0.0037 | 0.8226 | 0.7681 | 0.0198 | 0.0277 | 0.0284 | 0.4522 | 142562 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8185 | 0.8185 | +0.0000 | 0.0068 | 0.8185 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8295 | 0.8197 | +0.0097 | 0.0046 | 0.8295 | 0.7606 | 0.0290 | 0.0427 | 0.0439 | 0.4953 | 142562 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8212 | 0.8195 | +0.0016 | 0.0042 | 0.8212 | 0.7662 | 0.0188 | 0.0254 | 0.0261 | 0.4592 | 142562 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0109 | [+0.0044, +0.0175] | 3/0/0 | +0.0190 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0093 | [+0.0026, +0.0159] | 3/0/0 | +0.0266 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0026 | [-0.0053, +0.0106] | 2/0/1 | +0.2873 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0041 | [-0.0052, +0.0133] | 3/0/0 | +0.1992 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0083 | [+0.0068, +0.0098] | 3/0/0 | +0.0018 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0069 | [+0.0041, +0.0096] | 3/0/0 | +0.0084 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0116 | [+0.0086, +0.0146] | 3/0/0 | +0.0036 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0122 | [+0.0089, +0.0155] | 3/0/0 | +0.0039 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0028 | [-0.0036, +0.0093] | 2/1/0 | +0.2007 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | +0.0015 | [-0.0070, +0.0099] | 2/0/1 | +0.5310 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0088 | [+0.0052, +0.0123] | 3/0/0 | +0.0086 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0101 | [+0.0023, +0.0180] | 3/0/0 | +0.0310 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0038 | [-0.0153, +0.0228] | 2/0/1 | +0.4862 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0035 | [-0.0162, +0.0232] | 1/0/2 | +0.5259 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0033 | [-0.0168, +0.0233] | 1/0/2 | +0.5555 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0033 | [-0.0166, +0.0232] | 1/0/2 | +0.5476 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | +0.0005 | [-0.0020, +0.0030] | 1/1/1 | +0.4830 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | +0.0004 | [-0.0022, +0.0030] | 1/1/1 | +0.5471 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0009 | [-0.0046, +0.0029] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | -0.0009 | [-0.0046, +0.0029] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0009 | [-0.0046, +0.0029] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0009 | [-0.0046, +0.0029] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0050 | [+0.0019, +0.0081] | 3/0/0 | +0.0203 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0056 | [+0.0049, +0.0064] | 3/0/0 | +0.0010 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0079 | [+0.0051, +0.0108] | 3/0/0 | +0.0070 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0052 | [+0.0036, +0.0067] | 3/0/0 | +0.0047 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0024 | [-0.0055, +0.0103] | 2/0/1 | +0.3192 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0042 | [-0.0141, +0.0225] | 2/0/1 | +0.4274 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | -0.0004 | [-0.0030, +0.0022] | 1/1/1 | +0.5471 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | -0.0002 | [-0.0028, +0.0025] | 1/1/1 | +0.8164 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0001 | [-0.0002, +0.0003] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
