# Mechanism Diagnosis

This report aligns four evidence layers:

1. expert complementarity and fixed-alpha fallback,
2. preference routing signal,
3. utility routing conversion,
4. representation-control conversion.

## Scorecard

| Dataset | Expert H4 | Pref rel-feat AUC | Pref comb-feat AUC | Utility headroom | Repr finetune rel-fixed | Repr finetune true-shuffled | Binary true-shuffled | Diagnosis |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Actor | SUPPORTED | +0.0003 | +0.0116 | +0.1196 | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Amazon-ratings | n/a | +0.0234 | +0.0274 | +0.0105 | +0.0020 | +0.0012 | n/a | mixed-or-negative |
| Chameleon | SUPPORTED | +0.0816 | +0.0600 | +0.1064 | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Citeseer | SUPPORTED | n/a | n/a | +0.0766 | -0.0009 | -0.0007 | n/a | expert-complementarity-with-unrealized-headroom |
| Cora | SUPPORTED | n/a | n/a | +0.0512 | -0.0068 | -0.0006 | n/a | expert-complementarity-with-unrealized-headroom |
| Minesweeper | n/a | +0.0623 | -0.0218 | +0.0000 | n/a | n/a | +0.0000 | mixed-or-negative |
| Pubmed | SUPPORTED | n/a | n/a | +0.0722 | -0.0018 | +0.0012 | n/a | expert-complementarity-with-unrealized-headroom |
| Questions | n/a | n/a | n/a | n/a | n/a | n/a | +0.0015 | mixed-or-negative |
| Roman-empire | n/a | -0.0677 | +0.0705 | +0.0522 | +0.0104 | +0.0088 | n/a | representation-positive |
| Squirrel | SUPPORTED | +0.0856 | +0.0643 | +0.1331 | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Tolokers | n/a | n/a | n/a | n/a | n/a | n/a | +0.0041 | mixed-or-negative |

## Dataset Notes

### Actor

- Expert complementarity: SUPPORTED (+0.1695).
- Preference routing: reliability-feature AUC delta +0.0003, combined-feature AUC delta +0.0116.
- Utility routing headroom: oracle-fixed delta +0.1196; reliability router-fixed delta -0.0018; combined router-fixed delta -0.0009.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Amazon-ratings

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0234, combined-feature AUC delta +0.0274.
- Utility routing headroom: oracle-fixed delta +0.0105; reliability router-fixed delta +0.0003; combined router-fixed delta +0.0000.
- Representation control: finetune reliability-fixed +0.0020; finetune true-shuffled +0.0012.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `mixed-or-negative`.

### Chameleon

- Expert complementarity: SUPPORTED (+0.1002).
- Preference routing: reliability-feature AUC delta +0.0816, combined-feature AUC delta +0.0600.
- Utility routing headroom: oracle-fixed delta +0.1064; reliability router-fixed delta -0.0053; combined router-fixed delta -0.0055.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Citeseer

- Expert complementarity: SUPPORTED (+0.0765).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0766; reliability router-fixed delta -0.0014; combined router-fixed delta -0.0014.
- Representation control: finetune reliability-fixed -0.0009; finetune true-shuffled -0.0007.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Cora

- Expert complementarity: SUPPORTED (+0.0502).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0512; reliability router-fixed delta -0.0014; combined router-fixed delta +0.0000.
- Representation control: finetune reliability-fixed -0.0068; finetune true-shuffled -0.0006.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Minesweeper

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0623, combined-feature AUC delta -0.0218.
- Utility routing headroom: oracle-fixed delta +0.0000; reliability router-fixed delta +0.0000; combined router-fixed delta +0.0000.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled +0.0000.
- Diagnosis: `mixed-or-negative`.

### Pubmed

- Expert complementarity: SUPPORTED (+0.0734).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0722; reliability router-fixed delta -0.0012; combined router-fixed delta -0.0009.
- Representation control: finetune reliability-fixed -0.0018; finetune true-shuffled +0.0012.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Questions

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta n/a; reliability router-fixed delta n/a; combined router-fixed delta n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled +0.0015.
- Diagnosis: `mixed-or-negative`.

### Roman-empire

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta -0.0677, combined-feature AUC delta +0.0705.
- Utility routing headroom: oracle-fixed delta +0.0522; reliability router-fixed delta -0.0140; combined router-fixed delta -0.0081.
- Representation control: finetune reliability-fixed +0.0104; finetune true-shuffled +0.0088.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `representation-positive`.

### Squirrel

- Expert complementarity: SUPPORTED (+0.1222).
- Preference routing: reliability-feature AUC delta +0.0856, combined-feature AUC delta +0.0643.
- Utility routing headroom: oracle-fixed delta +0.1331; reliability router-fixed delta +0.0002; combined router-fixed delta +0.0000.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Tolokers

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta n/a; reliability router-fixed delta n/a; combined router-fixed delta n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a.
- Binary iterative screen: finetune true-shuffled +0.0041.
- Diagnosis: `mixed-or-negative`.

