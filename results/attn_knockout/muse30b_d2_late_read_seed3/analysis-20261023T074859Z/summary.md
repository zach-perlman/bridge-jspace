# attn_knockout / muse30b_d2_late_read_seed3

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 300}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.02,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.463,
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
 "bands": {}
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | final | all | value | 300 | 2% [1,4] | 98% | -5.97 [-6.15,-5.77] | - | +98 [+96,+99] | needed |
| RL | lookup | question | all | value | 300 | 46% [41,52] | 40% | -1.48 [-1.61,-1.34] | - | +53 [+47,+59] | needed |
| RL | lookup_off | final | all | value | 300 | 100% [99,100] | 0% | +0.00 [-0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | all | value | 300 | 100% [98,100] | 0% | -0.01 [-0.02,+0.00] | - | - | not_needed |
