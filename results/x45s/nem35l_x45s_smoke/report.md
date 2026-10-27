# 45s smoke: nem35l_x45s_smoke (PASS)

- kernel revision: ok
- kernel vs torch NLL: ok
- lens map at the layer: ok
- main: scenes: ok
- clean: scenes: ok
- main: no-op and write: ok
- clean: no-op and write: ok

Kernel: loaded ['28017f36635a6b94d911333812beeed5dd901ac0'], expected 28017f36635a6b94d911333812beeed5dd901ac0; NLL kernels 2.6999 vs torch 2.6995 (diff 0.00037), top-1 agreement 0.9696.

## main (cf)

Scenes made {'chat': 516} of 600; dropped {'chat: the bridge is not one token at one position in org and alt': 84}; one-token answers per reader {'PP': 516, 'PM': 516} (need 150).
First 8 scenes x 2 readers: no-op exact 16/16 (max |dlogit| 0.0); write max rel 0.00e+00 (tol 0.01); unedited right 13, S right 13, whole change switches 4 (2 where S reads its answer); alone vs batch: max |dlogit| 0.59375, same top 15/16; lens top 10 among the domain's items: org bridge 8/8, alt 8/8.

## clean (fresh)

Scenes made {'chat': 559} of 600; dropped {'chat: the bridge is not one token at one position in org and alt': 41}; one-token answers per reader {'PP': 559, 'PM': 559} (need 150).
First 8 scenes x 2 readers: no-op exact 16/16 (max |dlogit| 0.0); write max rel 0.00e+00 (tol 0.01); unedited right 14, S right 10, whole change switches 4 (3 where S reads its answer); alone vs batch: max |dlogit| 1.203125, same top 16/16; lens top 10 among the domain's items: org bridge 8/8, alt 8/8.

