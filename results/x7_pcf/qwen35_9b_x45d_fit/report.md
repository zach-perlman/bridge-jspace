# 45d's fit: a label-free basis per format in the varied scenes (qwen35_9b_x45d_fit)

Model qwen3.5-9b, layer 12; set x0b_v2, half 1 of the bridge items (seed 0); pairs: the bridge's locker statement trades places with another item's, both before the asked pick, numbers kept; PCA centered, rank 4. Descriptive; the test is x0b_generalize --pcf-from. UNVERIFIED.

| format | pairs | scenes | bridge items | variance explained 1-4 (cum.) | split-half mean cos² | mean cos² with U (random 0.0010) |
|---|---|---|---|---|---|---|
| prose | 878 | 367 | 29 | 0.532 | 0.908 | 0.524 |
| json | 326 | 121 | 14 | 0.521 | 0.661 | 0.226 |
| table | 1227 | 455 | 30 | 0.553 | 0.968 | 0.241 |

Mean cos² between the formats' bases: prose/json 0.279, prose/table 0.294, json/table 0.553.
