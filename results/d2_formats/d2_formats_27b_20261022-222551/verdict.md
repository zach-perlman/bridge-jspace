# d2_formats / d2_formats_27b

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | 2% [0, 10] (n 54) / 100% [93, 100] (n 54) / 100% [93, 100] (n 54) | True | 3% [1, 11] (n 60) | True, True, False (testable: False) |
| prose | 9% [4, 20] (n 53) / 98% [90, 100] (n 53) / 98% [90, 100] (n 53) | True | 18% [10, 30] (n 55) | True, True, False (testable: False) |
| table | 4% [1, 13] (n 52) / 100% [93, 100] (n 52) / 100% [93, 100] (n 52) | True | 15% [7, 29] (n 40) | True, True, False (testable: False) |

Name vs digit cells (MP, right [95%]):

- json: lookup|question 91% [80, 96]; lookup_nodigit|question 94% [85, 98]; lookup_noname|question 98% [90, 100]; lookup_noname|final 4% [1, 13]; lookup_nodigit|final 94% [85, 98]
- prose: lookup|question 91% [80, 96]; lookup_nodigit|question 92% [82, 97]; lookup_noname|question 100% [93, 100]; lookup_noname|final 9% [4, 20]; lookup_nodigit|final 87% [75, 93]
- table: lookup|question 98% [90, 100]; lookup_nodigit|question 98% [90, 100]; lookup_noname|question 100% [93, 100]; lookup_noname|final 4% [1, 13]; lookup_nodigit|final 96% [87, 99]
