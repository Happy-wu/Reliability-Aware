# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings, Cora, Pubmed
- Families: iterative_relation_frozen, iterative_relation_finetune
- Runs: 3
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial scalar-alpha adjustment: n/a
- Iterative relation steps: 2
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.
- `iterative_relation_frozen/fixed` is the same selected hidden baseline with zero relation correction.
- `iterative_relation_finetune/fixed` fine-tunes the fixed mixing architecture without a relation controller.

## Summary

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Relation/Base | Update gate | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | iterative_relation_finetune | combined | 0.4772 | 0.4667 | +0.0105 | 0.0042 | 0.6966 | 0.0461 | 0.3654 | 0.5330 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_constant | 0.4810 | 0.4667 | +0.0143 | 0.0019 | 0.7172 | 0.0705 | 0.5535 | 0.5044 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled | 0.4804 | 0.4667 | +0.0137 | 0.0023 | 0.7128 | 0.0684 | 0.5596 | 0.5410 | 166144 | 94853 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability | 0.4816 | 0.4667 | +0.0150 | 0.0020 | 0.7184 | 0.0734 | 0.5815 | 0.5316 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | feature_only | 0.4834 | 0.4667 | +0.0168 | 0.0035 | 0.7163 | 0.0708 | 0.5525 | 0.5663 | 156544 | 94853 |
| Amazon-ratings | iterative_relation_finetune | fixed | 0.4808 | 0.4667 | +0.0141 | 0.0038 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 94853 |
| Amazon-ratings | iterative_relation_finetune | reliability_only | 0.4879 | 0.4667 | +0.0212 | 0.0007 | 0.7118 | 0.0682 | 0.5590 | 0.5536 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability | 0.4745 | 0.4667 | +0.0078 | 0.0059 | 0.6984 | 0.0455 | 0.3612 | 0.5515 | 157568 | 94853 |
| Amazon-ratings | iterative_relation_frozen | combined | 0.4700 | 0.4667 | +0.0033 | 0.0067 | 0.6670 | 0.0113 | 0.0996 | 0.4993 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_constant | 0.4692 | 0.4667 | +0.0025 | 0.0057 | 0.6671 | 0.0175 | 0.1216 | 0.5253 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled | 0.4706 | 0.4667 | +0.0040 | 0.0053 | 0.6672 | 0.0170 | 0.1419 | 0.5078 | 166144 | 0 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability | 0.4701 | 0.4667 | +0.0034 | 0.0054 | 0.6668 | 0.0151 | 0.1208 | 0.5070 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | feature_only | 0.4702 | 0.4667 | +0.0035 | 0.0055 | 0.6669 | 0.0151 | 0.1215 | 0.5030 | 156544 | 0 |
| Amazon-ratings | iterative_relation_frozen | fixed | 0.4667 | 0.4667 | +0.0000 | 0.0086 | 0.6667 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Amazon-ratings | iterative_relation_frozen | reliability_only | 0.4687 | 0.4667 | +0.0021 | 0.0063 | 0.6663 | 0.0130 | 0.1009 | 0.5075 | 157568 | 0 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability | 0.4689 | 0.4667 | +0.0023 | 0.0062 | 0.6665 | 0.0136 | 0.1059 | 0.5058 | 157568 | 0 |
| Cora | iterative_relation_finetune | combined | 0.6937 | 0.6823 | +0.0113 | 0.0037 | 0.8294 | 0.0167 | 0.1306 | 0.5013 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_constant | 0.6950 | 0.6823 | +0.0127 | 0.0051 | 0.8288 | 0.0199 | 0.1506 | 0.5019 | 166144 | 167495 |
| Cora | iterative_relation_finetune | combined_shuffled | 0.6867 | 0.6823 | +0.0043 | 0.0077 | 0.8293 | 0.0159 | 0.1202 | 0.5005 | 166144 | 167495 |
| Cora | iterative_relation_finetune | constant_reliability | 0.6887 | 0.6823 | +0.0063 | 0.0054 | 0.8267 | 0.0191 | 0.0792 | 0.4976 | 157568 | 167495 |
| Cora | iterative_relation_finetune | feature_only | 0.6820 | 0.6823 | -0.0003 | 0.0085 | 0.8300 | 0.0111 | 0.1034 | 0.4950 | 156544 | 167495 |
| Cora | iterative_relation_finetune | fixed | 0.7020 | 0.6823 | +0.0197 | 0.0143 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 167495 |
| Cora | iterative_relation_finetune | reliability_only | 0.6897 | 0.6823 | +0.0073 | 0.0058 | 0.8308 | 0.0107 | 0.0633 | 0.5038 | 157568 | 167495 |
| Cora | iterative_relation_finetune | shuffled_reliability | 0.6860 | 0.6823 | +0.0037 | 0.0049 | 0.8302 | 0.0124 | 0.0578 | 0.4938 | 157568 | 167495 |
| Cora | iterative_relation_frozen | combined | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_constant | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4962 | 166144 | 0 |
| Cora | iterative_relation_frozen | combined_shuffled | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4957 | 166144 | 0 |
| Cora | iterative_relation_frozen | constant_reliability | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4977 | 157568 | 0 |
| Cora | iterative_relation_frozen | feature_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4951 | 156544 | 0 |
| Cora | iterative_relation_frozen | fixed | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Cora | iterative_relation_frozen | reliability_only | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4971 | 157568 | 0 |
| Cora | iterative_relation_frozen | shuffled_reliability | 0.6823 | 0.6823 | +0.0000 | 0.0094 | 0.8333 | 0.0000 | 0.0000 | 0.4971 | 157568 | 0 |
| Pubmed | iterative_relation_finetune | combined | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8315 | 0.0019 | 0.0295 | 0.5025 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_constant | 0.7393 | 0.7377 | +0.0017 | 0.0111 | 0.8314 | 0.0019 | 0.0406 | 0.5065 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | combined_shuffled | 0.7387 | 0.7377 | +0.0010 | 0.0102 | 0.8316 | 0.0018 | 0.0350 | 0.5051 | 166144 | 107523 |
| Pubmed | iterative_relation_finetune | constant_reliability | 0.7387 | 0.7377 | +0.0010 | 0.0102 | 0.8304 | 0.0030 | 0.0320 | 0.5048 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | feature_only | 0.7400 | 0.7377 | +0.0023 | 0.0108 | 0.8299 | 0.0072 | 0.0707 | 0.5044 | 156544 | 107523 |
| Pubmed | iterative_relation_finetune | fixed | 0.7397 | 0.7377 | +0.0020 | 0.0116 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 107523 |
| Pubmed | iterative_relation_finetune | reliability_only | 0.7403 | 0.7377 | +0.0027 | 0.0126 | 0.8313 | 0.0020 | 0.0439 | 0.4929 | 157568 | 107523 |
| Pubmed | iterative_relation_finetune | shuffled_reliability | 0.7390 | 0.7377 | +0.0013 | 0.0107 | 0.8308 | 0.0025 | 0.0407 | 0.4961 | 157568 | 107523 |
| Pubmed | iterative_relation_frozen | combined | 0.7383 | 0.7377 | +0.0007 | 0.0083 | 0.8335 | 0.0007 | 0.0027 | 0.5039 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_constant | 0.7383 | 0.7377 | +0.0007 | 0.0083 | 0.8335 | 0.0009 | 0.0031 | 0.5070 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | combined_shuffled | 0.7350 | 0.7377 | -0.0027 | 0.0112 | 0.8357 | 0.0295 | 0.0815 | 0.5244 | 166144 | 0 |
| Pubmed | iterative_relation_frozen | constant_reliability | 0.7373 | 0.7377 | -0.0003 | 0.0091 | 0.8342 | 0.0076 | 0.0239 | 0.5144 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | feature_only | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8341 | 0.0051 | 0.0183 | 0.5050 | 156544 | 0 |
| Pubmed | iterative_relation_frozen | fixed | 0.7377 | 0.7377 | +0.0000 | 0.0088 | 0.8333 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Pubmed | iterative_relation_frozen | reliability_only | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8334 | 0.0006 | 0.0020 | 0.5008 | 157568 | 0 |
| Pubmed | iterative_relation_frozen | shuffled_reliability | 0.7380 | 0.7377 | +0.0003 | 0.0085 | 0.8336 | 0.0024 | 0.0078 | 0.5043 | 157568 | 0 |
| Roman-empire | iterative_relation_finetune | combined | 0.8463 | 0.8166 | +0.0297 | 0.0055 | 0.7835 | 0.0499 | 0.5721 | 0.5044 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_constant | 0.8213 | 0.8166 | +0.0047 | 0.0106 | 0.7643 | 0.0201 | 0.1992 | 0.4573 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | combined_shuffled | 0.8202 | 0.8166 | +0.0036 | 0.0090 | 0.7636 | 0.0186 | 0.1825 | 0.4557 | 166144 | 95698 |
| Roman-empire | iterative_relation_finetune | constant_reliability | 0.8210 | 0.8166 | +0.0044 | 0.0101 | 0.7638 | 0.0187 | 0.1800 | 0.4609 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | feature_only | 0.8207 | 0.8166 | +0.0041 | 0.0097 | 0.7638 | 0.0178 | 0.1729 | 0.4682 | 156544 | 95698 |
| Roman-empire | iterative_relation_finetune | fixed | 0.8253 | 0.8166 | +0.0086 | 0.0066 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 95698 |
| Roman-empire | iterative_relation_finetune | reliability_only | 0.8447 | 0.8166 | +0.0281 | 0.0062 | 0.7806 | 0.0483 | 0.5611 | 0.4981 | 157568 | 95698 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability | 0.8250 | 0.8166 | +0.0084 | 0.0063 | 0.7804 | 0.0392 | 0.3594 | 0.4949 | 157568 | 95698 |
| Roman-empire | iterative_relation_frozen | combined | 0.8315 | 0.8166 | +0.0149 | 0.0058 | 0.7631 | 0.0597 | 0.7176 | 0.4943 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_constant | 0.8201 | 0.8166 | +0.0035 | 0.0075 | 0.7706 | 0.0380 | 0.3717 | 0.4344 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | combined_shuffled | 0.8195 | 0.8166 | +0.0029 | 0.0067 | 0.7695 | 0.0348 | 0.3706 | 0.4602 | 166144 | 0 |
| Roman-empire | iterative_relation_frozen | constant_reliability | 0.8247 | 0.8166 | +0.0081 | 0.0078 | 0.7777 | 0.0622 | 0.4910 | 0.4539 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | feature_only | 0.8200 | 0.8166 | +0.0034 | 0.0076 | 0.7695 | 0.0372 | 0.3751 | 0.4270 | 156544 | 0 |
| Roman-empire | iterative_relation_frozen | fixed | 0.8166 | 0.8166 | +0.0000 | 0.0042 | 0.7500 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 |
| Roman-empire | iterative_relation_frozen | reliability_only | 0.8364 | 0.8166 | +0.0198 | 0.0050 | 0.7642 | 0.0613 | 0.7396 | 0.5059 | 157568 | 0 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability | 0.8213 | 0.8166 | +0.0046 | 0.0076 | 0.7735 | 0.0447 | 0.4511 | 0.4667 | 157568 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | iterative_relation_frozen | feature_only - fixed | +0.0034 | [-0.0116, +0.0183] | 2/0/1 | +0.4357 |
| Roman-empire | iterative_relation_frozen | reliability_only - fixed | +0.0198 | [+0.0114, +0.0281] | 3/0/0 | +0.0095 |
| Roman-empire | iterative_relation_frozen | combined - fixed | +0.0149 | [+0.0058, +0.0240] | 3/0/0 | +0.0197 |
| Roman-empire | iterative_relation_frozen | shuffled_reliability - fixed | +0.0046 | [-0.0124, +0.0217] | 2/0/1 | +0.3606 |
| Roman-empire | iterative_relation_frozen | constant_reliability - fixed | +0.0081 | [-0.0081, +0.0242] | 3/0/0 | +0.1653 |
| Roman-empire | iterative_relation_frozen | combined_shuffled - fixed | +0.0029 | [-0.0100, +0.0158] | 2/0/1 | +0.4386 |
| Roman-empire | iterative_relation_frozen | combined_constant - fixed | +0.0035 | [-0.0113, +0.0182] | 2/0/1 | +0.4174 |
| Roman-empire | iterative_relation_frozen | reliability_only - feature_only | +0.0164 | [+0.0085, +0.0243] | 3/0/0 | +0.0123 |
| Roman-empire | iterative_relation_frozen | true reliability - shuffled reliability | +0.0151 | [+0.0062, +0.0241] | 3/0/0 | +0.0184 |
| Roman-empire | iterative_relation_frozen | true reliability - constant reliability | +0.0117 | [+0.0029, +0.0205] | 3/0/0 | +0.0294 |
| Roman-empire | iterative_relation_frozen | combined - feature_only | +0.0115 | [+0.0056, +0.0175] | 3/0/0 | +0.0139 |
| Roman-empire | iterative_relation_frozen | combined - combined_shuffled | +0.0120 | [+0.0082, +0.0158] | 3/0/0 | +0.0054 |
| Roman-empire | iterative_relation_frozen | combined - combined_constant | +0.0114 | [+0.0057, +0.0171] | 3/0/0 | +0.0132 |
| Roman-empire | iterative_relation_finetune | feature_only - fixed | -0.0046 | [-0.0290, +0.0199] | 1/1/1 | +0.5040 |
| Roman-empire | iterative_relation_finetune | reliability_only - fixed | +0.0195 | [+0.0054, +0.0336] | 3/0/0 | +0.0271 |
| Roman-empire | iterative_relation_finetune | combined - fixed | +0.0211 | [+0.0049, +0.0372] | 3/0/0 | +0.0303 |
| Roman-empire | iterative_relation_finetune | shuffled_reliability - fixed | -0.0003 | [-0.0016, +0.0010] | 0/2/1 | +0.4226 |
| Roman-empire | iterative_relation_finetune | constant_reliability - fixed | -0.0043 | [-0.0295, +0.0209] | 1/1/1 | +0.5398 |
| Roman-empire | iterative_relation_finetune | combined_shuffled - fixed | -0.0051 | [-0.0284, +0.0182] | 1/1/1 | +0.4489 |
| Roman-empire | iterative_relation_finetune | combined_constant - fixed | -0.0039 | [-0.0301, +0.0222] | 1/1/1 | +0.5836 |
| Roman-empire | iterative_relation_finetune | reliability_only - feature_only | +0.0241 | [+0.0122, +0.0359] | 3/0/0 | +0.0128 |
| Roman-empire | iterative_relation_finetune | true reliability - shuffled reliability | +0.0198 | [+0.0052, +0.0343] | 3/0/0 | +0.0280 |
| Roman-empire | iterative_relation_finetune | true reliability - constant reliability | +0.0238 | [+0.0108, +0.0367] | 3/0/0 | +0.0156 |
| Roman-empire | iterative_relation_finetune | combined - feature_only | +0.0257 | [+0.0128, +0.0385] | 3/0/0 | +0.0132 |
| Roman-empire | iterative_relation_finetune | combined - combined_shuffled | +0.0261 | [+0.0152, +0.0370] | 3/0/0 | +0.0093 |
| Roman-empire | iterative_relation_finetune | combined - combined_constant | +0.0250 | [+0.0095, +0.0405] | 3/0/0 | +0.0202 |
| Amazon-ratings | iterative_relation_frozen | feature_only - fixed | +0.0035 | [-0.0061, +0.0132] | 2/1/0 | +0.2543 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - fixed | +0.0021 | [-0.0058, +0.0099] | 2/1/0 | +0.3755 |
| Amazon-ratings | iterative_relation_frozen | combined - fixed | +0.0033 | [-0.0038, +0.0105] | 2/1/0 | +0.1836 |
| Amazon-ratings | iterative_relation_frozen | shuffled_reliability - fixed | +0.0023 | [-0.0055, +0.0101] | 2/1/0 | +0.3356 |
| Amazon-ratings | iterative_relation_frozen | constant_reliability - fixed | +0.0034 | [-0.0065, +0.0134] | 2/1/0 | +0.2767 |
| Amazon-ratings | iterative_relation_frozen | combined_shuffled - fixed | +0.0040 | [-0.0060, +0.0139] | 2/1/0 | +0.2275 |
| Amazon-ratings | iterative_relation_frozen | combined_constant - fixed | +0.0025 | [-0.0083, +0.0133] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_frozen | reliability_only - feature_only | -0.0015 | [-0.0047, +0.0018] | 0/1/2 | +0.1885 |
| Amazon-ratings | iterative_relation_frozen | true reliability - shuffled reliability | -0.0002 | [-0.0008, +0.0004] | 0/1/2 | +0.2697 |
| Amazon-ratings | iterative_relation_frozen | true reliability - constant reliability | -0.0014 | [-0.0043, +0.0016] | 0/1/2 | +0.1842 |
| Amazon-ratings | iterative_relation_frozen | combined - feature_only | -0.0002 | [-0.0059, +0.0055] | 1/1/1 | +0.8845 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_shuffled | -0.0007 | [-0.0057, +0.0044] | 1/1/1 | +0.6348 |
| Amazon-ratings | iterative_relation_frozen | combined - combined_constant | +0.0008 | [-0.0085, +0.0101] | 1/1/1 | +0.7418 |
| Amazon-ratings | iterative_relation_finetune | feature_only - fixed | +0.0027 | [-0.0113, +0.0166] | 1/0/2 | +0.4978 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - fixed | +0.0071 | [-0.0038, +0.0181] | 3/0/0 | +0.1075 |
| Amazon-ratings | iterative_relation_finetune | combined - fixed | -0.0036 | [-0.0257, +0.0185] | 1/1/1 | +0.5564 |
| Amazon-ratings | iterative_relation_finetune | shuffled_reliability - fixed | -0.0063 | [-0.0356, +0.0231] | 1/0/2 | +0.4553 |
| Amazon-ratings | iterative_relation_finetune | constant_reliability - fixed | +0.0009 | [-0.0160, +0.0177] | 2/0/1 | +0.8446 |
| Amazon-ratings | iterative_relation_finetune | combined_shuffled - fixed | -0.0004 | [-0.0183, +0.0175] | 2/0/1 | +0.9354 |
| Amazon-ratings | iterative_relation_finetune | combined_constant - fixed | +0.0002 | [-0.0156, +0.0160] | 1/1/1 | +0.9582 |
| Amazon-ratings | iterative_relation_finetune | reliability_only - feature_only | +0.0045 | [-0.0039, +0.0128] | 3/0/0 | +0.1478 |
| Amazon-ratings | iterative_relation_finetune | true reliability - shuffled reliability | +0.0134 | [-0.0050, +0.0318] | 3/0/0 | +0.0884 |
| Amazon-ratings | iterative_relation_finetune | true reliability - constant reliability | +0.0063 | [+0.0004, +0.0121] | 3/0/0 | +0.0445 |
| Amazon-ratings | iterative_relation_finetune | combined - feature_only | -0.0063 | [-0.0288, +0.0163] | 1/0/2 | +0.3551 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_shuffled | -0.0032 | [-0.0101, +0.0037] | 0/1/2 | +0.1846 |
| Amazon-ratings | iterative_relation_finetune | combined - combined_constant | -0.0038 | [-0.0184, +0.0108] | 1/0/2 | +0.3774 |
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
| Cora | iterative_relation_finetune | feature_only - fixed | -0.0200 | [-0.0459, +0.0059] | 0/0/3 | +0.0801 |
| Cora | iterative_relation_finetune | reliability_only - fixed | -0.0123 | [-0.0384, +0.0138] | 0/0/3 | +0.1790 |
| Cora | iterative_relation_finetune | combined - fixed | -0.0083 | [-0.0583, +0.0416] | 1/0/2 | +0.5474 |
| Cora | iterative_relation_finetune | shuffled_reliability - fixed | -0.0160 | [-0.0446, +0.0126] | 0/0/3 | +0.1382 |
| Cora | iterative_relation_finetune | constant_reliability - fixed | -0.0133 | [-0.0440, +0.0173] | 0/0/3 | +0.2022 |
| Cora | iterative_relation_finetune | combined_shuffled - fixed | -0.0153 | [-0.0613, +0.0306] | 1/0/2 | +0.2877 |
| Cora | iterative_relation_finetune | combined_constant - fixed | -0.0070 | [-0.0363, +0.0223] | 1/0/2 | +0.4119 |
| Cora | iterative_relation_finetune | reliability_only - feature_only | +0.0077 | [-0.0089, +0.0242] | 3/0/0 | +0.1843 |
| Cora | iterative_relation_finetune | true reliability - shuffled reliability | +0.0037 | [-0.0001, +0.0075] | 3/0/0 | +0.0533 |
| Cora | iterative_relation_finetune | true reliability - constant reliability | +0.0010 | [-0.0065, +0.0085] | 2/0/1 | +0.6220 |
| Cora | iterative_relation_finetune | combined - feature_only | +0.0117 | [-0.0158, +0.0391] | 2/1/0 | +0.2092 |
| Cora | iterative_relation_finetune | combined - combined_shuffled | +0.0070 | [-0.0093, +0.0233] | 2/1/0 | +0.2057 |
| Cora | iterative_relation_finetune | combined - combined_constant | -0.0013 | [-0.0220, +0.0194] | 1/0/2 | +0.8075 |
| Pubmed | iterative_relation_frozen | feature_only - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | reliability_only - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | shuffled_reliability - fixed | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | constant_reliability - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined_shuffled - fixed | -0.0027 | [-0.0186, +0.0133] | 1/1/1 | +0.5471 |
| Pubmed | iterative_relation_frozen | combined_constant - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_frozen | true reliability - constant reliability | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - feature_only | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - combined_shuffled | +0.0033 | [-0.0110, +0.0177] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Pubmed | iterative_relation_finetune | feature_only - fixed | +0.0003 | [-0.0035, +0.0041] | 1/1/1 | +0.7418 |
| Pubmed | iterative_relation_finetune | reliability_only - fixed | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | shuffled_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | constant_reliability - fixed | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_shuffled - fixed | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined_constant - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | reliability_only - feature_only | +0.0003 | [-0.0059, +0.0066] | 1/1/1 | +0.8399 |
| Pubmed | iterative_relation_finetune | true reliability - shuffled reliability | +0.0013 | [-0.0044, +0.0071] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | true reliability - constant reliability | +0.0017 | [-0.0055, +0.0088] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - feature_only | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - combined_shuffled | +0.0007 | [-0.0022, +0.0035] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Roman-empire | iterative_relation_protocol | fixed: finetune - frozen | +0.0086 | [-0.0113, +0.0286] | 2/1/0 | +0.2033 |
| Roman-empire | iterative_relation_protocol | feature_only: finetune - frozen | +0.0007 | [-0.0107, +0.0121] | 2/0/1 | +0.8148 |
| Roman-empire | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0084 | [+0.0045, +0.0122] | 3/0/0 | +0.0112 |
| Roman-empire | iterative_relation_protocol | combined: finetune - frozen | +0.0148 | [+0.0118, +0.0179] | 3/0/0 | +0.0023 |
| Roman-empire | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0037 | [-0.0071, +0.0145] | 2/0/1 | +0.2779 |
| Roman-empire | iterative_relation_protocol | constant_reliability: finetune - frozen | -0.0037 | [-0.0166, +0.0092] | 0/0/3 | +0.3424 |
| Roman-empire | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0007 | [-0.0111, +0.0125] | 2/0/1 | +0.8212 |
| Roman-empire | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0012 | [-0.0120, +0.0145] | 2/0/1 | +0.7275 |
| Amazon-ratings | iterative_relation_protocol | fixed: finetune - frozen | +0.0141 | [-0.0169, +0.0451] | 2/1/0 | +0.1893 |
| Amazon-ratings | iterative_relation_protocol | feature_only: finetune - frozen | +0.0132 | [+0.0044, +0.0220] | 3/0/0 | +0.0231 |
| Amazon-ratings | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0192 | [+0.0016, +0.0367] | 3/0/0 | +0.0426 |
| Amazon-ratings | iterative_relation_protocol | combined: finetune - frozen | +0.0072 | [-0.0237, +0.0381] | 1/2/0 | +0.4226 |
| Amazon-ratings | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0056 | [-0.0115, +0.0227] | 2/0/1 | +0.2971 |
| Amazon-ratings | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0115 | [-0.0006, +0.0237] | 3/0/0 | +0.0550 |
| Amazon-ratings | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0097 | [-0.0094, +0.0289] | 3/0/0 | +0.1603 |
| Amazon-ratings | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0118 | [-0.0001, +0.0237] | 3/0/0 | +0.0505 |
| Cora | iterative_relation_protocol | fixed: finetune - frozen | +0.0197 | [-0.0524, +0.0918] | 2/0/1 | +0.3614 |
| Cora | iterative_relation_protocol | feature_only: finetune - frozen | -0.0003 | [-0.0527, +0.0520] | 1/0/2 | +0.9806 |
| Cora | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0073 | [-0.0388, +0.0534] | 2/0/1 | +0.5643 |
| Cora | iterative_relation_protocol | combined: finetune - frozen | +0.0113 | [-0.0140, +0.0367] | 3/0/0 | +0.1946 |
| Cora | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0037 | [-0.0398, +0.0471] | 2/0/1 | +0.7515 |
| Cora | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0063 | [-0.0371, +0.0497] | 2/0/1 | +0.5943 |
| Cora | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0043 | [-0.0359, +0.0446] | 1/0/2 | +0.6886 |
| Cora | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0127 | [-0.0310, +0.0563] | 2/0/1 | +0.3379 |
| Pubmed | iterative_relation_protocol | fixed: finetune - frozen | +0.0020 | [-0.0066, +0.0106] | 1/2/0 | +0.4226 |
| Pubmed | iterative_relation_protocol | feature_only: finetune - frozen | +0.0020 | [-0.0055, +0.0095] | 2/0/1 | +0.3675 |
| Pubmed | iterative_relation_protocol | reliability_only: finetune - frozen | +0.0023 | [-0.0099, +0.0146] | 1/1/1 | +0.4987 |
| Pubmed | iterative_relation_protocol | combined: finetune - frozen | +0.0010 | [-0.0080, +0.0100] | 1/1/1 | +0.6784 |
| Pubmed | iterative_relation_protocol | shuffled_reliability: finetune - frozen | +0.0010 | [-0.0056, +0.0076] | 1/1/1 | +0.5799 |
| Pubmed | iterative_relation_protocol | constant_reliability: finetune - frozen | +0.0013 | [-0.0025, +0.0051] | 2/1/0 | +0.2697 |
| Pubmed | iterative_relation_protocol | combined_shuffled: finetune - frozen | +0.0037 | [-0.0113, +0.0186] | 2/0/1 | +0.4026 |
| Pubmed | iterative_relation_protocol | combined_constant: finetune - frozen | +0.0010 | [-0.0080, +0.0100] | 1/1/1 | +0.6784 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
