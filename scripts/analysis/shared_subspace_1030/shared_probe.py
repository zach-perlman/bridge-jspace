"""Post hoc, CPU-only, descriptive: what does note 52's keepShared subspace contain?

Rebuilds note 44's capital / country spans and note 52's Shared (and note 52b's SharedNoLit) exactly as
scripts/ablate_v2.py does (LensDictionary atoms = normalize((W_U[letters] * gain) @ J_l); Cap = QR of every capital
form's first-token atoms; Cty = the same for kn2's 49 countries (count-matched subsample = all of them, so identical
for every item); Shared = bisectors of principal-vector pairs with cosine >= 0.9; SharedNoLit = Shared projected off
the literal shared rows), then reads it out against the whole letter-token dictionary.

Usage (on the box, from /tmp): BJ_TARGET=<target> HF_HOME=/workspace/hf_cache CUDA_VISIBLE_DEVICES="" nice -n 19 \
    /workspace/bridge-jspace/.venv/bin/python -I shared_probe.py <run_dir> <band_lo> <band_hi> <layerA> <layerB> <out.json>
Reads the repo only (never writes there).
"""

import hashlib
import json
import os
import random
import re
import sys
import time
import zlib

sys.path.insert(0, "/workspace/bridge-jspace/src")
sys.path.insert(0, "/workspace/bridge-jspace")
import torch  # noqa: E402

torch.set_num_threads(int(os.environ.get("NTHREADS", "12")))
from bridge_jspace import pins, tokens  # noqa: E402
from huggingface_hub import hf_hub_download, snapshot_download  # noqa: E402
from safetensors import safe_open  # noqa: E402

RUN_DIR, LO, HI, LA_A, LA_B, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
SHARED_COS, PERP_TOL = 0.9, 1e-3  # ablate_v2's constants
_HAS_LETTER = re.compile(r"[^\W\d_]")
t0 = time.time()


def log(*a):
    print(f"[{time.time() - t0:7.1f}s]", *a, flush=True)


# ---------------- model pieces (lm_head, final norm gain, tokenizer, letters) ----------------
path = snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True,
                         ignore_patterns=pins.TARGETS[pins.TARGET].get("snapshot_ignore"))
wm = json.load(open(os.path.join(path, "model.safetensors.index.json")))["weight_map"]
norm_key = [k for k in wm if k in ("model.language_model.norm.weight", "backbone.norm_f.weight", "model.norm.weight")]
assert len(norm_key) == 1, norm_key


def tensor(key):
    with safe_open(os.path.join(path, wm[key]), framework="pt") as f:
        return f.get_tensor(key)


W = tensor("lm_head.weight")  # [vocab, d] bf16
nw = tensor(norm_key[0]).float()
gain = 1.0 + nw if pins.TARGETS[pins.TARGET]["norm_gain"] == "one_plus_weight" else nw
tok = tokens.load_tokenizer()
vocab = W.shape[0]
decoded = tok.batch_decode([[i] for i in range(vocab)])
special = frozenset(tok.all_special_ids) | frozenset(int(i) for i in tok.added_tokens_decoder)
letters = torch.tensor([i for i, s in enumerate(decoded) if i not in special and _HAS_LETTER.search(s)])
row_of = torch.full((vocab,), -1, dtype=torch.long)
row_of[letters] = torch.arange(letters.numel())
wg = W[letters].float() * gain  # as ablate_v2: model.hf.lm_head.weight[letters].float() * model.norm_gain()
dec = [decoded[int(i)] for i in letters]
N, d = wg.shape
log(pins.TARGET, "vocab", vocab, "letters", N, "d", d, "norm", norm_key[0])

# ---------------- lens (frozen J++), sha256-checked ----------------
src = pins.LENS_SOURCES[pins.FROZEN_LENS]
lens_path = (pins.REPO_ROOT / src[1]) if src[0] == "local" else hf_hub_download(src[0], src[1], revision=src[2], local_files_only=True)
h = hashlib.sha256()
with open(lens_path, "rb") as fh:
    for blk in iter(lambda: fh.read(1 << 24), b""):
        h.update(blk)
sha = h.hexdigest()
assert sha == pins.FROZEN_LENS_SHA256, (sha, pins.FROZEN_LENS_SHA256)
blob = torch.load(lens_path, map_location="cpu", weights_only=True, mmap=True)
log("lens", pins.FROZEN_LENS, "sha256 ok", sha[:12])


