"""exp19_fit_data: a phone-friendly page of per-layer lens ranks, jpp_chat64 against jpp_wiki64 (and the published J++).

    python3 scripts/exp19_fit_data/examples.py   (on the GPU box; writes examples/exp19_fit_data/index.html)

Reads the fit_v3 evals (chat64, wiki64) and fit_v2's eval for the published J++, and the J++ eval prompts. Every number
on the page is a rank from those CSVs; the page's pass@k is recomputed from them and checked against the analysis.
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RES = REPO / "results/exp19_fit_data"
EVAL_DIR = Path("/workspace/lensfit/jpp_lens/data/jlens/evaluations")
OUT = REPO / "examples/exp19_fit_data/index.html"
FAMILIES = ("multihop", "multilingual", "typo", "association", "poetry")
LENSES = {
    "c": ("jpp_chat64", RES / "fit_v3/eval_chat64/eval_ranks.csv"),
    "w": ("jpp_wiki64", RES / "fit_v3/eval_wiki64/eval_ranks.csv"),
    "p": ("Qwen3.6-27B_jpp_lens", RES / "fit_v2/eval_ranks.csv"),
}
N_LAYERS = 63


def load_ranks():
    ranks = defaultdict(dict)  # (family, item, intermediate) -> key -> [rank per layer]
    for key, (lens, path) in LENSES.items():
        with open(path) as f:
            for r in csv.DictReader(f):
                if r["lens"] != lens:
                    continue
                k = (r["eval"], r["item"], r["intermediate"])
                ranks[k].setdefault(key, [None] * N_LAYERS)[int(r["layer"])] = int(r["rank"])
    return ranks


def main():
    ranks = load_ranks()
    prompts = {}
    for fam in FAMILIES:
        for it in json.load(open(EVAL_DIR / f"lens-eval-{fam}.json"))["items"]:
            prompts[(fam, it["name"])] = it
    items = defaultdict(list)
    for (fam, name, inter), by in ranks.items():
        if "c" not in by or "w" not in by:
            continue
        for key, rs in by.items():
            assert None not in rs, (fam, name, inter, key)
        items[(fam, name)].append({"x": inter, **by})
    data = []
    for (fam, name), inters in sorted(items.items()):
        src = prompts[(fam, name)]
        order = {w: i for i, w in enumerate(src["intermediates"])}
        inters.sort(key=lambda x: order.get(x["x"], 99))
        data.append({"f": fam, "n": name, "q": src["prompt"], "t": src.get("target"), "I": inters})

    # the page's pass@10 must match the analysis (results/exp19_fit_data/fit_v3/analysis_*/summary.json)
    for key, want in (("c", 0.7161538461538461), ("w", 0.6676194537170147)):
        fams = []
        for fam in FAMILIES:
            sc = [sum(min(i[key]) <= 10 for i in d["I"]) / len(d["I"]) for d in data if d["f"] == fam]
            fams.append(sum(sc) / len(sc))
        got = sum(fams) / len(fams)
        assert abs(got - want) < 1e-9, (key, got, want)
    print(f"{len(data)} items; pass@10 matches the analysis", file=sys.stderr)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.replace("/*DATA*/null", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    OUT.write_text(html)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)", file=sys.stderr)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>exp19 · chat64 vs wiki64 per-layer ranks</title>
<style>
:root {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink2: #52514e; --muted: #898781;
  --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10); --band: #f0efec;
  --chat: #2a78d6; --wiki: #eb6834; --pub: #898781;
  --r1: #104281; --r10: #2a78d6; --r100: #6da7ec; --r1k: #b7d3f6; --rx: #eeede8;
  --good: #006300; --chip: #ffffff; --chip-on: #0b0b0b; --chip-on-ink: #fcfcfb;
}
@media (prefers-color-scheme: dark) {
  :root {
    color-scheme: dark;
    --page: #0d0d0d; --surface: #1a1a19; --ink: #f0efec; --ink2: #c3c2b7; --muted: #898781;
    --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10); --band: #262624;
    --chat: #3987e5; --wiki: #d95926; --pub: #898781;
    --r1: #b7d3f6; --r10: #5598e7; --r100: #256abf; --r1k: #184f95; --rx: #2c2c2a;
    --good: #0ca30c; --chip: #1a1a19; --chip-on: #f0efec; --chip-on-ink: #0d0d0d;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--page); color: var(--ink);
  font: 15px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
.wrap { max-width: 760px; margin: 0 auto; padding: 0 12px calc(84px + env(safe-area-inset-bottom)); }
h1 { font-size: 19px; line-height: 1.25; margin: 16px 0 4px; }
h2 { font-size: 16px; margin: 0; }
.sub { color: var(--ink2); font-size: 13.5px; margin: 0 0 10px; }
.tag { display: inline-block; font-size: 11px; font-weight: 600; letter-spacing: .03em; padding: 1px 6px;
  border-radius: 4px; border: 1px solid var(--border); color: var(--ink2); vertical-align: 2px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px; margin: 10px 0; }
.tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.tile .v { font-size: 22px; font-weight: 600; }
.tile .l { font-size: 12px; color: var(--ink2); }
.sw { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 5px; vertical-align: 0; }
.ln { display: inline-block; width: 16px; height: 3px; border-radius: 2px; margin-right: 5px; vertical-align: 3px; }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 12.5px; color: var(--ink2); }
details.how summary { cursor: pointer; font-size: 13.5px; color: var(--ink2); }
details.how p { font-size: 13.5px; color: var(--ink2); margin: 6px 0; }
.bar { position: sticky; top: 0; z-index: 5; background: var(--page); padding: 8px 0 6px; border-bottom: 1px solid var(--border); }
.row { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding: 2px 0; }
.row::-webkit-scrollbar { display: none; }
.row + .row { margin-top: 6px; }
.chip { flex: none; border: 1px solid var(--border); background: var(--chip); color: var(--ink); border-radius: 999px;
  padding: 7px 12px; font: inherit; font-size: 13.5px; min-height: 36px; cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--chip-on); color: var(--chip-on-ink); border-color: var(--chip-on); }
.chip .n { opacity: .65; margin-left: 4px; font-variant-numeric: tabular-nums; }
.count { font-size: 12.5px; color: var(--ink2); margin: 8px 2px 0; }
a.item { display: block; color: inherit; text-decoration: none; }
a.item:active .card { border-color: var(--axis); }
.ihead { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
.fam { font-size: 11.5px; color: var(--ink2); text-transform: uppercase; letter-spacing: .05em; }
.name { font-weight: 600; word-break: break-word; }
.prompt { font-size: 13.5px; color: var(--ink2); margin: 4px 0 8px; display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden; white-space: pre-wrap; }
.verdict { flex: none; font-size: 12px; font-weight: 600; white-space: nowrap; }
.inter { margin-top: 6px; }
.iw { font-size: 13px; display: flex; justify-content: space-between; gap: 8px; }
.iw b { font-weight: 600; }
.best { color: var(--ink2); font-variant-numeric: tabular-nums; white-space: nowrap; }
.strip { display: grid; grid-template-columns: 66px 1fr; white-space: nowrap; align-items: center; gap: 6px; margin-top: 3px; font-size: 11.5px; color: var(--ink2); }
.strip svg { width: 100%; height: 10px; display: block; }
.axisnote { display: grid; grid-template-columns: 66px 1fr; gap: 6px; font-size: 10.5px; color: var(--muted); }
.axisnote span { display: flex; justify-content: space-between; }
/* detail */
.back { display: inline-flex; align-items: center; gap: 4px; margin: 12px 0 0; padding: 8px 12px 8px 4px; min-height: 40px;
  color: var(--ink); text-decoration: none; font-weight: 600; }
.full { white-space: pre-wrap; font-size: 14.5px; background: var(--band); border-radius: 8px; padding: 10px; margin: 8px 0; word-break: break-word; }
.readout { font-size: 13.5px; min-height: 42px; display: flex; flex-wrap: wrap; gap: 2px 12px; align-items: center;
  font-variant-numeric: tabular-nums; margin: 6px 0 2px; }
.readout .L { font-weight: 600; min-width: 64px; }
.chart svg { width: 100%; height: auto; display: block; touch-action: pan-y; }
.chart svg:focus { outline: none; }
.chart svg:focus-visible { outline: 2px solid var(--chat); outline-offset: 2px; border-radius: 6px; }
.hint { font-size: 12px; color: var(--muted); margin-top: 2px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
th, td { padding: 4px 6px; text-align: right; border-bottom: 1px solid var(--grid); }
th:first-child, td:first-child { text-align: left; }
th { color: var(--ink2); font-weight: 600; position: sticky; top: 0; background: var(--surface); }
td.b { font-weight: 700; }
tr.sel td { background: var(--band); }
details.tbl summary { cursor: pointer; font-size: 13.5px; color: var(--ink2); padding: 8px 0; min-height: 36px; }
.tblwrap { max-height: 360px; overflow-y: auto; }
.nav { position: fixed; left: 0; right: 0; bottom: 0; z-index: 6; background: var(--page); border-top: 1px solid var(--border);
  padding: 8px 12px calc(8px + env(safe-area-inset-bottom)); }
.nav .in { max-width: 760px; margin: 0 auto; display: flex; gap: 8px; align-items: center; justify-content: space-between; }
.nav button { font: inherit; font-weight: 600; border: 1px solid var(--border); background: var(--surface); color: var(--ink);
  border-radius: 10px; min-height: 44px; padding: 0 16px; cursor: pointer; }
.nav button:disabled { opacity: .35; }
.nav .pos { font-size: 13px; color: var(--ink2); font-variant-numeric: tabular-nums; text-align: center; }
label.tog { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; color: var(--ink2); min-height: 32px; }
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
const DATA = /*DATA*/null;
const FAMS = ["multihop", "multilingual", "typo", "association", "poetry"];
const L = 63, YMAX = 250000;
const LENS = [
  {k: "c", name: "chat64", long: "J++ fit on 64 chat (UltraChat) texts", v: "--chat"},
  {k: "w", name: "wiki64", long: "J++ fit on 64 WikiText texts", v: "--wiki"},
  {k: "p", name: "published", long: "published Qwen3.6-27B J++ (reference)", v: "--pub"},
];
const st = {fam: "all", out: "all", k: 10, pub: true};
const best = a => { let b = 0; for (let i = 1; i < a.length; i++) if (a[i] < a[b]) b = i; return b; };
const fmt = r => r >= 10000 ? Math.round(r / 1000) + "k" : r >= 1000 ? (r / 1000).toFixed(1) + "k" : String(r);
const esc = s => s.replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const show = s => esc(s).replace(/\n/g, '<span style="color:var(--muted)">↵</span>\n');
const score = (d, key, k) => d.I.filter(i => Math.min(...i[key]) <= k).length / d.I.length;
function outcome(d, k) {
  const c = score(d, "c", k), w = score(d, "w", k);
  return c > w ? "chat" : w > c ? "wiki" : (c > 0 ? "both" : "none");
}
// how far apart the two lenses' best ranks are, in decades (signed: + = chat better)
const gap = d => d.I.reduce((s, i) => s + Math.log10(Math.min(...i.w)) - Math.log10(Math.min(...i.c)), 0);
const OUT = {
  chat: {label: "chat64 better", icon: "▲", color: "var(--chat)"},
  wiki: {label: "wiki64 better", icon: "▼", color: "var(--wiki)"},
  both: {label: "both hit", icon: "＝", color: "var(--ink2)"},
  none: {label: "neither hits", icon: "○", color: "var(--muted)"},
};
const keyOf = d => d.f + "/" + d.n;

function filtered() {
  return DATA.filter(d => (st.fam === "all" || d.f === st.fam) && (st.out === "all" || outcome(d, st.k) === st.out))
    .sort((a, b) => {
      const oa = score(a, "c", st.k) - score(a, "w", st.k), ob = score(b, "c", st.k) - score(b, "w", st.k);
      return Math.abs(ob) - Math.abs(oa) || Math.abs(gap(b)) - Math.abs(gap(a)) || keyOf(a).localeCompare(keyOf(b));
    });
}
function passAt(key, k, fam) {
  const fams = fam === "all" ? FAMS : [fam];
  const m = fams.map(f => { const xs = DATA.filter(d => d.f === f); return xs.reduce((s, d) => s + score(d, key, k), 0) / xs.length; });
  return m.reduce((a, b) => a + b, 0) / m.length;
}

function rankColor(r) {
  return r <= 1 ? "var(--r1)" : r <= 10 ? "var(--r10)" : r <= 100 ? "var(--r100)" : r <= 1000 ? "var(--r1k)" : "var(--rx)";
}
function strip(ranks) {
  const w = 100 / L;
  let s = '<svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">';
  ranks.forEach((r, i) => { s += `<rect x="${(i * w).toFixed(3)}" y="0" width="${(w * 0.82).toFixed(3)}" height="10" rx="0.4" fill="${rankColor(r)}"/>`; });
  return s + "</svg>";
}
const rankLegend = `<div class="legend" style="margin-top:6px">
  <span><span class="sw" style="background:var(--r1)"></span>rank 1</span>
  <span><span class="sw" style="background:var(--r10)"></span>2–10</span>
  <span><span class="sw" style="background:var(--r100)"></span>11–100</span>
  <span><span class="sw" style="background:var(--r1k)"></span>101–1k</span>
  <span><span class="sw" style="background:var(--rx);outline:1px solid var(--border)"></span>&gt;1k</span></div>`;

function header() {
  const fam = st.fam, k = st.k;
  const c = passAt("c", k, fam), w = passAt("w", k, fam);
  const n = fam === "all" ? DATA.length : DATA.filter(d => d.f === fam).length;
  return `<h1>chat64 vs wiki64: per-layer lens ranks <span class="tag">UNVERIFIED</span></h1>
  <p class="sub">exp19 fit_v3 · Qwen3.6-27B · J++ lenses fit on 64 chat vs 64 WikiText texts · held-out items · one fit per lens</p>
  <div class="card">
    <div class="tiles">
      <div class="tile"><div class="v" style="color:var(--ink)">${c.toFixed(3)}</div><div class="l"><span class="ln" style="background:var(--chat)"></span>chat64 pass@${k}</div></div>
      <div class="tile"><div class="v">${w.toFixed(3)}</div><div class="l"><span class="ln" style="background:var(--wiki)"></span>wiki64 pass@${k}</div></div>
      <div class="tile"><div class="v">${(c - w >= 0 ? "+" : "−") + Math.abs(c - w).toFixed(3)}</div><div class="l">difference · ${fam === "all" ? "macro" : fam}, n=${n}</div></div>
    </div>
    <details class="how" style="margin-top:8px"><summary>How to read this</summary>
      <p>Each item is a prompt plus one or more target words (e.g. the hidden “Brazil” in a two-hop fact). At every layer 0–62 the lens ranks the whole vocabulary; we show the target’s rank (1 = top). An item is a <b>hit at k</b> if its best rank over all layers is ≤ k — this is the eval’s pass@k.</p>
      <p>Strips: one cell per layer, left = layer 0, right = layer 62, darker = better rank. Tap an item for the full per-layer chart and table.</p>
      <p>Macro pass@10 over all families: chat64 − wiki64 = +0.049, 95% CI [+0.01, +0.08] (paired bootstrap over items). That interval covers item sampling only, not fit-to-fit noise: there is one fit per lens.</p>
    </details>
  </div>`;
}

function controls() {
  const chip = (grp, val, label, n) => `<button class="chip" data-g="${grp}" data-v="${val}" aria-pressed="${st[grp] === val}">${label}${n != null ? `<span class="n">${n}</span>` : ""}</button>`;
  const inFam = DATA.filter(d => st.fam === "all" || d.f === st.fam);
  const cnt = o => inFam.filter(d => outcome(d, st.k) === o).length;
  return `<div class="bar">
    <div class="row">${chip("fam", "all", "All", DATA.length)}${FAMS.map(f => chip("fam", f, f, DATA.filter(d => d.f === f).length)).join("")}</div>
    <div class="row">${chip("out", "all", "Any result")}${["chat", "wiki", "both", "none"].map(o => chip("out", o, OUT[o].icon + " " + OUT[o].label, cnt(o))).join("")}</div>
    <div class="row">${chip("k", 10, "hit = top 10")}${chip("k", 1, "hit = top 1")}</div>
  </div>`;
}

function itemCard(d) {
  const o = OUT[outcome(d, st.k)];
  const inters = d.I.map(i => {
    const bc = best(i.c), bw = best(i.w);
    return `<div class="inter"><div class="iw"><span>target <b>${esc(i.x)}</b></span>
      <span class="best"><span style="color:var(--chat)">●</span> #${fmt(i.c[bc])} @L${bc} · <span style="color:var(--wiki)">●</span> #${fmt(i.w[bw])} @L${bw}</span></div>
      <div class="strip"><span><span class="ln" style="background:var(--chat);width:8px"></span>chat64</span>${strip(i.c)}</div>
      <div class="strip"><span><span class="ln" style="background:var(--wiki);width:8px"></span>wiki64</span>${strip(i.w)}</div></div>`;
  }).join("");
  return `<a class="item" href="#${encodeURIComponent(keyOf(d))}"><div class="card">
    <div class="ihead"><div><div class="fam">${d.f}</div><div class="name">${esc(d.n)}</div></div>
    <div class="verdict" style="color:${o.color}">${o.icon} ${o.label}</div></div>
    <div class="prompt">${show(d.q)}</div>${inters}
    <div class="axisnote" style="margin-top:2px"><span></span><span><span>L0</span><span>L31</span><span>L62</span></span></div>
  </div></a>`;
}

function listView() {
  const xs = filtered();
  document.title = "exp19 · chat64 vs wiki64 per-layer ranks";
  app.innerHTML = header() + controls() +
    `<div class="count">${xs.length} item${xs.length === 1 ? "" : "s"} · sorted by biggest difference first</div>
     <div class="card" style="padding:8px 12px"><div style="font-size:12.5px;color:var(--ink2)">Strip colors = rank at that layer</div>${rankLegend}</div>` +
    xs.map(itemCard).join("") + `<p class="sub" style="text-align:center;margin-top:16px">Ranks from results/exp19_fit_data (fit_v3 evals; published J++ from fit_v2’s eval).</p>`;
  app.querySelectorAll(".chip").forEach(b => b.onclick = () => {
    const g = b.dataset.g; st[g] = g === "k" ? +b.dataset.v : b.dataset.v;
    if (g === "fam") st.out = "all";
    const y = window.scrollY; listView(); window.scrollTo(0, y);
  });
}

// ---- detail chart
const W = 360, H = 230, M = {l: 40, r: 10, t: 10, b: 30};
const xs = l => M.l + (W - M.l - M.r) * l / (L - 1);
const ys = r => M.t + (H - M.t - M.b) * Math.log10(Math.min(YMAX, Math.max(1, r))) / Math.log10(YMAX);
function chartSVG(i, id) {
  const lenses = LENS.filter(x => i[x.k] && (x.k !== "p" || st.pub));
  let s = `<svg id="${id}" viewBox="0 0 ${W} ${H}" tabindex="0" role="img" aria-label="Rank of ${esc(i.x)} at each layer for ${lenses.map(x => x.name).join(", ")}. Full values in the table below.">`;
  s += `<rect x="${M.l}" y="${ys(1)}" width="${W - M.l - M.r}" height="${ys(10) - ys(1)}" fill="var(--band)"/>`;
  [1, 10, 100, 1000, 10000, 100000].forEach(r => {
    s += `<line x1="${M.l}" x2="${W - M.r}" y1="${ys(r)}" y2="${ys(r)}" stroke="var(--grid)" stroke-width="1"/>`;
    s += `<text x="${M.l - 5}" y="${ys(r) + 3.5}" text-anchor="end" font-size="10" fill="var(--muted)" style="font-variant-numeric:tabular-nums">${fmt(r)}</text>`;
  });
  [0, 10, 20, 30, 40, 50, 62].forEach(l => {
    s += `<text x="${xs(l)}" y="${H - M.b + 14}" text-anchor="middle" font-size="10" fill="var(--muted)">${l}</text>`;
  });
  s += `<line x1="${M.l}" x2="${W - M.r}" y1="${H - M.b}" y2="${H - M.b}" stroke="var(--axis)"/>`;
  s += `<text x="${(M.l + W - M.r) / 2}" y="${H - 2}" text-anchor="middle" font-size="10.5" fill="var(--ink2)">layer</text>`;
  s += `<text x="10" y="${M.t + (H - M.t - M.b) / 2}" text-anchor="middle" font-size="10.5" fill="var(--ink2)" transform="rotate(-90 10 ${M.t + (H - M.t - M.b) / 2})">rank (1 = top, log)</text>`;
  for (const x of [...lenses].reverse()) {
    const pts = i[x.k].map((r, l) => `${xs(l).toFixed(1)},${ys(r).toFixed(1)}`).join(" ");
    s += `<polyline points="${pts}" fill="none" stroke="var(${x.v})" stroke-width="${x.k === "p" ? 1.5 : 2}" stroke-linejoin="round" stroke-linecap="round" opacity="${x.k === "p" ? 0.9 : 1}"/>`;
  }
  for (const x of lenses) {
    const b = best(i[x.k]);
    s += `<circle cx="${xs(b)}" cy="${ys(i[x.k][b])}" r="4.5" fill="var(${x.v})" stroke="var(--surface)" stroke-width="2"/>`;
  }
  s += `<text x="${M.l + 4}" y="${ys(1) + 11}" font-size="10" fill="var(--ink2)" stroke="var(--band)" stroke-width="3" paint-order="stroke">top 10</text>`;
  s += `<line class="cross" x1="0" x2="0" y1="${M.t}" y2="${H - M.b}" stroke="var(--ink2)" stroke-width="1" visibility="hidden"/>`;
  s += `<g class="dots"></g>`;
  s += `<rect class="hit" x="${M.l - 8}" y="0" width="${W - M.l - M.r + 16}" height="${H}" fill="transparent"/>`;
  return s + "</svg>";
}
function readoutHTML(i, l) {
  const lenses = LENS.filter(x => i[x.k] && (x.k !== "p" || st.pub));
  if (l == null) {
    return `<span class="L">Best</span>` + lenses.map(x => { const b = best(i[x.k]); return `<span><span class="ln" style="background:var(${x.v})"></span>${x.name} <b>#${i[x.k][b].toLocaleString()}</b> @L${b}</span>`; }).join("");
  }
  return `<span class="L">Layer ${l}</span>` + lenses.map(x => `<span><span class="ln" style="background:var(${x.v})"></span>${x.name} <b>#${i[x.k][l].toLocaleString()}</b></span>`).join("");
}
function tableHTML(i, id) {
  const lenses = LENS.filter(x => i[x.k] && (x.k !== "p" || st.pub));
  const bs = Object.fromEntries(lenses.map(x => [x.k, best(i[x.k])]));
  let s = `<details class="tbl"><summary>All 63 layers as a table</summary><div class="tblwrap"><table id="${id}"><thead><tr><th>layer</th>${lenses.map(x => `<th><span class="ln" style="background:var(${x.v});width:10px"></span>${x.name}</th>`).join("")}</tr></thead><tbody>`;
  for (let l = 0; l < L; l++) s += `<tr data-l="${l}"><td>L${l}</td>${lenses.map(x => `<td class="${bs[x.k] === l ? "b" : ""}">${i[x.k][l].toLocaleString()}</td>`).join("")}</tr>`;
  return s + `</tbody></table></div><div class="hint">Bold = that lens's best layer.</div></details>`;
}
function wireChart(i, n) {
  const svg = document.getElementById("ch" + n), out = document.getElementById("ro" + n), tb = document.getElementById("tb" + n);
  const cross = svg.querySelector(".cross"), dots = svg.querySelector(".dots");
  const lenses = LENS.filter(x => i[x.k] && (x.k !== "p" || st.pub));
  let cur = null;
  const set = l => {
    cur = l;
    if (l == null) { cross.setAttribute("visibility", "hidden"); dots.innerHTML = ""; out.innerHTML = readoutHTML(i, null); }
    else {
      cross.setAttribute("x1", xs(l)); cross.setAttribute("x2", xs(l)); cross.setAttribute("visibility", "visible");
      dots.innerHTML = lenses.map(x => `<circle cx="${xs(l)}" cy="${ys(i[x.k][l])}" r="4" fill="var(${x.v})" stroke="var(--surface)" stroke-width="2"/>`).join("");
      out.innerHTML = readoutHTML(i, l);
    }
    tb.querySelectorAll("tr.sel").forEach(r => r.classList.remove("sel"));
    if (l != null) tb.querySelector(`tr[data-l="${l}"]`).classList.add("sel");
  };
  const at = e => {
    const p = svg.getBoundingClientRect(), x = (e.clientX - p.left) / p.width * W;
    return Math.max(0, Math.min(L - 1, Math.round((x - M.l) / (W - M.l - M.r) * (L - 1))));
  };
  svg.addEventListener("pointerdown", e => set(at(e)));
  svg.addEventListener("pointermove", e => { if (e.pointerType === "mouse" || e.buttons) set(at(e)); });
  svg.addEventListener("pointerleave", e => { if (e.pointerType === "mouse") set(null); });
  svg.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { set(cur == null ? 0 : Math.min(L - 1, cur + 1)); e.preventDefault(); }
    if (e.key === "ArrowLeft") { set(cur == null ? L - 1 : Math.max(0, cur - 1)); e.preventDefault(); }
    if (e.key === "Escape") set(null);
  });
  set(null);
}

function detailView(key) {
  const xsF = filtered();
  let idx = xsF.findIndex(d => keyOf(d) === key);
  const d = idx >= 0 ? xsF[idx] : DATA.find(x => keyOf(x) === key);
  if (!d) { location.hash = ""; return; }
  const list = idx >= 0 ? xsF : [d]; if (idx < 0) idx = 0;
  const o = OUT[outcome(d, st.k)];
  document.title = d.n + " · exp19";
  app.innerHTML = `<a class="back" href="#">‹ All items</a>
  <div class="card">
    <div class="ihead"><div><div class="fam">${d.f}</div><h2>${esc(d.n)}</h2></div>
    <div class="verdict" style="color:${o.color}">${o.icon} ${o.label} <span style="font-weight:400;color:var(--ink2)">(top ${st.k})</span></div></div>
    <div class="full">${show(d.q)}</div>
    ${d.t ? `<div style="font-size:13.5px;color:var(--ink2)">Model's answer: <b style="color:var(--ink)">${esc(d.t)}</b></div>` : ""}
    <div class="legend" style="margin-top:10px">${LENS.map(x => `<span title="${x.long}"><span class="ln" style="background:var(${x.v})"></span>${x.name}</span>`).join("")}</div>
    <label class="tog"><input type="checkbox" id="pub" ${st.pub ? "checked" : ""}> show published J++ (gray)</label>
  </div>
  ${d.I.map((i, n) => `<div class="card chart">
    <div class="iw" style="font-size:14.5px"><span>Target word <b>${esc(i.x)}</b></span><span class="best">${n + 1} of ${d.I.length}</span></div>
    <div class="readout" id="ro${n}" aria-live="polite"></div>
    ${chartSVG(i, "ch" + n)}
    <div class="hint">Tap or drag on the chart to read a layer · dots mark each lens's best layer</div>
    ${tableHTML(i, "tb" + n)}
  </div>`).join("")}
  <div class="nav"><div class="in">
    <button id="prev" ${idx <= 0 ? "disabled" : ""}>‹ Prev</button>
    <div class="pos">${idx + 1} / ${list.length}<br>${st.fam === "all" ? "all families" : st.fam}${st.out === "all" ? "" : " · " + OUT[st.out].label}</div>
    <button id="next" ${idx >= list.length - 1 ? "disabled" : ""}>Next ›</button>
  </div></div>`;
  d.I.forEach((i, n) => wireChart(i, n));
  document.getElementById("pub").onchange = e => { st.pub = e.target.checked; detailView(key); };
  const go = j => { location.hash = encodeURIComponent(keyOf(list[j])); };
  document.getElementById("prev").onclick = () => idx > 0 && go(idx - 1);
  document.getElementById("next").onclick = () => idx < list.length - 1 && go(idx + 1);
}

let listScroll = 0;
function route() {
  const key = decodeURIComponent(location.hash.slice(1));
  if (key) { if (!app.querySelector(".back")) listScroll = window.scrollY; detailView(key); window.scrollTo(0, 0); }
  else { listView(); window.scrollTo(0, listScroll); }
}
window.addEventListener("hashchange", route);
route();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
