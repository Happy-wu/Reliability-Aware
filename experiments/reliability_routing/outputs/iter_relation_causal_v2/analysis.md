# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 10
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial scalar-alpha adjustment: n/a
- Iterative relation steps: 1
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.
- External local/global expert logits are embedded in node diagnostics for preference-alignment analysis.
- `relation_relative_strength` and `relation_to_branch_disagreement` are the stable relation-magnitude diagnostics. Per-node `relation_to_base_norm` is retained only as an auxiliary diagnostic because small base norms can inflate it.
- `iterative_relation_frozen/fixed` is the same selected hidden baseline with zero relation correction.
- `iterative_relation_finetune/fixed` fine-tunes the fixed mixing architecture without a relation controller.

## Summary

| Dataset | Metric | Family | Control | Primary | Baseline | Delta | Std | Accuracy | Alpha | Adjustment | Relation strength | Relation/disagreement | Update gate | Active ctrl params | Backbone params |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | accuracy | iterative_relation_finetune | combined | 0.4723 | 0.4665 | +0.0058 | 0.0107 | 0.4723 | 0.8178 | 0.0276 | 0.0179 | 0.0188 | 0.5016 | 166144 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | fixed | 0.4713 | 0.4665 | +0.0048 | 0.0092 | 0.4713 | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_finetune | reliability_only | 0.4710 | 0.4665 | +0.0045 | 0.0114 | 0.4710 | 0.8187 | 0.0271 | 0.0170 | 0.0178 | 0.5063 | 157568 | 94853 |
| Amazon-ratings | accuracy | iterative_relation_frozen | combined | 0.4656 | 0.4665 | -0.0009 | 0.0083 | 0.4656 | 0.7982 | 0.0044 | 0.0090 | 0.0101 | 0.4913 | 166144 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | fixed | 0.4665 | 0.4665 | +0.0000 | 0.0083 | 0.4665 | 0.8000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | accuracy | iterative_relation_frozen | reliability_only | 0.4658 | 0.4665 | -0.0006 | 0.0083 | 0.4658 | 0.7976 | 0.0061 | 0.0119 | 0.0132 | 0.4922 | 157568 | 0 |
| Roman-empire | accuracy | iterative_relation_finetune | combined | 0.8434 | 0.8169 | +0.0265 | 0.0053 | 0.8434 | 0.8005 | 0.0471 | 0.0387 | 0.0399 | 0.5071 | 166144 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | fixed | 0.8216 | 0.8169 | +0.0047 | 0.0083 | 0.8216 | 0.7750 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | accuracy | iterative_relation_finetune | reliability_only | 0.8436 | 0.8169 | +0.0267 | 0.0051 | 0.8436 | 0.7981 | 0.0472 | 0.0412 | 0.0425 | 0.5256 | 157568 | 95698 |
| Roman-empire | accuracy | iterative_relation_frozen | combined | 0.8303 | 0.8169 | +0.0133 | 0.0052 | 0.8303 | 0.7834 | 0.0518 | 0.0525 | 0.0553 | 0.4678 | 166144 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | fixed | 0.8169 | 0.8169 | +0.0000 | 0.0056 | 0.8169 | 0.7750 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | accuracy | iterative_relation_frozen | reliability_only | 0.8341 | 0.8169 | +0.0171 | 0.0063 | 0.8341 | 0.7829 | 0.0533 | 0.0521 | 0.0547 | 0.4833 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0171 | [+0.0143, +0.0199] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0133 | [+0.0123, +0.0144] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0220 | [+0.0160, +0.0279] | 10/0/0 | +0.0000 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0218 | [+0.0159, +0.0277] | 10/0/0 | +0.0000 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | -0.0006 | [-0.0023, +0.0010] | 2/5/3 | +0.4087 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | -0.0009 | [-0.0035, +0.0017] | 3/5/2 | +0.4714 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0003 | [-0.0061, +0.0055] | 5/4/1 | +0.9108 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0010 | [-0.0034, +0.0055] | 4/4/2 | +0.6095 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0047 | [+0.0019, +0.0075] | 8/2/0 | +0.0041 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0095 | [+0.0037, +0.0154] | 10/0/0 | +0.0049 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0131 | [+0.0091, +0.0171] | 10/0/0 | +0.0000 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0048 | [-0.0005, +0.0101] | 4/5/1 | +0.0690 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0051 | [+0.0005, +0.0098] | 6/3/1 | +0.0344 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0067 | [+0.0012, +0.0122] | 6/3/1 | +0.0224 |

