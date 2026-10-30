# C2 lookup: route under whole -> route under the arm (n scenes per model; rows whole, columns arm)

## qwen3.5-9b (qwen35_9b_x6_routes), n = 300; whole: identity 144, position 153, value 0, original 3, other 0

**no_alf** (without the pointer directions); identity -> position: 3

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 61 | 3 | 0 | 80 | 0 | 144 |
| position | 48 | 22 | 0 | 83 | 0 | 153 |
| original | 0 | 0 | 0 | 3 | 0 | 3 |

identity -> position scenes: C2-0164, C2-0498, C2-0506

**no_alf_rand** (size-matched random part (control of the pointer arm)); identity -> position: 18

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 119 | 18 | 0 | 7 | 0 | 144 |
| position | 1 | 145 | 0 | 7 | 0 | 153 |
| original | 0 | 0 | 0 | 3 | 0 | 3 |

identity -> position scenes: C2-0003, C2-0017, C2-0036, C2-0079, C2-0082, C2-0132, C2-0170, C2-0172, C2-0236, C2-0284, C2-0295, C2-0304, C2-0311, C2-0337, C2-0364, C2-0481, C2-0498, C2-0539

**no_jpp** (without J++); identity -> position: 35

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 103 | 35 | 0 | 6 | 0 | 144 |
| position | 2 | 147 | 0 | 4 | 0 | 153 |
| original | 0 | 0 | 0 | 3 | 0 | 3 |

identity -> position scenes: C2-0003, C2-0004, C2-0017, C2-0036, C2-0043, C2-0045, C2-0068, C2-0079, C2-0127, C2-0132, C2-0170, C2-0172, C2-0182, C2-0228, C2-0236, C2-0284, C2-0294, C2-0295, C2-0304, C2-0311, C2-0328, C2-0337, C2-0354, C2-0357, C2-0447, C2-0448, C2-0472, C2-0475, C2-0481, C2-0495, C2-0498, C2-0508, C2-0522, C2-0539, C2-0542

**no_jpp_rand** (size-matched random part (control of the J++ arm)); identity -> position: 17

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 121 | 17 | 0 | 6 | 0 | 144 |
| position | 1 | 134 | 0 | 18 | 0 | 153 |
| original | 0 | 0 | 0 | 3 | 0 | 3 |

identity -> position scenes: C2-0003, C2-0017, C2-0036, C2-0079, C2-0082, C2-0132, C2-0170, C2-0172, C2-0182, C2-0236, C2-0284, C2-0295, C2-0311, C2-0337, C2-0481, C2-0495, C2-0539

## qwen3.6-27b (x6_routes_27b), n = 300; whole: identity 197, position 101, value 0, original 1, other 1

**no_alf** (without the pointer directions); identity -> position: 2

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 156 | 2 | 0 | 39 | 0 | 197 |
| position | 60 | 16 | 0 | 24 | 1 | 101 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |
| other | 1 | 0 | 0 | 0 | 0 | 1 |

identity -> position scenes: C2-0128, C2-0200

**no_alf_rand** (size-matched random part (control of the pointer arm)); identity -> position: 1

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 190 | 1 | 0 | 6 | 0 | 197 |
| position | 18 | 75 | 0 | 7 | 1 | 101 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |
| other | 1 | 0 | 0 | 0 | 0 | 1 |

identity -> position scenes: C2-0012

**no_jpp** (without J++); identity -> position: 36

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 135 | 36 | 0 | 26 | 0 | 197 |
| position | 0 | 91 | 0 | 10 | 0 | 101 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |
| other | 0 | 0 | 0 | 0 | 1 | 1 |

identity -> position scenes: C2-0012, C2-0014, C2-0024, C2-0032, C2-0047, C2-0068, C2-0070, C2-0080, C2-0085, C2-0089, C2-0132, C2-0134, C2-0142, C2-0160, C2-0168, C2-0183, C2-0187, C2-0200, C2-0216, C2-0228, C2-0242, C2-0260, C2-0275, C2-0279, C2-0293, C2-0295, C2-0297, C2-0299, C2-0307, C2-0366, C2-0369, C2-0400, C2-0408, C2-0427, C2-0430, C2-0447

**no_jpp_rand** (size-matched random part (control of the J++ arm)); identity -> position: 0

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 194 | 0 | 0 | 3 | 0 | 197 |
| position | 15 | 85 | 0 | 0 | 1 | 101 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |
| other | 1 | 0 | 0 | 0 | 0 | 1 |

## muse-glimmer-30b (muse30b_x6_routes), n = 300; whole: identity 131, position 163, value 0, original 6, other 0

