/* ================= KokoShield cinematic pitch (v5): four acts ================= */
/* Act boundaries: 1 Storm & crisis (S[0]-S[2]), 2 Activation (S[2]-S[5]), 3 Race (S[5]-S[7]), 4 Vision & ask (S[7]-END). */
const AI = (txt) => `<div class="aitag">${txt}</div>`;   /* placeholder tag for AI clips still to be generated */

/* ---------- ACT 1: storm and crisis (cold, dark) ---------- */
const COLD = 'saturate(.55) brightness(.62) contrast(1.15) hue-rotate(-8deg)';
shot('18_rain.jpg', -0.2, 4.3, [1.12, 0, 0], [1.28, -2, 1], COLD);
shot('13_black_pod.jpg', 3.9, 8.6, [1.02, 0, 0], [1.2, -5, -4], 'saturate(.7) brightness(.66) contrast(1.15)', '50% 43%');
shot('19_rain.jpg', 8.2, S[1] + 0.5, [1.1, 0, 0], [1.2, 2, 0], COLD);
shot('14_farmer.jpg', S[1] + 0.1, at(1, 7.0), [1.04, 0, 0], [1.16, -2, 1], 'saturate(.6) brightness(.6) contrast(1.12)', '50% 35%',
  AI('Live-action clip to be generated: the farmer steps out after the storm'));
shot('06_farm.jpg', at(1, 6.6), S[2] + 0.5, [1.12, 0, 0], [1.26, -3, -2], 'saturate(.55) brightness(.5) contrast(1.15) blur(1px)');
/* ---------- ACT 2: activation (the glow) ---------- */
shot('02_hook_close.jpg', S[2] - 0.2, S[3] + 0.5, [1.18, 0, 0], [1.3, 0, 0], 'brightness(.3) blur(8px) saturate(.7)');
shot('06_farm.jpg', S[3] + 0.1, at(3, 6.2), [1.1, 0, 0], [1.2, 0, 0], 'brightness(.35) blur(6px) saturate(.8)');
shot('16_farmer.jpg', at(3, 11.5), S[4] + 0.4, [1.04, 0, 0], [1.14, 2, 0], 'brightness(.7) saturate(.9)', '50% 30%',
  AI('Live-action clip to be generated: he reads the route, decides, and walks in'));
/* ---------- ACT 3: the race (warming) ---------- */
shot('06_farm.jpg', S[5] - 0.2, S[6] + 0.4, [1.1, 0, 0], [1.18, 0, 0], 'brightness(.32) blur(8px)');
shot('12_black_pod.jpg', S[6] - 0.2, at(6, 5.6), [1.0, 0, 0], [1.14, -3, 0], 'brightness(.85) saturate(1.05)', '50% 40%',
  AI('Live-action clip to be generated: minute 7, the find'));
shot('19_rain.jpg', at(6, 5.2), S[7] + 0.4, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.3) blur(8px)');
/* ---------- ACT 4: vision (golden) ---------- */
const GOLD = 'sepia(.25) saturate(1.2) brightness(.9) contrast(1.05)';
shot('01_hook_close.jpg', S[7] - 0.2, at(7, 4.4), [1.22, -2, -1], [1.06, 0, 0], GOLD);
shot('15_farmer.jpg', at(7, 4.0), at(7, 8.4), [1.04, 0, 0], [1.12, 0, -2], GOLD, '50% 30%');
shot('22_rice.jpg', at(7, 8.0), S[8] + 0.6, [1.04, 0, 0], [1.14, 2, 0], GOLD);
shot('02_hook_close.jpg', S[8] + 0.2, END + 1, [1.2, -2, -1], [1.04, 0, 0], GOLD);

/* ---------- ACT 1 overlays ---------- */
ov(`<div class="kick">GSC 2026–27 · Food Resilience</div><div class="h1" style="font-size:66px">Black pod is driven by rain.</div><div class="big" style="font-size:112px;color:#ff8a66;margin-top:12px" id="loss">0%</div><div class="lbl" style="color:#e6cfc7">of the world's cocoa destroyed every year <span style="color:#9a8c86">(Guest 2007)</span></div>`,
  'left:70px;top:230px;width:860px', 4.6, S[1] - 0.3, 'left', 'glass dark');