def J(la):
    return blob["J"][la].float()


# ---------------- note 44's rows, recomputed and checked against the run's n44_spans.json ----------------
from scripts import jsuite_v5key as K5  # noqa: E402
from scripts import tasks_v2 as T  # noqa: E402

caps = sorted(set(K5.CAPITAL.values()) | {x for v in K5.CAPITAL_ALIASES.values() for x in v})
ctys = sorted({v for it in T.load("jsuite_v5kn2_test_chat") if it["word"] == "MM" for v in it["answer_vocab"]})


def every_form(vals):
    ids = {tok(f, add_special_tokens=False).input_ids[0] for v in vals for f in (v, v.lower(), " " + v, " " + v.lower())}
    rr = row_of[torch.tensor(sorted(ids))]
    return rr[rr >= 0].unique()


cap_rows, cty_rows = every_form(caps), every_form(ctys)
spans = json.load(open(os.path.join(RUN_DIR, "n44_spans.json")))
assert spans["capitals"] == caps and spans["countries"] == ctys
assert cap_rows.tolist() == spans["cap_rows"] and cty_rows.tolist() == spans["cty_rows"], "rows differ from the run's"
lit = sorted(set(cap_rows.tolist()) & set(cty_rows.tolist()))
assert lit == spans["shared_rows"]
rows44 = [json.loads(l_) for l_ in open(os.path.join(RUN_DIR, "n44_rows.jsonl"))]
assert all(r["cty_rows"] == cty_rows.tolist() for r in rows44), "Cty differs by item"
log(f"caps {len(caps)} -> {cap_rows.numel()} rows; ctys {len(ctys)} -> {cty_rows.numel()} rows; literal {len(lit)}:",
    [dec[i] for i in lit])

keeplog = {}
kp = os.path.join(RUN_DIR, "keeplog.jsonl")
for l_ in open(kp):
    r = json.loads(l_)
    if r.get("condition") == "paper10":
        keeplog[r["id"]] = r
logged_rank = next(iter(keeplog.values())).get("rank", {})
log("logged band-average ranks:", logged_rank)


# ---------------- ablate_v2's span machinery (verbatim logic, CPU) ----------------
def tf32(x):
    """Round fp32 to TF32 (10-bit mantissa), round-to-nearest, as an emulation of allow_tf32 matmul inputs."""
    i = x.contiguous().view(torch.int32)
    i = (i + 0x1000) & ~0x1FFF
    return i.view(torch.float32)


class Dic:
    def __init__(self, la, emulate_tf32):
        self.Jm = J(la)
        self.e = emulate_tf32
        self.Jt = tf32(self.Jm) if emulate_tf32 else self.Jm

    def atoms(self, idx):
        w = wg[idx]
        a = (tf32(w) if self.e else w) @ self.Jt
        return a / a.norm(dim=-1, keepdim=True)


def qr_span(dic, rr):
    return torch.linalg.qr(dic.atoms(rr).double().T)[0]


def perp_basis(Q, V):
    k = Q.shape[1]
    q, r = torch.linalg.qr(torch.cat([Q.double(), V.double().T], 1))
    keep = r.diagonal()[k:].abs() >= PERP_TOL
    return q[:, k:][:, keep].contiguous()


def shared_basis(Qa, Qb):
    U, S_, Vh = torch.linalg.svd(Qa.T.double() @ Qb.double(), full_matrices=False)
    sel = S_ >= SHARED_COS
    B = Qa.double() @ U[:, sel] + Qb.double() @ Vh.T[:, sel]
    return (B / B.norm(dim=0, keepdim=True)).contiguous(), S_


def build(dic):
    Qc, Qt = qr_span(dic, cap_rows), qr_span(dic, cty_rows)
    B, S_ = shared_basis(Qc, Qt)
    ql = qr_span(dic, torch.tensor(lit))
    B2 = perp_basis(ql, B.T)
    return Qc, Qt, B, B2, S_


