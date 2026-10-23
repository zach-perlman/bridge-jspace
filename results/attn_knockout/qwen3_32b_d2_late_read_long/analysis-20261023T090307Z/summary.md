# attn_knockout / qwen3_32b_d2_late_read_long

Measure: correct (items: {"RL": {"items": 93, "unedited_right": 93}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.022,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.43,
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
| RL | lookup | final | all | value | 93 | 2% [1,8] | 94% | -8.81 [-9.46,-8.13] | - | +98 [+95,+100] | needed |
| RL | lookup | question | all | value | 93 | 43% [33,53] | 29% | -2.33 [-2.81,-1.86] | - | +57 [+47,+67] | needed |
| RL | lookup_off | final | all | value | 93 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | all | value | 93 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
