# attn_knockout / qwen35_9b_d2_late_read_seed2

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.01,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.013,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.997,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.653,
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
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | both | attn | value | 300 | 2% [1,4] | 94% | -4.30 [-4.48,-4.14] | - | +98 [+96,+99] | needed |
| RL | lookup | both | gdn | value | 300 | 97% [94,98] | 2% | -0.14 [-0.16,-0.11] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 300 | 1% [0,3] | 98% | -4.74 [-4.91,-4.58] | 0.98 | +99 [+98,+100] | needed |
| RL | lookup | final | attn | value | 300 | 1% [1,3] | 98% | -4.50 [-4.67,-4.34] | - | +99 [+97,+100] | needed |
| RL | lookup | final | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 65% [60,70] | 27% | -0.95 [-1.04,-0.86] | 0.97 | +34 [+29,+39] | needed |
| RL | lookup | question | attn | value | 300 | 74% [68,78] | 24% | -0.76 [-0.86,-0.66] | - | +26 [+21,+31] | needed |
| RL | lookup | question | gdn | value | 300 | 97% [95,99] | 2% | -0.13 [-0.16,-0.11] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | +0.02 [+0.01,+0.02] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 99% [98,100] | 1% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | +0.01 [-0.00,+0.01] | 0.97 | - | not_needed |