ov(`<div style="display:flex;align-items:center;gap:22px"><svg width="110" height="110" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="10"/><circle id="clk1" cx="50" cy="50" r="44" fill="none" stroke="#ff8a66" stroke-width="10" stroke-dasharray="276.5" stroke-dashoffset="0" transform="rotate(-90 50 50)" stroke-linecap="round"/></svg><div><div style="font-size:70px;font-weight:800;color:#ff8a66;line-height:1" id="tmin">30:00</div><div class="lbl" style="color:#e6cfc7">to scout the whole farm</div></div></div>`,
  'left:70px;top:150px', at(1, 1.0), S[2] - 0.3, 'left', 'glass dark');
ov(`<div class="h2" style="font-size:40px">Which block first?</div><div class="lbl" style="color:#e6cfc7;margin-top:8px">Memory and habit. Nothing else.</div>`,
  'left:70px;top:420px;width:620px', at(1, 6.0), S[2] - 0.3, 'left', 'glass dark');
const qblocks = ['A', 'B', 'C', 'D', 'E', 'G', 'H'].map((k, i) => ov(`<span class="chip" style="background:rgba(10,20,16,.85);color:#fff;font-size:30px;border:2px solid rgba(255,255,255,.25)">${k}?</span>`,
  `left:${1000 + (i % 4) * 190}px;top:${300 + Math.floor(i / 4) * 150 + (i % 2) * 40}px`, at(1, 6.4 + i * 0.25), S[2] - 0.3, 'up'));

/* ---------- ACT 2: activation + hologram ---------- */
ov(`<div style="text-align:center"><div style="font-size:26px;letter-spacing:.2em;color:#9fe0bf;font-weight:800">24 H RAINFALL</div><div style="display:flex;align-items:baseline;justify-content:center;gap:14px"><span id="mm2" class="big" style="font-size:150px;color:#7fd4ff;text-shadow:0 0 40px rgba(127,212,255,.6)">0</span><span style="font-size:44px;font-weight:800;color:#7fd4ff">mm</span></div>
<div style="position:relative;height:14px;background:rgba(255,255,255,.12);border-radius:8px;width:560px;margin:10px auto"><div id="mmbar2" style="height:100%;width:0;background:#7fd4ff;border-radius:8px;box-shadow:0 0 18px #7fd4ff"></div><div style="position:absolute;left:280px;top:-9px;width:4px;height:32px;background:#ff8a66"></div></div>
<div id="trig2" class="lbl" style="color:#cfe6da">Trigger 30 mm</div></div>`, 'left:560px;top:300px;width:800px', S[2] + 0.2, at(2, 9.8), 'fade', 'holo');
ov(`<div style="text-align:center"><div class="h1" style="font-size:78px;color:#fff;text-shadow:0 0 30px rgba(159,224,191,.5)">KokoShield</div><div style="font-size:30px;color:#9fe0bf;font-weight:700;letter-spacing:.08em">WEATHER-GUIDED DISEASE SCOUTING</div><div id="act2" style="margin-top:14px;font-size:34px;font-weight:800;color:#7fd4ff;opacity:0">● SYSTEM ACTIVE</div></div>`,
  'left:460px;top:160px;width:1000px', at(2, 3.6), S[3] - 0.3, 'fade', 'holo');
