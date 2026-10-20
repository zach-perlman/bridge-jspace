# ablate_v2 / smoke_v1check_1020: 28 prompts, 16s

Unedited accuracy: BL/clean 100%, BL/hop 100%, BR/hop 100%, RL/hop 100%, RR/hop 100%, BR/clean 100%, RL/clean 100%, RR/clean 100%, TYPO/clean 100%, TYPO/hop 100%, TRANS/clean 100%, TRANS/hop 100%, country-R/clean 100%, country-B/clean 100%

## omp25: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 100 | 100 | 50 | 100 | 50 | 50 | 100 | 50 | 0 | 50 | 0 | 50 | 50 | 50 |

## gauss: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |

## agreement with ablate_pilot v1 (same items)

{
 "none": {
  "n": 28,
  "same_correct": 1,
  "median_abs_dlogp": 0.00011546886526048183,
  "accuracy_ours": 1,
  "accuracy_v1": 1
 },
 "omp25": {
  "n": 28,
  "same_correct": 0.8214285714285714,
  "median_abs_dlogp": 0.3025650978088379,
  "accuracy_ours": 0.5714285714285714,
  "accuracy_v1": 0.6071428571428571
 },
 "gauss": {
  "n": 28,
  "same_correct": 1,
  "median_abs_dlogp": 0.013172977603971958,
  "accuracy_ours": 1,
  "accuracy_v1": 1
 }
}
