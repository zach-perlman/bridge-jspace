#!/bin/bash
# matched-energy (amendment 70) reads of finished note 43/46/48 runs, from a scratch root (repo results untouched)
set -u
S=/workspace/scratch/me_read; B=/workspace/bridge-jspace; PY=$B/.venv/bin/python
mkdir -p $S/root/results/ablate_v2 $S/out
cd $S/root
[ -e data ] || ln -s $B/data data
rm -rf scripts; cp -r $B/scripts scripts
[ -e src ] || ln -s $B/src src
for d in $B/results/*; do n=$(basename $d); [ "$n" = ablate_v2 ] && continue; [ -e results/$n ] || ln -s $d results/$n; done
for d in $B/results/ablate_v2/*; do n=$(basename $d); [ "$n" = nn_ko_read ] && continue; [ -e results/ablate_v2/$n ] || ln -s $d results/ablate_v2/$n; done
mkdir -p results/ablate_v2/nn_ko_read
for P in qwen35_9b_ "" nem35l_; do
  for pair in "n43 jsuite_v4p4002_test_chat" "n48 jsuite_v4p4003_test_chat" "n46 jsuite_v5al_test_chat"; do
    set -- $pair; r=${P}${2}_ko37_cand2_v1
    [ -f results/ablate_v2/$r/summary.json ] || continue
    $PY scripts/nn_ko41_read.py "$P" --set $2 --run-a $r --run-n37 $r --matched-energy > $S/out/$1_${P:-27b_}.txt 2>&1
    echo "== $1 ${P:-27b_}"; grep -i "matched energy\|rule e\|rule l\|interpol" $S/out/$1_${P:-27b_}.txt | cut -c1-330
  done
done
