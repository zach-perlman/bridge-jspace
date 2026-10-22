# Attention-sink diagnostic: NOT ARTIFACT (rule fixed in docs/prereg_sink_1021.md)

Gemma 4 31B-it, held-out ctrl_v8, knock-out with sink positions left unedited (accuracy %):

| window | condition | PP | MP | PM | MM |
|---|---|---|---|---|---|
| L30-38 | paper10_nosink | 34 | 27 | 54 | 57 |
| L30-38 | paper10_nosink_rot | 100 | 100 | 100 | 100 |
| L40-48 | paper10_nosink | 47 | 48 | 23 | 24 |
| L40-48 | paper10_nosink_rot | 100 | 100 | 99 | 99 |
| L48-56 | paper10_nosink | 3 | 4 | 13 | 6 |
| L48-56 | paper10_nosink_rot | 100 | 100 | 99 | 100 |

Per window: {"L30-38": {"P->P": 34, "M->P": 27, "gap": -26, "control min": 100, "pass": false}, "L40-48": {"P->P": 47, "M->P": 48, "gap": 23, "control min": 99, "pass": false}, "L48-56": {"P->P": 3, "M->P": 4, "gap": -7, "control min": 99, "pass": false}}

Sink positions left unedited (share of positions): L30-38/paper10_nosink 0.5%, L30-38/paper10_nosink_rot 0.5%, L40-48/paper10_nosink 0.5%, L40-48/paper10_nosink_rot 0.5%, L48-56/paper10_nosink 0.5%, L48-56/paper10_nosink_rot 0.5%

## 27B, ctrl_v8 (descriptive): sink_diag_27b_v1

| band | condition | PP | MP | PM | MM |
|---|---|---|---|---|---|
| L12-20 | paper10_nosink | 66 | 71 | 62 | 82 |
| L12-20 | paper10_nosink_rot | 100 | 99 | 100 | 98 |
| L32-40 | paper10_nosink | 100 | 89 | 48 | 46 |
| L32-40 | paper10_nosink_rot | 100 | 94 | 99 | 100 |

## Gemma dose, layers 30-38 (descriptive): gemma4itf_sink_dose_v1

| band | condition | PP | MP | PM | MM |
|---|---|---|---|---|---|
| L30-38 | top1 | 70 | 66 | 84 | 93 |
| L30-38 | top1_rot | 100 | 100 | 99 | 100 |
| L30-38 | top2 | 59 | 53 | 80 | 91 |
| L30-38 | top2_rot | 100 | 100 | 100 | 100 |
| L30-38 | top5 | 50 | 37 | 64 | 76 |
| L30-38 | top5_rot | 100 | 100 | 100 | 99 |

## Gemma plain-text loss, layers 30-38 (gemma4itf_sink_textloss_v1; nats per token, descriptive)

none 7.66, top1 12.95, top1_rot 7.62, top1_nosink 12.83, top1_nosink_rot 7.65, top10 16.91, top10_rot 7.67, top10_nosink 17.06, top10_nosink_rot 7.67
