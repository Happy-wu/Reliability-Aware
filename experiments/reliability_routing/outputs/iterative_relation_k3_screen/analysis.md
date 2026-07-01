# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings, Cora, Pubmed
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial scalar-alpha adjustment: n/a
- Iterative relation steps: 3
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.
- `iterative_relation_frozen/fixed` is the same selected hidden baseline with zero relation correction.
- `iterative_relation_finetune/fixed` fine-tunes the fixed mixing architecture without a relation controller.

## Summary

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Relation/Base | Update gate | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 0.4767 | 0.4667 | +0.0100 | 0.0052 | 0.7115 | 0.0672 | 0.5137 | 0.5315 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_constant | 0.4807 | 0.4667 | +0.0140 | 0.0030 | 0.7021 | 0.0484 | 0.3709 | 0.5193 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled | 0.4784 | 0.4667 | +0.0118 | 0.0036 | 0.7118 | 0.0683 | 0.5434 | 0.5126 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability | 0.4827 | 0.4667 | +0.0161 | 0.0054 | 0.7169 | 0.0711 | 0.5605 | 0.5330 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | feature_only | 0.4815 | 0.4667 | +0.0149 | 0.0067 | 0.7135 | 0.0701 | 0.5277 | 0.5454 | 156544 | 94853 |
| Amazon-ratings | iterative_relation_finetune | fixed | 0.4753 | 0.4667 | +0.0087 | 0.0060 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 0.4798 | 0.4667 | +0.0131 | 0.0033 | 0.6963 | 0.0456 | 0.3683 | 0.5427 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability | 0.4806 | 0.4667 | +0.0140 | 0.0019 | 0.7150 | 0.0684 | 0.5481 | 0.5859 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_frozen | combined | 0.4701 | 0.4667 | +0.0035 | 0.0065 | 0.6670 | 0.0116 | 0.1012 | 0.5056 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_constant | 0.4708 | 0.4667 | +0.0041 | 0.0052 | 0.6676 | 0.0332 | 0.2222 | 0.5680 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled | 0.4710 | 0.4667 | +0.0044 | 0.0049 | 0.6674 | 0.0326 | 0.2158 | 0.5606 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability | 0.4704 | 0.4667 | +0.0037 | 0.0053 | 0.6668 | 0.0155 | 0.1225 | 0.5176 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | feature_only | 0.4704 | 0.4667 | +0.0037 | 0.0053 | 0.6670 | 0.0153 | 0.1225 | 0.5143 | 156544 | 0 |
| Amazon-ratings | iterative_relation_frozen | fixed | 0.4667 | 0.4667 | +0.0000 | 0.0086 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 0.4687 | 0.4667 | +0.0020 | 0.0064 | 0.6663 | 0.0134 | 0.1045 | 0.5159 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability | 0.4691 | 0.4667 | +0.0024 | 0.0062 | 0.6665 | 0.0141 | 0.1092 | 0.5170 | 157568 | 0 |
| Cora | iterative_relation_finetune | combined | 0.6910 | 0.6823 | +0.0087 | 0.0029 | 0.8295 | 0.0162 | 0.1242 | 0.4940 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_constant | 0.6917 | 0.6823 | +0.0093 | 0.0076 | 0.8285 | 0.0198 | 0.1381 | 0.4879 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_shuffled | 0.6900 | 0.6823 | +0.0077 | 0.0094 | 0.8294 | 0.0172 | 0.1186 | 0.4913 | 166144 | 167495 |
| Cora | iterative_relation_finetune | constant_reliability | 0.6840 | 0.6823 | +0.0017 | 0.0106 | 0.8271 | 0.0200 | 0.1240 | 0.4907 | 157568 | 167495 |
| Cora | iterative_relation_finetune | feature_only | 0.6823 | 0.6823 | +0.0000 | 0.0087 | 0.8303 | 0.0108 | 0.1084 | 0.4895 | 156544 | 167495 |
| Cora | iterative_relation_finetune | fixed | 0.7147 | 0.6823 | +0.0323 | 0.0033 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 167495 |
| Cora | iterative_relation_finetune | reliability_only | 0.6863 | 0.6823 | +0.0040 | 0.0061 | 0.8306 | 0.0108 | 0.0615 | 0.4949 | 157568 | 167495 |
| Cora | iterative_relation_finetune | shuffled_reliability | 0.6880 | 0.6823 | +0.0057 | 0.0102 | 0.8280 | 0.0159 | 0.0784 | 0.5026 | 157568 | 167495 |
| Cora | iterative_relation_frozen | combined | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_constant | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4962 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_shuffled | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | constant_reliability | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4978 | 157568 | 0 |
| Cora | iterative_relation_frozen | feature_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4950 | 156544 | 0 |
| Cora | iterative_relation_frozen | fixed | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Cora | iterative_relation_frozen | reliability_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4972 | 157568 | 0 |
| Cora | iterative_relation_frozen | shuffled_reliability | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4972 | 157568 | 0 |
| Pubmed | iterative_relation_finetune | combined | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8316 | 0.0018 | 0.0316 | 0.4991 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_constant | 0.7397 | 0.7377 | +0.0020 | 0.0116 | 0.8315 | 0.0018 | 0.0339 | 0.5069 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_shuffled | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8311 | 0.0022 | 0.0367 | 0.5040 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | constant_reliability | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8306 | 0.0027 | 0.0401 | 0.5087 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | feature_only | 0.7413 | 0.7377 | +0.0037 | 0.0146 | 0.8291 | 0.0082 | 0.0975 | 0.4988 | 156544 | 107523 |
| Pubmed | iterative_relation_finetune | fixed | 0.7397 | 0.7377 | +0.0020 | 0.0116 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 107523 |
| Pubmed | iterative_relation_finetune | reliability_only | 0.7397 | 0.7377 | +0.0020 | 0.0116 | 0.8312 | 0.0021 | 0.0439 | 0.4925 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | shuffled_reliability | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8312 | 0.0021 | 0.0450 | 0.4964 | 157568 | 107523 |
| Pubmed | iterative_relation_frozen | combined | 0.7383 | 0.7377 | +0.0007 | 0.0083 | 0.8335 | 0.0008 | 0.0028 | 0.5040 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_constant | 0.7383 | 0.7377 | +0.0007 | 0.0083 | 0.8335 | 0.0010 | 0.0033 | 0.5072 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_shuffled | 0.7360 | 0.7377 | -0.0017 | 0.0100 | 0.8362 | 0.0291 | 0.0792 | 0.5267 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | constant_reliability | 0.7377 | 0.7377 | +0.0000 | 0.0088 | 0.8342 | 0.0080 | 0.0248 | 0.5187 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | feature_only | 0.7387 | 0.7377 | +0.0010 | 0.0080 | 0.8337 | 0.0023 | 0.0083 | 0.5040 | 156544 | 0 |
| Pubmed | iterative_relation_frozen | fixed | 0.7377 | 0.7377 | +0.0000 | 0.0088 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Pubmed | iterative_relation_frozen | reliability_only | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8334 | 0.0006 | 0.0021 | 0.5011 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | shuffled_reliability | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8336 | 0.0025 | 0.0081 | 0.5057 | 157568 | 0 |
| Roman-empire | iterative_relation_finetune | combined | 0.8457 | 0.8166 | +0.0291 | 0.0055 | 0.7830 | 0.0502 | 0.5741 | 0.5084 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_constant | 0.8237 | 0.8166 | +0.0071 | 0.0081 | 0.7812 | 0.0429 | 0.4107 | 0.4810 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_shuffled | 0.8196 | 0.8166 | +0.0029 | 0.0081 | 0.7634 | 0.0180 | 0.1781 | 0.4546 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | constant_reliability | 0.8200 | 0.8166 | +0.0034 | 0.0088 | 0.7636 | 0.0180 | 0.1710 | 0.4615 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | feature_only | 0.8237 | 0.8166 | +0.0071 | 0.0068 | 0.7801 | 0.0392 | 0.3728 | 0.4923 | 156544 | 95698 |
| Roman-empire | iterative_relation_finetune | fixed | 0.8235 | 0.8166 | +0.0069 | 0.0055 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | iterative_relation_finetune | reliability_only | 0.8466 | 0.8166 | +0.0299 | 0.0069 | 0.7806 | 0.0473 | 0.5565 | 0.4791 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability | 0.8243 | 0.8166 | +0.0077 | 0.0065 | 0.7803 | 0.0392 | 0.3673 | 0.4922 | 157568 | 95698 |
| Roman-empire | iterative_relation_frozen | combined | 0.8332 | 0.8166 | +0.0165 | 0.0045 | 0.7678 | 0.0574 | 0.6604 | 0.5020 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_constant | 0.8185 | 0.8166 | +0.0019 | 0.0063 | 0.7704 | 0.0423 | 0.3753 | 0.4513 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_shuffled | 0.8210 | 0.8166 | +0.0044 | 0.0064 | 0.7752 | 0.0501 | 0.4935 | 0.4810 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | constant_reliability | 0.8246 | 0.8166 | +0.0080 | 0.0088 | 0.7764 | 0.0618 | 0.5073 | 0.4687 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | feature_only | 0.8192 | 0.8166 | +0.0025 | 0.0071 | 0.7702 | 0.0405 | 0.3822 | 0.4312 | 156544 | 0 |
| Roman-empire | iterative_relation_frozen | fixed | 0.8166 | 0.8166 | +0.0000 | 0.0042 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | iterative_relation_frozen | reliability_only | 0.8356 | 0.8166 | +0.0190 | 0.0060 | 0.7684 | 0.0590 | 0.6721 | 0.5144 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability | 0.8213 | 0.8166 | +0.0047 | 0.0066 | 0.7721 | 0.0483 | 0.4823 | 0.4874 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | feature_only - fixed | +0.0025 | [-0.0120, +0.0170] | 2/0/1 | +0.5313 |
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0190 | [+0.0101, +0.0279] | 3/0/0 | +0.0115 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0165 | [+0.0011, +0.0320] | 3/0/0 | +0.0441 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0047 | [-0.0104, +0.0198] | 2/0/1 | +0.3110 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0080 | [-0.0126, +0.0286] | 2/0/1 | +0.2371 |
| Roman-empire | iterative_relation_frozen | combined_shuffled - fixed | +0.0044 | [-0.0108, +0.0197] | 2/0/1 | +0.3391 |
| Roman-empire | iterative_relation_frozen | combined_constant - fixed | +0.0019 | [-0.0109, +0.0147] | 2/0/1 | +0.5916 |
| Roman-empire | iterative_relation_frozen | reliability_only - feature_only | +0.0165 | [+0.0105, +0.0224] | 3/0/0 | +0.0070 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0143 | [+0.0066, +0.0220] | 3/0/0 | +0.0152 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0110 | [-0.0010, +0.0230] | 3/0/0 | +0.0590 |
| Roman-empire | iterative_relation_frozen | combined - feature_only | +0.0140 | [+0.0016, +0.0264] | 3/0/0 | +0.0399 |
| Roman-empire | iterative_relation_frozen | combined - combined_shuffled | +0.0121 | [+0.0038, +0.0205] | 3/0/0 | +0.0248 |
| Roman-empire | iterative_relation_frozen | combined - combined_constant | +0.0146 | [+0.0048, +0.0245] | 3/0/0 | +0.0237 |
| Roman-empire | iterative_relation_finetune | feature_only - fixed | +0.0002 | [-0.0064, +0.0068] | 1/1/1 | +0.8921 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0231 | [+0.0145, +0.0317] | 3/0/0 | +0.0074 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0222 | [+0.0139, +0.0305] | 3/0/0 | +0.0075 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | +0.0008 | [-0.0027, +0.0044] | 1/2/0 | +0.4226 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0035 | [-0.0240, +0.0170] | 1/1/1 | +0.5417 |
| Roman-empire | iterative_relation_finetune | combined_shuffled - fixed | -0.0039 | [-0.0232, +0.0153] | 1/1/1 | +0.4719 |
| Roman-empire | iterative_relation_finetune | combined_constant - fixed | +0.0002 | [-0.0123, +0.0127] | 1/1/1 | +0.9571 |
| Roman-empire | iterative_relation_finetune | reliability_only - feature_only | +0.0228 | [+0.0204, +0.0252] | 3/0/0 | +0.0006 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0222 | [+0.0161, +0.0283] | 3/0/0 | +0.0040 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0265 | [+0.0141, +0.0389] | 3/0/0 | +0.0116 |
| Roman-empire | iterative_relation_finetune | combined - feature_only | +0.0219 | [+0.0164, +0.0275] | 3/0/0 | +0.0035 |
| Roman-empire | iterative_relation_finetune | combined - combined_shuffled | +0.0261 | [+0.0148, +0.0374] | 3/0/0 | +0.0099 |
| Roman-empire | iterative_relation_finetune | combined - combined_constant | +0.0220 | [+0.0140, +0.0300] | 3/0/0 | +0.0071 |
| Amazon-ratings | iterative_relation_frozen | feature_only - fixed | +0.0037 | [-0.0063, +0.0137] | 2/1/0 | +0.2530 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0020 | [-0.0056, +0.0097] | 2/1/0 | +0.3741 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0035 | [-0.0041, +0.0110] | 2/1/0 | +0.1851 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0024 | [-0.0052, +0.0101] | 2/1/0 | +0.2999 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0037 | [-0.0066, +0.0140] | 2/1/0 | +0.2612 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled - fixed | +0.0044 | [-0.0070, +0.0158] | 2/1/0 | +0.2419 |
| Amazon-ratings | iterative_relation_frozen | combined_constant - fixed | +0.0041 | [-0.0062, +0.0145] | 2/1/0 | +0.2275 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - feature_only | -0.0017 | [-0.0053, +0.0019] | 0/1/2 | +0.1839 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0004 | [-0.0017, +0.0008] | 0/1/2 | +0.2697 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0017 | [-0.0053, +0.0019] | 0/1/2 | +0.1839 |
| Amazon-ratings | iterative_relation_frozen | combined - feature_only | -0.0002 | [-0.0055, +0.0051] | 1/1/1 | +0.8758 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_shuffled | -0.0009 | [-0.0069, +0.0051] | 1/1/1 | +0.5949 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_constant | -0.0007 | [-0.0053, +0.0040] | 1/1/1 | +0.6090 |
| Amazon-ratings | iterative_relation_finetune | feature_only - fixed | +0.0062 | [-0.0306, +0.0430] | 2/0/1 | +0.5439 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | +0.0045 | [-0.0232, +0.0321] | 1/1/1 | +0.5596 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | +0.0014 | [-0.0326, +0.0354] | 1/0/2 | +0.8791 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | +0.0053 | [-0.0081, +0.0187] | 2/1/0 | +0.2286 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | +0.0074 | [-0.0258, +0.0406] | 2/0/1 | +0.4390 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled - fixed | +0.0031 | [-0.0247, +0.0309] | 2/0/1 | +0.6789 |
| Amazon-ratings | iterative_relation_finetune | combined_constant - fixed | +0.0054 | [-0.0196, +0.0304] | 1/1/1 | +0.4510 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - feature_only | -0.0017 | [-0.0197, +0.0162] | 1/0/2 | +0.7168 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | -0.0009 | [-0.0166, +0.0148] | 1/0/2 | +0.8334 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | -0.0029 | [-0.0178, +0.0119] | 1/0/2 | +0.4831 |
| Amazon-ratings | iterative_relation_finetune | combined - feature_only | -0.0048 | [-0.0149, +0.0052] | 0/0/3 | +0.1728 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_shuffled | -0.0017 | [-0.0105, +0.0070] | 1/0/2 | +0.4808 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_constant | -0.0040 | [-0.0175, +0.0094] | 0/0/3 | +0.3270 |
| Cora | iterative_relation_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | iterative_relation_finetune | feature_only - fixed | -0.0323 | [-0.0489, -0.0158] | 0/0/3 | +0.0138 |
| Cora | iterative_relation_finetune | reliability_only - fixed | -0.0283 | [-0.0384, -0.0183] | 0/0/3 | +0.0067 |
| Cora | iterative_relation_finetune | combined - fixed | -0.0237 | [-0.0324, -0.0149] | 0/0/3 | +0.0073 |
| Cora | iterative_relation_finetune | shuffled_reliability - fixed | -0.0267 | [-0.0503, -0.0031] | 0/0/3 | +0.0398 |
| Cora | iterative_relation_finetune | constant_reliability - fixed | -0.0307 | [-0.0555, -0.0058] | 0/0/3 | +0.0338 |
| Cora | iterative_relation_finetune | combined_shuffled - fixed | -0.0247 | [-0.0433, -0.0060] | 0/0/3 | +0.0295 |
| Cora | iterative_relation_finetune | combined_constant - fixed | -0.0230 | [-0.0361, -0.0099] | 0/0/3 | +0.0172 |
| Cora | iterative_relation_finetune | reliability_only - feature_only | +0.0040 | [-0.0068, +0.0148] | 3/0/0 | +0.2529 |
| Cora | iterative_relation_finetune | true reliability - shuffled reliability | -0.0017 | [-0.0153, +0.0120] | 1/0/2 | +0.6525 |
| Cora | iterative_relation_finetune | true reliability - constant reliability | +0.0023 | [-0.0250, +0.0297] | 2/0/1 | +0.7489 |
| Cora | iterative_relation_finetune | combined - feature_only | +0.0087 | [-0.0143, +0.0316] | 2/0/1 | +0.2457 |
| Cora | iterative_relation_finetune | combined - combined_shuffled | +0.0010 | [-0.0230, +0.0250] | 2/0/1 | +0.8740 |
| Cora | iterative_relation_finetune | combined - combined_constant | -0.0007 | [-0.0209, +0.0196] | 2/0/1 | +0.9003 |
| Pubmed | iterative_relation_frozen | feature_only - fixed | +0.0010 | [-0.0033, +0.0053] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | reliability_only - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | shuffled_reliability - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | combined_shuffled - fixed | -0.0017 | [-0.0111, +0.0077] | 1/1/1 | +0.5254 |
| Pubmed | iterative_relation_frozen | combined_constant - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | reliability_only - feature_only | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | true reliability - constant reliability | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - feature_only | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - combined_shuffled | +0.0023 | [-0.0057, +0.0103] | 2/1/0 | +0.3356 |
| Pubmed | iterative_relation_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | feature_only - fixed | +0.0017 | [-0.0077, +0.0111] | 1/1/1 | +0.5254 |
| Pubmed | iterative_relation_finetune | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | combined - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | shuffled_reliability - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | constant_reliability - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_shuffled - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | reliability_only - feature_only | -0.0017 | [-0.0111, +0.0077] | 1/1/1 | +0.5254 |
| Pubmed | iterative_relation_finetune | true reliability - shuffled reliability | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | true reliability - constant reliability | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - feature_only | -0.0020 | [-0.0128, +0.0088] | 1/1/1 | +0.5101 |
| Pubmed | iterative_relation_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | combined - combined_constant | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0069 | [-0.0092, +0.0230] | 2/1/0 | +0.2075 |
| Roman-empire | iterative_relation_protocol | feature_only: finetune - frozen | +0.0046 | [+0.0015, +0.0077] | 3/0/0 | +0.0233 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0109 | [+0.0051, +0.0167] | 3/0/0 | +0.0148 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0125 | [+0.0027, +0.0223] | 3/0/0 | +0.0314 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0030 | [-0.0004, +0.0064] | 3/0/0 | +0.0637 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0046 | [-0.0202, +0.0110] | 1/0/2 | +0.3333 |
| Roman-empire | iterative_relation_protocol | combined_shuffled: finetune - frozen | -0.0015 | [-0.0166, +0.0137] | 2/0/1 | +0.7166 |
| Roman-empire | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0052 | [-0.0008, +0.0112] | 3/0/0 | +0.0652 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0087 | [-0.0286, +0.0459] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | feature_only: finetune - frozen | +0.0112 | [-0.0007, +0.0230] | 3/0/0 | +0.0557 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0111 | [-0.0128, +0.0350] | 2/1/0 | +0.1835 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0065 | [-0.0094, +0.0225] | 2/0/1 | +0.2204 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0115 | [-0.0075, +0.0306] | 3/0/0 | +0.1213 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0124 | [+0.0021, +0.0227] | 3/0/0 | +0.0355 |
| Amazon-ratings | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0074 | [-0.0004, +0.0152] | 3/0/0 | +0.0546 |
| Amazon-ratings | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0099 | [-0.0120, +0.0318] | 2/1/0 | +0.1905 |
| Cora | iterative_relation_protocol | fixed: finetune - frozen | +0.0323 | [-0.0032, +0.0678] | 3/0/0 | +0.0594 |
| Cora | iterative_relation_protocol | feature_only: finetune - frozen | +0.0000 | [-0.0499, +0.0499] | 1/0/2 | +1.0000 |
| Cora | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0040 | [-0.0415, +0.0495] | 1/1/1 | +0.7418 |
| Cora | iterative_relation_protocol | combined: finetune - frozen | +0.0087 | [-0.0186, +0.0359] | 2/1/0 | +0.3046 |
| Cora | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0057 | [-0.0532, +0.0646] | 2/0/1 | +0.7191 |
| Cora | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0017 | [-0.0417, +0.0451] | 1/0/2 | +0.8840 |
| Cora | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0077 | [-0.0426, +0.0579] | 1/0/2 | +0.5790 |
| Cora | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0093 | [-0.0381, +0.0567] | 2/0/1 | +0.4862 |
| Pubmed | iterative_relation_protocol | fixed: finetune - frozen | +0.0020 | [-0.0066, +0.0106] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_protocol | feature_only: finetune - frozen | +0.0027 | [-0.0176, +0.0229] | 1/0/2 | +0.6278 |
| Pubmed | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0017 | [-0.0077, +0.0111] | 1/1/1 | +0.5254 |
| Pubmed | iterative_relation_protocol | combined: finetune - frozen | +0.0010 | [-0.0080, +0.0100] | 1/1/1 | +0.6784 |
| Pubmed | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0013 | [-0.0067, +0.0093] | 1/1/1 | +0.5471 |
| Pubmed | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0017 | [-0.0055, +0.0088] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0033 | [-0.0061, +0.0127] | 2/0/1 | +0.2668 |
| Pubmed | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0013 | [-0.0090, +0.0117] | 1/1/1 | +0.6349 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
