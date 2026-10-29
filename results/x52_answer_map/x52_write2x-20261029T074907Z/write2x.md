# x52_write2x: what the model outputs under 52 B's write, at 1x and 2x (descriptive; UNVERIFIED)

Dan, 29 Oct morning brief (CPU): the recall's write moves 0.37 / 0.70 / 0.65 to S's answer at gain 1 but 0.03 / 0.09 / 0.01 at gain 2 (9B / Muse / Lightning). Classes of the top token (full vocabulary): target = S's answer token, original = O's, written = one of the written answer word's own tokens, digit = another digit, other = anything else. Main test, write cell per reader as in 52 B. Keep out of the README (Dan).

## qwen3.5-9b (results/x52_answer_map/qwen35_9b_x52_write_main)

| reader | arm | n | target | original | written | digit | other | top written / digit / other tokens |
|---|---|---|---|---|---|---|---|---|
| recall | ans1 | 200 | 0.37 | 0.60 | 0.00 | 0.01 | 0.01 | digit: '3' 1, '4' 1, '9' 1; other: '<|im_end|>' 3 |
| recall | ans2 | 200 | 0.03 | 0.04 | 0.76 | 0.00 | 0.17 | written: 'Four' 35, 'Six' 25, 'Two' 19, 'Eight' 17, 'Three' 13; other: '<|im_end|>' 34 |
| recall | freq1 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| recall | freq2 | 200 | 0.00 | 0.01 | 0.00 | 0.00 | 0.99 | other: ' jLabel' 36, ' Auf' 27, '\tusing' 22, '.Value' 18, 'UpInside' 17 |
| recall | none | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| recall | rand1 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '2' 1, '5' 1 |
| recall | rand2 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '2' 1, '5' 1, '1' 1 |
| recall | whole | 200 | 0.92 | 0.05 | 0.00 | 0.03 | 0.00 | digit: '2' 2, '7' 1, '3' 1, '5' 1, '6' 1 |
| lookup | ans1 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '9' 2 |
| lookup | ans2 | 200 | 0.01 | 0.96 | 0.01 | 0.01 | 0.00 | written: 'Eight' 2, 'Four' 1; digit: '9' 2 |
| lookup | freq1 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '9' 1, '2' 1 |
| lookup | freq2 | 200 | 0.01 | 0.97 | 0.00 | 0.01 | 0.01 | digit: '9' 1, '2' 1; other: ' ValueError' 1, ' me' 1, 'あって' 1 |
| lookup | none | 200 | 0.01 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '9' 1 |
| lookup | rand1 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '2' 2 |
| lookup | rand2 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '2' 2, '9' 1 |
| lookup | whole | 200 | 0.55 | 0.43 | 0.00 | 0.03 | 0.00 | digit: '9' 2, '5' 1, '8' 1, '2' 1 |

## qwen3.6-27b (results/x52_answer_map/x52_write_main_27b)

| reader | arm | n | target | original | written | digit | other | top written / digit / other tokens |
|---|---|---|---|---|---|---|---|---|
| recall | ans1 | 200 | 0.08 | 0.89 | 0.00 | 0.03 | 0.00 | digit: '5' 4, '7' 1, '8' 1 |
| recall | ans2 | 200 | 0.20 | 0.74 | 0.00 | 0.06 | 0.01 | digit: '5' 7, '3' 2, '7' 1, '1' 1; other: ' single' 1 |
| recall | freq1 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '6' 1, '5' 1 |
| recall | freq2 | 200 | 0.01 | 0.94 | 0.00 | 0.04 | 0.00 | digit: '1' 3, '8' 2, '5' 1, '6' 1, '3' 1 |
| recall | none | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| recall | rand1 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '5' 1 |
| recall | rand2 | 200 | 0.00 | 0.98 | 0.00 | 0.02 | 0.00 | digit: '8' 3, '5' 1 |
| recall | whole | 200 | 0.34 | 0.62 | 0.00 | 0.04 | 0.00 | digit: '5' 4, '9' 1, '8' 1, '6' 1 |
| lookup | ans1 | 200 | 0.00 | 0.98 | 0.00 | 0.00 | 0.02 | other: '<|im_end|>' 4 |
| lookup | ans2 | 200 | 0.00 | 0.30 | 0.00 | 0.00 | 0.70 | other: '<|im_end|>' 140 |
| lookup | freq1 | 200 | 0.00 | 0.97 | 0.00 | 0.00 | 0.03 | other: '<|im_end|>' 5 |
| lookup | freq2 | 200 | 0.00 | 0.49 | 0.00 | 0.00 | 0.51 | other: '<|im_end|>' 102 |
| lookup | none | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 200 | 0.00 | 0.92 | 0.00 | 0.00 | 0.08 | other: '<|im_end|>' 16 |
| lookup | whole | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |

