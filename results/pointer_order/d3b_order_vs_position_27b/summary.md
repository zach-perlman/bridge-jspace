# pointer_order

Verdict: **ORDER: the pointer direction encodes the Nth statement**

Primary (memory → prompt, asked statement before the filler, targets after it, layer 48, 2x): order 31% [24, 40] (n=125), token 9% [5, 15] (n=125); order - token +22 [+14, +31] points (scene bootstrap)

Positive control (targets before the filler): 51% [46, 56] (n=392)
Random push: {"order": [0.0, 0.0, 0.0298, 125], "token": [0.0, 0.0, 0.0298, 125]}
Shuffled labels: {"order": [0.0, 0.0, 0.0298, 125], "token": [0.0, 0.0, 0.0298, 125]}
memory → memory, answer changed: 2% [1, 3] (n=1148)
Filler-cell targets: order 25% [17, 36] (n=83), answer org 40% [30, 51] (n=83)
Neutral push (target minus the mean): order 18% [13, 26] (n=125), token 2% [1, 7] (n=125)
Asked statement after the filler: order 16% [11, 21] (n=231), token 16% [12, 21] (n=231)

Read test (asked statement after the filler; nearest fitted mean): {"40": {"post_order": [0.322, 0.2169, 0.449, 59], "post_token": [0.2034, 0.1204, 0.3227, 59], "pre_correct": [0.3733, 0.3, 0.453, 150]}, "42": {"post_order": [0.339, 0.2314, 0.4663, 59], "post_token": [0.2034, 0.1204, 0.3227, 59], "pre_correct": [0.4267, 0.3503, 0.5067, 150]}, "44": {"post_order": [0.4068, 0.2909, 0.5341, 59], "post_token": [0.1695, 0.0948, 0.2846, 59], "pre_correct": [0.48, 0.4015, 0.5594, 150]}, "46": {"post_order": [0.4746, 0.3527, 0.5996, 59], "post_token": [0.1017, 0.0474, 0.2046, 59], "pre_correct": [0.52, 0.4406, 0.5985, 150]}, "48": {"post_order": [0.5085, 0.3843, 0.6316, 59], "post_token": [0.1186, 0.0587, 0.2252, 59], "pre_correct": [0.56, 0.48, 0.637, 150]}, "50": {"post_order": [0.5424, 0.4166, 0.663, 59], "post_token": [0.1186, 0.0587, 0.2252, 59], "pre_correct": [0.6067, 0.5268, 0.6812, 150]}, "52": {"post_order": [0.4237, 0.3061, 0.5507, 59], "post_token": [0.1186, 0.0587, 0.2252, 59], "pre_correct": [0.54, 0.4602, 0.6178, 150]}}
