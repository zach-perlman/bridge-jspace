# attn_knockout / qwen35_122b_d2_late_read_seed2_after

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.06,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.063,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.997,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.6,
    "verdict": "needed"
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
   "question": "needed"
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
   "kind_needed": [
    "attn"
   ],
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
  },
  "RL/lookup/after": {
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
| RL | lookup | after | all | value | 300 | 9% [7,13] | 57% | -3.53 [-3.76,-3.32] | 0.96 | +91 [+87,+94] | needed |
| RL | lookup | after | attn | value | 300 | 8% [5,11] | 72% | -3.86 [-4.09,-3.65] | - | +92 [+89,+95] | needed |
| RL | lookup | after | gdn | value | 300 | 94% [90,96] | 1% | -0.19 [-0.26,-0.14] | 0.96 | - | not_needed |
| RL | lookup | both | attn | value | 300 | 8% [6,12] | 71% | -3.74 [-3.97,-3.53] | - | +92 [+89,+95] | needed |
| RL | lookup | both | gdn | value | 300 | 99% [98,100] | 0% | -0.04 [-0.06,-0.03] | 0.98 | - | not_needed |
| RL | lookup | final | all | value | 300 | 6% [4,9] | 90% | -4.76 [-5.00,-4.54] | 0.99 | +94 [+91,+97] | needed |
| RL | lookup | final | attn | value | 300 | 6% [4,10] | 91% | -4.54 [-4.77,-4.32] | - | +94 [+91,+96] | needed |
| RL | lookup | final | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 60% [54,65] | 13% | -1.29 [-1.45,-1.14] | 0.97 | +40 [+34,+46] | needed |
| RL | lookup | question | attn | value | 300 | 76% [71,81] | 12% | -0.69 [-0.82,-0.58] | - | +24 [+19,+29] | needed |
| RL | lookup | question | gdn | value | 300 | 99% [98,100] | 0% | -0.04 [-0.07,-0.03] | 0.97 | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | after | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | gdn | value | 300 | 99% [97,100] | 1% | -0.02 [-0.04,-0.01] | 0.96 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
