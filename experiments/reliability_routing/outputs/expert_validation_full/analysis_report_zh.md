# Expert Fusion 正式实验分析

## 1. 实验完整性

- 共检查 7 个实验套件、120 个结果 CSV、1200 条运行记录。
- 每个核心配置包含 6 个数据集、10 次运行。
- `alpha=1` 与 PyG-GCN 的输出/准确率完全一致。
- `alpha=0` 与 GlobalExpert 的输出/准确率完全一致。

因此，本轮结果不是由融合公式、fallback 实现或结果文件缺失造成的。

## 2. 核心结论

### 2.1 学习型 gate 没有超过固定权重

| 数据集 | Ordinary gate | 验证集选择的固定 alpha | 差值及 95% CI |
|---|---:|---:|---:|
| Cora | 0.6389 | 0.8121 | -0.1732 [-0.2205, -0.1259] |
| Citeseer | 0.5575 | 0.6929 | -0.1354 [-0.1756, -0.0952] |
| Pubmed | 0.7324 | 0.7687 | -0.0363 [-0.0460, -0.0266] |
| Chameleon | 0.5737 | 0.6456 | -0.0719 [-0.0953, -0.0486] |
| Squirrel | 0.3549 | 0.4736 | -0.1186 [-0.1333, -0.1039] |
| Actor | 0.3528 | 0.3535 | -0.0007 [-0.0027, 0.0013] |

前五个数据集上的负差距稳定且幅度较大。Actor 上两者基本相当。

验证集选择的固定权重也具有明确规律：

- Cora、Pubmed、Squirrel：10/10 选择 `alpha=1.0`。
- Citeseer、Chameleon：9/10 选择 `alpha=1.0`，1/10 选择 `alpha=0.75`。
- Actor：6/10 选择 `alpha=0.0`，4/10 选择 `alpha=0.25`。

这说明前五个数据集总体应强烈依赖局部 GCN，而 Actor 更应依赖全局专家。

### 2.2 gate 训练大多没有改善初始化

`best_epoch=-1` 表示初始化的常数 `alpha=0.5` 优于所有训练 epoch。

| 数据集 | Ordinary gate 未改善次数 | Reliability gate 未改善次数 |
|---|---:|---:|
| Cora | 9/10 | 9/10 |
| Citeseer | 9/10 | 10/10 |
| Pubmed | 8/10 | 9/10 |
| Chameleon | 9/10 | 8/10 |
| Squirrel | 8/10 | 9/10 |
| Actor | 0/10 | 0/10 |

所以当前问题不是简单的训练轮数不足，而是 gate 的监督目标、输入表达或优化方式没有学到正确的专家选择规律。

### 2.3 reliability 没有提供稳定增益

Reliability gate 相对 Ordinary gate 的差值：

- Cora：0.0000
- Citeseer：-0.0011
- Pubmed：+0.0027
- Chameleon：+0.0026
- Squirrel：+0.0005
- Actor：+0.0014

六个数据集的 95% CI 均未完全高于 0。四个单独 component 也没有稳定超过普通 gate 或完整 reliability；Actor 上 RWSE 相对完整 reliability 反而略差。

因此，本轮实验不支持“degree、local similarity、neighbor variance、RWSE 能稳定改善节点级路由”的当前实现。

### 2.4 专家仍然具有明显互补性

如果诊断性地使用标签构造 oracle，选择两个专家中预测正确的一个，其理论上界为：

| 数据集 | 最强单专家 | Oracle union | 潜在提升 |
|---|---:|---:|---:|
| Cora | 0.8121 | 0.8623 | +0.0502 |
| Citeseer | 0.6931 | 0.7696 | +0.0765 |
| Pubmed | 0.7687 | 0.8421 | +0.0734 |
| Chameleon | 0.6436 | 0.7439 | +0.1002 |
| Squirrel | 0.4736 | 0.5958 | +0.1222 |
| Actor | 0.3526 | 0.4731 | +0.1205 |

这说明失败点不是“两个专家完全重复”，而是当前 gate 无法识别应该信任哪个专家的节点。

### 2.5 边方向协议影响很大

| 数据集 | Undirected | Source-to-target | Target-to-source |
|---|---:|---:|---:|
| Chameleon | 0.6436 | 0.4268 | 0.6643 |
| Squirrel | 0.4736 | 0.2891 | 0.5193 |
| Actor | 0.3036 | 0.2844 | 0.2748 |

Chameleon 和 Squirrel 对方向协议极其敏感。主结果应固定并明确报告 undirected/symmetrized 协议，同时把 directed 结果作为敏感性分析，不能混用。

## 3. 对论文假设的判断

本轮结果否定的是较具体的操作性假设：

> 当前四类静态 reliability 特征，通过现有 logits-level gate 和端到端分类损失，可以稳定改善普通 gate。

它尚未否定更宽泛的研究出发点：

> 节点状态可能帮助判断局部与全局信息源的可靠性。

原因是专家之间存在 5 到 12 个百分点以上的可利用互补空间，但当前训练方法没有把这个空间转化为收益。

## 4. 建议的下一步

1. 暂停 Q/K modulation、hidden fusion 和更多同类 seed；当前瓶颈已经不是统计功效。
2. 增加 oracle routing 报告，确认每个数据集的可实现上界。
3. 构造“专家偏好”标签：仅在训练节点上标记 local-only-correct 与 global-only-correct，忽略两者同对或同错。
4. 分别训练 reliability-only、ordinary-feature、两者组合的二分类路由器，并报告 preference AUC、balanced accuracy 和 test routing accuracy。
5. 检查两个专家的 logit 范数与温度校准；未经校准的 logits 线性混合会把尺度差异误当成专家置信度。
6. 只有当 reliability-only 路由器显著优于随机且优于 ordinary-feature 路由器时，再重做融合 gate。

建议设定停止标准：如果 reliability-only 在至少两个异配数据集上的 preference AUC 仍接近 0.5，且相对普通路由特征没有稳定增益，就应收缩或转向课题，而不是继续堆叠编码器。

## 5. 统计解释注意事项

- 组件实验包含较多同时比较，单个边缘显著结果不应在未经多重比较校正时单独强调。
- Planetoid 数据集主要体现同一公开划分下的随机种子变化；异配数据集体现不同官方 split，二者方差来源不同。
- Oracle 只用于诊断可利用空间，不能作为可部署模型结果。

