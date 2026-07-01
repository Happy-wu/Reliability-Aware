# Expert Fusion Validation Matrix

- Profile: sanity
- Runs per model: 3
- Datasets: Cora, Chameleon, Actor
- Suites: core_undirected, directed_source_to_target, directed_target_to_source, component_degree, component_local_similarity, component_neighbor_variance, component_rwse

## Claim Summary

| Dataset | Claim | Status | Estimate | Detail |
|---|---|---|---:|---|
| Cora | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Cora | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Cora | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.2330 | delta=-0.2330, CI=[-0.2717, -0.1943] |
| Cora | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0013 | delta=+0.0013, CI=[-0.0015, +0.0042] |
| Cora | H4 global expert provides complementary predictions | SUPPORTED | +0.0550 | global-only correct fraction=+0.0550, P(global correct | local wrong)=+0.2763 |
| Chameleon | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Chameleon | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Chameleon | H2 ordinary gate beats validation-selected fixed alpha | INCONCLUSIVE | -0.0548 | delta=-0.0548, CI=[-0.1815, +0.0719] |
| Chameleon | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | -0.0000 | delta=-0.0000, CI=[-0.0163, +0.0163] |
| Chameleon | H4 global expert provides complementary predictions | SUPPORTED | +0.1477 | global-only correct fraction=+0.1477, P(global correct | local wrong)=+0.3165 |
| Actor | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Actor | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Actor | H2 ordinary gate beats validation-selected fixed alpha | INCONCLUSIVE | -0.0011 | delta=-0.0011, CI=[-0.0086, +0.0065] |
| Actor | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | -0.0004 | delta=-0.0004, CI=[-0.0014, +0.0005] |
| Actor | H4 global expert provides complementary predictions | SUPPORTED | +0.1816 | global-only correct fraction=+0.1816, P(global correct | local wrong)=+0.2549 |
| Chameleon | H5 GCN is sensitive to directed edge protocol | SUPPORTED | +0.1301 | undirected=+0.5329, source_to_target=+0.4306, target_to_source=+0.5607 |
| Actor | H5 GCN is sensitive to directed edge protocol | NOT_SUPPORTED | +0.0138 | undirected=+0.2879, source_to_target=+0.2888, target_to_source=+0.2750 |
| Cora | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0003 | delta=+0.0003, CI=[-0.0011, +0.0018] |
| Cora | H6 degree reliability vs full reliability | INCONCLUSIVE | -0.0010 | delta=-0.0010, CI=[-0.0035, +0.0015] |
| Chameleon | H6 degree reliability vs ordinary gate | INCONCLUSIVE | -0.0015 | delta=-0.0015, CI=[-0.0128, +0.0099] |
| Chameleon | H6 degree reliability vs full reliability | INCONCLUSIVE | -0.0015 | delta=-0.0015, CI=[-0.0289, +0.0260] |
| Actor | H6 degree reliability vs ordinary gate | INCONCLUSIVE | -0.0002 | delta=-0.0002, CI=[-0.0027, +0.0023] |
| Actor | H6 degree reliability vs full reliability | INCONCLUSIVE | +0.0002 | delta=+0.0002, CI=[-0.0023, +0.0027] |
| Cora | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0007 | delta=+0.0007, CI=[-0.0008, +0.0021] |
| Cora | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | -0.0007 | delta=-0.0007, CI=[-0.0021, +0.0008] |
| Chameleon | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | -0.0022 | delta=-0.0022, CI=[-0.0116, +0.0072] |
| Chameleon | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | -0.0022 | delta=-0.0022, CI=[-0.0116, +0.0072] |
| Actor | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | -0.0000 | delta=-0.0000, CI=[-0.0016, +0.0016] |
| Actor | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | +0.0004 | delta=+0.0004, CI=[-0.0014, +0.0023] |
| Cora | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0010 | delta=+0.0010, CI=[-0.0015, +0.0035] |
| Cora | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | -0.0003 | delta=-0.0003, CI=[-0.0018, +0.0011] |
| Chameleon | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0044 | delta=+0.0044, CI=[-0.0065, +0.0153] |
| Chameleon | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | +0.0044 | delta=+0.0044, CI=[-0.0100, +0.0188] |
| Actor | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0002 | delta=+0.0002, CI=[-0.0007, +0.0012] |
| Actor | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | +0.0007 | delta=+0.0007, CI=[-0.0010, +0.0023] |
| Cora | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0003 | delta=+0.0003, CI=[-0.0011, +0.0018] |
| Cora | H6 rwse reliability vs full reliability | INCONCLUSIVE | -0.0010 | delta=-0.0010, CI=[-0.0035, +0.0015] |
| Chameleon | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | -0.0022 | delta=-0.0022, CI=[-0.0076, +0.0033] |
| Chameleon | H6 rwse reliability vs full reliability | INCONCLUSIVE | -0.0022 | delta=-0.0022, CI=[-0.0218, +0.0174] |
| Actor | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[-0.0016, +0.0016] |
| Actor | H6 rwse reliability vs full reliability | INCONCLUSIVE | +0.0004 | delta=+0.0004, CI=[-0.0021, +0.0029] |

## Interpretation Rules

- `PASS`: deterministic fallback difference is numerically zero.
- `SUPPORTED`: paired 95% CI is entirely above zero.
- `NOT_SUPPORTED`: paired 95% CI is entirely below zero.
- `INCONCLUSIVE`: CI crosses zero or required output is missing.
- Complementarity is marked supported when the global-only correct fraction is at least 1 percentage point or conditional correction is at least 10%.
