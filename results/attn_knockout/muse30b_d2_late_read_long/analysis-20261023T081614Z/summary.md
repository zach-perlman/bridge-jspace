# attn_knockout / muse30b_d2_late_read_long

Measure: correct (items: {"RL": {"items": 167, "unedited_right": 167}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.168,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": 0.659,
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
| RL | lookup | final | all | value | 167 | 17% [12,23] | 83% | -3.59 [-3.87,-3.29] | - | +83 [+77,+89] | needed |
| RL | lookup | question | all | value | 167 | 66% [58,73] | 34% | -0.87 [-1.01,-0.73] | - | +34 [+27,+41] | needed |
| RL | lookup_off | final | all | value | 167 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
| RL | lookup_off | question | all | value | 167 | 100% [98,100] | 0% | +0.01 [+0.00,+0.01] | - | - | not_needed |