# rank check over the whole band, fp32 and TF32-emulated
rank_check = {}
for la in range(LO, HI + 1):
    out = {}
    for mode in (False, True):
        _, _, B, B2, S_ = build(Dic(la, mode))
        near = int(((S_ > 0.88) & (S_ < 0.92)).sum())
        out["tf32" if mode else "fp32"] = {"shared": B.shape[1], "nolit": B2.shape[1], "n_cos_0.88_0.92": near,
                                           "cos_around_cut": [round(float(x), 4) for x in S_[max(0, B.shape[1] - 3): B.shape[1] + 3]]}
    rank_check[la] = out
    log("L", la, out)
for mode in ("fp32", "tf32"):
    rank_check["mean_" + mode] = {k: sum(rank_check[la][mode][k] for la in range(LO, HI + 1)) / (HI - LO + 1) for k in ("shared", "nolit")}
log("band means", rank_check["mean_fp32"], rank_check["mean_tf32"], "logged", logged_rank)
match = {m: abs(rank_check["mean_" + m]["shared"] - logged_rank.get("Shared", -1)) < 1e-6 for m in ("fp32", "tf32")}
use_tf32 = match["tf32"] or not match["fp32"]  # the runner's numerics (TF32) unless only plain fp32 reproduces the logged rank
rank_check["matches_logged"] = match
log("basis numerics:", "tf32-emulated" if use_tf32 else "fp32")

# ---------------- token categories ----------------
CAPS_SET = {c.lower() for c in caps} | {c.split()[0].lower() for c in caps}
CTYS_SET = {c.lower() for c in ctys} | {c.split()[0].lower() for c in ctys}
OTHER_COUNTRIES = """afghanistan albania algeria andorra angola armenia azerbaijan bahamas bahrain bangladesh barbados belarus belize
benin bhutan bolivia bosnia botswana brunei bulgaria burkina burundi cameroon chad comoros congo croatia cuba cyprus
djibouti dominica ecuador eritrea estonia eswatini ethiopia fiji gabon gambia georgia ghana grenada guatemala guinea
guyana haiti honduras iceland iran iraq kazakhstan kiribati kosovo kuwait kyrgyzstan laos latvia lebanon lesotho liberia
libya liechtenstein lithuania luxembourg madagascar malawi maldives mali malta mauritania mauritius moldova monaco
mongolia montenegro mozambique myanmar burma namibia nauru nepal nicaragua niger oman pakistan palau panama paraguay
philippines qatar romania rwanda samoa senegal serbia seychelles singapore slovakia slovenia somalia sudan suriname
switzerland syria tajikistan togo tonga tunisia turkmenistan tuvalu uganda ukraine uruguay uzbekistan vanuatu yemen
zambia zimbabwe scotland wales britain korea zealand emirates arabia salvador lanka""".split()
OTHER_CAPITALS = """kabul tirana algiers luanda yerevan baku manama dhaka minsk brussels sofia ottawa zagreb havana nicosia quito
tallinn addis ababa tbilisi accra conakry tehran baghdad reykjavik nairobi pyongyang kuwait bishkek vientiane riga beirut
monrovia tripoli vilnius antananarivo lilongwe bamako valletta nouakchott chisinau ulaanbaatar podgorica maputo windhoek
kathmandu wellington managua niamey muscat islamabad panama asuncion manila doha bucharest kigali dakar belgrade freetown
bratislava ljubljana mogadishu khartoum paramaribo bern damascus dushanbe lome tunis ashgabat kampala kyiv kiev montevideo
tashkent caracas sanaa lusaka harare canberra luxembourg abu dhabi riyadh colombo""".split()
OTHER_CITIES = """sydney melbourne toronto montreal vancouver shanghai mumbai bombay chicago houston boston seattle miami dallas atlanta
detroit denver phoenix philadelphia barcelona milan naples venice florence munich hamburg frankfurt cologne marseille lyon
nice manchester liverpool birmingham glasgow edinburgh osaka kyoto yokohama istanbul dubai karachi lahore kolkata calcutta
chennai bangalore hyderabad hongkong shenzhen guangzhou wuhan chengdu busan rio janeiro paulo salvador cordoba medellin
cali guadalajara monterrey alexandria casablanca marrakech lagos johannesburg durban cape mombasa zurich geneva rotterdam
antwerp porto seville valencia krakow gdansk orlando vegas austin portland oakland berkeley brooklyn manhattan hollywood
quebec calgary auckland perth brisbane adelaide jeddah mecca tel aviv haifa gothenburg malmo bergen turku salzburg
saigon chiang""".split()
DEMONYMS = """american americans canadian mexican brazilian argentine argentinian chilean peruvian colombian venezuelan cuban
jamaican british english scottish welsh irish french german germans dutch belgian swiss austrian italian italians spanish
spaniard portuguese greek turkish russian russians polish czech hungarian swedish norwegian danish finnish icelandic
ukrainian romanian bulgarian serbian croatian bosnian albanian slovak slovenian estonian latvian lithuanian belarusian
chinese japanese korean vietnamese thai cambodian malaysian indonesian filipino indian pakistani bangladeshi nepali
afghan iranian persian iraqi syrian lebanese israeli jordanian saudi egyptian moroccan algerian tunisian libyan nigerian
kenyan ethiopian ghanaian tanzanian ugandan somali sudanese african african european asian australian zealander taiwanese
mongolian tibetan arab arabic hispanic latino""".split()
US_STATES = """alabama alaska arizona arkansas california colorado connecticut delaware florida georgia hawaii idaho illinois
indiana iowa kansas kentucky louisiana maine maryland massachusetts michigan minnesota mississippi missouri montana nebraska
nevada hampshire jersey york carolina dakota ohio oklahoma oregon pennsylvania rhode tennessee texas utah vermont virginia
washington wisconsin wyoming""".split()
GEO_TERMS = """africa europe asia america americas oceania antarctica arctic atlantic pacific mediterranean caribbean balkans
scandinavia middle east eastern western northern southern country countries nation nations capital capitals city cities
continent region kingdom republic empire province state states territory island islands""".split()
FUNCTION = """the a an of to in on at by for with from and or but not no is are was were be been being am it its this that these
those he she they them his her their our we you your i me my mine us there here what which who whom whose when where why how
all any both each few more most other some such only own same so than too very can will just should now as if then into
over under again further once about above below up down out off do does did doing have has had having would could may
might must shall also yet nor per via upon""".split()

