# Representation Control Screening

- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor, Roman-empire, Amazon-ratings
- Families: hidden_mixing_frozen, hidden_mixing_finetune
- Runs: 5
- Edge protocol: undirected
- Max adjustment: 0.05
- Initial adjustment: 0.001
- `hidden_mixing_frozen/fixed` is the untouched selected hidden baseline.
- `hidden_mixing_finetune/fixed` is the same-architecture fixed-mixing fine-tuning control.
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.

## Summary

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Actor | hidden_mixing_finetune | combined | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 34948 | 135301 |
| Actor | hidden_mixing_finetune | combined_constant | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 34948 | 135301 |
| Actor | hidden_mixing_finetune | combined_shuffled | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 34948 | 135301 |
| Actor | hidden_mixing_finetune | constant_reliability | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 26372 | 135301 |
| Actor | hidden_mixing_finetune | feature_only | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 25348 | 135301 |
| Actor | hidden_mixing_finetune | fixed | 0.3647 | 0.3647 | +0.0000 | 0.0074 | 0.8500 | 0.0000 | 0 | 135301 |
| Actor | hidden_mixing_finetune | reliability_only | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 26372 | 135301 |
| Actor | hidden_mixing_finetune | shuffled_reliability | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 26372 | 135301 |
| Actor | hidden_mixing_finetune | zero_reliability | 0.3645 | 0.3647 | -0.0003 | 0.0069 | 0.8497 | 0.0010 | 26372 | 135301 |
| Actor | hidden_mixing_frozen | combined | 0.3637 | 0.3647 | -0.0011 | 0.0065 | 0.8443 | 0.0067 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_constant | 0.3649 | 0.3647 | +0.0001 | 0.0078 | 0.8463 | 0.0046 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_shuffled | 0.3633 | 0.3647 | -0.0014 | 0.0076 | 0.8388 | 0.0124 | 34948 | 0 |
| Actor | hidden_mixing_frozen | constant_reliability | 0.3650 | 0.3647 | +0.0003 | 0.0076 | 0.8434 | 0.0074 | 26372 | 0 |
| Actor | hidden_mixing_frozen | feature_only | 0.3624 | 0.3647 | -0.0024 | 0.0067 | 0.8384 | 0.0123 | 25348 | 0 |
| Actor | hidden_mixing_frozen | fixed | 0.3647 | 0.3647 | +0.0000 | 0.0074 | 0.8500 | 0.0000 | 0 | 0 |
| Actor | hidden_mixing_frozen | reliability_only | 0.3647 | 0.3647 | -0.0000 | 0.0071 | 0.8419 | 0.0094 | 26372 | 0 |
| Actor | hidden_mixing_frozen | shuffled_reliability | 0.3642 | 0.3647 | -0.0005 | 0.0078 | 0.8373 | 0.0142 | 26372 | 0 |
| Actor | hidden_mixing_frozen | zero_reliability | 0.3650 | 0.3647 | +0.0003 | 0.0076 | 0.8434 | 0.0074 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_finetune | combined | 0.4736 | 0.4672 | +0.0064 | 0.0089 | 0.7487 | 0.0198 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant | 0.4717 | 0.4672 | +0.0045 | 0.0082 | 0.7532 | 0.0165 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled | 0.4758 | 0.4672 | +0.0086 | 0.0082 | 0.7571 | 0.0348 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability | 0.4765 | 0.4672 | +0.0093 | 0.0100 | 0.7561 | 0.0205 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | feature_only | 0.4728 | 0.4672 | +0.0057 | 0.0100 | 0.7520 | 0.0248 | 25348 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | fixed | 0.4747 | 0.4672 | +0.0075 | 0.0095 | 0.7500 | 0.0000 | 0 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only | 0.4718 | 0.4672 | +0.0046 | 0.0084 | 0.7486 | 0.0158 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability | 0.4754 | 0.4672 | +0.0082 | 0.0081 | 0.7552 | 0.0244 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability | 0.4733 | 0.4672 | +0.0061 | 0.0083 | 0.7536 | 0.0157 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_frozen | combined | 0.4667 | 0.4672 | -0.0005 | 0.0043 | 0.7463 | 0.0054 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant | 0.4669 | 0.4672 | -0.0003 | 0.0038 | 0.7471 | 0.0045 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled | 0.4670 | 0.4672 | -0.0002 | 0.0039 | 0.7462 | 0.0057 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability | 0.4671 | 0.4672 | -0.0001 | 0.0039 | 0.7452 | 0.0069 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | feature_only | 0.4670 | 0.4672 | -0.0002 | 0.0039 | 0.7470 | 0.0047 | 25348 | 0 |
| Amazon-ratings | hidden_mixing_frozen | fixed | 0.4672 | 0.4672 | +0.0000 | 0.0040 | 0.7500 | 0.0000 | 0 | 0 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only | 0.4668 | 0.4672 | -0.0004 | 0.0045 | 0.7464 | 0.0051 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability | 0.4668 | 0.4672 | -0.0004 | 0.0040 | 0.7467 | 0.0051 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability | 0.4671 | 0.4672 | -0.0001 | 0.0039 | 0.7453 | 0.0069 | 26372 | 0 |
| Chameleon | hidden_mixing_finetune | combined | 0.5430 | 0.5434 | -0.0004 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_constant | 0.5425 | 0.5434 | -0.0009 | 0.0296 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_shuffled | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | constant_reliability | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | feature_only | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 25348 | 224453 |
| Chameleon | hidden_mixing_finetune | fixed | 0.5439 | 0.5434 | +0.0004 | 0.0314 | 0.8000 | 0.0000 | 0 | 224453 |
| Chameleon | hidden_mixing_finetune | reliability_only | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | zero_reliability | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_frozen | combined | 0.5439 | 0.5434 | +0.0004 | 0.0310 | 0.8002 | 0.0160 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_constant | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7972 | 0.0057 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_shuffled | 0.5399 | 0.5434 | -0.0035 | 0.0338 | 0.7974 | 0.0121 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | constant_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7972 | 0.0058 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | feature_only | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7973 | 0.0104 | 25348 | 0 |
| Chameleon | hidden_mixing_frozen | fixed | 0.5434 | 0.5434 | +0.0000 | 0.0316 | 0.8000 | 0.0000 | 0 | 0 |
| Chameleon | hidden_mixing_frozen | reliability_only | 0.5430 | 0.5434 | -0.0004 | 0.0315 | 0.8002 | 0.0182 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability | 0.5421 | 0.5434 | -0.0013 | 0.0330 | 0.7983 | 0.0079 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | zero_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7972 | 0.0057 | 26372 | 0 |
| Citeseer | hidden_mixing_finetune | combined | 0.6132 | 0.6144 | -0.0012 | 0.0229 | 0.7498 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_constant | 0.6132 | 0.6144 | -0.0012 | 0.0229 | 0.7498 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_shuffled | 0.6132 | 0.6144 | -0.0012 | 0.0229 | 0.7498 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | constant_reliability | 0.6178 | 0.6144 | +0.0034 | 0.0171 | 0.7498 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | feature_only | 0.6164 | 0.6144 | +0.0020 | 0.0186 | 0.7498 | 0.0010 | 25348 | 312710 |
| Citeseer | hidden_mixing_finetune | fixed | 0.6168 | 0.6144 | +0.0024 | 0.0217 | 0.7500 | 0.0000 | 0 | 312710 |
| Citeseer | hidden_mixing_finetune | reliability_only | 0.6172 | 0.6144 | +0.0028 | 0.0177 | 0.7498 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability | 0.6184 | 0.6144 | +0.0040 | 0.0166 | 0.7498 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | zero_reliability | 0.6176 | 0.6144 | +0.0032 | 0.0173 | 0.7498 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_frozen | combined | 0.6142 | 0.6144 | -0.0002 | 0.0229 | 0.7433 | 0.0096 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_constant | 0.6146 | 0.6144 | +0.0002 | 0.0234 | 0.7492 | 0.0018 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_shuffled | 0.6146 | 0.6144 | +0.0002 | 0.0234 | 0.7433 | 0.0097 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | constant_reliability | 0.6144 | 0.6144 | +0.0000 | 0.0238 | 0.7502 | 0.0046 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | feature_only | 0.6148 | 0.6144 | +0.0004 | 0.0235 | 0.7505 | 0.0041 | 25348 | 0 |
| Citeseer | hidden_mixing_frozen | fixed | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7500 | 0.0000 | 0 | 0 |
| Citeseer | hidden_mixing_frozen | reliability_only | 0.6136 | 0.6144 | -0.0008 | 0.0230 | 0.7444 | 0.0082 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability | 0.6140 | 0.6144 | -0.0004 | 0.0236 | 0.7504 | 0.0046 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | zero_reliability | 0.6142 | 0.6144 | -0.0002 | 0.0236 | 0.7502 | 0.0047 | 26372 | 0 |
| Cora | hidden_mixing_finetune | combined | 0.7026 | 0.6872 | +0.0154 | 0.0151 | 0.7996 | 0.0011 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_constant | 0.6996 | 0.6872 | +0.0124 | 0.0148 | 0.7997 | 0.0010 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_shuffled | 0.7024 | 0.6872 | +0.0152 | 0.0162 | 0.7994 | 0.0013 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | constant_reliability | 0.7010 | 0.6872 | +0.0138 | 0.0141 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | feature_only | 0.6994 | 0.6872 | +0.0122 | 0.0151 | 0.7997 | 0.0010 | 25348 | 167495 |
| Cora | hidden_mixing_finetune | fixed | 0.7050 | 0.6872 | +0.0178 | 0.0099 | 0.8000 | 0.0000 | 0 | 167495 |
| Cora | hidden_mixing_finetune | reliability_only | 0.7008 | 0.6872 | +0.0136 | 0.0144 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | shuffled_reliability | 0.7010 | 0.6872 | +0.0138 | 0.0147 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | zero_reliability | 0.6994 | 0.6872 | +0.0122 | 0.0148 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_frozen | combined | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7955 | 0.0066 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_constant | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_shuffled | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | constant_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | feature_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 25348 | 0 |
| Cora | hidden_mixing_frozen | fixed | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.8000 | 0.0000 | 0 | 0 |
| Cora | hidden_mixing_frozen | reliability_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7954 | 0.0067 | 26372 | 0 |
| Cora | hidden_mixing_frozen | shuffled_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | zero_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Pubmed | hidden_mixing_finetune | combined | 0.7304 | 0.7344 | -0.0040 | 0.0106 | 0.8459 | 0.0058 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_constant | 0.7284 | 0.7344 | -0.0060 | 0.0127 | 0.8459 | 0.0058 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_shuffled | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8460 | 0.0058 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | constant_reliability | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8461 | 0.0056 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | feature_only | 0.7312 | 0.7344 | -0.0032 | 0.0100 | 0.8475 | 0.0038 | 25348 | 107523 |
| Pubmed | hidden_mixing_finetune | fixed | 0.7356 | 0.7344 | +0.0012 | 0.0138 | 0.8500 | 0.0000 | 0 | 107523 |
| Pubmed | hidden_mixing_finetune | reliability_only | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8460 | 0.0057 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8459 | 0.0058 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | zero_reliability | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8460 | 0.0058 | 26372 | 107523 |
| Pubmed | hidden_mixing_frozen | combined | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8494 | 0.0013 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_constant | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8491 | 0.0017 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_shuffled | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8491 | 0.0016 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | constant_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8480 | 0.0032 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | feature_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8493 | 0.0015 | 25348 | 0 |
| Pubmed | hidden_mixing_frozen | fixed | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8500 | 0.0000 | 0 | 0 |
| Pubmed | hidden_mixing_frozen | reliability_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8488 | 0.0020 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability | 0.7348 | 0.7344 | +0.0004 | 0.0124 | 0.8421 | 0.0092 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | zero_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8477 | 0.0035 | 26372 | 0 |
| Roman-empire | hidden_mixing_finetune | combined | 0.8304 | 0.8199 | +0.0104 | 0.0028 | 0.7462 | 0.0220 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_constant | 0.8255 | 0.8199 | +0.0055 | 0.0050 | 0.7498 | 0.0029 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled | 0.8232 | 0.8199 | +0.0033 | 0.0043 | 0.7500 | 0.0059 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | constant_reliability | 0.8250 | 0.8199 | +0.0050 | 0.0022 | 0.7501 | 0.0013 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | feature_only | 0.8238 | 0.8199 | +0.0038 | 0.0042 | 0.7487 | 0.0026 | 25348 | 95698 |
| Roman-empire | hidden_mixing_finetune | fixed | 0.8245 | 0.8199 | +0.0046 | 0.0060 | 0.7500 | 0.0000 | 0 | 95698 |
| Roman-empire | hidden_mixing_finetune | reliability_only | 0.8334 | 0.8199 | +0.0134 | 0.0016 | 0.7463 | 0.0245 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability | 0.8231 | 0.8199 | +0.0032 | 0.0043 | 0.7501 | 0.0049 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | zero_reliability | 0.8261 | 0.8199 | +0.0061 | 0.0035 | 0.7501 | 0.0016 | 26372 | 95698 |
| Roman-empire | hidden_mixing_frozen | combined | 0.8219 | 0.8199 | +0.0019 | 0.0045 | 0.7519 | 0.0352 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_constant | 0.8194 | 0.8199 | -0.0005 | 0.0029 | 0.7535 | 0.0270 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled | 0.8194 | 0.8199 | -0.0005 | 0.0035 | 0.7539 | 0.0281 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | constant_reliability | 0.8197 | 0.8199 | -0.0002 | 0.0035 | 0.7539 | 0.0164 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | feature_only | 0.8200 | 0.8199 | +0.0000 | 0.0034 | 0.7537 | 0.0228 | 25348 | 0 |
| Roman-empire | hidden_mixing_frozen | fixed | 0.8199 | 0.8199 | +0.0000 | 0.0032 | 0.7500 | 0.0000 | 0 | 0 |
| Roman-empire | hidden_mixing_frozen | reliability_only | 0.8212 | 0.8199 | +0.0013 | 0.0038 | 0.7532 | 0.0290 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability | 0.8198 | 0.8199 | -0.0002 | 0.0033 | 0.7540 | 0.0203 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | zero_reliability | 0.8197 | 0.8199 | -0.0002 | 0.0034 | 0.7539 | 0.0165 | 26372 | 0 |
| Squirrel | hidden_mixing_finetune | combined | 0.3454 | 0.3500 | -0.0046 | 0.0206 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_constant | 0.3462 | 0.3500 | -0.0038 | 0.0201 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_shuffled | 0.3458 | 0.3500 | -0.0042 | 0.0206 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | constant_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | feature_only | 0.3476 | 0.3500 | -0.0025 | 0.0178 | 0.7498 | 0.0008 | 25348 | 209349 |
| Squirrel | hidden_mixing_finetune | fixed | 0.3472 | 0.3500 | -0.0029 | 0.0155 | 0.7500 | 0.0000 | 0 | 209349 |
| Squirrel | hidden_mixing_finetune | reliability_only | 0.3470 | 0.3500 | -0.0031 | 0.0201 | 0.7498 | 0.0009 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | zero_reliability | 0.3470 | 0.3500 | -0.0031 | 0.0199 | 0.7498 | 0.0009 | 26372 | 209349 |
| Squirrel | hidden_mixing_frozen | combined | 0.3479 | 0.3500 | -0.0021 | 0.0165 | 0.7461 | 0.0115 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_constant | 0.3493 | 0.3500 | -0.0008 | 0.0158 | 0.7461 | 0.0059 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_shuffled | 0.3499 | 0.3500 | -0.0002 | 0.0157 | 0.7492 | 0.0017 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | constant_reliability | 0.3495 | 0.3500 | -0.0006 | 0.0157 | 0.7465 | 0.0053 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | feature_only | 0.3497 | 0.3500 | -0.0004 | 0.0161 | 0.7473 | 0.0044 | 25348 | 0 |
| Squirrel | hidden_mixing_frozen | fixed | 0.3500 | 0.3500 | +0.0000 | 0.0155 | 0.7500 | 0.0000 | 0 | 0 |
| Squirrel | hidden_mixing_frozen | reliability_only | 0.3487 | 0.3500 | -0.0013 | 0.0167 | 0.7449 | 0.0156 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability | 0.3500 | 0.3500 | +0.0000 | 0.0155 | 0.7493 | 0.0016 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | zero_reliability | 0.3493 | 0.3500 | -0.0008 | 0.0158 | 0.7464 | 0.0054 | 26372 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Cora | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_finetune | feature_only - fixed | -0.0056 | [-0.0310, +0.0198] | 2/0/3 | +0.5735 |
| Cora | hidden_mixing_finetune | reliability_only - fixed | -0.0042 | [-0.0300, +0.0216] | 2/0/3 | +0.6742 |
| Cora | hidden_mixing_finetune | combined - fixed | -0.0024 | [-0.0309, +0.0261] | 2/0/3 | +0.8265 |
| Cora | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0040 | [-0.0301, +0.0221] | 2/0/3 | +0.6922 |
| Cora | hidden_mixing_finetune | constant_reliability - fixed | -0.0040 | [-0.0293, +0.0213] | 2/0/3 | +0.6836 |
| Cora | hidden_mixing_finetune | zero_reliability - fixed | -0.0056 | [-0.0303, +0.0191] | 2/0/3 | +0.5637 |
| Cora | hidden_mixing_finetune | combined_shuffled - fixed | -0.0026 | [-0.0330, +0.0278] | 2/0/3 | +0.8240 |
| Cora | hidden_mixing_finetune | combined_constant - fixed | -0.0054 | [-0.0292, +0.0184] | 2/0/3 | +0.5636 |
| Cora | hidden_mixing_finetune | reliability_only - feature_only | +0.0014 | [-0.0013, +0.0041] | 2/3/0 | +0.2262 |
| Cora | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_finetune | true reliability - constant reliability | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_finetune | true reliability - zero reliability | +0.0014 | [-0.0018, +0.0046] | 2/3/0 | +0.2962 |
| Cora | hidden_mixing_finetune | combined - feature_only | +0.0032 | [-0.0037, +0.0101] | 3/2/0 | +0.2661 |
| Cora | hidden_mixing_finetune | combined - combined_shuffled | +0.0002 | [-0.0020, +0.0024] | 1/3/1 | +0.8149 |
| Cora | hidden_mixing_finetune | combined - combined_constant | +0.0030 | [-0.0060, +0.0120] | 1/3/1 | +0.4090 |
| Citeseer | hidden_mixing_frozen | feature_only - fixed | +0.0004 | [-0.0003, +0.0011] | 2/3/0 | +0.1778 |
| Citeseer | hidden_mixing_frozen | reliability_only - fixed | -0.0008 | [-0.0022, +0.0006] | 0/3/2 | +0.1778 |
| Citeseer | hidden_mixing_frozen | combined - fixed | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0004 | [-0.0018, +0.0010] | 1/2/2 | +0.4766 |
| Citeseer | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [-0.0015, +0.0015] | 2/2/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | zero_reliability - fixed | -0.0002 | [-0.0016, +0.0012] | 1/3/1 | +0.7040 |
| Citeseer | hidden_mixing_frozen | combined_shuffled - fixed | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined_constant - fixed | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | reliability_only - feature_only | -0.0012 | [-0.0028, +0.0004] | 0/2/3 | +0.1087 |
| Citeseer | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0004 | [-0.0023, +0.0015] | 1/3/1 | +0.5871 |
| Citeseer | hidden_mixing_frozen | true reliability - constant reliability | -0.0008 | [-0.0024, +0.0008] | 0/3/2 | +0.2420 |
| Citeseer | hidden_mixing_frozen | true reliability - zero reliability | -0.0006 | [-0.0017, +0.0005] | 0/3/2 | +0.2080 |
| Citeseer | hidden_mixing_frozen | combined - feature_only | -0.0006 | [-0.0017, +0.0005] | 0/3/2 | +0.2080 |
| Citeseer | hidden_mixing_frozen | combined - combined_shuffled | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined - combined_constant | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | feature_only - fixed | -0.0004 | [-0.0136, +0.0128] | 1/2/2 | +0.9368 |
| Citeseer | hidden_mixing_finetune | reliability_only - fixed | +0.0004 | [-0.0147, +0.0155] | 1/2/2 | +0.9450 |
| Citeseer | hidden_mixing_finetune | combined - fixed | -0.0036 | [-0.0107, +0.0035] | 0/3/2 | +0.2296 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0016 | [-0.0166, +0.0198] | 1/2/2 | +0.8189 |
| Citeseer | hidden_mixing_finetune | constant_reliability - fixed | +0.0010 | [-0.0156, +0.0176] | 1/2/2 | +0.8755 |
| Citeseer | hidden_mixing_finetune | zero_reliability - fixed | +0.0008 | [-0.0153, +0.0169] | 1/2/2 | +0.8971 |
| Citeseer | hidden_mixing_finetune | combined_shuffled - fixed | -0.0036 | [-0.0107, +0.0035] | 0/3/2 | +0.2296 |
| Citeseer | hidden_mixing_finetune | combined_constant - fixed | -0.0036 | [-0.0107, +0.0035] | 0/3/2 | +0.2296 |
| Citeseer | hidden_mixing_finetune | reliability_only - feature_only | +0.0008 | [-0.0014, +0.0030] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0012 | [-0.0045, +0.0021] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | true reliability - constant reliability | -0.0006 | [-0.0023, +0.0011] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | true reliability - zero reliability | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | combined - feature_only | -0.0032 | [-0.0121, +0.0057] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0004 | [-0.0007, +0.0015] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_finetune | feature_only - fixed | -0.0044 | [-0.0141, +0.0053] | 0/3/2 | +0.2756 |
| Pubmed | hidden_mixing_finetune | reliability_only - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | combined - fixed | -0.0052 | [-0.0151, +0.0047] | 0/3/2 | +0.2174 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | constant_reliability - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | zero_reliability - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | combined_shuffled - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | combined_constant - fixed | -0.0072 | [-0.0194, +0.0050] | 0/3/2 | +0.1778 |
| Pubmed | hidden_mixing_finetune | reliability_only - feature_only | -0.0010 | [-0.0038, +0.0018] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_finetune | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_finetune | combined - feature_only | -0.0008 | [-0.0030, +0.0014] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - combined_shuffled | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - combined_constant | +0.0020 | [-0.0036, +0.0076] | 1/4/0 | +0.3739 |
| Chameleon | hidden_mixing_frozen | feature_only - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | reliability_only - fixed | -0.0004 | [-0.0027, +0.0018] | 1/2/2 | +0.6213 |
| Chameleon | hidden_mixing_frozen | combined - fixed | +0.0004 | [-0.0018, +0.0027] | 2/2/1 | +0.6213 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0013 | [-0.0038, +0.0011] | 0/3/2 | +0.2080 |
| Chameleon | hidden_mixing_frozen | constant_reliability - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | zero_reliability - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | combined_shuffled - fixed | -0.0035 | [-0.0092, +0.0021] | 0/2/3 | +0.1596 |
| Chameleon | hidden_mixing_frozen | combined_constant - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | reliability_only - feature_only | +0.0004 | [-0.0018, +0.0027] | 2/2/1 | +0.6213 |
| Chameleon | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0009 | [-0.0033, +0.0050] | 1/3/1 | +0.5870 |
| Chameleon | hidden_mixing_frozen | true reliability - constant reliability | +0.0004 | [-0.0018, +0.0027] | 2/2/1 | +0.6213 |
| Chameleon | hidden_mixing_frozen | true reliability - zero reliability | +0.0004 | [-0.0018, +0.0027] | 2/2/1 | +0.6213 |
| Chameleon | hidden_mixing_frozen | combined - feature_only | +0.0013 | [-0.0002, +0.0028] | 3/2/0 | +0.0705 |
| Chameleon | hidden_mixing_frozen | combined - combined_shuffled | +0.0039 | [-0.0028, +0.0107] | 3/2/0 | +0.1813 |
| Chameleon | hidden_mixing_frozen | combined - combined_constant | +0.0013 | [-0.0002, +0.0028] | 3/2/0 | +0.0705 |
| Chameleon | hidden_mixing_finetune | feature_only - fixed | -0.0044 | [-0.0184, +0.0096] | 1/2/2 | +0.4340 |
| Chameleon | hidden_mixing_finetune | reliability_only - fixed | -0.0022 | [-0.0166, +0.0122] | 2/2/1 | +0.6943 |
| Chameleon | hidden_mixing_finetune | combined - fixed | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0044 | [-0.0184, +0.0096] | 1/2/2 | +0.4340 |
| Chameleon | hidden_mixing_finetune | constant_reliability - fixed | -0.0022 | [-0.0184, +0.0140] | 2/2/1 | +0.7265 |
| Chameleon | hidden_mixing_finetune | zero_reliability - fixed | -0.0022 | [-0.0184, +0.0140] | 2/2/1 | +0.7265 |
| Chameleon | hidden_mixing_finetune | combined_shuffled - fixed | -0.0022 | [-0.0184, +0.0140] | 2/2/1 | +0.7265 |
| Chameleon | hidden_mixing_finetune | combined_constant - fixed | -0.0013 | [-0.0185, +0.0159] | 2/2/1 | +0.8420 |
| Chameleon | hidden_mixing_finetune | reliability_only - feature_only | +0.0022 | [-0.0042, +0.0086] | 2/2/1 | +0.3943 |
| Chameleon | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0022 | [-0.0042, +0.0086] | 2/2/1 | +0.3943 |
| Chameleon | hidden_mixing_finetune | true reliability - constant reliability | +0.0000 | [-0.0019, +0.0019] | 1/3/1 | +1.0000 |
| Chameleon | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [-0.0019, +0.0019] | 1/3/1 | +1.0000 |
| Chameleon | hidden_mixing_finetune | combined - feature_only | +0.0035 | [-0.0062, +0.0133] | 1/4/0 | +0.3739 |
| Chameleon | hidden_mixing_finetune | combined - combined_shuffled | +0.0013 | [-0.0011, +0.0038] | 2/3/0 | +0.2080 |
| Chameleon | hidden_mixing_finetune | combined - combined_constant | +0.0004 | [-0.0008, +0.0017] | 1/4/0 | +0.3739 |
| Squirrel | hidden_mixing_frozen | feature_only - fixed | -0.0004 | [-0.0039, +0.0032] | 2/1/2 | +0.7781 |
| Squirrel | hidden_mixing_frozen | reliability_only - fixed | -0.0013 | [-0.0045, +0.0018] | 0/3/2 | +0.2962 |
| Squirrel | hidden_mixing_frozen | combined - fixed | -0.0021 | [-0.0053, +0.0011] | 0/2/3 | +0.1407 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Squirrel | hidden_mixing_frozen | constant_reliability - fixed | -0.0006 | [-0.0038, +0.0026] | 2/1/2 | +0.6455 |
| Squirrel | hidden_mixing_frozen | zero_reliability - fixed | -0.0008 | [-0.0039, +0.0023] | 1/2/2 | +0.5275 |
| Squirrel | hidden_mixing_frozen | combined_shuffled - fixed | -0.0002 | [-0.0007, +0.0003] | 0/4/1 | +0.3739 |
| Squirrel | hidden_mixing_frozen | combined_constant - fixed | -0.0008 | [-0.0039, +0.0023] | 1/2/2 | +0.5275 |
| Squirrel | hidden_mixing_frozen | reliability_only - feature_only | -0.0010 | [-0.0055, +0.0036] | 2/0/3 | +0.5886 |
| Squirrel | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0013 | [-0.0045, +0.0018] | 0/3/2 | +0.2962 |
| Squirrel | hidden_mixing_frozen | true reliability - constant reliability | -0.0008 | [-0.0052, +0.0036] | 2/0/3 | +0.6541 |
| Squirrel | hidden_mixing_frozen | true reliability - zero reliability | -0.0006 | [-0.0050, +0.0039] | 2/1/2 | +0.7362 |
| Squirrel | hidden_mixing_frozen | combined - feature_only | -0.0017 | [-0.0050, +0.0016] | 1/1/3 | +0.2205 |
| Squirrel | hidden_mixing_frozen | combined - combined_shuffled | -0.0019 | [-0.0053, +0.0015] | 0/3/2 | +0.1890 |
| Squirrel | hidden_mixing_frozen | combined - combined_constant | -0.0013 | [-0.0047, +0.0020] | 1/2/2 | +0.3251 |
| Squirrel | hidden_mixing_finetune | feature_only - fixed | +0.0004 | [-0.0081, +0.0088] | 1/2/2 | +0.9057 |
| Squirrel | hidden_mixing_finetune | reliability_only - fixed | -0.0002 | [-0.0112, +0.0108] | 2/2/1 | +0.9637 |
| Squirrel | hidden_mixing_finetune | combined - fixed | -0.0017 | [-0.0132, +0.0098] | 1/2/2 | +0.6981 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0017 | [-0.0131, +0.0096] | 1/2/2 | +0.6935 |
| Squirrel | hidden_mixing_finetune | constant_reliability - fixed | -0.0017 | [-0.0131, +0.0096] | 1/2/2 | +0.6935 |
| Squirrel | hidden_mixing_finetune | zero_reliability - fixed | -0.0002 | [-0.0107, +0.0104] | 1/3/1 | +0.9621 |
| Squirrel | hidden_mixing_finetune | combined_shuffled - fixed | -0.0013 | [-0.0129, +0.0102] | 1/2/2 | +0.7627 |
| Squirrel | hidden_mixing_finetune | combined_constant - fixed | -0.0010 | [-0.0117, +0.0098] | 1/2/2 | +0.8160 |
| Squirrel | hidden_mixing_finetune | reliability_only - feature_only | -0.0006 | [-0.0086, +0.0075] | 1/3/1 | +0.8525 |
| Squirrel | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0015 | [-0.0034, +0.0065] | 1/3/1 | +0.4382 |
| Squirrel | hidden_mixing_finetune | true reliability - constant reliability | +0.0015 | [-0.0034, +0.0065] | 1/3/1 | +0.4382 |
| Squirrel | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [-0.0008, +0.0008] | 1/3/1 | +1.0000 |
| Squirrel | hidden_mixing_finetune | combined - feature_only | -0.0021 | [-0.0080, +0.0038] | 0/4/1 | +0.3739 |
| Squirrel | hidden_mixing_finetune | combined - combined_shuffled | -0.0004 | [-0.0022, +0.0014] | 1/3/1 | +0.5870 |
| Squirrel | hidden_mixing_finetune | combined - combined_constant | -0.0008 | [-0.0023, +0.0008] | 0/3/2 | +0.2420 |
| Actor | hidden_mixing_frozen | feature_only - fixed | -0.0024 | [-0.0064, +0.0017] | 0/3/2 | +0.1778 |
| Actor | hidden_mixing_frozen | reliability_only - fixed | -0.0000 | [-0.0008, +0.0008] | 2/1/2 | +1.0000 |
| Actor | hidden_mixing_frozen | combined - fixed | -0.0011 | [-0.0035, +0.0014] | 0/3/2 | +0.3058 |
| Actor | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0005 | [-0.0025, +0.0014] | 1/3/1 | +0.4954 |
| Actor | hidden_mixing_frozen | constant_reliability - fixed | +0.0003 | [-0.0007, +0.0012] | 2/2/1 | +0.4766 |
| Actor | hidden_mixing_frozen | zero_reliability - fixed | +0.0003 | [-0.0007, +0.0012] | 2/2/1 | +0.4766 |
| Actor | hidden_mixing_frozen | combined_shuffled - fixed | -0.0014 | [-0.0046, +0.0017] | 0/3/2 | +0.2756 |
| Actor | hidden_mixing_frozen | combined_constant - fixed | +0.0001 | [-0.0008, +0.0010] | 1/3/1 | +0.7040 |
| Actor | hidden_mixing_frozen | reliability_only - feature_only | +0.0024 | [-0.0009, +0.0057] | 4/1/0 | +0.1169 |
| Actor | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0005 | [-0.0012, +0.0023] | 3/1/1 | +0.4557 |
| Actor | hidden_mixing_frozen | true reliability - constant reliability | -0.0003 | [-0.0015, +0.0010] | 1/3/1 | +0.5870 |
| Actor | hidden_mixing_frozen | true reliability - zero reliability | -0.0003 | [-0.0015, +0.0010] | 1/3/1 | +0.5870 |
| Actor | hidden_mixing_frozen | combined - feature_only | +0.0013 | [-0.0015, +0.0041] | 2/3/0 | +0.2663 |
| Actor | hidden_mixing_frozen | combined - combined_shuffled | +0.0004 | [-0.0034, +0.0042] | 1/3/1 | +0.7881 |
| Actor | hidden_mixing_frozen | combined - combined_constant | -0.0012 | [-0.0045, +0.0021] | 0/4/1 | +0.3739 |
| Actor | hidden_mixing_finetune | feature_only - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | reliability_only - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | combined - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | constant_reliability - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | zero_reliability - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | combined_shuffled - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | combined_constant - fixed | -0.0003 | [-0.0012, +0.0007] | 1/2/2 | +0.4766 |
| Actor | hidden_mixing_finetune | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Roman-empire | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [-0.0004, +0.0004] | 2/1/2 | +0.8148 |
| Roman-empire | hidden_mixing_frozen | reliability_only - fixed | +0.0013 | [-0.0008, +0.0034] | 4/0/1 | +0.1601 |
| Roman-empire | hidden_mixing_frozen | combined - fixed | +0.0019 | [-0.0000, +0.0039] | 5/0/0 | +0.0514 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0002 | [-0.0013, +0.0009] | 1/1/3 | +0.6779 |
| Roman-empire | hidden_mixing_frozen | constant_reliability - fixed | -0.0002 | [-0.0009, +0.0005] | 2/1/2 | +0.4375 |
| Roman-empire | hidden_mixing_frozen | zero_reliability - fixed | -0.0002 | [-0.0009, +0.0004] | 2/0/3 | +0.3627 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled - fixed | -0.0005 | [-0.0017, +0.0006] | 1/0/4 | +0.2625 |
| Roman-empire | hidden_mixing_frozen | combined_constant - fixed | -0.0005 | [-0.0014, +0.0004] | 2/0/3 | +0.1841 |
| Roman-empire | hidden_mixing_frozen | reliability_only - feature_only | +0.0013 | [-0.0008, +0.0033] | 4/0/1 | +0.1635 |
| Roman-empire | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0015 | [-0.0014, +0.0044] | 3/0/2 | +0.2284 |
| Roman-empire | hidden_mixing_frozen | true reliability - constant reliability | +0.0015 | [-0.0009, +0.0040] | 4/0/1 | +0.1629 |
| Roman-empire | hidden_mixing_frozen | true reliability - zero reliability | +0.0016 | [-0.0010, +0.0041] | 4/0/1 | +0.1603 |
| Roman-empire | hidden_mixing_frozen | combined - feature_only | +0.0019 | [+0.0002, +0.0036] | 5/0/0 | +0.0367 |
| Roman-empire | hidden_mixing_frozen | combined - combined_shuffled | +0.0025 | [+0.0003, +0.0046] | 5/0/0 | +0.0328 |
| Roman-empire | hidden_mixing_frozen | combined - combined_constant | +0.0025 | [-0.0002, +0.0051] | 5/0/0 | +0.0615 |
| Roman-empire | hidden_mixing_finetune | feature_only - fixed | -0.0007 | [-0.0044, +0.0029] | 1/1/3 | +0.6003 |
| Roman-empire | hidden_mixing_finetune | reliability_only - fixed | +0.0089 | [+0.0020, +0.0157] | 5/0/0 | +0.0232 |
| Roman-empire | hidden_mixing_finetune | combined - fixed | +0.0059 | [+0.0009, +0.0109] | 5/0/0 | +0.0313 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0014 | [-0.0055, +0.0027] | 1/1/3 | +0.3947 |
| Roman-empire | hidden_mixing_finetune | constant_reliability - fixed | +0.0005 | [-0.0060, +0.0069] | 3/0/2 | +0.8533 |
| Roman-empire | hidden_mixing_finetune | zero_reliability - fixed | +0.0015 | [-0.0041, +0.0071] | 3/0/2 | +0.4940 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled - fixed | -0.0013 | [-0.0049, +0.0023] | 1/1/3 | +0.3719 |
| Roman-empire | hidden_mixing_finetune | combined_constant - fixed | +0.0009 | [-0.0025, +0.0043] | 2/1/2 | +0.4936 |
| Roman-empire | hidden_mixing_finetune | reliability_only - feature_only | +0.0096 | [+0.0051, +0.0142] | 5/0/0 | +0.0042 |
| Roman-empire | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0103 | [+0.0056, +0.0149] | 5/0/0 | +0.0036 |
| Roman-empire | hidden_mixing_finetune | true reliability - constant reliability | +0.0084 | [+0.0059, +0.0109] | 5/0/0 | +0.0007 |
| Roman-empire | hidden_mixing_finetune | true reliability - zero reliability | +0.0073 | [+0.0046, +0.0101] | 5/0/0 | +0.0018 |
| Roman-empire | hidden_mixing_finetune | combined - feature_only | +0.0066 | [+0.0035, +0.0097] | 5/0/0 | +0.0039 |
| Roman-empire | hidden_mixing_finetune | combined - combined_shuffled | +0.0072 | [+0.0042, +0.0101] | 5/0/0 | +0.0025 |
| Roman-empire | hidden_mixing_finetune | combined - combined_constant | +0.0049 | [+0.0011, +0.0088] | 5/0/0 | +0.0237 |
| Amazon-ratings | hidden_mixing_frozen | feature_only - fixed | -0.0002 | [-0.0015, +0.0011] | 2/1/2 | +0.6478 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - fixed | -0.0004 | [-0.0019, +0.0011] | 2/1/2 | +0.5068 |
| Amazon-ratings | hidden_mixing_frozen | combined - fixed | -0.0005 | [-0.0018, +0.0008] | 1/1/3 | +0.3565 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0004 | [-0.0020, +0.0011] | 2/1/2 | +0.4871 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability - fixed | -0.0001 | [-0.0012, +0.0010] | 2/1/2 | +0.8117 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability - fixed | -0.0001 | [-0.0012, +0.0010] | 2/1/2 | +0.8117 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled - fixed | -0.0002 | [-0.0011, +0.0008] | 2/1/2 | +0.6686 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant - fixed | -0.0003 | [-0.0015, +0.0010] | 2/1/2 | +0.5918 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - feature_only | -0.0002 | [-0.0014, +0.0011] | 1/2/2 | +0.7283 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [-0.0011, +0.0011] | 1/2/2 | +0.9391 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - constant reliability | -0.0003 | [-0.0016, +0.0010] | 1/2/2 | +0.5624 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - zero reliability | -0.0003 | [-0.0016, +0.0010] | 1/2/2 | +0.5624 |
| Amazon-ratings | hidden_mixing_frozen | combined - feature_only | -0.0003 | [-0.0009, +0.0004] | 1/2/2 | +0.3375 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_shuffled | -0.0003 | [-0.0010, +0.0003] | 1/2/2 | +0.2397 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0009, +0.0005] | 2/1/2 | +0.4137 |
| Amazon-ratings | hidden_mixing_finetune | feature_only - fixed | -0.0018 | [-0.0104, +0.0068] | 3/0/2 | +0.5874 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - fixed | -0.0028 | [-0.0112, +0.0055] | 2/1/2 | +0.3998 |
| Amazon-ratings | hidden_mixing_finetune | combined - fixed | -0.0011 | [-0.0105, +0.0083] | 3/0/2 | +0.7584 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0008 | [-0.0076, +0.0091] | 4/0/1 | +0.8147 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability - fixed | +0.0019 | [-0.0033, +0.0071] | 4/0/1 | +0.3769 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability - fixed | -0.0013 | [-0.0110, +0.0083] | 2/0/3 | +0.7188 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled - fixed | +0.0011 | [-0.0047, +0.0070] | 4/0/1 | +0.6155 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant - fixed | -0.0030 | [-0.0114, +0.0054] | 3/0/2 | +0.3784 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - feature_only | -0.0010 | [-0.0101, +0.0080] | 2/2/1 | +0.7717 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0036 | [-0.0162, +0.0090] | 1/1/3 | +0.4720 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - constant reliability | -0.0047 | [-0.0173, +0.0079] | 2/1/2 | +0.3570 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - zero reliability | -0.0015 | [-0.0071, +0.0041] | 1/2/2 | +0.4998 |
| Amazon-ratings | hidden_mixing_finetune | combined - feature_only | +0.0007 | [-0.0073, +0.0088] | 2/2/1 | +0.8164 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_shuffled | -0.0023 | [-0.0132, +0.0087] | 2/1/2 | +0.5970 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_constant | +0.0019 | [-0.0051, +0.0089] | 2/2/1 | +0.4930 |
| Cora | hidden_protocol | fixed: finetune - frozen | +0.0178 | [-0.0004, +0.0360] | 5/0/0 | +0.0530 |
| Cora | hidden_protocol | feature_only: finetune - frozen | +0.0122 | [-0.0079, +0.0323] | 3/2/0 | +0.1676 |
| Cora | hidden_protocol | reliability_only: finetune - frozen | +0.0136 | [-0.0068, +0.0340] | 3/2/0 | +0.1375 |
| Cora | hidden_protocol | combined: finetune - frozen | +0.0154 | [-0.0068, +0.0376] | 3/2/0 | +0.1265 |
| Cora | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0138 | [-0.0071, +0.0347] | 3/2/0 | +0.1401 |
| Cora | hidden_protocol | constant_reliability: finetune - frozen | +0.0138 | [-0.0065, +0.0341] | 3/2/0 | +0.1321 |
| Cora | hidden_protocol | zero_reliability: finetune - frozen | +0.0122 | [-0.0078, +0.0322] | 3/2/0 | +0.1654 |
| Cora | hidden_protocol | combined_shuffled: finetune - frozen | +0.0152 | [-0.0079, +0.0383] | 3/2/0 | +0.1413 |
| Cora | hidden_protocol | combined_constant: finetune - frozen | +0.0124 | [-0.0080, +0.0328] | 3/2/0 | +0.1661 |
| Citeseer | hidden_protocol | fixed: finetune - frozen | +0.0024 | [-0.0043, +0.0091] | 1/4/0 | +0.3739 |
| Citeseer | hidden_protocol | feature_only: finetune - frozen | +0.0016 | [-0.0088, +0.0120] | 1/1/3 | +0.6916 |
| Citeseer | hidden_protocol | reliability_only: finetune - frozen | +0.0036 | [-0.0083, +0.0155] | 3/1/1 | +0.4470 |
| Citeseer | hidden_protocol | combined: finetune - frozen | -0.0010 | [-0.0039, +0.0019] | 1/2/2 | +0.3943 |
| Citeseer | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0044 | [-0.0108, +0.0196] | 2/1/2 | +0.4658 |
| Citeseer | hidden_protocol | constant_reliability: finetune - frozen | +0.0034 | [-0.0106, +0.0174] | 2/1/2 | +0.5374 |
| Citeseer | hidden_protocol | zero_reliability: finetune - frozen | +0.0034 | [-0.0100, +0.0168] | 2/2/1 | +0.5189 |
| Citeseer | hidden_protocol | combined_shuffled: finetune - frozen | -0.0014 | [-0.0040, +0.0012] | 0/2/3 | +0.2056 |
| Citeseer | hidden_protocol | combined_constant: finetune - frozen | -0.0014 | [-0.0040, +0.0012] | 0/2/3 | +0.2056 |
| Pubmed | hidden_protocol | fixed: finetune - frozen | +0.0012 | [-0.0021, +0.0045] | 1/4/0 | +0.3739 |
| Pubmed | hidden_protocol | feature_only: finetune - frozen | -0.0032 | [-0.0097, +0.0033] | 0/3/2 | +0.2420 |
| Pubmed | hidden_protocol | reliability_only: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 0/3/2 | +0.1836 |
| Pubmed | hidden_protocol | combined: finetune - frozen | -0.0040 | [-0.0110, +0.0030] | 0/3/2 | +0.1890 |
| Pubmed | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0046 | [-0.0115, +0.0023] | 0/2/3 | +0.1374 |
| Pubmed | hidden_protocol | constant_reliability: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 0/3/2 | +0.1836 |
| Pubmed | hidden_protocol | zero_reliability: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 0/3/2 | +0.1836 |
| Pubmed | hidden_protocol | combined_shuffled: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 0/3/2 | +0.1836 |
| Pubmed | hidden_protocol | combined_constant: finetune - frozen | -0.0060 | [-0.0165, +0.0045] | 0/3/2 | +0.1890 |
| Chameleon | hidden_protocol | fixed: finetune - frozen | +0.0004 | [-0.0008, +0.0017] | 1/4/0 | +0.3739 |
| Chameleon | hidden_protocol | feature_only: finetune - frozen | -0.0031 | [-0.0181, +0.0119] | 2/2/1 | +0.6000 |
| Chameleon | hidden_protocol | reliability_only: finetune - frozen | -0.0013 | [-0.0170, +0.0144] | 2/1/2 | +0.8276 |
| Chameleon | hidden_protocol | combined: finetune - frozen | -0.0009 | [-0.0196, +0.0178] | 2/1/2 | +0.9028 |
| Chameleon | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0026 | [-0.0180, +0.0127] | 2/2/1 | +0.6585 |
| Chameleon | hidden_protocol | constant_reliability: finetune - frozen | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_protocol | zero_reliability: finetune - frozen | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_protocol | combined_shuffled: finetune - frozen | +0.0018 | [-0.0183, +0.0218] | 3/1/1 | +0.8200 |
| Chameleon | hidden_protocol | combined_constant: finetune - frozen | -0.0000 | [-0.0190, +0.0190] | 2/2/1 | +1.0000 |
| Squirrel | hidden_protocol | fixed: finetune - frozen | -0.0029 | [-0.0096, +0.0039] | 1/2/2 | +0.3013 |
| Squirrel | hidden_protocol | feature_only: finetune - frozen | -0.0021 | [-0.0084, +0.0042] | 2/0/3 | +0.4029 |
| Squirrel | hidden_protocol | reliability_only: finetune - frozen | -0.0017 | [-0.0093, +0.0059] | 2/2/1 | +0.5624 |
| Squirrel | hidden_protocol | combined: finetune - frozen | -0.0025 | [-0.0104, +0.0054] | 2/1/2 | +0.4317 |
| Squirrel | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0046 | [-0.0139, +0.0047] | 0/3/2 | +0.2420 |
| Squirrel | hidden_protocol | constant_reliability: finetune - frozen | -0.0040 | [-0.0146, +0.0065] | 2/0/3 | +0.3495 |
| Squirrel | hidden_protocol | zero_reliability: finetune - frozen | -0.0023 | [-0.0131, +0.0085] | 3/0/2 | +0.5860 |
| Squirrel | hidden_protocol | combined_shuffled: finetune - frozen | -0.0040 | [-0.0146, +0.0066] | 1/2/2 | +0.3508 |
| Squirrel | hidden_protocol | combined_constant: finetune - frozen | -0.0031 | [-0.0135, +0.0074] | 2/0/3 | +0.4598 |
| Actor | hidden_protocol | fixed: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_protocol | feature_only: finetune - frozen | +0.0021 | [-0.0011, +0.0053] | 3/2/0 | +0.1452 |
| Actor | hidden_protocol | reliability_only: finetune - frozen | -0.0003 | [-0.0007, +0.0002] | 0/3/2 | +0.1778 |
| Actor | hidden_protocol | combined: finetune - frozen | +0.0008 | [-0.0010, +0.0026] | 2/3/0 | +0.2835 |
| Actor | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0003 | [-0.0018, +0.0023] | 2/2/1 | +0.7396 |
| Actor | hidden_protocol | constant_reliability: finetune - frozen | -0.0005 | [-0.0020, +0.0009] | 0/4/1 | +0.3739 |
| Actor | hidden_protocol | zero_reliability: finetune - frozen | -0.0005 | [-0.0020, +0.0009] | 0/4/1 | +0.3739 |
| Actor | hidden_protocol | combined_shuffled: finetune - frozen | +0.0012 | [-0.0017, +0.0040] | 2/3/0 | +0.3134 |
| Actor | hidden_protocol | combined_constant: finetune - frozen | -0.0004 | [-0.0020, +0.0012] | 1/3/1 | +0.5291 |
| Roman-empire | hidden_protocol | fixed: finetune - frozen | +0.0046 | [-0.0012, +0.0104] | 3/2/0 | +0.0942 |
| Roman-empire | hidden_protocol | feature_only: finetune - frozen | +0.0038 | [+0.0000, +0.0076] | 4/1/0 | +0.0491 |
| Roman-empire | hidden_protocol | reliability_only: finetune - frozen | +0.0121 | [+0.0090, +0.0153] | 5/0/0 | +0.0004 |
| Roman-empire | hidden_protocol | combined: finetune - frozen | +0.0085 | [+0.0049, +0.0121] | 5/0/0 | +0.0027 |
| Roman-empire | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0034 | [-0.0004, +0.0071] | 5/0/0 | +0.0688 |
| Roman-empire | hidden_protocol | constant_reliability: finetune - frozen | +0.0053 | [+0.0019, +0.0086] | 5/0/0 | +0.0117 |
| Roman-empire | hidden_protocol | zero_reliability: finetune - frozen | +0.0064 | [+0.0053, +0.0074] | 5/0/0 | +0.0001 |
| Roman-empire | hidden_protocol | combined_shuffled: finetune - frozen | +0.0038 | [+0.0007, +0.0070] | 5/0/0 | +0.0282 |
| Roman-empire | hidden_protocol | combined_constant: finetune - frozen | +0.0060 | [+0.0015, +0.0106] | 5/0/0 | +0.0208 |
| Amazon-ratings | hidden_protocol | fixed: finetune - frozen | +0.0075 | [-0.0011, +0.0160] | 3/2/0 | +0.0720 |
| Amazon-ratings | hidden_protocol | feature_only: finetune - frozen | +0.0059 | [-0.0037, +0.0154] | 3/2/0 | +0.1631 |
| Amazon-ratings | hidden_protocol | reliability_only: finetune - frozen | +0.0050 | [-0.0016, +0.0116] | 4/1/0 | +0.1020 |
| Amazon-ratings | hidden_protocol | combined: finetune - frozen | +0.0069 | [-0.0007, +0.0144] | 4/1/0 | +0.0646 |
| Amazon-ratings | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0087 | [-0.0003, +0.0176] | 5/0/0 | +0.0557 |
| Amazon-ratings | hidden_protocol | constant_reliability: finetune - frozen | +0.0094 | [-0.0010, +0.0199] | 4/1/0 | +0.0664 |
| Amazon-ratings | hidden_protocol | zero_reliability: finetune - frozen | +0.0062 | [-0.0010, +0.0135] | 3/2/0 | +0.0743 |
| Amazon-ratings | hidden_protocol | combined_shuffled: finetune - frozen | +0.0088 | [+0.0008, +0.0168] | 5/0/0 | +0.0377 |
| Amazon-ratings | hidden_protocol | combined_constant: finetune - frozen | +0.0047 | [-0.0026, +0.0121] | 3/2/0 | +0.1490 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
