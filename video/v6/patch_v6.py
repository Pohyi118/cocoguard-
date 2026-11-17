"""Turn the v5 scene file into v6: real prototype footage (laptop + phone), route/race/find matched to the prototype."""
import pathlib, re
p = pathlib.Path("stage/scenes_v5.js"); s = p.read_text(encoding="utf-8")
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70]); s = s.replace(a, b)
def drop_line(prefix):
    global s
    lines = s.split("\n"); hit = [i for i, l in enumerate(lines) if l.startswith(prefix)]; assert len(hit) == 1, (prefix, hit)
    i = hit[0]; j = i
    while not lines[j].rstrip().endswith(";"): j += 1   # statement may wrap
    del lines[i:j + 1]; s = "\n".join(lines)

# ---------- ACT 2: activation -> real Field plan on a laptop ----------
rep("at(2, 9.8), 'fade', 'holo')", "at(2, 5.6), 'fade', 'holo')")
rep("S[3] - 0.3, 'fade', 'holo')", "at(2, 6.4), 'fade', 'holo')")
rep("shot('02_hook_close.jpg', S[2] - 0.2, S[3] + 0.5,", "shot('02_hook_close.jpg', S[2] - 0.2, S[3] + 0.5,")
rep("shot('06_farm.jpg', S[3] + 0.1, at(3, 6.2),", "shot('06_farm.jpg', S[3] + 0.1, S[4] + 0.4,")
drop_line("shot('16_farmer.jpg', at(3, 11.5)")
drop_line("ov(`<div class=\"holoframe\"><img src=\"assets/app_plan_route.jpg\"")
drop_line("ov(`<div class=\"h2\" style=\"font-size:44px\">Blocks A and G first.")
# drone hologram: shorter, route matches the prototype (A -> D -> B -> G)
rep("at(3, 0.6), at(3, 11.0), 'fade')", "at(3, 0.6), at(3, 6.5), 'fade')")
rep("at(3, 0.9), at(3, 11.0), 'right', 'glass')", "at(3, 0.9), at(3, 6.5), 'right', 'glass')")
rep('points="42,336 137,93 185,300 133,205 294,87"', 'points="42,336 137,93 133,205 294,87 185,300"')
rep("[['A', 137, 93, 1], ['G', 185, 300, 2], ['D', 133, 205, 3], ['B', 294, 87, 4]]", "[['A', 137, 93, 1], ['D', 133, 205, 2], ['B', 294, 87, 3], ['G', 185, 300, 4]]")
rep("A → G → D → B</div>", "A → D → B → G</div>")
rep("[0, 1, 2, 3].forEach(i => { const a = ramp(u, 1.2 + i, 1.6 + i);", "[0, 1, 2, 3].forEach(i => { const a = ramp(u, 1.1 + i * 0.6, 1.4 + i * 0.6);")
rep("$('#hr').setAttribute('stroke-dashoffset', 900 * (1 - ramp(u, 5.6, 7.4)));", "$('#hr').setAttribute('stroke-dashoffset', 900 * (1 - ramp(u, 3.6, 5.0)));")
rep("[1, 2, 3, 4].forEach(n => $('#hn' + n).setAttribute('opacity', ramp(u, 5.8 + n * 0.4, 6.1 + n * 0.4)));", "[1, 2, 3, 4].forEach(n => $('#hn' + n).setAttribute('opacity', ramp(u, 3.5 + n * 0.3, 3.8 + n * 0.3)));")
rep("$('#out2').style.opacity = ramp(u, 7.4, 7.9);", "$('#out2').style.opacity = ramp(u, 4.9, 5.3);")

# ---------- ACT 2b: node 3D then the real Sensor node page ----------
rep("'left:80px;top:140px', S[4] + 0.2, S[5] - 0.2, 'fade', ''", "'left:80px;top:140px', S[4] + 0.2, at(4, 7.4), 'fade', ''")
rep("'left:1230px;top:200px;width:620px', S[4] + 0.6, S[5] - 0.3, 'right', 'glass');", "'left:1230px;top:200px;width:620px', S[4] + 0.6, at(4, 7.4), 'right', 'glass');")

