# exp08_brew_read / read_v1

Items: fresh 154, bank 82

## fresh items

| reader | works (A at L62) | I | X | S | A | I - X (pts) | reads I |
|---|---|---|---|---|---|---|---|
| jpp | yes | 15% | 8% | 9% | 8% | +7 [+5, +9] | yes |
| jlens | yes | 12% | 8% | 7% | 11% | +5 [+2, +7] | yes |
| logit | yes | 12% | 7% | 10% | 7% | +5 [+2, +7] | yes |
| code |  | 41% | 4% | 17% | 8% | +36 [+32, +40] | yes |

Window read score: per item, the share of (window layer, position) cells with the colour top-1.

## bank items

| reader | works (A at L62) | I | X | S | A | I - X (pts) | reads I |
|---|---|---|---|---|---|---|---|
| jpp | yes | 13% | 8% | 7% | 9% | +5 [+2, +8] | yes |
| jlens | yes | 13% | 7% | 8% | 10% | +5 [+2, +8] | yes |
| logit | yes | 9% | 10% | 8% | 9% | -1 [-4, +3] | no |
| code |  | 40% | 3% | 21% | 8% | +37 [+32, +42] | yes |

Window read score: per item, the share of (window layer, position) cells with the colour top-1.

