# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: raw_concat
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4781 | 0.4716 | +0.0065 | 0.0086 | 0.4781 | 0.6950 | 0.0446 | 0.0324 | 0.0339 | 0.5235 | 166144 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4737 | 0.4716 | +0.0021 | 0.0067 | 0.4737 | 0.6950 | 0.0495 | 0.0389 | 0.0408 | 0.5157 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4789 | 0.4716 | +0.0073 | 0.0035 | 0.4789 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4771 | 0.4716 | +0.0055 | 0.0079 | 0.4771 | 0.6955 | 0.0459 | 0.0346 | 0.0362 | 0.5045 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4751 | 0.4716 | +0.0035 | 0.0085 | 0.4751 | 0.6958 | 0.0464 | 0.0311 | 0.0326 | 0.5199 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4710 | 0.4703 | +0.0007 | 0.0022 | 0.4710 | 0.6667 | 0.0014 | 0.0020 | 0.0020 | 0.4912 | 166144 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4722 | 0.4716 | +0.0005 | 0.0038 | 0.4722 | 0.6666 | 0.0014 | 0.0020 | 0.0021 | 0.4915 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4740 | 0.4740 | +0.0000 | 0.0017 | 0.4740 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4702 | 0.4703 | -0.0001 | 0.0021 | 0.4702 | 0.6663 | 0.0027 | 0.0047 | 0.0049 | 0.4911 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4719 | 0.4716 | +0.0003 | 0.0041 | 0.4719 | 0.6666 | 0.0013 | 0.0020 | 0.0021 | 0.4927 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8410 | 0.8199 | +0.0211 | 0.0055 | 0.8410 | 0.7792 | 0.0520 | 0.0415 | 0.0428 | 0.4897 | 166144 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8223 | 0.8199 | +0.0024 | 0.0060 | 0.8223 | 0.7833 | 0.0434 | 0.0234 | 0.0240 | 0.4839 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8240 | 0.8199 | +0.0041 | 0.0073 | 0.8240 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8447 | 0.8199 | +0.0248 | 0.0062 | 0.8447 | 0.7760 | 0.0500 | 0.0419 | 0.0432 | 0.4937 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8226 | 0.8199 | +0.0027 | 0.0063 | 0.8226 | 0.7793 | 0.0414 | 0.0234 | 0.0240 | 0.4801 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8319 | 0.8199 | +0.0120 | 0.0036 | 0.8319 | 0.7638 | 0.0596 | 0.0588 | 0.0604 | 0.4605 | 166144 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8256 | 0.8199 | +0.0056 | 0.0051 | 0.8256 | 0.7778 | 0.0613 | 0.0511 | 0.0524 | 0.4149 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8210 | 0.8210 | +0.0000 | 0.0043 | 0.8210 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8381 | 0.8210 | +0.0171 | 0.0063 | 0.8381 | 0.7658 | 0.0595 | 0.0538 | 0.0553 | 0.4603 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8220 | 0.8199 | +0.0021 | 0.0055 | 0.8220 | 0.7741 | 0.0490 | 0.0459 | 0.0471 | 0.4393 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0171 | [+0.0107, +0.0234] | 3/0/0 | +0.0075 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0109 | [+0.0058, +0.0160] | 3/0/0 | +0.0116 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0010 | [-0.0031, +0.0051] | 2/0/1 | +0.4081 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0045 | [+0.0012, +0.0078] | 3/0/0 | +0.0273 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0161 | [+0.0103, +0.0218] | 3/0/0 | +0.0068 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0125 | [+0.0062, +0.0189] | 3/0/0 | +0.0135 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0207 | [+0.0172, +0.0243] | 3/0/0 | +0.0016 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0170 | [+0.0095, +0.0245] | 3/0/0 | +0.0105 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | -0.0014 | [-0.0045, +0.0018] | 0/1/2 | +0.2021 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0017 | [-0.0057, +0.0023] | 0/1/2 | +0.2063 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0221 | [+0.0198, +0.0243] | 3/0/0 | +0.0006 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0224 | [+0.0200, +0.0249] | 3/0/0 | +0.0006 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | -0.0037 | [-0.0086, +0.0012] | 0/0/3 | +0.0833 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | -0.0030 | [-0.0094, +0.0035] | 0/1/2 | +0.1836 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | -0.0020 | [-0.0149, +0.0108] | 1/0/2 | +0.5694 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | -0.0018 | [-0.0141, +0.0105] | 1/0/2 | +0.5943 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0017 | [-0.0097, +0.0063] | 1/1/1 | +0.4586 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0019 | [-0.0094, +0.0056] | 0/1/2 | +0.3888 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0018 | [-0.0189, +0.0153] | 1/0/2 | +0.6960 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | -0.0008 | [-0.0199, +0.0184] | 2/0/1 | +0.8800 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0038 | [-0.0189, +0.0114] | 1/0/2 | +0.3980 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0052 | [-0.0152, +0.0047] | 0/0/3 | +0.1522 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0020 | [-0.0136, +0.0176] | 1/1/1 | +0.6428 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0034 | [-0.0093, +0.0161] | 2/1/0 | +0.3654 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0029 | [-0.0106, +0.0165] | 2/0/1 | +0.4491 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0066 | [-0.0036, +0.0167] | 3/0/0 | +0.1079 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0091 | [+0.0002, +0.0179] | 3/0/0 | +0.0475 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0006 | [-0.0121, +0.0133] | 2/0/1 | +0.8602 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0033 | [-0.0154, +0.0088] | 1/0/2 | +0.3622 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0050 | [-0.0073, +0.0172] | 3/0/0 | +0.2249 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0069 | [-0.0108, +0.0245] | 2/0/1 | +0.2371 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0072 | [-0.0125, +0.0269] | 2/0/1 | +0.2568 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0032 | [-0.0105, +0.0169] | 2/0/1 | +0.4200 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0015 | [-0.0073, +0.0104] | 2/0/1 | +0.5360 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
