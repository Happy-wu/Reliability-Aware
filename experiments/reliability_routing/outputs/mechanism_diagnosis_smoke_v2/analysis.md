# Mechanism Diagnosis

This report aligns four evidence layers:

1. expert complementarity and fixed-alpha fallback,
2. preference routing signal,
3. utility routing conversion,
4. representation-control conversion.


## Scorecard

| Dataset | Expert H4 | Pref rel-feat AUC | Pref comb-feat AUC | Utility headroom | Iter K1 ft rel-fixed | Iter K1 ft true-shuffled | Legacy repr ft true-shuffled | Diagnosis |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Actor | SUPPORTED | +0.0003 | +0.0116 | +0.1196 | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Amazon-ratings | n/a | +0.0234 | +0.0274 | +0.0105 | -0.0019 | -0.0054 | +0.0012 | preference-signal-not-converted |
| Chameleon | SUPPORTED | +0.0816 | +0.0600 | +0.1064 | n/a | n/a | n/a | preference-signal-not-converted |
| Citeseer | SUPPORTED | n/a | n/a | +0.0766 | n/a | n/a | -0.0007 | expert-complementarity-with-unrealized-headroom |
| Cora | SUPPORTED | n/a | n/a | +0.0512 | -0.0253 | -0.0073 | -0.0006 | expert-complementarity-with-unrealized-headroom |
| Minesweeper | n/a | +0.0623 | -0.0218 | +0.0000 | n/a | n/a | n/a | preference-signal-not-converted |
| Pubmed | SUPPORTED | n/a | n/a | +0.0722 | -0.0007 | +0.0000 | +0.0012 | expert-complementarity-with-unrealized-headroom |
| Roman-empire | n/a | -0.0677 | +0.0705 | +0.0522 | +0.0212 | +0.0229 | +0.0088 | iterative-relation-frozen-positive |
| Squirrel | SUPPORTED | +0.0856 | +0.0643 | +0.1331 | n/a | n/a | n/a | preference-signal-not-converted |

## Dataset Notes

### Actor

- Expert complementarity: SUPPORTED (+0.1695).
- Preference routing: reliability-feature AUC delta +0.0003, combined-feature AUC delta +0.0116.
- Utility routing headroom: oracle-fixed delta +0.1196; reliability router-fixed delta -0.0018; combined router-fixed delta -0.0009.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Amazon-ratings

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0234, combined-feature AUC delta +0.0274.
- Utility routing headroom: oracle-fixed delta +0.0105; reliability router-fixed delta +0.0003; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed +0.0016; frozen true-shuffled -0.0005; finetune reliability-fixed -0.0019; finetune true-shuffled -0.0054.
- Representation control: finetune reliability-fixed +0.0020; finetune true-shuffled +0.0012.
- Diagnosis: `preference-signal-not-converted`.

### Chameleon

- Expert complementarity: SUPPORTED (+0.1002).
- Preference routing: reliability-feature AUC delta +0.0816, combined-feature AUC delta +0.0600.
- Utility routing headroom: oracle-fixed delta +0.1064; reliability router-fixed delta -0.0053; combined router-fixed delta -0.0055.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Diagnosis: `preference-signal-not-converted`.

### Citeseer

- Expert complementarity: SUPPORTED (+0.0765).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0766; reliability router-fixed delta -0.0014; combined router-fixed delta -0.0014.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Representation control: finetune reliability-fixed -0.0009; finetune true-shuffled -0.0007.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Cora

- Expert complementarity: SUPPORTED (+0.0502).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0512; reliability router-fixed delta -0.0014; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed +0.0000; frozen true-shuffled +0.0000; finetune reliability-fixed -0.0253; finetune true-shuffled -0.0073.
- Representation control: finetune reliability-fixed -0.0068; finetune true-shuffled -0.0006.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Minesweeper

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0623, combined-feature AUC delta -0.0218.
- Utility routing headroom: oracle-fixed delta +0.0000; reliability router-fixed delta +0.0000; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Diagnosis: `preference-signal-not-converted`.

### Pubmed

- Expert complementarity: SUPPORTED (+0.0734).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0722; reliability router-fixed delta -0.0012; combined router-fixed delta -0.0009.
- Iterative relation K=1: frozen reliability-fixed +0.0003; frozen true-shuffled +0.0000; finetune reliability-fixed -0.0007; finetune true-shuffled +0.0000.
- Representation control: finetune reliability-fixed -0.0018; finetune true-shuffled +0.0012.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Roman-empire

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta -0.0677, combined-feature AUC delta +0.0705.
- Utility routing headroom: oracle-fixed delta +0.0522; reliability router-fixed delta -0.0140; combined router-fixed delta -0.0081.
- Iterative relation K=1: frozen reliability-fixed +0.0197; frozen true-shuffled +0.0153; finetune reliability-fixed +0.0212; finetune true-shuffled +0.0229.
- Representation control: finetune reliability-fixed +0.0104; finetune true-shuffled +0.0088.
- Diagnosis: `iterative-relation-frozen-positive`.

### Squirrel

- Expert complementarity: SUPPORTED (+0.1222).
- Preference routing: reliability-feature AUC delta +0.0856, combined-feature AUC delta +0.0643.
- Utility routing headroom: oracle-fixed delta +0.1331; reliability router-fixed delta +0.0002; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Diagnosis: `preference-signal-not-converted`.