geo_lists = [("other_country", set(OTHER_COUNTRIES) - CTYS_SET), ("other_capital", set(OTHER_CAPITALS) - CAPS_SET),
             ("other_city", set(OTHER_CITIES) - CAPS_SET - CTYS_SET), ("demonym", set(DEMONYMS)),
             ("us_state", set(US_STATES) - CAPS_SET - CTYS_SET), ("geo_term", set(GEO_TERMS)), ("function_word", set(FUNCTION))]
cap_set, cty_set = set(cap_rows.tolist()), set(cty_rows.tolist())
cat = []
for i, s in enumerate(dec):
    w = s.strip()
    k = w.lower()
    if i in cap_set and i in cty_set:
        c = "vocab_literal_both"
    elif i in cap_set:
        c = "vocab_capital_word" if k in CAPS_SET else "vocab_capital_fragment"
    elif i in cty_set:
        c = "vocab_country_word" if k in CTYS_SET else "vocab_country_fragment"
    elif k in CAPS_SET:
        c = "capital_word_other_form"  # a capital's word in a form whose first token is not a vocab row (e.g. mid-word)
    elif k in CTYS_SET:
        c = "country_word_other_form"
    else:
        c = None
        for name, st in geo_lists:
            if k in st and len(k) >= 3 or (name == "function_word" and k in st):
                c = name
                break
        if c is None:
            c = "other_capitalised" if (w[:1].isupper() and w.isalpha() and len(w) >= 3) else (
                "other_word" if (w.isalpha() and len(w) >= 3) else "other_short_or_mixed")
    cat.append(c)
CATS = sorted(set(cat))
cat_idx = {c: torch.tensor([i for i, x in enumerate(cat) if x == c]) for c in CATS}
log({c: int(v.numel()) for c, v in cat_idx.items()})

# ---------------- items: gold capitals / countries (MC0), pools ----------------
items = {it["id"]: it for it in T.load("jsuite_v5kn2c_test_chat")}
mc0 = [r for r in rows44 if r["family"] == "MC0"]
seen, mc0u = set(), []
for r in mc0:
    if r["id"] not in seen:
        seen.add(r["id"])
        mc0u.append(r)
ctrl_items = mc0u[:10]
log("MC0 rows", len(mc0u), "control items", [r["id"] for r in ctrl_items])


def form_rows(v):
    ids = {tok(f, add_special_tokens=False).input_ids[0] for f in (v, v.lower(), " " + v, " " + v.lower())}
    rr = row_of[torch.tensor(sorted(ids))]
    return sorted(set(rr[rr >= 0].tolist()))


