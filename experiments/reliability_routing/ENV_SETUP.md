# 环境配置流程

下面流程以 Windows + PowerShell 为主，也适用于 Linux/macOS，只需要把虚拟环境激活命令换成对应系统版本。

## 1. 进入实验目录

```powershell
cd D:\Desktop\调研\experiments\reliability_routing
```

## 2. 创建虚拟环境

推荐使用 Python 3.10 到 3.12。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

如果 PowerShell 不允许激活脚本，可以先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. 安装依赖

CPU 版本：

```powershell
pip install -r requirements.txt
```

如果你要使用 CUDA，建议先去 PyTorch 官方安装页选择与你显卡驱动匹配的命令：

https://pytorch.org/get-started/locally/

一般流程是先安装对应 CUDA 版本的 PyTorch，再安装其余依赖：

```powershell
pip install numpy scikit-learn tqdm
```

## 4. Windows OpenMP 冲突处理

如果运行时出现：

```text
OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
```

可以在当前 PowerShell 会话中临时设置：

```powershell
$env:KMP_DUPLICATE_LIB_OK="TRUE"
```

然后重新运行实验。这个设置是 Windows 科学计算环境里常见的兜底做法，适合先跑通原型实验；正式大规模实验时，最好使用干净虚拟环境或 conda 环境，避免多个 OpenMP runtime 混装。

## 5. Smoke Test

先跑一个小图，确认代码能启动：

```powershell
python run_synthetic.py --graph-type heterophily --model reliability_gt --num-nodes 180 --epochs 3 --patience 3 --seeds 0 --hidden-dim 32 --num-heads 4
```

如果输出类似下面这样，就说明环境和代码都能正常工作：

```text
model=reliability_gt graph=heterophily
test_acc mean=...
gate/local-sim corr mean=...
saved: outputs\heterophily_reliability_gt.csv
```

## 6. 第一组正式对比实验

异配图上比较四个模型：

```powershell
python run_synthetic.py --graph-type heterophily --model mlp
python run_synthetic.py --graph-type heterophily --model gcn
python run_synthetic.py --graph-type heterophily --model linear_gt
python run_synthetic.py --graph-type heterophily --model qk_gt
python run_synthetic.py --graph-type heterophily --model gate_gt
python run_synthetic.py --graph-type heterophily --model reliability_gt
```

同配图上比较四个模型：

```powershell
python run_synthetic.py --graph-type homophily --model mlp
python run_synthetic.py --graph-type homophily --model gcn
python run_synthetic.py --graph-type homophily --model linear_gt
python run_synthetic.py --graph-type homophily --model reliability_gt
```

噪声图上比较四个模型：

```powershell
python run_synthetic.py --graph-type noisy --model mlp
python run_synthetic.py --graph-type noisy --model gcn
python run_synthetic.py --graph-type noisy --model linear_gt
python run_synthetic.py --graph-type noisy --model reliability_gt
```

## 7. 使用 GPU

如果 PyTorch 能检测到 CUDA，可以加：

```powershell
python run_synthetic.py --graph-type heterophily --model reliability_gt --device cuda
```

检查 CUDA 是否可用：

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.__version__)"
```

## 8. 输出文件

结果会写入：

```text
outputs\<graph_type>_<model>.csv
```

其中包含：

- `best_val_acc`
- `test_acc_at_best_val`
- `gate_local_similarity_corr`
- `elapsed_sec`

`gate_local_similarity_corr` 是解释性指标。若它在同配图上为正，表示局部越可靠，模型越倾向 local branch；若异配图或噪声图上分布更复杂，则需要结合 gate 分布和准确率一起分析。
