"""Add the drone survey to the interactive 3D page and move its story onto the v4 (9-scene) narration."""
import pathlib
P = pathlib.Path("index.html"); s = P.read_text(encoding="utf-8")
assert "DRONE_SEG" not in s, "already patched"
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)

# --- timeline: v4 story time drives captions/chapters/audio; v3 visuals are reached through a piecewise map ---
rep("const NAMES = ['Hook','Climate risk','Market gap','Solution','Record & confirm','Pilot','Impact & market','Close'];",
"""const NAMES = ['Hook','Climate risk','Market gap','Solution','Record & confirm','Pilot','Impact & market','Close'];
const S4 = window.KS4_STARTS, END4 = S4[9], NAMES4 = window.KS4_NAMES;
const DR = 7.6;   /* drone part of story scene 4, in story seconds */
const SEGS = [[S4[0], S4[1], S[0], S[1]], [S4[1], S4[2], S[1], S[2]], [S4[2], S4[3], S[2], S[3]], [S4[3], S4[3] + DR, null, null],
  [S4[3] + DR, S4[4], S[3] + 0.4, S[3] + 5.6], [S4[4], S4[5], S[3] + 5.6, S[4]], [S4[5], S4[6], S[4], S[5]], [S4[6], S4[7], S[5], S[6]], [S4[7], S4[8], S[6], S[7]], [S4[8], S4[9], S[7], S[8]]];
function m43(t4) { for (const [a, b, c, d] of SEGS) if (t4 >= a && t4 < b) return c === null ? null : c + (t4 - a) / (b - a) * (d - c); return S[8] + (t4 - S4[9]); }
let T4 = 0, DRONE_SEG = false;""")

# --- overlays: hide story cards during the drone sequence; wipes/chapter/captions/progress follow story time ---
rep("  for (const o of OV) {\n    let vis = o.fx === 'none'",
    "  for (const o of OV) {\n    if (DRONE_SEG && o !== brand && o !== chap && o !== cap) { o.el.style.display = 'none'; continue; }\n    let vis = o.fx === 'none'")
rep("  let wp = -1; for (let k = 1; k < 8; k++) if (Math.abs(t - S[k]) < 0.42) wp = (t - S[k] + 0.42) / 0.84;",
    "  let wp = -1; for (let k = 1; k < 9; k++) if (Math.abs(T4 - S4[k]) < 0.42) wp = (T4 - S4[k] + 0.42) / 0.84;")
rep("  const si = Math.max(0, S.findIndex((s, i) => i < 8 && t >= s && t < S[i + 1]));\n  chap.el.textContent = `${si + 1} / 8 · ${NAMES[si]}`;\n  const c = CAPS.find(c => t >= c[0] - 0.05 && t < c[1] + 0.25);",
    "  let si = 0; for (let i = 0; i < 9; i++) if (T4 >= S4[i]) si = i;\n  chap.el.textContent = `${si + 1} / 9 · ${NAMES4[si]}`;\n  const c = CAPS.find(c => T4 >= c[0] - 0.05 && T4 < c[1] + 0.25);")
rep("  prog.style.width = (1920 * clamp(t / END)) + 'px';", "  prog.style.width = (1920 * clamp(T4 / END4)) + 'px';")

# --- drone module + frame driven by story time ---
drone_js = pathlib.Path("drone3d.js").read_text(encoding="utf-8")
rep("/* ---------- render / modes ---------- */", drone_js + "\n/* ---------- render / modes ---------- */")
rep("function frame(tt) { update(tt); if (postUpdate) postUpdate(); if (exploring) controls.update(); renderer.render(scene, camera); }",
    "function frame(t4, fixed3 = null) { T4 = t4; const t3 = fixed3 ?? m43(t4); DRONE_SEG = fixed3 === null && t3 === null; update(DRONE_SEG ? S[3] + 0.45 : t3); droneUpdate(t4, fixed3 !== null); if (postUpdate) postUpdate(); if (exploring) controls.update(); renderer.render(scene, camera); }")