## muse-glimmer-30b (results/x52_answer_map/muse30_x52_write_main)

| reader | arm | n | target | original | written | digit | other | top written / digit / other tokens |
|---|---|---|---|---|---|---|---|---|
| recall | ans1 | 200 | 0.70 | 0.23 | 0.00 | 0.07 | 0.00 | digit: '9' 3, '7' 2, '8' 2, '5' 2, '2' 2 |
| recall | ans2 | 200 | 0.09 | 0.03 | 0.84 | 0.04 | 0.00 | written: 'Four' 39, 'Two' 27, 'Six' 27, 'Eight' 21, 'Seven' 17; digit: '3' 4, '4' 2, '5' 1, '2' 1, '1' 1 |
| recall | freq1 | 200 | 0.01 | 0.87 | 0.00 | 0.12 | 0.00 | digit: '5' 7, '2' 4, '4' 4, '6' 3, '3' 2 |
| recall | freq2 | 200 | 0.02 | 0.36 | 0.00 | 0.21 | 0.41 | digit: '5' 8, '6' 6, '9' 6, '1' 6, '2' 4; other: 'apped' 31, 'ぶ' 11, 'ays' 9, 'Beg' 8, 'mates' 6 |
| recall | none | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.01 | digit: '6' 1; other: '19' 1 |
| recall | rand1 | 200 | 0.01 | 0.90 | 0.00 | 0.09 | 0.00 | digit: '5' 4, '3' 4, '6' 3, '2' 2, '9' 2 |
| recall | rand2 | 200 | 0.06 | 0.55 | 0.00 | 0.39 | 0.00 | digit: '3' 24, '2' 17, '8' 9, '5' 9, '6' 7 |
| recall | whole | 200 | 0.98 | 0.01 | 0.00 | 0.01 | 0.00 | digit: '7' 1 |
| lookup | ans1 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | ans2 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | freq1 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | freq2 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | none | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | whole | 200 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |

## nemotron-3.5-lightning (results/x52_answer_map/nem35l_x52_write_main)

| reader | arm | n | target | original | written | digit | other | top written / digit / other tokens |
|---|---|---|---|---|---|---|---|---|
| recall | ans1 | 200 | 0.65 | 0.17 | 0.14 | 0.05 | 0.00 | written: 'Three' 7, 'Four' 4, 'Seven' 4, 'One' 4, 'Five' 3; digit: '1' 4, '7' 3, '3' 1, '5' 1, '9' 1 |
| recall | ans2 | 200 | 0.01 | 0.00 | 0.96 | 0.00 | 0.03 | written: 'Four' 40, 'Two' 27, ' Eight' 26, 'Three' 21, 'Seven' 14; other: ' T' 5 |
| recall | freq1 | 200 | 0.01 | 0.77 | 0.00 | 0.04 | 0.18 | digit: '9' 3, '6' 2, '8' 1, '5' 1; other: 'argin' 8, ' ' 7, 'Carousel' 6, '.io' 4, 'reat' 3 |
| recall | freq2 | 200 | 0.00 | 0.01 | 0.00 | 0.00 | 0.99 | other: ' ' 108, 'Carousel' 26, ' Dich' 19, 'udy' 14, 'argin' 11 |
| recall | none | 200 | 0.01 | 0.99 | 0.00 | 0.00 | 0.00 |  |
| recall | rand1 | 200 | 0.01 | 0.94 | 0.00 | 0.06 | 0.00 | digit: '5' 4, '9' 3, '4' 2, '3' 1, '6' 1 |
| recall | rand2 | 200 | 0.03 | 0.83 | 0.00 | 0.14 | 0.00 | digit: '5' 9, '6' 7, '4' 6, '9' 3, '3' 3 |
| recall | whole | 200 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | ans1 | 200 | 0.01 | 0.98 | 0.00 | 0.01 | 0.00 | digit: '8' 1 |
| lookup | ans2 | 200 | 0.10 | 0.90 | 0.00 | 0.01 | 0.00 | digit: '8' 1 |
| lookup | freq1 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '8' 1, '5' 1 |
| lookup | freq2 | 200 | 0.01 | 0.94 | 0.00 | 0.01 | 0.04 | digit: '8' 1; other: 'ulen' 9 |
| lookup | none | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '5' 1 |
| lookup | rand1 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '8' 1 |
| lookup | rand2 | 200 | 0.00 | 0.99 | 0.00 | 0.01 | 0.00 | digit: '8' 1 |
| lookup | whole | 200 | 0.93 | 0.07 | 0.00 | 0.01 | 0.00 | digit: '5' 1 |

