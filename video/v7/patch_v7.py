"""v6 -> v7: real Pexels footage, explicit problem / solution beats, race rebuilt on real footage with the prototype's aerial mini-map."""
import pathlib, re
HERE = pathlib.Path(__file__).parent
proto = (HERE / "../../prototype/KokoShield_Prototype.html").resolve().read_text(encoding="utf-8")
NODE = re.search(r"const NODE=\{.*?\};", proto, re.S).group(0)
LINKS = re.search(r"const LINKS='[^']*';", proto).group(0)
p = HERE / "stage/scenes_v5.js"; s = p.read_text(encoding="utf-8")
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
def block(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

FRAMES = dict(rain1=150, rainleaf=156, ghana=198, orchard_a=348, leafbg=349, aerialbg=486, orchard_b=319, path_a=319, podbg=258, aerial_v=144, path_end=481)
VCRED = dict(rain1="Video: Nothing Ahead · Pexels", rainleaf="Video: Srinivas Kashyap · Pexels", ghana="Cocoa farmer, Ghana · Video: Zeal Creative Studios · Pexels",
             orchard_a="Video: Prodèép Nëpalënsis · Pexels", leafbg="", aerialbg="", orchard_b="", path_a="", podbg="",
             aerial_v="Video: Serg Alesenko · Pexels", path_end="Video: Ucundinamarca Virtual · Pexels")
vdefs = "const VFR = " + str(FRAMES).replace("'", '"') + ", VCRED = " + str(VCRED).replace("'", '"').replace('\\xa0', ' ') + ";"

# ---------- real-footage shots replace the photo shots of acts 1-4 ----------
block("/* ---------- ACT 1: storm and crisis (cold, dark) ---------- */", "/* ---------- ACT 1 overlays ---------- */", """/* ---------- real footage (Pexels License clips, cut to 30 fps frame sequences by extract_footage.py) ---------- */
""" + vdefs + """
const VS = [];
function vshot(seg, t0, t1, from, to, grade = '', credit = null) {
  const el = document.createElement('div'); el.className = 'shot';
  el.innerHTML = `<img style="filter:${grade};width:100%;height:100%;object-fit:cover">`; $('#bg').appendChild(el);
  const o = { el, file: seg, t0, t1, from, to, credit: credit ?? VCRED[seg] ?? '' }; SHOTS.push(o);
  VS.push({ img: el.querySelector('img'), seg, n: VFR[seg], t0 }); return o;
}
function updateVids(t) {
  for (const v of VS) {
    const shown = v.img.closest('.shot, .ov'); if (shown && shown.style.display === 'none') continue;
    const i = Math.max(0, Math.min(v.n - 1, Math.round((t - v.t0) * 30)));
    if (v.img.dataset.i !== String(i)) { v.img.dataset.i = i; v.img.src = `assets/vid/${v.seg}/f${String(i + 1).padStart(4, '0')}.jpg`; PEND.push(v.img.decode().catch(() => 0)); }
  }
}
/* ---------- ACT 1: the disease and the problem (cold) ---------- */
const COLD = 'saturate(.6) brightness(.62) contrast(1.12) hue-rotate(-6deg)';
vshot('rain1', -0.2, 4.6, [1.04, 0, 0], [1.14, -1, 1], COLD);
vshot('rainleaf', 4.2, 8.9, [1.03, 0, 0], [1.1, 1, 0], 'saturate(.7) brightness(.66) contrast(1.1)');
shot('13_black_pod.jpg', 8.5, S[1] + 0.5, [1.02, 0, 0], [1.16, -4, -3], 'saturate(.8) brightness(.72) contrast(1.12)', '50% 43%');
vshot('ghana', S[1] - 0.1, at(1, 6.4), [1.03, 0, 0], [1.1, 0, 0], 'saturate(.7) brightness(.66) contrast(1.08)');
vshot('orchard_a', at(1, 5.8), S[2] + 0.5, [1.03, 0, 0], [1.12, 0, 0], 'saturate(.5) brightness(.55) contrast(1.15)');
/* ---------- ACT 2: the solution (glow over dim real footage) ---------- */
vshot('leafbg', S[2] - 0.2, S[3] + 0.5, [1.15, 0, 0], [1.2, 0, 0], 'brightness(.3) blur(8px) saturate(.7)', '');
vshot('aerialbg', S[3] + 0.1, S[4] + 0.4, [1.1, 0, 0], [1.18, 0, 0], 'brightness(.38) blur(6px) saturate(.85)', '');
/* ---------- ACT 3: proof and the find ---------- */
shot('06_farm.jpg', at(5, 9.6), S[6] + 0.4, [1.1, 0, 0], [1.18, 0, 0], 'brightness(.32) blur(8px)');
shot('12_black_pod.jpg', S[6] - 0.2, at(6, 4.0), [1.0, 0, 0], [1.14, -3, 0], 'brightness(.85) saturate(1.05)', '50% 40%');
vshot('podbg', at(6, 3.4), at(6, 9.2), [1.1, 0, 0], [1.16, 0, 0], 'brightness(.4) blur(9px)', '');
shot('06_farm.jpg', at(6, 8.6), S[7] + 0.4, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.3) blur(8px)');
/* ---------- ACT 4: impact and the ask (golden) ---------- */
const GOLD = 'sepia(.22) saturate(1.15) brightness(.9) contrast(1.05)';
vshot('aerial_v', S[7] - 0.2, at(7, 4.4), [1.04, 0, 0], [1.12, 0, 0], GOLD);
shot('15_farmer.jpg', at(7, 4.0), at(7, 8.4), [1.04, 0, 0], [1.12, 0, -2], GOLD, '50% 30%');
shot('22_rice.jpg', at(7, 8.0), S[8] + 0.6, [1.04, 0, 0], [1.14, 2, 0], GOLD);
vshot('path_end', S[8] + 0.2, END + 1, [1.04, 0, 0], [1.1, 0, 0], GOLD);

""")

# ---------- ACT 1: explicit problem statement ----------
lines = s.split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith('ov(`<div class="h2" style="font-size:40px">Which block first?'))
j = i
while not lines[j].rstrip().endswith(";"): j += 1
k = next(q for q, l in enumerate(lines) if l.startswith("const qblocks = "))
m = k
while not lines[m].rstrip().endswith(";"): m += 1
PROB = """ov(`<div class="kick" style="color:#ff8a66">The problem</div><div class="h2" style="font-size:38px">Too many blocks, too little time</div>${['Rain spreads black pod within days', 'About 30 minutes to scout after a storm', 'Usual round: the wettest blocks are found late'].map((x, i) => `<div class="row" id="pb${i}" style="opacity:0"><div class="num" style="background:#B0452E">${i + 1}</div><div style="font-size:25px;font-weight:700">${x}</div></div>`).join('')}`,
  'left:70px;top:330px;width:780px', at(1, 1.4), S[2] - 0.3, 'left', 'glass dark');"""
