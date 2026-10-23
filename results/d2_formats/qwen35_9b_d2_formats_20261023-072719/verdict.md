# d2_formats / qwen35_9b_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 0% [0, 12] (n 27) / 100% [88, 100] (n 27) / 100% [88, 100] (n 27) | True | 6% [2, 19] (n 34) | True, True, False (testable: False) |
| prose | 8% [2, 26] (n 24) / 100% [86, 100] (n 24) / 96% [80, 99] (n 24) | True | 10% [4, 23] (n 41) | True, True, False (testable: False) |
| table | 0% [0, 11] (n 32) / 100% [89, 100] (n 32) / 100% [89, 100] (n 32) | True | 9% [4, 22] (n 43) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 85% [68, 94]; lookup_nodigit|question 89% [72, 96]; lookup_noname|question 96% [82, 99]; lookup_noname|final 4% [1, 18]; lookup_nodigit|final 96% [82, 99]
- prose: lookup|question 83% [64, 93]; lookup_nodigit|question 83% [64, 93]; lookup_noname|question 100% [86, 100]; lookup_noname|final 8% [2, 26]; lookup_nodigit|final 96% [80, 99]
- table: lookup|question 84% [68, 93]; lookup_nodigit|question 88% [72, 95]; lookup_noname|question 97% [84, 99]; lookup_noname|final 0% [0, 11]; lookup_nodigit|final 97% [84, 99]
