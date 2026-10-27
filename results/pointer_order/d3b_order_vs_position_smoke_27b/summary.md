# pointer_order

Verdict: **inconclusive (controls failed or n too small: not interpretable)**

Primary (memory → prompt, asked statement before the filler, targets after it, layer 48, 2x): order 10% [2, 40] (n=10), token 10% [2, 40] (n=10); order - token +0 [-27, +27] points (scene bootstrap)

Positive control (targets before the filler): 56% [34, 75] (n=18)
Random push: {"order": [0.0, -0.0, 0.2775, 10], "token": [0.0, -0.0, 0.2775, 10]}
Shuffled labels: {"order": [0.0, -0.0, 0.2775, 10], "token": [0.0, -0.0, 0.2775, 10]}
memory → memory, answer changed: 0% [0, 6] (n=64)
Filler-cell targets: order 50% [15, 85] (n=4), answer org 25% [5, 70] (n=4)
Neutral push (target minus the mean): order 0% [-0, 28] (n=10), token 0% [-0, 28] (n=10)
Asked statement after the filler: order 7% [1, 31] (n=14), token 7% [1, 31] (n=14)

Read test (asked statement after the filler; nearest fitted mean): {"40": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "42": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "44": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "46": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "48": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "50": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.5, 0.2152, 0.7848, 8]}, "52": {"post_order": [0.0, 0.0, 0.6576, 2], "post_token": [0.5, 0.0945, 0.9055, 2], "pre_correct": [0.375, 0.1368, 0.6943, 8]}}
