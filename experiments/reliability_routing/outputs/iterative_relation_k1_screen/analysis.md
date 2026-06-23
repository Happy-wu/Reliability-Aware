# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings, Cora, Pubmed
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

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Relation/Base | Update gate | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 0.4840 | 0.4667 | +0.0174 | 0.0057 | 0.6974 | 0.0463 | 0.3721 | 0.5279 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_constant | 0.4790 | 0.4667 | +0.0123 | 0.0009 | 0.7160 | 0.0686 | 0.5392 | 0.5097 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled | 0.4779 | 0.4667 | +0.0112 | 0.0012 | 0.7140 | 0.0701 | 0.5828 | 0.5398 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability | 0.4833 | 0.4667 | +0.0166 | 0.0011 | 0.7177 | 0.0735 | 0.5815 | 0.5407 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | feature_only | 0.4803 | 0.4667 | +0.0137 | 0.0008 | 0.7162 | 0.0705 | 0.5569 | 0.5773 | 156544 | 94853 |
| Amazon-ratings | iterative_relation_finetune | fixed | 0.4762 | 0.4667 | +0.0095 | 0.0067 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 0.4743 | 0.4667 | +0.0077 | 0.0071 | 0.6936 | 0.0438 | 0.3133 | 0.5297 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability | 0.4797 | 0.4667 | +0.0131 | 0.0029 | 0.7152 | 0.0686 | 0.5479 | 0.5570 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_frozen | combined | 0.4707 | 0.4667 | +0.0040 | 0.0054 | 0.6669 | 0.0160 | 0.1357 | 0.4928 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_constant | 0.4712 | 0.4667 | +0.0045 | 0.0044 | 0.6674 | 0.0175 | 0.1485 | 0.4846 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled | 0.4705 | 0.4667 | +0.0039 | 0.0055 | 0.6675 | 0.0232 | 0.1834 | 0.4972 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability | 0.4695 | 0.4667 | +0.0029 | 0.0059 | 0.6668 | 0.0148 | 0.1176 | 0.4835 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | feature_only | 0.4699 | 0.4667 | +0.0033 | 0.0057 | 0.6668 | 0.0149 | 0.1200 | 0.4889 | 156544 | 0 |
| Amazon-ratings | iterative_relation_frozen | fixed | 0.4667 | 0.4667 | +0.0000 | 0.0086 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 0.4683 | 0.4667 | +0.0016 | 0.0058 | 0.6662 | 0.0143 | 0.1113 | 0.4916 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability | 0.4688 | 0.4667 | +0.0022 | 0.0063 | 0.6664 | 0.0136 | 0.1054 | 0.4906 | 157568 | 0 |
| Cora | iterative_relation_finetune | combined | 0.6943 | 0.6823 | +0.0120 | 0.0025 | 0.8298 | 0.0144 | 0.0947 | 0.5169 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_constant | 0.6950 | 0.6823 | +0.0127 | 0.0045 | 0.8290 | 0.0198 | 0.1360 | 0.5273 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_shuffled | 0.6917 | 0.6823 | +0.0093 | 0.0076 | 0.8294 | 0.0170 | 0.1174 | 0.5198 | 166144 | 167495 |
| Cora | iterative_relation_finetune | constant_reliability | 0.6860 | 0.6823 | +0.0037 | 0.0099 | 0.8272 | 0.0204 | 0.1138 | 0.5316 | 157568 | 167495 |
| Cora | iterative_relation_finetune | feature_only | 0.6837 | 0.6823 | +0.0013 | 0.0080 | 0.8303 | 0.0107 | 0.1004 | 0.5022 | 156544 | 167495 |
| Cora | iterative_relation_finetune | fixed | 0.7053 | 0.6823 | +0.0230 | 0.0153 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 167495 |
| Cora | iterative_relation_finetune | reliability_only | 0.6800 | 0.6823 | -0.0023 | 0.0107 | 0.8303 | 0.0116 | 0.0770 | 0.5070 | 157568 | 167495 |
| Cora | iterative_relation_finetune | shuffled_reliability | 0.6873 | 0.6823 | +0.0050 | 0.0059 | 0.8303 | 0.0125 | 0.0568 | 0.5104 | 157568 | 167495 |
| Cora | iterative_relation_frozen | combined | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_constant | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4962 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_shuffled | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | constant_reliability | 0.6817 | 0.6823 | -0.0007 | 0.0095 | 0.8307 | 0.0027 | 0.0679 | 0.4975 | 157568 | 0 |
| Cora | iterative_relation_frozen | feature_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4953 | 156544 | 0 |
| Cora | iterative_relation_frozen | fixed | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Cora | iterative_relation_frozen | reliability_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4969 | 157568 | 0 |
| Cora | iterative_relation_frozen | shuffled_reliability | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4969 | 157568 | 0 |
| Pubmed | iterative_relation_finetune | combined | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8319 | 0.0015 | 0.0217 | 0.4983 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_constant | 0.7403 | 0.7377 | +0.0027 | 0.0126 | 0.8312 | 0.0021 | 0.0515 | 0.5000 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_shuffled | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8316 | 0.0017 | 0.0184 | 0.5037 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | constant_reliability | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8307 | 0.0026 | 0.0287 | 0.4990 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | feature_only | 0.7407 | 0.7377 | +0.0030 | 0.0124 | 0.8300 | 0.0070 | 0.0780 | 0.5042 | 156544 | 107523 |
| Pubmed | iterative_relation_finetune | fixed | 0.7397 | 0.7377 | +0.0020 | 0.0116 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 107523 |
| Pubmed | iterative_relation_finetune | reliability_only | 0.7390 | 0.7377 | +0.0013 | 0.0107 | 0.8317 | 0.0017 | 0.0284 | 0.4910 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | shuffled_reliability | 0.7390 | 0.7377 | +0.0013 | 0.0107 | 0.8311 | 0.0023 | 0.0393 | 0.4966 | 157568 | 107523 |
| Pubmed | iterative_relation_frozen | combined | 0.7383 | 0.7377 | +0.0007 | 0.0083 | 0.8335 | 0.0007 | 0.0026 | 0.5037 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_constant | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8339 | 0.0037 | 0.0130 | 0.5071 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_shuffled | 0.7343 | 0.7377 | -0.0033 | 0.0120 | 0.8362 | 0.0315 | 0.0890 | 0.5041 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | constant_reliability | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8342 | 0.0070 | 0.0224 | 0.5096 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | feature_only | 0.7350 | 0.7377 | -0.0027 | 0.0110 | 0.8380 | 0.0309 | 0.0847 | 0.4799 | 156544 | 0 |
| Pubmed | iterative_relation_frozen | fixed | 0.7377 | 0.7377 | +0.0000 | 0.0088 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Pubmed | iterative_relation_frozen | reliability_only | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8334 | 0.0005 | 0.0018 | 0.5003 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | shuffled_reliability | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8336 | 0.0023 | 0.0075 | 0.5011 | 157568 | 0 |
| Roman-empire | iterative_relation_finetune | combined | 0.8455 | 0.8166 | +0.0288 | 0.0062 | 0.7839 | 0.0509 | 0.5841 | 0.5181 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_constant | 0.8253 | 0.8166 | +0.0087 | 0.0076 | 0.7829 | 0.0440 | 0.4203 | 0.4932 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_shuffled | 0.8248 | 0.8166 | +0.0082 | 0.0065 | 0.7822 | 0.0420 | 0.3922 | 0.4864 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | constant_reliability | 0.8235 | 0.8166 | +0.0069 | 0.0065 | 0.7820 | 0.0417 | 0.3917 | 0.5039 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | feature_only | 0.8254 | 0.8166 | +0.0088 | 0.0072 | 0.7819 | 0.0409 | 0.3855 | 0.4918 | 156544 | 95698 |
| Roman-empire | iterative_relation_finetune | fixed | 0.8247 | 0.8166 | +0.0081 | 0.0063 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | iterative_relation_finetune | reliability_only | 0.8460 | 0.8166 | +0.0294 | 0.0057 | 0.7810 | 0.0497 | 0.5839 | 0.5190 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability | 0.8231 | 0.8166 | +0.0065 | 0.0055 | 0.7813 | 0.0399 | 0.3606 | 0.5020 | 157568 | 95698 |
| Roman-empire | iterative_relation_frozen | combined | 0.8333 | 0.8166 | +0.0167 | 0.0054 | 0.7635 | 0.0592 | 0.6915 | 0.4823 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_constant | 0.8195 | 0.8166 | +0.0029 | 0.0075 | 0.7704 | 0.0383 | 0.3776 | 0.4239 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_shuffled | 0.8209 | 0.8166 | +0.0042 | 0.0063 | 0.7757 | 0.0488 | 0.4950 | 0.4474 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | constant_reliability | 0.8249 | 0.8166 | +0.0083 | 0.0074 | 0.7759 | 0.0614 | 0.4954 | 0.4242 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | feature_only | 0.8188 | 0.8166 | +0.0022 | 0.0075 | 0.7686 | 0.0369 | 0.3767 | 0.4169 | 156544 | 0 |
| Roman-empire | iterative_relation_frozen | fixed | 0.8166 | 0.8166 | +0.0000 | 0.0042 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | iterative_relation_frozen | reliability_only | 0.8363 | 0.8166 | +0.0197 | 0.0051 | 0.7664 | 0.0602 | 0.7069 | 0.4889 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability | 0.8210 | 0.8166 | +0.0044 | 0.0080 | 0.7753 | 0.0507 | 0.4967 | 0.4479 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | feature_only - fixed | +0.0022 | [-0.0141, +0.0185] | 2/0/1 | +0.6241 |
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0197 | [+0.0115, +0.0279] | 3/0/0 | +0.0093 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0167 | [+0.0077, +0.0257] | 3/0/0 | +0.0153 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0044 | [-0.0147, +0.0235] | 2/0/1 | +0.4243 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0083 | [-0.0070, +0.0236] | 3/0/0 | +0.1444 |
| Roman-empire | iterative_relation_frozen | combined_shuffled - fixed | +0.0042 | [-0.0116, +0.0201] | 2/0/1 | +0.3686 |
| Roman-empire | iterative_relation_frozen | combined_constant - fixed | +0.0029 | [-0.0120, +0.0177] | 2/0/1 | +0.4912 |
| Roman-empire | iterative_relation_frozen | reliability_only - feature_only | +0.0175 | [+0.0091, +0.0260] | 3/0/0 | +0.0122 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0153 | [+0.0044, +0.0262] | 3/0/0 | +0.0265 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0114 | [+0.0037, +0.0191] | 3/0/0 | +0.0236 |
| Roman-empire | iterative_relation_frozen | combined - feature_only | +0.0145 | [+0.0071, +0.0219] | 3/0/0 | +0.0138 |
| Roman-empire | iterative_relation_frozen | combined - combined_shuffled | +0.0125 | [+0.0050, +0.0199] | 3/0/0 | +0.0188 |
| Roman-empire | iterative_relation_frozen | combined - combined_constant | +0.0138 | [+0.0074, +0.0202] | 3/0/0 | +0.0113 |
| Roman-empire | iterative_relation_finetune | feature_only - fixed | +0.0006 | [-0.0033, +0.0046] | 1/1/1 | +0.5564 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0212 | [+0.0113, +0.0312] | 3/0/0 | +0.0117 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0207 | [+0.0102, +0.0312] | 3/0/0 | +0.0135 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | -0.0016 | [-0.0058, +0.0025] | 0/1/2 | +0.2311 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0012 | [-0.0077, +0.0053] | 1/1/1 | +0.4987 |
| Roman-empire | iterative_relation_finetune | combined_shuffled - fixed | +0.0001 | [-0.0010, +0.0012] | 1/1/1 | +0.8399 |
| Roman-empire | iterative_relation_finetune | combined_constant - fixed | +0.0006 | [-0.0061, +0.0073] | 1/1/1 | +0.7418 |
| Roman-empire | iterative_relation_finetune | reliability_only - feature_only | +0.0206 | [+0.0115, +0.0297] | 3/0/0 | +0.0104 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0229 | [+0.0169, +0.0289] | 3/0/0 | +0.0037 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0225 | [+0.0179, +0.0270] | 3/0/0 | +0.0022 |
| Roman-empire | iterative_relation_finetune | combined - feature_only | +0.0201 | [+0.0111, +0.0290] | 3/0/0 | +0.0107 |
| Roman-empire | iterative_relation_finetune | combined - combined_shuffled | +0.0206 | [+0.0110, +0.0303] | 3/0/0 | +0.0117 |
| Roman-empire | iterative_relation_finetune | combined - combined_constant | +0.0201 | [+0.0123, +0.0279] | 3/0/0 | +0.0080 |
| Amazon-ratings | iterative_relation_frozen | feature_only - fixed | +0.0033 | [-0.0055, +0.0121] | 2/1/0 | +0.2508 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0016 | [-0.0071, +0.0104] | 2/0/1 | +0.5073 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0040 | [-0.0057, +0.0138] | 2/1/0 | +0.2174 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0022 | [-0.0055, +0.0099] | 2/1/0 | +0.3468 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0029 | [-0.0054, +0.0112] | 2/1/0 | +0.2725 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled - fixed | +0.0039 | [-0.0057, +0.0134] | 2/1/0 | +0.2232 |
| Amazon-ratings | iterative_relation_frozen | combined_constant - fixed | +0.0045 | [-0.0085, +0.0176] | 2/1/0 | +0.2750 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - feature_only | -0.0016 | [-0.0027, -0.0006] | 0/0/3 | +0.0225 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0005 | [-0.0022, +0.0011] | 0/0/3 | +0.2893 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0013 | [-0.0019, -0.0006] | 0/0/3 | +0.0130 |
| Amazon-ratings | iterative_relation_frozen | combined - feature_only | +0.0008 | [-0.0011, +0.0026] | 2/1/0 | +0.2149 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_shuffled | +0.0002 | [-0.0002, +0.0006] | 2/1/0 | +0.2254 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_constant | -0.0005 | [-0.0049, +0.0039] | 1/1/1 | +0.6784 |
| Amazon-ratings | iterative_relation_finetune | feature_only - fixed | +0.0041 | [-0.0139, +0.0222] | 2/0/1 | +0.4277 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | -0.0019 | [-0.0113, +0.0076] | 1/1/1 | +0.4863 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0078 | [-0.0235, +0.0392] | 2/0/1 | +0.3947 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | +0.0035 | [-0.0223, +0.0293] | 1/0/2 | +0.6148 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | +0.0071 | [-0.0156, +0.0297] | 2/0/1 | +0.3109 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled - fixed | +0.0017 | [-0.0215, +0.0249] | 2/0/1 | +0.7839 |
| Amazon-ratings | iterative_relation_finetune | combined_constant - fixed | +0.0028 | [-0.0154, +0.0209] | 2/0/1 | +0.5778 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - feature_only | -0.0060 | [-0.0258, +0.0139] | 1/0/2 | +0.3240 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | -0.0054 | [-0.0293, +0.0185] | 1/0/2 | +0.4336 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | -0.0089 | [-0.0316, +0.0138] | 1/0/2 | +0.2328 |
| Amazon-ratings | iterative_relation_finetune | combined - feature_only | +0.0037 | [-0.0140, +0.0215] | 2/0/1 | +0.4643 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_shuffled | +0.0062 | [-0.0081, +0.0204] | 3/0/0 | +0.2040 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_constant | +0.0051 | [-0.0119, +0.0221] | 2/0/1 | +0.3286 |
| Cora | iterative_relation_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | constant_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Cora | iterative_relation_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | true reliability - constant reliability | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Cora | iterative_relation_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_finetune | feature_only - fixed | -0.0217 | [-0.0580, +0.0147] | 0/0/3 | +0.1244 |
| Cora | iterative_relation_finetune | reliability_only - fixed | -0.0253 | [-0.0738, +0.0231] | 0/0/3 | +0.1534 |
| Cora | iterative_relation_finetune | combined - fixed | -0.0110 | [-0.0510, +0.0290] | 1/0/2 | +0.3581 |
| Cora | iterative_relation_finetune | shuffled_reliability - fixed | -0.0180 | [-0.0466, +0.0106] | 0/0/3 | +0.1139 |
| Cora | iterative_relation_finetune | constant_reliability - fixed | -0.0193 | [-0.0848, +0.0461] | 1/0/2 | +0.3316 |
| Cora | iterative_relation_finetune | combined_shuffled - fixed | -0.0137 | [-0.0565, +0.0292] | 1/0/2 | +0.3035 |
| Cora | iterative_relation_finetune | combined_constant - fixed | -0.0103 | [-0.0455, +0.0248] | 1/0/2 | +0.3334 |
| Cora | iterative_relation_finetune | reliability_only - feature_only | -0.0037 | [-0.0173, +0.0100] | 0/1/2 | +0.3681 |
| Cora | iterative_relation_finetune | true reliability - shuffled reliability | -0.0073 | [-0.0412, +0.0266] | 1/0/2 | +0.4503 |
| Cora | iterative_relation_finetune | true reliability - constant reliability | -0.0060 | [-0.0288, +0.0168] | 1/0/2 | +0.3745 |
| Cora | iterative_relation_finetune | combined - feature_only | +0.0107 | [-0.0135, +0.0348] | 2/1/0 | +0.1975 |
| Cora | iterative_relation_finetune | combined - combined_shuffled | +0.0027 | [-0.0222, +0.0275] | 2/0/1 | +0.6900 |
| Cora | iterative_relation_finetune | combined - combined_constant | -0.0007 | [-0.0124, +0.0111] | 2/0/1 | +0.8298 |
| Pubmed | iterative_relation_frozen | feature_only - fixed | -0.0027 | [-0.0163, +0.0110] | 1/1/1 | +0.4899 |
| Pubmed | iterative_relation_frozen | reliability_only - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | shuffled_reliability - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | constant_reliability - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined_shuffled - fixed | -0.0033 | [-0.0221, +0.0155] | 1/1/1 | +0.5254 |
| Pubmed | iterative_relation_frozen | combined_constant - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | reliability_only - feature_only | +0.0030 | [-0.0099, +0.0159] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | combined - feature_only | +0.0033 | [-0.0089, +0.0156] | 2/1/0 | +0.3624 |
| Pubmed | iterative_relation_frozen | combined - combined_shuffled | +0.0040 | [-0.0132, +0.0212] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - combined_constant | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | feature_only - fixed | +0.0010 | [-0.0015, +0.0035] | 2/1/0 | +0.2254 |
| Pubmed | iterative_relation_finetune | reliability_only - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | shuffled_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | constant_reliability - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_shuffled - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_constant - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | reliability_only - feature_only | -0.0017 | [-0.0068, +0.0035] | 0/1/2 | +0.2999 |
| Pubmed | iterative_relation_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | true reliability - constant reliability | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - feature_only | -0.0013 | [-0.0051, +0.0025] | 0/1/2 | +0.2697 |
| Pubmed | iterative_relation_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | combined - combined_constant | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0081 | [-0.0105, +0.0268] | 2/1/0 | +0.2021 |
| Roman-empire | iterative_relation_protocol | feature_only: finetune - frozen | +0.0066 | [+0.0002, +0.0129] | 3/0/0 | +0.0466 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0096 | [+0.0074, +0.0119] | 3/0/0 | +0.0029 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0121 | [+0.0097, +0.0145] | 3/0/0 | +0.0021 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0021 | [-0.0059, +0.0100] | 2/0/1 | +0.3814 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0014 | [-0.0058, +0.0030] | 1/0/2 | +0.3001 |
| Roman-empire | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0039 | [+0.0006, +0.0073] | 3/0/0 | +0.0362 |
| Roman-empire | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0058 | [-0.0005, +0.0121] | 3/0/0 | +0.0582 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0095 | [-0.0186, +0.0377] | 2/1/0 | +0.2824 |
| Amazon-ratings | iterative_relation_protocol | feature_only: finetune - frozen | +0.0104 | [-0.0071, +0.0278] | 3/0/0 | +0.1244 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0060 | [-0.0085, +0.0206] | 2/0/1 | +0.2164 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0133 | [-0.0203, +0.0470] | 2/1/0 | +0.2306 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0109 | [-0.0048, +0.0266] | 3/0/0 | +0.0963 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0137 | [-0.0030, +0.0305] | 3/0/0 | +0.0718 |
| Amazon-ratings | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0073 | [-0.0123, +0.0270] | 2/0/1 | +0.2493 |
| Amazon-ratings | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0078 | [-0.0063, +0.0218] | 3/0/0 | +0.1400 |
| Cora | iterative_relation_protocol | fixed: finetune - frozen | +0.0230 | [-0.0511, +0.0971] | 2/0/1 | +0.3133 |
| Cora | iterative_relation_protocol | feature_only: finetune - frozen | +0.0013 | [-0.0497, +0.0523] | 1/0/2 | +0.9207 |
| Cora | iterative_relation_protocol | reliability_only: finetune - frozen | -0.0023 | [-0.0569, +0.0522] | 1/0/2 | +0.8710 |
| Cora | iterative_relation_protocol | combined: finetune - frozen | +0.0120 | [-0.0222, +0.0462] | 2/0/1 | +0.2697 |
| Cora | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0050 | [-0.0405, +0.0505] | 2/0/1 | +0.6831 |
| Cora | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0043 | [-0.0329, +0.0415] | 1/1/1 | +0.6660 |
| Cora | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0093 | [-0.0381, +0.0567] | 2/0/1 | +0.4862 |
| Cora | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0127 | [-0.0296, +0.0549] | 2/0/1 | +0.3261 |
| Pubmed | iterative_relation_protocol | fixed: finetune - frozen | +0.0020 | [-0.0066, +0.0106] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_protocol | feature_only: finetune - frozen | +0.0057 | [-0.0089, +0.0202] | 2/0/1 | +0.2359 |
| Pubmed | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0010 | [-0.0056, +0.0076] | 1/1/1 | +0.5799 |
| Pubmed | iterative_relation_protocol | combined: finetune - frozen | +0.0010 | [-0.0080, +0.0100] | 1/1/1 | +0.6784 |
| Pubmed | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0010 | [-0.0056, +0.0076] | 1/1/1 | +0.5799 |
| Pubmed | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0013 | [-0.0067, +0.0093] | 1/1/1 | +0.5471 |
| Pubmed | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0050 | [-0.0124, +0.0224] | 2/0/1 | +0.3416 |
| Pubmed | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0023 | [-0.0099, +0.0146] | 1/1/1 | +0.4987 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
