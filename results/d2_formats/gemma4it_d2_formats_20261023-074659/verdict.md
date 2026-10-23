# d2_formats / gemma4it_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 21% [13, 34] (n 56) / 100% [94, 100] (n 56) / - | False | 22% [14, 33] (n 73) | True, True, False (testable: False) |
| prose | 34% [21, 51] (n 35) / 100% [90, 100] (n 35) / - | False | 49% [36, 62] (n 51) | True, True, False (testable: False) |
| table | 15% [8, 26] (n 55) / 100% [93, 100] (n 55) / - | True | 17% [10, 29] (n 63) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 98% [91, 100]; lookup_nodigit|question 98% [91, 100]; lookup_noname|question 100% [94, 100]; lookup_noname|final 23% [14, 36]; lookup_nodigit|final 96% [88, 99]
- prose: lookup|question 100% [90, 100]; lookup_nodigit|question 97% [85, 99]; lookup_noname|question 100% [90, 100]; lookup_noname|final 34% [21, 51]; lookup_nodigit|final 97% [85, 99]
- table: lookup|question 96% [88, 99]; lookup_nodigit|question 96% [88, 99]; lookup_noname|question 100% [93, 100]; lookup_noname|final 11% [5, 22]; lookup_nodigit|final 89% [78, 95]
