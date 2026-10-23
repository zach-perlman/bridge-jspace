# attn_knockout / olmo_hybrid_7b_d2_late_read_long

Measure: correct (items: {"RL": {"items": 53, "unedited_right": 53}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.075,
     "verdict": "needed"
    },
    "attn": {
     "acc": 0.075,
     "verdict": "needed"
    },
    "gdn": {
     "acc": 1.0,
     "verdict": "not_needed"
    }
   },
   "question_all": {
    "acc": 0.245,
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
| RL | lookup | both | attn | value | 53 | 2% [0,10] | 85% | -4.62 [-5.20,-4.08] | - | +96 [+91,+100] | needed |
| RL | lookup | both | gdn | value | 53 | 100% [93,100] | 0% | -0.03 [-0.06,-0.02] | 1.00 | - | not_needed |
| RL | lookup | final | all | value | 53 | 8% [3,18] | 79% | -4.43 [-5.01,-3.86] | 1.00 | +92 [+85,+98] | needed |
| RL | lookup | final | attn | value | 53 | 8% [3,18] | 79% | -4.19 [-4.75,-3.61] | - | +92 [+85,+98] | needed |
| RL | lookup | final | gdn | value | 53 | 100% [93,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup | question | all | value | 53 | 25% [15,38] | 68% | -2.91 [-3.51,-2.36] | 1.00 | +74 [+60,+85] | needed |
| RL | lookup | question | attn | value | 53 | 30% [20,44] | 62% | -2.89 [-3.53,-2.27] | - | +68 [+55,+79] | needed |
| RL | lookup | question | gdn | value | 53 | 100% [93,100] | 0% | -0.03 [-0.05,-0.01] | 1.00 | - | not_needed |
| RL | lookup_off | both | attn | value | 53 | 98% [90,100] | 2% | -0.02 [-0.05,+0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 53 | 100% [93,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | all | value | 53 | 100% [93,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| RL | lookup_off | final | attn | value | 53 | 100% [93,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 53 | 100% [93,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 53 | 98% [90,100] | 2% | -0.03 [-0.07,-0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | attn | value | 53 | 98% [90,100] | 2% | -0.02 [-0.07,-0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 53 | 100% [93,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
