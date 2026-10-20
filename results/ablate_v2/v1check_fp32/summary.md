# ablate_v2 / v1check_fp32: 1400 prompts, 932s

Unedited accuracy: BL/clean 100%, BL/hop 100%, BR/hop 100%, RL/hop 100%, RR/hop 100%, BR/clean 100%, RL/clean 100%, RR/clean 100%, TYPO/clean 100%, TYPO/hop 100%, TRANS/clean 100%, TRANS/hop 100%, country-R/clean 100%, country-B/clean 100%

## omp25: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 99 | 99 | 12 | 99 | 12 | 17 | 97 | 24 | 12 | 46 | 7 | 59 | 30 | 38 |

## gauss: accuracy (%) by band

| band | BL/clean | BL/hop | BR/hop | RL/hop | RR/hop | BR/clean | RL/clean | RR/clean | TYPO/clean | TYPO/hop | TRANS/clean | TRANS/hop | country-R/clean | country-B/clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32,36,40 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 99 | 100 |

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
  "same_correct": 0.8964285714285715,
  "median_abs_dlogp": 0.2556249164044857,
  "accuracy_ours": 0.465,
  "accuracy_v1": 0.47
 },
 "gauss": {
  "n": 1400,
  "same_correct": 1,
  "median_abs_dlogp": 0.0,
  "accuracy_ours": 0.9992857142857143,
  "accuracy_v1": 0.9992857142857143
 }
}
