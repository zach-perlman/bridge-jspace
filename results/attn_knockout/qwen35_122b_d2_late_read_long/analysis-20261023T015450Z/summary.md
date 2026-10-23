# attn_knockout / qwen35_122b_d2_late_read_long

Measure: correct (items: {"RL": {"items": 172, "unedited_right": 171}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.07,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.07,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.877,
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
| RL | lookup | both | attn | value | 171 | 5% [2,9] | 83% | -3.98 [-4.26,-3.69] | - | +95 [+92,+98] | needed |
| RL | lookup | both | gdn | value | 171 | 99% [97,100] | 1% | -0.01 [-0.03,-0.00] | 1.00 | - | not_needed |
| RL | lookup | final | all | value | 171 | 7% [4,12] | 91% | -4.51 [-4.78,-4.24] | 1.00 | +93 [+89,+96] | needed |
| RL | lookup | final | attn | value | 171 | 7% [4,12] | 91% | -4.44 [-4.71,-4.17] | - | +93 [+89,+96] | needed |
| RL | lookup | final | gdn | value | 171 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup | question | all | value | 171 | 88% [82,92] | 8% | -0.54 [-0.69,-0.41] | 1.00 | +12 [+8,+18] | partial |
| RL | lookup | question | attn | value | 171 | 89% [83,93] | 8% | -0.44 [-0.58,-0.32] | - | +11 [+6,+16] | partial |
| RL | lookup | question | gdn | value | 171 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | both | attn | value | 171 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 171 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | all | value | 171 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | attn | value | 171 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 171 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 171 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | attn | value | 171 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 171 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