**no_alf** (without the pointer directions); identity -> position: 2

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 100 | 2 | 0 | 29 | 0 | 131 |
| position | 30 | 80 | 0 | 53 | 0 | 163 |
| original | 0 | 0 | 0 | 6 | 0 | 6 |

identity -> position scenes: C2-0363, C2-0634

**no_alf_rand** (size-matched random part (control of the pointer arm)); identity -> position: 6

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 123 | 6 | 0 | 2 | 0 | 131 |
| position | 1 | 158 | 0 | 4 | 0 | 163 |
| original | 0 | 0 | 0 | 6 | 0 | 6 |

identity -> position scenes: C2-0167, C2-0172, C2-0234, C2-0492, C2-0505, C2-0634

**no_jpp** (without J++); identity -> position: 8

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 118 | 8 | 0 | 5 | 0 | 131 |
| position | 1 | 161 | 0 | 1 | 0 | 163 |
| original | 0 | 0 | 0 | 6 | 0 | 6 |

identity -> position scenes: C2-0167, C2-0172, C2-0234, C2-0353, C2-0410, C2-0505, C2-0608, C2-0634

**no_jpp_rand** (size-matched random part (control of the J++ arm)); identity -> position: 4

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 118 | 4 | 0 | 9 | 0 | 131 |
| position | 2 | 156 | 0 | 5 | 0 | 163 |
| original | 0 | 0 | 0 | 6 | 0 | 6 |

identity -> position scenes: C2-0172, C2-0492, C2-0505, C2-0634

## nemotron-3.5-lightning (nem35l_x52_routes), n = 300; whole: identity 133, position 166, value 0, original 1, other 0

**no_alf** (without the pointer directions); identity -> position: 0

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 57 | 0 | 0 | 76 | 0 | 133 |
| position | 37 | 31 | 0 | 98 | 0 | 166 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

**no_alf_rand** (size-matched random part (control of the pointer arm)); identity -> position: 10

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 122 | 10 | 0 | 1 | 0 | 133 |
| position | 4 | 158 | 0 | 4 | 0 | 166 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0028, C2-0031, C2-0075, C2-0093, C2-0171, C2-0284, C2-0418, C2-0479, C2-0516, C2-0545

**no_jpp** (without J++); identity -> position: 22

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 105 | 22 | 0 | 6 | 0 | 133 |
| position | 3 | 152 | 0 | 11 | 0 | 166 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0020, C2-0028, C2-0031, C2-0060, C2-0093, C2-0125, C2-0149, C2-0158, C2-0171, C2-0199, C2-0228, C2-0331, C2-0341, C2-0371, C2-0386, C2-0399, C2-0418, C2-0485, C2-0524, C2-0545, C2-0570, C2-0596

**no_jpp_rand** (size-matched random part (control of the J++ arm)); identity -> position: 11

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 116 | 11 | 0 | 6 | 0 | 133 |
| position | 8 | 130 | 0 | 28 | 0 | 166 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0031, C2-0093, C2-0171, C2-0176, C2-0245, C2-0284, C2-0316, C2-0418, C2-0479, C2-0516, C2-0545

## qwen3.5-122b-a10b (qwen35_122b_x6_routes_g75), n = 300; whole: identity 184, position 115, value 0, original 1, other 0

**no_alf** (without the pointer directions); identity -> position: 0

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 120 | 0 | 0 | 64 | 0 | 184 |
| position | 66 | 14 | 0 | 35 | 0 | 115 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

**no_alf_rand** (size-matched random part (control of the pointer arm)); identity -> position: 7

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 176 | 7 | 0 | 1 | 0 | 184 |
| position | 8 | 101 | 0 | 6 | 0 | 115 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0036, C2-0037, C2-0127, C2-0333, C2-0427, C2-0470, C2-0602

**no_jpp** (without J++); identity -> position: 26

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 156 | 26 | 0 | 2 | 0 | 184 |
| position | 0 | 113 | 0 | 2 | 0 | 115 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0036, C2-0037, C2-0045, C2-0052, C2-0070, C2-0132, C2-0194, C2-0216, C2-0237, C2-0294, C2-0325, C2-0333, C2-0354, C2-0366, C2-0369, C2-0427, C2-0444, C2-0447, C2-0451, C2-0470, C2-0475, C2-0515, C2-0527, C2-0539, C2-0602, C2-0649

**no_jpp_rand** (size-matched random part (control of the J++ arm)); identity -> position: 5

| whole \ arm | identity | position | value | original | other | total |
|---|---|---|---|---|---|---|
| identity | 169 | 5 | 0 | 10 | 0 | 184 |
| position | 9 | 95 | 0 | 11 | 0 | 115 |
| original | 0 | 0 | 0 | 1 | 0 | 1 |

identity -> position scenes: C2-0036, C2-0127, C2-0427, C2-0470, C2-0602