# ---------- ACT 3: race matched to the prototype's Compare data ----------
rep("const PLAN_R = [['A', 7, 3], ['G', 7, 2], ['D', 8, 1], ['B', 8, 1]]", "const PLAN_R = [['A', 7, 3], ['D', 8, 2], ['B', 8, 1], ['G', 7, 1]]")
# finds land evenly inside each stop, like the prototype's finds() timeline
s = re.sub(r"function walk2\(plan, min\) \{.*?\n\}\n", lambda m: '''function walk2(plan, min) {
  let t0 = 0, prev = WP.gate, tr = 0, total = 0; const segs = []; { let p = WP.gate; for (const [k] of plan) { const l = Math.hypot(WP[k][0] - p[0], WP[k][1] - p[1]); segs.push(l); total += l; p = WP[k]; } }
  const times = []; { let e = 0; for (const [, m, f] of plan) { for (let q = 1; q <= f; q++) times.push(e + m * q / (f + 1)); e += m; } }
  const finds = times.filter(x => x <= min).length, first = times.length && times[0] <= min ? times[0] : null;
  for (let i = 0; i < plan.length; i++) { const [k, m] = plan[i], c = WP[k], tw = m * 0.25;
    if (min < t0 + m) { const u = min - t0; if (u < tw) { const a = sm(u / tw); return { pos: [lerp(prev[0], c[0], a), lerp(prev[1], c[1], a)], finds, first, trail: (tr + segs[i] * a) / total }; }
      const ph = (u - tw) / (m - tw) * Math.PI * 2; return { pos: [c[0] + Math.sin(ph) * 14, c[1] + Math.cos(ph) * 9 - 9], finds, first, trail: (tr + segs[i]) / total }; }
    t0 += m; tr += segs[i]; prev = c; }
  return { pos: prev, finds, first, trail: 1 };
}
''', s, count=1, flags=re.S)
assert "const times = []" in s
rep("const raceT0 = at(5, 1.0), raceT1 = at(5, 10.2)", "const raceT0 = at(5, 1.0), raceT1 = at(5, 9.6)")
rep("'KokoShield route · A → G → D → B'", "'KokoShield route · A → D → B → G'")
rep("S[5] + 0.2, S[6] - 0.2, 'fade', '', 'Demo simulation on the Field Desk map · prototype preset findings');", "S[5] + 0.2, at(5, 10.3), 'fade', '', 'Demo simulation on the Field Desk map · prototype preset findings');")
rep("$('#hr2f').textContent = a.first ? `First find ${a.first} min` : 'First find —'; $('#huf').textContent = b.first ? `First find ${b.first} min` : 'First find —';",
    "$('#hr2f').textContent = a.first ? `First find ${Math.round(a.first)} min` : 'First find —'; $('#huf').textContent = b.first ? `First find ${Math.round(b.first)} min` : 'First find —';")

# ---------- ACT 3b: the find -> phone Walk screen, then Scout log confirm ----------
rep("shot('12_black_pod.jpg', S[6] - 0.2, at(6, 5.6),", "shot('12_black_pod.jpg', S[6] - 0.2, at(6, 4.0),")
rep("AI('Live-action clip to be generated: minute 7, the find')", "AI('Live-action clip to be generated: minute 2, the find')")
rep("shot('19_rain.jpg', at(6, 5.2), S[7] + 0.4, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.3) blur(8px)');",
    "shot('12_black_pod.jpg', at(6, 3.4), at(6, 9.2), [1.18, 0, 0], [1.26, 0, 0], 'brightness(.32) blur(10px)', '50% 40%');\nshot('06_farm.jpg', at(6, 8.6), S[7] + 0.4, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.3) blur(8px)');")
rep("""ov(`<div class="kick">Minute 7 · Block A</div><div class="h2" style="font-size:40px">Brown lesions. Logged for review.</div>`, 'left:70px;top:150px;width:760px', at(6, 0.4), at(6, 5.4), 'left', 'glass');""",
    """ov(`<div class="kick">Minute 2 · Block A · Stop 1 of 4</div><div class="h2" style="font-size:40px">Dark lesions on the lower pods.</div><div class="lbl" style="color:#cfe6da;margin-top:6px">Logged on the phone, offline, in three taps.</div>`, 'left:70px;top:150px;width:720px', at(6, 0.4), at(6, 8.8), 'left', 'glass');""")
