# d2_formats / olmo_hybrid_7b_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 0% [0, 22] (n 14) / 93% [69, 99] (n 14) / 93% [69, 99] (n 14) | False | 0% [-0, 16] (n 20) | False, True, False (testable: False) |
| prose | 14% [4, 40] (n 14) / 100% [78, 100] (n 14) / 100% [78, 100] (n 14) | False | 10% [3, 30] (n 20) | False, True, False (testable: False) |
| table | 0% [0, 14] (n 24) / 100% [86, 100] (n 24) / 88% [69, 96] (n 24) | False | 5% [1, 24] (n 20) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 71% [45, 88]; lookup_nodigit|question 71% [45, 88]; lookup_noname|question 86% [60, 96]; lookup_noname|final 0% [0, 22]; lookup_nodigit|final 100% [78, 100]
- prose: lookup|question 71% [45, 88]; lookup_nodigit|question 64% [39, 84]; lookup_noname|question 93% [69, 99]; lookup_noname|final 14% [4, 40]; lookup_nodigit|final 93% [69, 99]
- table: lookup|question 75% [55, 88]; lookup_nodigit|question 75% [55, 88]; lookup_noname|question 92% [74, 98]; lookup_noname|final 0% [0, 14]; lookup_nodigit|final 92% [74, 98]