lines = lines[:i] + [PROB] + lines[j + 1:k] + lines[m + 1:]
s = "\n".join(lines)
rep("  qblocks.forEach((q, i) => { const p = 1 + 0.06 * Math.sin(t * 5 + i); q.el.style.scale = p; });",
    "  [0, 1, 2].forEach(i => { const d = [3.0, 5.5, 9.8][i], q = ramp(t, at(1, d), at(1, d + 0.4)); const e = $('#pb' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * -30}px)`; });")
rep("Math.max(Math.min(ramp(t, 0, 1.0), 1 - ramp(t, S[1] + 0.2, S[1] + 2.2))", "Math.max(0.4 * Math.min(ramp(t, 0, 1.0), 1 - ramp(t, S[1] + 0.2, S[1] + 2.2))")

# ---------- ACT 2 labels ----------
rep('<div class="h1" style="font-size:78px;color:#fff;text-shadow:0 0 30px rgba(159,224,191,.5)">KokoShield</div>',
    '<div class="kick" style="color:#9fe0bf;font-size:24px">The solution</div><div class="h1" style="font-size:78px;color:#fff;text-shadow:0 0 30px rgba(159,224,191,.5)">KokoShield</div>')
rep('<div class="kick">Inputs</div>', '<div class="kick">How it works · inputs</div>')

