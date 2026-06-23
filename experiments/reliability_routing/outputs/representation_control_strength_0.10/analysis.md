# Representation Control Screening

- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor, Roman-empire, Amazon-ratings
- Families: hidden_mixing_frozen, hidden_mixing_finetune
- Runs: 5
- Edge protocol: undirected
- Max adjustment: 0.1
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
| Actor | hidden_mixing_frozen | combined | 0.3633 | 0.3647 | -0.0014 | 0.0084 | 0.8307 | 0.0208 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_constant | 0.3637 | 0.3647 | -0.0011 | 0.0069 | 0.8340 | 0.0307 | 34948 | 0 |
| Actor | hidden_mixing_frozen | combined_shuffled | 0.3632 | 0.3647 | -0.0016 | 0.0075 | 0.8300 | 0.0216 | 34948 | 0 |
| Actor | hidden_mixing_frozen | constant_reliability | 0.3645 | 0.3647 | -0.0003 | 0.0073 | 0.8331 | 0.0176 | 26372 | 0 |
| Actor | hidden_mixing_frozen | feature_only | 0.3622 | 0.3647 | -0.0025 | 0.0066 | 0.8304 | 0.0204 | 25348 | 0 |
| Actor | hidden_mixing_frozen | fixed | 0.3647 | 0.3647 | +0.0000 | 0.0074 | 0.8500 | 0.0000 | 0 | 0 |
| Actor | hidden_mixing_frozen | reliability_only | 0.3649 | 0.3647 | +0.0001 | 0.0068 | 0.8358 | 0.0168 | 26372 | 0 |
| Actor | hidden_mixing_frozen | shuffled_reliability | 0.3637 | 0.3647 | -0.0011 | 0.0085 | 0.8270 | 0.0244 | 26372 | 0 |
| Actor | hidden_mixing_frozen | zero_reliability | 0.3645 | 0.3647 | -0.0003 | 0.0073 | 0.8332 | 0.0176 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_finetune | combined | 0.4761 | 0.4672 | +0.0089 | 0.0087 | 0.7576 | 0.0526 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant | 0.4734 | 0.4672 | +0.0062 | 0.0091 | 0.7579 | 0.0351 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled | 0.4725 | 0.4672 | +0.0054 | 0.0094 | 0.7605 | 0.0462 | 34948 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability | 0.4733 | 0.4672 | +0.0061 | 0.0090 | 0.7555 | 0.0235 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | feature_only | 0.4750 | 0.4672 | +0.0078 | 0.0082 | 0.7605 | 0.0434 | 25348 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | fixed | 0.4756 | 0.4672 | +0.0084 | 0.0110 | 0.7500 | 0.0000 | 0 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only | 0.4733 | 0.4672 | +0.0061 | 0.0088 | 0.7515 | 0.0343 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability | 0.4734 | 0.4672 | +0.0062 | 0.0099 | 0.7580 | 0.0366 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability | 0.4756 | 0.4672 | +0.0085 | 0.0080 | 0.7606 | 0.0336 | 26372 | 94853 |
| Amazon-ratings | hidden_mixing_frozen | combined | 0.4665 | 0.4672 | -0.0007 | 0.0034 | 0.7408 | 0.0210 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant | 0.4663 | 0.4672 | -0.0009 | 0.0042 | 0.7413 | 0.0190 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled | 0.4671 | 0.4672 | -0.0001 | 0.0039 | 0.7417 | 0.0106 | 34948 | 0 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability | 0.4672 | 0.4672 | +0.0000 | 0.0039 | 0.7456 | 0.0065 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | feature_only | 0.4667 | 0.4672 | -0.0005 | 0.0045 | 0.7394 | 0.0135 | 25348 | 0 |
| Amazon-ratings | hidden_mixing_frozen | fixed | 0.4672 | 0.4672 | +0.0000 | 0.0040 | 0.7500 | 0.0000 | 0 | 0 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only | 0.4667 | 0.4672 | -0.0005 | 0.0044 | 0.7438 | 0.0077 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability | 0.4670 | 0.4672 | -0.0002 | 0.0041 | 0.7469 | 0.0048 | 26372 | 0 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability | 0.4672 | 0.4672 | +0.0000 | 0.0039 | 0.7456 | 0.0064 | 26372 | 0 |
| Chameleon | hidden_mixing_finetune | combined | 0.5430 | 0.5434 | -0.0004 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_constant | 0.5425 | 0.5434 | -0.0009 | 0.0296 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_shuffled | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | constant_reliability | 0.5390 | 0.5434 | -0.0044 | 0.0302 | 0.7997 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | feature_only | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 25348 | 224453 |
| Chameleon | hidden_mixing_finetune | fixed | 0.5439 | 0.5434 | +0.0004 | 0.0314 | 0.8000 | 0.0000 | 0 | 224453 |
| Chameleon | hidden_mixing_finetune | reliability_only | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability | 0.5395 | 0.5434 | -0.0039 | 0.0301 | 0.7997 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | zero_reliability | 0.5417 | 0.5434 | -0.0018 | 0.0297 | 0.7998 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_frozen | combined | 0.5439 | 0.5434 | +0.0004 | 0.0310 | 0.7999 | 0.0292 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_constant | 0.5421 | 0.5434 | -0.0013 | 0.0326 | 0.7988 | 0.0144 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_shuffled | 0.5425 | 0.5434 | -0.0009 | 0.0346 | 0.7930 | 0.0161 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | constant_reliability | 0.5421 | 0.5434 | -0.0013 | 0.0326 | 0.7969 | 0.0065 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | feature_only | 0.5421 | 0.5434 | -0.0013 | 0.0326 | 0.7969 | 0.0064 | 25348 | 0 |
| Chameleon | hidden_mixing_frozen | fixed | 0.5434 | 0.5434 | +0.0000 | 0.0316 | 0.8000 | 0.0000 | 0 | 0 |
| Chameleon | hidden_mixing_frozen | reliability_only | 0.5447 | 0.5434 | +0.0013 | 0.0307 | 0.8001 | 0.0292 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0349 | 0.7938 | 0.0130 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | zero_reliability | 0.5425 | 0.5434 | -0.0009 | 0.0320 | 0.7970 | 0.0063 | 26372 | 0 |
| Citeseer | hidden_mixing_finetune | combined | 0.6118 | 0.6144 | -0.0026 | 0.0226 | 0.7547 | 0.0109 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_constant | 0.6132 | 0.6144 | -0.0012 | 0.0229 | 0.7498 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_shuffled | 0.6118 | 0.6144 | -0.0026 | 0.0226 | 0.7547 | 0.0109 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | constant_reliability | 0.6178 | 0.6144 | +0.0034 | 0.0171 | 0.7498 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | feature_only | 0.6118 | 0.6144 | -0.0026 | 0.0226 | 0.7547 | 0.0109 | 25348 | 312710 |
| Citeseer | hidden_mixing_finetune | fixed | 0.6168 | 0.6144 | +0.0024 | 0.0217 | 0.7500 | 0.0000 | 0 | 312710 |
| Citeseer | hidden_mixing_finetune | reliability_only | 0.6158 | 0.6144 | +0.0014 | 0.0176 | 0.7548 | 0.0109 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability | 0.6170 | 0.6144 | +0.0026 | 0.0166 | 0.7548 | 0.0109 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | zero_reliability | 0.6174 | 0.6144 | +0.0030 | 0.0175 | 0.7498 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_frozen | combined | 0.6150 | 0.6144 | +0.0006 | 0.0238 | 0.7387 | 0.0157 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_constant | 0.6146 | 0.6144 | +0.0002 | 0.0234 | 0.7492 | 0.0019 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_shuffled | 0.6142 | 0.6144 | -0.0002 | 0.0230 | 0.7506 | 0.0045 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | constant_reliability | 0.6140 | 0.6144 | -0.0004 | 0.0235 | 0.7491 | 0.0020 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | feature_only | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7494 | 0.0016 | 25348 | 0 |
| Citeseer | hidden_mixing_frozen | fixed | 0.6144 | 0.6144 | +0.0000 | 0.0231 | 0.7500 | 0.0000 | 0 | 0 |
| Citeseer | hidden_mixing_frozen | reliability_only | 0.6144 | 0.6144 | +0.0000 | 0.0239 | 0.7400 | 0.0141 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability | 0.6142 | 0.6144 | -0.0002 | 0.0237 | 0.7492 | 0.0019 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | zero_reliability | 0.6142 | 0.6144 | -0.0002 | 0.0237 | 0.7491 | 0.0020 | 26372 | 0 |
| Cora | hidden_mixing_finetune | combined | 0.7076 | 0.6872 | +0.0204 | 0.0198 | 0.7996 | 0.0011 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_constant | 0.6990 | 0.6872 | +0.0118 | 0.0151 | 0.7997 | 0.0010 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_shuffled | 0.7028 | 0.6872 | +0.0156 | 0.0151 | 0.7994 | 0.0014 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | constant_reliability | 0.7048 | 0.6872 | +0.0176 | 0.0160 | 0.7998 | 0.0008 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | feature_only | 0.6994 | 0.6872 | +0.0122 | 0.0151 | 0.7996 | 0.0010 | 25348 | 167495 |
| Cora | hidden_mixing_finetune | fixed | 0.7046 | 0.6872 | +0.0174 | 0.0101 | 0.8000 | 0.0000 | 0 | 167495 |
| Cora | hidden_mixing_finetune | reliability_only | 0.6996 | 0.6872 | +0.0124 | 0.0146 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | shuffled_reliability | 0.6990 | 0.6872 | +0.0118 | 0.0152 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | zero_reliability | 0.6994 | 0.6872 | +0.0122 | 0.0148 | 0.7997 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_frozen | combined | 0.6870 | 0.6872 | -0.0002 | 0.0116 | 0.7977 | 0.0039 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_constant | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_shuffled | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | constant_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | feature_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 25348 | 0 |
| Cora | hidden_mixing_frozen | fixed | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.8000 | 0.0000 | 0 | 0 |
| Cora | hidden_mixing_frozen | reliability_only | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7917 | 0.0117 | 26372 | 0 |
| Cora | hidden_mixing_frozen | shuffled_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | zero_reliability | 0.6872 | 0.6872 | +0.0000 | 0.0116 | 0.7997 | 0.0010 | 26372 | 0 |
| Pubmed | hidden_mixing_finetune | combined | 0.7304 | 0.7344 | -0.0040 | 0.0106 | 0.8422 | 0.0108 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_constant | 0.7304 | 0.7344 | -0.0040 | 0.0106 | 0.8422 | 0.0108 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | combined_shuffled | 0.7300 | 0.7344 | -0.0044 | 0.0109 | 0.8422 | 0.0108 | 34948 | 107523 |
| Pubmed | hidden_mixing_finetune | constant_reliability | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8431 | 0.0096 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | feature_only | 0.7310 | 0.7344 | -0.0034 | 0.0101 | 0.8464 | 0.0054 | 25348 | 107523 |
| Pubmed | hidden_mixing_finetune | fixed | 0.7356 | 0.7344 | +0.0012 | 0.0138 | 0.8500 | 0.0000 | 0 | 107523 |
| Pubmed | hidden_mixing_finetune | reliability_only | 0.7330 | 0.7344 | -0.0014 | 0.0097 | 0.8422 | 0.0108 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability | 0.7302 | 0.7344 | -0.0042 | 0.0107 | 0.8423 | 0.0107 | 26372 | 107523 |
| Pubmed | hidden_mixing_finetune | zero_reliability | 0.7300 | 0.7344 | -0.0044 | 0.0109 | 0.8425 | 0.0104 | 26372 | 107523 |
| Pubmed | hidden_mixing_frozen | combined | 0.7342 | 0.7344 | -0.0002 | 0.0124 | 0.8487 | 0.0038 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_constant | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8477 | 0.0039 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | combined_shuffled | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8480 | 0.0034 | 34948 | 0 |
| Pubmed | hidden_mixing_frozen | constant_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8476 | 0.0038 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | feature_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8484 | 0.0026 | 25348 | 0 |
| Pubmed | hidden_mixing_frozen | fixed | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8500 | 0.0000 | 0 | 0 |
| Pubmed | hidden_mixing_frozen | reliability_only | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8489 | 0.0019 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0116 | 0.8367 | 0.0148 | 26372 | 0 |
| Pubmed | hidden_mixing_frozen | zero_reliability | 0.7344 | 0.7344 | +0.0000 | 0.0121 | 0.8478 | 0.0035 | 26372 | 0 |
| Roman-empire | hidden_mixing_finetune | combined | 0.8349 | 0.8199 | +0.0149 | 0.0033 | 0.7449 | 0.0309 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_constant | 0.8265 | 0.8199 | +0.0066 | 0.0031 | 0.7502 | 0.0034 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled | 0.8240 | 0.8199 | +0.0041 | 0.0042 | 0.7498 | 0.0053 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | constant_reliability | 0.8247 | 0.8199 | +0.0048 | 0.0036 | 0.7501 | 0.0013 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | feature_only | 0.8241 | 0.8199 | +0.0042 | 0.0040 | 0.7490 | 0.0025 | 25348 | 95698 |
| Roman-empire | hidden_mixing_finetune | fixed | 0.8230 | 0.8199 | +0.0030 | 0.0051 | 0.7500 | 0.0000 | 0 | 95698 |
| Roman-empire | hidden_mixing_finetune | reliability_only | 0.8344 | 0.8199 | +0.0144 | 0.0041 | 0.7424 | 0.0323 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability | 0.8237 | 0.8199 | +0.0037 | 0.0049 | 0.7499 | 0.0033 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | zero_reliability | 0.8255 | 0.8199 | +0.0056 | 0.0023 | 0.7502 | 0.0017 | 26372 | 95698 |
| Roman-empire | hidden_mixing_frozen | combined | 0.8240 | 0.8199 | +0.0041 | 0.0049 | 0.7531 | 0.0667 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_constant | 0.8203 | 0.8199 | +0.0004 | 0.0037 | 0.7560 | 0.0372 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled | 0.8209 | 0.8199 | +0.0010 | 0.0051 | 0.7561 | 0.0349 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | constant_reliability | 0.8202 | 0.8199 | +0.0002 | 0.0037 | 0.7571 | 0.0304 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | feature_only | 0.8211 | 0.8199 | +0.0012 | 0.0044 | 0.7554 | 0.0386 | 25348 | 0 |
| Roman-empire | hidden_mixing_frozen | fixed | 0.8199 | 0.8199 | +0.0000 | 0.0032 | 0.7500 | 0.0000 | 0 | 0 |
| Roman-empire | hidden_mixing_frozen | reliability_only | 0.8232 | 0.8199 | +0.0032 | 0.0034 | 0.7560 | 0.0411 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability | 0.8198 | 0.8199 | -0.0001 | 0.0035 | 0.7580 | 0.0362 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | zero_reliability | 0.8203 | 0.8199 | +0.0004 | 0.0036 | 0.7562 | 0.0265 | 26372 | 0 |
| Squirrel | hidden_mixing_finetune | combined | 0.3462 | 0.3500 | -0.0038 | 0.0203 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_constant | 0.3460 | 0.3500 | -0.0040 | 0.0201 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_shuffled | 0.3458 | 0.3500 | -0.0042 | 0.0206 | 0.7498 | 0.0008 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | constant_reliability | 0.3474 | 0.3500 | -0.0027 | 0.0198 | 0.7498 | 0.0010 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | feature_only | 0.3474 | 0.3500 | -0.0027 | 0.0179 | 0.7498 | 0.0008 | 25348 | 209349 |
| Squirrel | hidden_mixing_finetune | fixed | 0.3462 | 0.3500 | -0.0038 | 0.0159 | 0.7500 | 0.0000 | 0 | 209349 |
| Squirrel | hidden_mixing_finetune | reliability_only | 0.3458 | 0.3500 | -0.0042 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | zero_reliability | 0.3454 | 0.3500 | -0.0046 | 0.0204 | 0.7498 | 0.0008 | 26372 | 209349 |
| Squirrel | hidden_mixing_frozen | combined | 0.3485 | 0.3500 | -0.0015 | 0.0158 | 0.7392 | 0.0177 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_constant | 0.3504 | 0.3500 | +0.0004 | 0.0154 | 0.7481 | 0.0132 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_shuffled | 0.3510 | 0.3500 | +0.0010 | 0.0150 | 0.7484 | 0.0136 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | constant_reliability | 0.3504 | 0.3500 | +0.0004 | 0.0154 | 0.7478 | 0.0137 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | feature_only | 0.3510 | 0.3500 | +0.0010 | 0.0164 | 0.7487 | 0.0128 | 25348 | 0 |
| Squirrel | hidden_mixing_frozen | fixed | 0.3500 | 0.3500 | +0.0000 | 0.0155 | 0.7500 | 0.0000 | 0 | 0 |
| Squirrel | hidden_mixing_frozen | reliability_only | 0.3500 | 0.3500 | +0.0000 | 0.0152 | 0.7405 | 0.0326 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability | 0.3499 | 0.3500 | -0.0002 | 0.0158 | 0.7462 | 0.0253 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | zero_reliability | 0.3504 | 0.3500 | +0.0004 | 0.0154 | 0.7479 | 0.0141 | 26372 | 0 |

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
| Cora | hidden_mixing_finetune | feature_only - fixed | -0.0052 | [-0.0304, +0.0200] | 2/0/3 | +0.5971 |
| Cora | hidden_mixing_finetune | reliability_only - fixed | -0.0050 | [-0.0291, +0.0191] | 2/0/3 | +0.5951 |
| Cora | hidden_mixing_finetune | combined - fixed | +0.0030 | [-0.0355, +0.0415] | 2/0/3 | +0.8393 |
| Cora | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0056 | [-0.0293, +0.0181] | 2/0/3 | +0.5471 |
| Cora | hidden_mixing_finetune | constant_reliability - fixed | +0.0002 | [-0.0317, +0.0321] | 2/0/3 | +0.9869 |
| Cora | hidden_mixing_finetune | zero_reliability - fixed | -0.0052 | [-0.0297, +0.0193] | 2/0/3 | +0.5875 |
| Cora | hidden_mixing_finetune | combined_shuffled - fixed | -0.0018 | [-0.0306, +0.0270] | 2/0/3 | +0.8704 |
| Cora | hidden_mixing_finetune | combined_constant - fixed | -0.0056 | [-0.0287, +0.0175] | 2/0/3 | +0.5373 |
| Cora | hidden_mixing_finetune | reliability_only - feature_only | +0.0002 | [-0.0012, +0.0016] | 1/3/1 | +0.7040 |
| Cora | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0006 | [-0.0018, +0.0030] | 1/3/1 | +0.5291 |
| Cora | hidden_mixing_finetune | true reliability - constant reliability | -0.0052 | [-0.0190, +0.0086] | 0/3/2 | +0.3531 |
| Cora | hidden_mixing_finetune | true reliability - zero reliability | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Cora | hidden_mixing_finetune | combined - feature_only | +0.0082 | [-0.0125, +0.0289] | 3/2/0 | +0.3334 |
| Cora | hidden_mixing_finetune | combined - combined_shuffled | +0.0048 | [-0.0085, +0.0181] | 1/4/0 | +0.3739 |
| Cora | hidden_mixing_finetune | combined - combined_constant | +0.0086 | [-0.0160, +0.0332] | 1/3/1 | +0.3863 |
| Citeseer | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [-0.0018, +0.0018] | 1/3/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | combined - fixed | +0.0006 | [-0.0011, +0.0023] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0002 | [-0.0016, +0.0012] | 1/3/1 | +0.7040 |
| Citeseer | hidden_mixing_frozen | constant_reliability - fixed | -0.0004 | [-0.0015, +0.0007] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | zero_reliability - fixed | -0.0002 | [-0.0016, +0.0012] | 1/3/1 | +0.7040 |
| Citeseer | hidden_mixing_frozen | combined_shuffled - fixed | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined_constant - fixed | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [-0.0018, +0.0018] | 1/3/1 | +1.0000 |
| Citeseer | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | true reliability - constant reliability | +0.0004 | [-0.0007, +0.0015] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | true reliability - zero reliability | +0.0002 | [-0.0004, +0.0008] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined - feature_only | +0.0006 | [-0.0011, +0.0023] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_frozen | combined - combined_shuffled | +0.0008 | [-0.0008, +0.0024] | 2/3/0 | +0.2420 |
| Citeseer | hidden_mixing_frozen | combined - combined_constant | +0.0004 | [-0.0007, +0.0015] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_finetune | feature_only - fixed | -0.0050 | [-0.0135, +0.0035] | 0/3/2 | +0.1783 |
| Citeseer | hidden_mixing_finetune | reliability_only - fixed | -0.0010 | [-0.0175, +0.0155] | 1/2/2 | +0.8747 |
| Citeseer | hidden_mixing_finetune | combined - fixed | -0.0050 | [-0.0135, +0.0035] | 0/3/2 | +0.1783 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0002 | [-0.0193, +0.0197] | 1/2/2 | +0.9787 |
| Citeseer | hidden_mixing_finetune | constant_reliability - fixed | +0.0010 | [-0.0156, +0.0176] | 1/2/2 | +0.8755 |
| Citeseer | hidden_mixing_finetune | zero_reliability - fixed | +0.0006 | [-0.0150, +0.0162] | 1/2/2 | +0.9202 |
| Citeseer | hidden_mixing_finetune | combined_shuffled - fixed | -0.0050 | [-0.0135, +0.0035] | 0/3/2 | +0.1783 |
| Citeseer | hidden_mixing_finetune | combined_constant - fixed | -0.0036 | [-0.0107, +0.0035] | 0/3/2 | +0.2296 |
| Citeseer | hidden_mixing_finetune | reliability_only - feature_only | +0.0040 | [-0.0071, +0.0151] | 1/4/0 | +0.3739 |
| Citeseer | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0012 | [-0.0045, +0.0021] | 0/4/1 | +0.3739 |
| Citeseer | hidden_mixing_finetune | true reliability - constant reliability | -0.0020 | [-0.0058, +0.0018] | 0/3/2 | +0.2204 |
| Citeseer | hidden_mixing_finetune | true reliability - zero reliability | -0.0016 | [-0.0054, +0.0022] | 0/3/2 | +0.3058 |
| Citeseer | hidden_mixing_finetune | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Citeseer | hidden_mixing_finetune | combined - combined_constant | -0.0014 | [-0.0053, +0.0025] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - fixed | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [-0.0009, +0.0009] | 1/3/1 | +1.0000 |
| Pubmed | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [-0.0009, +0.0009] | 1/3/1 | +1.0000 |
| Pubmed | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Pubmed | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | combined - combined_shuffled | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_frozen | combined - combined_constant | -0.0002 | [-0.0008, +0.0004] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_finetune | feature_only - fixed | -0.0046 | [-0.0143, +0.0051] | 0/3/2 | +0.2576 |
| Pubmed | hidden_mixing_finetune | reliability_only - fixed | -0.0026 | [-0.0136, +0.0084] | 1/3/1 | +0.5483 |
| Pubmed | hidden_mixing_finetune | combined - fixed | -0.0052 | [-0.0151, +0.0047] | 0/3/2 | +0.2174 |
| Pubmed | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | constant_reliability - fixed | -0.0054 | [-0.0154, +0.0046] | 0/3/2 | +0.2080 |
| Pubmed | hidden_mixing_finetune | zero_reliability - fixed | -0.0056 | [-0.0157, +0.0045] | 0/3/2 | +0.2003 |
| Pubmed | hidden_mixing_finetune | combined_shuffled - fixed | -0.0056 | [-0.0157, +0.0045] | 0/3/2 | +0.2003 |
| Pubmed | hidden_mixing_finetune | combined_constant - fixed | -0.0052 | [-0.0151, +0.0047] | 0/3/2 | +0.2174 |
| Pubmed | hidden_mixing_finetune | reliability_only - feature_only | +0.0020 | [-0.0036, +0.0076] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0028 | [-0.0050, +0.0106] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - constant reliability | +0.0028 | [-0.0050, +0.0106] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | true reliability - zero reliability | +0.0030 | [-0.0053, +0.0113] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - feature_only | -0.0006 | [-0.0023, +0.0011] | 0/4/1 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - combined_shuffled | +0.0004 | [-0.0007, +0.0015] | 1/4/0 | +0.3739 |
| Pubmed | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Chameleon | hidden_mixing_frozen | feature_only - fixed | -0.0013 | [-0.0038, +0.0011] | 0/3/2 | +0.2080 |
| Chameleon | hidden_mixing_frozen | reliability_only - fixed | +0.0013 | [-0.0028, +0.0054] | 2/2/1 | +0.4263 |
| Chameleon | hidden_mixing_frozen | combined - fixed | +0.0004 | [-0.0018, +0.0027] | 2/2/1 | +0.6213 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0009 | [-0.0058, +0.0041] | 1/2/2 | +0.6483 |
| Chameleon | hidden_mixing_frozen | constant_reliability - fixed | -0.0013 | [-0.0038, +0.0011] | 0/3/2 | +0.2080 |
| Chameleon | hidden_mixing_frozen | zero_reliability - fixed | -0.0009 | [-0.0033, +0.0016] | 0/4/1 | +0.3739 |
| Chameleon | hidden_mixing_frozen | combined_shuffled - fixed | -0.0009 | [-0.0054, +0.0037] | 1/2/2 | +0.6213 |
| Chameleon | hidden_mixing_frozen | combined_constant - fixed | -0.0013 | [-0.0038, +0.0011] | 0/3/2 | +0.2080 |
| Chameleon | hidden_mixing_frozen | reliability_only - feature_only | +0.0026 | [-0.0009, +0.0062] | 3/2/0 | +0.1087 |
| Chameleon | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0022 | [-0.0045, +0.0089] | 2/2/1 | +0.4130 |
| Chameleon | hidden_mixing_frozen | true reliability - constant reliability | +0.0026 | [-0.0009, +0.0062] | 3/2/0 | +0.1087 |
| Chameleon | hidden_mixing_frozen | true reliability - zero reliability | +0.0022 | [-0.0011, +0.0055] | 3/2/0 | +0.1419 |
| Chameleon | hidden_mixing_frozen | combined - feature_only | +0.0018 | [-0.0005, +0.0040] | 3/2/0 | +0.0993 |
| Chameleon | hidden_mixing_frozen | combined - combined_shuffled | +0.0013 | [-0.0036, +0.0063] | 3/1/1 | +0.5012 |
| Chameleon | hidden_mixing_frozen | combined - combined_constant | +0.0018 | [-0.0005, +0.0040] | 3/2/0 | +0.0993 |
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
| Squirrel | hidden_mixing_frozen | feature_only - fixed | +0.0010 | [-0.0037, +0.0056] | 2/1/2 | +0.5946 |
| Squirrel | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [-0.0037, +0.0037] | 1/2/2 | +1.0000 |
| Squirrel | hidden_mixing_frozen | combined - fixed | -0.0015 | [-0.0037, +0.0006] | 0/2/3 | +0.1202 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0002 | [-0.0044, +0.0041] | 1/2/2 | +0.9062 |
| Squirrel | hidden_mixing_frozen | constant_reliability - fixed | +0.0004 | [-0.0044, +0.0052] | 2/1/2 | +0.8355 |
| Squirrel | hidden_mixing_frozen | zero_reliability - fixed | +0.0004 | [-0.0044, +0.0052] | 2/1/2 | +0.8355 |
| Squirrel | hidden_mixing_frozen | combined_shuffled - fixed | +0.0010 | [-0.0031, +0.0050] | 1/2/2 | +0.5457 |
| Squirrel | hidden_mixing_frozen | combined_constant - fixed | +0.0004 | [-0.0044, +0.0052] | 2/1/2 | +0.8355 |
| Squirrel | hidden_mixing_frozen | reliability_only - feature_only | -0.0010 | [-0.0036, +0.0017] | 1/1/3 | +0.3739 |
| Squirrel | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0002 | [-0.0032, +0.0036] | 1/2/2 | +0.8835 |
| Squirrel | hidden_mixing_frozen | true reliability - constant reliability | -0.0004 | [-0.0026, +0.0018] | 2/0/3 | +0.6483 |
| Squirrel | hidden_mixing_frozen | true reliability - zero reliability | -0.0004 | [-0.0026, +0.0018] | 2/0/3 | +0.6483 |
| Squirrel | hidden_mixing_frozen | combined - feature_only | -0.0025 | [-0.0057, +0.0007] | 1/0/4 | +0.0978 |
| Squirrel | hidden_mixing_frozen | combined - combined_shuffled | -0.0025 | [-0.0059, +0.0009] | 0/2/3 | +0.1138 |
| Squirrel | hidden_mixing_frozen | combined - combined_constant | -0.0019 | [-0.0052, +0.0013] | 1/1/3 | +0.1778 |
| Squirrel | hidden_mixing_finetune | feature_only - fixed | +0.0012 | [-0.0063, +0.0086] | 1/2/2 | +0.6885 |
| Squirrel | hidden_mixing_finetune | reliability_only - fixed | -0.0004 | [-0.0114, +0.0106] | 1/3/1 | +0.9273 |
| Squirrel | hidden_mixing_finetune | combined - fixed | +0.0000 | [-0.0111, +0.0111] | 2/2/1 | +1.0000 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0008 | [-0.0114, +0.0099] | 1/2/2 | +0.8510 |
| Squirrel | hidden_mixing_finetune | constant_reliability - fixed | +0.0012 | [-0.0101, +0.0124] | 2/2/1 | +0.7899 |
| Squirrel | hidden_mixing_finetune | zero_reliability - fixed | -0.0008 | [-0.0114, +0.0099] | 1/2/2 | +0.8510 |
| Squirrel | hidden_mixing_finetune | combined_shuffled - fixed | -0.0004 | [-0.0118, +0.0111] | 2/2/1 | +0.9303 |
| Squirrel | hidden_mixing_finetune | combined_constant - fixed | -0.0002 | [-0.0107, +0.0104] | 1/3/1 | +0.9621 |
| Squirrel | hidden_mixing_finetune | reliability_only - feature_only | -0.0015 | [-0.0080, +0.0049] | 1/3/1 | +0.5448 |
| Squirrel | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0004 | [-0.0014, +0.0022] | 1/3/1 | +0.5870 |
| Squirrel | hidden_mixing_finetune | true reliability - constant reliability | -0.0015 | [-0.0052, +0.0021] | 0/3/2 | +0.3058 |
| Squirrel | hidden_mixing_finetune | true reliability - zero reliability | +0.0004 | [-0.0014, +0.0022] | 1/3/1 | +0.5870 |
| Squirrel | hidden_mixing_finetune | combined - feature_only | -0.0012 | [-0.0082, +0.0059] | 1/3/1 | +0.6724 |
| Squirrel | hidden_mixing_finetune | combined - combined_shuffled | +0.0004 | [-0.0003, +0.0010] | 2/3/0 | +0.1778 |
| Squirrel | hidden_mixing_finetune | combined - combined_constant | +0.0002 | [-0.0011, +0.0015] | 1/3/1 | +0.7040 |
| Actor | hidden_mixing_frozen | feature_only - fixed | -0.0025 | [-0.0068, +0.0018] | 0/3/2 | +0.1786 |
| Actor | hidden_mixing_frozen | reliability_only - fixed | +0.0001 | [-0.0009, +0.0012] | 2/1/2 | +0.7489 |
| Actor | hidden_mixing_frozen | combined - fixed | -0.0014 | [-0.0059, +0.0030] | 1/3/1 | +0.4213 |
| Actor | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0011 | [-0.0045, +0.0024] | 1/2/2 | +0.4500 |
| Actor | hidden_mixing_frozen | constant_reliability - fixed | -0.0003 | [-0.0015, +0.0010] | 1/3/1 | +0.5870 |
| Actor | hidden_mixing_frozen | zero_reliability - fixed | -0.0003 | [-0.0015, +0.0010] | 1/3/1 | +0.5870 |
| Actor | hidden_mixing_frozen | combined_shuffled - fixed | -0.0016 | [-0.0048, +0.0016] | 0/3/2 | +0.2420 |
| Actor | hidden_mixing_frozen | combined_constant - fixed | -0.0011 | [-0.0045, +0.0023] | 1/2/2 | +0.4382 |
| Actor | hidden_mixing_frozen | reliability_only - feature_only | +0.0026 | [-0.0008, +0.0060] | 4/1/0 | +0.0993 |
| Actor | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0012 | [-0.0022, +0.0045] | 3/1/1 | +0.3804 |
| Actor | hidden_mixing_frozen | true reliability - constant reliability | +0.0004 | [-0.0005, +0.0013] | 3/1/1 | +0.3046 |
| Actor | hidden_mixing_frozen | true reliability - zero reliability | +0.0004 | [-0.0005, +0.0013] | 3/1/1 | +0.3046 |
| Actor | hidden_mixing_frozen | combined - feature_only | +0.0011 | [-0.0034, +0.0055] | 1/3/1 | +0.5448 |
| Actor | hidden_mixing_frozen | combined - combined_shuffled | +0.0001 | [-0.0019, +0.0022] | 1/3/1 | +0.8662 |
| Actor | hidden_mixing_frozen | combined - combined_constant | -0.0004 | [-0.0057, +0.0049] | 1/2/2 | +0.8466 |
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
| Roman-empire | hidden_mixing_frozen | feature_only - fixed | +0.0012 | [-0.0008, +0.0031] | 4/0/1 | +0.1717 |
| Roman-empire | hidden_mixing_frozen | reliability_only - fixed | +0.0032 | [+0.0025, +0.0039] | 5/0/0 | +0.0002 |
| Roman-empire | hidden_mixing_frozen | combined - fixed | +0.0041 | [+0.0007, +0.0074] | 5/0/0 | +0.0282 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0001 | [-0.0015, +0.0012] | 1/1/3 | +0.7825 |
| Roman-empire | hidden_mixing_frozen | constant_reliability - fixed | +0.0002 | [-0.0013, +0.0018] | 3/0/2 | +0.7228 |
| Roman-empire | hidden_mixing_frozen | zero_reliability - fixed | +0.0004 | [-0.0011, +0.0019] | 3/0/2 | +0.5114 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled - fixed | +0.0010 | [-0.0019, +0.0038] | 3/0/2 | +0.4053 |
| Roman-empire | hidden_mixing_frozen | combined_constant - fixed | +0.0004 | [-0.0010, +0.0018] | 3/0/2 | +0.4785 |
| Roman-empire | hidden_mixing_frozen | reliability_only - feature_only | +0.0020 | [+0.0002, +0.0039] | 4/1/0 | +0.0372 |
| Roman-empire | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0034 | [+0.0025, +0.0042] | 5/0/0 | +0.0004 |
| Roman-empire | hidden_mixing_frozen | true reliability - constant reliability | +0.0030 | [+0.0018, +0.0042] | 5/0/0 | +0.0026 |
| Roman-empire | hidden_mixing_frozen | true reliability - zero reliability | +0.0028 | [+0.0016, +0.0041] | 5/0/0 | +0.0032 |
| Roman-empire | hidden_mixing_frozen | combined - feature_only | +0.0029 | [-0.0006, +0.0064] | 5/0/0 | +0.0846 |
| Roman-empire | hidden_mixing_frozen | combined - combined_shuffled | +0.0031 | [-0.0010, +0.0072] | 4/0/1 | +0.1026 |
| Roman-empire | hidden_mixing_frozen | combined - combined_constant | +0.0037 | [-0.0000, +0.0073] | 5/0/0 | +0.0503 |
| Roman-empire | hidden_mixing_finetune | feature_only - fixed | +0.0012 | [-0.0031, +0.0055] | 3/1/1 | +0.4934 |
| Roman-empire | hidden_mixing_finetune | reliability_only - fixed | +0.0114 | [+0.0049, +0.0179] | 5/0/0 | +0.0084 |
| Roman-empire | hidden_mixing_finetune | combined - fixed | +0.0119 | [+0.0085, +0.0153] | 5/0/0 | +0.0006 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0007 | [-0.0018, +0.0032] | 1/2/2 | +0.4710 |
| Roman-empire | hidden_mixing_finetune | constant_reliability - fixed | +0.0018 | [-0.0018, +0.0054] | 3/0/2 | +0.2463 |
| Roman-empire | hidden_mixing_finetune | zero_reliability - fixed | +0.0025 | [-0.0015, +0.0066] | 4/0/1 | +0.1535 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled - fixed | +0.0011 | [-0.0024, +0.0045] | 3/1/1 | +0.4452 |
| Roman-empire | hidden_mixing_finetune | combined_constant - fixed | +0.0035 | [-0.0004, +0.0075] | 5/0/0 | +0.0693 |
| Roman-empire | hidden_mixing_finetune | reliability_only - feature_only | +0.0102 | [+0.0047, +0.0158] | 5/0/0 | +0.0067 |
| Roman-empire | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0107 | [+0.0046, +0.0168] | 5/0/0 | +0.0081 |
| Roman-empire | hidden_mixing_finetune | true reliability - constant reliability | +0.0096 | [+0.0030, +0.0163] | 5/0/0 | +0.0158 |
| Roman-empire | hidden_mixing_finetune | true reliability - zero reliability | +0.0089 | [+0.0047, +0.0130] | 5/0/0 | +0.0040 |
| Roman-empire | hidden_mixing_finetune | combined - feature_only | +0.0107 | [+0.0076, +0.0138] | 5/0/0 | +0.0006 |
| Roman-empire | hidden_mixing_finetune | combined - combined_shuffled | +0.0108 | [+0.0082, +0.0135] | 5/0/0 | +0.0003 |
| Roman-empire | hidden_mixing_finetune | combined - combined_constant | +0.0084 | [+0.0063, +0.0105] | 5/0/0 | +0.0004 |
| Amazon-ratings | hidden_mixing_frozen | feature_only - fixed | -0.0005 | [-0.0029, +0.0019] | 2/2/1 | +0.5769 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - fixed | -0.0005 | [-0.0017, +0.0008] | 1/1/3 | +0.3766 |
| Amazon-ratings | hidden_mixing_frozen | combined - fixed | -0.0007 | [-0.0021, +0.0007] | 1/1/3 | +0.2258 |
| Amazon-ratings | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0002 | [-0.0015, +0.0011] | 2/1/2 | +0.6885 |
| Amazon-ratings | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [-0.0008, +0.0009] | 2/1/2 | +0.9216 |
| Amazon-ratings | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [-0.0008, +0.0009] | 2/1/2 | +0.9216 |
| Amazon-ratings | hidden_mixing_frozen | combined_shuffled - fixed | -0.0001 | [-0.0009, +0.0007] | 2/1/2 | +0.7489 |
| Amazon-ratings | hidden_mixing_frozen | combined_constant - fixed | -0.0009 | [-0.0022, +0.0005] | 1/1/3 | +0.1439 |
| Amazon-ratings | hidden_mixing_frozen | reliability_only - feature_only | +0.0001 | [-0.0012, +0.0014] | 1/2/2 | +0.8960 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - shuffled reliability | -0.0003 | [-0.0008, +0.0003] | 0/3/2 | +0.2420 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - constant reliability | -0.0005 | [-0.0014, +0.0005] | 1/2/2 | +0.2215 |
| Amazon-ratings | hidden_mixing_frozen | true reliability - zero reliability | -0.0005 | [-0.0014, +0.0005] | 1/2/2 | +0.2215 |
| Amazon-ratings | hidden_mixing_frozen | combined - feature_only | -0.0002 | [-0.0021, +0.0017] | 2/1/2 | +0.7863 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_shuffled | -0.0006 | [-0.0021, +0.0008] | 2/1/2 | +0.2987 |
| Amazon-ratings | hidden_mixing_frozen | combined - combined_constant | +0.0002 | [-0.0015, +0.0018] | 2/1/2 | +0.7990 |
| Amazon-ratings | hidden_mixing_finetune | feature_only - fixed | -0.0006 | [-0.0056, +0.0044] | 3/0/2 | +0.7592 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - fixed | -0.0024 | [-0.0163, +0.0116] | 3/0/2 | +0.6636 |
| Amazon-ratings | hidden_mixing_finetune | combined - fixed | +0.0005 | [-0.0068, +0.0078] | 3/0/2 | +0.8518 |
| Amazon-ratings | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0022 | [-0.0173, +0.0129] | 3/0/2 | +0.7034 |
| Amazon-ratings | hidden_mixing_finetune | constant_reliability - fixed | -0.0024 | [-0.0147, +0.0100] | 3/0/2 | +0.6246 |
| Amazon-ratings | hidden_mixing_finetune | zero_reliability - fixed | +0.0000 | [-0.0077, +0.0078] | 3/0/2 | +0.9912 |
| Amazon-ratings | hidden_mixing_finetune | combined_shuffled - fixed | -0.0031 | [-0.0160, +0.0099] | 3/0/2 | +0.5462 |
| Amazon-ratings | hidden_mixing_finetune | combined_constant - fixed | -0.0022 | [-0.0172, +0.0128] | 3/0/2 | +0.7062 |
| Amazon-ratings | hidden_mixing_finetune | reliability_only - feature_only | -0.0018 | [-0.0124, +0.0089] | 2/1/2 | +0.6689 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0001 | [-0.0034, +0.0032] | 2/2/1 | +0.9174 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - constant reliability | +0.0000 | [-0.0037, +0.0037] | 1/2/2 | +1.0000 |
| Amazon-ratings | hidden_mixing_finetune | true reliability - zero reliability | -0.0024 | [-0.0095, +0.0048] | 2/1/2 | +0.4076 |
| Amazon-ratings | hidden_mixing_finetune | combined - feature_only | +0.0011 | [-0.0029, +0.0051] | 2/1/2 | +0.4878 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_shuffled | +0.0036 | [-0.0063, +0.0135] | 2/1/2 | +0.3709 |
| Amazon-ratings | hidden_mixing_finetune | combined - combined_constant | +0.0027 | [-0.0080, +0.0135] | 2/1/2 | +0.5224 |
| Cora | hidden_protocol | fixed: finetune - frozen | +0.0174 | [-0.0005, +0.0353] | 5/0/0 | +0.0543 |
| Cora | hidden_protocol | feature_only: finetune - frozen | +0.0122 | [-0.0079, +0.0323] | 3/2/0 | +0.1676 |
| Cora | hidden_protocol | reliability_only: finetune - frozen | +0.0124 | [-0.0075, +0.0323] | 3/2/0 | +0.1589 |
| Cora | hidden_protocol | combined: finetune - frozen | +0.0206 | [-0.0101, +0.0513] | 3/2/0 | +0.1362 |
| Cora | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0118 | [-0.0086, +0.0322] | 3/2/0 | +0.1844 |
| Cora | hidden_protocol | constant_reliability: finetune - frozen | +0.0176 | [-0.0072, +0.0424] | 3/2/0 | +0.1199 |
| Cora | hidden_protocol | zero_reliability: finetune - frozen | +0.0122 | [-0.0078, +0.0322] | 3/2/0 | +0.1654 |
| Cora | hidden_protocol | combined_shuffled: finetune - frozen | +0.0156 | [-0.0068, +0.0380] | 3/2/0 | +0.1257 |
| Cora | hidden_protocol | combined_constant: finetune - frozen | +0.0118 | [-0.0086, +0.0322] | 3/2/0 | +0.1844 |
| Citeseer | hidden_protocol | fixed: finetune - frozen | +0.0024 | [-0.0043, +0.0091] | 1/4/0 | +0.3739 |
| Citeseer | hidden_protocol | feature_only: finetune - frozen | -0.0026 | [-0.0091, +0.0039] | 0/3/2 | +0.3321 |
| Citeseer | hidden_protocol | reliability_only: finetune - frozen | +0.0014 | [-0.0130, +0.0158] | 2/1/2 | +0.8008 |
| Citeseer | hidden_protocol | combined: finetune - frozen | -0.0032 | [-0.0095, +0.0031] | 0/2/3 | +0.2310 |
| Citeseer | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0028 | [-0.0146, +0.0202] | 2/1/2 | +0.6776 |
| Citeseer | hidden_protocol | constant_reliability: finetune - frozen | +0.0038 | [-0.0098, +0.0174] | 2/2/1 | +0.4824 |
| Citeseer | hidden_protocol | zero_reliability: finetune - frozen | +0.0032 | [-0.0095, +0.0159] | 2/1/2 | +0.5220 |
| Citeseer | hidden_protocol | combined_shuffled: finetune - frozen | -0.0024 | [-0.0084, +0.0036] | 0/3/2 | +0.3285 |
| Citeseer | hidden_protocol | combined_constant: finetune - frozen | -0.0014 | [-0.0040, +0.0012] | 0/2/3 | +0.2056 |
| Pubmed | hidden_protocol | fixed: finetune - frozen | +0.0012 | [-0.0021, +0.0045] | 1/4/0 | +0.3739 |
| Pubmed | hidden_protocol | feature_only: finetune - frozen | -0.0034 | [-0.0099, +0.0031] | 0/3/2 | +0.2228 |
| Pubmed | hidden_protocol | reliability_only: finetune - frozen | -0.0014 | [-0.0092, +0.0064] | 1/3/1 | +0.6458 |
| Pubmed | hidden_protocol | combined: finetune - frozen | -0.0038 | [-0.0111, +0.0035] | 1/2/2 | +0.2199 |
| Pubmed | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 1/1/3 | +0.1861 |
| Pubmed | hidden_protocol | constant_reliability: finetune - frozen | -0.0042 | [-0.0115, +0.0031] | 0/3/2 | +0.1836 |
| Pubmed | hidden_protocol | zero_reliability: finetune - frozen | -0.0044 | [-0.0119, +0.0031] | 0/3/2 | +0.1802 |
| Pubmed | hidden_protocol | combined_shuffled: finetune - frozen | -0.0044 | [-0.0119, +0.0031] | 0/3/2 | +0.1802 |
| Pubmed | hidden_protocol | combined_constant: finetune - frozen | -0.0040 | [-0.0110, +0.0030] | 0/3/2 | +0.1890 |
| Chameleon | hidden_protocol | fixed: finetune - frozen | +0.0004 | [-0.0008, +0.0017] | 1/4/0 | +0.3739 |
| Chameleon | hidden_protocol | feature_only: finetune - frozen | -0.0026 | [-0.0178, +0.0126] | 3/1/1 | +0.6560 |
| Chameleon | hidden_protocol | reliability_only: finetune - frozen | -0.0031 | [-0.0178, +0.0117] | 1/1/3 | +0.5940 |
| Chameleon | hidden_protocol | combined: finetune - frozen | -0.0009 | [-0.0196, +0.0178] | 2/1/2 | +0.9028 |
| Chameleon | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0031 | [-0.0188, +0.0126] | 2/1/2 | +0.6163 |
| Chameleon | hidden_protocol | constant_reliability: finetune - frozen | -0.0031 | [-0.0178, +0.0117] | 3/1/1 | +0.5940 |
| Chameleon | hidden_protocol | zero_reliability: finetune - frozen | -0.0009 | [-0.0188, +0.0170] | 2/2/1 | +0.8984 |
| Chameleon | hidden_protocol | combined_shuffled: finetune - frozen | -0.0009 | [-0.0192, +0.0174] | 3/0/2 | +0.9007 |
| Chameleon | hidden_protocol | combined_constant: finetune - frozen | +0.0004 | [-0.0186, +0.0194] | 3/1/1 | +0.9520 |
| Squirrel | hidden_protocol | fixed: finetune - frozen | -0.0038 | [-0.0097, +0.0021] | 0/2/3 | +0.1451 |
| Squirrel | hidden_protocol | feature_only: finetune - frozen | -0.0037 | [-0.0113, +0.0040] | 2/0/3 | +0.2562 |
| Squirrel | hidden_protocol | reliability_only: finetune - frozen | -0.0042 | [-0.0139, +0.0055] | 1/2/2 | +0.2935 |
| Squirrel | hidden_protocol | combined: finetune - frozen | -0.0023 | [-0.0116, +0.0070] | 2/1/2 | +0.5307 |
| Squirrel | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0044 | [-0.0158, +0.0070] | 2/1/2 | +0.3423 |
| Squirrel | hidden_protocol | constant_reliability: finetune - frozen | -0.0031 | [-0.0135, +0.0074] | 2/0/3 | +0.4598 |
| Squirrel | hidden_protocol | zero_reliability: finetune - frozen | -0.0050 | [-0.0164, +0.0064] | 2/0/3 | +0.2892 |
| Squirrel | hidden_protocol | combined_shuffled: finetune - frozen | -0.0052 | [-0.0161, +0.0058] | 2/1/2 | +0.2588 |
| Squirrel | hidden_protocol | combined_constant: finetune - frozen | -0.0044 | [-0.0152, +0.0064] | 2/0/3 | +0.3202 |
| Actor | hidden_protocol | fixed: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/5/0 | n/a |
| Actor | hidden_protocol | feature_only: finetune - frozen | +0.0022 | [-0.0012, +0.0057] | 3/2/0 | +0.1459 |
| Actor | hidden_protocol | reliability_only: finetune - frozen | -0.0004 | [-0.0008, +0.0001] | 0/2/3 | +0.0705 |
| Actor | hidden_protocol | combined: finetune - frozen | +0.0012 | [-0.0032, +0.0056] | 2/2/1 | +0.4943 |
| Actor | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0008 | [-0.0028, +0.0044] | 2/2/1 | +0.5734 |
| Actor | hidden_protocol | constant_reliability: finetune - frozen | -0.0000 | [-0.0012, +0.0012] | 1/3/1 | +1.0000 |
| Actor | hidden_protocol | zero_reliability: finetune - frozen | -0.0000 | [-0.0012, +0.0012] | 1/3/1 | +1.0000 |
| Actor | hidden_protocol | combined_shuffled: finetune - frozen | +0.0013 | [-0.0015, +0.0041] | 3/2/0 | +0.2577 |
| Actor | hidden_protocol | combined_constant: finetune - frozen | +0.0008 | [-0.0019, +0.0035] | 3/1/1 | +0.4581 |
| Roman-empire | hidden_protocol | fixed: finetune - frozen | +0.0030 | [-0.0007, +0.0068] | 3/2/0 | +0.0897 |
| Roman-empire | hidden_protocol | feature_only: finetune - frozen | +0.0030 | [-0.0030, +0.0091] | 3/0/2 | +0.2361 |
| Roman-empire | hidden_protocol | reliability_only: finetune - frozen | +0.0112 | [+0.0071, +0.0154] | 5/0/0 | +0.0017 |
| Roman-empire | hidden_protocol | combined: finetune - frozen | +0.0109 | [+0.0074, +0.0143] | 5/0/0 | +0.0010 |
| Roman-empire | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0039 | [+0.0012, +0.0066] | 5/0/0 | +0.0158 |
| Roman-empire | hidden_protocol | constant_reliability: finetune - frozen | +0.0046 | [+0.0010, +0.0082] | 4/1/0 | +0.0248 |
| Roman-empire | hidden_protocol | zero_reliability: finetune - frozen | +0.0052 | [+0.0028, +0.0076] | 5/0/0 | +0.0038 |
| Roman-empire | hidden_protocol | combined_shuffled: finetune - frozen | +0.0031 | [-0.0022, +0.0085] | 4/0/1 | +0.1760 |
| Roman-empire | hidden_protocol | combined_constant: finetune - frozen | +0.0062 | [+0.0045, +0.0078] | 5/0/0 | +0.0005 |
| Amazon-ratings | hidden_protocol | fixed: finetune - frozen | +0.0084 | [-0.0040, +0.0209] | 3/2/0 | +0.1335 |
| Amazon-ratings | hidden_protocol | feature_only: finetune - frozen | +0.0084 | [+0.0003, +0.0165] | 5/0/0 | +0.0457 |
| Amazon-ratings | hidden_protocol | reliability_only: finetune - frozen | +0.0065 | [-0.0004, +0.0135] | 4/1/0 | +0.0588 |
| Amazon-ratings | hidden_protocol | combined: finetune - frozen | +0.0097 | [+0.0011, +0.0182] | 4/1/0 | +0.0346 |
| Amazon-ratings | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0064 | [-0.0020, +0.0148] | 4/1/0 | +0.1027 |
| Amazon-ratings | hidden_protocol | constant_reliability: finetune - frozen | +0.0060 | [-0.0021, +0.0142] | 3/2/0 | +0.1082 |
| Amazon-ratings | hidden_protocol | zero_reliability: finetune - frozen | +0.0084 | [+0.0016, +0.0153] | 4/1/0 | +0.0271 |
| Amazon-ratings | hidden_protocol | combined_shuffled: finetune - frozen | +0.0055 | [-0.0027, +0.0136] | 4/1/0 | +0.1358 |
| Amazon-ratings | hidden_protocol | combined_constant: finetune - frozen | +0.0071 | [-0.0008, +0.0150] | 4/1/0 | +0.0669 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
