# d2_formats / muse30b_d2_formats

| format | late read MP: hidden / off-path / DeltaNet only | holds | PP hidden | name vs digit (MP): valid-split, digit-final-split, name-q-split |
|---|---|---|---|---|
| json | nan% [nan, nan] (n 0) / nan% [nan, nan] (n 0) / - | False | 0% [-0, 43] (n 5) | None, None, None (testable: None) |
| prose | 40% [12, 77] (n 5) / 100% [57, 100] (n 5) / - | False | 0% [0, 39] (n 6) | True, False, False (testable: False) |
| table | nan% [nan, nan] (n 0) / nan% [nan, nan] (n 0) / - | False | 0% [0, 79] (n 1) | None, None, None (testable: None) |

Name vs digit cells (MP, right [95%]):

- json: 
- prose: lookup|question 80% [38, 96]; lookup_nodigit|question 80% [38, 96]; lookup_noname|question 100% [57, 100]; lookup_noname|final 40% [12, 77]; lookup_nodigit|final 100% [57, 100]
- table: 
