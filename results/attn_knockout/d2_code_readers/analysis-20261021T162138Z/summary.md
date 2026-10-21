# attn_knockout / d2_code_readers

Measure: correct (items: {"DK": {"items": 200, "unedited_right": 200}, "IX": {"items": 200, "unedited_right": 200}, "CH2": {"items": 200, "unedited_right": 199}, "CH3": {"items": 200, "unedited_right": 200}, "RK": {"items": 100, "unedited_right": 100}})

Claims: {
 "positive_control": {},
 "late_attention_read": {
  "DK": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.475,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": null,
    "verdict": null
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "IX": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.35,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": null,
    "verdict": null
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "CH2": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.412,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": null,
    "verdict": null
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "CH3": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.325,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": null,
    "verdict": null
   },
   "late_attention_read": null,
   "bands": {
    "early": null,
    "middle": null,
    "late": null
   }
  },
  "RK": {
   "path": true,
   "final": {
    "all": {
     "acc": 0.2,
     "verdict": "needed"
    }
   },
   "question_all": {
    "acc": null,
    "verdict": null
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
   "final": null,
   "question": null
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
| DK | lookup | after | all | value | 200 | 2% [1,6] | 21% | -3.45 [-3.60,-3.31] | 0.96 | +98 [+95,+100] | needed |
| DK | lookup | after_dict | all | value | 200 | 0% [0,2] | 9% | -3.54 [-3.68,-3.38] | 0.99 | +100 [+100,+100] | needed |
| DK | lookup | final | all | value | 200 | 48% [41,54] | 46% | -2.53 [-2.88,-2.18] | 1.00 | +52 [+46,+59] | needed |
| DK | lookup | final+print | all | value | 200 | 0% [0,2] | 6% | -3.55 [-3.70,-3.40] | 0.99 | +100 [+100,+100] | needed |
| DK | lookup | final+print+selector+nl | all | value | 200 | 0% [0,2] | 9% | -3.54 [-3.69,-3.39] | 0.99 | +100 [+100,+100] | needed |
| DK | lookup | nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup | print | all | value | 200 | 6% [3,10] | 2% | -2.37 [-2.48,-2.26] | 0.97 | +94 [+90,+97] | needed |
| DK | lookup_off | after | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| DK | lookup_off | after_dict | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | final | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| DK | lookup_off | final+print | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | final+print+selector+nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| DK | lookup_off | nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| DK | lookup_off | print | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| IX | lookup | after | all | value | 200 | 3% [1,6] | 68% | -3.76 [-3.93,-3.58] | 0.97 | +97 [+94,+99] | needed |
| IX | lookup | after_dict | all | value | 200 | 6% [4,11] | 72% | -3.76 [-3.94,-3.58] | 0.99 | +94 [+90,+97] | needed |
| IX | lookup | final | all | value | 200 | 35% [29,42] | 61% | -3.35 [-3.75,-2.96] | 1.00 | +65 [+58,+72] | needed |
| IX | lookup | final+print | all | value | 200 | 34% [28,41] | 62% | -3.42 [-3.83,-3.02] | 0.99 | +66 [+59,+72] | needed |
| IX | lookup | final+print+selector | all | value | 200 | 7% [4,11] | 70% | -3.73 [-3.92,-3.55] | 0.99 | +93 [+90,+96] | needed |
| IX | lookup | final+print+selector+nl | all | value | 200 | 6% [4,11] | 72% | -3.75 [-3.93,-3.56] | 0.99 | +94 [+90,+97] | needed |
| IX | lookup | final+selector | all | value | 200 | 6% [4,11] | 74% | -3.77 [-3.95,-3.58] | 0.99 | +94 [+90,+96] | needed |
| IX | lookup | list | all | value | 200 | 44% [37,50] | 46% | -1.66 [-1.83,-1.50] | 0.98 | +56 [+49,+63] | needed |
| IX | lookup | nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| IX | lookup | print | all | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| IX | lookup_off | after | all | value | 200 | 100% [98,100] | 0% | -0.01 [-0.02,-0.01] | 0.97 | - | not_needed |
| IX | lookup_off | after_dict | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| IX | lookup_off | final | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final+print | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | final+print+selector | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| IX | lookup_off | final+print+selector+nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| IX | lookup_off | final+selector | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| IX | lookup_off | list | all | value | 200 | 100% [97,100] | 0% | -0.02 [-0.05,-0.01] | 0.98 | - | not_needed |
| IX | lookup_off | nl | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| IX | lookup_off | print | all | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup | after | all | value | 199 | 1% [0,4] | 87% | -5.34 [-5.60,-5.06] | 0.97 | +99 [+97,+100] | needed |
| CH2 | lookup | after_dict | all | value | 199 | 6% [3,10] | 89% | -5.06 [-5.38,-4.76] | 0.99 | +94 [+91,+97] | needed |
| CH2 | lookup | chain_distractor1 | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| CH2 | lookup | chain_distractor2 | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup | chain_target1 | all | value | 199 | 44% [37,51] | 54% | -1.96 [-2.20,-1.72] | 0.98 | +56 [+49,+63] | needed |
| CH2 | lookup | chain_target2 | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup | final | all | value | 199 | 41% [35,48] | 56% | -3.27 [-3.68,-2.86] | 1.00 | +59 [+52,+65] | needed |
| CH2 | lookup | final+print | all | value | 199 | 37% [30,44] | 60% | -3.45 [-3.87,-3.02] | 1.00 | +63 [+56,+70] | needed |
| CH2 | lookup | final+print+selector | all | value | 199 | 6% [3,10] | 88% | -4.95 [-5.26,-4.66] | 0.99 | +94 [+90,+97] | needed |
| CH2 | lookup | final+print+selector+nl | all | value | 199 | 6% [3,10] | 89% | -5.03 [-5.34,-4.73] | 0.99 | +94 [+91,+97] | needed |
| CH2 | lookup | final+selector | all | value | 199 | 7% [4,11] | 88% | -4.97 [-5.27,-4.67] | 0.99 | +93 [+90,+96] | needed |
| CH2 | lookup | nl | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| CH2 | lookup | print | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | after | all | value | 199 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| CH2 | lookup_off | after_dict | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | chain_distractor1 | all | value | 199 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| CH2 | lookup_off | chain_distractor2 | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | chain_target1 | all | value | 199 | 99% [97,100] | 1% | -0.01 [-0.02,-0.00] | 0.97 | - | not_needed |
| CH2 | lookup_off | chain_target2 | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | final | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final+print | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | final+print+selector | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | final+print+selector+nl | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | final+selector | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH2 | lookup_off | nl | all | value | 199 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH2 | lookup_off | print | all | value | 199 | 100% [98,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| CH3 | lookup | after | all | value | 200 | 1% [0,4] | 97% | -6.15 [-6.38,-5.91] | 0.97 | +99 [+98,+100] | needed |
| CH3 | lookup | after_dict | all | value | 200 | 6% [3,10] | 94% | -6.06 [-6.35,-5.76] | 0.99 | +94 [+91,+98] | needed |
| CH3 | lookup | chain_distractor1 | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| CH3 | lookup | chain_distractor2 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup | chain_distractor3 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup | chain_target1 | all | value | 200 | 40% [34,47] | 60% | -1.73 [-1.94,-1.52] | 0.98 | +58 [+52,+66] | needed |
| CH3 | lookup | chain_target2 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup | chain_target3 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup | final | all | value | 200 | 32% [26,39] | 66% | -3.86 [-4.31,-3.44] | 1.00 | +68 [+61,+74] | needed |
| CH3 | lookup | final+print | all | value | 200 | 33% [27,40] | 65% | -3.95 [-4.40,-3.52] | 1.00 | +67 [+60,+74] | needed |
| CH3 | lookup | final+print+selector | all | value | 200 | 6% [4,11] | 94% | -5.85 [-6.14,-5.55] | 0.99 | +94 [+90,+97] | needed |
| CH3 | lookup | final+print+selector+nl | all | value | 200 | 6% [3,10] | 94% | -6.06 [-6.35,-5.76] | 0.99 | +94 [+91,+98] | needed |
| CH3 | lookup | final+selector | all | value | 200 | 6% [4,11] | 94% | -5.84 [-6.12,-5.54] | 0.99 | +94 [+90,+97] | needed |
| CH3 | lookup | nl | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup | print | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | after | all | value | 200 | 100% [98,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| CH3 | lookup_off | after_dict | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| CH3 | lookup_off | chain_distractor1 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.98 | - | not_needed |
| CH3 | lookup_off | chain_distractor2 | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | chain_distractor3 | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | chain_target1 | all | value | 200 | 99% [96,100] | 1% | -0.01 [-0.03,-0.00] | 0.98 | - | not_needed |
| CH3 | lookup_off | chain_target2 | all | value | 200 | 100% [97,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | chain_target3 | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | final | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | final+print | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 1.00 | - | not_needed |
| CH3 | lookup_off | final+print+selector | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| CH3 | lookup_off | final+print+selector+nl | all | value | 200 | 100% [98,100] | 0% | +0.00 [-0.00,+0.01] | 0.99 | - | not_needed |
| CH3 | lookup_off | final+selector | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.01,+0.00] | 0.99 | - | not_needed |
| CH3 | lookup_off | nl | all | value | 200 | 100% [98,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| CH3 | lookup_off | print | all | value | 200 | 100% [98,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup | after | all | value | 100 | 3% [1,8] | 93% | -4.92 [-5.26,-4.58] | 0.96 | +96 [+92,+99] | needed |
| RK | lookup | after_dict | all | value | 100 | 2% [1,7] | 97% | -5.12 [-5.45,-4.77] | 0.99 | +98 [+95,+100] | needed |
| RK | lookup | final | all | value | 100 | 20% [13,29] | 80% | -3.96 [-4.40,-3.48] | 1.00 | +80 [+72,+87] | needed |
| RK | lookup | final+print+selector+nl | all | value | 100 | 2% [1,7] | 97% | -5.12 [-5.45,-4.77] | 0.99 | +98 [+95,+100] | needed |
| RK | lookup | nl | all | value | 100 | 91% [84,95] | 9% | -0.26 [-0.35,-0.18] | 0.99 | +9 [+4,+15] | partial |
| RK | lookup_off | after | all | value | 100 | 99% [95,100] | 1% | -0.06 [-0.15,-0.01] | 0.96 | - | not_needed |
| RK | lookup_off | after_dict | all | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RK | lookup_off | final | all | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RK | lookup_off | final+print+selector+nl | all | value | 100 | 100% [96,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RK | lookup_off | nl | all | value | 100 | 100% [96,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
