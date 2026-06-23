# Representation Control Screening

- Datasets: Chameleon, Squirrel, Roman-empire, Cora, Citeseer
- Families: residual_alpha, hidden_mixing_frozen, hidden_mixing_finetune
- Runs: 3
- Edge protocol: undirected
- Max adjustment: 0.1
- Initial adjustment: 0.001
- `hidden_mixing_frozen/fixed` is the untouched selected hidden baseline.
- `hidden_mixing_finetune/fixed` is the same-architecture fixed-mixing fine-tuning control.
- `zero_reliability` is a learnable controller receiving an all-zero reliability input; `fixed` is the no-controller baseline.

## Summary

| Dataset | Family | Control | Accuracy | Baseline | Delta | Std | Alpha | Adjustment | Active ctrl params | Backbone params |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Chameleon | hidden_mixing_finetune | combined | 0.5446 | 0.5424 | +0.0022 | 0.0092 | 0.9163 | 0.0009 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_constant | 0.5446 | 0.5424 | +0.0022 | 0.0092 | 0.9163 | 0.0009 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | combined_shuffled | 0.5395 | 0.5424 | -0.0029 | 0.0129 | 0.9164 | 0.0008 | 34948 | 224453 |
| Chameleon | hidden_mixing_finetune | constant_reliability | 0.5439 | 0.5424 | +0.0015 | 0.0100 | 0.9163 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | feature_only | 0.5387 | 0.5424 | -0.0037 | 0.0137 | 0.9163 | 0.0008 | 25348 | 224453 |
| Chameleon | hidden_mixing_finetune | fixed | 0.5431 | 0.5424 | +0.0007 | 0.0108 | 0.9167 | 0.0000 | 0 | 224453 |
| Chameleon | hidden_mixing_finetune | reliability_only | 0.5395 | 0.5424 | -0.0029 | 0.0129 | 0.9163 | 0.0008 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability | 0.5446 | 0.5424 | +0.0022 | 0.0092 | 0.9163 | 0.0009 | 26372 | 224453 |
| Chameleon | hidden_mixing_finetune | zero_reliability | 0.5431 | 0.5424 | +0.0007 | 0.0102 | 0.9164 | 0.0006 | 26372 | 224453 |
| Chameleon | hidden_mixing_frozen | combined | 0.5439 | 0.5424 | +0.0015 | 0.0100 | 0.9224 | 0.0289 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_constant | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9196 | 0.0139 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | combined_shuffled | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9161 | 0.0012 | 34948 | 0 |
| Chameleon | hidden_mixing_frozen | constant_reliability | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9163 | 0.0010 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | feature_only | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9163 | 0.0010 | 25348 | 0 |
| Chameleon | hidden_mixing_frozen | fixed | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9167 | 0.0000 | 0 | 0 |
| Chameleon | hidden_mixing_frozen | reliability_only | 0.5446 | 0.5424 | +0.0022 | 0.0092 | 0.9219 | 0.0307 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9160 | 0.0013 | 26372 | 0 |
| Chameleon | hidden_mixing_frozen | zero_reliability | 0.5424 | 0.5424 | +0.0000 | 0.0117 | 0.9163 | 0.0010 | 26372 | 0 |
| Chameleon | residual_alpha | combined | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 162178 | 0 |
| Chameleon | residual_alpha | combined_constant | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 162178 | 0 |
| Chameleon | residual_alpha | combined_shuffled | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 162178 | 0 |
| Chameleon | residual_alpha | constant_reliability | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 13186 | 0 |
| Chameleon | residual_alpha | feature_only | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 157378 | 0 |
| Chameleon | residual_alpha | fixed | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9167 | 0.0000 | 0 | 0 |
| Chameleon | residual_alpha | reliability_only | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 13186 | 0 |
| Chameleon | residual_alpha | shuffled_reliability | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 13186 | 0 |
| Chameleon | residual_alpha | zero_reliability | 0.6330 | 0.6330 | +0.0000 | 0.0166 | 0.9163 | 0.0010 | 13186 | 0 |
| Citeseer | hidden_mixing_finetune | combined | 0.6013 | 0.6017 | -0.0003 | 0.0213 | 0.8330 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_constant | 0.6013 | 0.6017 | -0.0003 | 0.0213 | 0.8330 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | combined_shuffled | 0.6013 | 0.6017 | -0.0003 | 0.0213 | 0.8330 | 0.0010 | 34948 | 312710 |
| Citeseer | hidden_mixing_finetune | constant_reliability | 0.6090 | 0.6017 | +0.0073 | 0.0151 | 0.8331 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | feature_only | 0.6067 | 0.6017 | +0.0050 | 0.0165 | 0.8331 | 0.0010 | 25348 | 312710 |
| Citeseer | hidden_mixing_finetune | fixed | 0.6063 | 0.6017 | +0.0047 | 0.0221 | 0.8333 | 0.0000 | 0 | 312710 |
| Citeseer | hidden_mixing_finetune | reliability_only | 0.6080 | 0.6017 | +0.0063 | 0.0156 | 0.8330 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability | 0.6100 | 0.6017 | +0.0083 | 0.0147 | 0.8330 | 0.0010 | 26372 | 312710 |
| Citeseer | hidden_mixing_finetune | zero_reliability | 0.6083 | 0.6017 | +0.0067 | 0.0155 | 0.8331 | 0.0011 | 26372 | 312710 |
| Citeseer | hidden_mixing_frozen | combined | 0.6017 | 0.6017 | +0.0000 | 0.0212 | 0.8330 | 0.0010 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_constant | 0.6017 | 0.6017 | +0.0000 | 0.0212 | 0.8330 | 0.0010 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | combined_shuffled | 0.6017 | 0.6017 | +0.0000 | 0.0212 | 0.8330 | 0.0010 | 34948 | 0 |
| Citeseer | hidden_mixing_frozen | constant_reliability | 0.6010 | 0.6017 | -0.0007 | 0.0214 | 0.8330 | 0.0010 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | feature_only | 0.6017 | 0.6017 | +0.0000 | 0.0212 | 0.8330 | 0.0009 | 25348 | 0 |
| Citeseer | hidden_mixing_frozen | fixed | 0.6017 | 0.6017 | +0.0000 | 0.0212 | 0.8333 | 0.0000 | 0 | 0 |
| Citeseer | hidden_mixing_frozen | reliability_only | 0.6010 | 0.6017 | -0.0007 | 0.0214 | 0.8330 | 0.0010 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | shuffled_reliability | 0.6010 | 0.6017 | -0.0007 | 0.0214 | 0.8330 | 0.0010 | 26372 | 0 |
| Citeseer | hidden_mixing_frozen | zero_reliability | 0.6010 | 0.6017 | -0.0007 | 0.0214 | 0.8330 | 0.0010 | 26372 | 0 |
| Citeseer | residual_alpha | combined | 0.6883 | 0.6907 | -0.0023 | 0.0071 | 0.9921 | 0.0086 | 250370 | 0 |
| Citeseer | residual_alpha | combined_constant | 0.6923 | 0.6907 | +0.0017 | 0.0087 | 0.9882 | 0.0124 | 250370 | 0 |
| Citeseer | residual_alpha | combined_shuffled | 0.6880 | 0.6907 | -0.0027 | 0.0071 | 0.9932 | 0.0074 | 250370 | 0 |
| Citeseer | residual_alpha | constant_reliability | 0.6920 | 0.6907 | +0.0013 | 0.0078 | 0.9878 | 0.0129 | 13186 | 0 |
| Citeseer | residual_alpha | feature_only | 0.6913 | 0.6907 | +0.0007 | 0.0047 | 0.9960 | 0.0047 | 245570 | 0 |
| Citeseer | residual_alpha | fixed | 0.6907 | 0.6907 | +0.0000 | 0.0058 | 1.0000 | 0.0000 | 0 | 0 |
| Citeseer | residual_alpha | reliability_only | 0.6897 | 0.6907 | -0.0010 | 0.0059 | 0.9936 | 0.0072 | 13186 | 0 |
| Citeseer | residual_alpha | shuffled_reliability | 0.6893 | 0.6907 | -0.0013 | 0.0123 | 0.9765 | 0.0241 | 13186 | 0 |
| Citeseer | residual_alpha | zero_reliability | 0.6913 | 0.6907 | +0.0007 | 0.0087 | 0.9874 | 0.0132 | 13186 | 0 |
| Cora | hidden_mixing_finetune | combined | 0.6960 | 0.6803 | +0.0157 | 0.0123 | 0.7498 | 0.0009 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_constant | 0.6973 | 0.6803 | +0.0170 | 0.0141 | 0.7499 | 0.0008 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | combined_shuffled | 0.6970 | 0.6803 | +0.0167 | 0.0136 | 0.7498 | 0.0009 | 34948 | 167495 |
| Cora | hidden_mixing_finetune | constant_reliability | 0.6967 | 0.6803 | +0.0163 | 0.0132 | 0.7498 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | feature_only | 0.6993 | 0.6803 | +0.0190 | 0.0168 | 0.7498 | 0.0009 | 25348 | 167495 |
| Cora | hidden_mixing_finetune | fixed | 0.6917 | 0.6803 | +0.0113 | 0.0071 | 0.7500 | 0.0000 | 0 | 167495 |
| Cora | hidden_mixing_finetune | reliability_only | 0.6983 | 0.6803 | +0.0180 | 0.0154 | 0.7498 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | shuffled_reliability | 0.6963 | 0.6803 | +0.0160 | 0.0128 | 0.7498 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_finetune | zero_reliability | 0.6983 | 0.6803 | +0.0180 | 0.0154 | 0.7498 | 0.0009 | 26372 | 167495 |
| Cora | hidden_mixing_frozen | combined | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_constant | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | combined_shuffled | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 34948 | 0 |
| Cora | hidden_mixing_frozen | constant_reliability | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | feature_only | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 25348 | 0 |
| Cora | hidden_mixing_frozen | fixed | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7500 | 0.0000 | 0 | 0 |
| Cora | hidden_mixing_frozen | reliability_only | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 26372 | 0 |
| Cora | hidden_mixing_frozen | shuffled_reliability | 0.6800 | 0.6803 | -0.0003 | 0.0119 | 0.7519 | 0.0053 | 26372 | 0 |
| Cora | hidden_mixing_frozen | zero_reliability | 0.6803 | 0.6803 | +0.0000 | 0.0119 | 0.7498 | 0.0010 | 26372 | 0 |
| Cora | residual_alpha | combined | 0.8057 | 0.8023 | +0.0033 | 0.0105 | 0.9853 | 0.0153 | 105090 | 0 |
| Cora | residual_alpha | combined_constant | 0.8067 | 0.8023 | +0.0043 | 0.0125 | 0.9802 | 0.0205 | 105090 | 0 |
| Cora | residual_alpha | combined_shuffled | 0.8073 | 0.8023 | +0.0050 | 0.0108 | 0.9800 | 0.0206 | 105090 | 0 |
| Cora | residual_alpha | constant_reliability | 0.8097 | 0.8023 | +0.0073 | 0.0076 | 0.9805 | 0.0201 | 13186 | 0 |
| Cora | residual_alpha | feature_only | 0.8090 | 0.8023 | +0.0067 | 0.0079 | 0.9752 | 0.0254 | 100290 | 0 |
| Cora | residual_alpha | fixed | 0.8023 | 0.8023 | +0.0000 | 0.0116 | 1.0000 | 0.0000 | 0 | 0 |
| Cora | residual_alpha | reliability_only | 0.8093 | 0.8023 | +0.0070 | 0.0066 | 0.9799 | 0.0207 | 13186 | 0 |
| Cora | residual_alpha | shuffled_reliability | 0.8080 | 0.8023 | +0.0057 | 0.0070 | 0.9738 | 0.0268 | 13186 | 0 |
| Cora | residual_alpha | zero_reliability | 0.8103 | 0.8023 | +0.0080 | 0.0080 | 0.9810 | 0.0196 | 13186 | 0 |
| Roman-empire | hidden_mixing_finetune | combined | 0.8341 | 0.8183 | +0.0158 | 0.0037 | 0.7439 | 0.0313 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_constant | 0.8253 | 0.8183 | +0.0071 | 0.0052 | 0.7499 | 0.0013 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled | 0.8244 | 0.8183 | +0.0061 | 0.0069 | 0.7487 | 0.0050 | 34948 | 95698 |
| Roman-empire | hidden_mixing_finetune | constant_reliability | 0.8259 | 0.8183 | +0.0076 | 0.0054 | 0.7499 | 0.0007 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | feature_only | 0.8249 | 0.8183 | +0.0066 | 0.0076 | 0.7489 | 0.0023 | 25348 | 95698 |
| Roman-empire | hidden_mixing_finetune | fixed | 0.8256 | 0.8183 | +0.0073 | 0.0056 | 0.7500 | 0.0000 | 0 | 95698 |
| Roman-empire | hidden_mixing_finetune | reliability_only | 0.8325 | 0.8183 | +0.0142 | 0.0034 | 0.7422 | 0.0323 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability | 0.8253 | 0.8183 | +0.0071 | 0.0061 | 0.7487 | 0.0035 | 26372 | 95698 |
| Roman-empire | hidden_mixing_finetune | zero_reliability | 0.8255 | 0.8183 | +0.0072 | 0.0040 | 0.7499 | 0.0008 | 26372 | 95698 |
| Roman-empire | hidden_mixing_frozen | combined | 0.8220 | 0.8183 | +0.0037 | 0.0063 | 0.7557 | 0.0546 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_constant | 0.8187 | 0.8183 | +0.0004 | 0.0054 | 0.7585 | 0.0342 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled | 0.8179 | 0.8183 | -0.0004 | 0.0061 | 0.7611 | 0.0454 | 34948 | 0 |
| Roman-empire | hidden_mixing_frozen | constant_reliability | 0.8192 | 0.8183 | +0.0009 | 0.0055 | 0.7595 | 0.0379 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | feature_only | 0.8187 | 0.8183 | +0.0004 | 0.0056 | 0.7620 | 0.0491 | 25348 | 0 |
| Roman-empire | hidden_mixing_frozen | fixed | 0.8183 | 0.8183 | +0.0000 | 0.0043 | 0.7500 | 0.0000 | 0 | 0 |
| Roman-empire | hidden_mixing_frozen | reliability_only | 0.8220 | 0.8183 | +0.0037 | 0.0055 | 0.7611 | 0.0474 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability | 0.8189 | 0.8183 | +0.0006 | 0.0050 | 0.7591 | 0.0379 | 26372 | 0 |
| Roman-empire | hidden_mixing_frozen | zero_reliability | 0.8192 | 0.8183 | +0.0009 | 0.0055 | 0.7595 | 0.0379 | 26372 | 0 |
| Roman-empire | residual_alpha | combined | 0.6778 | 0.6779 | -0.0001 | 0.0025 | 0.4883 | 0.0239 | 32578 | 0 |
| Roman-empire | residual_alpha | combined_constant | 0.6778 | 0.6779 | -0.0001 | 0.0024 | 0.4882 | 0.0242 | 32578 | 0 |
| Roman-empire | residual_alpha | combined_shuffled | 0.6778 | 0.6779 | -0.0001 | 0.0025 | 0.4883 | 0.0240 | 32578 | 0 |
| Roman-empire | residual_alpha | constant_reliability | 0.6777 | 0.6779 | -0.0002 | 0.0024 | 0.4874 | 0.0258 | 13186 | 0 |
| Roman-empire | residual_alpha | feature_only | 0.6780 | 0.6779 | +0.0001 | 0.0027 | 0.4927 | 0.0153 | 27778 | 0 |
| Roman-empire | residual_alpha | fixed | 0.6779 | 0.6779 | +0.0000 | 0.0029 | 0.5000 | 0.0000 | 0 | 0 |
| Roman-empire | residual_alpha | reliability_only | 0.6776 | 0.6779 | -0.0003 | 0.0023 | 0.4871 | 0.0264 | 13186 | 0 |
| Roman-empire | residual_alpha | shuffled_reliability | 0.6776 | 0.6779 | -0.0003 | 0.0023 | 0.4870 | 0.0266 | 13186 | 0 |
| Roman-empire | residual_alpha | zero_reliability | 0.6777 | 0.6779 | -0.0002 | 0.0024 | 0.4875 | 0.0257 | 13186 | 0 |
| Squirrel | hidden_mixing_finetune | combined | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0010 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_constant | 0.3340 | 0.3337 | +0.0003 | 0.0061 | 0.7498 | 0.0009 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | combined_shuffled | 0.3330 | 0.3337 | -0.0006 | 0.0059 | 0.7456 | 0.0065 | 34948 | 209349 |
| Squirrel | hidden_mixing_finetune | constant_reliability | 0.3324 | 0.3337 | -0.0013 | 0.0059 | 0.7498 | 0.0009 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | feature_only | 0.3314 | 0.3337 | -0.0022 | 0.0062 | 0.7473 | 0.0043 | 25348 | 209349 |
| Squirrel | hidden_mixing_finetune | fixed | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7500 | 0.0000 | 0 | 209349 |
| Squirrel | hidden_mixing_finetune | reliability_only | 0.3327 | 0.3337 | -0.0010 | 0.0059 | 0.7494 | 0.0015 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | shuffled_reliability | 0.3305 | 0.3337 | -0.0032 | 0.0068 | 0.7535 | 0.0164 | 26372 | 209349 |
| Squirrel | hidden_mixing_finetune | zero_reliability | 0.3327 | 0.3337 | -0.0010 | 0.0059 | 0.7499 | 0.0012 | 26372 | 209349 |
| Squirrel | hidden_mixing_frozen | combined | 0.3343 | 0.3337 | +0.0006 | 0.0028 | 0.7402 | 0.0249 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_constant | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0010 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | combined_shuffled | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0011 | 34948 | 0 |
| Squirrel | hidden_mixing_frozen | constant_reliability | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0010 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | feature_only | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0010 | 25348 | 0 |
| Squirrel | hidden_mixing_frozen | fixed | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7500 | 0.0000 | 0 | 0 |
| Squirrel | hidden_mixing_frozen | reliability_only | 0.3343 | 0.3337 | +0.0006 | 0.0036 | 0.7440 | 0.0226 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability | 0.3333 | 0.3337 | -0.0003 | 0.0057 | 0.7448 | 0.0083 | 26372 | 0 |
| Squirrel | hidden_mixing_frozen | zero_reliability | 0.3337 | 0.3337 | +0.0000 | 0.0060 | 0.7497 | 0.0010 | 26372 | 0 |
| Squirrel | residual_alpha | combined | 0.4505 | 0.4576 | -0.0070 | 0.0095 | 0.9343 | 0.0660 | 147074 | 0 |
| Squirrel | residual_alpha | combined_constant | 0.4524 | 0.4576 | -0.0051 | 0.0088 | 0.9354 | 0.0648 | 147074 | 0 |
| Squirrel | residual_alpha | combined_shuffled | 0.4518 | 0.4576 | -0.0058 | 0.0085 | 0.9393 | 0.0610 | 147074 | 0 |
| Squirrel | residual_alpha | constant_reliability | 0.4515 | 0.4576 | -0.0061 | 0.0082 | 0.9321 | 0.0681 | 13186 | 0 |
| Squirrel | residual_alpha | feature_only | 0.4512 | 0.4576 | -0.0064 | 0.0082 | 0.9328 | 0.0675 | 142274 | 0 |
| Squirrel | residual_alpha | fixed | 0.4576 | 0.4576 | +0.0000 | 0.0126 | 1.0000 | 0.0000 | 0 | 0 |
| Squirrel | residual_alpha | reliability_only | 0.4576 | 0.4576 | +0.0000 | 0.0135 | 0.9590 | 0.0414 | 13186 | 0 |
| Squirrel | residual_alpha | shuffled_reliability | 0.4524 | 0.4576 | -0.0051 | 0.0090 | 0.9337 | 0.0665 | 13186 | 0 |
| Squirrel | residual_alpha | zero_reliability | 0.4515 | 0.4576 | -0.0061 | 0.0082 | 0.9321 | 0.0682 | 13186 | 0 |

