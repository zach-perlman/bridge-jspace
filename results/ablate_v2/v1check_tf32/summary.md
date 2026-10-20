# ablate_v2 / v1check_tf32: 1400 prompts, 216s

Unedited accuracy: BL/clean 100%, BL/hop 100%, BR/hop 100%, RL/hop 100%, RR/hop 100%, BR/clean 100%, RL/clean 100%, RR/clean 100%, TYPO/clean 100%, TYPO/hop 100%, TRANS/clean 100%, TRANS/hop 100%, country-R/clean 100%, country-B/clean 100%

## omp25: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 99 | 99 | 14 | 99 | 13 | 17 | 98 | 24 | 10 | 48 | 10 | 58 | 38 | 36 |

## gauss: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 100 | 100 | 100 | 100 | 100 | 99 | 100 | 100 | 98 | 100 | 100 | 100 | 100 | 100 |

## agreement with ablate_pilot v1 (same items)

{
 "none": {
  "n": 1400,
  "same_correct": 1,
  "median_abs_dlogp": 0.0,
  "accuracy_ours": 1,
  "accuracy_v1": 1
 },
 "omp25": {
  "n": 1400,
  "same_correct": 0.8978571428571429,
  "median_abs_dlogp": 0.27324193716049194,
  "accuracy_ours": 0.4735714285714286,
  "accuracy_v1": 0.47
 },
 "gauss": {
  "n": 1400,
  "same_correct": 0.9971428571428571,
  "median_abs_dlogp": 0.007535961223766208,
  "accuracy_ours": 0.9978571428571429,
  "accuracy_v1": 0.9992857142857143
 }
}
