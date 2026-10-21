# ablate_v2 / pad_check_exact_1021: 288 prompts, 1648s

Unedited accuracy: PP/clean 100%, PM/clean 100%, MP/step1 83%, MM/step1 83%, PP/step1 100%, PM/step1 100%, MP/clean 100%, PPP/clean 100%, CP/clean 100%, MPP/step1 92%, MPM/step1 92%, MM/clean 100%, CP/step1 100%, CM/step1 100%, CM/clean 100%, PPM/clean 100%, MPP/clean 100%, PPP/step1 100%, PPM/step1 100%, MMP/step1 83%, MMP/clean 100%, MPM/clean 100%, PMP/clean 100%, PMP/step1 100%

## paper10: accuracy (%) by band

| band | PP/clean | PM/clean | MP/step1 | MM/step1 | PP/step1 | PM/step1 | MP/clean | PPP/clean | CP/clean | MPP/step1 | MPM/step1 | MM/clean | CP/step1 | CM/step1 | CM/clean | PPM/clean | MPP/clean | PPP/step1 | PPM/step1 | MMP/step1 | MMP/clean | MPM/clean | PMP/clean | PMP/step1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32-40 | 100 | 42 | 83 | 83 | 100 | 100 | 100 | 92 | 92 | 92 | 92 | 42 | 92 | 92 | 58 | 67 | 92 | 100 | 100 | 75 | 75 | 83 | 83 | 92 |
| L0-62 | 33 | 17 | 0 | 0 | 0 | 0 | 58 | 17 | 0 | 0 | 0 | 8 | 0 | 0 | 8 | 25 | 0 | 0 | 0 | 0 | 8 | 8 | 33 | 0 |

## paper10_rot: accuracy (%) by band

| band | PP/clean | PM/clean | MP/step1 | MM/step1 | PP/step1 | PM/step1 | MP/clean | PPP/clean | CP/clean | MPP/step1 | MPM/step1 | MM/clean | CP/step1 | CM/step1 | CM/clean | PPM/clean | MPP/clean | PPP/step1 | PPM/step1 | MMP/step1 | MMP/clean | MPM/clean | PMP/clean | PMP/step1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32-40 | 100 | 92 | 92 | 92 | 100 | 100 | 100 | 92 | 100 | 92 | 92 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 83 | 92 | 100 |
| L0-62 | 100 | 75 | 67 | 67 | 100 | 100 | 92 | 67 | 92 | 92 | 92 | 75 | 83 | 83 | 58 | 33 | 67 | 100 | 100 | 92 | 75 | 58 | 75 | 100 |

## top5: accuracy (%) by band

| band | PP/clean | PM/clean | MP/step1 | MM/step1 | PP/step1 | PM/step1 | MP/clean | PPP/clean | CP/clean | MPP/step1 | MPM/step1 | MM/clean | CP/step1 | CM/step1 | CM/clean | PPM/clean | MPP/clean | PPP/step1 | PPM/step1 | MMP/step1 | MMP/clean | MPM/clean | PMP/clean | PMP/step1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L32-40 | 100 | 42 | 92 | 92 | 100 | 100 | 100 | 92 | 100 | 83 | 83 | 42 | 100 | 100 | 58 | 83 | 92 | 100 | 100 | 75 | 75 | 83 | 83 | 92 |
| L0-62 | 33 | 0 | 0 | 0 | 0 | 0 | 67 | 8 | 25 | 0 | 0 | 33 | 0 | 0 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 33 | 50 | 0 |