drop_line("ov(`<div class=\"phone\"><div class=\"scr\"><img src=\"assets/g_mobile_log.jpg\"")
drop_line("ov(`<div class=\"holoframe\" style=\"width:1240px\"><img src=\"assets/app_log_reviewed.jpg\"")
rep("Treat only block A · the rest of the farm stays clean</span>`, 'left:560px;top:40px', at(6, 7.0), S[7] - 0.3, 'up');",
    "Adviser confirms · only the affected blocks are treated</span>`, 'left:600px;top:40px', at(6, 10.4), S[7] - 0.3, 'up');")
rep("$('#lock').style.opacity", "void 0; const __lock = 0 && ")   # phone lock-on highlight is gone

# ---------- ACT 4: real rice-blast profile on the phone ----------
rep('<img src="assets/g_mobile_plan.jpg" alt="">', '<img src="assets/rec/rice/f0000.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 0">')

# ---------- real footage clips: laptop / phone frames with camera moves ----------
clips = r'''
/* ================= real prototype footage (recorded frame by frame from prototype/KokoShield_Prototype.html) ================= */
const PEND = []; const RECS = [];
const LAPCSS = 'left:0;top:0;width:1920px;height:1080px';
function rec({ name, n, kind, tin, tout, map, cam = [[0, 1, 720, 450]], at: pos = '', fx = 'fade', credit = 'KokoShield Field Desk prototype · demo farm and demo data' }) {
  const W = kind === 'lap' ? 1440 : 390, H = kind === 'lap' ? 900 : 844;
  const html = kind === 'lap'
    ? `<div class="lapwrap" style="${pos}"><div class="lap"><div class="lscr"><div class="cam" style="width:${W}px;height:${H}px"><img style="width:${W}px;height:${H}px"></div><div class="glare"></div></div></div><div class="deck"></div></div>`
    : `<div class="ph2wrap" style="${pos}"><div class="ph2"><div class="pscr"><div class="cam" style="width:${W}px;height:${H}px"><img style="width:${W}px;height:${H}px"></div><div class="glare"></div></div></div></div>`;
  const o = ov(html, LAPCSS, tin, tout, fx, '', credit);
  const r = { o, name, n, kind, map, cam, W, H, img: o.el.querySelector('img'), camEl: o.el.querySelector('.cam'), dev: o.el.querySelector(kind === 'lap' ? '.lapwrap' : '.ph2wrap'), tin, tout };
  RECS.push(r); return r;
}
function camAt(cam, rt) {
  if (rt <= cam[0][0]) return cam[0].slice(1);
  for (let i = 0; i < cam.length - 1; i++) { const a = cam[i], b = cam[i + 1];
    if (rt <= b[0]) { const k = sm((rt - a[0]) / (b[0] - a[0])); return [lerp(a[1], b[1], k), lerp(a[2], b[2], k), lerp(a[3], b[3], k)]; } }
  return cam[cam.length - 1].slice(1);
}
function updateRecs(t) {
  for (const r of RECS) {
    if (r.o.el.style.display === 'none') continue;
    const rt = Math.max(0, r.map(t)), i = Math.max(0, Math.min(r.n - 1, Math.round(rt * 30)));
    if (r.img.dataset.i !== String(i)) { r.img.dataset.i = i; r.img.src = `assets/rec/${r.name}/f${String(i).padStart(4, '0')}.jpg`; PEND.push(r.img.decode().catch(() => 0)); }
    const [sc, cx, cy] = camAt(r.cam, rt);
    const tx = Math.min(0, Math.max(r.W - r.W * sc, r.W / 2 - cx * sc)), ty = Math.min(0, Math.max(r.H - r.H * sc, r.H / 2 - cy * sc));
    r.camEl.style.transform = `translate(${tx}px,${ty}px) scale(${sc})`;
    const life = (t - r.tin) / Math.max(0.1, r.tout - r.tin);   /* slow cinematic drift of the device itself */
    r.dev.style.transform = r.kind === 'lap'
      ? `translateX(-50%) perspective(2200px) rotateX(${4 - 3 * life}deg) rotateY(${-5 + 6 * life}deg) scale(${0.86 + 0.05 * life})`
      : `translateX(-50%) perspective(1800px) rotateY(${-8 + 10 * life}deg) rotateZ(${-1.5 + 2 * life}deg) scale(${0.98 + 0.04 * life})`;
  }
}
/* Act 2: the alert lands on the real Field plan (rec 0-6.5 s), push to the rain card */
rec({ name: 'plan', n: 522, kind: 'lap', tin: at(2, 6.0), tout: S[3] + 0.25, map: t => t - at(2, 6.0),
  cam: [[0, 1.0, 720, 450], [1.2, 1.0, 720, 450], [3.2, 1.7, 1245, 205], [6.5, 1.75, 1245, 205]] });
/* Act 2: after the drone sweep, the same recording continues (rec 6.5-17.4 s): blocks, usual vs priority, route list, Start scouting */
rec({ name: 'plan', n: 522, kind: 'lap', tin: at(3, 6.0), tout: S[4] + 0.2, map: t => 6.5 + (t - at(3, 6.0)),
  cam: [[6.5, 1.0, 720, 450], [7.3, 1.3, 330, 470], [10.6, 1.3, 330, 470], [11.4, 1.0, 720, 450], [13.1, 1.0, 720, 450], [13.6, 1.55, 1245, 330], [15.0, 1.55, 1245, 330], [15.5, 1.3, 1245, 620], [16.2, 1.0, 720, 450]] });
/* Act 2b: the Field Node in the app (Sensor node page, Assembled -> Exploded) */
rec({ name: 'sensor', n: 84, kind: 'lap', tin: at(4, 7.0), tout: S[5] + 0.2, map: t => t - at(4, 7.0),
  cam: [[0, 1.25, 640, 560], [2.8, 1.35, 640, 560]] });
/* Act 3: race ends on the prototype's own Compare screen */
rec({ name: 'compare', n: 162, kind: 'lap', tin: at(5, 10.0), tout: S[6] + 0.2, map: t => t - at(5, 10.0),
  cam: [[0, 1.0, 720, 450], [1.4, 1.5, 360, 330], [2.6, 1.5, 360, 330], [4.6, 1.35, 720, 560]] });
/* Act 3b: the scout's phone, Walk screen: Found black pod -> 3 pods -> Save -> Stop 2 */
rec({ name: 'walk', n: 180, kind: 'phone', tin: at(6, 3.2), tout: at(6, 9.0), map: t => t - at(6, 3.2), at: 'left:1330px;top:110px',
  cam: [[0, 1.0, 195, 422], [6, 1.0, 195, 422]] });
/* Act 3b: adviser confirms on the Scout log */
rec({ name: 'log', n: 144, kind: 'lap', tin: at(6, 8.6), tout: S[7] + 0.2, map: t => t - at(6, 8.6),
  cam: [[0, 1.0, 720, 450], [0.9, 1.45, 560, 300], [4.8, 1.45, 560, 300]] });
'''
rep("/* ---------- per-frame ---------- */", clips + "\n/* ---------- per-frame ---------- */")
rep("  /* act 3 */\n  const m = raceMin(t)", "  updateRecs(t);\n  /* act 3 */\n  const m = raceMin(t)")
p.write_text(s, encoding="utf-8"); print("scenes v6 patched")

