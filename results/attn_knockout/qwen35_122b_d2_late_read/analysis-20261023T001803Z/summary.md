# attn_knockout / qwen35_122b_d2_late_read

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.053,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.05,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 0.997,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.57,
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
| RL | lookup | both | attn | value | 300 | 8% [5,11] | 73% | -3.78 [-4.00,-3.57] | - | +92 [+89,+95] | needed |
| RL | lookup | both | gdn | value | 300 | 97% [95,99] | 1% | -0.07 [-0.11,-0.04] | 0.98 | - | not_needed |
| RL | lookup | final | all | value | 300 | 5% [3,8] | 93% | -4.74 [-4.97,-4.52] | 0.99 | +95 [+92,+97] | needed |
| RL | lookup | final | attn | value | 300 | 5% [3,8] | 94% | -4.49 [-4.71,-4.28] | - | +95 [+92,+97] | needed |
| RL | lookup | final | gdn | value | 300 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 300 | 57% [51,62] | 13% | -1.30 [-1.45,-1.15] | 0.97 | +43 [+37,+49] | needed |
| RL | lookup | question | attn | value | 300 | 78% [73,82] | 10% | -0.69 [-0.81,-0.58] | - | +22 [+18,+27] | needed |
| RL | lookup | question | gdn | value | 300 | 98% [95,99] | 1% | -0.07 [-0.11,-0.04] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 300 | 100% [99,100] | 0% | +0.01 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.02] | 0.98 | - | not_needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | final | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [+0.00,+0.01] | 0.99 | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | 0.97 | - | not_needed |
| RL | lookup_off | question | attn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 300 | 100% [99,100] | 0% | +0.00 [-0.01,+0.01] | 0.97 | - | not_needed |
