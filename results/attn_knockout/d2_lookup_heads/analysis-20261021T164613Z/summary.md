# attn_knockout / d2_lookup_heads

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
  "RL/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "late"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "DL/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "late"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/final": {
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
| RL | lookup | final | L51 | value | 200 | 96% [92,98] | 4% | -0.08 [-0.11,-0.06] | - | - | not_needed |
| RL | lookup | final | L51:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h04 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h12 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | final | L51:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h16 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | final | L51:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h20 | value | 200 | 100% [97,100] | 0% | -0.03 [-0.04,-0.02] | - | - | not_needed |
| RL | lookup | final | L51:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:h22 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup | final | L51:h23 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | final | L51:kv0 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L51:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L51:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | final | L51:kv3 | value | 200 | 96% [92,98] | 4% | -0.09 [-0.11,-0.06] | - | - | not_needed |
| RL | lookup | final | L55 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | final | L55:h00 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L55:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h02 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L55:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L55:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h05 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup | final | L55:h06 | value | 200 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | - | - | not_needed |
| RL | lookup | final | L55:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L55:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:h22 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | final | L55:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L55:kv0 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | final | L55:kv1 | value | 200 | 100% [98,100] | 0% | -0.02 [-0.03,-0.02] | - | - | not_needed |
| RL | lookup | final | L55:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L55:kv3 | value | 200 | 100% [98,100] | 0% | +0.01 [+0.01,+0.01] | - | - | not_needed |
| RL | lookup | final | L59 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.02] | - | - | not_needed |
| RL | lookup | final | L59:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h03 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.03,-0.01] | - | - | not_needed |
| RL | lookup | final | L59:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L59:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L59:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:kv0 | value | 200 | 100% [97,100] | 0% | -0.02 [-0.02,-0.01] | - | - | not_needed |
| RL | lookup | final | L59:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L59:kv3 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L63 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L63:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | L63:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L63:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | L63:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | L63:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | late | value | 200 | 18% [13,23] | 80% | -3.93 [-4.23,-3.62] | - | +82 [+77,+88] | needed |
| RL | lookup_off | final | L51 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L51:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | L55:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | L55:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L55:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L59 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L59:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | L63:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | late | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| DL | lookup | final | L51 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L51:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L51:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h02 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h17 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L55:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L55:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L59:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L59:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L63 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L63:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup | final | L63:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | L63:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup | final | late | value | 200 | 10% [7,15] | 90% | -6.17 [-6.50,-5.80] | - | +90 [+86,+94] | needed |
| DL | lookup_off | final | L51 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h00 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h01 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h09 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h13 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L51:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h04 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h05 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h07 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h11 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h12 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h15 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h19 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h20 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:h23 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:kv0 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L55:kv3 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | L59 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h03 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h06 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h08 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h10 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h14 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h16 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h18 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h21 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h22 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:kv1 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:kv2 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | L59:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h00 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h01 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h02 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h03 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h04 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h05 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h06 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h07 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h08 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h09 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h10 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h11 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h12 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h13 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h14 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h15 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h16 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h17 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h18 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h19 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h20 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h21 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h22 | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:h23 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:kv0 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:kv1 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:kv2 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | L63:kv3 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| DL | lookup_off | final | late | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | L51 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | L55 | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| RR | lookup | final | L59 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | L63 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | late | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RR | lookup_off | final | L51 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | L55 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | L59 | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | L63 | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | late | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
