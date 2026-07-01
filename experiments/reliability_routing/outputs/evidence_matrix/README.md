# Evidence Matrix Record

This directory is the running evidence ledger for the reliability-routing project.
It should be updated whenever a new dataset, control family, GraphGPS reproduction,
or broader benchmark result becomes relevant to the main research claim.

## Files

| File | Purpose |
|---|---|
| `current_evidence_matrix.md` | Human-readable current evidence map for discussion and reporting |
| `current_evidence_matrix.csv` | Machine-readable version of the same evidence map |
| `graphgps_results.csv` | All completed local GraphGPS reproduction rows discovered from `GraphGPS-main` |
| `README.md` | Maintenance policy for this evidence ledger |

## Update Rule

Regenerate the matrix from the project root with:

```bash
python build_current_evidence_matrix.py
```

Then check:

```text
1. Runs
2. Source
3. Config tag
4. Protocol level
5. Reliability-specific?
6. Paper Use
```

Do not mix old-architecture diagnostics, current best representation-control
runs, local GraphGPS reproductions, and broader benchmark adaptations without
explicit protocol labels.

## Current Interpretation

```text
Roman-empire = main positive
Arxiv-year = mechanism-positive dataset under 10-run confirmation
OGBN-Arxiv original = confirmed original-task 10-run mechanism positive under h128-l3 frozen reliability control
Questions = supplemental weak evidence
Amazon-ratings = negative with headroom / signal failure
WebKB = family-level negative boundary
Chameleon / Squirrel = protocol caution only
Cora / Citeseer / Pubmed old runs = historical diagnostic only
PascalVOC-SP = broader benchmark pending
```

## GraphGPS Note

`Local GraphGPS Repro` means locally reproduced GraphGPS results under available
configs in `D:\Desktop\调研\GraphGPS-main`. These are not copied from the original
GraphGPS paper and should not be cited as official paper numbers without a
separate source check.