## Paired Comparisons

| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |
|---|---|---|---:|---:|---:|---:|
| Chameleon | residual_alpha | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | residual_alpha | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | reliability_only - fixed | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | combined - fixed | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_mixing_frozen | reliability_only - feature_only | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | true reliability - constant reliability | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | true reliability - zero reliability | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | combined - feature_only | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | combined - combined_shuffled | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_frozen | combined - combined_constant | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | feature_only - fixed | -0.0044 | [-0.0332, +0.0244] | 1/1/1 | +0.5799 |
| Chameleon | hidden_mixing_finetune | reliability_only - fixed | -0.0037 | [-0.0294, +0.0221] | 1/1/1 | +0.6035 |
| Chameleon | hidden_mixing_finetune | combined - fixed | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | constant_reliability - fixed | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | zero_reliability - fixed | +0.0000 | [-0.0054, +0.0054] | 1/1/1 | +1.0000 |
| Chameleon | hidden_mixing_finetune | combined_shuffled - fixed | -0.0037 | [-0.0294, +0.0221] | 1/1/1 | +0.6035 |
| Chameleon | hidden_mixing_finetune | combined_constant - fixed | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | reliability_only - feature_only | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0051 | [-0.0271, +0.0169] | 0/2/1 | +0.4226 |
| Chameleon | hidden_mixing_finetune | true reliability - constant reliability | -0.0044 | [-0.0281, +0.0194] | 1/1/1 | +0.5101 |
| Chameleon | hidden_mixing_finetune | true reliability - zero reliability | -0.0037 | [-0.0243, +0.0170] | 1/1/1 | +0.5254 |
| Chameleon | hidden_mixing_finetune | combined - feature_only | +0.0058 | [-0.0193, +0.0310] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | combined - combined_shuffled | +0.0051 | [-0.0169, +0.0271] | 1/2/0 | +0.4226 |
| Chameleon | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | residual_alpha | feature_only - fixed | -0.0064 | [-0.0321, +0.0193] | 1/0/2 | +0.3964 |
| Squirrel | residual_alpha | reliability_only - fixed | +0.0000 | [-0.0048, +0.0048] | 1/1/1 | +1.0000 |
| Squirrel | residual_alpha | combined - fixed | -0.0070 | [-0.0279, +0.0138] | 0/1/2 | +0.2832 |
| Squirrel | residual_alpha | shuffled_reliability - fixed | -0.0051 | [-0.0300, +0.0197] | 1/0/2 | +0.4684 |
| Squirrel | residual_alpha | constant_reliability - fixed | -0.0061 | [-0.0283, +0.0161] | 0/1/2 | +0.3591 |
| Squirrel | residual_alpha | zero_reliability - fixed | -0.0061 | [-0.0283, +0.0161] | 0/1/2 | +0.3591 |
| Squirrel | residual_alpha | combined_shuffled - fixed | -0.0058 | [-0.0288, +0.0172] | 1/0/2 | +0.3939 |
| Squirrel | residual_alpha | combined_constant - fixed | -0.0051 | [-0.0254, +0.0152] | 1/0/2 | +0.3909 |
| Squirrel | residual_alpha | reliability_only - feature_only | +0.0064 | [-0.0191, +0.0319] | 2/1/0 | +0.3931 |
| Squirrel | residual_alpha | true reliability - shuffled reliability | +0.0051 | [-0.0190, +0.0293] | 1/1/1 | +0.4575 |
| Squirrel | residual_alpha | true reliability - constant reliability | +0.0061 | [-0.0161, +0.0283] | 2/1/0 | +0.3591 |
| Squirrel | residual_alpha | true reliability - zero reliability | +0.0061 | [-0.0161, +0.0283] | 2/1/0 | +0.3591 |
| Squirrel | residual_alpha | combined - feature_only | -0.0006 | [-0.0066, +0.0054] | 1/0/2 | +0.6914 |
| Squirrel | residual_alpha | combined - combined_shuffled | -0.0013 | [-0.0049, +0.0024] | 0/1/2 | +0.2697 |
| Squirrel | residual_alpha | combined - combined_constant | -0.0019 | [-0.0043, +0.0005] | 0/0/3 | +0.0742 |
| Squirrel | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_frozen | reliability_only - fixed | +0.0006 | [-0.0084, +0.0097] | 1/0/2 | +0.7892 |
| Squirrel | hidden_mixing_frozen | combined - fixed | +0.0006 | [-0.0090, +0.0103] | 1/1/1 | +0.8020 |
| Squirrel | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0003 | [-0.0017, +0.0011] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_frozen | reliability_only - feature_only | +0.0006 | [-0.0084, +0.0097] | 1/0/2 | +0.7892 |
| Squirrel | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0010 | [-0.0076, +0.0096] | 1/1/1 | +0.6784 |
| Squirrel | hidden_mixing_frozen | true reliability - constant reliability | +0.0006 | [-0.0084, +0.0097] | 1/0/2 | +0.7892 |
| Squirrel | hidden_mixing_frozen | true reliability - zero reliability | +0.0006 | [-0.0084, +0.0097] | 1/0/2 | +0.7892 |
| Squirrel | hidden_mixing_frozen | combined - feature_only | +0.0006 | [-0.0090, +0.0103] | 1/1/1 | +0.8020 |
| Squirrel | hidden_mixing_frozen | combined - combined_shuffled | +0.0006 | [-0.0090, +0.0103] | 1/1/1 | +0.8020 |
| Squirrel | hidden_mixing_frozen | combined - combined_constant | +0.0006 | [-0.0090, +0.0103] | 1/1/1 | +0.8020 |
| Squirrel | hidden_mixing_finetune | feature_only - fixed | -0.0022 | [-0.0119, +0.0074] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | reliability_only - fixed | -0.0010 | [-0.0051, +0.0032] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0032 | [-0.0170, +0.0106] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | constant_reliability - fixed | -0.0013 | [-0.0068, +0.0042] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | zero_reliability - fixed | -0.0010 | [-0.0051, +0.0032] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | combined_shuffled - fixed | -0.0006 | [-0.0034, +0.0021] | 0/2/1 | +0.4226 |
| Squirrel | hidden_mixing_finetune | combined_constant - fixed | +0.0003 | [-0.0011, +0.0017] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | reliability_only - feature_only | +0.0013 | [-0.0042, +0.0068] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0022 | [-0.0074, +0.0119] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | true reliability - constant reliability | +0.0003 | [-0.0011, +0.0017] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_mixing_finetune | combined - feature_only | +0.0022 | [-0.0074, +0.0119] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | combined - combined_shuffled | +0.0006 | [-0.0021, +0.0034] | 1/2/0 | +0.4226 |
| Squirrel | hidden_mixing_finetune | combined - combined_constant | -0.0003 | [-0.0017, +0.0011] | 0/2/1 | +0.4226 |
| Roman-empire | residual_alpha | feature_only - fixed | +0.0001 | [-0.0006, +0.0007] | 1/1/1 | +0.7418 |
| Roman-empire | residual_alpha | reliability_only - fixed | -0.0003 | [-0.0028, +0.0022] | 1/1/1 | +0.6621 |
| Roman-empire | residual_alpha | combined - fixed | -0.0001 | [-0.0015, +0.0012] | 1/1/1 | +0.7418 |
| Roman-empire | residual_alpha | shuffled_reliability - fixed | -0.0003 | [-0.0028, +0.0022] | 1/1/1 | +0.6621 |
| Roman-empire | residual_alpha | constant_reliability - fixed | -0.0002 | [-0.0025, +0.0020] | 1/1/1 | +0.6968 |
| Roman-empire | residual_alpha | zero_reliability - fixed | -0.0002 | [-0.0025, +0.0020] | 1/1/1 | +0.6968 |
| Roman-empire | residual_alpha | combined_shuffled - fixed | -0.0001 | [-0.0016, +0.0015] | 1/1/1 | +0.8845 |
| Roman-empire | residual_alpha | combined_constant - fixed | -0.0001 | [-0.0019, +0.0017] | 1/1/1 | +0.8020 |
| Roman-empire | residual_alpha | reliability_only - feature_only | -0.0004 | [-0.0023, +0.0016] | 1/1/1 | +0.5101 |
| Roman-empire | residual_alpha | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Roman-empire | residual_alpha | true reliability - constant reliability | -0.0001 | [-0.0003, +0.0002] | 0/2/1 | +0.4226 |
| Roman-empire | residual_alpha | true reliability - zero reliability | -0.0001 | [-0.0003, +0.0002] | 0/2/1 | +0.4226 |
| Roman-empire | residual_alpha | combined - feature_only | -0.0002 | [-0.0009, +0.0006] | 0/2/1 | +0.4226 |
| Roman-empire | residual_alpha | combined - combined_shuffled | -0.0001 | [-0.0003, +0.0002] | 0/2/1 | +0.4226 |
| Roman-empire | residual_alpha | combined - combined_constant | +0.0000 | [-0.0004, +0.0004] | 1/1/1 | +1.0000 |
| Roman-empire | hidden_mixing_frozen | feature_only - fixed | +0.0004 | [-0.0039, +0.0047] | 2/0/1 | +0.7218 |
| Roman-empire | hidden_mixing_frozen | reliability_only - fixed | +0.0037 | [-0.0002, +0.0076] | 3/0/0 | +0.0548 |
| Roman-empire | hidden_mixing_frozen | combined - fixed | +0.0037 | [-0.0038, +0.0112] | 3/0/0 | +0.1666 |
| Roman-empire | hidden_mixing_frozen | shuffled_reliability - fixed | +0.0006 | [-0.0022, +0.0034] | 2/0/1 | +0.4639 |
| Roman-empire | hidden_mixing_frozen | constant_reliability - fixed | +0.0009 | [-0.0037, +0.0055] | 2/0/1 | +0.4941 |
| Roman-empire | hidden_mixing_frozen | zero_reliability - fixed | +0.0009 | [-0.0038, +0.0057] | 2/0/1 | +0.4820 |
| Roman-empire | hidden_mixing_frozen | combined_shuffled - fixed | -0.0004 | [-0.0065, +0.0056] | 2/0/1 | +0.7972 |
| Roman-empire | hidden_mixing_frozen | combined_constant - fixed | +0.0004 | [-0.0039, +0.0047] | 2/0/1 | +0.7218 |
| Roman-empire | hidden_mixing_frozen | reliability_only - feature_only | +0.0033 | [+0.0004, +0.0062] | 3/0/0 | +0.0399 |
| Roman-empire | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0031 | [-0.0002, +0.0064] | 3/0/0 | +0.0552 |
| Roman-empire | hidden_mixing_frozen | true reliability - constant reliability | +0.0028 | [-0.0010, +0.0066] | 3/0/0 | +0.0853 |
| Roman-empire | hidden_mixing_frozen | true reliability - zero reliability | +0.0028 | [-0.0013, +0.0068] | 3/0/0 | +0.0990 |
| Roman-empire | hidden_mixing_frozen | combined - feature_only | +0.0033 | [-0.0039, +0.0105] | 2/1/0 | +0.1881 |
| Roman-empire | hidden_mixing_frozen | combined - combined_shuffled | +0.0041 | [-0.0032, +0.0115] | 3/0/0 | +0.1376 |
| Roman-empire | hidden_mixing_frozen | combined - combined_constant | +0.0033 | [-0.0047, +0.0113] | 2/0/1 | +0.2200 |
| Roman-empire | hidden_mixing_finetune | feature_only - fixed | -0.0006 | [-0.0072, +0.0059] | 1/0/2 | +0.7134 |
| Roman-empire | hidden_mixing_finetune | reliability_only - fixed | +0.0069 | [+0.0001, +0.0136] | 3/0/0 | +0.0482 |
| Roman-empire | hidden_mixing_finetune | combined - fixed | +0.0085 | [+0.0020, +0.0150] | 3/0/0 | +0.0300 |
| Roman-empire | hidden_mixing_finetune | shuffled_reliability - fixed | -0.0002 | [-0.0020, +0.0015] | 1/0/2 | +0.6253 |
| Roman-empire | hidden_mixing_finetune | constant_reliability - fixed | +0.0003 | [-0.0037, +0.0043] | 1/0/2 | +0.7805 |
| Roman-empire | hidden_mixing_finetune | zero_reliability - fixed | -0.0001 | [-0.0053, +0.0051] | 2/0/1 | +0.9317 |
| Roman-empire | hidden_mixing_finetune | combined_shuffled - fixed | -0.0012 | [-0.0070, +0.0046] | 2/0/1 | +0.4762 |
| Roman-empire | hidden_mixing_finetune | combined_constant - fixed | -0.0002 | [-0.0038, +0.0033] | 1/0/2 | +0.8020 |
| Roman-empire | hidden_mixing_finetune | reliability_only - feature_only | +0.0075 | [-0.0057, +0.0207] | 3/0/0 | +0.1337 |
| Roman-empire | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0071 | [-0.0011, +0.0153] | 3/0/0 | +0.0649 |
| Roman-empire | hidden_mixing_finetune | true reliability - constant reliability | +0.0066 | [-0.0010, +0.0142] | 3/0/0 | +0.0653 |
| Roman-empire | hidden_mixing_finetune | true reliability - zero reliability | +0.0070 | [+0.0034, +0.0106] | 3/0/0 | +0.0138 |
| Roman-empire | hidden_mixing_finetune | combined - feature_only | +0.0092 | [-0.0027, +0.0210] | 3/0/0 | +0.0797 |
| Roman-empire | hidden_mixing_finetune | combined - combined_shuffled | +0.0097 | [+0.0001, +0.0193] | 3/0/0 | +0.0491 |
| Roman-empire | hidden_mixing_finetune | combined - combined_constant | +0.0088 | [+0.0042, +0.0133] | 3/0/0 | +0.0143 |
| Cora | residual_alpha | feature_only - fixed | +0.0067 | [-0.0051, +0.0184] | 3/0/0 | +0.1345 |
| Cora | residual_alpha | reliability_only - fixed | +0.0070 | [-0.0081, +0.0221] | 3/0/0 | +0.1844 |
| Cora | residual_alpha | combined - fixed | +0.0033 | [-0.0018, +0.0085] | 3/0/0 | +0.1091 |
| Cora | residual_alpha | shuffled_reliability - fixed | +0.0057 | [-0.0130, +0.0243] | 2/0/1 | +0.3211 |
| Cora | residual_alpha | constant_reliability - fixed | +0.0073 | [-0.0049, +0.0196] | 3/0/0 | +0.1235 |
| Cora | residual_alpha | zero_reliability - fixed | +0.0080 | [-0.0028, +0.0188] | 3/0/0 | +0.0863 |
| Cora | residual_alpha | combined_shuffled - fixed | +0.0050 | [+0.0025, +0.0075] | 3/0/0 | +0.0131 |
| Cora | residual_alpha | combined_constant - fixed | +0.0043 | [+0.0005, +0.0081] | 3/0/0 | +0.0390 |
| Cora | residual_alpha | reliability_only - feature_only | +0.0003 | [-0.0035, +0.0041] | 1/1/1 | +0.7418 |
| Cora | residual_alpha | true reliability - shuffled reliability | +0.0013 | [-0.0099, +0.0125] | 2/0/1 | +0.6595 |
| Cora | residual_alpha | true reliability - constant reliability | -0.0003 | [-0.0032, +0.0025] | 1/0/2 | +0.6667 |
| Cora | residual_alpha | true reliability - zero reliability | -0.0010 | [-0.0060, +0.0040] | 1/0/2 | +0.4778 |
| Cora | residual_alpha | combined - feature_only | -0.0033 | [-0.0113, +0.0047] | 0/0/3 | +0.2143 |
| Cora | residual_alpha | combined - combined_shuffled | -0.0017 | [-0.0068, +0.0035] | 0/1/2 | +0.2999 |
| Cora | residual_alpha | combined - combined_constant | -0.0010 | [-0.0100, +0.0080] | 1/1/1 | +0.6784 |
| Cora | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Cora | hidden_mixing_frozen | constant_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | zero_reliability - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | reliability_only - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0003 | [-0.0011, +0.0018] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_finetune | feature_only - fixed | +0.0077 | [-0.0253, +0.0407] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | reliability_only - fixed | +0.0067 | [-0.0220, +0.0354] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | combined - fixed | +0.0043 | [-0.0143, +0.0230] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0047 | [-0.0154, +0.0247] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | constant_reliability - fixed | +0.0050 | [-0.0165, +0.0265] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | zero_reliability - fixed | +0.0067 | [-0.0220, +0.0354] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | combined_shuffled - fixed | +0.0053 | [-0.0176, +0.0283] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | combined_constant - fixed | +0.0057 | [-0.0187, +0.0300] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | reliability_only - feature_only | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Cora | hidden_mixing_finetune | true reliability - shuffled reliability | +0.0020 | [-0.0066, +0.0106] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | true reliability - constant reliability | +0.0017 | [-0.0055, +0.0088] | 1/2/0 | +0.4226 |
| Cora | hidden_mixing_finetune | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Cora | hidden_mixing_finetune | combined - feature_only | -0.0033 | [-0.0177, +0.0110] | 0/2/1 | +0.4226 |
| Cora | hidden_mixing_finetune | combined - combined_shuffled | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Cora | hidden_mixing_finetune | combined - combined_constant | -0.0013 | [-0.0071, +0.0044] | 0/2/1 | +0.4226 |
| Citeseer | residual_alpha | feature_only - fixed | +0.0007 | [-0.0105, +0.0119] | 2/0/1 | +0.8218 |
| Citeseer | residual_alpha | reliability_only - fixed | -0.0010 | [-0.0141, +0.0121] | 2/0/1 | +0.7745 |
| Citeseer | residual_alpha | combined - fixed | -0.0023 | [-0.0211, +0.0165] | 2/0/1 | +0.6469 |
| Citeseer | residual_alpha | shuffled_reliability - fixed | -0.0013 | [-0.0451, +0.0424] | 2/0/1 | +0.9077 |
| Citeseer | residual_alpha | constant_reliability - fixed | +0.0013 | [-0.0297, +0.0324] | 2/0/1 | +0.8705 |
| Citeseer | residual_alpha | zero_reliability - fixed | +0.0007 | [-0.0329, +0.0342] | 2/0/1 | +0.9396 |
| Citeseer | residual_alpha | combined_shuffled - fixed | -0.0027 | [-0.0163, +0.0110] | 1/1/1 | +0.4899 |
| Citeseer | residual_alpha | combined_constant - fixed | +0.0017 | [-0.0331, +0.0365] | 2/0/1 | +0.8558 |
| Citeseer | residual_alpha | reliability_only - feature_only | -0.0017 | [-0.0055, +0.0021] | 0/1/2 | +0.1994 |
| Citeseer | residual_alpha | true reliability - shuffled reliability | +0.0003 | [-0.0307, +0.0314] | 1/1/1 | +0.9674 |
| Citeseer | residual_alpha | true reliability - constant reliability | -0.0023 | [-0.0216, +0.0170] | 1/1/1 | +0.6547 |
| Citeseer | residual_alpha | true reliability - zero reliability | -0.0017 | [-0.0231, +0.0198] | 1/1/1 | +0.7696 |
| Citeseer | residual_alpha | combined - feature_only | -0.0030 | [-0.0120, +0.0060] | 0/1/2 | +0.2863 |
| Citeseer | residual_alpha | combined - combined_shuffled | +0.0003 | [-0.0059, +0.0066] | 1/1/1 | +0.8399 |
| Citeseer | residual_alpha | combined - combined_constant | -0.0040 | [-0.0234, +0.0154] | 1/1/1 | +0.4686 |
| Citeseer | hidden_mixing_frozen | feature_only - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | reliability_only - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_frozen | combined - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | shuffled_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_frozen | constant_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_frozen | zero_reliability - fixed | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_frozen | combined_shuffled - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined_constant - fixed | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | reliability_only - feature_only | -0.0007 | [-0.0035, +0.0022] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_frozen | true reliability - shuffled reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | true reliability - constant reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | true reliability - zero reliability | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined - feature_only | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_frozen | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_finetune | feature_only - fixed | +0.0003 | [-0.0352, +0.0358] | 1/0/2 | +0.9715 |
| Citeseer | hidden_mixing_finetune | reliability_only - fixed | +0.0017 | [-0.0393, +0.0427] | 1/0/2 | +0.8772 |
| Citeseer | hidden_mixing_finetune | combined - fixed | -0.0050 | [-0.0205, +0.0105] | 0/1/2 | +0.2999 |
| Citeseer | hidden_mixing_finetune | shuffled_reliability - fixed | +0.0037 | [-0.0457, +0.0530] | 1/0/2 | +0.7794 |
| Citeseer | hidden_mixing_finetune | constant_reliability - fixed | +0.0027 | [-0.0425, +0.0478] | 1/0/2 | +0.8231 |
| Citeseer | hidden_mixing_finetune | zero_reliability - fixed | +0.0020 | [-0.0404, +0.0444] | 1/0/2 | +0.8579 |
| Citeseer | hidden_mixing_finetune | combined_shuffled - fixed | -0.0050 | [-0.0205, +0.0105] | 0/1/2 | +0.2999 |
| Citeseer | hidden_mixing_finetune | combined_constant - fixed | -0.0050 | [-0.0205, +0.0105] | 0/1/2 | +0.2999 |
| Citeseer | hidden_mixing_finetune | reliability_only - feature_only | +0.0013 | [-0.0044, +0.0071] | 1/2/0 | +0.4226 |
| Citeseer | hidden_mixing_finetune | true reliability - shuffled reliability | -0.0020 | [-0.0106, +0.0066] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_finetune | true reliability - constant reliability | -0.0010 | [-0.0053, +0.0033] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_finetune | true reliability - zero reliability | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_finetune | combined - feature_only | -0.0053 | [-0.0283, +0.0176] | 0/2/1 | +0.4226 |
| Citeseer | hidden_mixing_finetune | combined - combined_shuffled | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Citeseer | hidden_mixing_finetune | combined - combined_constant | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Chameleon | hidden_protocol | fixed: finetune - frozen | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | hidden_protocol | feature_only: finetune - frozen | -0.0037 | [-0.0346, +0.0273] | 1/1/1 | +0.6621 |
| Chameleon | hidden_protocol | reliability_only: finetune - frozen | -0.0051 | [-0.0271, +0.0169] | 0/2/1 | +0.4226 |
| Chameleon | hidden_protocol | combined: finetune - frozen | +0.0007 | [-0.0024, +0.0039] | 1/2/0 | +0.4226 |
| Chameleon | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Chameleon | hidden_protocol | constant_reliability: finetune - frozen | +0.0015 | [-0.0048, +0.0078] | 1/2/0 | +0.4226 |
| Chameleon | hidden_protocol | zero_reliability: finetune - frozen | +0.0007 | [-0.0076, +0.0091] | 1/1/1 | +0.7418 |
| Chameleon | hidden_protocol | combined_shuffled: finetune - frozen | -0.0029 | [-0.0309, +0.0250] | 1/1/1 | +0.6968 |
| Chameleon | hidden_protocol | combined_constant: finetune - frozen | +0.0022 | [-0.0072, +0.0116] | 1/2/0 | +0.4226 |
| Squirrel | hidden_protocol | fixed: finetune - frozen | +0.0000 | [+0.0000, +0.0000] | 0/3/0 | n/a |
| Squirrel | hidden_protocol | feature_only: finetune - frozen | -0.0022 | [-0.0119, +0.0074] | 0/2/1 | +0.4226 |
| Squirrel | hidden_protocol | reliability_only: finetune - frozen | -0.0016 | [-0.0089, +0.0057] | 1/0/2 | +0.4444 |
| Squirrel | hidden_protocol | combined: finetune - frozen | -0.0006 | [-0.0103, +0.0090] | 1/1/1 | +0.8020 |
| Squirrel | hidden_protocol | shuffled_reliability: finetune - frozen | -0.0029 | [-0.0174, +0.0116] | 1/1/1 | +0.4830 |
| Squirrel | hidden_protocol | constant_reliability: finetune - frozen | -0.0013 | [-0.0068, +0.0042] | 0/2/1 | +0.4226 |
| Squirrel | hidden_protocol | zero_reliability: finetune - frozen | -0.0010 | [-0.0051, +0.0032] | 0/2/1 | +0.4226 |
| Squirrel | hidden_protocol | combined_shuffled: finetune - frozen | -0.0006 | [-0.0034, +0.0021] | 0/2/1 | +0.4226 |
| Squirrel | hidden_protocol | combined_constant: finetune - frozen | +0.0003 | [-0.0011, +0.0017] | 1/2/0 | +0.4226 |
| Roman-empire | hidden_protocol | fixed: finetune - frozen | +0.0073 | [+0.0009, +0.0137] | 3/0/0 | +0.0390 |
| Roman-empire | hidden_protocol | feature_only: finetune - frozen | +0.0062 | [-0.0028, +0.0153] | 3/0/0 | +0.0971 |
| Roman-empire | hidden_protocol | reliability_only: finetune - frozen | +0.0105 | [+0.0022, +0.0188] | 3/0/0 | +0.0323 |
| Roman-empire | hidden_protocol | combined: finetune - frozen | +0.0121 | [+0.0039, +0.0203] | 3/0/0 | +0.0240 |
| Roman-empire | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0065 | [-0.0026, +0.0156] | 3/0/0 | +0.0925 |
| Roman-empire | hidden_protocol | constant_reliability: finetune - frozen | +0.0067 | [+0.0021, +0.0113] | 3/0/0 | +0.0242 |
| Roman-empire | hidden_protocol | zero_reliability: finetune - frozen | +0.0062 | [-0.0008, +0.0132] | 3/0/0 | +0.0617 |
| Roman-empire | hidden_protocol | combined_shuffled: finetune - frozen | +0.0065 | [+0.0012, +0.0118] | 3/0/0 | +0.0340 |
| Roman-empire | hidden_protocol | combined_constant: finetune - frozen | +0.0066 | [+0.0018, +0.0115] | 3/0/0 | +0.0280 |
| Cora | hidden_protocol | fixed: finetune - frozen | +0.0113 | [-0.0374, +0.0601] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | feature_only: finetune - frozen | +0.0190 | [-0.0628, +0.1008] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | reliability_only: finetune - frozen | +0.0180 | [-0.0594, +0.0954] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | combined: finetune - frozen | +0.0157 | [-0.0517, +0.0831] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0163 | [-0.0518, +0.0845] | 2/1/0 | +0.4107 |
| Cora | hidden_protocol | constant_reliability: finetune - frozen | +0.0163 | [-0.0539, +0.0866] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | zero_reliability: finetune - frozen | +0.0180 | [-0.0594, +0.0954] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | combined_shuffled: finetune - frozen | +0.0167 | [-0.0550, +0.0884] | 1/2/0 | +0.4226 |
| Cora | hidden_protocol | combined_constant: finetune - frozen | +0.0170 | [-0.0561, +0.0901] | 1/2/0 | +0.4226 |
| Citeseer | hidden_protocol | fixed: finetune - frozen | +0.0047 | [-0.0095, +0.0188] | 2/1/0 | +0.2911 |
| Citeseer | hidden_protocol | feature_only: finetune - frozen | +0.0050 | [-0.0187, +0.0287] | 1/1/1 | +0.4598 |
| Citeseer | hidden_protocol | reliability_only: finetune - frozen | +0.0070 | [-0.0210, +0.0350] | 2/1/0 | +0.3945 |
| Citeseer | hidden_protocol | combined: finetune - frozen | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Citeseer | hidden_protocol | shuffled_reliability: finetune - frozen | +0.0090 | [-0.0276, +0.0456] | 2/1/0 | +0.4009 |
| Citeseer | hidden_protocol | constant_reliability: finetune - frozen | +0.0080 | [-0.0243, +0.0403] | 2/1/0 | +0.3981 |
| Citeseer | hidden_protocol | zero_reliability: finetune - frozen | +0.0073 | [-0.0221, +0.0368] | 2/1/0 | +0.3958 |
| Citeseer | hidden_protocol | combined_shuffled: finetune - frozen | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |
| Citeseer | hidden_protocol | combined_constant: finetune - frozen | -0.0003 | [-0.0018, +0.0011] | 0/2/1 | +0.4226 |

## Screening Rule

- A mechanism is a screening candidate when it wins at least 2/3 runs, has a mean gain of at least 0.005, and true reliability exceeds its shuffled or constant counterpart.
- Three-run intervals are descriptive only. Confirm selected mechanisms with 10 official splits or seeds before making statistical claims.
