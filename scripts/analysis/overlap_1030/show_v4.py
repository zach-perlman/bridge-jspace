import json
d = json.load(open("/tmp/ana_v4.json"))
F = ["n_bridges", "n_MM", "n_MP", "gap_paper10", "gap_paper10_ci", "gap_paper10_rot", "lossMM_paper10", "lossMP_paper10", "keepA_rescue",
     "keepA_rescue_ci", "gap_paper10_keepA", "onlyA_net_share", "onlyA_net_share_ci", "onlyA_gap_share", "onlyA_gap_share_ci",
     "S1_onlyA_minus_onlyRperp", "S1_ci", "onlyRperp_net_share", "D1_K30", "D1_K30_ci", "D1_K100"]
short = lambda k: k.replace("gap_paper10", "g").replace("_net_share", "_ns").replace("_gap_share", "_gs").replace("S1_onlyA_minus_onlyRperp", "S1")
def line(m):
    return " ".join(f"{short(k)}={m.get(k)}" for k in F if k in m)
for P, R in d.items():
    print("=====", P, "mid", R["mid_layer"], "bridges gated", R["n_bridges_gated"], "with overlap", R["n_bridges_with_overlap"])
    print(" overlap by relation", R["overlap_by_relation"])
    for g in ("all", "with_concept_token", "no_concept_token"):
        print(" ", g, line(R[g]))
    for s in ("excess_A", "excess_A_bandmean", "excess_own", "raw_A"):
        x = R[s]
        print(" ", s, "cut", x["cut"], "low rel", x["low_relations"], "high rel", x["high_relations"])
        for h in ("low", "high"):
            print("    ", h, line(x[h]))
    for t, v in R["tertiles_excess_A"].items():
        print("  ", t, v["relations"], line(v))
    for h, v in R["within_relation_split"].items():
        print("   within", h, line(v))
    for rel, v in R["relation"].items():
        print("   rel", rel, line(v))
