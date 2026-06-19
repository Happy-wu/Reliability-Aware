# Preference Routing 正式实验解读

## 实验完整性

- 实际运行数据集：Chameleon、Squirrel、Actor、Roman-empire、Amazon-ratings、Minesweeper。
- 每个数据集计划 10 个 split，每个 split 比较 reliability-only、node-feature-only、combined。
- 除 Minesweeper 外均为 10/10 有效。
- Minesweeper 仅 7/10 有效，另外 3 个 split 的 validation preference 只有单一类别。
- 本轮没有运行 Cora、Citeseer、Pubmed。

## 核心问题一：reliability 能否预测 expert preference？

| 数据集 | Reliability-only AUC | 95% CI | 判断 |
|---|---:|---:|---|
| Chameleon | 0.6606 | [0.6219, 0.6994] | 强支持 |
| Squirrel | 0.6098 | [0.5864, 0.6331] | 支持 |
| Actor | 0.5279 | [0.5098, 0.5460] | 信号很弱 |
| Roman-empire | 0.6997 | [0.6899, 0.7094] | 强支持 |
| Amazon-ratings | 0.5580 | [0.5377, 0.5783] | 支持 |
| Minesweeper | 0.5911 | [0.5128, 0.6695] | 样本不足，不宜作为主证据 |

对六个数据集的检验做 Holm 校正后，上述 AUC 高于 0.5 的统计结果仍然成立；但 Actor 的实际效应很小，Minesweeper 有有效 split 缺失问题。

因此，当前四类 reliability 不是完全无效的静态统计量。它们确实包含“局部专家还是全局专家更可能正确”的预测信息。

## 核心问题二：reliability 是否提供 feature 之外的增量信息？

Combined 相对 node-feature-only 的 AUC 配对差值：

| 数据集 | AUC 差值 | 95% CI |
|---|---:|---:|
| Chameleon | +0.0600 | [+0.0316, +0.0884] |
| Squirrel | +0.0643 | [+0.0367, +0.0918] |
| Actor | +0.0116 | [-0.0229, +0.0460] |
| Roman-empire | +0.0705 | [+0.0594, +0.0816] |
| Amazon-ratings | +0.0274 | [+0.0083, +0.0465] |
| Minesweeper | -0.0218 | [-0.0898, +0.0462] |

Holm 校正后，Chameleon、Squirrel、Roman-empire、Amazon-ratings 仍显著为正。

其中 Roman-empire 和 Amazon-ratings 是官方原生无向异配图。因此，正向结果不能仅用 Chameleon/Squirrel 的边方向问题解释，预设的“至少两个无向异配数据集上 combined 超过 feature-only”继续标准已经达到。

## 核心问题三：为什么最终分类准确率仍然没有明显提高？

当前阈值按 validation preference balanced accuracy 选择。这会主动照顾少数 preference 类别，但最终节点分类准确率更偏好选择总体更强的专家。

结果表现为：

- Chameleon、Squirrel：router 的 preference balanced accuracy 提升，但最终分类仍低于直接选择 local expert。
- Roman-empire：combined AUC 达到 0.8379，但最终分类仍低于直接选择 global expert。
- Actor：信号弱，router 低于 global expert。
- Amazon-ratings：combined 最终准确率 0.4225，高于 majority baseline 0.4142，但配对 CI 仍跨 0。
- Minesweeper：两个专家几乎一样，oracle 空间只有约 0.33 个百分点。

因此，这轮实验已经证明“存在可预测信号”，但尚未证明“当前决策规则能把信号转化为总体分类收益”。这是两个不同命题。

## 数据集层面的可利用空间

| 数据集 | Preference 节点占比 | 最佳单专家 | Oracle 上界 | Oracle gap |
|---|---:|---:|---:|---:|
| Actor | 29.0% | 0.3526 | 0.4731 | +0.1205 |
| Amazon-ratings | 30.0% | 0.4153 | 0.5581 | +0.1428 |
| Chameleon | 36.9% | 0.6436 | 0.7439 | +0.1002 |
| Minesweeper | 0.8% | 0.8007 | 0.8040 | +0.0033 |
| Roman-empire | 41.3% | 0.6599 | 0.7291 | +0.0692 |
| Squirrel | 40.8% | 0.4736 | 0.5958 | +0.1222 |

Minesweeper 不适合当前 expert-preference 诊断，因为两个专家几乎从不形成有用分歧。

## 结论

论文课题的 reliability 出发点没有失败。更准确的结论是：

> 手工构造的 structural reliability state 对 expert preference 具有稳定预测信息，并在两个原生无向异配数据集上提供了原始节点特征之外的增量信息；但当前基于 balanced preference 的决策阈值尚不能稳定提高总体节点分类准确率。

下一阶段不应回到 Q/K modulation，也不需要继续证明 reliability 是否“有信息”。下一步应研究如何把已有 preference ranking 信号转化为分类效用，例如增加一个仅在 validation 上选择、以最终节点分类准确率为目标的 utility threshold，并与当前 balanced threshold 同时报告。

在论文完整性方面，还需要补跑 Cora、Citeseer、Pubmed，作为同配图负面对照与 fallback 安全性检验。