css = pathlib.Path("stage/extra.css"); c = css.read_text(encoding="utf-8")
if ".lapwrap" not in c:
    c += """
.lapwrap{position:absolute;left:50%;top:46px;transform-origin:50% 0}
.lap{width:1468px;padding:14px;background:#0b0e0d;border-radius:24px;box-shadow:0 50px 110px rgba(0,0,0,.65),0 0 0 2px #2c3330 inset,0 0 80px rgba(159,224,191,.10)}
.lscr,.pscr{position:relative;overflow:hidden;background:#fff}
.lscr{width:1440px;height:900px;border-radius:8px}
.deck{width:1640px;height:30px;margin:-2px 0 0 -86px;background:linear-gradient(#4a504d,#202523 70%,#121514);border-radius:2px 2px 26px 26px;box-shadow:0 30px 60px rgba(0,0,0,.6)}
.cam{position:absolute;left:0;top:0;transform-origin:0 0}.cam img{display:block}
.glare{position:absolute;inset:0;pointer-events:none;background:linear-gradient(118deg,rgba(255,255,255,.10) 0%,rgba(255,255,255,0) 38%)}
.ph2wrap{position:absolute;transform-origin:50% 50%}
.ph2{width:414px;padding:12px;background:#0b0e0d;border-radius:58px;box-shadow:0 50px 110px rgba(0,0,0,.65),0 0 0 2px #2c3330 inset}
.pscr{width:390px;height:844px;border-radius:46px}
"""
    css.write_text(c, encoding="utf-8"); print("css added")
