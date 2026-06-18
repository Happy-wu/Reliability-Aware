# Real GCN Diagnostic Validation Report

## Material Passport

- Artifact: `outputs/real_gcn_diagnostic`
- Mode: statistical validation and reproducibility diagnosis
- Verification status: ANALYZED
- Configuration: 6 datasets, 5 models, 10 paired runs per dataset/model
- Total training rows: 300
- Missing or malformed result files: 0
- Limitation: `outputs/real_gcn_classic` is not present, so the classic GCN
  training protocol has not yet been validated.

## Main Findings

### 1. Planetoid data and baseline processing are healthy

Under the same standard training profile, custom GCN and PyG-GCN are close:

| Dataset | Custom GCN | PyG-GCN | Paired delta |
|---|---:|---:|---:|
| Cora | 0.8088 | 0.8121 | +0.0033 |
| Citeseer | 0.6842 | 0.6931 | +0.0089 |
| Pubmed | 0.7642 | 0.7687 | +0.0045 |

Cora and Citeseer confidence intervals include zero. Pubmed has a small
uncorrected difference, but it does not survive correction across the 18
reported comparisons. These results do not support a Planetoid data-processing
failure.

### 2. Directed-edge semantics explain the large heterophily discrepancy

| Dataset | Custom GCN | PyG-GCN | PyG minus custom |
|---|---:|---:|---:|
| Chameleon | 0.6474 | 0.4268 | -0.2206 |
| Squirrel | 0.4688 | 0.2891 | -0.1796 |
| Actor | 0.2745 | 0.2841 | +0.0097 |

The custom adjacency stores `edge_index[0]` as sparse-matrix rows and
`edge_index[1]` as columns. Sparse matrix multiplication therefore aggregates
features from the edge target into the edge source. PyG `GCNConv` follows its
source-to-target message-passing convention and aggregates into the target.

These implementations are equivalent on effectively undirected Planetoid
graphs, but not on directed Chameleon, Squirrel, and Actor graphs. Therefore,
the Chameleon and Squirrel gap is an edge-direction protocol mismatch, not a
normal implementation fluctuation. The custom GCN, local GT branch, and
PyG-GCN should not yet be described as the same GCN baseline on these datasets.

### 3. The GT local path does not recover standard GCN

On the three Planetoid datasets, Local-only GT is consistently worse than
PyG-GCN:

| Dataset | Local-only GT | PyG-GCN | Delta | 95% CI |
|---|---:|---:|---:|---:|
| Cora | 0.7398 | 0.8121 | -0.0723 | [-0.0824, -0.0622] |
| Citeseer | 0.6488 | 0.6931 | -0.0443 | [-0.0546, -0.0340] |
| Pubmed | 0.7348 | 0.7687 | -0.0339 | [-0.0469, -0.0209] |

All 10 paired runs lose on every dataset. This confirms that the GT local path,
which remains inside input projection, residual, LayerNorm, and FFN blocks, is
not an exact fallback to a two-layer GCN.

The positive Local-only GT versus PyG-GCN gaps on Chameleon and Squirrel cannot
be interpreted as evidence that this local architecture is better, because the
two models currently use opposite directed-edge aggregation conventions.

### 4. Routing usually hurts relative to Local-only GT

Gate-GT minus Local-only GT:

| Dataset | Delta | 95% CI | Interpretation |
|---|---:|---:|---|
| Cora | -0.0412 | [-0.0550, -0.0274] | clear degradation |
| Citeseer | -0.0216 | [-0.0414, -0.0019] | modest degradation |
| Pubmed | -0.0039 | [-0.0183, +0.0105] | no clear difference |
| Chameleon | -0.0211 | [-0.0354, -0.0067] | degradation |
| Squirrel | -0.0155 | [-0.0244, -0.0065] | degradation |
| Actor | +0.0137 | [+0.0067, +0.0207] | improvement |

Actor is the only dataset where routing clearly improves over the local-only
path. On Cora, Citeseer, Chameleon, and Squirrel, mixing in the global branch
reduces accuracy.

### 5. Gate values alone overstate the effective local contribution

Gate means range from approximately 0.47 to 0.64, but the two branches have
different norms and are often strongly opposed:

- Cora Gate-GT: local/global norm ratio 2.67, cosine -0.484.
- Citeseer Gate-GT: ratio 2.51, cosine -0.487.
- Chameleon Gate-GT: ratio 2.16, cosine -0.480.
- Squirrel Gate-GT: ratio 0.89, cosine -0.661.

Because local and global representations frequently have negative cosine
similarity, the mixture partially cancels information. A gate mean of 0.6 does
not mean that 60% of the effective representation is local. Branch
normalization or scale-aware routing is needed before gate values can be
interpreted directly.

### 6. Q/K modulation still has no stable accuracy contribution

Reliability-GT versus Gate-GT:

- Cora: +0.0016, p=0.8408.
- Citeseer: -0.0061, p=0.4983.
- Pubmed: +0.0031, p=0.5793.
- Chameleon: -0.0013, p=0.8265.
- Squirrel: +0.0082, p=0.2096.
- Actor: -0.0074, p=0.0002.

Five datasets show no reliable difference. Actor shows a consistent
Reliability-GT degradation. Learned Q/K strength remains approximately
0.0066-0.0074, so this experiment provides no evidence that Q/K modulation is a
positive contribution under the current initialization and reliability
representation.

## Statistical Cautions

- The generated report contains 18 paired tests without correction.
- Bonferroni alpha for 18 tests is approximately 0.0028.
- The small Pubmed PyG-GCN advantage (p=0.0322) does not survive correction.
- Large and consistent findings, such as the Planetoid Local-only GT deficits
  and Chameleon/Squirrel direction gaps, remain robust.
- Ten runs are sufficient for strong paired effects but provide limited
  precision for small differences.
- Chameleon, Squirrel, and Actor use different official splits across runs,
  whereas Planetoid repeats one public split with different initialization
  seeds. Their standard deviations measure different sources of variation.

## Fallacy Scan

Coverage: 11/11 checked.

- Simpson's paradox: no reversal detected; dataset-level results are reported
  separately.
- Ecological fallacy: not applicable; no individual-level inference is made.
- Berkson's paradox: not applicable to these benchmark samples.
- Collider bias: no covariate-adjusted statistical model is used.
- Base-rate neglect: accuracy may hide class imbalance, so macro-F1 should be
  added before final evaluation.
- Regression to the mean: not applicable.
- Survivorship bias: no failed runs are missing from the 300 expected rows.
- Look-elsewhere effect: caution; multiple comparisons are uncorrected.
- Garden of forking paths: caution; several architecture and strength sweeps
  have been explored, so final claims need a predefined finalist protocol.
- Correlation versus causation: mechanism statistics are diagnostic
  associations, not causal evidence.
- Reverse causality: not applicable to the benchmark comparison.

## Verdict

1. There is no evidence that Cora, Citeseer, or Pubmed are incorrectly loaded.
2. The large Chameleon/Squirrel GCN discrepancy is caused by incompatible
   directed-edge aggregation semantics.
3. The current GT local branch cannot recover standard PyG-GCN performance on
   homophilic datasets.
4. Routing mostly damages the stronger local path, except on Actor.
5. Q/K modulation does not provide a stable gain and is harmful on Actor.
6. The next required experiment is an edge-direction-controlled comparison
   before further architectural conclusions are drawn.
