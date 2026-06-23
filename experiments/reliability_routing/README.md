# Reliability-Aware Linear Graph Transformer: Minimal Experiment

## Current Main Pipeline

The current research pipeline uses complete experts and logits-level routing:

- `LocalExpert`: two-layer PyG GCN.
- `GlobalExpert`: independent linear-attention classifier.
- `fixed_alpha`: fixed logits interpolation.
- `ordinary_gate`: node-wise gate without reliability information.
- `reliability_gate`: same gate architecture with reliability information.
- Learned gates start exactly at `alpha=0.5`; epoch `-1` records the
  pre-update gate and remains eligible for early-stopping restoration.
- Main edge protocol: symmetrized undirected edges.
- Directed sensitivity: `source_to_target` and `target_to_source`.

Main batch entry point:

```bash
CUDA_VISIBLE_DEVICES=0 python run_expert_fusion_suite.py \
  --datasets Cora Citeseer Pubmed Chameleon Squirrel Actor \
  --models gcn_pyg global_only ordinary_gate reliability_gate \
  --fixed-alphas 0 0.25 0.5 0.75 1.0 \
  --edge-protocol undirected \
  --runs 10 \
  --data-root data \
  --out-dir outputs/expert_fusion_undirected \
  --no-download \
  --device cuda
```

The earlier synthetic and Q/K scripts are archived under
`scripts/legacy_synthetic/`. Q/K modulation is frozen until reliability-aware
routing consistently exceeds the ordinary gate.

### One-command validation matrix

Run the recommended multi-claim sanity validation:

```bash
CUDA_VISIBLE_DEVICES=0 python run_expert_validation_matrix.py \
  --profile sanity \
  --include-directed \
  --include-components \
  --data-root data \
  --out-dir outputs/expert_validation_sanity \
  --no-download \
  --device cuda
```

Run the full confirmatory matrix:

```bash
CUDA_VISIBLE_DEVICES=0 python run_expert_validation_matrix.py \
  --profile full \
  --include-directed \
  --include-components \
  --data-root data \
  --out-dir outputs/expert_validation_full \
  --no-download \
  --device cuda
```

The matrix tests GCN/global fallback, ordinary gate versus validation-selected
fixed alpha, reliability gate versus ordinary gate, expert complementarity,
directed-edge sensitivity, and individual reliability components. It writes
`validation_findings.csv` and `validation_report.md`.

这个目录用于做第一步简单实验验证，不依赖 PyTorch Geometric。实验目标不是直接追 SOTA，而是快速检查下面两个设计是否有信号：

1. structural reliability state `r_i` 调制 linear attention 的 Q/K；
2. reliability-aware routing gate 自适应融合 local GNN 与 global linear attention。

## 文件结构

- `src/data.py`: 合成同配、异配、混合、噪声图，并计算 reliability features。
- `src/models.py`: MLP、GCN、普通 LinearGT、ReliabilityGT。
- `run_synthetic.py`: 训练与评估入口。
- `requirements.txt`: 最小依赖。

## 模型对照

- `mlp`: 只用节点特征，不用图结构。
- `gcn`: 标准两层 GCN。
- `linear_gt`: local GCN + global linear attention，固定比例融合。
- `q_only_gt`: 只用 `r_qk` 调制 Q，不调制 K。
- `k_only_gt`: 只用 `r_qk` 调制 K，不调制 Q。
- `qk_gt`: 只加入 reliability-aware Q/K modulation，不使用 routing gate。当前版本采用小幅乘性残差调制：去掉 beta、最后层 zero-init、可学习调制强度从接近 0 开始。
- `gate_gt`: 只加入 reliability-aware routing gate，不调制 Q/K。
- `reliability_gt`: `r_i` 调制 Q/K，并使用 node-wise routing gate。
- `qk_gt_encoded`: 用 learnable `ReliabilityEncoder` 编码 `degree + RWSE`，再接 Q/K head。
- `gate_gt_encoded`: 用 learnable `ReliabilityEncoder` 编码完整 reliability，再输入 routing gate。
- `reliability_gt_encoded`: Q/K 与 gate 使用各自的 branch-specific encoder，输入视图与 static 版本一致。

原有模型属于 `static reliability basis + separate learnable heads`。带 `_encoded`
后缀的模型用于检验：在不改变各分支 reliability 输入的前提下，更深的 learned
reliability representation 是否优于当前浅层投影。encoder 是逐层构造的，不跨层共享。