/* hologram: the real Field Desk screens floating with scanlines + the drone sweep over the app map with wet blocks */
ov(`<div class="holoframe"><img src="assets/app_plan_route.jpg" alt=""><div class="scan"></div></div>`, 'left:150px;top:150px', at(3, 8.2), at(3, 11.0), 'up', '', 'KokoShield Field Desk prototype (demo data)');
const WATER2 = { A: [[118, 104, 34, 18], [160, 70, 20, 12]], D: [[118, 222, 40, 20], [158, 245, 18, 10]], G: [[150, 312, 36, 14], [222, 302, 22, 10]] };
const SWEEP = [[40, 42], [610, 42], [610, 130], [40, 130], [40, 218], [610, 218], [610, 306], [40, 306]];
const sweepLen = SWEEP.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - SWEEP[i][0], p[1] - SWEEP[i][1]), 0);
ov(`<div class="holomap">${mapSVG('hm', 'priority', `<polyline id="sw" points="${SWEEP.map(p => p.join(',')).join(' ')}" fill="none" stroke="#7fd4ff" stroke-width="2.5" stroke-dasharray="${sweepLen}" stroke-dashoffset="${sweepLen}" opacity=".8"/>
  ${Object.entries(WATER2).map(([k, bl]) => `<g id="hw${k}" clip-path="url(#hm-c${k})" opacity="0">${bl.map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#7fd4ff" opacity=".75"/>`).join('')}</g>`).join('')}
  ${['A', 'D', 'G'].map(k => `<g id="hs${k}" opacity="0"><rect x="${WATER2[k][0][0] - 46}" y="${WATER2[k][0][1] - 40}" width="92" height="22" rx="7" fill="#1f6fb8"/><text x="${WATER2[k][0][0]}" y="${WATER2[k][0][1] - 25}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">STANDING WATER</text></g>`).join('')}
  <polyline id="hr" points="42,336 137,93 185,300 133,205 294,87" fill="none" stroke="#9fe0bf" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900"/>
  ${[['A', 137, 93, 1], ['G', 185, 300, 2], ['D', 133, 205, 3], ['B', 294, 87, 4]].map(([k, x, y, n]) => `<g id="hn${n}" opacity="0"><circle cx="${x}" cy="${y}" r="13" fill="#17201C" stroke="#9fe0bf" stroke-width="2.5"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">${n}</text></g>`).join('')}
  <g id="hd" transform="translate(40 42)">${DRONE}</g>`)}<div class="scan"></div></div>`, 'left:150px;top:150px', at(3, 0.6), at(3, 11.0), 'fade');
ov(`<div class="kick">Inputs</div>${[['Drone: standing water', 'A · D · G', 1.2], ['Rain gauge', '48 mm / 24 h', 2.2], ['Block drainage', 'slow in A, D, G', 3.2], ['Past confirmed cases', 'A · B', 4.2]].map(([a, b, d], i) => `<div class="row" id="in${i}" style="opacity:0"><div class="num" style="background:#1f6fb8">✓</div><div style="flex:1;font-size:24px;font-weight:700">${a}</div><div style="font-size:22px;color:#9fe0bf;font-weight:800">${b}</div></div>`).join('')}
<div id="out2" style="opacity:0;border-top:2px solid rgba(255,255,255,.2);padding-top:12px;margin-top:6px"><div class="kick" style="color:#7fd4ff">Output · 30-minute priority route</div><div class="h2" style="font-size:38px">A → G → D → B</div><div class="lbl" style="color:#cfe6da">Computed in seconds. Reason beside every stop.</div></div>`,
  'left:1230px;top:150px;width:620px', at(3, 0.9), at(3, 11.0), 'right', 'glass');
ov(`<div class="h2" style="font-size:44px">Blocks A and G first.</div><div class="lbl" style="color:#cfe6da;margin-top:6px">He goes.</div>`, 'left:70px;top:150px;width:620px', at(3, 12.0), S[4] - 0.3, 'left', 'glass');


/* ---------- ACT 2b: Field Node 3D (real CAD model, turntable + explode) ---------- */
shot('06_farm.jpg', S[4] - 0.2, S[5] + 0.4, [1.12, 0, 0], [1.2, 0, 0], 'brightness(.28) blur(8px) saturate(.7)');
const n3d = ov(`<img id="n3d" src="assets/node3d/f0000.png" style="width:1100px;height:800px;display:block">`, 'left:80px;top:140px', S[4] + 0.2, S[5] - 0.2, 'fade', '', 'KokoShield Field Node CAD model (concept, not yet built)');
const N3D = Array.from({ length: 210 }, (_, i) => { const im = new Image(); im.src = `assets/node3d/f${String(i).padStart(4, '0')}.png`; return im; });
ov(`<div class="kick">Field Node · CAD concept</div><div class="h2" style="font-size:40px">Local sensor at block level</div>
${[['Ventilated hood', 'air temperature + humidity sensor', 1.8], ['Enclosure', '86 × 62 × 32 mm, 3D-printed', 2.6], ['Controller envelope', 'ESP32-class board', 3.4], ['Status', 'concept · not yet field-tested', 4.4]].map(([a, b, d], i) => `<div class="row" id="nc${i}" style="opacity:0"><div class="num" style="background:#1f6fb8">${i + 1}</div><div><div style="font-size:26px;font-weight:800">${a}</div><div style="font-size:21px;color:#cfe6da">${b}</div></div></div>`).join('')}`,
  'left:1230px;top:200px;width:620px', S[4] + 0.6, S[5] - 0.3, 'right', 'glass');

