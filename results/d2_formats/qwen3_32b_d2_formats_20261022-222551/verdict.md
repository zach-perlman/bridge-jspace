# d2_formats / qwen3_32b_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 0% [0, 9] (n 41) / 100% [91, 100] (n 41) / - | True | 0% [-0, 8] (n 46) | True, True, False (testable: False) |
| prose | 6% [2, 20] (n 32) / 100% [89, 100] (n 32) / - | True | 5% [1, 17] (n 40) | True, True, False (testable: False) |
| table | 0% [0, 9] (n 38) / 100% [91, 100] (n 38) / - | True | 6% [2, 21] (n 31) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 76% [61, 86]; lookup_nodigit|question 73% [58, 84]; lookup_noname|question 100% [91, 100]; lookup_noname|final 0% [0, 9]; lookup_nodigit|final 98% [87, 100]
- prose: lookup|question 88% [72, 95]; lookup_nodigit|question 84% [68, 93]; lookup_noname|question 100% [89, 100]; lookup_noname|final 6% [2, 20]; lookup_nodigit|final 91% [76, 97]
- table: lookup|question 79% [64, 89]; lookup_nodigit|question 79% [64, 89]; lookup_noname|question 97% [87, 100]; lookup_noname|final 0% [0, 9]; lookup_nodigit|final 82% [67, 91]
