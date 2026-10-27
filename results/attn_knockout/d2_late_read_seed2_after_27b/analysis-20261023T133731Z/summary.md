# attn_knockout / d2_late_read_seed2_after_27b

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.073,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.073,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.913,
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
| RL | lookup | after | all | value | 300 | 1% [0,3] | 96% | -5.03 [-5.21,-4.85] | 0.94 | +98 [+96,+99] | needed |
| RL | lookup | after | attn | value | 300 | 2% [1,4] | 92% | -5.35 [-5.56,-5.13] | - | +98 [+96,+99] | needed |
| RL | lookup | after | gdn | value | 300 | 99% [97,99] | 1% | -0.03 [-0.06,-0.02] | 0.94 | - | not_needed |
| RL | lookup | both | attn | value | 300 | 5% [3,8] | 90% | -5.17 [-5.40,-4.95] | - | +95 [+93,+98] | needed |
| RL | lookup | both | gdn | value | 300 | 99% [98,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 300 | 7% [5,11] | 88% | -4.28 [-4.49,-4.07] | 0.98 | +93 [+90,+96] | needed |
| RL | lookup | final | attn | value | 300 | 7% [5,11] | 89% | -4.21 [-4.42,-4.00] | - | +93 [+90,+96] | needed |
| RL | lookup | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 91% [88,94] | 8% | -0.33 [-0.38,-0.27] | 0.97 | +9 [+6,+12] | partial |
| RL | lookup | question | attn | value | 300 | 89% [85,92] | 11% | -0.41 [-0.53,-0.30] | - | +11 [+8,+15] | partial |
| RL | lookup | question | gdn | value | 300 | 99% [98,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 0.94 | - | not_needed |
| RL | lookup_off | after | attn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | after | gdn | value | 300 | 99% [98,100] | 1% | -0.02 [-0.03,-0.01] | 0.94 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
