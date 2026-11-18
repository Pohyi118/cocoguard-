"""Build race.html (the route race, using the app's own Compare maps) and render it to ../rec/race.mp4.
Timing comes from ../timeline.json: the clip starts at scene 10 and ends with scene 11."""
import json, pathlib, re, socket, subprocess, sys, time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent; V6 = HERE.parent; FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 30
TL = json.load(open(V6 / "timeline.json")); SC = {s["id"]: s for s in TL["scenes"]}


def wt(sid, word, occ=1):
    n = 0
    for a, b, w in SC[sid]["words"]:
        if w.lower().strip(".,;:?") == word.lower():
            n += 1
            if n == occ: return SC[sid]["speech_at"] + a
    raise KeyError(word)


C0, C1 = SC[10]["start"], SC[11]["end"]
T0 = wt(10, "routes") + 0.2; MISS = wt(11, "walks") - 0.1; K0 = wt(11, "KokoShield's") - 0.15; NONE = wt(11, "none") - 0.1
P = dict(T0=round(T0 - C0, 2), DU=round(MISS - 0.15 - T0, 2), MISS=round(MISS - C0, 2), RW=round(K0 - 0.95 - C0, 2), K0=round(K0 - C0, 2),
         DK=round(NONE - K0, 2), NONE=round(NONE - C0, 2), SB=round(NONE + 0.6 - C0, 2), END=round(C1 - C0, 2))


def svg(name, pre):
    s = (HERE / name).read_text(encoding="utf-8")
    s = re.sub(r'href="blob:[^"]+"', 'href="farm_aerial.jpg"', s)
    return s.replace('<svg class="map aerial"', f'<svg id="{pre}" class="map"', 1)


