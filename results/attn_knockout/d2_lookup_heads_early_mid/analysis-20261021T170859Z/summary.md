# attn_knockout / d2_lookup_heads_early_mid

Measure: correct (items: {"RL": {"items": 200, "unedited_right": 200}, "DL": {"items": 200, "unedited_right": 200}, "RR": {"items": 200, "unedited_right": 200}})

Claims: {
 "positive_control": {},
 "late_attention_read": {},
 "C1a_RL_breaks_RR_survives": {
  "RL": null,
  "RR": null,
  "holds": false
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": null,
   "question": null
  },
  "RL": {
   "final": null,
   "question": null
  },
  "BLR": {
   "final": null,
   "question": null
  },
  "BRL": {
   "final": null,
   "question": null
  }
 },
 "C1b_holds": false,
 "relay_holds": false,
 "recall_needs_no_locker": {
  "BR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "RR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  }
 },
 "binding_BL_vs_BR": {
  "BL": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BLR": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  },
  "BRL": {
   "question": null,
   "final": null,
   "both": null,
   "after": null
  }
 },
 "bands": {
  "RL/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "mid"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "early"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/cue": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "early"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | both | L35 | value | 200 | 99% [96,100] | 1% | -0.03 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | both | L35:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h12 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L35:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h17 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h18 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | both | L35:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L35:h20 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | both | L35:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L35:h23 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L35:kv0 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L35:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L35:kv2 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L35:kv3 | value | 200 | 99% [96,100] | 1% | -0.02 [-0.04,-0.01] | - | - | not_needed |
| RL | lookup | both | L39 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L39:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L39:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h12 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L39:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h15 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L39:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h19 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | both | L39:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:h22 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L39:h23 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L39:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L39:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L43 | value | 200 | 96% [92,98] | 4% | -0.17 [-0.21,-0.14] | - | - | not_needed |
| RL | lookup | both | L43:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h06 | value | 200 | 100% [98,100] | 0% | +0.02 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup | both | L43:h07 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:h08 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L43:h09 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L43:h10 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L43:h11 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L43:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:h13 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L43:h14 | value | 200 | 100% [97,100] | 0% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RL | lookup | both | L43:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L43:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h17 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:h18 | value | 200 | 100% [98,100] | 0% | -0.02 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L43:h19 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L43:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:h22 | value | 200 | 97% [94,99] | 3% | -0.11 [-0.14,-0.08] | - | - | not_needed |
| RL | lookup | both | L43:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L43:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L43:kv2 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | both | L43:kv3 | value | 200 | 98% [94,99] | 2% | -0.12 [-0.15,-0.09] | - | - | not_needed |
| RL | lookup | both | L47 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup | both | L47:h00 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L47:h01 | value | 200 | 99% [96,100] | 1% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | both | L47:h02 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | both | L47:h03 | value | 200 | 98% [96,99] | 2% | -0.06 [-0.08,-0.04] | - | - | not_needed |
| RL | lookup | both | L47:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L47:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L47:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L47:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | L47:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L47:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | both | L47:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | L47:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:kv0 | value | 200 | 99% [96,100] | 1% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | both | L47:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | L47:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | both | mid | value | 200 | 43% [36,50] | 57% | -1.17 [-1.29,-1.06] | - | +57 [+50,+64] | needed |
| RL | lookup_off | both | L35 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L35:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h22 | value | 200 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L39:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h06 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.02,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h08 | value | 200 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h13 | value | 200 | 100% [97,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | L43:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L43:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | L47 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h00 | value | 200 | 100% [97,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | L47:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | both | L47:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | mid | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| DL | lookup | cue | L03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | cue | L07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | cue | L11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | cue | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | cue | L19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | cue | L23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | cue | L27 | value | 200 | 95% [91,97] | 0% | -0.19 [-0.30,-0.10] | - | - | not_needed |
| DL | lookup | cue | L31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | cue | early | value | 200 | 3% [1,6] | 4% | -4.49 [-4.71,-4.29] | - | +97 [+94,+99] | needed |
| DL | lookup | question | L03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L03:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L03:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L07:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L07:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L07:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L11:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L11:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L15:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L15:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L19:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L19:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L19:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L23:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27 | value | 200 | 95% [91,97] | 0% | -0.20 [-0.31,-0.11] | - | - | not_needed |
| DL | lookup | question | L27:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L27:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L27:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L27:kv2 | value | 200 | 100% [97,100] | 0% | -0.05 [-0.09,-0.02] | - | - | not_needed |
| DL | lookup | question | L27:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L31:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | question | L31:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | L31:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | question | early | value | 200 | 3% [1,6] | 4% | -4.47 [-4.69,-4.26] | - | +97 [+94,+99] | needed |
| DL | lookup_off | cue | L03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | cue | L19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L27 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | L31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | cue | early | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L03:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L07:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L11:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | question | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L15:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L19:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L23:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L27:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | L31:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | question | early | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | L35 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | both | L39 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | L43 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | both | L47 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | mid | value | 200 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | - | - | not_needed |
| RR | lookup | question | L03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | L07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | L11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | L19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | L23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | L27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | question | L31 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RR | lookup | question | early | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RR | lookup_off | both | L35 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | L39 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | both | L43 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | L47 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | mid | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L27 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | L31 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | early | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