# --- interactive player ---
rep("const audio = new Audio('assets/soundtrack.m4a');", "const audio = new Audio('assets/soundtrack3d.m4a');")
rep("const chipBtns = NAMES.map((n, i) =>", "const chipBtns = NAMES4.map((n, i) =>")
rep("b.onclick = () => { setMode('story'); go(S[i] + 0.05); };", "b.onclick = () => { setMode('story'); go(S4[i] + 0.05); };")
rep("if (t >= END - 0.05) t = 0;", "if (t >= END4 - 0.05) t = 0;")
rep("function go(x) { t = clamp(x, 0, END);", "function go(x) { t = clamp(x, 0, END4);")
rep("    if (!playing) frame(mode === 'challenge' ? CH_T : t);", "    if (!playing) frame(t, mode === 'challenge' ? CH_T : null);")
rep("else if (/^Digit[1-8]$/.test(e.code)) { setMode('story'); go(S[+e.code.slice(5) - 1] + 0.05); }",
    "else if (/^Digit[1-9]$/.test(e.code)) { setMode('story'); go(S4[+e.code.slice(5) - 1] + 0.05); }")
rep("    const hn = mode === 'explore' ? ray.intersectObjects([nodeSpin, post], true)[0] : null;",
    "    const hd = mode === 'explore' && drone.visible ? ray.intersectObjects([drone], true)[0] : null; if (hd) return { drone: true };\n    const hn = mode === 'explore' ? ray.intersectObjects([nodeSpin, post], true)[0] : null;")
rep("  function showInfo(h) {\n    let html;\n    if (h.node) html = ",
    "  const DRONE_INFO = `<div class=\"kick\">Drone survey · concept</div><div class=\"h2\" style=\"font-size:34px;padding-right:60px\">Borrowed UM camera drone</div>\n"
    "      <p class=\"lbl\">Flight 1 maps the farm's blocks at setup. Flight 2, after heavy rain, shows where water is standing, marking the wet blocks that the ranked route checks first. It cannot see black pod under the canopy and does not spray. Flown only with the grower's consent, under current CAAM rules, never in storms.</p>`;\n"
    "  function showInfo(h) {\n    let html;\n    if (h.drone) html = DRONE_INFO;\n    else if (h.node) html = ")
rep("<label class=\"tog\"><input type=\"checkbox\" id=\"chint\"> Show KokoShield's signals</label>",
    "<label class=\"tog\"><input type=\"checkbox\" id=\"chint\"> Fly the drone survey (shows wet blocks and past cases)</label>")
rep("  el('chint').onchange = e => { C2.hint = e.target.checked; };",
    "  el('chint').onchange = e => { C2.hint = e.target.checked; if (C2.hint) C2.dT0 = performance.now(); };")
rep("    hintS.forEach(s => s.material.opacity = C2.hint ? 1 : 0);",
    """    { const nowS = performance.now() / 1000, f = C2.hint ? clamp((performance.now() - C2.dT0) / 4500) : 0;
      if (C2.hint) { const p = alongPath(LAWN3, f); placeDrone(p.pos, p.yaw, f < 1 ? -0.14 : 0, nowS * 40); }
      ['A', 'D', 'G'].forEach((k, i) => { const a = C2.hint ? clamp((f - rowFrac(k)) * 5) : 0; hintS[i].material.opacity = 0; setWater(k, a, nowS); });
      hintS[3].material.opacity = hintS[4].material.opacity = C2.hint ? ramp(f, 0.92, 1) : 0; }""")
rep("        if (t >= END) { t = END; setPlay(false); cta.hidden = false; el('ctaCh').focus(); }",
    "        if (t >= END4) { t = END4; setPlay(false); cta.hidden = false; el('ctaCh').focus(); }")
rep("      const si = Math.max(0, S.findIndex((s, i) => i < 8 && t >= s && t < S[i + 1]));",
    "      let si = 0; for (let i = 0; i < 9; i++) if (t >= S4[i]) si = i;")
rep("      frame(mode === 'challenge' ? CH_T : t);", "      frame(t, mode === 'challenge' ? CH_T : null);")
rep("    renderChallenge(); setPlay(false);", "    seek.max = END4.toFixed(1); renderChallenge(); setPlay(false);")
P.write_text(s, encoding="utf-8")
print("patched", len(s))
