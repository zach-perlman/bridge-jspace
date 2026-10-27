# attn_knockout / olmo3_7b_instruct_d2_smoke_v3

Measure: correct (items: {"RL": {"items": 3, "unedited_right": 3}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "RL": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.0,
     "verdict": "needed"
    },
    "band00-03": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band00-15": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band04-07": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band08-11": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band12-15": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band16-19": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band16-23": {
     "acc": 0.333,
     "verdict": "partial"
    },
    "band20-23": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band24-31": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band24-27": {
     "acc": 1.0,
     "verdict": "partial"
    },
    "band28-31": {
     "acc": 1.0,
     "verdict": "partial"
    }
   },
   "question_all": {
    "acc": 0.0,
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
  "RL": "needed",
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
  "RL/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  }
 }
}

| family | source | dest | layers | DeltaNet mode | n | accuracy [95%] | confusion | dlogp [95%] | norm ratio | vs control | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RL | lookup | after | all | value | 3 | 0% [0,56] | 33% | -5.24 [-6.76,-3.86] | - | +100 [+100,+100] | needed |
| RL | lookup | both | all | value | 3 | 0% [0,56] | 0% | -5.52 [-6.76,-4.28] | - | +100 [+100,+100] | needed |
| RL | lookup | final | all | value | 3 | 0% [0,56] | 100% | -7.01 [-9.00,-3.17] | - | +100 [+100,+100] | needed |
| RL | lookup | final | band00-03 | value | 3 | 100% [44,100] | 0% | +0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band00-15 | value | 3 | 100% [44,100] | 0% | -0.04 [-0.12,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band04-07 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band08-11 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band12-15 | value | 3 | 100% [44,100] | 0% | -0.04 [-0.12,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band16-19 | value | 3 | 100% [44,100] | 0% | -0.11 [-0.30,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band16-23 | value | 3 | 33% [6,79] | 67% | -1.82 [-3.63,-0.37] | - | +67 [+0,+100] | partial |
| RL | lookup | final | band20-23 | value | 3 | 100% [44,100] | 0% | -0.06 [-0.16,-0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band24-27 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band24-31 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | final | band28-31 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | +0 [+0,+0] | partial |
| RL | lookup | question | all | value | 3 | 0% [0,56] | 0% | -4.25 [-5.61,-2.87] | - | +100 [+100,+100] | needed |
| RL | lookup_off | after | all | value | 3 | 100% [44,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | both | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.01,+0.00] | - | - | partial |
| RL | lookup_off | final | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band00-03 | value | 3 | 100% [44,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band00-15 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band04-07 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band08-11 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band12-15 | value | 3 | 100% [44,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band16-19 | value | 3 | 100% [44,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band16-23 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band20-23 | value | 3 | 100% [44,100] | 0% | +0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band24-27 | value | 3 | 100% [44,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band24-31 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | final | band28-31 | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | lookup_off | question | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | after | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | both | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | final | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | random | question | all | value | 3 | 100% [44,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | trailing | after | all | value | 2 | 100% [34,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | trailing | both | all | value | 2 | 100% [34,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
| RL | trailing | final | all | value | 2 | 100% [34,100] | 0% | +0.00 [+0.00,+0.00] | - | - | partial |
| RL | trailing | question | all | value | 2 | 100% [34,100] | 0% | -0.00 [-0.00,+0.00] | - | - | partial |