/* ---------- ACT 3: split-screen race ---------- */
const PLAN_R = [['A', 7, 3], ['G', 7, 2], ['D', 8, 1], ['B', 8, 1]], PLAN_U = [['B', 8, 1], ['C', 7, 0], ['E', 8, 0], ['G', 7, 1]];
const WP = { gate: [42, 336], A: [137, 93], G: [185, 300], D: [133, 205], B: [294, 87], C: [462, 98], E: [307, 205] };
function walk2(plan, min) {
  let t0 = 0, prev = WP.gate, finds = 0, first = null, tr = 0, total = 0; const segs = []; { let p = WP.gate; for (const [k] of plan) { const l = Math.hypot(WP[k][0] - p[0], WP[k][1] - p[1]); segs.push(l); total += l; p = WP[k]; } }
  for (let i = 0; i < plan.length; i++) { const [k, m, f] = plan[i], c = WP[k], tw = m * 0.35;
    if (min < t0 + m) { const u = min - t0; if (u < tw) { const a = sm(u / tw); return { pos: [lerp(prev[0], c[0], a), lerp(prev[1], c[1], a)], finds, first, trail: (tr + segs[i] * a) / total }; }
      const ph = (u - tw) / (m - tw) * Math.PI * 2; return { pos: [c[0] + Math.sin(ph) * 14, c[1] + Math.cos(ph) * 9 - 9], finds, first, trail: (tr + segs[i]) / total }; }
    t0 += m; finds += f; if (f && first === null) first = t0; tr += segs[i]; prev = c; }
  return { pos: prev, finds, first, trail: 1 };
}
const plen = pts => pts.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
const rPts = p => [WP.gate, ...p.map(x => WP[x[0]])]; const LR = plen(rPts(PLAN_R)), LU = plen(rPts(PLAN_U));
const raceT0 = at(5, 1.0), raceT1 = at(5, 10.2), raceMin = t => 30 * ramp(t, raceT0, raceT1);
function half(id, title, col, plan, photo, grade) {
  const L = plen(rPts(plan));
  return `<div class="half" id="${id}"><img src="${PH}${photo}" style="filter:${grade}"><div class="hmap">${mapSVG(id + 'm', 'priority', `<polyline id="${id}tr" points="${rPts(plan).map(p => p.join(',')).join(' ')}" fill="none" stroke="${col}" stroke-width="5" stroke-linecap="round" stroke-dasharray="${L}" stroke-dashoffset="${L}"/><g id="${id}sc"><circle r="16" fill="${col}" opacity=".3"/><circle r="10" fill="${col}" stroke="#fff" stroke-width="3"/></g>`)}</div>
   <div class="hhead" style="border-color:${col}"><div style="font-size:26px;font-weight:800">${title}</div><div style="font-size:20px;color:#cfe6da" id="${id}f">First find —</div></div>
   <div class="hscore" style="color:${col}"><span id="${id}n">0</span><small>confirmed</small></div></div>`;
}
ov(`<div class="split">${half('hu', 'Usual round · B → C → E → G', '#8ea4b8', PLAN_U, '06_farm.jpg', 'saturate(.4) brightness(.5)')}${half('hr2', 'KokoShield route · A → G → D → B', '#3fe08f', PLAN_R, '13_black_pod.jpg', 'saturate(1.05) brightness(.8)')}
  <div class="vs"><div id="clk3" style="font-size:54px;font-weight:800;color:#fff">0:00</div><div style="font-size:18px;color:#cfe6da">of 30 min · same time</div></div></div>`, 'left:0;top:0', S[5] + 0.2, S[6] - 0.2, 'fade', '', 'Demo simulation on the Field Desk map · prototype preset findings');
ov(`<div class="kick">Minute 7 · Block A</div><div class="h2" style="font-size:40px">Brown lesions. Logged for review.</div>`, 'left:70px;top:150px;width:760px', at(6, 0.4), at(6, 5.4), 'left', 'glass');
ov(`<div class="phone"><div class="scr"><img src="assets/g_mobile_log.jpg" alt=""><div id="lock" style="position:absolute;left:28px;top:150px;width:276px;height:120px;border:4px solid #3fe08f;border-radius:12px;opacity:0;box-shadow:0 0 24px #3fe08f"></div></div></div>`, 'right:120px;top:150px', at(6, 1.2), at(6, 5.6), 'right');
ov(`<div class="holoframe" style="width:1240px"><img src="assets/app_log_reviewed.jpg" alt=""><div class="scan"></div></div>`, 'left:340px;top:150px', at(6, 5.2), S[7] - 0.3, 'up', '', 'KokoShield Field Desk prototype (demo data)');
ov(`<span class="chip" style="background:#2B654F;color:#fff;font-size:24px;box-shadow:0 8px 20px rgba(0,0,0,.3)">Treat only block A · the rest of the farm stays clean</span>`, 'left:560px;top:40px', at(6, 7.0), S[7] - 0.3, 'up');

