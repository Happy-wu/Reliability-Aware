# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: raw_concat
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4757 | 0.4685 | +0.0072 | 0.0081 | 0.4757 | 0.8664 | 0.0451 | 0.0306 | 0.0318 | 0.5005 | 166144 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4762 | 0.4685 | +0.0077 | 0.0084 | 0.4762 | 0.8693 | 0.0494 | 0.0324 | 0.0338 | 0.5297 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4726 | 0.4685 | +0.0041 | 0.0068 | 0.4726 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4767 | 0.4685 | +0.0082 | 0.0088 | 0.4767 | 0.8652 | 0.0445 | 0.0310 | 0.0323 | 0.5354 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4733 | 0.4685 | +0.0048 | 0.0073 | 0.4733 | 0.8664 | 0.0456 | 0.0293 | 0.0306 | 0.5477 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4674 | 0.4685 | -0.0011 | 0.0048 | 0.4674 | 0.8330 | 0.0003 | 0.0009 | 0.0010 | 0.4957 | 166144 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.4959 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8329 | 0.0005 | 0.0018 | 0.0022 | 0.4971 | 157568 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4685 | 0.4685 | +0.0000 | 0.0033 | 0.4685 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0.4969 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8430 | 0.8174 | +0.0256 | 0.0067 | 0.8430 | 0.7779 | 0.0512 | 0.0383 | 0.0396 | 0.5174 | 166144 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8206 | 0.8174 | +0.0032 | 0.0049 | 0.8206 | 0.7784 | 0.0449 | 0.0272 | 0.0280 | 0.4720 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8225 | 0.8174 | +0.0051 | 0.0021 | 0.8225 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8407 | 0.8174 | +0.0233 | 0.0054 | 0.8407 | 0.7756 | 0.0512 | 0.0396 | 0.0409 | 0.5190 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8213 | 0.8174 | +0.0039 | 0.0056 | 0.8213 | 0.7788 | 0.0438 | 0.0267 | 0.0275 | 0.4440 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8304 | 0.8174 | +0.0130 | 0.0086 | 0.8304 | 0.7668 | 0.0595 | 0.0580 | 0.0595 | 0.4587 | 166144 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8258 | 0.8174 | +0.0084 | 0.0071 | 0.8258 | 0.7812 | 0.0618 | 0.0515 | 0.0529 | 0.4203 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8174 | 0.8174 | +0.0000 | 0.0035 | 0.8174 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8370 | 0.8174 | +0.0196 | 0.0047 | 0.8370 | 0.7665 | 0.0598 | 0.0548 | 0.0562 | 0.4891 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8210 | 0.8174 | +0.0036 | 0.0070 | 0.8210 | 0.7682 | 0.0333 | 0.0312 | 0.0320 | 0.4280 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0196 | [+0.0139, +0.0254] | 3/0/0 | +0.0047 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0130 | [-0.0034, +0.0294] | 3/0/0 | +0.0759 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0036 | [-0.0073, +0.0146] | 2/0/1 | +0.2886 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0084 | [-0.0026, +0.0194] | 3/0/0 | +0.0816 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0160 | [+0.0074, +0.0246] | 3/0/0 | +0.0153 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0112 | [+0.0010, +0.0215] | 3/0/0 | +0.0424 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0182 | [-0.0013, +0.0377] | 3/0/0 | +0.0570 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0205 | [-0.0034, +0.0444] | 3/0/0 | +0.0665 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | -0.0012 | [-0.0159, +0.0136] | 1/0/2 | +0.7639 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0019 | [-0.0135, +0.0098] | 1/0/2 | +0.5589 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0194 | [+0.0048, +0.0340] | 3/0/0 | +0.0294 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0201 | [+0.0042, +0.0360] | 3/0/0 | +0.0323 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | -0.0011 | [-0.0058, +0.0036] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | +0.0041 | [-0.0124, +0.0206] | 2/1/0 | +0.3991 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0031 | [-0.0120, +0.0182] | 1/1/1 | +0.4709 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | +0.0007 | [-0.0206, +0.0221] | 1/1/1 | +0.8997 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | +0.0036 | [-0.0103, +0.0176] | 2/1/0 | +0.3781 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0034 | [-0.0069, +0.0137] | 2/1/0 | +0.2939 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0004 | [-0.0022, +0.0030] | 1/1/1 | +0.5471 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0051 | [-0.0064, +0.0166] | 2/1/0 | +0.1954 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0036 | [-0.0092, +0.0165] | 2/0/1 | +0.3471 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0126 | [-0.0088, +0.0340] | 3/0/0 | +0.1270 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0003 | [-0.0070, +0.0076] | 2/0/1 | +0.8781 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0052 | [-0.0179, +0.0075] | 0/0/3 | +0.2221 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0041 | [-0.0135, +0.0217] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0082 | [-0.0094, +0.0258] | 2/1/0 | +0.1842 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0083 | [-0.0026, +0.0192] | 3/0/0 | +0.0823 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0048 | [-0.0072, +0.0168] | 2/1/0 | +0.2272 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0077 | [-0.0093, +0.0248] | 2/1/0 | +0.1900 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