# ---------- ACT 3: the proof, rebuilt on real footage ----------
RACE = """/* ---------- ACT 3: the proof: two real scouts, same 30 minutes, the prototype's aerial map with GPS trails ---------- */
""" + NODE + "\n" + LINKS + """
const GRAPH = (() => { const g = {}; for (const k in NODE) g[k] = []; for (const l of LINKS.split(' ')) { const [a, b] = l.split('-'), d = Math.hypot(NODE[a][0] - NODE[b][0], NODE[a][1] - NODE[b][1]); g[a].push([b, d]); g[b].push([a, d]); } return g; })();
function shortestP(a, b) { const dist = { [a]: 0 }, prev = {}, done = new Set();
  for (;;) { let u = null; for (const k in dist) if (!done.has(k) && (u === null || dist[k] < dist[u])) u = k; if (u === null || u === b) break; done.add(u);
    for (const [v, w] of GRAPH[u]) { const nd = dist[u] + w; if (dist[v] === undefined || nd < dist[v]) { dist[v] = nd; prev[v] = u; } } }
  const nodes = [b]; while (nodes[0] !== a) nodes.unshift(prev[nodes[0]]); return nodes; }
const PLAN_R = [['A', 7, 3], ['D', 8, 2], ['B', 8, 1], ['G', 7, 1]], PLAN_U = [['B', 8, 1], ['C', 7, 0], ['E', 8, 0], ['G', 7, 1]];
function buildRoute(plan) {   /* path along the footpath network, one leg per stop, with find times like the prototype's finds() */
  const legs = []; let prev = 'gate', e = 0; const finds = [];
  for (const [k, m, f] of plan) { const pts = shortestP(prev, 'e' + k).map(n => NODE[n]); let L = 0; const cum = [0]; for (let i = 1; i < pts.length; i++) { L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); cum.push(L); }
    legs.push({ k, m, t0: e, pts, cum, L }); for (let q = 1; q <= f; q++) finds.push({ t: e + m * q / (f + 1), k, q }); e += m; prev = 'e' + k; }
  const all = []; legs.forEach((g, i) => g.pts.forEach((pt, j) => { if (i && !j) return; all.push(pt); }));
  return { legs, finds, all };
}
const RR = buildRoute(PLAN_R), RU = buildRoute(PLAN_U);
function posAt(R, min) {
  for (const g of R.legs) { if (min >= g.t0 + g.m && g !== R.legs[R.legs.length - 1]) continue;
    const u = Math.max(0, min - g.t0), tw = g.m * 0.28;
    if (u < tw) { const d = sm(u / tw) * g.L; let i = 1; while (i < g.cum.length - 1 && g.cum[i] < d) i++; const a = (d - g.cum[i - 1]) / Math.max(1e-6, g.cum[i] - g.cum[i - 1]);
      return { x: lerp(g.pts[i - 1][0], g.pts[i][0], a), y: lerp(g.pts[i - 1][1], g.pts[i][1], a), leg: g, walked: d }; }
    const c = g.pts[g.pts.length - 1], ph = (u - tw) / (g.m - tw) * Math.PI * 2;   /* searching inside the block */
    return { x: c[0] + Math.sin(ph) * 16, y: c[1] - 10 + Math.cos(ph) * 10 - 10 * Math.sin(ph / 2), leg: g, walked: g.L }; }
}
const STOPXY = k => NODE['e' + k];
function miniMap(id, R, col) {
  const poly = Object.keys(POLY).map(k => { const f = { A: '#B0452E', D: '#B0452E', G: '#B0452E', B: '#D6A03E' }[k];
    return `<polygon points="${POLY[k]}" fill="${f || 'none'}" fill-opacity="${f ? .32 : 0}" stroke="#fff" stroke-opacity="${k === 'F' ? .35 : .75}" stroke-width="${f ? 2.2 : 1.2}" stroke-linejoin="round"/>
      <text x="${LBL[k][0]}" y="${LBL[k][1]}" text-anchor="middle" dominant-baseline="central" font-size="17" font-weight="800" fill="#fff" style="paint-order:stroke" stroke="rgba(0,0,0,.45)" stroke-width="3">${k}</text>`; }).join('');
  const route = R.all.map(p => p.join(',')).join(' ');
  return `<svg viewBox="0 0 650 357" style="display:block;width:100%;height:100%;font-family:'Noto Sans','Segoe UI',sans-serif">
    <image href="assets/farm_aerial.jpg" x="-40" y="-188" width="1100" height="733" preserveAspectRatio="none"/><rect x="-40" y="-188" width="1100" height="733" fill="rgba(10,30,20,.18)"/>
    ${poly}<polyline points="${route}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-dasharray="6 7" stroke-linejoin="round"/>
    <polyline id="${id}trl" points="" fill="none" stroke="${col}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>
    <g id="${id}pins"></g>
    <rect x="36" y="330" width="12" height="12" rx="2" fill="#17201C" stroke="#fff" stroke-width="1.5"/>
    <g id="${id}dot"><circle r="15" fill="${col}" opacity=".28" id="${id}halo"/><circle r="8.5" fill="${col}" stroke="#fff" stroke-width="3"/></g></svg>`;
}
function realHalf(id, who, title, col, R, seg, grade) {
  return `<div class="half rh" id="${id}"><img id="${id}v" style="filter:${grade}">
    <div class="rtag"><span class="recdot" style="background:${col}"></span>${who}</div>
    <div class="hhead" style="border-color:${col};top:200px"><div style="font-size:24px;font-weight:800">${title}</div><div style="font-size:19px;color:#cfe6da" id="${id}f">First find —</div></div>
    <div class="rscore"><span id="${id}n" style="color:${col}">0</span><small>suspect pods</small></div>
    <div class="mm">${miniMap(id, R, col)}</div></div>`;
}
const raceT0 = at(5, 1.0), raceT1 = at(5, 9.6), raceMin = t => 30 * ramp(t, raceT0, raceT1);
const raceOv = ov(`<div class="split">${realHalf('hu', 'Scout 1 · usual round', 'Usual round · B → C → E → G', '#9fb4c6', RU, 'orchard_b', 'saturate(.55) brightness(.62) contrast(1.1)')}${realHalf('hr2', 'Scout 2 · KokoShield route', 'Priority route · A → D → B → G', '#3fe08f', RR, 'path_a', 'saturate(1.05) brightness(.8) contrast(1.05)')}
  <div class="vs"><div class="kick" style="margin:0;color:#9fe0bf">The proof · same farm</div><div id="clk3" style="font-size:54px;font-weight:800;color:#fff">0:00</div><div style="font-size:18px;color:#cfe6da">of 30 min · same time</div></div></div>`,
  'left:0;top:0', S[5] + 0.2, at(5, 10.3), 'fade', '', 'Real footage: Prodèép Nëpalënsis, Ucundinamarca Virtual · Pexels · routes and finds: demo simulation on the prototype map');
VS.push({ img: $('#huv'), seg: 'orchard_b', n: VFR.orchard_b, t0: S[5] + 0.2 }, { img: $('#hr2v'), seg: 'path_a', n: VFR.path_a, t0: S[5] + 0.2 });
function drawSide(id, R, min, col) {
  const p = posAt(R, min); $('#' + id + 'dot').setAttribute('transform', `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`);
  $('#' + id + 'halo').setAttribute('r', (13 + 5 * Math.abs(Math.sin(min * 3))).toFixed(1));
  const pts = []; for (const g of R.legs) { if (g.t0 > min) break; const done = g === p.leg ? p.walked : g.L;
    g.pts.forEach((pt, j) => { if (g.cum[j] <= done + 1e-6) pts.push(pt); }); if (g === p.leg) { pts.push([p.x, p.y]); break; } }
  $('#' + id + 'trl').setAttribute('points', pts.map(q => q[0].toFixed(1) + ',' + q[1].toFixed(1)).join(' '));
  const got = R.finds.filter(f => f.t <= min);
  $('#' + id + 'pins').innerHTML = got.map(f => { const [x, y] = STOPXY(f.k), a = Math.min(1, (min - f.t) / 0.8), dx = (f.q - 2) * 13;
    return `<g transform="translate(${x + dx} ${y - 22}) scale(${(0.4 + 0.6 * eo(a)).toFixed(2)})"><path d="M0 0c-7-9-11-14-11-20a11 11 0 0 1 22 0c0 6-4 11-11 20z" fill="#B0452E" stroke="#fff" stroke-width="2"/><circle cy="-20" r="4" fill="#fff"/></g>`; }).join('');
  $('#' + id + 'n').textContent = got.length; $('#' + id + 'f').textContent = got.length ? `First find at minute ${Math.round(got[0].t)}` : 'First find —';
}
"""
block("/* ---------- ACT 3: split-screen race ---------- */", 'ov(`<div class="kick">Minute 2', RACE)
s = re.sub(r"  /\* act 3 \*/\n.*?  /\* act 4 \*/", lambda _: """  /* act 3 */
  updateVids(t);
  { const m = raceMin(t); if (t > S[5] - 0.5 && t < at(5, 10.8)) { drawSide('hu', RU, m, '#9fb4c6'); drawSide('hr2', RR, m, '#3fe08f'); }
    $('#clk3').textContent = `${Math.floor(m)}:${String(Math.floor((m % 1) * 60)).padStart(2, '0')}`; }
  /* act 4 */""", s, count=1, flags=re.S)
