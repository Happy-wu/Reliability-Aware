# Representation Control Screening

- Datasets: Roman-empire, Amazon-ratings, Cora, Citeseer, Pubmed
- Families: hidden_mixing_frozen, hidden_mixing_finetune
- Runs: 10
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial adjustment: 0.001
- `hidden_mixing_frozen/fixed` is the untouched selected hidden baseline.
- `hidden_mixing_finetune/fixed` is the same-architecture fixed-mixing fine-tuning control.
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.

## Summary

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Amazon-ratings | hidden_mixing_finetune | combined | 0.4700 | 0.4654 | +0.0046 | 0.0084 | 0.7798 | 0.0403 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant | 0.4709 | 0.4654 | +0.0056 | 0.0085 | 0.7820 | 0.0280 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled | 0.4714 | 0.4654 | +0.0060 | 0.0091 | 0.7815 | 0.0347 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability | 0.4688 | 0.4654 | +0.0034 | 0.0088 | 0.7776 | 0.0123 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | feature_only | 0.4712 | 0.4654 | +0.0058 | 0.0083 | 0.7828 | 0.0352 | 25348 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | fixed | 0.4683 | 0.4654 | +0.0029 | 0.0081 | 0.7750 | 0.0000 | 0 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only | 0.4703 | 0.4654 | +0.0049 | 0.0089 | 0.7769 | 0.0277 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability | 0.4691 | 0.4654 | +0.0037 | 0.0081 | 0.7802 | 0.0245 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability | 0.4697 | 0.4654 | +0.0043 | 0.0071 | 0.7801 | 0.0171 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_frozen | combined | 0.4650 | 0.4654 | -0.0004 | 0.0050 | 0.7709 | 0.0167 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant | 0.4648 | 0.4654 | -0.0006 | 0.0055 | 0.7704 | 0.0123 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled | 0.4650 | 0.4654 | -0.0004 | 0.0056 | 0.7683 | 0.0085 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability | 0.4652 | 0.4654 | -0.0002 | 0.0055 | 0.7725 | 0.0054 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | feature_only | 0.4650 | 0.4654 | -0.0004 | 0.0057 | 0.7683 | 0.0096 | 25348 | 0 |
| Amazon-ratings | hidden_mixing_frozen | fixed | 0.4654 | 0.4654 | +0.0000 | 0.0055 | 0.7750 | 0.0000 | 0 | 0 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only | 0.4650 | 0.4654 | -0.0003 | 0.0056 | 0.7728 | 0.0097 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability | 0.4649 | 0.4654 | -0.0005 | 0.0058 | 0.7735 | 0.0058 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability | 0.4652 | 0.4654 | -0.0002 | 0.0055 | 0.7725 | 0.0053 | 26372 | 0 |
| Citeseer | hidden_mixing_finetune | combined | 0.6119 | 0.6137 | -0.0018 | 0.0198 | 0.7772 | 0.0059 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_constant | 0.6126 | 0.6137 | -0.0011 | 0.0199 | 0.7747 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_shuffled | 0.6119 | 0.6137 | -0.0018 | 0.0198 | 0.7772 | 0.0059 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | constant_reliability | 0.6151 | 0.6137 | +0.0014 | 0.0170 | 0.7748 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | feature_only | 0.6135 | 0.6137 | -0.0002 | 0.0175 | 0.7773 | 0.0059 | 25348 | 312710 |
| Citeseer | hidden_mixing_finetune | fixed | 0.6147 | 0.6137 | +0.0010 | 0.0190 | 0.7750 | 0.0000 | 0 | 312710 |
| Citeseer | hidden_mixing_finetune | reliability_only | 0.6138 | 0.6137 | +0.0001 | 0.0172 | 0.7772 | 0.0059 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability | 0.6145 | 0.6137 | +0.0008 | 0.0167 | 0.7772 | 0.0059 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | zero_reliability | 0.6149 | 0.6137 | +0.0012 | 0.0171 | 0.7748 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_frozen | combined | 0.6141 | 0.6137 | +0.0004 | 0.0206 | 0.7691 | 0.0085 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_constant | 0.6139 | 0.6137 | +0.0002 | 0.0203 | 0.7721 | 0.0047 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_shuffled | 0.6138 | 0.6137 | +0.0001 | 0.0201 | 0.7727 | 0.0060 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | constant_reliability | 0.6136 | 0.6137 | -0.0001 | 0.0204 | 0.7742 | 0.0018 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | feature_only | 0.6138 | 0.6137 | +0.0001 | 0.0202 | 0.7744 | 0.0015 | 25348 | 0 |
| Citeseer | hidden_mixing_frozen | fixed | 0.6137 | 0.6137 | +0.0000 | 0.0199 | 0.7750 | 0.0000 | 0 | 0 |
| Citeseer | hidden_mixing_frozen | reliability_only | 0.6138 | 0.6137 | +0.0001 | 0.0206 | 0.7698 | 0.0077 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability | 0.6137 | 0.6137 | +0.0000 | 0.0205 | 0.7740 | 0.0021 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | zero_reliability | 0.6137 | 0.6137 | +0.0000 | 0.0205 | 0.7741 | 0.0019 | 26372 | 0 |
| Cora | hidden_mixing_finetune | combined | 0.6964 | 0.6860 | +0.0104 | 0.0198 | 0.7996 | 0.0011 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_constant | 0.6918 | 0.6860 | +0.0058 | 0.0144 | 0.7997 | 0.0010 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_shuffled | 0.6923 | 0.6860 | +0.0063 | 0.0145 | 0.7996 | 0.0011 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | constant_reliability | 0.6947 | 0.6860 | +0.0087 | 0.0165 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | feature_only | 0.6920 | 0.6860 | +0.0060 | 0.0145 | 0.7997 | 0.0010 | 25348 | 167495 |
| Cora | hidden_mixing_finetune | fixed | 0.6989 | 0.6860 | +0.0129 | 0.0111 | 0.8000 | 0.0000 | 0 | 167495 |
| Cora | hidden_mixing_finetune | reliability_only | 0.6921 | 0.6860 | +0.0061 | 0.0143 | 0.7997 | 0.0010 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | shuffled_reliability | 0.6927 | 0.6860 | +0.0067 | 0.0145 | 0.7997 | 0.0010 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | zero_reliability | 0.6920 | 0.6860 | +0.0060 | 0.0144 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_frozen | combined | 0.6858 | 0.6860 | -0.0002 | 0.0105 | 0.7987 | 0.0024 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_constant | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_shuffled | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | constant_reliability | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | feature_only | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 25348 | 0 |
| Cora | hidden_mixing_frozen | fixed | 0.6860 | 0.6860 | +0.0000 | 0.0105 | 0.8000 | 0.0000 | 0 | 0 |
| Cora | hidden_mixing_frozen | reliability_only | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7957 | 0.0063 | 26372 | 0 |
| Cora | hidden_mixing_frozen | shuffled_reliability | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | zero_reliability | 0.6859 | 0.6860 | -0.0001 | 0.0105 | 0.7997 | 0.0010 | 26372 | 0 |
| Pubmed | hidden_mixing_finetune | combined | 0.7285 | 0.7289 | -0.0004 | 0.0144 | 0.8663 | 0.0104 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_constant | 0.7285 | 0.7289 | -0.0004 | 0.0144 | 0.8661 | 0.0107 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_shuffled | 0.7283 | 0.7289 | -0.0006 | 0.0145 | 0.8662 | 0.0106 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | constant_reliability | 0.7282 | 0.7289 | -0.0007 | 0.0142 | 0.8682 | 0.0084 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | feature_only | 0.7282 | 0.7289 | -0.0007 | 0.0136 | 0.8729 | 0.0033 | 25348 | 107523 |
| Pubmed | hidden_mixing_finetune | fixed | 0.7312 | 0.7289 | +0.0023 | 0.0142 | 0.8750 | 0.0000 | 0 | 107523 |
| Pubmed | hidden_mixing_finetune | reliability_only | 0.7294 | 0.7289 | +0.0005 | 0.0139 | 0.8685 | 0.0083 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability | 0.7282 | 0.7289 | -0.0007 | 0.0142 | 0.8680 | 0.0088 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | zero_reliability | 0.7282 | 0.7289 | -0.0007 | 0.0144 | 0.8676 | 0.0092 | 26372 | 107523 |
| Pubmed | hidden_mixing_frozen | combined | 0.7288 | 0.7289 | -0.0001 | 0.0146 | 0.8691 | 0.0179 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_constant | 0.7288 | 0.7289 | -0.0001 | 0.0144 | 0.8746 | 0.0118 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_shuffled | 0.7289 | 0.7289 | +0.0000 | 0.0143 | 0.8750 | 0.0120 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | constant_reliability | 0.7286 | 0.7289 | -0.0003 | 0.0145 | 0.8752 | 0.0088 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | feature_only | 0.7288 | 0.7289 | -0.0001 | 0.0144 | 0.8749 | 0.0117 | 25348 | 0 |
| Pubmed | hidden_mixing_frozen | fixed | 0.7289 | 0.7289 | +0.0000 | 0.0143 | 0.8750 | 0.0000 | 0 | 0 |
| Pubmed | hidden_mixing_frozen | reliability_only | 0.7287 | 0.7289 | -0.0002 | 0.0143 | 0.8742 | 0.0136 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability | 0.7285 | 0.7289 | -0.0004 | 0.0142 | 0.8651 | 0.0216 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | zero_reliability | 0.7286 | 0.7289 | -0.0003 | 0.0145 | 0.8754 | 0.0087 | 26372 | 0 |
| Roman-empire | hidden_mixing_finetune | combined | 0.8354 | 0.8189 | +0.0166 | 0.0047 | 0.7426 | 0.0312 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_constant | 0.8242 | 0.8189 | +0.0054 | 0.0060 | 0.7448 | 0.0063 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled | 0.8240 | 0.8189 | +0.0051 | 0.0048 | 0.7447 | 0.0093 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | constant_reliability | 0.8250 | 0.8189 | +0.0061 | 0.0052 | 0.7450 | 0.0061 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | feature_only | 0.8249 | 0.8189 | +0.0060 | 0.0057 | 0.7439 | 0.0073 | 25348 | 95698 |
| Roman-empire | hidden_mixing_finetune | fixed | 0.8231 | 0.8189 | +0.0042 | 0.0076 | 0.7500 | 0.0000 | 0 | 95698 |
| Roman-empire | hidden_mixing_finetune | reliability_only | 0.8335 | 0.8189 | +0.0146 | 0.0040 | 0.7412 | 0.0317 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability | 0.8246 | 0.8189 | +0.0058 | 0.0066 | 0.7485 | 0.0044 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | zero_reliability | 0.8247 | 0.8189 | +0.0059 | 0.0055 | 0.7451 | 0.0061 | 26372 | 95698 |
| Roman-empire | hidden_mixing_frozen | combined | 0.8222 | 0.8189 | +0.0034 | 0.0069 | 0.7577 | 0.0567 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_constant | 0.8196 | 0.8189 | +0.0008 | 0.0068 | 0.7583 | 0.0408 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled | 0.8196 | 0.8189 | +0.0007 | 0.0063 | 0.7572 | 0.0351 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | constant_reliability | 0.8194 | 0.8189 | +0.0005 | 0.0064 | 0.7561 | 0.0216 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | feature_only | 0.8199 | 0.8189 | +0.0010 | 0.0068 | 0.7571 | 0.0317 | 25348 | 0 |
| Roman-empire | hidden_mixing_frozen | fixed | 0.8189 | 0.8189 | +0.0000 | 0.0058 | 0.7500 | 0.0000 | 0 | 0 |
| Roman-empire | hidden_mixing_frozen | reliability_only | 0.8224 | 0.8189 | +0.0036 | 0.0068 | 0.7581 | 0.0429 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability | 0.8192 | 0.8189 | +0.0004 | 0.0064 | 0.7574 | 0.0281 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | zero_reliability | 0.8195 | 0.8189 | +0.0006 | 0.0064 | 0.7556 | 0.0197 | 26372 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Roman-empire | hidden_mixing_frozen | feature_only - fixed | +0.0010 | [-0.0001, +0.0022] | 7/1/2 | +0.0737 |
| Roman-empire | hidden_mixing_frozen | reliability_only - fixed | +0.0036 | [+0.0024, +0.0047] | 10/0/0 | +0.0001 |
| Roman-empire | hidden_mixing_frozen | combined - fixed | +0.0034 | [+0.0016, +0.0051] | 9/1/0 | +0.0022 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0004 | [-0.0006, +0.0013] | 5/1/4 | +0.3901 |
| Roman-empire | hidden_mixing_frozen | constant_reliability - fixed | +0.0005 | [-0.0004, +0.0014] | 7/1/2 | +0.2144 |
| Roman-empire | hidden_mixing_frozen | zero_reliability - fixed | +0.0006 | [-0.0003, +0.0015] | 7/1/2 | +0.1423 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled - fixed | +0.0007 | [-0.0007, +0.0020] | 5/2/3 | +0.2784 |
| Roman-empire | hidden_mixing_frozen | combined_constant - fixed | +0.0008 | [-0.0006, +0.0021] | 5/1/4 | +0.2356 |
| Roman-empire | hidden_mixing_frozen | reliability_only - feature_only | +0.0025 | [+0.0012, +0.0039] | 10/0/0 | +0.0018 |
| Roman-empire | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0032 | [+0.0022, +0.0042] | 10/0/0 | +0.0000 |
| Roman-empire | hidden_mixing_frozen | true reliability - constant reliability | +0.0031 | [+0.0020, +0.0041] | 10/0/0 | +0.0001 |
| Roman-empire | hidden_mixing_frozen | true reliability - zero reliability | +0.0030 | [+0.0019, +0.0041] | 10/0/0 | +0.0002 |
| Roman-empire | hidden_mixing_frozen | combined - feature_only | +0.0023 | [+0.0004, +0.0043] | 7/0/3 | +0.0254 |
| Roman-empire | hidden_mixing_frozen | combined - combined_shuffled | +0.0027 | [+0.0010, +0.0043] | 10/0/0 | +0.0057 |
| Roman-empire | hidden_mixing_frozen | combined - combined_constant | +0.0026 | [+0.0008, +0.0044] | 9/0/1 | +0.0092 |
| Roman-empire | hidden_mixing_finetune | feature_only - fixed | +0.0018 | [-0.0009, +0.0044] | 5/2/3 | +0.1642 |
| Roman-empire | hidden_mixing_finetune | reliability_only - fixed | +0.0104 | [+0.0054, +0.0154] | 10/0/0 | +0.0012 |
| Roman-empire | hidden_mixing_finetune | combined - fixed | +0.0123 | [+0.0075, +0.0172] | 10/0/0 | +0.0003 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0015 | [-0.0005, +0.0035] | 6/2/2 | +0.1166 |
| Roman-empire | hidden_mixing_finetune | constant_reliability - fixed | +0.0019 | [-0.0017, +0.0055] | 5/1/4 | +0.2677 |
| Roman-empire | hidden_mixing_finetune | zero_reliability - fixed | +0.0016 | [-0.0006, +0.0038] | 6/1/3 | +0.1314 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled - fixed | +0.0009 | [-0.0020, +0.0038] | 5/1/4 | +0.5155 |
| Roman-empire | hidden_mixing_finetune | combined_constant - fixed | +0.0011 | [-0.0012, +0.0035] | 4/1/5 | +0.3031 |
| Roman-empire | hidden_mixing_finetune | reliability_only - feature_only | +0.0086 | [+0.0053, +0.0119] | 10/0/0 | +0.0002 |
| Roman-empire | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0088 | [+0.0050, +0.0126] | 10/0/0 | +0.0005 |
| Roman-empire | hidden_mixing_finetune | true reliability - constant reliability | +0.0085 | [+0.0053, +0.0117] | 10/0/0 | +0.0002 |
| Roman-empire | hidden_mixing_finetune | true reliability - zero reliability | +0.0088 | [+0.0050, +0.0125] | 10/0/0 | +0.0005 |
| Roman-empire | hidden_mixing_finetune | combined - feature_only | +0.0106 | [+0.0074, +0.0137] | 10/0/0 | +0.0000 |
| Roman-empire | hidden_mixing_finetune | combined - combined_shuffled | +0.0115 | [+0.0088, +0.0141] | 10/0/0 | +0.0000 |
| Roman-empire | hidden_mixing_finetune | combined - combined_constant | +0.0112 | [+0.0073, +0.0151] | 10/0/0 | +0.0001 |
| Amazon-ratings | hidden_mixing_frozen | feature_only - fixed | -0.0004 | [-0.0016, +0.0007] | 4/4/2 | +0.4278 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - fixed | -0.0003 | [-0.0010, +0.0003] | 3/2/5 | +0.2743 |
| Amazon-ratings | hidden_mixing_frozen | combined - fixed | -0.0004 | [-0.0012, +0.0004] | 3/2/5 | +0.3381 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0005 | [-0.0012, +0.0003] | 3/3/4 | +0.2218 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability - fixed | -0.0002 | [-0.0009, +0.0006] | 4/2/4 | +0.6039 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability - fixed | -0.0002 | [-0.0009, +0.0006] | 4/2/4 | +0.6424 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled - fixed | -0.0004 | [-0.0009, +0.0002] | 2/2/6 | +0.1659 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant - fixed | -0.0006 | [-0.0017, +0.0005] | 3/3/4 | +0.2280 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - feature_only | +0.0001 | [-0.0005, +0.0007] | 2/4/4 | +0.7545 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0001 | [-0.0004, +0.0006] | 2/5/3 | +0.6249 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - constant reliability | -0.0002 | [-0.0007, +0.0003] | 2/5/3 | +0.4697 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - zero reliability | -0.0002 | [-0.0007, +0.0003] | 2/5/3 | +0.4292 |
| Amazon-ratings | hidden_mixing_frozen | combined - feature_only | +0.0001 | [-0.0008, +0.0009] | 3/3/4 | +0.8617 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_shuffled | -0.0000 | [-0.0009, +0.0009] | 4/4/2 | +1.0000 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_constant | +0.0002 | [-0.0005, +0.0010] | 4/4/2 | +0.4616 |
| Amazon-ratings | hidden_mixing_finetune | feature_only - fixed | +0.0029 | [-0.0019, +0.0077] | 5/2/3 | +0.2066 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - fixed | +0.0020 | [-0.0019, +0.0059] | 6/3/1 | +0.2736 |
| Amazon-ratings | hidden_mixing_finetune | combined - fixed | +0.0017 | [-0.0009, +0.0043] | 6/2/2 | +0.1644 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0008 | [-0.0008, +0.0023] | 6/3/1 | +0.2840 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability - fixed | +0.0005 | [-0.0022, +0.0032] | 5/3/2 | +0.6910 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability - fixed | +0.0014 | [-0.0044, +0.0072] | 5/2/3 | +0.5989 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled - fixed | +0.0031 | [-0.0001, +0.0063] | 7/3/0 | +0.0546 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant - fixed | +0.0027 | [+0.0001, +0.0053] | 6/2/2 | +0.0457 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - feature_only | -0.0009 | [-0.0052, +0.0034] | 3/5/2 | +0.6432 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0012 | [-0.0033, +0.0057] | 2/5/3 | +0.5554 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - constant reliability | +0.0015 | [-0.0025, +0.0055] | 3/5/2 | +0.4187 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - zero reliability | +0.0006 | [-0.0054, +0.0065] | 3/4/3 | +0.8282 |
| Amazon-ratings | hidden_mixing_finetune | combined - feature_only | -0.0012 | [-0.0052, +0.0028] | 3/4/3 | +0.5249 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_shuffled | -0.0014 | [-0.0038, +0.0010] | 2/4/4 | +0.2206 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_constant | -0.0009 | [-0.0034, +0.0015] | 1/4/5 | +0.4111 |
| Cora | hidden_mixing_frozen | feature_only - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | reliability_only - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | combined - fixed | -0.0002 | [-0.0005, +0.0001] | 0/8/2 | +0.1679 |
| Cora | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | constant_reliability - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | zero_reliability - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | combined_shuffled - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | combined_constant - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Cora | hidden_mixing_frozen | combined - feature_only | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | combined - combined_shuffled | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_frozen | combined - combined_constant | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_finetune | feature_only - fixed | -0.0069 | [-0.0190, +0.0052] | 2/2/6 | +0.2299 |
| Cora | hidden_mixing_finetune | reliability_only - fixed | -0.0068 | [-0.0186, +0.0050] | 2/2/6 | +0.2248 |
| Cora | hidden_mixing_finetune | combined - fixed | -0.0025 | [-0.0200, +0.0150] | 2/2/6 | +0.7544 |
| Cora | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0062 | [-0.0185, +0.0061] | 2/2/6 | +0.2845 |
| Cora | hidden_mixing_finetune | constant_reliability - fixed | -0.0042 | [-0.0188, +0.0104] | 2/2/6 | +0.5315 |
| Cora | hidden_mixing_finetune | zero_reliability - fixed | -0.0069 | [-0.0188, +0.0050] | 2/2/6 | +0.2228 |
| Cora | hidden_mixing_finetune | combined_shuffled - fixed | -0.0066 | [-0.0186, +0.0054] | 2/2/6 | +0.2448 |
| Cora | hidden_mixing_finetune | combined_constant - fixed | -0.0071 | [-0.0186, +0.0044] | 2/2/6 | +0.1954 |
| Cora | hidden_mixing_finetune | reliability_only - feature_only | +0.0001 | [-0.0004, +0.0006] | 1/8/1 | +0.6783 |
| Cora | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0006 | [-0.0020, +0.0008] | 0/9/1 | +0.3434 |
| Cora | hidden_mixing_finetune | true reliability - constant reliability | -0.0026 | [-0.0082, +0.0030] | 0/8/2 | +0.3238 |
| Cora | hidden_mixing_finetune | true reliability - zero reliability | +0.0001 | [-0.0001, +0.0003] | 1/9/0 | +0.3434 |
| Cora | hidden_mixing_finetune | combined - feature_only | +0.0044 | [-0.0048, +0.0136] | 3/7/0 | +0.3080 |
| Cora | hidden_mixing_finetune | combined - combined_shuffled | +0.0041 | [-0.0052, +0.0134] | 1/9/0 | +0.3434 |
| Cora | hidden_mixing_finetune | combined - combined_constant | +0.0046 | [-0.0061, +0.0153] | 1/8/1 | +0.3545 |
| Citeseer | hidden_mixing_frozen | feature_only - fixed | +0.0001 | [-0.0004, +0.0006] | 1/8/1 | +0.6783 |
| Citeseer | hidden_mixing_frozen | reliability_only - fixed | +0.0001 | [-0.0008, +0.0010] | 2/6/2 | +0.7976 |
| Citeseer | hidden_mixing_frozen | combined - fixed | +0.0004 | [-0.0004, +0.0012] | 2/7/1 | +0.3092 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [-0.0008, +0.0008] | 2/6/2 | +1.0000 |
| Citeseer | hidden_mixing_frozen | constant_reliability - fixed | -0.0001 | [-0.0008, +0.0006] | 1/7/2 | +0.7577 |
| Citeseer | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [-0.0008, +0.0008] | 2/6/2 | +1.0000 |
| Citeseer | hidden_mixing_frozen | combined_shuffled - fixed | +0.0001 | [-0.0005, +0.0007] | 2/6/2 | +0.7263 |
| Citeseer | hidden_mixing_frozen | combined_constant - fixed | +0.0002 | [-0.0004, +0.0008] | 2/7/1 | +0.4433 |
| Citeseer | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [-0.0007, +0.0007] | 1/8/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0001 | [-0.0001, +0.0003] | 1/9/0 | +0.3434 |
| Citeseer | hidden_mixing_frozen | true reliability - constant reliability | +0.0002 | [-0.0003, +0.0007] | 1/9/0 | +0.3434 |
| Citeseer | hidden_mixing_frozen | true reliability - zero reliability | +0.0001 | [-0.0001, +0.0003] | 1/9/0 | +0.3434 |
| Citeseer | hidden_mixing_frozen | combined - feature_only | +0.0003 | [-0.0004, +0.0010] | 1/9/0 | +0.3434 |
| Citeseer | hidden_mixing_frozen | combined - combined_shuffled | +0.0003 | [-0.0005, +0.0011] | 2/7/1 | +0.3938 |
| Citeseer | hidden_mixing_frozen | combined - combined_constant | +0.0002 | [-0.0003, +0.0007] | 1/9/0 | +0.3434 |
| Citeseer | hidden_mixing_finetune | feature_only - fixed | -0.0012 | [-0.0087, +0.0063] | 3/4/3 | +0.7261 |
| Citeseer | hidden_mixing_finetune | reliability_only - fixed | -0.0009 | [-0.0091, +0.0073] | 3/4/3 | +0.8090 |
| Citeseer | hidden_mixing_finetune | combined - fixed | -0.0028 | [-0.0090, +0.0034] | 2/5/3 | +0.3321 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0002 | [-0.0092, +0.0088] | 3/4/3 | +0.9610 |
| Citeseer | hidden_mixing_finetune | constant_reliability - fixed | +0.0004 | [-0.0075, +0.0083] | 3/4/3 | +0.9112 |
| Citeseer | hidden_mixing_finetune | zero_reliability - fixed | +0.0002 | [-0.0074, +0.0078] | 3/4/3 | +0.9536 |
| Citeseer | hidden_mixing_finetune | combined_shuffled - fixed | -0.0028 | [-0.0090, +0.0034] | 2/5/3 | +0.3321 |
| Citeseer | hidden_mixing_finetune | combined_constant - fixed | -0.0021 | [-0.0079, +0.0037] | 2/5/3 | +0.4321 |
| Citeseer | hidden_mixing_finetune | reliability_only - feature_only | +0.0003 | [-0.0007, +0.0013] | 1/8/1 | +0.4961 |
| Citeseer | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0007 | [-0.0021, +0.0007] | 0/8/2 | +0.2712 |
| Citeseer | hidden_mixing_finetune | true reliability - constant reliability | -0.0013 | [-0.0030, +0.0004] | 0/7/3 | +0.1154 |
| Citeseer | hidden_mixing_finetune | true reliability - zero reliability | -0.0011 | [-0.0027, +0.0005] | 0/7/3 | +0.1619 |
| Citeseer | hidden_mixing_finetune | combined - feature_only | -0.0016 | [-0.0052, +0.0020] | 0/9/1 | +0.3434 |
| Citeseer | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Citeseer | hidden_mixing_finetune | combined - combined_constant | -0.0007 | [-0.0023, +0.0009] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | feature_only - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | reliability_only - fixed | -0.0002 | [-0.0005, +0.0001] | 0/8/2 | +0.1679 |
| Pubmed | hidden_mixing_frozen | combined - fixed | -0.0001 | [-0.0005, +0.0003] | 1/7/2 | +0.5911 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0004 | [-0.0012, +0.0004] | 1/6/3 | +0.2695 |
| Pubmed | hidden_mixing_frozen | constant_reliability - fixed | -0.0003 | [-0.0010, +0.0004] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | zero_reliability - fixed | -0.0003 | [-0.0010, +0.0004] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_constant - fixed | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | reliability_only - feature_only | -0.0001 | [-0.0003, +0.0001] | 0/9/1 | +0.3434 |
| Pubmed | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0002 | [-0.0004, +0.0008] | 2/7/1 | +0.4433 |
| Pubmed | hidden_mixing_frozen | true reliability - constant reliability | +0.0001 | [-0.0004, +0.0006] | 1/8/1 | +0.6783 |
| Pubmed | hidden_mixing_frozen | true reliability - zero reliability | +0.0001 | [-0.0004, +0.0006] | 1/8/1 | +0.6783 |
| Pubmed | hidden_mixing_frozen | combined - feature_only | +0.0000 | [-0.0003, +0.0003] | 1/8/1 | +1.0000 |
| Pubmed | hidden_mixing_frozen | combined - combined_shuffled | -0.0001 | [-0.0005, +0.0003] | 1/7/2 | +0.5911 |
| Pubmed | hidden_mixing_frozen | combined - combined_constant | +0.0000 | [-0.0003, +0.0003] | 1/8/1 | +1.0000 |
| Pubmed | hidden_mixing_finetune | feature_only - fixed | -0.0030 | [-0.0085, +0.0025] | 2/4/4 | +0.2460 |
| Pubmed | hidden_mixing_finetune | reliability_only - fixed | -0.0018 | [-0.0077, +0.0041] | 3/4/3 | +0.5100 |
| Pubmed | hidden_mixing_finetune | combined - fixed | -0.0027 | [-0.0091, +0.0037] | 2/4/4 | +0.3628 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0030 | [-0.0091, +0.0031] | 2/4/4 | +0.2974 |
| Pubmed | hidden_mixing_finetune | constant_reliability - fixed | -0.0030 | [-0.0091, +0.0031] | 2/4/4 | +0.2974 |
| Pubmed | hidden_mixing_finetune | zero_reliability - fixed | -0.0030 | [-0.0093, +0.0033] | 2/4/4 | +0.3120 |
| Pubmed | hidden_mixing_finetune | combined_shuffled - fixed | -0.0029 | [-0.0094, +0.0036] | 2/4/4 | +0.3379 |
| Pubmed | hidden_mixing_finetune | combined_constant - fixed | -0.0027 | [-0.0091, +0.0037] | 2/4/4 | +0.3628 |
| Pubmed | hidden_mixing_finetune | reliability_only - feature_only | +0.0012 | [-0.0011, +0.0035] | 2/8/0 | +0.2598 |
| Pubmed | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0012 | [-0.0020, +0.0044] | 1/8/1 | +0.4250 |
| Pubmed | hidden_mixing_finetune | true reliability - constant reliability | +0.0012 | [-0.0020, +0.0044] | 1/8/1 | +0.4250 |
| Pubmed | hidden_mixing_finetune | true reliability - zero reliability | +0.0012 | [-0.0023, +0.0047] | 1/8/1 | +0.4620 |
| Pubmed | hidden_mixing_finetune | combined - feature_only | +0.0003 | [-0.0013, +0.0019] | 1/8/1 | +0.6783 |
| Pubmed | hidden_mixing_finetune | combined - combined_shuffled | +0.0002 | [-0.0003, +0.0007] | 1/9/0 | +0.3434 |
| Pubmed | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/10/0 | n/a |
| Roman-empire | hidden_protocol | fixed: finetune - frozen | +0.0042 | [+0.0010, +0.0075] | 7/2/1 | +0.0167 |
| Roman-empire | hidden_protocol | feature_only: finetune - frozen | +0.0050 | [+0.0027, +0.0072] | 10/0/0 | +0.0008 |
| Roman-empire | hidden_protocol | reliability_only: finetune - frozen | +0.0110 | [+0.0062, +0.0158] | 10/0/0 | +0.0006 |
| Roman-empire | hidden_protocol | combined: finetune - frozen | +0.0132 | [+0.0088, +0.0176] | 10/0/0 | +0.0001 |
| Roman-empire | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0054 | [+0.0022, +0.0086] | 8/1/1 | +0.0041 |
| Roman-empire | hidden_protocol | constant_reliability: finetune - frozen | +0.0056 | [+0.0026, +0.0086] | 9/0/1 | +0.0025 |
| Roman-empire | hidden_protocol | zero_reliability: finetune - frozen | +0.0052 | [+0.0025, +0.0080] | 8/1/1 | +0.0020 |
| Roman-empire | hidden_protocol | combined_shuffled: finetune - frozen | +0.0044 | [+0.0017, +0.0072] | 9/0/1 | +0.0056 |
| Roman-empire | hidden_protocol | combined_constant: finetune - frozen | +0.0046 | [+0.0022, +0.0070] | 9/0/1 | +0.0020 |
| Amazon-ratings | hidden_protocol | fixed: finetune - frozen | +0.0029 | [-0.0005, +0.0063] | 3/7/0 | +0.0896 |
| Amazon-ratings | hidden_protocol | feature_only: finetune - frozen | +0.0062 | [+0.0018, +0.0106] | 7/2/1 | +0.0115 |
| Amazon-ratings | hidden_protocol | reliability_only: finetune - frozen | +0.0052 | [+0.0008, +0.0096] | 7/3/0 | +0.0259 |
| Amazon-ratings | hidden_protocol | combined: finetune - frozen | +0.0050 | [+0.0011, +0.0089] | 8/1/1 | +0.0182 |
| Amazon-ratings | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0041 | [-0.0001, +0.0084] | 6/4/0 | +0.0566 |
| Amazon-ratings | hidden_protocol | constant_reliability: finetune - frozen | +0.0035 | [-0.0000, +0.0071] | 5/4/1 | +0.0511 |
| Amazon-ratings | hidden_protocol | zero_reliability: finetune - frozen | +0.0044 | [-0.0002, +0.0091] | 6/2/2 | +0.0580 |
| Amazon-ratings | hidden_protocol | combined_shuffled: finetune - frozen | +0.0064 | [+0.0015, +0.0112] | 8/2/0 | +0.0153 |
| Amazon-ratings | hidden_protocol | combined_constant: finetune - frozen | +0.0062 | [+0.0018, +0.0105] | 8/1/1 | +0.0108 |
| Cora | hidden_protocol | fixed: finetune - frozen | +0.0129 | [+0.0024, +0.0234] | 7/3/0 | +0.0216 |
| Cora | hidden_protocol | feature_only: finetune - frozen | +0.0061 | [-0.0029, +0.0151] | 3/7/0 | +0.1594 |
| Cora | hidden_protocol | reliability_only: finetune - frozen | +0.0062 | [-0.0028, +0.0152] | 3/7/0 | +0.1522 |
| Cora | hidden_protocol | combined: finetune - frozen | +0.0106 | [-0.0040, +0.0252] | 3/7/0 | +0.1361 |
| Cora | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0068 | [-0.0026, +0.0162] | 3/7/0 | +0.1346 |
| Cora | hidden_protocol | constant_reliability: finetune - frozen | +0.0088 | [-0.0028, +0.0204] | 3/7/0 | +0.1203 |
| Cora | hidden_protocol | zero_reliability: finetune - frozen | +0.0061 | [-0.0029, +0.0151] | 3/7/0 | +0.1575 |
| Cora | hidden_protocol | combined_shuffled: finetune - frozen | +0.0064 | [-0.0028, +0.0156] | 3/7/0 | +0.1510 |
| Cora | hidden_protocol | combined_constant: finetune - frozen | +0.0059 | [-0.0031, +0.0149] | 3/7/0 | +0.1734 |
| Citeseer | hidden_protocol | fixed: finetune - frozen | +0.0010 | [-0.0036, +0.0056] | 2/7/1 | +0.6373 |
| Citeseer | hidden_protocol | feature_only: finetune - frozen | -0.0003 | [-0.0054, +0.0048] | 2/5/3 | +0.8962 |
| Citeseer | hidden_protocol | reliability_only: finetune - frozen | +0.0000 | [-0.0059, +0.0059] | 3/4/3 | +1.0000 |
| Citeseer | hidden_protocol | combined: finetune - frozen | -0.0022 | [-0.0052, +0.0008] | 1/5/4 | +0.1286 |
| Citeseer | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0008 | [-0.0062, +0.0078] | 3/4/3 | +0.8022 |
| Citeseer | hidden_protocol | constant_reliability: finetune - frozen | +0.0015 | [-0.0041, +0.0071] | 3/5/2 | +0.5619 |
| Citeseer | hidden_protocol | zero_reliability: finetune - frozen | +0.0012 | [-0.0040, +0.0064] | 3/4/3 | +0.6157 |
| Citeseer | hidden_protocol | combined_shuffled: finetune - frozen | -0.0019 | [-0.0047, +0.0009] | 1/5/4 | +0.1578 |
| Citeseer | hidden_protocol | combined_constant: finetune - frozen | -0.0013 | [-0.0031, +0.0005] | 1/5/4 | +0.1461 |
| Pubmed | hidden_protocol | fixed: finetune - frozen | +0.0023 | [-0.0010, +0.0056] | 4/5/1 | +0.1480 |
| Pubmed | hidden_protocol | feature_only: finetune - frozen | -0.0006 | [-0.0045, +0.0033] | 2/6/2 | +0.7353 |
| Pubmed | hidden_protocol | reliability_only: finetune - frozen | +0.0007 | [-0.0035, +0.0049] | 4/5/1 | +0.7148 |
| Pubmed | hidden_protocol | combined: finetune - frozen | -0.0003 | [-0.0054, +0.0048] | 3/4/3 | +0.8980 |
| Pubmed | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0003 | [-0.0053, +0.0047] | 4/3/3 | +0.8941 |
| Pubmed | hidden_protocol | constant_reliability: finetune - frozen | -0.0004 | [-0.0053, +0.0045] | 2/6/2 | +0.8586 |
| Pubmed | hidden_protocol | zero_reliability: finetune - frozen | -0.0004 | [-0.0056, +0.0048] | 2/6/2 | +0.8658 |
| Pubmed | hidden_protocol | combined_shuffled: finetune - frozen | -0.0006 | [-0.0059, +0.0047] | 1/7/2 | +0.8041 |
| Pubmed | hidden_protocol | combined_constant: finetune - frozen | -0.0003 | [-0.0054, +0.0048] | 2/6/2 | +0.8978 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