/* ---------- ACT 4: vision and ask ---------- */
ov(`<div class="kick">Sustainable impact</div>${[['Fewer pods lost', 'to a climate-driven disease'], ['Higher smallholder income', 'and food systems that hold'], ['SDG 2.3 · 2.4 · 13.1', 'income, resilient farming, adaptation']].map(([a, b], i) => `<div class="row" id="vi${i}" style="opacity:0"><div class="num">✓</div><div><div style="font-size:30px;font-weight:800">${a}</div><div style="font-size:21px;color:#cfe6da">${b}</div></div></div>`).join('')}`,
  'left:70px;top:150px;width:760px', at(7, 2.6), at(7, 8.6), 'left', 'glass');
ov(`<div class="kick">Cross-crop</div><div class="h2" style="font-size:40px">Rice blast · China</div><div class="lbl" style="color:#cfe6da;margin-top:6px">Same route planner, new crop profile already in the prototype.</div>`, 'left:70px;top:150px;width:720px', at(7, 8.8), S[8] - 0.3, 'left', 'glass');
ov(`<div class="phone" style="width:300px;height:620px"><div class="scr"><img src="assets/g_mobile_plan.jpg" alt=""></div></div>`, 'right:140px;top:200px', at(7, 9.2), S[8] - 0.3, 'right');
ov(`<div style="text-align:center"><div class="kick" style="font-size:24px">The ask</div><div class="h1" style="font-size:78px;color:#fff">RM 1,200</div><div class="lbl" style="color:#cfe6da;font-size:28px;margin-top:8px">to complete the first single-farm pilot:<br>four paired post-rain rounds, one adviser, one Malaysian cocoa farm</div></div>`,
  'left:410px;top:230px;width:1100px', at(8, 0.6), at(8, 9.6), 'up', 'glass');
ov(`<div style="width:1920px;height:1080px;background:#0f2a20;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center">
  <svg width="130" height="146" viewBox="0 0 34 38"><path d="M17 2 31 7v11c0 9-6 15-14 18C9 33 3 27 3 18V7z" fill="#2B654F" stroke="#9fe0bf" stroke-width="1"/><path d="M17 11c-4 3-6 7-5 12 4 0 7-3 8-7 1 4 0 8-3 11" stroke="#9fe0bf" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>
  <div style="font-size:70px;font-weight:800;margin-top:18px">KokoShield</div><div style="font-size:30px;color:#9fe0bf;margin-top:6px">Find disease sooner after the rain.</div>
  <div style="font-size:22px;color:#cfe6da;margin-top:26px">Universiti Malaya · GSC 2026–27 · Food Resilience</div>
  <div style="font-size:16px;color:#a9c3b7;margin-top:40px;max-width:1300px;line-height:1.5">Photos: Isabell Schulz (CC BY-SA 2.0), Scot Nelson (CC0), USAID Indonesia (public domain), Irene Scott/AusAID (CC BY 2.0), Amizhthamathi Ponnuswamy (CC BY-SA 4.0), James Mann (CC BY 2.0), Nico (CC0), GPhoto15 (CC BY 4.0), via Wikimedia Commons. App screens and map: KokoShield prototype, demo data. Drone survey, route race and counts: demo simulation. Voice: AI-generated.</div></div>`,
  'left:0;top:0', at(8, 9.4), END + 5, 'fade');

