# attn_knockout / olmo3_7b_instruct_d2_late_read_seed3

Measure: correct (items: {"RL": {"items": 100, "unedited_right": 99}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.01,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.263,
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
| RL | lookup | final | all | value | 99 | 1% [0,6] | 97% | -8.23 [-8.88,-7.62] | - | +99 [+97,+100] | needed |
| RL | lookup | question | all | value | 99 | 26% [19,36] | 19% | -3.24 [-3.72,-2.77] | - | +73 [+63,+81] | needed |
| RL | lookup_off | final | all | value | 99 | 100% [96,100] | 0% | +0.00 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | all | value | 99 | 99% [94,100] | 1% | -0.01 [-0.03,+0.00] | - | - | not_needed |