## Causal Interventions

- Each intervention reuses the exact trained model and changes only the named inference-time mechanism.
- Positive drop means the intact learned mechanism performs better than its counterfactual intervention.
- For frozen families, `zero_all` returns to the unchanged fixed backbone. For finetuned families, it means the same jointly trained model evaluated without relation correction, not the original fixed baseline.
- Layer-wise relation ablation measures the total downstream effect of disabling that relation block; it is not an additive decomposition of independent layer contributions.
- `fixed` is a sanity control: relation and reliability interventions should have approximately zero effect.

| Dataset | Family | Control | Intervention | Primary drop | 95% CI | Accuracy drop | Changed predictions | Normal-only correct | Intervention-only correct | W/T/L |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | zero_all | +0.0115 | [+0.0005, +0.0224] | +0.0115 | 0.0944 | 0.0382 | 0.0268 | 4/6/0 |
| Amazon-ratings | iterative_relation_finetune | combined | zero_layer_0 | +0.0088 | [+0.0006, +0.0171] | +0.0088 | 0.0862 | 0.0342 | 0.0254 | 4/6/0 |
| Amazon-ratings | iterative_relation_finetune | combined | zero_layer_1 | +0.0007 | [-0.0006, +0.0021] | +0.0007 | 0.0258 | 0.0088 | 0.0081 | 3/6/1 |
| Amazon-ratings | iterative_relation_finetune | combined | shuffled_reliability | +0.0012 | [-0.0008, +0.0032] | +0.0012 | 0.0324 | 0.0111 | 0.0099 | 3/6/1 |
| Amazon-ratings | iterative_relation_finetune | combined | constant_reliability | +0.0031 | [+0.0002, +0.0059] | +0.0031 | 0.0315 | 0.0117 | 0.0086 | 4/6/0 |
| Amazon-ratings | iterative_relation_finetune | fixed | zero_all | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_finetune | fixed | zero_layer_0 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_finetune | fixed | zero_layer_1 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_finetune | fixed | shuffled_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_finetune | fixed | constant_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | zero_all | +0.0083 | [+0.0003, +0.0163] | +0.0083 | 0.0859 | 0.0339 | 0.0256 | 4/6/0 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | zero_layer_0 | +0.0078 | [+0.0003, +0.0154] | +0.0078 | 0.0764 | 0.0304 | 0.0226 | 4/6/0 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | zero_layer_1 | -0.0004 | [-0.0021, +0.0012] | -0.0004 | 0.0245 | 0.0079 | 0.0083 | 1/6/3 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | shuffled_reliability | +0.0008 | [-0.0006, +0.0022] | +0.0008 | 0.0346 | 0.0114 | 0.0106 | 3/6/1 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | constant_reliability | +0.0037 | [-0.0001, +0.0076] | +0.0037 | 0.0374 | 0.0138 | 0.0101 | 4/6/0 |
| Amazon-ratings | iterative_relation_frozen | combined | zero_all | -0.0009 | [-0.0035, +0.0017] | -0.0009 | 0.0237 | 0.0075 | 0.0083 | 3/5/2 |
| Amazon-ratings | iterative_relation_frozen | combined | zero_layer_0 | -0.0009 | [-0.0033, +0.0015] | -0.0009 | 0.0199 | 0.0061 | 0.0070 | 3/5/2 |
| Amazon-ratings | iterative_relation_frozen | combined | zero_layer_1 | -0.0001 | [-0.0009, +0.0007] | -0.0001 | 0.0066 | 0.0023 | 0.0024 | 2/7/1 |
| Amazon-ratings | iterative_relation_frozen | combined | shuffled_reliability | +0.0003 | [-0.0001, +0.0008] | +0.0003 | 0.0047 | 0.0017 | 0.0014 | 5/5/0 |
| Amazon-ratings | iterative_relation_frozen | combined | constant_reliability | +0.0005 | [-0.0002, +0.0011] | +0.0005 | 0.0047 | 0.0018 | 0.0013 | 4/5/1 |
| Amazon-ratings | iterative_relation_frozen | fixed | zero_all | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_frozen | fixed | zero_layer_0 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_frozen | fixed | zero_layer_1 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_frozen | fixed | shuffled_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_frozen | fixed | constant_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | zero_all | -0.0006 | [-0.0023, +0.0010] | -0.0006 | 0.0218 | 0.0070 | 0.0077 | 2/5/3 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | zero_layer_0 | -0.0003 | [-0.0014, +0.0008] | -0.0003 | 0.0167 | 0.0055 | 0.0058 | 1/5/4 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | zero_layer_1 | -0.0004 | [-0.0018, +0.0011] | -0.0004 | 0.0095 | 0.0030 | 0.0033 | 3/5/2 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | shuffled_reliability | +0.0007 | [-0.0012, +0.0026] | +0.0007 | 0.0103 | 0.0037 | 0.0030 | 2/5/3 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | constant_reliability | +0.0008 | [-0.0013, +0.0029] | +0.0008 | 0.0087 | 0.0033 | 0.0025 | 2/5/3 |
| Roman-empire | iterative_relation_finetune | combined | zero_all | +0.0484 | [+0.0400, +0.0569] | +0.0484 | 0.1146 | 0.0691 | 0.0206 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | combined | zero_layer_0 | +0.0309 | [+0.0212, +0.0406] | +0.0309 | 0.0856 | 0.0484 | 0.0175 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | combined | zero_layer_1 | +0.0147 | [+0.0078, +0.0217] | +0.0147 | 0.0520 | 0.0275 | 0.0128 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | combined | shuffled_reliability | +0.0502 | [+0.0400, +0.0605] | +0.0502 | 0.1130 | 0.0685 | 0.0182 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | combined | constant_reliability | +0.0367 | [+0.0315, +0.0420] | +0.0367 | 0.0990 | 0.0556 | 0.0188 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | fixed | zero_all | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_finetune | fixed | zero_layer_0 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_finetune | fixed | zero_layer_1 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_finetune | fixed | shuffled_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_finetune | fixed | constant_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_finetune | reliability_only | zero_all | +0.0474 | [+0.0399, +0.0549] | +0.0474 | 0.1117 | 0.0675 | 0.0202 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | reliability_only | zero_layer_0 | +0.0298 | [+0.0216, +0.0380] | +0.0298 | 0.0826 | 0.0465 | 0.0167 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | reliability_only | zero_layer_1 | +0.0149 | [+0.0076, +0.0221] | +0.0149 | 0.0520 | 0.0280 | 0.0131 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | reliability_only | shuffled_reliability | +0.0485 | [+0.0391, +0.0578] | +0.0485 | 0.1127 | 0.0675 | 0.0190 | 10/0/0 |
| Roman-empire | iterative_relation_finetune | reliability_only | constant_reliability | +0.0363 | [+0.0307, +0.0419] | +0.0363 | 0.0975 | 0.0546 | 0.0184 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | combined | zero_all | +0.0133 | [+0.0123, +0.0144] | +0.0133 | 0.0767 | 0.0353 | 0.0219 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | combined | zero_layer_0 | +0.0085 | [+0.0062, +0.0107] | +0.0085 | 0.0552 | 0.0250 | 0.0166 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | combined | zero_layer_1 | +0.0044 | [+0.0027, +0.0060] | +0.0044 | 0.0471 | 0.0196 | 0.0152 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | combined | shuffled_reliability | +0.0240 | [+0.0178, +0.0301] | +0.0240 | 0.0845 | 0.0439 | 0.0199 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | combined | constant_reliability | +0.0232 | [+0.0182, +0.0281] | +0.0232 | 0.0876 | 0.0442 | 0.0210 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | fixed | zero_all | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_frozen | fixed | zero_layer_0 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_frozen | fixed | zero_layer_1 | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_frozen | fixed | shuffled_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_frozen | fixed | constant_reliability | +0.0000 | [+0.0000, +0.0000] | +0.0000 | 0.0000 | 0.0000 | 0.0000 | 0/10/0 |
| Roman-empire | iterative_relation_frozen | reliability_only | zero_all | +0.0171 | [+0.0143, +0.0199] | +0.0171 | 0.0753 | 0.0370 | 0.0199 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | reliability_only | zero_layer_0 | +0.0076 | [+0.0056, +0.0096] | +0.0076 | 0.0545 | 0.0239 | 0.0164 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | reliability_only | zero_layer_1 | +0.0093 | [+0.0053, +0.0133] | +0.0093 | 0.0474 | 0.0224 | 0.0131 | 9/1/0 |
| Roman-empire | iterative_relation_frozen | reliability_only | shuffled_reliability | +0.0264 | [+0.0208, +0.0321] | +0.0264 | 0.0886 | 0.0468 | 0.0203 | 10/0/0 |
| Roman-empire | iterative_relation_frozen | reliability_only | constant_reliability | +0.0270 | [+0.0229, +0.0312] | +0.0270 | 0.0941 | 0.0489 | 0.0218 | 10/0/0 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