/* ---------- per-frame ---------- */
const rainAt = t => Math.max(Math.min(ramp(t, 0, 1.0), 1 - ramp(t, S[1] + 0.2, S[1] + 2.2)), 0.35 * Math.min(ramp(t, S[1] + 2.0, S[1] + 3), 1 - ramp(t, S[2] - 1.2, S[2] - 0.3)));
const FLASHES = [1.6, 3.4, 9.6];
const flashAt = t => { let v = 0; for (const f of FLASHES) { const d = t - f; v = Math.max(v, 0.85 * Math.exp(-((d / 0.045) ** 2)), 0.55 * Math.exp(-(((d - 0.17) / 0.05) ** 2)), 0.25 * Math.exp(-(((d - 0.32) / 0.08) ** 2))); } return v; };
function along(pts, f) { let L = 0; const segs = pts.slice(1).map((p, i) => { const l = Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]); L += l; return l; }); let d = clamp(f) * L;
  for (let i = 0; i < segs.length; i++) { if (d <= segs[i]) { const k = segs[i] ? d / segs[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k), Math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])]; } d -= segs[i]; }
  const p = pts[pts.length - 1]; return [p[0], p[1], 0]; }
function update(t) {
  for (const s of SHOTS) { const v = vis(t, s.t0, s.t1, 0.6, 0.6); if (v <= 0.001) { s.el.style.display = 'none'; continue; }
    s.el.style.display = 'block'; s.el.style.opacity = v; const k = sm((t - s.t0) / (s.t1 - s.t0));
    s.el.style.transform = `scale(${lerp(s.from[0], s.to[0], k)}) translate(${lerp(s.from[1], s.to[1], k)}%, ${lerp(s.from[2], s.to[2], k)}%)`; }
  drawRain(t, rainAt(t)); const fl = flashAt(t); $('#flash').style.opacity = (fl * 0.65).toFixed(3);
  const cold = Math.min(1, 1 - ramp(t, S[2] - 0.5, S[2] + 1)); $('#vig').style.opacity = 0.6 + 0.4 * cold;
  let credit = ''; for (const s of SHOTS) if (s.el.style.display === 'block' && +s.el.style.opacity > 0.5 && s.credit) credit = s.credit;
  for (const o of OV) {
    let v = o.fx === 'none' ? ((t >= o.tin && t <= o.tout) ? 1 : 0) : vis(t, o.tin, o.tout);
    if (v <= 0.001) { o.el.style.display = 'none'; continue; }
    o.el.style.display = o.el.dataset.d || 'block'; o.el.style.opacity = v; const k = 1 - v; let tr = '';
    if (o.fx === 'up') tr = `translateY(${k * 50}px)`; else if (o.fx === 'left') tr = `translateX(${-k * 80}px)`; else if (o.fx === 'right') tr = `translateX(${k * 80}px)`;
    if (o === cap) tr = 'translateX(-50%)'; o.el.style.transform = tr;
    if (o.credit && v > 0.5) credit = o.credit;
    if (o.words) o.words.forEach(w => { const a = eo((t - (w._at ?? o.tin) - 0.12 - w._j * 0.05) / 0.4); w.style.opacity = a; w.style.transform = a >= 1 ? '' : `translateY(${(1 - a) * 22}px)`; });
  }
  credEl.textContent = t < END - 2.3 ? credit : ''; credEl.style.display = 'block';
  let si = 0; for (let i = 0; i < S.length - 1; i++) if (t >= S[i]) si = i;
  chap.el.textContent = `Act ${[1, 1, 2, 2, 2, 3, 3, 4, 4][si]} · ${NAMES[si]}`;
  const c = CAPS.find(c => t >= c[0] - 0.05 && t < c[1] + 0.25); cap.el.style.display = c && t < END - 2.3 ? 'block' : 'none'; if (c && cap.el.textContent !== c[2]) cap.el.textContent = c[2];
  prog.style.width = (1920 * clamp(t / END)) + 'px';
  const wipe = $('#wipe'); let wp = -1; for (const k of [2, 5, 7]) if (Math.abs(t - S[k]) < 0.42) wp = (t - S[k] + 0.42) / 0.84;
  if (wp >= 0) { wipe.style.display = 'flex'; wipe.style.transform = `translateX(${-3050 + wp * 5420}px) skewX(-16deg)`; } else wipe.style.display = 'none';
  /* act 1 */
  $('#loss').textContent = t < 7.4 ? Math.round(30 * ramp(t, 5.6, 7.4)) + '%' : '20–30%';
  const left = 30 * 60 * (1 - 0.06 * ramp(t, at(1, 1.0), S[2])); const mm_ = Math.floor(left / 60), ss = Math.floor(left % 60);
  $('#tmin').textContent = `${mm_}:${String(ss).padStart(2, '0')}`; $('#clk1').style.strokeDashoffset = 276.5 * (1 - left / 1800);
  qblocks.forEach((q, i) => { const p = 1 + 0.06 * Math.sin(t * 5 + i); q.el.style.scale = p; });
  /* act 2 */
  const mm2 = 48 * ramp(t, at(2, 0.4), at(2, 2.8)); $('#mm2').textContent = Math.round(mm2); $('#mmbar2').style.width = (560 * Math.min(mm2, 60) / 60) + 'px';
  $('#trig2').innerHTML = mm2 >= 30 ? '<b style="color:#ff8a66">TRIGGER REACHED · 30 mm</b>' : 'Trigger 30 mm';
  $('#act2').style.opacity = ramp(t, at(2, 5.0), at(2, 5.4)) * (0.7 + 0.3 * Math.sin(t * 8));
  const u = t - S[3]; const f1 = sm((u - 0.8) / 2.4);
  const [dx, dy, dang] = along(SWEEP, f1); $('#hd').setAttribute('transform', `translate(${dx} ${dy}) rotate(${dang * 180 / Math.PI + 90}) scale(1.5)`);
  document.querySelectorAll('#hd .blade').forEach((b, i) => b.setAttribute('transform', `rotate(${(t * 2200 + i * 45) % 360})`));
  $('#sw').setAttribute('stroke-dashoffset', sweepLen * (1 - f1));
  ['A', 'D', 'G'].forEach(k => { const a = clamp((f1 - (WATER2[k][0][1] - 20) / 330) * 5); $('#hw' + k).setAttribute('opacity', a * (0.7 + 0.3 * Math.sin(t * 6))); $('#hs' + k).setAttribute('opacity', a); });
  [0, 1, 2, 3].forEach(i => { const a = ramp(u, 1.2 + i, 1.6 + i); const e = $('#in' + i); e.style.opacity = a; e.style.transform = `translateX(${(1 - a) * 30}px)`; });
  $('#hr').setAttribute('stroke-dashoffset', 900 * (1 - ramp(u, 5.6, 7.4)));
  [1, 2, 3, 4].forEach(n => $('#hn' + n).setAttribute('opacity', ramp(u, 5.8 + n * 0.4, 6.1 + n * 0.4)));
  $('#out2').style.opacity = ramp(u, 7.4, 7.9);
  document.querySelectorAll('.holoframe,.holomap').forEach(h => { h.style.transform = `perspective(1600px) rotateY(${-6 + 3 * Math.sin(t * 0.7)}deg) rotateX(${2 * Math.sin(t * 0.5)}deg)`; });
  /* act 2b */
  { const u = t - S[4] - 0.2; const fi = Math.max(0, Math.min(209, Math.round(u * 30))); const im = N3D[fi]; if (im.complete) $('#n3d').src = im.src; }
  [0, 1, 2, 3].forEach(i => { const q = ramp(t, S[4] + [1.8, 2.6, 3.4, 4.4][i], S[4] + [1.8, 2.6, 3.4, 4.4][i] + 0.4); const e = $('#nc' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * 30}px)`; });
  /* act 3 */
  const m = raceMin(t), a = walk2(PLAN_R, m), b = walk2(PLAN_U, m);
  $('#hr2sc').setAttribute('transform', `translate(${a.pos[0]} ${a.pos[1]})`); $('#husc').setAttribute('transform', `translate(${b.pos[0]} ${b.pos[1]})`);
  $('#hr2tr').setAttribute('stroke-dashoffset', LR * (1 - a.trail)); $('#hutr').setAttribute('stroke-dashoffset', LU * (1 - b.trail));
  $('#hr2n').textContent = a.finds; $('#hun').textContent = b.finds; $('#clk3').textContent = `${Math.floor(m)}:${String(Math.floor((m % 1) * 60)).padStart(2, '0')}`;
  $('#hr2f').textContent = a.first ? `First find ${a.first} min` : 'First find —'; $('#huf').textContent = b.first ? `First find ${b.first} min` : 'First find —';
  $('#hr2n').style.scale = 1 + 0.25 * (1 - ramp(t - (a.finds ? 0 : 99), 0, 0.4)) * 0;
  $('#lock').style.opacity = Math.min(ramp(t, at(6, 2.2), at(6, 2.5)), 1) * (0.7 + 0.3 * Math.sin(t * 7));
  /* act 4 */
  [0, 1, 2].forEach(i => { const q = ramp(t, at(7, 3.0 + i * 0.9), at(7, 3.5 + i * 0.9)); const e = $('#vi' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * -30}px)`; });
}
