# attn_knockout / d2_ko_core_v1

Measure: correct (items: {"BL": {"items": 60, "unedited_right": 60}, "BR": {"items": 60, "unedited_right": 60}, "RL": {"items": 60, "unedited_right": 60}, "RR": {"items": 60, "unedited_right": 60}})

Claims: {
 "positive_control": {
  "BL": {
   "sources": {
    "lookup": "needed",
    "binding": "needed"
   },
   "passed": true
  },
  "BR": {
   "sources": {
    "binding": "needed"
   },
   "passed": true
  },
  "RL": {
   "sources": {
    "lookup": "needed"
   },
   "passed": true
  }
 },
 "C1a_RL_breaks_RR_survives": {
  "RL": "needed",
  "RR": "not_needed",
  "holds": true
 },
 "C1b_answer_site_reads_lookup": {
  "BL": {
   "final": "needed",
   "question": "not_needed"
  },
  "RL": {
   "final": "needed",
   "question": "not_needed"
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
 "C1b_holds": true,
 "relay_holds": false,
 "recall_needs_no_locker": {
  "BR": {
   "question": "not_needed",
   "final": "not_needed",
   "both": "not_needed",
   "after": "not_needed"
  },
  "RR": {
   "question": "not_needed",
   "final": "not_needed",
   "both": "not_needed",
   "after": "not_needed"
  }
 },
 "binding_BL_vs_BR": {
  "BL": {
   "question": "needed",
   "final": "not_needed",
   "both": "needed",
   "after": "needed"
  },
  "BR": {
   "question": "needed",
   "final": "partial",
   "both": "needed",
   "after": "needed"
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
  "BL/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/lookup/both": {
   "windows_needed": [
    "win48-55",
    "win48-55:attn"
   ],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/binding/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BL/binding/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BR/binding/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BR/binding/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "BR/binding/both": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "kind_needed": [
    "attn"
   ],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
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
  "RR/lookup/question": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/final": {
   "windows_needed": [],
   "suf_needed": [],
   "pre_needed": [],
   "suf_max_needed": null,
   "pre_min_needed": null
  },
  "RR/lookup/both": {
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
| BL | binding | after | all | absent | 60 | 37% [26,49] | 63% | -1.26 [-1.39,-1.12] | 0.98 | +63 [+52,+77] | needed |
| BL | binding | after | all | value | 60 | 37% [26,49] | 63% | -1.28 [-1.41,-1.15] | 0.95 | +63 [+52,+75] | needed |
| BL | binding | both | all | absent | 60 | 45% [33,58] | 50% | -1.46 [-1.61,-1.31] | 0.99 | +55 [+42,+67] | needed |
| BL | binding | both | all | value | 60 | 43% [32,56] | 52% | -1.46 [-1.61,-1.32] | 0.98 | +57 [+43,+70] | needed |
| BL | binding | both | attn | value | 60 | 47% [35,59] | 52% | -1.40 [-1.54,-1.27] | - | +53 [+40,+67] | needed |
| BL | binding | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win24-31 | value | 60 | 92% [82,96] | 8% | -0.17 [-0.28,-0.09] | 0.99 | +8 [+2,+17] | partial |
| BL | binding | both | win24-31:attn | value | 60 | 93% [84,97] | 7% | -0.15 [-0.26,-0.08] | - | +7 [+2,+13] | partial |
| BL | binding | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | final | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding | question | all | value | 60 | 58% [46,70] | 38% | -1.21 [-1.34,-1.10] | 0.98 | +42 [+30,+53] | needed |
| BL | binding | question | attn | value | 60 | 58% [46,70] | 40% | -1.22 [-1.34,-1.12] | - | +42 [+30,+55] | needed |
| BL | binding | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | binding | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | binding | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win24-31 | value | 60 | 93% [84,97] | 7% | -0.17 [-0.27,-0.09] | 0.98 | +7 [+2,+13] | partial |
| BL | binding | question | win24-31:attn | value | 60 | 95% [86,98] | 5% | -0.15 [-0.25,-0.08] | - | +5 [+0,+12] | partial |
| BL | binding | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.03,-0.00] | 0.95 | - | not_needed |
| BL | binding_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | binding_off | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | binding_off | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | final | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | binding_off | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | binding_off | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | binding_off | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | binding_off | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | binding_off | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | after | all | absent | 60 | 2% [0,9] | 57% | -3.61 [-3.98,-3.27] | 0.98 | +98 [+95,+100] | needed |
| BL | lookup | after | all | value | 60 | 2% [0,9] | 55% | -3.52 [-3.92,-3.15] | 0.93 | +98 [+95,+100] | needed |
| BL | lookup | both | all | absent | 60 | 0% [-0,6] | 92% | -4.37 [-4.69,-4.05] | 0.99 | +100 [+100,+100] | needed |
| BL | lookup | both | all | value | 60 | 2% [0,9] | 92% | -4.53 [-4.89,-4.17] | 0.97 | +98 [+95,+100] | needed |
| BL | lookup | both | attn | value | 60 | 0% [-0,6] | 95% | -4.66 [-5.05,-4.26] | - | +100 [+100,+100] | needed |
| BL | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| BL | lookup | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| BL | lookup | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| BL | lookup | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | both | win40-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| BL | lookup | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win48-55 | value | 60 | 77% [65,86] | 23% | -0.62 [-0.86,-0.39] | 0.97 | +23 [+13,+35] | needed |
| BL | lookup | both | win48-55:attn | value | 60 | 78% [66,87] | 22% | -0.64 [-0.88,-0.41] | - | +22 [+12,+33] | needed |
| BL | lookup | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | both | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup | final | all | value | 60 | 3% [1,11] | 85% | -3.96 [-4.29,-3.61] | 0.98 | +97 [+92,+100] | needed |
| BL | lookup | final | attn | value | 60 | 3% [1,11] | 90% | -3.84 [-4.21,-3.47] | - | +97 [+92,+100] | needed |
| BL | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | - | - | not_needed |
| BL | lookup | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win48-55 | value | 60 | 85% [74,92] | 15% | -0.40 [-0.57,-0.24] | 0.98 | +15 [+7,+25] | partial |
| BL | lookup | final | win48-55:attn | value | 60 | 83% [72,91] | 17% | -0.42 [-0.60,-0.25] | - | +17 [+8,+27] | partial |
| BL | lookup | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | lookup | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| BL | lookup | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | question | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BL | lookup | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup | question | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.93 | - | not_needed |
| BL | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup_off | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup_off | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup_off | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup_off | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup_off | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BL | lookup_off | final | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | final | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | lookup_off | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 1.00 | - | not_needed |
| BL | lookup_off | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| BL | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | lookup_off | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.93 | - | not_needed |
| BL | lookup_off | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.93 | - | not_needed |
| BL | lookup_off | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup_off | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.94 | - | not_needed |
| BL | lookup_off | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| BL | lookup_off | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | lookup_off | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | lookup_off | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | lookup_off | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.03,-0.00] | 0.99 | - | not_needed |
| BL | random | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.01] | 0.94 | - | not_needed |
| BL | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | final | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BL | random | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | random | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BL | random | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BL | random | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BL | random | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | random | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BL | random | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BL | trailing | after | all | absent | 60 | 92% [82,96] | 8% | -0.20 [-0.29,-0.13] | 0.99 | - | partial |
| BL | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.02 [-0.02,-0.01] | 0.95 | - | not_needed |
| BL | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BL | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BL | trailing | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | binding | after | all | absent | 60 | 40% [29,53] | 25% | -1.47 [-1.71,-1.25] | 0.98 | +60 [+47,+73] | needed |
| BR | binding | after | all | value | 60 | 43% [32,56] | 27% | -1.38 [-1.60,-1.18] | 0.95 | +57 [+43,+70] | needed |
| BR | binding | both | all | absent | 60 | 10% [5,20] | 20% | -2.47 [-2.81,-2.13] | 0.99 | +90 [+82,+97] | needed |
| BR | binding | both | all | value | 60 | 12% [6,22] | 23% | -2.48 [-2.82,-2.14] | 0.98 | +88 [+80,+97] | needed |
| BR | binding | both | attn | value | 60 | 15% [8,26] | 22% | -2.06 [-2.37,-1.78] | - | +85 [+75,+93] | needed |
| BR | binding | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win24-31 | value | 60 | 93% [84,97] | 7% | -0.19 [-0.40,-0.06] | 0.98 | +7 [+2,+13] | partial |
| BR | binding | both | win24-31:attn | value | 60 | 93% [84,97] | 7% | -0.17 [-0.36,-0.06] | - | +7 [+2,+13] | partial |
| BR | binding | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.07 [-0.10,-0.04] | 0.98 | - | not_needed |
| BR | binding | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.03 [-0.05,-0.02] | - | - | not_needed |
| BR | binding | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | final | all | value | 60 | 87% [76,93] | 12% | -0.38 [-0.60,-0.19] | 0.99 | +13 [+5,+23] | partial |
| BR | binding | final | attn | value | 60 | 92% [82,96] | 8% | -0.16 [-0.26,-0.07] | - | +8 [+2,+17] | partial |
| BR | binding | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | binding | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | binding | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | binding | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.03 [-0.05,-0.02] | 0.99 | - | not_needed |
| BR | binding | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.01] | - | - | not_needed |
| BR | binding | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | binding | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | binding | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding | question | all | value | 60 | 18% [11,30] | 18% | -1.68 [-1.92,-1.45] | 0.98 | +82 [+72,+90] | needed |
| BR | binding | question | attn | value | 60 | 22% [13,34] | 13% | -1.61 [-1.85,-1.38] | - | +78 [+67,+88] | needed |
| BR | binding | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BR | binding | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| BR | binding | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win24-31 | value | 60 | 93% [84,97] | 7% | -0.19 [-0.36,-0.07] | 0.98 | +7 [+2,+13] | partial |
| BR | binding | question | win24-31:attn | value | 60 | 93% [84,97] | 7% | -0.17 [-0.32,-0.06] | - | +7 [+2,+13] | partial |
| BR | binding | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | binding | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | after | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| BR | binding_off | both | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | both | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | both | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding_off | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | binding_off | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | binding_off | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | binding_off | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | binding_off | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | lookup | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | lookup | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| BR | lookup | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | lookup | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| BR | lookup | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | lookup | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BR | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| BR | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| BR | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | random | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| BR | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| BR | random | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | both | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| BR | random | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| BR | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| BR | random | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| BR | random | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| BR | random | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| BR | random | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | random | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| BR | random | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| BR | trailing | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| BR | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| BR | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| BR | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| BR | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | binding | after | all | absent | 60 | 98% [91,100] | 2% | -0.03 [-0.06,-0.00] | 0.98 | - | not_needed |
| RL | binding | after | all | value | 60 | 100% [94,100] | 0% | -0.02 [-0.05,-0.00] | 0.95 | - | not_needed |
| RL | binding | both | all | absent | 60 | 93% [84,97] | 7% | -0.22 [-0.33,-0.13] | 0.99 | +7 [+2,+13] | partial |
| RL | binding | both | all | value | 60 | 93% [84,97] | 7% | -0.20 [-0.29,-0.12] | 0.98 | +7 [+2,+13] | partial |
| RL | binding | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | binding | question | all | value | 60 | 100% [94,100] | 0% | -0.05 [-0.09,-0.03] | 0.98 | - | not_needed |
| RL | binding_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | binding_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | binding_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | binding_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | binding_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | binding_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | after | all | absent | 60 | 3% [1,11] | 50% | -3.08 [-3.38,-2.80] | 0.98 | +97 [+92,+100] | needed |
| RL | lookup | after | all | value | 60 | 5% [2,14] | 40% | -2.97 [-3.26,-2.69] | 0.94 | +95 [+88,+100] | needed |
| RL | lookup | both | all | absent | 60 | 8% [4,18] | 62% | -3.65 [-4.02,-3.29] | 0.99 | +92 [+85,+98] | needed |
| RL | lookup | both | all | value | 60 | 8% [4,18] | 57% | -3.60 [-3.99,-3.21] | 0.97 | +92 [+85,+98] | needed |
| RL | lookup | both | attn | value | 60 | 7% [3,16] | 65% | -3.66 [-4.05,-3.28] | - | +93 [+87,+98] | needed |
| RL | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | lookup | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | both | win40-47 | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.01] | 0.97 | - | not_needed |
| RL | lookup | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.01] | - | - | not_needed |
| RL | lookup | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | both | win48-55 | value | 60 | 85% [74,92] | 15% | -0.33 [-0.46,-0.21] | 0.98 | +15 [+7,+25] | partial |
| RL | lookup | both | win48-55:attn | value | 60 | 87% [76,93] | 13% | -0.33 [-0.46,-0.21] | - | +13 [+5,+23] | partial |
| RL | lookup | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | both | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | all | value | 60 | 7% [3,16] | 67% | -3.29 [-3.66,-2.93] | 0.98 | +93 [+87,+98] | needed |
| RL | lookup | final | attn | value | 60 | 8% [4,18] | 68% | -3.07 [-3.43,-2.72] | - | +92 [+83,+98] | needed |
| RL | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | final | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win48-55 | value | 60 | 98% [91,100] | 2% | -0.07 [-0.11,-0.04] | 0.99 | - | not_needed |
| RL | lookup | final | win48-55:attn | value | 60 | 98% [91,100] | 2% | -0.07 [-0.12,-0.04] | - | - | not_needed |
| RL | lookup | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | - | - | not_needed |
| RL | lookup | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup | question | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RL | lookup | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RL | lookup | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| RL | lookup | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| RL | lookup | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup | question | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | not_needed |
| RL | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | lookup_off | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | lookup_off | both | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | both | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | both | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | lookup_off | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | lookup_off | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RL | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | lookup_off | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | lookup_off | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.95 | - | not_needed |
| RL | lookup_off | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RL | lookup_off | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RL | lookup_off | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| RL | lookup_off | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| RL | lookup_off | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RL | lookup_off | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | lookup_off | question | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | lookup_off | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RL | lookup_off | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | not_needed |
| RL | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | both | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | random | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win48-55 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RL | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | random | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | random | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RL | random | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RL | random | question | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RL | random | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | random | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RL | random | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RL | trailing | after | all | absent | 60 | 90% [80,95] | 10% | -0.24 [-0.36,-0.14] | 0.99 | - | partial |
| RL | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | not_needed |
| RL | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RL | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RL | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | binding | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.98 | - | not_needed |
| RR | binding | after | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.95 | - | not_needed |
| RR | binding | both | all | absent | 60 | 97% [89,99] | 3% | -0.09 [-0.15,-0.05] | 0.99 | +3 [+0,+8] | partial |
| RR | binding | both | all | value | 60 | 97% [89,99] | 3% | -0.08 [-0.14,-0.04] | 0.98 | +3 [+0,+8] | partial |
| RR | binding | final | all | value | 60 | 100% [94,100] | 0% | -0.01 [-0.02,-0.00] | 0.99 | - | not_needed |
| RR | binding | question | all | value | 60 | 100% [94,100] | 0% | -0.06 [-0.10,-0.03] | 0.98 | - | not_needed |
| RR | binding_off | after | all | absent | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | binding_off | after | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| RR | binding_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | binding_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | binding_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | binding_off | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RR | lookup | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | both | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup | final | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | question | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| RR | lookup | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| RR | lookup | question | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup | question | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | lookup_off | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.94 | - | not_needed |
| RR | lookup_off | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win00-07 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | both | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup_off | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | lookup_off | final | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | lookup_off | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | lookup_off | final | win56-63 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | lookup_off | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | lookup_off | question | all | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | win24-31 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.95 | - | not_needed |
| RR | lookup_off | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.95 | - | not_needed |
| RR | lookup_off | question | win32-39 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | lookup_off | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | lookup_off | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | lookup_off | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | lookup_off | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | after | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.94 | - | not_needed |
| RR | random | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RR | random | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | random | both | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | both | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | both | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | both | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | both | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | both | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | random | final | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | win00-07:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win08-15 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | random | final | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | win16-23 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | win16-23:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | win16-23:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | final | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | final | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | random | final | win32-39:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | random | final | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win40-47 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | - | - | not_needed |
| RR | random | final | win40-47:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | final | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | random | final | win56-63:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | final | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 1.00 | - | not_needed |
| RR | random | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win00-07 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win00-07:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win00-07:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win08-15 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win08-15:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win08-15:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win16-23 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | win16-23:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win16-23:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | win24-31 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | random | question | win24-31:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win24-31:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.96 | - | not_needed |
| RR | random | question | win32-39 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | win32-39:attn | value | 60 | 100% [94,100] | 0% | +0.00 [+0.00,+0.00] | - | - | not_needed |
| RR | random | question | win32-39:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.97 | - | not_needed |
| RR | random | question | win40-47 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win40-47:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win40-47:gdn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win48-55 | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win48-55:attn | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win48-55:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.98 | - | not_needed |
| RR | random | question | win56-63 | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | random | question | win56-63:attn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | - | - | not_needed |
| RR | random | question | win56-63:gdn | value | 60 | 100% [94,100] | 0% | +0.00 [-0.00,+0.00] | 0.99 | - | not_needed |
| RR | trailing | after | all | absent | 60 | 100% [94,100] | 0% | -0.01 [-0.01,-0.00] | 0.99 | - | not_needed |
| RR | trailing | after | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.01,-0.00] | 0.95 | - | not_needed |
| RR | trailing | both | all | absent | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 1.00 | - | not_needed |
| RR | trailing | both | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.98 | - | not_needed |
| RR | trailing | final | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.99 | - | not_needed |
| RR | trailing | question | all | value | 60 | 100% [94,100] | 0% | -0.00 [-0.00,-0.00] | 0.97 | - | not_needed |