## 推荐运行命令

环境配置见 [ENV_SETUP.md](ENV_SETUP.md)。

批量跑一组实验：

```bash
python scripts/legacy_synthetic/run_batch.py --graph-types heterophily homophily noisy --models mlp gcn linear_gt q_only_gt k_only_gt qk_gt gate_gt reliability_gt --seeds 0 1 2 3 4
```

快速 smoke test：

```bash
python scripts/legacy_synthetic/run_batch.py --graph-types heterophily --models linear_gt q_only_gt k_only_gt qk_gt gate_gt reliability_gt --seeds 0 --num-nodes 180 --epochs 2 --patience 2 --hidden-dim 32
```

批量脚本会输出：

- `outputs/batch_<tag>/raw_results.csv`
- `outputs/batch_<tag>/summary.csv`

## Reliability component 消融

完整 reliability basis 包含：

```text
degree local_similarity neighbor_variance rwse
```

使用 `--reliability-components` 选择保留的组件。未选择的维度会被置零，
张量维度和模型参数量保持不变。

单组件消融：

```bash
python scripts/legacy_synthetic/run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components degree --tag rel_only_degree --device cuda
python scripts/legacy_synthetic/run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components local_similarity --tag rel_only_local_sim --device cuda
python scripts/legacy_synthetic/run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components neighbor_variance --tag rel_only_neighbor_var --device cuda
python scripts/legacy_synthetic/run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components rwse --tag rel_only_rwse --device cuda
```

Leave-one-component-out 消融示例：

```bash
python scripts/legacy_synthetic/run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components local_similarity neighbor_variance rwse --tag rel_without_degree --device cuda
```

`reliability_qk` 只包含 `degree + RWSE`。因此只选择
`local_similarity` 或 `neighbor_variance` 时，Q/K reliability 输入会被置零；
这类实验主要用于分析 routing gate。

## Learnable ReliabilityEncoder 对照

先跑当前 separate-head 基线与 branch-specific encoded 版本：

```bash
python scripts/legacy_synthetic/run_batch.py --models gate_gt gate_gt_encoded qk_gt qk_gt_encoded reliability_gt reliability_gt_encoded --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --tag reliability_encoder_compare --device cuda
```

建议先在完整 reliability basis 上比较 encoder；只有 encoded 版本出现稳定增益后，
再组合 component 消融。当前版本暂不加入 hidden-based dynamic reliability。

消融诊断中的 gate correlation 始终使用 mask 前的原始 reliability 信号，因此即使
某个 component 没有作为输入，仍可观察 gate 是否与该真实结构信号对齐。

先跑异配图：

```bash
python scripts/legacy_synthetic/run_synthetic.py --graph-type heterophily --model mlp
python scripts/legacy_synthetic/run_synthetic.py --graph-type heterophily --model gcn
python scripts/legacy_synthetic/run_synthetic.py --graph-type heterophily --model linear_gt
python scripts/legacy_synthetic/run_synthetic.py --graph-type heterophily --model reliability_gt
```

再跑同配图和噪声图：

```bash
python scripts/legacy_synthetic/run_synthetic.py --graph-type homophily --model reliability_gt
python scripts/legacy_synthetic/run_synthetic.py --graph-type noisy --model reliability_gt
```

如果机器有 CUDA：

```bash
python scripts/legacy_synthetic/run_synthetic.py --graph-type heterophily --model reliability_gt --device cuda
```

## Q/K modulation 当前实现

当前代码使用两套 reliability 输入：

```text
r_gate = degree + local_similarity + neighbor_variance + RWSE
r_qk   = degree + RWSE
```

`gate_gt` 和 `reliability_gt` 的 routing gate 使用 `r_gate`。`qk_gt` 和 `reliability_gt` 的 Q/K modulation 使用更干净的 `r_qk`，避免把 local similarity / neighbor variance 这类局部可靠性信号直接注入 attention matching space。

旧版 Q/K modulation 使用 FiLM-style：

```text
q = gamma_q * q + beta_q
k = gamma_k * k + beta_k
```

消融结果显示这个版本会扰乱 attention formation。当前版本改成更保守的 QK-Mul-Small-ZeroInit：

```text
q = gamma_q * q
k = gamma_k * k
gamma = 1 + sigmoid(strength) * 0.5 * tanh(delta)
```

其中 `rel_proj` 最后一层使用 zero initialization，`strength` 初始化为 `-5.0`，所以训练开始时近似普通 `linear_gt`，再由模型自己学习是否打开 Q/K 调制。

