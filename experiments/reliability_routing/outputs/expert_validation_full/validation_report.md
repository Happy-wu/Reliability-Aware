# Expert Fusion Validation Matrix

- Profile: full
- Runs per model: 10
- Datasets: Cora, Citeseer, Pubmed, Chameleon, Squirrel, Actor
- Suites: core_undirected, directed_source_to_target, directed_target_to_source, component_degree, component_local_similarity, component_neighbor_variance, component_rwse

## Claim Summary

| Dataset | Claim | Status | Estimate | Detail |
|---|---|---|---:|---|
| Cora | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Cora | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Cora | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.1732 | delta=-0.1732, CI=[-0.2205, -0.1259] |
| Cora | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Cora | H4 global expert provides complementary predictions | SUPPORTED | +0.0502 | global-only correct fraction=+0.0502, P(global correct | local wrong)=+0.2671 |
| Citeseer | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Citeseer | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Citeseer | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.1354 | delta=-0.1354, CI=[-0.1756, -0.0952] |
| Citeseer | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | -0.0011 | delta=-0.0011, CI=[-0.0036, +0.0014] |
| Citeseer | H4 global expert provides complementary predictions | SUPPORTED | +0.0765 | global-only correct fraction=+0.0765, P(global correct | local wrong)=+0.2492 |
| Pubmed | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Pubmed | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Pubmed | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.0363 | delta=-0.0363, CI=[-0.0460, -0.0266] |
| Pubmed | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0027 | delta=+0.0027, CI=[-0.0034, +0.0088] |
| Pubmed | H4 global expert provides complementary predictions | SUPPORTED | +0.0734 | global-only correct fraction=+0.0734, P(global correct | local wrong)=+0.3172 |
| Chameleon | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Chameleon | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Chameleon | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.0719 | delta=-0.0719, CI=[-0.0953, -0.0486] |
| Chameleon | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0026 | delta=+0.0026, CI=[-0.0033, +0.0086] |
| Chameleon | H4 global expert provides complementary predictions | SUPPORTED | +0.1002 | global-only correct fraction=+0.1002, P(global correct | local wrong)=+0.2808 |
| Squirrel | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Squirrel | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Squirrel | H2 ordinary gate beats validation-selected fixed alpha | NOT_SUPPORTED | -0.1186 | delta=-0.1186, CI=[-0.1333, -0.1039] |
| Squirrel | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0005 | delta=+0.0005, CI=[-0.0006, +0.0016] |
| Squirrel | H4 global expert provides complementary predictions | SUPPORTED | +0.1222 | global-only correct fraction=+0.1222, P(global correct | local wrong)=+0.2322 |
| Actor | H1 alpha=1 recovers GCN | PASS | +0.0000 | paired delta=+0.0000 |
| Actor | H1 alpha=0 recovers global expert | PASS | +0.0000 | paired delta=+0.0000 |
| Actor | H2 ordinary gate beats validation-selected fixed alpha | INCONCLUSIVE | -0.0007 | delta=-0.0007, CI=[-0.0027, +0.0013] |
| Actor | H3 reliability adds value beyond ordinary gating | INCONCLUSIVE | +0.0014 | delta=+0.0014, CI=[-0.0003, +0.0030] |
| Actor | H4 global expert provides complementary predictions | SUPPORTED | +0.1695 | global-only correct fraction=+0.1695, P(global correct | local wrong)=+0.2435 |
| Chameleon | H5 GCN is sensitive to directed edge protocol | SUPPORTED | +0.2375 | undirected=+0.6436, source_to_target=+0.4268, target_to_source=+0.6643 |
| Squirrel | H5 GCN is sensitive to directed edge protocol | SUPPORTED | +0.2302 | undirected=+0.4736, source_to_target=+0.2891, target_to_source=+0.5193 |
| Actor | H5 GCN is sensitive to directed edge protocol | SUPPORTED | +0.0288 | undirected=+0.3036, source_to_target=+0.2844, target_to_source=+0.2748 |
| Cora | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Cora | H6 degree reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Citeseer | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Citeseer | H6 degree reliability vs full reliability | INCONCLUSIVE | +0.0011 | delta=+0.0011, CI=[-0.0014, +0.0036] |
| Pubmed | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0007 | delta=+0.0007, CI=[-0.0009, +0.0023] |
| Pubmed | H6 degree reliability vs full reliability | INCONCLUSIVE | -0.0020 | delta=-0.0020, CI=[-0.0065, +0.0025] |
| Chameleon | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0022 | delta=+0.0022, CI=[-0.0028, +0.0072] |
| Chameleon | H6 degree reliability vs full reliability | INCONCLUSIVE | -0.0004 | delta=-0.0004, CI=[-0.0014, +0.0006] |
| Squirrel | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0016 | delta=+0.0016, CI=[-0.0011, +0.0043] |
| Squirrel | H6 degree reliability vs full reliability | INCONCLUSIVE | +0.0012 | delta=+0.0012, CI=[-0.0015, +0.0038] |
| Actor | H6 degree reliability vs ordinary gate | INCONCLUSIVE | +0.0013 | delta=+0.0013, CI=[-0.0011, +0.0038] |
| Actor | H6 degree reliability vs full reliability | INCONCLUSIVE | -0.0001 | delta=-0.0001, CI=[-0.0020, +0.0019] |
| Cora | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Cora | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Citeseer | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | -0.0005 | delta=-0.0005, CI=[-0.0016, +0.0006] |
| Citeseer | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | +0.0006 | delta=+0.0006, CI=[-0.0008, +0.0020] |
| Pubmed | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0009 | delta=+0.0009, CI=[-0.0011, +0.0029] |
| Pubmed | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | -0.0018 | delta=-0.0018, CI=[-0.0059, +0.0023] |
| Chameleon | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0026 | delta=+0.0026, CI=[-0.0016, +0.0069] |
| Chameleon | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[-0.0030, +0.0030] |
| Squirrel | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0005 | delta=+0.0005, CI=[-0.0006, +0.0016] |
| Squirrel | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Actor | H6 local_similarity reliability vs ordinary gate | INCONCLUSIVE | +0.0011 | delta=+0.0011, CI=[-0.0010, +0.0031] |
| Actor | H6 local_similarity reliability vs full reliability | INCONCLUSIVE | -0.0003 | delta=-0.0003, CI=[-0.0021, +0.0014] |
| Cora | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Cora | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Citeseer | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0002 | delta=+0.0002, CI=[-0.0003, +0.0007] |
| Citeseer | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | +0.0013 | delta=+0.0013, CI=[-0.0016, +0.0042] |
| Pubmed | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Pubmed | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | -0.0027 | delta=-0.0027, CI=[-0.0088, +0.0034] |
| Chameleon | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | -0.0007 | delta=-0.0007, CI=[-0.0084, +0.0071] |
| Chameleon | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | -0.0033 | delta=-0.0033, CI=[-0.0115, +0.0049] |
| Squirrel | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0005 | delta=+0.0005, CI=[-0.0006, +0.0016] |
| Squirrel | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Actor | H6 neighbor_variance reliability vs ordinary gate | INCONCLUSIVE | +0.0011 | delta=+0.0011, CI=[-0.0007, +0.0029] |
| Actor | H6 neighbor_variance reliability vs full reliability | INCONCLUSIVE | -0.0003 | delta=-0.0003, CI=[-0.0019, +0.0013] |
| Cora | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Cora | H6 rwse reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Citeseer | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | -0.0011 | delta=-0.0011, CI=[-0.0036, +0.0014] |
| Citeseer | H6 rwse reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Pubmed | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0027 | delta=+0.0027, CI=[-0.0034, +0.0088] |
| Pubmed | H6 rwse reliability vs full reliability | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Chameleon | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0004 | delta=+0.0004, CI=[-0.0006, +0.0014] |
| Chameleon | H6 rwse reliability vs full reliability | INCONCLUSIVE | -0.0022 | delta=-0.0022, CI=[-0.0072, +0.0028] |
| Squirrel | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | +0.0000 | delta=+0.0000, CI=[+0.0000, +0.0000] |
| Squirrel | H6 rwse reliability vs full reliability | INCONCLUSIVE | -0.0005 | delta=-0.0005, CI=[-0.0016, +0.0006] |
| Actor | H6 rwse reliability vs ordinary gate | INCONCLUSIVE | -0.0007 | delta=-0.0007, CI=[-0.0026, +0.0011] |
| Actor | H6 rwse reliability vs full reliability | NOT_SUPPORTED | -0.0021 | delta=-0.0021, CI=[-0.0038, -0.0004] |

## Interpretation Rules

- `PASS`: deterministic fallback difference is numerically zero.
- `SUPPORTED`: paired 95% CI is entirely above zero.
- `NOT_SUPPORTED`: paired 95% CI is entirely below zero.
- `INCONCLUSIVE`: CI crosses zero or required output is missing.
- Complementarity is marked supported when the global-only correct fraction is at least 1 percentage point or conditional correction is at least 10%.
