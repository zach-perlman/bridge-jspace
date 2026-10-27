# attn_knockout / d2_late_read_long_27b_r3

Measure: correct (items: {"RL": {"items": 178, "unedited_right": 178}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.258,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.258,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.933,
    "verdict": "partial"
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  }
 },
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
   "final": "needed",
   "question": "partial"
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
  "RL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RL/lookup/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | both | attn | value | 178 | 11% [7,17] | 89% | -4.95 [-5.31,-4.60] | - | +89 [+84,+93] | needed |
| RL | lookup | both | gdn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RL | lookup | final | all | value | 178 | 26% [20,33] | 74% | -2.09 [-2.32,-1.86] | 1.00 | +74 [+67,+80] | needed |
| RL | lookup | final | attn | value | 178 | 26% [20,33] | 74% | -2.10 [-2.33,-1.87] | - | +74 [+67,+80] | needed |
| RL | lookup | final | gdn | value | 178 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup | question | all | value | 178 | 93% [89,96] | 7% | -0.32 [-0.43,-0.22] | 1.00 | +7 [+3,+11] | partial |
| RL | lookup | question | attn | value | 178 | 93% [88,96] | 7% | -0.33 [-0.47,-0.22] | - | +7 [+4,+11] | partial |
| RL | lookup | question | gdn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | both | attn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | all | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | attn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 178 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | attn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 178 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
