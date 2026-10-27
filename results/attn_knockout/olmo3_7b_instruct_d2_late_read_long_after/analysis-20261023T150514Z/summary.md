# attn_knockout / olmo3_7b_instruct_d2_late_read_long_after

Measure: correct (items: {"RL": {"items": 41, "unedited_right": 41}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.049,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.195,
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
| RL | lookup | after | all | value | 41 | 10% [4,23] | 71% | -4.04 [-4.50,-3.56] | - | +85 [+73,+95] | needed |
| RL | lookup | final | all | value | 41 | 5% [1,16] | 95% | -6.16 [-7.01,-5.33] | - | +95 [+88,+100] | needed |
| RL | lookup | question | all | value | 41 | 20% [10,34] | 56% | -2.64 [-3.20,-2.13] | - | +80 [+68,+93] | needed |
| RL | lookup_off | after | all | value | 41 | 95% [84,99] | 2% | -0.18 [-0.45,-0.02] | - | - | partial |
| RL | lookup_off | final | all | value | 41 | 100% [91,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | all | value | 41 | 100% [91,100] | 0% | -0.00 [-0.02,+0.01] | - | - | not_needed |
