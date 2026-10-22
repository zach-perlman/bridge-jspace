# attn_knockout / qwen35_9b_d2_late_read_long

Measure: correct (items: {"RL": {"items": 156, "unedited_right": 156}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.013,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.006,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.519,
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
| RL | lookup | both | attn | value | 156 | 0% [0,2] | 98% | -4.27 [-4.50,-4.06] | - | +99 [+98,+100] | needed |
| RL | lookup | both | gdn | value | 156 | 98% [94,99] | 2% | -0.04 [-0.05,-0.03] | 1.00 | - | not_needed |
| RL | lookup | final | all | value | 156 | 1% [0,5] | 99% | -4.70 [-4.90,-4.50] | 1.00 | +99 [+97,+100] | needed |
| RL | lookup | final | attn | value | 156 | 1% [0,4] | 99% | -4.65 [-4.86,-4.45] | - | +99 [+98,+100] | needed |
| RL | lookup | final | gdn | value | 156 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup | question | all | value | 156 | 52% [44,60] | 47% | -1.16 [-1.29,-1.06] | 1.00 | +47 [+40,+55] | needed |
| RL | lookup | question | attn | value | 156 | 51% [44,59] | 47% | -1.16 [-1.30,-1.03] | - | +48 [+40,+56] | needed |
| RL | lookup | question | gdn | value | 156 | 98% [94,99] | 2% | -0.04 [-0.06,-0.03] | 1.00 | - | not_needed |
| RL | lookup_off | both | attn | value | 156 | 99% [96,100] | 1% | +0.02 [+0.00,+0.03] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 156 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | all | value | 156 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | 1.00 | - | not_needed |
| RL | lookup_off | final | attn | value | 156 | 100% [98,100] | 0% | +0.01 [+0.01,+0.02] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 156 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 156 | 99% [96,100] | 1% | -0.00 [-0.01,+0.01] | 1.00 | - | not_needed |
| RL | lookup_off | question | attn | value | 156 | 99% [96,100] | 1% | -0.00 [-0.01,+0.01] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 156 | 99% [96,100] | 1% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
