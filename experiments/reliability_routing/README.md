# Reliability-Aware Linear Graph Transformer: Minimal Experiment

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
python run_batch.py --graph-types heterophily homophily noisy --models mlp gcn linear_gt q_only_gt k_only_gt qk_gt gate_gt reliability_gt --seeds 0 1 2 3 4
```

快速 smoke test：

```bash
python run_batch.py --graph-types heterophily --models linear_gt q_only_gt k_only_gt qk_gt gate_gt reliability_gt --seeds 0 --num-nodes 180 --epochs 2 --patience 2 --hidden-dim 32
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
python run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components degree --tag rel_only_degree --device cuda
python run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components local_similarity --tag rel_only_local_sim --device cuda
python run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components neighbor_variance --tag rel_only_neighbor_var --device cuda
python run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components rwse --tag rel_only_rwse --device cuda
```

Leave-one-component-out 消融示例：

```bash
python run_batch.py --models gate_gt reliability_gt --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --reliability-components local_similarity neighbor_variance rwse --tag rel_without_degree --device cuda
```

`reliability_qk` 只包含 `degree + RWSE`。因此只选择
`local_similarity` 或 `neighbor_variance` 时，Q/K reliability 输入会被置零；
这类实验主要用于分析 routing gate。

## Learnable ReliabilityEncoder 对照

先跑当前 separate-head 基线与 branch-specific encoded 版本：

```bash
python run_batch.py --models gate_gt gate_gt_encoded qk_gt qk_gt_encoded reliability_gt reliability_gt_encoded --graph-types heterophily homophily noisy --seeds 0 1 2 3 4 5 6 7 8 9 --tag reliability_encoder_compare --device cuda
```

建议先在完整 reliability basis 上比较 encoder；只有 encoded 版本出现稳定增益后，
再组合 component 消融。当前版本暂不加入 hidden-based dynamic reliability。

消融诊断中的 gate correlation 始终使用 mask 前的原始 reliability 信号，因此即使
某个 component 没有作为输入，仍可观察 gate 是否与该真实结构信号对齐。

先跑异配图：

```bash
python run_synthetic.py --graph-type heterophily --model mlp
python run_synthetic.py --graph-type heterophily --model gcn
python run_synthetic.py --graph-type heterophily --model linear_gt
python run_synthetic.py --graph-type heterophily --model reliability_gt
```

再跑同配图和噪声图：

```bash
python run_synthetic.py --graph-type homophily --model reliability_gt
python run_synthetic.py --graph-type noisy --model reliability_gt
```

如果机器有 CUDA：

```bash
python run_synthetic.py --graph-type heterophily --model reliability_gt --device cuda
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