assert "drawSide('hu'" in s

# ---------- find card: no AI placeholder now ----------
rep("Minute 2 · Block A · Stop 1 of 4</div>", "The find · Block A · minute 2</div>")
# ---------- end card credits ----------
s = re.sub(r"Photos: Isabell Schulz.*?Voice: AI-generated\.", "Footage: Nothing Ahead, Srinivas Kashyap, Zeal Creative Studios, Prodèép Nëpalënsis, Ucundinamarca Virtual, Serg Alesenko (Pexels License). Photos: Scot Nelson (CC0), Irene Scott/AusAID (CC BY 2.0), Isabell Schulz (CC BY-SA 2.0), GPhoto15 (CC BY 4.0), via Wikimedia Commons. App footage: KokoShield Field Desk prototype, demo data. Drone survey, routes and counts: demo simulation. Voice: AI-generated.", s, count=1, flags=re.S)
assert "Footage: Nothing Ahead" in s
assert "AI('" not in s.replace("const AI = (txt)", "")
p.write_text(s, encoding="utf-8"); print("scenes v7 patched")

css = HERE / "stage/extra.css"; c = css.read_text(encoding="utf-8")
if ".rh img" not in c:
    c += """
.rh img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rtag{position:absolute;left:40px;top:140px;display:flex;align-items:center;gap:10px;background:rgba(8,16,12,.78);color:#fff;font-size:20px;font-weight:700;padding:8px 14px;border-radius:10px}
.recdot{width:12px;height:12px;border-radius:50%;box-shadow:0 0 10px currentColor}
.rscore{position:absolute;right:40px;top:200px;text-align:right;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.7);font-variant-numeric:tabular-nums}
.rscore span{display:block;font-size:76px;font-weight:800;line-height:1}.rscore small{font-size:19px;color:#e2efe8;font-weight:700}
.mm{position:absolute;left:40px;top:330px;width:500px;height:275px;border-radius:14px;overflow:hidden;border:2px solid rgba(255,255,255,.55);box-shadow:0 20px 50px rgba(0,0,0,.55)}
"""
    css.write_text(c, encoding="utf-8"); print("css added")
