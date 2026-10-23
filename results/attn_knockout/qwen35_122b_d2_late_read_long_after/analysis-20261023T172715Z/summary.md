# attn_knockout / qwen35_122b_d2_late_read_long_after

Measure: correct (items: {"RL": {"items": 172, "unedited_right": 172}})

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
     "acc": 0.994,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.855,
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
| RL | lookup | after | all | value | 172 | 3% [1,7] | 77% | -3.85 [-4.11,-3.60] | 1.00 | +97 [+94,+99] | needed |
| RL | lookup | after | attn | value | 172 | 2% [1,5] | 86% | -4.20 [-4.45,-3.94] | - | +98 [+96,+100] | needed |
| RL | lookup | after | gdn | value | 172 | 98% [95,99] | 2% | -0.05 [-0.10,-0.02] | 1.00 | - | not_needed |
| RL | lookup | both | attn | value | 172 | 5% [2,9] | 84% | -3.96 [-4.22,-3.68] | - | +95 [+91,+98] | needed |
| RL | lookup | both | gdn | value | 172 | 99% [96,100] | 1% | -0.02 [-0.05,-0.00] | 1.00 | - | not_needed |
| RL | lookup | final | all | value | 172 | 7% [4,12] | 91% | -4.49 [-4.75,-4.22] | 1.00 | +93 [+89,+97] | needed |
| RL | lookup | final | attn | value | 172 | 7% [4,12] | 91% | -4.45 [-4.72,-4.18] | - | +93 [+89,+97] | needed |
| RL | lookup | final | gdn | value | 172 | 99% [97,100] | 1% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| RL | lookup | question | all | value | 172 | 85% [79,90] | 7% | -0.59 [-0.74,-0.45] | 1.00 | +13 [+8,+18] | partial |
| RL | lookup | question | attn | value | 172 | 88% [82,92] | 9% | -0.46 [-0.60,-0.34] | - | +12 [+7,+16] | partial |
| RL | lookup | question | gdn | value | 172 | 99% [96,100] | 1% | -0.02 [-0.04,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | after | all | value | 172 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | after | attn | value | 172 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | after | gdn | value | 172 | 99% [97,100] | 1% | -0.01 [-0.03,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | both | attn | value | 172 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 172 | 99% [97,100] | 1% | -0.00 [-0.01,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | all | value | 172 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | attn | value | 172 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 172 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 172 | 99% [96,100] | 1% | -0.01 [-0.02,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | attn | value | 172 | 99% [97,100] | 1% | -0.00 [-0.01,+0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 172 | 99% [97,100] | 1% | -0.01 [-0.01,-0.00] | 1.00 | - | not_needed |
