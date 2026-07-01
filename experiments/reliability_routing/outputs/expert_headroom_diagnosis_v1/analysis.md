# Expert Headroom Diagnosis

This report checks two preconditions before adding new control modules:

1. whether each dataset has meaningful local/global expert headroom,
2. whether handcrafted reliability separates oracle preference.

## Dataset Summary

| Dataset | Runs | Oracle-best fixed | Oracle-best single | Disagreement | Pref balance | Rel AUC | Feat AUC | Comb AUC | Degree AUC | Local-sim AUC | Var AUC | RWSE AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Roman-empire | 10 | 0.0373 | 0.0692 | 0.4130 | 0.1675 | 0.6997 | 0.7674 | 0.8379 | 0.6333 | 0.5058 | 0.6267 | 0.5704 |
| Amazon-ratings | 10 | 0.1330 | 0.1428 | 0.2995 | 0.4783 | 0.5580 | 0.5346 | 0.5620 | 0.5480 | 0.5005 | 0.5088 | 0.5655 |

## Notes

### Roman-empire

- Oracle headroom over validation-selected fixed alpha: 0.0373.
- Oracle headroom over the best single expert: 0.0692.
- Test disagreement rate: 0.4130.
- Preference balance: 0.1675.
- Preference AUCs: reliability 0.6997, feature 0.7674, combined 0.8379.
- Raw component AUCs: degree 0.6333, local similarity 0.5058, neighbor variance 0.6267, rwse 0.5704.

### Amazon-ratings

- Oracle headroom over validation-selected fixed alpha: 0.1330.
- Oracle headroom over the best single expert: 0.1428.
- Test disagreement rate: 0.2995.
- Preference balance: 0.4783.
- Preference AUCs: reliability 0.5580, feature 0.5346, combined 0.5620.
- Raw component AUCs: degree 0.5480, local similarity 0.5005, neighbor variance 0.5088, rwse 0.5655.