def gram_rand_in(Q, r, seed):
    g = torch.Generator().manual_seed(seed)
    M = torch.randn(Q.shape[1], r, generator=g, dtype=torch.float64)
    return Q @ torch.linalg.qr(M)[0]


results = {"target": pins.TARGET, "model_repo": pins.MODEL_REPO, "revision": pins.MODEL_REVISION, "lens_sha256": sha,
           "run_dir": RUN_DIR, "band": [LO, HI], "n_letters": N, "d": d, "caps": caps, "ctys": ctys,
           "n_cap_rows": int(cap_rows.numel()), "n_cty_rows": int(cty_rows.numel()),
           "literal_rows": [dec[i] for i in lit], "rank_check": rank_check, "logged_rank": logged_rank,
           "basis_numerics": "tf32-emulated" if use_tf32 else "fp32", "cat_counts": {c: int(v.numel()) for c, v in cat_idx.items()},
           "ctrl_items": [r["id"] for r in ctrl_items], "layers": {}}


def cat_table(share):
    out = {}
    for c in CATS:
        s = share[cat_idx[c]]
        out[c] = {"n": int(s.numel()), "mean": float(s.mean()), "median": float(s.median()),
                  "frac_of_total_energy": float(s.sum() / share.sum())}
    return out


def top_tokens(share, k=60):
    v, ix = share.topk(k)
    return [[dec[int(i)], cat[int(i)], round(float(x), 4)] for x, i in zip(v, ix)]


