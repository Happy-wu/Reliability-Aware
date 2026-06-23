# Mechanism Diagnosis

This report aligns four evidence layers:

1. expert complementarity and fixed-alpha fallback,
2. preference routing signal,
3. utility routing conversion,
4. representation-control conversion.


## Scorecard

| Dataset | Expert H4 | Pref rel-feat AUC | Pref comb-feat AUC | Utility headroom | Iter K1 ft rel-fixed | Iter K1 ft true-shuffled | Iter K1 ft true-constant | Iter K1 ft rel/base | Iter K1 ft alpha std | Legacy repr ft true-shuffled | Diagnosis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Actor | SUPPORTED | +0.0003 | +0.0116 | +0.1196 | n/a | n/a | n/a | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Amazon-ratings | n/a | +0.0234 | +0.0274 | +0.0105 | -0.0019 | -0.0054 | -0.0089 | +0.3133 | +0.0405 | n/a | preference-signal-not-converted |
| Chameleon | SUPPORTED | +0.0816 | +0.0600 | +0.1064 | n/a | n/a | n/a | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Citeseer | SUPPORTED | n/a | n/a | +0.0766 | n/a | n/a | n/a | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |
| Cora | SUPPORTED | n/a | n/a | +0.0512 | -0.0253 | -0.0073 | -0.0060 | +0.0770 | +0.0166 | n/a | expert-complementarity-with-unrealized-headroom |
| Minesweeper | n/a | +0.0623 | -0.0218 | +0.0000 | n/a | n/a | n/a | n/a | n/a | n/a | mixed-or-negative |
| Pubmed | SUPPORTED | n/a | n/a | +0.0722 | -0.0007 | +0.0000 | -0.0003 | +0.0284 | +0.0032 | n/a | expert-complementarity-with-unrealized-headroom |
| Roman-empire | n/a | -0.0677 | +0.0705 | +0.0522 | +0.0212 | +0.0229 | +0.0225 | +0.5839 | +0.0484 | n/a | iterative-relation-frozen-positive |
| Squirrel | SUPPORTED | +0.0856 | +0.0643 | +0.1331 | n/a | n/a | n/a | n/a | n/a | n/a | expert-complementarity-with-unrealized-headroom |

## Dataset Notes

### Actor

- Expert complementarity: SUPPORTED (+0.1695).
- Preference routing: reliability-feature AUC delta +0.0003, combined-feature AUC delta +0.0116.
- Utility routing headroom: oracle-fixed delta +0.1196; reliability router-fixed delta -0.0018; combined router-fixed delta -0.0009.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; frozen true-constant n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Iterative mechanism stats: finetune alpha std n/a; finetune adjustment mean n/a; finetune relation/base n/a; finetune update gate n/a; finetune alpha corr degree n/a; finetune alpha corr neighbor variance n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Amazon-ratings

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0234, combined-feature AUC delta +0.0274.
- Utility routing headroom: oracle-fixed delta +0.0105; reliability router-fixed delta +0.0003; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed +0.0016; frozen true-shuffled -0.0005; frozen true-constant -0.0013; finetune reliability-fixed -0.0019; finetune true-shuffled -0.0054; finetune true-constant -0.0089.
- Iterative mechanism stats: finetune alpha std +0.0405; finetune adjustment mean +0.0438; finetune relation/base +0.3133; finetune update gate +0.5297; finetune alpha corr degree -0.0604; finetune alpha corr neighbor variance +0.2096.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `preference-signal-not-converted`.

### Chameleon

- Expert complementarity: SUPPORTED (+0.1002).
- Preference routing: reliability-feature AUC delta +0.0816, combined-feature AUC delta +0.0600.
- Utility routing headroom: oracle-fixed delta +0.1064; reliability router-fixed delta -0.0053; combined router-fixed delta -0.0055.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; frozen true-constant n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Iterative mechanism stats: finetune alpha std n/a; finetune adjustment mean n/a; finetune relation/base n/a; finetune update gate n/a; finetune alpha corr degree n/a; finetune alpha corr neighbor variance n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Citeseer

