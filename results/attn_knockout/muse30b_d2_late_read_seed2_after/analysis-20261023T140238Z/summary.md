# attn_knockout / muse30b_d2_late_read_seed2_after

Measure: correct (items: {"RL": {"items": 300, "unedited_right": 299}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.013,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.505,
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
| RL | lookup | after | all | value | 299 | 2% [1,4] | 92% | -3.56 [-3.72,-3.41] | - | +97 [+95,+98] | needed |
| RL | lookup | final | all | value | 299 | 1% [1,3] | 97% | -5.96 [-6.17,-5.76] | - | +98 [+97,+100] | needed |
| RL | lookup | question | all | value | 299 | 51% [45,56] | 39% | -1.38 [-1.51,-1.25] | - | +49 [+43,+55] | needed |
| RL | lookup_off | after | all | value | 299 | 99% [97,99] | 1% | -0.04 [-0.06,-0.03] | - | - | not_needed |
| RL | lookup_off | final | all | value | 299 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | all | value | 299 | 100% [98,100] | 0% | +0.00 [-0.01,+0.01] | - | - | not_needed |
