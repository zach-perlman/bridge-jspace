# attn_knockout / qwen35_9b_d2_late_read_seed2_after

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
    "acc": 0.66,
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
| RL | lookup | after | all | value | 300 | 4% [2,6] | 87% | -4.07 [-4.27,-3.89] | 0.94 | +95 [+93,+98] | needed |
| RL | lookup | after | attn | value | 300 | 1% [1,3] | 96% | -4.40 [-4.58,-4.24] | - | +98 [+97,+100] | needed |
| RL | lookup | after | gdn | value | 300 | 84% [80,88] | 13% | -0.41 [-0.49,-0.34] | 0.94 | +15 [+11,+19] | partial |
| RL | lookup | both | attn | value | 300 | 2% [1,4] | 94% | -4.29 [-4.47,-4.12] | - | +98 [+96,+99] | needed |
| RL | lookup | both | gdn | value | 300 | 97% [94,98] | 2% | -0.14 [-0.16,-0.11] | 0.97 | - | not_needed |
| RL | lookup | final | all | value | 300 | 1% [0,3] | 98% | -4.74 [-4.91,-4.58] | 0.98 | +99 [+97,+100] | needed |
| RL | lookup | final | attn | value | 300 | 1% [1,3] | 98% | -4.50 [-4.67,-4.34] | - | +99 [+97,+100] | needed |
| RL | lookup | final | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 66% [60,71] | 27% | -0.95 [-1.04,-0.86] | 0.97 | +33 [+28,+38] | needed |
| RL | lookup | question | attn | value | 300 | 73% [67,77] | 25% | -0.76 [-0.85,-0.66] | - | +27 [+22,+32] | needed |
| RL | lookup | question | gdn | value | 300 | 97% [95,99] | 2% | -0.13 [-0.16,-0.11] | 0.97 | - | not_needed |
| RL | lookup_off | after | all | value | 300 | 99% [97,100] | 1% | +0.00 [-0.01,+0.02] | 0.95 | - | not_needed |
| RL | lookup_off | after | attn | value | 300 | 100% [98,100] | 0% | +0.01 [-0.00,+0.02] | - | - | not_needed |
| RL | lookup_off | after | gdn | value | 300 | 99% [98,100] | 1% | -0.02 [-0.04,-0.01] | 0.94 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | +0.02 [+0.01,+0.02] | 0.97 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 99% [98,100] | 1% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | +0.01 [+0.00,+0.02] | 0.97 | - | not_needed |