- Expert complementarity: SUPPORTED (+0.0765).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0766; reliability router-fixed delta -0.0014; combined router-fixed delta -0.0014.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; frozen true-constant n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Iterative mechanism stats: finetune alpha std n/a; finetune adjustment mean n/a; finetune relation/base n/a; finetune update gate n/a; finetune alpha corr degree n/a; finetune alpha corr neighbor variance n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Cora

- Expert complementarity: SUPPORTED (+0.0502).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0512; reliability router-fixed delta -0.0014; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed +0.0000; frozen true-shuffled +0.0000; frozen true-constant +0.0007; finetune reliability-fixed -0.0253; finetune true-shuffled -0.0073; finetune true-constant -0.0060.
- Iterative mechanism stats: finetune alpha std +0.0166; finetune adjustment mean +0.0116; finetune relation/base +0.0770; finetune update gate +0.5070; finetune alpha corr degree -0.5267; finetune alpha corr neighbor variance -0.3530.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Minesweeper

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta +0.0623, combined-feature AUC delta -0.0218.
- Utility routing headroom: oracle-fixed delta +0.0000; reliability router-fixed delta +0.0000; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; frozen true-constant n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Iterative mechanism stats: finetune alpha std n/a; finetune adjustment mean n/a; finetune relation/base n/a; finetune update gate n/a; finetune alpha corr degree n/a; finetune alpha corr neighbor variance n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `mixed-or-negative`.

### Pubmed

- Expert complementarity: SUPPORTED (+0.0734).
- Preference routing: reliability-feature AUC delta n/a, combined-feature AUC delta n/a.
- Utility routing headroom: oracle-fixed delta +0.0722; reliability router-fixed delta -0.0012; combined router-fixed delta -0.0009.
- Iterative relation K=1: frozen reliability-fixed +0.0003; frozen true-shuffled +0.0000; frozen true-constant +0.0000; finetune reliability-fixed -0.0007; finetune true-shuffled +0.0000; finetune true-constant -0.0003.
- Iterative mechanism stats: finetune alpha std +0.0032; finetune adjustment mean +0.0017; finetune relation/base +0.0284; finetune update gate +0.4910; finetune alpha corr degree -0.5253; finetune alpha corr neighbor variance -0.3606.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

### Roman-empire

- Expert complementarity: n/a (n/a).
- Preference routing: reliability-feature AUC delta -0.0677, combined-feature AUC delta +0.0705.
- Utility routing headroom: oracle-fixed delta +0.0522; reliability router-fixed delta -0.0140; combined router-fixed delta -0.0081.
- Iterative relation K=1: frozen reliability-fixed +0.0197; frozen true-shuffled +0.0153; frozen true-constant +0.0114; finetune reliability-fixed +0.0212; finetune true-shuffled +0.0229; finetune true-constant +0.0225.
- Iterative mechanism stats: finetune alpha std +0.0484; finetune adjustment mean +0.0497; finetune relation/base +0.5839; finetune update gate +0.5190; finetune alpha corr degree -0.0337; finetune alpha corr neighbor variance -0.1658.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `iterative-relation-frozen-positive`.

### Squirrel

- Expert complementarity: SUPPORTED (+0.1222).
- Preference routing: reliability-feature AUC delta +0.0856, combined-feature AUC delta +0.0643.
- Utility routing headroom: oracle-fixed delta +0.1331; reliability router-fixed delta +0.0002; combined router-fixed delta +0.0000.
- Iterative relation K=1: frozen reliability-fixed n/a; frozen true-shuffled n/a; frozen true-constant n/a; finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Iterative mechanism stats: finetune alpha std n/a; finetune adjustment mean n/a; finetune relation/base n/a; finetune update gate n/a; finetune alpha corr degree n/a; finetune alpha corr neighbor variance n/a.
- Representation control: finetune reliability-fixed n/a; finetune true-shuffled n/a; finetune true-constant n/a.
- Diagnosis: `expert-complementarity-with-unrealized-headroom`.

