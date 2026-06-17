# Server Environment Setup for RTX A6000 / CUDA 12.2 Driver

This setup targets the server shown by `nvidia-smi`:

- Driver: `535.183.01`
- Reported CUDA capability: `12.2`
- GPU: NVIDIA RTX A6000

Use a PyTorch `cu121` build for this server. It is safer than `cu124/cu126` under the current 535 driver and is sufficient for the current synthetic experiment plus later PyG/OGB benchmark experiments.

## 1. Create Conda Environment

```bash
cd /path/to/reliability_routing
conda env create -f environment-server-cu121.yml
conda activate rel-gt-cu121
```

If the environment already exists:

```bash
conda activate rel-gt-cu121
conda env update -f environment-server-cu121.yml --prune
```

## 2. Install PyTorch CUDA 12.1 Build

Recommended stable baseline:

```bash
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
```

This version is a good target for graph-learning packages because PyG provides matching wheels for `torch-2.4.1+cu121`.

## 3. Install Current Minimal Experiment Dependencies

The current synthetic experiment only needs these packages:

```bash
pip install -r requirements.txt
```

If PyTorch is already installed from step 2, this command should keep it unless pip resolves a newer version. To avoid accidental torch replacement, use:

```bash
pip install numpy scikit-learn tqdm
```

## 4. Install PyTorch Geometric for Later Real-Graph Benchmarks

Install PyG and accelerated sparse operators matching PyTorch 2.4.1 + CUDA 12.1:

```bash
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv \
  -f https://data.pyg.org/whl/torch-2.4.1+cu121.html

pip install torch_geometric
```

For newer PyG versions, `torch_cluster` and `torch_spline_conv` may not be needed for most node-classification experiments, but installing the full set keeps older baselines easier to reproduce.

## 5. Optional Benchmark Packages

For OGB and common graph baselines:

```bash
pip install ogb networkx pandas matplotlib seaborn
```

If you later reproduce DGL baselines, create a separate environment. Mixing PyG and DGL is possible, but separate envs make CUDA dependency debugging easier.

## 6. Verify Installation

```bash
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
print("torch cuda:", torch.version.cuda)
print("device count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("gpu 0:", torch.cuda.get_device_name(0))
PY
```

PyG check:

```bash
python - <<'PY'
import torch
import torch_geometric
import torch_scatter
import torch_sparse
print("torch:", torch.__version__)
print("pyg:", torch_geometric.__version__)
print("scatter ok:", torch_scatter.__version__)
print("sparse ok:", torch_sparse.__version__)
PY
```

## 7. Run Current Smoke Test

The server is currently heavily occupied, so start with a small CPU or selected-GPU test.

Use CPU:

```bash
python run_synthetic.py --graph-type heterophily --model reliability_gt \
  --num-nodes 180 --epochs 3 --patience 3 --seeds 0 \
  --hidden-dim 32 --num-heads 4 --device cpu
```

Use one visible GPU:

```bash
CUDA_VISIBLE_DEVICES=0 python run_synthetic.py --graph-type heterophily --model reliability_gt \
  --num-nodes 900 --epochs 300 --seeds 0 1 2 \
  --hidden-dim 64 --num-heads 4 --device cuda
```

Because `CUDA_VISIBLE_DEVICES=0` remaps that GPU to `cuda:0` inside the process, keep `--device cuda`.

## 8. GPU Selection Notes

Your `nvidia-smi` snapshot shows all GPUs are already using about 29-31 GB memory, and GPU 2/3 have non-trivial utilization. For this small experiment, CPU is fine. For later real datasets, choose the GPU with:

- lowest memory usage,
- lowest utilization,
- acceptable temperature.

Example:

```bash
watch -n 2 nvidia-smi
CUDA_VISIBLE_DEVICES=0 python run_synthetic.py --graph-type heterophily --model reliability_gt --device cuda
```

## 9. Recommended Version Matrix

| Stage | Python | PyTorch | CUDA wheel | PyG | Use case |
|---|---:|---:|---:|---:|---|
| Current synthetic validation | 3.10 | 2.4.1 | cu121 | optional | safest first run |
| Real PyG datasets | 3.10 | 2.4.1 | cu121 | 2.6.x or compatible | Cora, Pubmed, heterophily datasets |
| Baseline reproduction from older repos | 3.9/3.10 | match repo | cu121/cu118 | match repo | separate env |

Avoid using `cu124`, `cu126`, or newer CUDA wheels unless the server driver is upgraded beyond the current 535 series.