html = """<!doctype html><html><head><meta charset="utf-8"><title>Route race</title><style>
@font-face{font-family:Plex;src:url(../fonts/plex.woff2) format("woff2");font-weight:100 700}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0f1a15;font-family:Plex,sans-serif;color:#fff}
body{background:radial-gradient(120% 90% at 50% 40%,#1b2c24 0%,#0f1a15 60%,#0a120e 100%)}
.side{position:absolute;top:226px;width:860px;transition:none}
#L{left:70px}#R{left:990px}
.side h2{margin:0;font-weight:600;font-size:40px;letter-spacing:-.01em}.side p{margin:6px 0 18px;font-size:24px;color:#b9c9c0}
.frame{position:relative;width:860px;height:472px;border-radius:14px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.45)}
svg.map{width:860px;height:472px;display:block}
.ml{font:600 12px Plex;fill:#fff;paint-order:stroke;stroke:rgba(0,0,0,.55);stroke-width:3px}
.mnum{fill:#fff;font:700 11.5px Plex;text-anchor:middle;dominant-baseline:central}
.chev{display:none}
.count{display:flex;align-items:baseline;gap:14px;margin-top:22px}.count b{font-weight:600;font-size:84px;line-height:1}.count span{font-size:26px;color:#cfdcd4}
.miss{font-size:26px;color:#ffb3a1;margin-top:4px;height:34px}
#clock{position:absolute;left:0;right:0;top:56px;text-align:center}
#clock .t{font-weight:600;font-size:64px;letter-spacing:-.01em}#clock .t small{font-size:30px;font-weight:500;color:#b9c9c0;margin-left:8px}
#bar{width:520px;height:8px;border-radius:4px;background:rgba(255,255,255,.15);margin:14px auto 0;overflow:hidden}#bar i{display:block;height:100%;background:#5fc095;width:0}
#demo{position:absolute;left:0;right:0;top:186px;text-align:center;font-size:21px;color:#9fb3a8}
.dot{fill:#fff;stroke:#1E5A43;stroke-width:3}
.find{fill:#e0533a;stroke:#fff;stroke-width:1.6}
.dot{r:6}
.missblk{fill:rgba(224,83,58,.0);stroke:#ff6a4d;stroke-width:3}
#big{position:absolute;left:260px;top:196px;width:1400px;height:768px;border-radius:14px;overflow:hidden;box-shadow:0 22px 60px rgba(0,0,0,.5)}
#big .frame{position:absolute;inset:0;width:1400px;height:768px;border-radius:0;box-shadow:none}
#big svg.map{width:1400px;height:768px}
#clock{top:40px}#clock .t{font-size:56px}#demo{position:static;margin-top:8px;font-size:20px;color:#9fb3a8}
#title{position:absolute;left:260px;top:60px}#title h2{margin:0;font-size:46px;font-weight:600}#title p{margin:4px 0 0;font-size:24px;color:#b9c9c0}
#score{position:absolute;z-index:5;right:260px;top:52px;display:flex;align-items:baseline;gap:14px}
#score b{font-size:76px;font-weight:600;line-height:1;display:inline-block;transform-origin:0 80%}#score span{font-size:28px;color:#d6e3db}
#score em{position:absolute;right:0;top:96px;white-space:nowrap;font-style:normal;font-size:26px;color:#ffb3a1}
#board{position:absolute;z-index:6;inset:0;display:flex;justify-content:center;align-items:center;gap:60px;opacity:0}
#board .col{width:560px;padding:40px 44px;border-radius:18px;background:rgba(20,34,27,.94);box-shadow:0 20px 60px rgba(0,0,0,.5)}
#board .win{box-shadow:0 0 0 3px #6fd3a4,0 0 50px rgba(95,192,149,.55)}
#board h3{margin:0 0 10px;font-size:36px;font-weight:600}#board .n{font-size:150px;font-weight:600;line-height:1}#board .l{font-size:30px;color:#cfdcd4}
#board .m{margin-top:16px;font-size:32px;font-weight:600}.bad{color:#ff9f88}.good{color:#8fe3b8}

.route-line{filter:drop-shadow(0 0 3px rgba(140,240,190,.95)) drop-shadow(0 0 8px rgba(95,192,149,.7))}
.plus{font:700 15px Plex;fill:#fff;paint-order:stroke;stroke:#c2412b;stroke-width:3px;text-anchor:middle}
.frame{transform-origin:0 0;z-index:1}#R .frame{z-index:2}
.count b{display:inline-block;transform-origin:0 80%}
#intro{position:absolute;left:0;right:0;top:64px;text-align:center;font-weight:600;font-size:52px;letter-spacing:-.01em}
#intro small{display:block;font-size:26px;font-weight:500;color:#b9c9c0;margin-top:8px}
</style></head><body>
<div id="intro">Same farm. Same 30 minutes.<small>Two ways to search it</small></div>
<div id="clock"><div class="t"><span id="min">0</span><small>of 30 min</small></div><div id="bar"><i></i></div><div id="demo">Demo data from the KokoShield prototype</div></div>
<div id="title"><h2 id="tname">Usual round</h2><p id="tsub">The farmer's normal order</p></div>
<div id="big"><div class="frame" id="FU">USUAL</div><div class="frame" id="FK">RANKED</div></div>
<div id="score"><b id="cnt">0</b><span>infected pods found</span><em id="miss"></em></div>
<div id="board"><div class="col" id="bu"><h3>Usual round</h3><div class="n">2</div><div class="l">pods found</div><div class="m bad">2 sick blocks missed</div></div>
<div class="col win" id="bk"><h3>KokoShield route</h3><div class="n">7</div><div class="l">pods found</div><div class="m good">0 missed</div></div></div>
<script>
const P = PARAMS;
const sm = x => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
// minutes on the clock -> where the scout is (stop marker id), with finds in minutes (from the app's Compare timeline)
const PLAN = {
  R: { holds: [['A', 1.0, 6.0], ['D', 8.6, 13.0], ['B', 17.6, 19.6], ['G', 25.6, 27.2]], finds: [[1.75, 'A'], [3.5, 'A'], [5.25, 'A'], [9.67, 'D'], [12.34, 'D'], [19.0, 'B'], [26.5, 'G']] },
  U: { holds: [['B', 3.2, 5.0], ['C', 9.8, 13.6], ['E', 17.4, 21.0], ['G', 25.6, 27.2]], finds: [[4.0, 'B'], [26.5, 'G']], missed: ['A', 'D'] } };
const NS = 'http://www.w3.org/2000/svg';
function setup(id, key) {
  const svg = document.getElementById(id), g = svg.querySelector('.route-line').parentNode, paths = [...g.querySelectorAll('path')].filter(p => !p.classList.contains('chev'));
  // paths: 0 white underlay (return), 1 dashed (return), 2 white underlay (route), 3 route-line
  paths[0].style.display = paths[1].style.display = 'none';
  const route = paths[3], under = paths[2], len = route.getTotalLength();
  [route, under].forEach(p => { p.removeAttribute('pathLength'); p.style.strokeDasharray = len + ' ' + len; });
  const marks = {}; svg.querySelectorAll('.mk[data-id]').forEach(m => { const c = m.querySelector('circle'); marks[m.dataset.id] = { el: m, x: +c.getAttribute('cx'), y: +c.getAttribute('cy') }; m.style.opacity = 0; });
  // path length at each stop: first point after the previous stop that comes within 3 units of the marker
  const N = 1400, pts = [...Array(N + 1)].map((_, i) => { const p = route.getPointAtLength(len * i / N); return [p.x, p.y, len * i / N]; });
  let from = 0; const at = {};
  for (const [id] of PLAN[key].holds) { let best = null, bd = 1e9; for (let i = from; i <= N; i++) { const d = Math.hypot(pts[i][0] - marks[id].x, pts[i][1] - marks[id].y); if (d < bd) { bd = d; best = i; } if (bd < 2 && d > 25) break; } at[id] = pts[best][2]; from = best; }
  const keys = [[0, 0]]; for (const [id, a, b] of PLAN[key].holds) keys.push([a, at[id]], [b, at[id]]); keys.push([30, len]);
  const dot = document.createElementNS(NS, 'circle'); dot.setAttribute('r', 7); dot.setAttribute('class', 'dot'); svg.appendChild(dot);
  const finds = PLAN[key].finds.map(([m, id], i) => { const c = document.createElementNS(NS, 'circle'); c.setAttribute('class', 'find');
    const k = PLAN[key].finds.slice(0, i).filter(f => f[1] === id).length; const a = -0.6 + k * 1.15;
    c.setAttribute('cx', marks[id].x + 19 * Math.cos(a)); c.setAttribute('cy', marks[id].y + 19 * Math.sin(a)); c.setAttribute('r', 0); svg.appendChild(c); return { m, c }; });
  const miss = (PLAN[key].missed || []).map(id => { const poly = [...svg.querySelectorAll('g')].find(gg => (gg.querySelector('title') || {}).textContent?.startsWith('Block ' + id + ','));
    const pg = poly.querySelector('polygon').cloneNode(); pg.setAttribute('class', 'missblk'); pg.removeAttribute('style'); pg.style.opacity = 0; svg.appendChild(pg); return pg; });
  const plus = finds.map(f => { const tx = document.createElementNS(NS, 'text'); tx.setAttribute('class', 'plus'); tx.textContent = '+1';
    tx.setAttribute('x', f.c.getAttribute('cx')); tx.setAttribute('y', +f.c.getAttribute('cy') - 12); tx.style.opacity = 0; svg.appendChild(tx); return tx; });
  return { route, under, len, keys, dot, marks, finds, miss, plus };
}
const S = { U: setup('svgU', 'U'), R: setup('svgR', 'R') };
function lenAt(keys, m) { for (let i = 1; i < keys.length; i++) if (m <= keys[i][0]) { const [a, la] = keys[i - 1], [b, lb] = keys[i]; return la + (lb - la) * sm((m - a) / (b - a || 1)); } return keys[keys.length - 1][1]; }
function runSide(k, m, t, tStart, dur) {
  const s = S[k], L = lenAt(s.keys, m), off = s.len - L;
  s.route.style.strokeDashoffset = off; s.under.style.strokeDashoffset = off;
  const p = s.route.getPointAtLength(Math.max(0.01, L)); s.dot.setAttribute('cx', p.x); s.dot.setAttribute('cy', p.y);
  for (const [id, mk] of Object.entries(s.marks)) { const h = PLAN[k].holds.find(h => h[0] === id); mk.el.style.opacity = h && m >= h[1] - 0.3 ? 1 : 0; }
  let n = 0, last = 99; s.finds.forEach((f, i) => { const age = (m - f.m) * dur / 30; const r = age < 0 ? 0 : 8.5 * (age < 0.18 ? 1.5 * age / 0.18 : 1 + 0.5 * Math.max(0, 1 - (age - 0.18) / 0.25));
    f.c.setAttribute('r', r); const pl = s.plus[i]; pl.style.opacity = age < 0 ? 0 : Math.max(0, 1 - age / 0.7); pl.setAttribute('transform', `translate(0 ${-Math.max(0, age) * 26})`);
    if (age >= 0) { n++; last = Math.min(last, age); } });
  return { n, last };
}
const $ = id => document.getElementById(id);
window.renderAt = t => {
  document.body.style.opacity = sm(t / 0.6);
  const intro = 1 - sm((t - (P.T0 - 0.9)) / 0.5); $('intro').style.opacity = intro;
  ['clock', 'title', 'score'].forEach(i => $(i).style.opacity = (1 - intro) * (1 - sm((t - P.SB) / 0.4)));
  // phase: usual run, then rewind, then KokoShield run
  let k, m;
  if (t < P.RW) { k = 'U'; m = 30 * Math.min(1, Math.max(0, (t - P.T0) / P.DU)); }
  else if (t < P.K0) { k = 'U'; m = 30 * (1 - sm((t - P.RW) / (P.K0 - P.RW - 0.1))); }
  else { k = 'K'; m = 30 * Math.min(1, Math.max(0, (t - P.K0) / P.DK)); }
  const sw = sm((t - (P.K0 - 0.25)) / 0.3);   // swap overlays at the end of the rewind
  $('FU').style.opacity = 1 - sw; $('FK').style.opacity = sw;
  $('min').textContent = Math.round(m); $('bar').firstChild.style.width = (m / 30 * 100) + '%';
  $('bar').firstChild.style.background = k === 'K' ? '#5fc095' : '#c9b37a';
  const r = runSide(k === 'K' ? 'R' : 'U', m, t, 0, k === 'K' ? P.DK : P.DU);
  if (k === 'K') { S.U.dot.style.opacity = 0; S.R.dot.style.opacity = 1; } else { S.U.dot.style.opacity = t > P.T0 - 0.4 ? 1 : 0; S.R.dot.style.opacity = 0; }
  $('cnt').textContent = r.n; $('cnt').style.transform = `scale(${1 + 0.28 * Math.exp(-r.last * 7)})`;
  $('tname').textContent = k === 'K' ? 'KokoShield route' : 'Usual round'; $('tsub').textContent = k === 'K' ? 'Ranked by rain and past records' : "The farmer's normal order";
  $('tname').style.color = k === 'K' ? '#8fe3b8' : '#fff';
  const rw = t >= P.RW && t < P.K0; $('big').style.filter = rw ? `saturate(${0.4}) brightness(.85)` : 'none';
  const pulse = 0.55 + 0.45 * Math.sin((t - P.MISS) * 7), showMiss = t > P.MISS && t < P.RW;
  S.U.miss.forEach(pg => { pg.style.opacity = showMiss ? 1 : 0; pg.style.fill = 'rgba(224,83,58,' + (0.18 + 0.25 * pulse) + ')'; });
  $('miss').textContent = showMiss ? 'Missed 2 sick blocks (A, D)' : (k === 'K' && t > P.NONE ? 'Missed none' : '');
  $('miss').style.color = k === 'K' ? '#8fe3b8' : '#ffb3a1';
  const b = sm((t - P.SB) / 0.45); $('board').style.opacity = b; $('big').style.opacity = 1 - 0.75 * b;
  $('board').style.transform = `scale(${0.94 + 0.06 * b})`;
  return true;
};
window.KS_READY = document.fonts.ready.then(() => true);
</script></body></html>"""
html = html.replace("PARAMS", json.dumps(P)).replace("USUAL", svg("map_usual.svg", "svgU")).replace("RANKED", svg("map_ranked.svg", "svgR"))
(HERE / "race.html").write_text(html, encoding="utf-8"); print("params", P)

PORT = 8792; srv = None
if socket.socket().connect_ex(("127.0.0.1", PORT)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"], cwd=V6, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
preview = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]] if "--preview" in sys.argv else None
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1920, "height": 1080}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(f"http://127.0.0.1:{PORT}/race/race.html"); pg.evaluate("window.KS_READY"); pg.wait_for_timeout(500)
    if preview:
        for t in preview: pg.evaluate(f"window.renderAt({t})"); pg.screenshot(path=str(HERE / f"preview_{t:05.2f}.jpg"), type="jpeg", quality=85)
    else:
        n = int(P["END"] * FPS)
        enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-", "-vf", "format=yuv420p",
                                "-c:v", "libx264", "-preset", "medium", "-crf", "14", str(V6 / "rec/race.mp4")], stdin=subprocess.PIPE)
        for i in range(n): pg.evaluate(f"window.renderAt({i / FPS})"); enc.stdin.write(pg.screenshot(type="jpeg", quality=93))
        enc.stdin.close(); enc.wait(); print("frames", n)
    print("errors", errs[:3]); b.close()
if srv: srv.terminate()
