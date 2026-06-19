# Experiment Outputs

本目录保存 Reliability-Aware Graph Transformer 项目的实验结果。2026-06-19
之前生成的结果已按实验目的归档，后续实验仍可直接写入 `outputs/`，不会覆盖
归档内容。

## Directory Layout

```text
outputs/
├── README.md
├── archive_manifest.csv
└── archive/
    └── 2026-06-19/
        ├── 01_synthetic_baselines/
        ├── 02_qk_diagnostics/
        ├── 03_reliability_ablation/
        ├── 04_real_data/
        ├── 05_combined_analysis/
        └── 99_legacy_single_runs/
```

本次归档包含 29 个实验条目、108 个文件，约 0.78 MiB。归档过程只移动文件，
没有删除或修改原始 CSV、JSON 和 Markdown 内容。

## Archive Categories

### 01_synthetic_baselines

Synthetic 数据上的基础模型比较和早期架构消融。

- `batch_main/`: MLP、GCN、LinearGT、Reliability-GT 等主模型比较。
- `batch_ablation_full/`: Q-only、K-only、QK、gate 和完整模型消融。
- 每个实验目录中的 `raw_results.csv` 保存逐 seed 结果。
- `summary.csv` 保存按 graph type 和 model 汇总的均值与标准差。

### 02_qk_diagnostics

用于判断 Q/K modulation 强度是否过弱，以及不同初始化或固定强度是否有效。

- `batch_qk_init_m5/`, `batch_qk_init_m3/`, `batch_qk_init_m2/`:
  learnable strength 初始化 sweep。
- `batch_qk_fixed_002/`, `batch_qk_fixed_005/`, `batch_qk_fixed_010/`:
  固定 Q/K strength 实验。
- `batch_qk_residual_full/`, `batch_qk_residual_repeat/`:
  residual modulation 版本及重复实验。
- `batch_diagnostics_n10_full/`: 10 seeds 的 Q/K 与 gate 诊断。
- `batch_qk_clean_reliability_full/`: 使用更干净 Q/K reliability 输入的实验。

分析时优先查看各目录的 `summary.csv`，需要检查 seed 波动时再查看
`raw_results.csv`。

### 03_reliability_ablation

Reliability component 和 learnable encoder 的完整消融结果。

- `batch_reliability_encoder_compare/`: static reliability 与 encoded reliability
  的直接比较。
- `batch_rel_only_*`: 每次仅保留一个 reliability component。
- `batch_rel_without_*`: 每次移除一个 reliability component。
- `suite_config.json`: 对应实验的模型、组件、seed 和训练超参数。

这一组实验统一使用 3 类 synthetic graph、10 seeds、900 个节点、hidden
dimension 64、300 epochs 和 CUDA。

### 04_real_data

六个真实数据集的第一轮完整实验。

```text
real_suite/
├── <Dataset>_<Model>.csv
├── <Dataset>_validation.json
├── dataset_validation.json
├── suite_config.json
├── summary.csv
├── paired_comparisons.csv
└── preliminary_analysis.md
```

数据集包括 Cora、Citeseer、Pubmed、Chameleon、Squirrel 和 Actor；模型包括
MLP、custom GCN、LinearGT、QK-GT、Gate-GT 和 Reliability-GT，每组 10 runs。

注意：这是加入 `gcn_pyg`、`local_only_gt` 和经典 GCN protocol 之前生成的
结果。因此它适合保留为第一轮真实数据基线，但不应替代后续的
`real_gcn_diagnostic` 和 `real_gcn_classic` 实验。

推荐阅读顺序：

1. `real_suite/preliminary_analysis.md`
2. `real_suite/summary.csv`
3. `real_suite/paired_comparisons.csv`
4. 单个 `<Dataset>_<Model>.csv`

`real_dataset_validation.json` 是归档前位于 `outputs/` 根目录的数据校验报告；
`real_suite/dataset_validation.json` 是真实数据 suite 内保存的同轮校验报告。

### 05_combined_analysis

跨 reliability encoder 和 component ablation 的综合分析。

- `preliminary_analysis.md`: 当前最完整的文字分析。
- `component_ablation_summary.csv`: component 消融汇总。
- `encoder_paired_comparisons.csv`: encoded 与 static 版本的配对比较。
- `suite_manifest.json`: 分析所依赖的实验清单。

### 99_legacy_single_runs

项目早期直接写入 `outputs/` 根目录的单次 synthetic CSV。它们缺少完整的
suite 配置和统一汇总，仅用于追溯早期开发结果，不建议用于最终论文表格。

## File Conventions

- `raw_results.csv`: 每个 seed/run 的原始结果，是重新统计的主要数据源。
- `summary.csv`: 按数据集或 graph type 汇总的均值和标准差。
- `suite_config.json`: 实验参数和代码 fingerprint。
- `dataset_validation.json`: 数据规模、特征、类别和 split 校验。
- `paired_comparisons.csv`: 相同 split/seed 下的模型配对差值。
- `preliminary_analysis.md`: 脚本自动生成的初步分析。

完整归档索引见 `archive_manifest.csv`。其中记录了每个条目的分类、文件数量、
大小、是否包含 raw results、summary 和 config，以及归档后的相对路径。

## New Experiments

当前主线已经切换到可恢复 GCN 的 logits-level expert fusion。主实验命令：

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

该实验先独立训练 LocalExpert 和 GlobalExpert，再冻结 expert 训练 gate。
`fixed_alpha_100` 必须与 `gcn_pyg` 完全恢复，ordinary gate 与 reliability
gate 使用相同参数结构。

一次性验证 fallback、gate、reliability、互补性、edge protocol 和 reliability
components：

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

新的真实数据诊断实验建议写入独立目录：

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

经典 GCN 复现实验：

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

不要将新的结果直接写入 `outputs/archive/`。完成一轮实验并确认结果完整后，
再按日期建立新的归档批次。
