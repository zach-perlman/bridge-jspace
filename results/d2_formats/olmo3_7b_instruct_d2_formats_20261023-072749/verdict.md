# d2_formats / olmo3_7b_instruct_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 6% [1, 28] (n 16) / 100% [81, 100] (n 16) / - | False | 0% [0, 22] (n 14) | True, True, False (testable: False) |
| prose | 0% [0, 18] (n 18) / 89% [67, 97] (n 18) / - | False | 15% [5, 36] (n 20) | False, True, False (testable: False) |
| table | 0% [-0, 14] (n 23) / 100% [86, 100] (n 23) / - | True | 20% [4, 62] (n 5) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 94% [72, 99]; lookup_nodigit|question 88% [64, 97]; lookup_noname|question 100% [81, 100]; lookup_noname|final 0% [0, 19]; lookup_nodigit|final 100% [81, 100]
- prose: lookup|question 83% [61, 94]; lookup_nodigit|question 83% [61, 94]; lookup_noname|question 100% [82, 100]; lookup_noname|final 0% [0, 18]; lookup_nodigit|final 89% [67, 97]
- table: lookup|question 87% [68, 95]; lookup_nodigit|question 87% [68, 95]; lookup_noname|question 91% [73, 98]; lookup_noname|final 0% [-0, 14]; lookup_nodigit|final 100% [86, 100]