for la in (LA_A, LA_B):
    dic = Dic(la, use_tf32)
    Qc, Qt, B, B2, S_ = build(dic)
    r, r2 = B.shape[1], B2.shape[1]
    # controls: (a) equal-rank random letter rows = the first r rows of the item's Rcap pool (ablate_v2's random-keep draw);
    # (b) energy-matched RShared = the first k_RShared rows (k from the run's keeplog, band level); (c) random r-dim subspace
    # of span(Cap) and of span(Cty)
    ctrl = {"R_eq": [], "R_eq_nolit": [], "R_energy": [], "Rin_Cap": [], "Rin_Cty": []}
    k_energy = []
    for j, it in enumerate(ctrl_items):
        pool = torch.tensor(it["rcap_pool"])
        ctrl["R_eq"].append(qr_span(dic, pool[:r]))
        ctrl["R_eq_nolit"].append(qr_span(dic, pool[:r2]))
        kl = keeplog.get(it["id"], {}).get("k52b", {}).get("k_RShared")
        if kl:
            k_energy.append(kl)
            ctrl["R_energy"].append(qr_span(dic, pool[:kl]))
        ctrl["Rin_Cap"].append(gram_rand_in(Qc, r, 1000 + j))
        ctrl["Rin_Cty"].append(gram_rand_in(Qt, r, 2000 + j))
    ctrl = {k: v for k, v in ctrl.items() if v}
    blocks = [("Shared", B), ("SharedNoLit", B2)] + [(f"{k}#{j}", m) for k, v in ctrl.items() for j, m in enumerate(v)]
    Bcat = torch.cat([m.float() for _, m in blocks], 1)
    offs, o = {}, 0
    for name, m in blocks:
        offs[name] = (o, o + m.shape[1])
        o += m.shape[1]
    # J++ readout: every letter atom (fp32, unit) projected on every block; also the Shared coordinates for the axes
    shares = torch.zeros(len(blocks), N)
    coordS = torch.zeros(N, r)
    Jm = dic.Jm
    for s in range(0, N, 16384):
        a = wg[s: s + 16384] @ Jm
        a = a / a.norm(dim=-1, keepdim=True)
        P = a @ Bcat
        for bi, (name, _) in enumerate(blocks):
            lo_, hi_ = offs[name]
            shares[bi, s: s + 16384] = P[:, lo_:hi_].pow(2).sum(1)
        coordS[s: s + 16384] = P[:, offs["Shared"][0]: offs["Shared"][1]]
    # logit-lens readout: unit unembedding rows (gain folded) on the same blocks; plus the logit-lens analogue of Shared
    U = wg / wg.norm(dim=-1, keepdim=True)
    BU, SU = shared_basis(torch.linalg.qr(U[cap_rows].double().T)[0], torch.linalg.qr(U[cty_rows].double().T)[0])
    BU2 = perp_basis(torch.linalg.qr(U[torch.tensor(lit)].double().T)[0], BU.T)
    PU = U @ torch.cat([B.float(), B2.float(), BU.float(), BU2.float()] + [m.float() for m in ctrl["R_eq"]], 1)
    sU = {"Shared": PU[:, :r].pow(2).sum(1), "SharedNoLit": PU[:, r: r + r2].pow(2).sum(1),
          "SharedU": PU[:, r + r2: r + r2 + BU.shape[1]].pow(2).sum(1),
          "SharedU_NoLit": PU[:, r + r2 + BU.shape[1]: r + r2 + BU.shape[1] + BU2.shape[1]].pow(2).sum(1)}
    oo = r + r2 + BU.shape[1] + BU2.shape[1]
    sU["R_eq_mean"] = torch.stack([PU[:, oo + j * r: oo + (j + 1) * r].pow(2).sum(1) for j in range(len(ctrl["R_eq"]))]).mean(0)
    # principal axes of the dictionary's projection on Shared
    _, sv, Vh = torch.linalg.svd(coordS, full_matrices=False)
    axes = []
    for ax in range(6):
        c = coordS @ Vh[ax]
        axes.append({"sv_frac": float(sv[ax] ** 2 / (sv ** 2).sum()),
                     "plus": [[dec[int(i)], round(float(c[i]), 3)] for i in c.topk(15).indices],
                     "minus": [[dec[int(i)], round(float(c[i]), 3)] for i in (-c).topk(15).indices]})
    # Shared's own columns ordered as the runner's (by principal cosine): nearest tokens per column
    cols = []
    for ci in range(r):
        c = coordS[:, ci]
        cols.append({"cos": round(float(S_[ci]), 4), "plus": [dec[int(i)] for i in c.topk(6).indices],
                     "minus": [dec[int(i)] for i in (-c).topk(4).indices]})
    sh = {name: shares[bi] for bi, (name, _) in enumerate(blocks)}
    mean_ctrl = {k: torch.stack([sh[f"{k}#{j}"] for j in range(len(v))]).mean(0) for k, v in ctrl.items()}
    sd_ctrl_cats = {k: {c: float(torch.tensor([sh[f"{k}#{j}"][cat_idx[c]].mean() for j in range(len(v))]).std())
                        for c in CATS} for k, v in ctrl.items()}
    # gold overlap per MC0 item
    gold = []
    for it in mc0u:
        g = items[it["id"]]
        capv = [g["answer"]] + list(g.get("answer_aliases", [])) + K5.CAPITAL_ALIASES.get(g["answer"], [])
        ctyv = g["memory_answer"]
        crow = sorted({x for v in capv for x in form_rows(v)})
        trow = form_rows(ctyv)
        others = [c for c in g["answer_vocab"] if c != g["answer"]]
        orow = sorted({x for v in others for x in form_rows(v)})
        pool = torch.tensor(it["rcap_pool"])
        Rq = qr_span(dic, pool[:r])
        Rq2 = qr_span(dic, pool[:r2])
        RC = gram_rand_in(Qc, r, zlib.crc32(it["id"].encode()) % 100000)

        def sh_(rows, Q):
            if not rows:
                return None
            a = dic.atoms(torch.tensor(rows)).double()
            return float((a @ Q).pow(2).sum(1).mean())

        gold.append({"id": it["id"], "kind": it["kind"], "capital": g["answer"], "country": ctyv,
                     "cap_forms": [dec[x] for x in crow], "cty_forms": [dec[x] for x in trow],
                     "cap_in_Shared": sh_(crow, B), "cap_in_NoLit": sh_(crow, B2), "cap_in_Req": sh_(crow, Rq),
                     "cap_in_Req_nolit": sh_(crow, Rq2), "cap_in_RinCap": sh_(crow, RC),
                     "cty_in_Shared": sh_(trow, B), "cty_in_NoLit": sh_(trow, B2), "cty_in_Req": sh_(trow, Rq),
                     "cty_in_Req_nolit": sh_(trow, Rq2),
                     "distractor_caps_in_Shared": sh_(orow, B), "distractor_caps_in_NoLit": sh_(orow, B2)})
    # per-capital whole vocabulary: each capital's forms in Shared (is it uniform across capitals?)
    per_cap = {c: {"Shared": float(sum(sh["Shared"][x] for x in form_rows(c)) / max(1, len(form_rows(c)))),
                   "NoLit": float(sum(sh["SharedNoLit"][x] for x in form_rows(c)) / max(1, len(form_rows(c)))),
                   "forms": [dec[x] for x in form_rows(c)]} for c in caps}
    per_cty = {c: {"Shared": float(sum(sh["Shared"][x] for x in form_rows(c)) / max(1, len(form_rows(c)))),
                   "NoLit": float(sum(sh["SharedNoLit"][x] for x in form_rows(c)) / max(1, len(form_rows(c)))),
                   "forms": [dec[x] for x in form_rows(c)]} for c in ctys}
    # top tokens and categories of the top 200
    def top_comp(share, k=200):
        ix = share.topk(k).indices
        cc = {}
        for i in ix.tolist():
            cc[cat[i]] = cc.get(cat[i], 0) + 1
        return cc

    L = {"rank_shared": r, "rank_nolit": r2, "principal_cos_selected": [round(float(x), 4) for x in S_[:r]],
         "rank_SharedU_logitlens": BU.shape[1], "rank_SharedU_nolit": BU2.shape[1],
         "k_energy_RShared": k_energy,
         "overlap_Shared_SharedU": float((B.T @ BU).pow(2).sum() / max(1, min(r, BU.shape[1]))),
         "cats": {"Shared": cat_table(sh["Shared"]), "SharedNoLit": cat_table(sh["SharedNoLit"]),
                  **{k + "_mean": cat_table(v) for k, v in mean_ctrl.items()}},
         "cats_sd_over_draws": sd_ctrl_cats,
         "mean_share_all": {"Shared": float(sh["Shared"].mean()), "SharedNoLit": float(sh["SharedNoLit"].mean()),
                            **{k: float(v.mean()) for k, v in mean_ctrl.items()}},
         "top_Shared": top_tokens(sh["Shared"]), "top_SharedNoLit": top_tokens(sh["SharedNoLit"]),
         "top_R_eq_draw0": top_tokens(sh["R_eq#0"], 40),
         "top200_comp": {"Shared": top_comp(sh["Shared"]), "SharedNoLit": top_comp(sh["SharedNoLit"]),
                         "R_eq_draw0": top_comp(sh["R_eq#0"]), "Rin_Cap_draw0": top_comp(sh["Rin_Cap#0"])},
         "top_nonvocab_Shared": [t for t in top_tokens(sh["Shared"], 400) if not t[1].startswith("vocab_")][:40],
         "top_nonvocab_SharedNoLit": [t for t in top_tokens(sh["SharedNoLit"], 400) if not t[1].startswith("vocab_")][:40],
         "logit_lens": {"cats": {k: cat_table(v) for k, v in sU.items()}, "top": {k: top_tokens(v, 40) for k, v in sU.items()},
                        "mean_share_all": {k: float(v.mean()) for k, v in sU.items()}},
         "cat_top": {sub: {c: [[dec[int(i)], round(float(sh[sub][cat_idx[c]][j]), 3)] for j, i in
                               zip(sh[sub][cat_idx[c]].topk(min(10, cat_idx[c].numel())).indices.tolist(),
                                   cat_idx[c][sh[sub][cat_idx[c]].topk(min(10, cat_idx[c].numel())).indices].tolist())]
                           for c in CATS if c not in ("other_word", "other_short_or_mixed")} for sub in ("Shared", "SharedNoLit")},
         "logitlens_principal_cos_top20": [round(float(x), 4) for x in SU[:20]],
         "axes": axes, "shared_columns": cols, "gold": gold, "per_capital": per_cap, "per_country": per_cty}
    results["layers"][la] = L
    log("layer", la, "r", r, "r2", r2, "rU", BU.shape[1], "mean share Shared", L["mean_share_all"])
    log("top Shared:", [t[0] for t in L["top_Shared"][:40]])
    log("top nonvocab Shared:", [t[0] for t in L["top_nonvocab_Shared"][:30]])
    log("top nonvocab NoLit:", [t[0] for t in L["top_nonvocab_SharedNoLit"][:30]])

json.dump(results, open(OUT, "w"), indent=1)
log("wrote", OUT)
