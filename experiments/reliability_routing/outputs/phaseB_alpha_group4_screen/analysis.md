# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Reliability encoder mode: component_concat
- Reliability component dim: 16
- Component missing mode: zero_slot
- Iterative alpha type: group
- Iterative alpha groups: 4
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
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4975 | 151528 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | constant_reliability | 0.4736 | 0.4713 | +0.0023 | 0.0056 | 0.4736 | 0.7810 | 0.0310 | 0.0278 | 0.0288 | 0.5307 | 142952 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4755 | 0.4713 | +0.0042 | 0.0078 | 0.4755 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4915 | 142952 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | shuffled_reliability | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.4915 | 142952 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4711 | 0.4713 | -0.0002 | 0.0034 | 0.4711 | 0.7403 | 0.0097 | 0.0202 | 0.0240 | 0.5198 | 151528 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | constant_reliability | 0.4707 | 0.4713 | -0.0005 | 0.0039 | 0.4707 | 0.7425 | 0.0075 | 0.0157 | 0.0186 | 0.5139 | 142952 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4713 | 0.4713 | +0.0000 | 0.0031 | 0.4713 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4705 | 0.4713 | -0.0008 | 0.0042 | 0.4705 | 0.7402 | 0.0098 | 0.0209 | 0.0249 | 0.5137 | 142952 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | shuffled_reliability | 0.4712 | 0.4713 | -0.0001 | 0.0032 | 0.4712 | 0.7489 | 0.0011 | 0.0026 | 0.0031 | 0.4933 | 142952 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8397 | 0.8195 | +0.0202 | 0.0050 | 0.8397 | 0.7878 | 0.0446 | 0.0310 | 0.0319 | 0.4748 | 151528 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | constant_reliability | 0.8272 | 0.8195 | +0.0077 | 0.0035 | 0.8272 | 0.8040 | 0.0541 | 0.0250 | 0.0255 | 0.5213 | 142952 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8255 | 0.8195 | +0.0059 | 0.0057 | 0.8255 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8386 | 0.8195 | +0.0191 | 0.0059 | 0.8386 | 0.7849 | 0.0425 | 0.0303 | 0.0311 | 0.4684 | 142952 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | shuffled_reliability | 0.8259 | 0.8195 | +0.0064 | 0.0043 | 0.8259 | 0.8035 | 0.0537 | 0.0244 | 0.0249 | 0.4950 | 142952 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8313 | 0.8195 | +0.0118 | 0.0049 | 0.8313 | 0.7657 | 0.0402 | 0.0580 | 0.0596 | 0.4564 | 151528 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | constant_reliability | 0.8244 | 0.8195 | +0.0049 | 0.0055 | 0.8244 | 0.7710 | 0.0304 | 0.0545 | 0.0560 | 0.4402 | 142952 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8195 | 0.8195 | +0.0000 | 0.0035 | 0.8195 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8313 | 0.8195 | +0.0118 | 0.0055 | 0.8313 | 0.7643 | 0.0344 | 0.0515 | 0.0529 | 0.4539 | 142952 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | shuffled_reliability | 0.8229 | 0.8195 | +0.0034 | 0.0041 | 0.8229 | 0.7693 | 0.0245 | 0.0422 | 0.0434 | 0.4363 | 142952 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0118 | [+0.0028, +0.0208] | 3/0/0 | +0.0302 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0118 | [+0.0074, +0.0162] | 3/0/0 | +0.0074 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0034 | [-0.0023, +0.0091] | 3/0/0 | +0.1236 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0049 | [-0.0027, +0.0125] | 3/0/0 | +0.1103 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0084 | [+0.0040, +0.0127] | 3/0/0 | +0.0146 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0069 | [+0.0042, +0.0096] | 3/0/0 | +0.0080 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0131 | [+0.0048, +0.0214] | 3/0/0 | +0.0208 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0143 | [+0.0104, +0.0182] | 3/0/0 | +0.0040 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0005 | [-0.0076, +0.0086] | 1/0/2 | +0.8257 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | +0.0018 | [-0.0051, +0.0086] | 2/0/1 | +0.3830 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0126 | [+0.0076, +0.0177] | 3/0/0 | +0.0085 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0114 | [+0.0021, +0.0206] | 3/0/0 | +0.0341 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | -0.0008 | [-0.0043, +0.0027] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | -0.0002 | [-0.0012, +0.0007] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | -0.0001 | [-0.0006, +0.0004] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | -0.0005 | [-0.0029, +0.0018] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0007 | [-0.0038, +0.0023] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0003 | [-0.0014, +0.0009] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0042 | [-0.0222, +0.0138] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | -0.0042 | [-0.0222, +0.0138] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0042 | [-0.0222, +0.0138] | 0/2/1 | +0.4226 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | -0.0019 | [-0.0264, +0.0226] | 1/1/1 | +0.7696 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | -0.0023 | [-0.0121, +0.0076] | 0/2/1 | +0.4226 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0059 | [-0.0010, +0.0129] | 3/0/0 | +0.0669 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0073 | [+0.0059, +0.0087] | 3/0/0 | +0.0020 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0085 | [+0.0067, +0.0102] | 3/0/0 | +0.0023 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0030 | [+0.0021, +0.0039] | 3/0/0 | +0.0046 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0028 | [-0.0046, +0.0102] | 3/0/0 | +0.2412 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0042 | [-0.0138, +0.0222] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0008 | [-0.0027, +0.0043] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0002 | [-0.0007, +0.0012] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0001 | [-0.0004, +0.0006] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0028 | [-0.0061, +0.0117] | 2/1/0 | +0.3046 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