批量结果会记录诊断字段：

- `qk_strength_mean`: `sigmoid(qk_mod_strength)` 的层均值。
- `qk_strength_layer1`, `qk_strength_layer2`: 分层 Q/K 调制强度。
- `qk_gamma_q_abs_dev_mean`, `qk_gamma_k_abs_dev_mean`: Q/K gamma 偏离 1 的平均幅度。
- `qk_gamma_q_std`, `qk_gamma_k_std`: Q/K gamma 的标准差。
- `qk_gamma_q_abs_dev_max`, `qk_gamma_k_abs_dev_max`: Q/K gamma 最大偏移。
- `gate_corr_degree`
- `gate_corr_local_similarity`
- `gate_corr_neighbor_variance`
- `gate_corr_rwse_mean`
- `gate_corr_layer1_local_similarity`
- `gate_corr_layer2_local_similarity`

## 结果解读

输出中的 `test_acc_at_best_val` 是验证集最佳时对应的测试准确率。

`gate_local_similarity_corr` 只对 `reliability_gt` 有意义。它表示 routing gate 与 local feature similarity 的相关性。若为正，说明局部邻居越相似，模型越倾向 local branch；这与课题假设一致。

## 下一步

如果合成实验能看到稳定趋势，再迁移到真实数据集：

- Cora / Citeseer / Pubmed / ogbn-arxiv
- Chameleon / Squirrel / Actor
- Roman-empire / Amazon-ratings / Minesweeper / Tolokers / Questions

真实数据集建议第二步接入 PyTorch Geometric 或直接复用 SGFormer / Polynormer 的数据管线。

## Confirmatory synthetic finalists

冻结模型结构后，运行预注册的六个 finalist 对照：

```bash
CUDA_VISIBLE_DEVICES=0 python scripts/legacy_synthetic/run_synthetic_finalists.py \
  --seeds 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 \
  --device cuda
```

默认候选：

- heterophily: `gate_gt only local_similarity`, `reliability_gt without neighbor_variance`
- homophily: `gate_gt only RWSE`, `reliability_gt only local_similarity`
- noisy: `gate_gt only degree`, `reliability_gt only RWSE`

脚本会将每个候选与同模型 full reliability 进行同 seed 配对比较。

## Real dataset pipeline

先安装 PyG，然后校验/下载数据：

```bash
python prepare_real_datasets.py \
  --datasets Cora Citeseer Pubmed Chameleon Squirrel Actor \
  --data-root data \
  --report outputs/real_dataset_validation.json
```

本地文件不会因为目录存在就被直接信任。校验器会检查标准规模、标签、边索引、
官方 split、有限值和 raw 文件 SHA-256。缺失数据通过 PyG 官方 dataset loader 下载。

运行第一批真实数据：

```bash
CUDA_VISIBLE_DEVICES=0 python run_real_suite.py \
  --datasets Cora Citeseer Pubmed Chameleon Squirrel Actor \
  --models mlp gcn linear_gt qk_gt gate_gt reliability_gt \
  --runs 10 \
  --device cuda
```

协议：

- Cora/CiteSeer/PubMed 使用 public split，10 runs 对应 10 个训练随机种子。
- Chameleon/Squirrel/Actor 使用 10 个官方 Geom-GCN splits。
- 真实图 RWSE 使用固定种子的 Monte Carlo return probability 估计，避免 PubMed 上的 dense adjacency power。
- 输出位于 `outputs/real_suite/`，包括数据校验、逐模型 CSV、summary、paired comparisons 和初步分析报告。

### GCN implementation and local-branch diagnostics

First compare the custom sparse GCN, PyG `GCNConv`, and the GT local-only path
under exactly the same training settings:

```bash
CUDA_VISIBLE_DEVICES=0 python run_real_suite.py \
  --datasets Cora Citeseer Pubmed Chameleon Squirrel Actor \
  --models gcn gcn_pyg local_only_gt gate_gt reliability_gt \
  --runs 10 \
  --data-root data \
  --out-dir outputs/real_gcn_diagnostic \
  --no-download \
  --device cuda
```

Then reproduce the classic GCN protocol on the three Planetoid datasets. This
profile fixes hidden size 16, dropout 0.5, Adam learning rate 0.01, first-layer
weight decay 5e-4, 200 epochs, and rolling validation-loss early stopping:

```bash
CUDA_VISIBLE_DEVICES=0 python run_real_suite.py \
  --datasets Cora Citeseer Pubmed \
  --models gcn_pyg \
  --training-profile classic_gcn \
  --runs 10 \
  --data-root data \
  --out-dir outputs/real_gcn_classic \
  --no-download \
  --device cuda
```

GT result CSV files now include `gate_mean`, `gate_std`, gate range,
local/global/mixed branch norms, and their mean cosine similarity.

# Preference-routing diagnostic

The preference-routing experiment tests whether the handcrafted reliability
state predicts which frozen expert is correct. Training preference labels are
generated with stratified out-of-fold expert predictions:

- local correct, global wrong: local preference (`1`)
- local wrong, global correct: global preference (`0`)
- both correct or both wrong: ignored

It compares `reliability_only`, `node_feature_only`, and `combined` routers.
Primary metrics are preference ROC-AUC, balanced accuracy, and routing accuracy.
Final routed node accuracy is reported only as a secondary metric.

Each trained router is evaluated with three hard-routing decision rules:

- `fixed_0.5`: the raw sigmoid threshold.
- `preference_threshold`: selected on validation preference balanced accuracy.
- `utility_threshold`: selected on validation routed node accuracy after the
  router checkpoint is fixed.

Utility routing is compared against a validation-selected best single expert,
a validation-selected fixed-alpha interpolation, and the test oracle union
(diagnostic upper bound only).

Two checkpoint variants are reported separately:

- Preference-selected checkpoint plus post-hoc utility threshold.
- Utility-selected checkpoint plus utility threshold.

The utility threshold is conservative by default: thresholds within one
validation node of the best accuracy are eligible, and the one that switches
the fewest nodes away from the stronger validation expert is selected. Set
`--utility-epsilon-nodes 0` for strict validation-accuracy maximization.

The real-data loader also supports the officially undirected heterophily
benchmarks `Roman-empire`, `Amazon-ratings`, `Minesweeper`, `Tolokers`, and
`Questions` through PyG's `HeterophilousGraphDataset`.

Sanity run:

```bash
CUDA_VISIBLE_DEVICES=0 python run_preference_routing_suite.py \
  --datasets Chameleon Actor Roman-empire \
  --runs 1 \
  --oof-folds 3 \
  --expert-epochs 100 \
  --router-epochs 80 \
  --patience 30 \
  --data-root data \
  --out-dir outputs/preference_routing_sanity \
  --no-download \
  --device cuda
```

Formal run:

```bash
CUDA_VISIBLE_DEVICES=0 python run_preference_routing_suite.py \
  --datasets Cora Citeseer Pubmed Chameleon Squirrel Actor \
             Roman-empire Amazon-ratings Minesweeper \
  --routers reliability_only node_feature_only combined \
  --runs 10 \
  --oof-folds 5 \
  --expert-epochs 500 \
  --router-epochs 300 \
  --patience 100 \
  --data-root data \
  --out-dir outputs/preference_routing_full \
  --no-download \
  --device cuda
```

# Representation-control screening

`run_representation_control_suite.py` evaluates three isolated protocols:

- `residual_alpha`: frozen local/global experts with a conservative node-wise
  adjustment around the validation-selected fixed logit alpha.
- `hidden_mixing_frozen`: hidden-state mixing initialized from a
  validation-selected fixed hidden alpha; the backbone stays in evaluation
  mode and only the controller is trained.
- `hidden_mixing_finetune`: the same initialization followed by end-to-end
  fine-tuning, measuring performance potential rather than controller-only
  attribution.

Both families use the same parameterization for true, shuffled, constant, and
zero reliability controls. The initial interpolation weight is small, so every
dynamic model starts close to its fixed baseline even when the selected alpha
is exactly zero or one.

`zero_reliability` is a learnable zero-input reliability controller, not the
absence of a controller. The `fixed` control is the true no-controller
baseline.

For `hidden_mixing_frozen`, `fixed` is the untouched selected baseline. For
`hidden_mixing_finetune`, `fixed` is the same-architecture fixed-mixing
fine-tuning control.

Recommended three-run screening:

```bash
CUDA_VISIBLE_DEVICES=0 python run_representation_control_suite.py \
  --datasets Chameleon Squirrel Roman-empire Cora Citeseer \
  --families residual_alpha hidden_mixing_frozen hidden_mixing_finetune \
  --controls fixed feature_only reliability_only combined \
             shuffled_reliability constant_reliability zero_reliability \
             combined_shuffled combined_constant \
  --runs 3 \
  --fixed-alphas 0.0 0.25 0.5 0.75 1.0 \
  --max-adjustment 0.1 \
  --lambda-init 0.001 \
  --expert-epochs 300 \
  --control-epochs 200 \
  --patience 60 \
  --data-root data \
  --out-dir outputs/representation_control_screen_v1 \
  --no-download \
  --device cuda
```

The suite writes per-run CSV files, `summary.csv`,
`paired_comparisons.csv`, and `analysis.md`. The shared expert and hidden
backbone caches prevent each control variant from retraining the same baseline.

The coarse alpha grid above is intended for screening. Formal confirmation
should use a 0.05-step grid:

```text
0.00 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50
0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00
```

## Iterative local-global relation control

The iterative relation families keep each layer's local and global
representations fixed inside an inner refinement loop. Shared controller
parameters update only a relation state and a channel-wise mixing correction:

```text
base = alpha0 * local + (1 - alpha0) * global
relation = (channel_alpha - alpha0) * (local - global)
output = base + relation
```

The correction head is zero-initialized, so every iterative model starts
exactly at the validation-selected fixed hidden-mixing baseline. The total
channel adjustment is bounded by `--max-adjustment`.

Available families:

- `iterative_relation_frozen`: freeze the selected hidden backbone and train
  only the shared iterative relation controller.
- `iterative_relation_finetune`: initialize from the same backbone and
  fine-tune the complete model.

The suite defaults now target the iterative-relation question:

```text
datasets = Roman-empire, Amazon-ratings, Cora, Pubmed
families = iterative_relation_frozen, iterative_relation_finetune
```

It prints the complete number of requested training runs before launching.
Other representation-control families remain available through explicit
`--families`.

`Minesweeper`, `Tolokers`, and `Questions` are imbalanced binary benchmarks.
For these datasets, checkpoint selection, fixed-alpha selection, summary
tables, and paired comparisons use ROC-AUC. Accuracy and macro-F1 remain in the
CSV as secondary diagnostics. Other datasets continue to use accuracy as the
primary metric.

Recommended `K=1,2,3` screening with one shared fixed-backbone cache:

```bash
for K in 1 2 3; do
  CUDA_VISIBLE_DEVICES=0 python run_representation_control_suite.py \
    --datasets Roman-empire Amazon-ratings Cora Pubmed \
    --families iterative_relation_frozen iterative_relation_finetune \
    --controls fixed feature_only reliability_only combined \
               shuffled_reliability constant_reliability \
               combined_shuffled combined_constant \
    --relation-steps "${K}" \
    --runs 3 \
    --fixed-alphas 0.0 0.25 0.5 0.75 1.0 \
    --max-adjustment 0.1 \
    --expert-epochs 300 \
    --control-epochs 200 \
    --patience 60 \
    --data-root data \
    --backbone-cache-dir outputs/iterative_relation_shared_backbone_cache \
    --out-dir "outputs/iterative_relation_k${K}_screen" \
    --no-download \
    --device cuda
done
```

`K=0` is represented by the `fixed` control. The 0.25 alpha grid above is for
screening. Formal confirmation should pass the 0.05-step grid listed in the
previous section. Result CSV files include relation-state update-gate,
relation-norm, and channel-wise alpha diagnostics.

### Additional undirected heterophily screening

After selecting `K=1`, screen the three remaining native-undirected binary
benchmarks with the smaller reliability-focused control set:

```bash
CUDA_VISIBLE_DEVICES=1 python run_representation_control_suite.py \
  --datasets Minesweeper Tolokers Questions \
  --families iterative_relation_frozen iterative_relation_finetune \
  --controls fixed feature_only reliability_only \
             shuffled_reliability constant_reliability \
  --edge-protocol undirected \
  --runs 3 \
  --relation-steps 1 \
  --fixed-alphas 0.0 0.25 0.5 0.75 1.0 \
  --max-adjustment 0.1 \
  --expert-epochs 300 \
  --control-epochs 200 \
  --patience 60 \
  --data-root data \
  --backbone-cache-dir outputs/iterative_relation_binary_shared_backbone \
  --out-dir outputs/iterative_relation_binary_k1_screen \
  --no-download \
  --device cuda
```

This is `3 datasets x 2 families x 5 controls x 3 runs = 90` requested run
records. The suite uses ROC-AUC for checkpoint selection and comparisons on
all three datasets.
