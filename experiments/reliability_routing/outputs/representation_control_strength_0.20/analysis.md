# Representation Control Screening

- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor, Roman-empire, Amazon-ratings
- Families: hidden_mixing_frozen, hidden_mixing_finetune
- Runs: 5
- Edge protocol: undirected
- Max adjustment: 0.2
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
| Actor | hidden_mixing_frozen | combined | 0.3641 | 0.3647 | -0.0007 | 0.0077 | 0.8157 | 0.0376 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_constant | 0.3628 | 0.3647 | -0.0020 | 0.0080 | 0.8133 | 0.0599 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_shuffled | 0.3626 | 0.3647 | -0.0021 | 0.0077 | 0.8125 | 0.0398 | 34948 | 0 |
| Actor | hidden_mixing_frozen | constant_reliability | 0.3637 | 0.3647 | -0.0011 | 0.0072 | 0.8134 | 0.0374 | 26372 | 0 |
| Actor | hidden_mixing_frozen | feature_only | 0.3624 | 0.3647 | -0.0024 | 0.0068 | 0.8159 | 0.0420 | 25348 | 0 |
| Actor | hidden_mixing_frozen | fixed | 0.3647 | 0.3647 | +0.0000 | 0.0074 | 0.8500 | 0.0000 | 0 | 0 |
| Actor | hidden_mixing_frozen | reliability_only | 0.3642 | 0.3647 | -0.0005 | 0.0075 | 0.8127 | 0.0401 | 26372 | 0 |
| Actor | hidden_mixing_frozen | shuffled_reliability | 0.3625 | 0.3647 | -0.0022 | 0.0079 | 0.8084 | 0.0668 | 26372 | 0 |
| Actor | hidden_mixing_frozen | zero_reliability | 0.3637 | 0.3647 | -0.0011 | 0.0072 | 0.8134 | 0.0374 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_finetune | combined | 0.4727 | 0.4672 | +0.0055 | 0.0078 | 0.7473 | 0.0202 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant | 0.4728 | 0.4672 | +0.0056 | 0.0084 | 0.7524 | 0.0151 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled | 0.4710 | 0.4672 | +0.0038 | 0.0061 | 0.7567 | 0.0288 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability | 0.4713 | 0.4672 | +0.0041 | 0.0083 | 0.7512 | 0.0062 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | feature_only | 0.4724 | 0.4672 | +0.0052 | 0.0081 | 0.7512 | 0.0128 | 25348 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | fixed | 0.4739 | 0.4672 | +0.0067 | 0.0091 | 0.7500 | 0.0000 | 0 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only | 0.4712 | 0.4672 | +0.0040 | 0.0084 | 0.7486 | 0.0155 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability | 0.4719 | 0.4672 | +0.0047 | 0.0077 | 0.7580 | 0.0367 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability | 0.4710 | 0.4672 | +0.0038 | 0.0070 | 0.7515 | 0.0073 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_frozen | combined | 0.4656 | 0.4672 | -0.0016 | 0.0031 | 0.7374 | 0.0347 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant | 0.4657 | 0.4672 | -0.0015 | 0.0033 | 0.7371 | 0.0340 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled | 0.4668 | 0.4672 | -0.0004 | 0.0040 | 0.7400 | 0.0121 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability | 0.4671 | 0.4672 | -0.0001 | 0.0040 | 0.7463 | 0.0165 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | feature_only | 0.4658 | 0.4672 | -0.0014 | 0.0031 | 0.7375 | 0.0340 | 25348 | 0 |
| Amazon-ratings | hidden_mixing_frozen | fixed | 0.4672 | 0.4672 | +0.0000 | 0.0040 | 0.7500 | 0.0000 | 0 | 0 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only | 0.4665 | 0.4672 | -0.0007 | 0.0038 | 0.7407 | 0.0268 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability | 0.4669 | 0.4672 | -0.0003 | 0.0040 | 0.7467 | 0.0051 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability | 0.4672 | 0.4672 | -0.0000 | 0.0039 | 0.7446 | 0.0187 | 26372 | 0 |
| Chameleon | hidden_mixing_finetune | combined | 0.5430 | 0.5434 | -0.0004 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_constant | 0.5425 | 0.5434 | -0.0009 | 0.0296 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_shuffled | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | constant_reliability | 0.5390 | 0.5434 | -0.0044 | 0.0302 | 0.7997 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | feature_only | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 25348 | 224453 |
| Chameleon | hidden_mixing_finetune | fixed | 0.5439 | 0.5434 | +0.0004 | 0.0314 | 0.8000 | 0.0000 | 0 | 224453 |
| Chameleon | hidden_mixing_finetune | reliability_only | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | zero_reliability | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_frozen | combined | 0.5447 | 0.5434 | +0.0013 | 0.0308 | 0.8057 | 0.0321 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_constant | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7999 | 0.0166 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_shuffled | 0.5417 | 0.5434 | -0.0018 | 0.0319 | 0.7940 | 0.0098 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | constant_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7970 | 0.0062 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | feature_only | 0.5421 | 0.5434 | -0.0013 | 0.0326 | 0.7970 | 0.0061 | 25348 | 0 |
| Chameleon | hidden_mixing_frozen | fixed | 0.5434 | 0.5434 | +0.0000 | 0.0316 | 0.8000 | 0.0000 | 0 | 0 |
| Chameleon | hidden_mixing_frozen | reliability_only | 0.5456 | 0.5434 | +0.0022 | 0.0310 | 0.8082 | 0.0357 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability | 0.5408 | 0.5434 | -0.0026 | 0.0322 | 0.7910 | 0.0186 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | zero_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7971 | 0.0059 | 26372 | 0 |
| Citeseer | hidden_mixing_finetune | combined | 0.6130 | 0.6144 | -0.0014 | 0.0228 | 0.7597 | 0.0209 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_constant | 0.6126 | 0.6144 | -0.0018 | 0.0227 | 0.7597 | 0.0209 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_shuffled | 0.6138 | 0.6144 | -0.0006 | 0.0231 | 0.7597 | 0.0209 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | constant_reliability | 0.6158 | 0.6144 | +0.0014 | 0.0173 | 0.7597 | 0.0209 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | feature_only | 0.6132 | 0.6144 | -0.0012 | 0.0229 | 0.7498 | 0.0010 | 25348 | 312710 |
| Citeseer | hidden_mixing_finetune | fixed | 0.6168 | 0.6144 | +0.0024 | 0.0217 | 0.7500 | 0.0000 | 0 | 312710 |
| Citeseer | hidden_mixing_finetune | reliability_only | 0.6162 | 0.6144 | +0.0018 | 0.0178 | 0.7597 | 0.0208 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability | 0.6166 | 0.6144 | +0.0022 | 0.0167 | 0.7596 | 0.0206 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | zero_reliability | 0.6168 | 0.6144 | +0.0024 | 0.0174 | 0.7598 | 0.0209 | 26372 | 312710 |
| Citeseer | hidden_mixing_frozen | combined | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7346 | 0.0213 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_constant | 0.6146 | 0.6144 | +0.0002 | 0.0234 | 0.7492 | 0.0019 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_shuffled | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7492 | 0.0018 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | constant_reliability | 0.6142 | 0.6144 | -0.0002 | 0.0236 | 0.7502 | 0.0046 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | feature_only | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7494 | 0.0016 | 25348 | 0 |
| Citeseer | hidden_mixing_frozen | fixed | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7500 | 0.0000 | 0 | 0 |
| Citeseer | hidden_mixing_frozen | reliability_only | 0.6140 | 0.6144 | -0.0004 | 0.0235 | 0.7325 | 0.0240 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability | 0.6140 | 0.6144 | -0.0004 | 0.0236 | 0.7504 | 0.0046 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | zero_reliability | 0.6144 | 0.6144 | +0.0000 | 0.0238 | 0.7502 | 0.0046 | 26372 | 0 |
| Cora | hidden_mixing_finetune | combined | 0.7040 | 0.6872 | +0.0168 | 0.0159 | 0.7996 | 0.0011 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_constant | 0.6990 | 0.6872 | +0.0118 | 0.0151 | 0.7996 | 0.0010 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_shuffled | 0.6992 | 0.6872 | +0.0120 | 0.0151 | 0.7994 | 0.0013 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | constant_reliability | 0.7016 | 0.6872 | +0.0144 | 0.0142 | 0.7998 | 0.0008 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | feature_only | 0.6994 | 0.6872 | +0.0122 | 0.0151 | 0.7996 | 0.0010 | 25348 | 167495 |
| Cora | hidden_mixing_finetune | fixed | 0.7044 | 0.6872 | +0.0172 | 0.0100 | 0.8000 | 0.0000 | 0 | 167495 |
| Cora | hidden_mixing_finetune | reliability_only | 0.6996 | 0.6872 | +0.0124 | 0.0146 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | shuffled_reliability | 0.7010 | 0.6872 | +0.0138 | 0.0147 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | zero_reliability | 0.6994 | 0.6872 | +0.0122 | 0.0151 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_frozen | combined | 0.6870 | 0.6872 | -0.0002 | 0.0117 | 0.7975 | 0.0040 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_constant | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_shuffled | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | constant_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | feature_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 25348 | 0 |
| Cora | hidden_mixing_frozen | fixed | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.8000 | 0.0000 | 0 | 0 |
| Cora | hidden_mixing_frozen | reliability_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | shuffled_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | zero_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Pubmed | hidden_mixing_finetune | combined | 0.7298 | 0.7344 | -0.0046 | 0.0111 | 0.8493 | 0.0014 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_constant | 0.7324 | 0.7344 | -0.0020 | 0.0097 | 0.8348 | 0.0213 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_shuffled | 0.7298 | 0.7344 | -0.0046 | 0.0111 | 0.8491 | 0.0017 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | constant_reliability | 0.7300 | 0.7344 | -0.0044 | 0.0109 | 0.8383 | 0.0160 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | feature_only | 0.7292 | 0.7344 | -0.0052 | 0.0117 | 0.8405 | 0.0132 | 25348 | 107523 |
| Pubmed | hidden_mixing_finetune | fixed | 0.7356 | 0.7344 | +0.0012 | 0.0138 | 0.8500 | 0.0000 | 0 | 107523 |
| Pubmed | hidden_mixing_finetune | reliability_only | 0.7316 | 0.7344 | -0.0028 | 0.0099 | 0.8399 | 0.0139 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability | 0.7300 | 0.7344 | -0.0044 | 0.0109 | 0.8367 | 0.0182 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | zero_reliability | 0.7298 | 0.7344 | -0.0046 | 0.0111 | 0.8495 | 0.0012 | 26372 | 107523 |
| Pubmed | hidden_mixing_frozen | combined | 0.7342 | 0.7344 | -0.0002 | 0.0124 | 0.8480 | 0.0064 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_constant | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8475 | 0.0038 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_shuffled | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8478 | 0.0035 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | constant_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8480 | 0.0032 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | feature_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8492 | 0.0015 | 25348 | 0 |
| Pubmed | hidden_mixing_frozen | fixed | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8500 | 0.0000 | 0 | 0 |
| Pubmed | hidden_mixing_frozen | reliability_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8489 | 0.0020 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability | 0.7338 | 0.7344 | -0.0006 | 0.0112 | 0.8238 | 0.0285 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | zero_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8476 | 0.0038 | 26372 | 0 |
| Roman-empire | hidden_mixing_finetune | combined | 0.8354 | 0.8199 | +0.0154 | 0.0021 | 0.7468 | 0.0447 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_constant | 0.8254 | 0.8199 | +0.0054 | 0.0034 | 0.7501 | 0.0026 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled | 0.8256 | 0.8199 | +0.0056 | 0.0029 | 0.7493 | 0.0046 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | constant_reliability | 0.8242 | 0.8199 | +0.0043 | 0.0042 | 0.7500 | 0.0012 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | feature_only | 0.8234 | 0.8199 | +0.0034 | 0.0044 | 0.7492 | 0.0020 | 25348 | 95698 |
| Roman-empire | hidden_mixing_finetune | fixed | 0.8246 | 0.8199 | +0.0047 | 0.0053 | 0.7500 | 0.0000 | 0 | 95698 |
| Roman-empire | hidden_mixing_finetune | reliability_only | 0.8341 | 0.8199 | +0.0141 | 0.0025 | 0.7430 | 0.0514 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability | 0.8251 | 0.8199 | +0.0051 | 0.0050 | 0.7498 | 0.0035 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | zero_reliability | 0.8244 | 0.8199 | +0.0044 | 0.0033 | 0.7499 | 0.0007 | 26372 | 95698 |
| Roman-empire | hidden_mixing_frozen | combined | 0.8232 | 0.8199 | +0.0033 | 0.0038 | 0.7538 | 0.0677 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_constant | 0.8206 | 0.8199 | +0.0007 | 0.0041 | 0.7593 | 0.0479 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled | 0.8200 | 0.8199 | +0.0001 | 0.0053 | 0.7600 | 0.0555 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | constant_reliability | 0.8200 | 0.8199 | +0.0000 | 0.0034 | 0.7566 | 0.0275 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | feature_only | 0.8209 | 0.8199 | +0.0009 | 0.0039 | 0.7597 | 0.0473 | 25348 | 0 |
| Roman-empire | hidden_mixing_frozen | fixed | 0.8199 | 0.8199 | +0.0000 | 0.0032 | 0.7500 | 0.0000 | 0 | 0 |
| Roman-empire | hidden_mixing_frozen | reliability_only | 0.8235 | 0.8199 | +0.0035 | 0.0032 | 0.7587 | 0.0634 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability | 0.8201 | 0.8199 | +0.0001 | 0.0038 | 0.7562 | 0.0296 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | zero_reliability | 0.8199 | 0.8199 | -0.0000 | 0.0035 | 0.7561 | 0.0251 | 26372 | 0 |
| Squirrel | hidden_mixing_finetune | combined | 0.3466 | 0.3500 | -0.0035 | 0.0202 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_constant | 0.3462 | 0.3500 | -0.0038 | 0.0201 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_shuffled | 0.3468 | 0.3500 | -0.0033 | 0.0204 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | constant_reliability | 0.3470 | 0.3500 | -0.0031 | 0.0199 | 0.7498 | 0.0009 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | feature_only | 0.3474 | 0.3500 | -0.0027 | 0.0179 | 0.7498 | 0.0008 | 25348 | 209349 |
| Squirrel | hidden_mixing_finetune | fixed | 0.3454 | 0.3500 | -0.0046 | 0.0168 | 0.7500 | 0.0000 | 0 | 209349 |
| Squirrel | hidden_mixing_finetune | reliability_only | 0.3458 | 0.3500 | -0.0042 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | zero_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_frozen | combined | 0.3495 | 0.3500 | -0.0006 | 0.0163 | 0.7298 | 0.0501 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_constant | 0.3497 | 0.3500 | -0.0004 | 0.0165 | 0.7458 | 0.0063 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_shuffled | 0.3504 | 0.3500 | +0.0004 | 0.0153 | 0.7411 | 0.0246 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | constant_reliability | 0.3510 | 0.3500 | +0.0010 | 0.0161 | 0.7492 | 0.0132 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | feature_only | 0.3497 | 0.3500 | -0.0004 | 0.0163 | 0.7434 | 0.0096 | 25348 | 0 |
| Squirrel | hidden_mixing_frozen | fixed | 0.3500 | 0.3500 | +0.0000 | 0.0155 | 0.7500 | 0.0000 | 0 | 0 |
| Squirrel | hidden_mixing_frozen | reliability_only | 0.3483 | 0.3500 | -0.0017 | 0.0160 | 0.7382 | 0.0284 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability | 0.3514 | 0.3500 | +0.0013 | 0.0150 | 0.7480 | 0.0280 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | zero_reliability | 0.3504 | 0.3500 | +0.0004 | 0.0154 | 0.7481 | 0.0128 | 26372 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Cora | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - fixed | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Cora | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_frozen | combined - combined_shuffled | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Cora | hidden_mixing_finetune | feature_only - fixed | -0.0050 | [-0.0297, +0.0197] | 2/0/3 | +0.6047 |
| Cora | hidden_mixing_finetune | reliability_only - fixed | -0.0048 | [-0.0284, +0.0188] | 2/0/3 | +0.6031 |
| Cora | hidden_mixing_finetune | combined - fixed | -0.0004 | [-0.0309, +0.0301] | 2/0/3 | +0.9727 |
| Cora | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0034 | [-0.0289, +0.0221] | 2/0/3 | +0.7302 |
| Cora | hidden_mixing_finetune | constant_reliability - fixed | -0.0028 | [-0.0285, +0.0229] | 2/0/3 | +0.7771 |
| Cora | hidden_mixing_finetune | zero_reliability - fixed | -0.0050 | [-0.0297, +0.0197] | 2/0/3 | +0.6047 |
| Cora | hidden_mixing_finetune | combined_shuffled - fixed | -0.0052 | [-0.0286, +0.0182] | 2/0/3 | +0.5709 |
| Cora | hidden_mixing_finetune | combined_constant - fixed | -0.0054 | [-0.0281, +0.0173] | 2/0/3 | +0.5442 |
| Cora | hidden_mixing_finetune | reliability_only - feature_only | +0.0002 | [-0.0012, +0.0016] | 1/3/1 | +0.7040 |
| Cora | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0014 | [-0.0046, +0.0018] | 0/3/2 | +0.2962 |
| Cora | hidden_mixing_finetune | true reliability - constant reliability | -0.0020 | [-0.0069, +0.0029] | 0/3/2 | +0.3194 |
| Cora | hidden_mixing_finetune | true reliability - zero reliability | +0.0002 | [-0.0012, +0.0016] | 1/3/1 | +0.7040 |
| Cora | hidden_mixing_finetune | combined - feature_only | +0.0046 | [-0.0061, +0.0153] | 3/2/0 | +0.3001 |
| Cora | hidden_mixing_finetune | combined - combined_shuffled | +0.0048 | [-0.0085, +0.0181] | 1/4/0 | +0.3739 |
| Cora | hidden_mixing_finetune | combined - combined_constant | +0.0050 | [-0.0096, +0.0196] | 1/3/1 | +0.3951 |
| Citeseer | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | reliability_only - fixed | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0004 | [-0.0018, +0.0010] | 1/2/2 | +0.4766 |
| Citeseer | hidden_mixing_frozen | constant_reliability - fixed | -0.0002 | [-0.0016, +0.0012] | 1/3/1 | +0.7040 |
| Citeseer | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [-0.0015, +0.0015] | 2/2/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined_constant - fixed | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | reliability_only - feature_only | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [-0.0009, +0.0009] | 1/3/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | true reliability - constant reliability | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | true reliability - zero reliability | -0.0004 | [-0.0011, +0.0003] | 0/3/2 | +0.1778 |
| Citeseer | hidden_mixing_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | feature_only - fixed | -0.0036 | [-0.0107, +0.0035] | 0/3/2 | +0.2296 |
| Citeseer | hidden_mixing_finetune | reliability_only - fixed | -0.0006 | [-0.0159, +0.0147] | 1/2/2 | +0.9187 |
| Citeseer | hidden_mixing_finetune | combined - fixed | -0.0038 | [-0.0110, +0.0034] | 0/3/2 | +0.2143 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0002 | [-0.0202, +0.0198] | 1/2/2 | +0.9792 |
| Citeseer | hidden_mixing_finetune | constant_reliability - fixed | -0.0010 | [-0.0190, +0.0170] | 1/2/2 | +0.8851 |
| Citeseer | hidden_mixing_finetune | zero_reliability - fixed | -0.0000 | [-0.0161, +0.0161] | 1/2/2 | +1.0000 |
| Citeseer | hidden_mixing_finetune | combined_shuffled - fixed | -0.0030 | [-0.0100, +0.0040] | 0/3/2 | +0.3013 |
| Citeseer | hidden_mixing_finetune | combined_constant - fixed | -0.0042 | [-0.0117, +0.0033] | 0/3/2 | +0.1936 |
| Citeseer | hidden_mixing_finetune | reliability_only - feature_only | +0.0030 | [-0.0083, +0.0143] | 1/3/1 | +0.5024 |
| Citeseer | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0004 | [-0.0057, +0.0049] | 1/3/1 | +0.8446 |
| Citeseer | hidden_mixing_finetune | true reliability - constant reliability | +0.0004 | [-0.0032, +0.0040] | 1/3/1 | +0.7717 |
| Citeseer | hidden_mixing_finetune | true reliability - zero reliability | -0.0006 | [-0.0017, +0.0005] | 0/3/2 | +0.2080 |
| Citeseer | hidden_mixing_finetune | combined - feature_only | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | combined - combined_shuffled | -0.0008 | [-0.0030, +0.0014] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | combined - combined_constant | +0.0004 | [-0.0007, +0.0015] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - fixed | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0006 | [-0.0030, +0.0018] | 1/3/1 | +0.5291 |
| Pubmed | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0006 | [-0.0018, +0.0030] | 1/3/1 | +0.5291 |
| Pubmed | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | combined - combined_shuffled | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_finetune | feature_only - fixed | -0.0064 | [-0.0174, +0.0046] | 0/3/2 | +0.1822 |
| Pubmed | hidden_mixing_finetune | reliability_only - fixed | -0.0040 | [-0.0138, +0.0058] | 0/3/2 | +0.3194 |
| Pubmed | hidden_mixing_finetune | combined - fixed | -0.0058 | [-0.0161, +0.0045] | 0/3/2 | +0.1940 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0056 | [-0.0157, +0.0045] | 0/3/2 | +0.2003 |
| Pubmed | hidden_mixing_finetune | constant_reliability - fixed | -0.0056 | [-0.0157, +0.0045] | 0/3/2 | +0.2003 |
| Pubmed | hidden_mixing_finetune | zero_reliability - fixed | -0.0058 | [-0.0161, +0.0045] | 0/3/2 | +0.1940 |
| Pubmed | hidden_mixing_finetune | combined_shuffled - fixed | -0.0058 | [-0.0161, +0.0045] | 0/3/2 | +0.1940 |
| Pubmed | hidden_mixing_finetune | combined_constant - fixed | -0.0032 | [-0.0135, +0.0071] | 1/3/1 | +0.4382 |
| Pubmed | hidden_mixing_finetune | reliability_only - feature_only | +0.0024 | [-0.0043, +0.0091] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0016 | [-0.0028, +0.0060] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - constant reliability | +0.0016 | [-0.0028, +0.0060] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - zero reliability | +0.0018 | [-0.0032, +0.0068] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - feature_only | +0.0006 | [-0.0011, +0.0023] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_finetune | combined - combined_constant | -0.0026 | [-0.0098, +0.0046] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | feature_only - fixed | -0.0013 | [-0.0038, +0.0011] | 0/3/2 | +0.2080 |
| Chameleon | hidden_mixing_frozen | reliability_only - fixed | +0.0022 | [-0.0055, +0.0099] | 1/3/1 | +0.4734 |
| Chameleon | hidden_mixing_frozen | combined - fixed | +0.0013 | [-0.0046, +0.0073] | 2/2/1 | +0.5734 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0026 | [-0.0062, +0.0009] | 0/2/3 | +0.1087 |
| Chameleon | hidden_mixing_frozen | constant_reliability - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | zero_reliability - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | combined_shuffled - fixed | -0.0018 | [-0.0040, +0.0005] | 0/2/3 | +0.0993 |
| Chameleon | hidden_mixing_frozen | combined_constant - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | reliability_only - feature_only | +0.0035 | [-0.0033, +0.0103] | 3/2/0 | +0.2272 |
| Chameleon | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0048 | [-0.0020, +0.0116] | 3/2/0 | +0.1194 |
| Chameleon | hidden_mixing_frozen | true reliability - constant reliability | +0.0031 | [-0.0040, +0.0102] | 2/3/0 | +0.2962 |
| Chameleon | hidden_mixing_frozen | true reliability - zero reliability | +0.0031 | [-0.0040, +0.0102] | 2/3/0 | +0.2962 |
| Chameleon | hidden_mixing_frozen | combined - feature_only | +0.0026 | [-0.0022, +0.0075] | 2/3/0 | +0.2080 |
| Chameleon | hidden_mixing_frozen | combined - combined_shuffled | +0.0031 | [-0.0015, +0.0076] | 3/2/0 | +0.1347 |
| Chameleon | hidden_mixing_frozen | combined - combined_constant | +0.0022 | [-0.0025, +0.0069] | 2/3/0 | +0.2663 |
| Chameleon | hidden_mixing_finetune | feature_only - fixed | -0.0044 | [-0.0184, +0.0096] | 1/2/2 | +0.4340 |
| Chameleon | hidden_mixing_finetune | reliability_only - fixed | -0.0022 | [-0.0166, +0.0122] | 2/2/1 | +0.6943 |
| Chameleon | hidden_mixing_finetune | combined - fixed | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0044 | [-0.0184, +0.0096] | 1/2/2 | +0.4340 |
| Chameleon | hidden_mixing_finetune | constant_reliability - fixed | -0.0048 | [-0.0184, +0.0087] | 1/2/2 | +0.3783 |
| Chameleon | hidden_mixing_finetune | zero_reliability - fixed | -0.0022 | [-0.0184, +0.0140] | 2/2/1 | +0.7265 |
| Chameleon | hidden_mixing_finetune | combined_shuffled - fixed | -0.0022 | [-0.0184, +0.0140] | 2/2/1 | +0.7265 |
| Chameleon | hidden_mixing_finetune | combined_constant - fixed | -0.0013 | [-0.0185, +0.0159] | 2/2/1 | +0.8420 |
| Chameleon | hidden_mixing_finetune | reliability_only - feature_only | +0.0022 | [-0.0042, +0.0086] | 2/2/1 | +0.3943 |
| Chameleon | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0022 | [-0.0042, +0.0086] | 2/2/1 | +0.3943 |
| Chameleon | hidden_mixing_finetune | true reliability - constant reliability | +0.0026 | [-0.0033, +0.0085] | 2/3/0 | +0.2835 |
| Chameleon | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [-0.0019, +0.0019] | 1/3/1 | +1.0000 |
| Chameleon | hidden_mixing_finetune | combined - feature_only | +0.0035 | [-0.0062, +0.0133] | 1/4/0 | +0.3739 |
| Chameleon | hidden_mixing_finetune | combined - combined_shuffled | +0.0013 | [-0.0011, +0.0038] | 2/3/0 | +0.2080 |
| Chameleon | hidden_mixing_finetune | combined - combined_constant | +0.0004 | [-0.0008, +0.0017] | 1/4/0 | +0.3739 |
| Squirrel | hidden_mixing_frozen | feature_only - fixed | -0.0004 | [-0.0036, +0.0028] | 2/1/2 | +0.7572 |
| Squirrel | hidden_mixing_frozen | reliability_only - fixed | -0.0017 | [-0.0042, +0.0007] | 0/2/3 | +0.1210 |
| Squirrel | hidden_mixing_frozen | combined - fixed | -0.0006 | [-0.0042, +0.0031] | 2/1/2 | +0.6827 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0013 | [-0.0024, +0.0051] | 1/4/0 | +0.3739 |
| Squirrel | hidden_mixing_frozen | constant_reliability - fixed | +0.0010 | [-0.0038, +0.0057] | 2/1/2 | +0.6060 |
| Squirrel | hidden_mixing_frozen | zero_reliability - fixed | +0.0004 | [-0.0044, +0.0052] | 2/1/2 | +0.8355 |
| Squirrel | hidden_mixing_frozen | combined_shuffled - fixed | +0.0004 | [-0.0032, +0.0039] | 2/1/2 | +0.7780 |
| Squirrel | hidden_mixing_frozen | combined_constant - fixed | -0.0004 | [-0.0042, +0.0034] | 1/2/2 | +0.7943 |
| Squirrel | hidden_mixing_frozen | reliability_only - feature_only | -0.0013 | [-0.0038, +0.0011] | 1/1/3 | +0.2056 |
| Squirrel | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0031 | [-0.0064, +0.0002] | 0/1/4 | +0.0614 |
| Squirrel | hidden_mixing_frozen | true reliability - constant reliability | -0.0027 | [-0.0059, +0.0005] | 0/2/3 | +0.0800 |
| Squirrel | hidden_mixing_frozen | true reliability - zero reliability | -0.0021 | [-0.0055, +0.0013] | 1/1/3 | +0.1609 |
| Squirrel | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0025, +0.0021] | 1/1/3 | +0.8276 |
| Squirrel | hidden_mixing_frozen | combined - combined_shuffled | -0.0010 | [-0.0045, +0.0026] | 2/0/3 | +0.4975 |
| Squirrel | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0020, +0.0016] | 1/2/2 | +0.7780 |
| Squirrel | hidden_mixing_finetune | feature_only - fixed | +0.0019 | [-0.0060, +0.0099] | 2/2/1 | +0.5393 |
| Squirrel | hidden_mixing_finetune | reliability_only - fixed | +0.0004 | [-0.0091, +0.0099] | 1/2/2 | +0.9159 |
| Squirrel | hidden_mixing_finetune | combined - fixed | +0.0012 | [-0.0082, +0.0105] | 2/2/1 | +0.7498 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0000 | [-0.0096, +0.0096] | 1/2/2 | +1.0000 |
| Squirrel | hidden_mixing_finetune | constant_reliability - fixed | +0.0015 | [-0.0075, +0.0106] | 2/2/1 | +0.6611 |
| Squirrel | hidden_mixing_finetune | zero_reliability - fixed | -0.0000 | [-0.0096, +0.0096] | 1/2/2 | +1.0000 |
| Squirrel | hidden_mixing_finetune | combined_shuffled - fixed | +0.0013 | [-0.0085, +0.0112] | 2/2/1 | +0.7250 |
| Squirrel | hidden_mixing_finetune | combined_constant - fixed | +0.0008 | [-0.0083, +0.0098] | 1/2/2 | +0.8254 |
| Squirrel | hidden_mixing_finetune | reliability_only - feature_only | -0.0015 | [-0.0080, +0.0049] | 1/3/1 | +0.5448 |
| Squirrel | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0004 | [-0.0014, +0.0022] | 1/3/1 | +0.5870 |
| Squirrel | hidden_mixing_finetune | true reliability - constant reliability | -0.0012 | [-0.0037, +0.0014] | 0/3/2 | +0.2835 |
| Squirrel | hidden_mixing_finetune | true reliability - zero reliability | +0.0004 | [-0.0014, +0.0022] | 1/3/1 | +0.5870 |
| Squirrel | hidden_mixing_finetune | combined - feature_only | -0.0008 | [-0.0085, +0.0069] | 1/3/1 | +0.7955 |
| Squirrel | hidden_mixing_finetune | combined - combined_shuffled | -0.0002 | [-0.0015, +0.0011] | 1/3/1 | +0.7040 |
| Squirrel | hidden_mixing_finetune | combined - combined_constant | +0.0004 | [-0.0014, +0.0022] | 1/3/1 | +0.5871 |
| Actor | hidden_mixing_frozen | feature_only - fixed | -0.0024 | [-0.0055, +0.0007] | 0/2/3 | +0.1004 |
| Actor | hidden_mixing_frozen | reliability_only - fixed | -0.0005 | [-0.0035, +0.0025] | 2/1/2 | +0.6541 |
| Actor | hidden_mixing_frozen | combined - fixed | -0.0007 | [-0.0034, +0.0021] | 2/2/1 | +0.5457 |
| Actor | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0022 | [-0.0064, +0.0020] | 1/0/4 | +0.2124 |
| Actor | hidden_mixing_frozen | constant_reliability - fixed | -0.0011 | [-0.0037, +0.0016] | 1/2/2 | +0.3274 |
| Actor | hidden_mixing_frozen | zero_reliability - fixed | -0.0011 | [-0.0037, +0.0016] | 1/2/2 | +0.3274 |
| Actor | hidden_mixing_frozen | combined_shuffled - fixed | -0.0021 | [-0.0059, +0.0017] | 0/2/3 | +0.1993 |
| Actor | hidden_mixing_frozen | combined_constant - fixed | -0.0020 | [-0.0073, +0.0034] | 2/1/2 | +0.3641 |
| Actor | hidden_mixing_frozen | reliability_only - feature_only | +0.0018 | [-0.0003, +0.0040] | 4/1/0 | +0.0729 |
| Actor | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0017 | [-0.0008, +0.0042] | 3/1/1 | +0.1293 |
| Actor | hidden_mixing_frozen | true reliability - constant reliability | +0.0005 | [-0.0002, +0.0012] | 3/2/0 | +0.0993 |
| Actor | hidden_mixing_frozen | true reliability - zero reliability | +0.0005 | [-0.0002, +0.0012] | 3/2/0 | +0.0993 |
| Actor | hidden_mixing_frozen | combined - feature_only | +0.0017 | [-0.0003, +0.0037] | 4/1/0 | +0.0732 |
| Actor | hidden_mixing_frozen | combined - combined_shuffled | +0.0014 | [-0.0000, +0.0029] | 4/1/0 | +0.0514 |
| Actor | hidden_mixing_frozen | combined - combined_constant | +0.0013 | [-0.0015, +0.0041] | 2/2/1 | +0.2577 |
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
| Roman-empire | hidden_mixing_frozen | feature_only - fixed | +0.0009 | [-0.0002, +0.0021] | 4/1/0 | +0.0917 |
| Roman-empire | hidden_mixing_frozen | reliability_only - fixed | +0.0035 | [+0.0022, +0.0049] | 5/0/0 | +0.0021 |
| Roman-empire | hidden_mixing_frozen | combined - fixed | +0.0033 | [+0.0008, +0.0058] | 4/0/1 | +0.0222 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0001 | [-0.0019, +0.0022] | 1/2/2 | +0.8590 |
| Roman-empire | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [-0.0007, +0.0008] | 2/1/2 | +0.9062 |
| Roman-empire | hidden_mixing_frozen | zero_reliability - fixed | -0.0000 | [-0.0010, +0.0009] | 2/0/3 | +0.9216 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled - fixed | +0.0001 | [-0.0030, +0.0031] | 2/0/3 | +0.9523 |
| Roman-empire | hidden_mixing_frozen | combined_constant - fixed | +0.0007 | [-0.0006, +0.0020] | 3/2/0 | +0.2254 |
| Roman-empire | hidden_mixing_frozen | reliability_only - feature_only | +0.0026 | [+0.0006, +0.0047] | 5/0/0 | +0.0241 |
| Roman-empire | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0034 | [+0.0007, +0.0061] | 5/0/0 | +0.0252 |
| Roman-empire | hidden_mixing_frozen | true reliability - constant reliability | +0.0035 | [+0.0015, +0.0055] | 5/0/0 | +0.0078 |
| Roman-empire | hidden_mixing_frozen | true reliability - zero reliability | +0.0036 | [+0.0015, +0.0056] | 5/0/0 | +0.0084 |
| Roman-empire | hidden_mixing_frozen | combined - feature_only | +0.0024 | [+0.0001, +0.0046] | 4/0/1 | +0.0421 |
| Roman-empire | hidden_mixing_frozen | combined - combined_shuffled | +0.0032 | [-0.0005, +0.0069] | 5/0/0 | +0.0727 |
| Roman-empire | hidden_mixing_frozen | combined - combined_constant | +0.0026 | [+0.0003, +0.0049] | 4/0/1 | +0.0342 |
| Roman-empire | hidden_mixing_finetune | feature_only - fixed | -0.0012 | [-0.0050, +0.0025] | 1/1/3 | +0.4140 |
| Roman-empire | hidden_mixing_finetune | reliability_only - fixed | +0.0095 | [+0.0025, +0.0165] | 5/0/0 | +0.0198 |
| Roman-empire | hidden_mixing_finetune | combined - fixed | +0.0108 | [+0.0028, +0.0187] | 5/0/0 | +0.0197 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0005 | [-0.0021, +0.0030] | 3/1/1 | +0.6481 |
| Roman-empire | hidden_mixing_finetune | constant_reliability - fixed | -0.0004 | [-0.0037, +0.0029] | 2/1/2 | +0.7577 |
| Roman-empire | hidden_mixing_finetune | zero_reliability - fixed | -0.0002 | [-0.0057, +0.0052] | 1/0/4 | +0.9053 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled - fixed | +0.0010 | [-0.0034, +0.0053] | 3/0/2 | +0.5741 |
| Roman-empire | hidden_mixing_finetune | combined_constant - fixed | +0.0008 | [-0.0026, +0.0042] | 2/0/3 | +0.5601 |
| Roman-empire | hidden_mixing_finetune | reliability_only - feature_only | +0.0107 | [+0.0053, +0.0161] | 5/0/0 | +0.0052 |
| Roman-empire | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0090 | [+0.0035, +0.0145] | 5/0/0 | +0.0105 |
| Roman-empire | hidden_mixing_finetune | true reliability - constant reliability | +0.0098 | [+0.0050, +0.0147] | 5/0/0 | +0.0048 |
| Roman-empire | hidden_mixing_finetune | true reliability - zero reliability | +0.0097 | [+0.0035, +0.0160] | 5/0/0 | +0.0125 |
| Roman-empire | hidden_mixing_finetune | combined - feature_only | +0.0120 | [+0.0062, +0.0178] | 5/0/0 | +0.0045 |
| Roman-empire | hidden_mixing_finetune | combined - combined_shuffled | +0.0098 | [+0.0058, +0.0138] | 5/0/0 | +0.0024 |
| Roman-empire | hidden_mixing_finetune | combined - combined_constant | +0.0100 | [+0.0052, +0.0148] | 5/0/0 | +0.0045 |
| Amazon-ratings | hidden_mixing_frozen | feature_only - fixed | -0.0014 | [-0.0041, +0.0013] | 0/1/4 | +0.2195 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - fixed | -0.0007 | [-0.0016, +0.0003] | 0/2/3 | +0.1260 |
| Amazon-ratings | hidden_mixing_frozen | combined - fixed | -0.0016 | [-0.0044, +0.0012] | 0/1/4 | +0.1877 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0003 | [-0.0016, +0.0010] | 2/1/2 | +0.6074 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability - fixed | -0.0001 | [-0.0012, +0.0011] | 2/1/2 | +0.8807 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability - fixed | -0.0000 | [-0.0009, +0.0009] | 2/1/2 | +0.9246 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled - fixed | -0.0004 | [-0.0014, +0.0006] | 1/1/3 | +0.3375 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant - fixed | -0.0015 | [-0.0046, +0.0016] | 1/2/2 | +0.2599 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - feature_only | +0.0008 | [-0.0021, +0.0036] | 2/1/2 | +0.5046 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0004 | [-0.0010, +0.0002] | 0/2/3 | +0.1533 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - constant reliability | -0.0006 | [-0.0011, -0.0000] | 0/1/4 | +0.0408 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - zero reliability | -0.0006 | [-0.0011, -0.0001] | 0/1/4 | +0.0236 |
| Amazon-ratings | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0010, +0.0006] | 2/1/2 | +0.5354 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_shuffled | -0.0012 | [-0.0046, +0.0022] | 1/2/2 | +0.3816 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_constant | -0.0001 | [-0.0006, +0.0003] | 1/1/3 | +0.4557 |
| Amazon-ratings | hidden_mixing_finetune | feature_only - fixed | -0.0015 | [-0.0126, +0.0097] | 2/0/3 | +0.7326 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - fixed | -0.0026 | [-0.0118, +0.0065] | 2/1/2 | +0.4658 |
| Amazon-ratings | hidden_mixing_finetune | combined - fixed | -0.0011 | [-0.0128, +0.0105] | 3/0/2 | +0.7988 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0020 | [-0.0120, +0.0081] | 3/0/2 | +0.6162 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability - fixed | -0.0026 | [-0.0118, +0.0066] | 3/0/2 | +0.4786 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability - fixed | -0.0028 | [-0.0133, +0.0076] | 3/0/2 | +0.4923 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled - fixed | -0.0029 | [-0.0145, +0.0088] | 2/0/3 | +0.5302 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant - fixed | -0.0011 | [-0.0117, +0.0095] | 3/0/2 | +0.7912 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - feature_only | -0.0012 | [-0.0077, +0.0054] | 1/2/2 | +0.6442 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0007 | [-0.0039, +0.0025] | 2/2/1 | +0.5846 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - constant reliability | -0.0001 | [-0.0004, +0.0002] | 1/3/1 | +0.5870 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - zero reliability | +0.0002 | [-0.0039, +0.0043] | 1/2/2 | +0.9018 |
| Amazon-ratings | hidden_mixing_finetune | combined - feature_only | +0.0003 | [-0.0048, +0.0054] | 1/2/2 | +0.8672 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_shuffled | +0.0017 | [-0.0017, +0.0052] | 2/2/1 | +0.2329 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_constant | -0.0001 | [-0.0038, +0.0037] | 2/2/1 | +0.9635 |
| Cora | hidden_protocol | fixed: finetune - frozen | +0.0172 | [-0.0002, +0.0346] | 5/0/0 | +0.0518 |
| Cora | hidden_protocol | feature_only: finetune - frozen | +0.0122 | [-0.0079, +0.0323] | 3/2/0 | +0.1676 |
| Cora | hidden_protocol | reliability_only: finetune - frozen | +0.0124 | [-0.0075, +0.0323] | 3/2/0 | +0.1589 |
| Cora | hidden_protocol | combined: finetune - frozen | +0.0170 | [-0.0073, +0.0413] | 3/2/0 | +0.1240 |
| Cora | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0138 | [-0.0071, +0.0347] | 3/2/0 | +0.1401 |
| Cora | hidden_protocol | constant_reliability: finetune - frozen | +0.0144 | [-0.0063, +0.0351] | 3/2/0 | +0.1258 |
| Cora | hidden_protocol | zero_reliability: finetune - frozen | +0.0122 | [-0.0079, +0.0323] | 3/2/0 | +0.1676 |
| Cora | hidden_protocol | combined_shuffled: finetune - frozen | +0.0120 | [-0.0084, +0.0324] | 3/2/0 | +0.1781 |
| Cora | hidden_protocol | combined_constant: finetune - frozen | +0.0118 | [-0.0086, +0.0322] | 3/2/0 | +0.1844 |
| Citeseer | hidden_protocol | fixed: finetune - frozen | +0.0024 | [-0.0043, +0.0091] | 1/4/0 | +0.3739 |
| Citeseer | hidden_protocol | feature_only: finetune - frozen | -0.0012 | [-0.0039, +0.0015] | 0/3/2 | +0.2835 |
| Citeseer | hidden_protocol | reliability_only: finetune - frozen | +0.0022 | [-0.0105, +0.0149] | 2/2/1 | +0.6558 |
| Citeseer | hidden_protocol | combined: finetune - frozen | -0.0014 | [-0.0046, +0.0018] | 0/3/2 | +0.2962 |
| Citeseer | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0026 | [-0.0151, +0.0203] | 2/1/2 | +0.7043 |
| Citeseer | hidden_protocol | constant_reliability: finetune - frozen | +0.0016 | [-0.0148, +0.0180] | 2/2/1 | +0.7998 |
| Citeseer | hidden_protocol | zero_reliability: finetune - frozen | +0.0024 | [-0.0114, +0.0162] | 2/1/2 | +0.6548 |
| Citeseer | hidden_protocol | combined_shuffled: finetune - frozen | -0.0006 | [-0.0017, +0.0005] | 0/3/2 | +0.2080 |
| Citeseer | hidden_protocol | combined_constant: finetune - frozen | -0.0020 | [-0.0062, +0.0022] | 0/2/3 | +0.2577 |
| Pubmed | hidden_protocol | fixed: finetune - frozen | +0.0012 | [-0.0021, +0.0045] | 1/4/0 | +0.3739 |
| Pubmed | hidden_protocol | feature_only: finetune - frozen | -0.0052 | [-0.0141, +0.0037] | 0/3/2 | +0.1795 |
| Pubmed | hidden_protocol | reliability_only: finetune - frozen | -0.0028 | [-0.0093, +0.0037] | 0/3/2 | +0.2962 |
| Pubmed | hidden_protocol | combined: finetune - frozen | -0.0044 | [-0.0125, +0.0037] | 1/2/2 | +0.2049 |
| Pubmed | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0038 | [-0.0123, +0.0047] | 1/1/3 | +0.2838 |
| Pubmed | hidden_protocol | constant_reliability: finetune - frozen | -0.0044 | [-0.0119, +0.0031] | 0/3/2 | +0.1802 |
| Pubmed | hidden_protocol | zero_reliability: finetune - frozen | -0.0046 | [-0.0124, +0.0032] | 0/3/2 | +0.1783 |
| Pubmed | hidden_protocol | combined_shuffled: finetune - frozen | -0.0046 | [-0.0124, +0.0032] | 0/3/2 | +0.1783 |
| Pubmed | hidden_protocol | combined_constant: finetune - frozen | -0.0020 | [-0.0090, +0.0050] | 1/3/1 | +0.4734 |
| Chameleon | hidden_protocol | fixed: finetune - frozen | +0.0004 | [-0.0008, +0.0017] | 1/4/0 | +0.3739 |
| Chameleon | hidden_protocol | feature_only: finetune - frozen | -0.0026 | [-0.0178, +0.0126] | 3/1/1 | +0.6560 |
| Chameleon | hidden_protocol | reliability_only: finetune - frozen | -0.0039 | [-0.0192, +0.0113] | 1/2/2 | +0.5110 |
| Chameleon | hidden_protocol | combined: finetune - frozen | -0.0018 | [-0.0210, +0.0175] | 1/1/3 | +0.8131 |
| Chameleon | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0013 | [-0.0175, +0.0149] | 3/1/1 | +0.8324 |
| Chameleon | hidden_protocol | constant_reliability: finetune - frozen | -0.0035 | [-0.0180, +0.0110] | 2/2/1 | +0.5381 |
| Chameleon | hidden_protocol | zero_reliability: finetune - frozen | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_protocol | combined_shuffled: finetune - frozen | -0.0000 | [-0.0181, +0.0181] | 4/0/1 | +1.0000 |
| Chameleon | hidden_protocol | combined_constant: finetune - frozen | -0.0000 | [-0.0190, +0.0190] | 2/2/1 | +1.0000 |
| Squirrel | hidden_protocol | fixed: finetune - frozen | -0.0046 | [-0.0120, +0.0028] | 0/2/3 | +0.1596 |
| Squirrel | hidden_protocol | feature_only: finetune - frozen | -0.0023 | [-0.0087, +0.0040] | 2/0/3 | +0.3701 |
| Squirrel | hidden_protocol | reliability_only: finetune - frozen | -0.0025 | [-0.0113, +0.0063] | 2/1/2 | +0.4743 |
| Squirrel | hidden_protocol | combined: finetune - frozen | -0.0029 | [-0.0129, +0.0071] | 2/0/3 | +0.4676 |
| Squirrel | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0060 | [-0.0163, +0.0044] | 0/3/2 | +0.1851 |
| Squirrel | hidden_protocol | constant_reliability: finetune - frozen | -0.0040 | [-0.0141, +0.0060] | 2/0/3 | +0.3281 |
| Squirrel | hidden_protocol | zero_reliability: finetune - frozen | -0.0050 | [-0.0164, +0.0064] | 2/0/3 | +0.2892 |
| Squirrel | hidden_protocol | combined_shuffled: finetune - frozen | -0.0037 | [-0.0147, +0.0074] | 2/0/3 | +0.4106 |
| Squirrel | hidden_protocol | combined_constant: finetune - frozen | -0.0035 | [-0.0139, +0.0070] | 2/0/3 | +0.4089 |
| Actor | hidden_protocol | fixed: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_protocol | feature_only: finetune - frozen | +0.0021 | [-0.0006, +0.0048] | 4/1/0 | +0.0940 |
| Actor | hidden_protocol | reliability_only: finetune - frozen | +0.0003 | [-0.0024, +0.0029] | 1/1/3 | +0.7943 |
| Actor | hidden_protocol | combined: finetune - frozen | +0.0004 | [-0.0022, +0.0030] | 1/2/2 | +0.6903 |
| Actor | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0020 | [-0.0021, +0.0060] | 3/0/2 | +0.2468 |
| Actor | hidden_protocol | constant_reliability: finetune - frozen | +0.0008 | [-0.0014, +0.0030] | 1/4/0 | +0.3739 |
| Actor | hidden_protocol | zero_reliability: finetune - frozen | +0.0008 | [-0.0014, +0.0030] | 1/4/0 | +0.3739 |
| Actor | hidden_protocol | combined_shuffled: finetune - frozen | +0.0018 | [-0.0015, +0.0052] | 3/2/0 | +0.2056 |
| Actor | hidden_protocol | combined_constant: finetune - frozen | +0.0017 | [-0.0032, +0.0066] | 2/2/1 | +0.3862 |
| Roman-empire | hidden_protocol | fixed: finetune - frozen | +0.0047 | [-0.0002, +0.0096] | 4/1/0 | +0.0573 |
| Roman-empire | hidden_protocol | feature_only: finetune - frozen | +0.0025 | [-0.0020, +0.0070] | 3/1/1 | +0.1991 |
| Roman-empire | hidden_protocol | reliability_only: finetune - frozen | +0.0106 | [+0.0079, +0.0133] | 5/0/0 | +0.0004 |
| Roman-empire | hidden_protocol | combined: finetune - frozen | +0.0121 | [+0.0074, +0.0169] | 5/0/0 | +0.0021 |
| Roman-empire | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0050 | [+0.0020, +0.0080] | 5/0/0 | +0.0100 |
| Roman-empire | hidden_protocol | constant_reliability: finetune - frozen | +0.0042 | [+0.0007, +0.0077] | 5/0/0 | +0.0286 |
| Roman-empire | hidden_protocol | zero_reliability: finetune - frozen | +0.0044 | [-0.0012, +0.0101] | 4/0/1 | +0.0946 |
| Roman-empire | hidden_protocol | combined_shuffled: finetune - frozen | +0.0055 | [+0.0018, +0.0093] | 5/0/0 | +0.0152 |
| Roman-empire | hidden_protocol | combined_constant: finetune - frozen | +0.0048 | [+0.0012, +0.0083] | 5/0/0 | +0.0209 |
| Amazon-ratings | hidden_protocol | fixed: finetune - frozen | +0.0067 | [-0.0029, +0.0162] | 3/2/0 | +0.1248 |
| Amazon-ratings | hidden_protocol | feature_only: finetune - frozen | +0.0066 | [-0.0010, +0.0142] | 4/1/0 | +0.0737 |
| Amazon-ratings | hidden_protocol | reliability_only: finetune - frozen | +0.0047 | [-0.0024, +0.0118] | 4/1/0 | +0.1411 |
| Amazon-ratings | hidden_protocol | combined: finetune - frozen | +0.0071 | [-0.0007, +0.0149] | 4/1/0 | +0.0643 |
| Amazon-ratings | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0050 | [-0.0014, +0.0113] | 4/1/0 | +0.0963 |
| Amazon-ratings | hidden_protocol | constant_reliability: finetune - frozen | +0.0041 | [-0.0026, +0.0109] | 3/2/0 | +0.1609 |
| Amazon-ratings | hidden_protocol | zero_reliability: finetune - frozen | +0.0039 | [-0.0007, +0.0084] | 3/2/0 | +0.0802 |
| Amazon-ratings | hidden_protocol | combined_shuffled: finetune - frozen | +0.0042 | [-0.0010, +0.0094] | 4/1/0 | +0.0900 |
| Amazon-ratings | hidden_protocol | combined_constant: finetune - frozen | +0.0071 | [-0.0008, +0.0149] | 4/1/0 | +0.0672 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
