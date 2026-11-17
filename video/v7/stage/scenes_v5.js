/* ================= KokoShield cinematic pitch (v5): four acts ================= */
/* Act boundaries: 1 Storm & crisis (S[0]-S[2]), 2 Activation (S[2]-S[5]), 3 Race (S[5]-S[7]), 4 Vision & ask (S[7]-END). */
const AI = (txt) => `<div class="aitag">${txt}</div>`;   /* placeholder tag for AI clips still to be generated */

/* ---------- real footage (Pexels License clips, cut to 30 fps frame sequences by extract_footage.py) ---------- */
const VFR = {"rain1": 150, "rainleaf": 156, "ghana": 198, "orchard_a": 348, "leafbg": 349, "aerialbg": 486, "orchard_b": 319, "path_a": 319, "podbg": 258, "aerial_v": 144, "path_end": 481}, VCRED = {"rain1": "Video: Nothing Ahead · Pexels", "rainleaf": "Video: Srinivas Kashyap · Pexels", "ghana": "Cocoa farmer, Ghana · Video: Zeal Creative Studios · Pexels", "orchard_a": "Video: Prodèép Nëpalënsis · Pexels", "leafbg": "", "aerialbg": "", "orchard_b": "", "path_a": "", "podbg": "", "aerial_v": "Video: Serg Alesenko · Pexels", "path_end": "Video: Ucundinamarca Virtual · Pexels"};
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

/* ---------- ACT 1 overlays ---------- */
ov(`<div class="kick">GSC 2026–27 · Food Resilience</div><div class="h1" style="font-size:66px">Black pod is driven by rain.</div><div class="big" style="font-size:112px;color:#ff8a66;margin-top:12px" id="loss">0%</div><div class="lbl" style="color:#e6cfc7">of the world's cocoa destroyed every year <span style="color:#9a8c86">(Guest 2007)</span></div>`,
  'left:70px;top:230px;width:860px', 4.6, S[1] - 0.3, 'left', 'glass dark');
ov(`<div style="display:flex;align-items:center;gap:22px"><svg width="110" height="110" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="10"/><circle id="clk1" cx="50" cy="50" r="44" fill="none" stroke="#ff8a66" stroke-width="10" stroke-dasharray="276.5" stroke-dashoffset="0" transform="rotate(-90 50 50)" stroke-linecap="round"/></svg><div><div style="font-size:70px;font-weight:800;color:#ff8a66;line-height:1" id="tmin">30:00</div><div class="lbl" style="color:#e6cfc7">to scout the whole farm</div></div></div>`,
  'left:70px;top:150px', at(1, 1.0), S[2] - 0.3, 'left', 'glass dark');
ov(`<div class="kick" style="color:#ff8a66">The problem</div><div class="h2" style="font-size:38px">Too many blocks, too little time</div>${['Rain spreads black pod within days', 'About 30 minutes to scout after a storm', 'Usual round: the wettest blocks are found late'].map((x, i) => `<div class="row" id="pb${i}" style="opacity:0"><div class="num" style="background:#B0452E">${i + 1}</div><div style="font-size:25px;font-weight:700">${x}</div></div>`).join('')}`,
  'left:70px;top:330px;width:780px', at(1, 1.4), S[2] - 0.3, 'left', 'glass dark');

/* ---------- ACT 2: activation + hologram ---------- */
ov(`<div style="text-align:center"><div style="font-size:26px;letter-spacing:.2em;color:#9fe0bf;font-weight:800">24 H RAINFALL</div><div style="display:flex;align-items:baseline;justify-content:center;gap:14px"><span id="mm2" class="big" style="font-size:150px;color:#7fd4ff;text-shadow:0 0 40px rgba(127,212,255,.6)">0</span><span style="font-size:44px;font-weight:800;color:#7fd4ff">mm</span></div>
<div style="position:relative;height:14px;background:rgba(255,255,255,.12);border-radius:8px;width:560px;margin:10px auto"><div id="mmbar2" style="height:100%;width:0;background:#7fd4ff;border-radius:8px;box-shadow:0 0 18px #7fd4ff"></div><div style="position:absolute;left:280px;top:-9px;width:4px;height:32px;background:#ff8a66"></div></div>
<div id="trig2" class="lbl" style="color:#cfe6da">Trigger 30 mm</div></div>`, 'left:560px;top:300px;width:800px', S[2] + 0.2, at(2, 5.6), 'fade', 'holo');
ov(`<div style="text-align:center"><div class="kick" style="color:#9fe0bf;font-size:24px">The solution</div><div class="h1" style="font-size:78px;color:#fff;text-shadow:0 0 30px rgba(159,224,191,.5)">KokoShield</div><div style="font-size:30px;color:#9fe0bf;font-weight:700;letter-spacing:.08em">WEATHER-GUIDED DISEASE SCOUTING</div><div id="act2" style="margin-top:14px;font-size:34px;font-weight:800;color:#7fd4ff;opacity:0">● SYSTEM ACTIVE</div></div>`,
  'left:460px;top:160px;width:1000px', at(2, 3.6), at(2, 6.4), 'fade', 'holo');
/* hologram: the real Field Desk screens floating with scanlines + the drone sweep over the app map with wet blocks */
const WATER2 = { A: [[118, 104, 34, 18], [160, 70, 20, 12]], D: [[118, 222, 40, 20], [158, 245, 18, 10]], G: [[150, 312, 36, 14], [222, 302, 22, 10]] };
const SWEEP = [[40, 42], [610, 42], [610, 130], [40, 130], [40, 218], [610, 218], [610, 306], [40, 306]];
const sweepLen = SWEEP.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - SWEEP[i][0], p[1] - SWEEP[i][1]), 0);
ov(`<div class="holomap">${mapSVG('hm', 'priority', `<polyline id="sw" points="${SWEEP.map(p => p.join(',')).join(' ')}" fill="none" stroke="#7fd4ff" stroke-width="2.5" stroke-dasharray="${sweepLen}" stroke-dashoffset="${sweepLen}" opacity=".8"/>
  ${Object.entries(WATER2).map(([k, bl]) => `<g id="hw${k}" clip-path="url(#hm-c${k})" opacity="0">${bl.map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#7fd4ff" opacity=".75"/>`).join('')}</g>`).join('')}
  ${['A', 'D', 'G'].map(k => `<g id="hs${k}" opacity="0"><rect x="${WATER2[k][0][0] - 46}" y="${WATER2[k][0][1] - 40}" width="92" height="22" rx="7" fill="#1f6fb8"/><text x="${WATER2[k][0][0]}" y="${WATER2[k][0][1] - 25}" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">STANDING WATER</text></g>`).join('')}
  <polyline id="hr" points="42,336 137,93 133,205 294,87 185,300" fill="none" stroke="#9fe0bf" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900"/>
  ${[['A', 137, 93, 1], ['D', 133, 205, 2], ['B', 294, 87, 3], ['G', 185, 300, 4]].map(([k, x, y, n]) => `<g id="hn${n}" opacity="0"><circle cx="${x}" cy="${y}" r="13" fill="#17201C" stroke="#9fe0bf" stroke-width="2.5"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">${n}</text></g>`).join('')}
  <g id="hd" transform="translate(40 42)">${DRONE}</g>`)}<div class="scan"></div></div>`, 'left:150px;top:150px', at(3, 0.6), at(3, 6.5), 'fade');
ov(`<div class="kick">How it works · inputs</div>${[['Drone: standing water', 'A · D · G', 1.2], ['Rain gauge', '48 mm / 24 h', 2.2], ['Block drainage', 'slow in A, D, G', 3.2], ['Past confirmed cases', 'A · B', 4.2]].map(([a, b, d], i) => `<div class="row" id="in${i}" style="opacity:0"><div class="num" style="background:#1f6fb8">✓</div><div style="flex:1;font-size:24px;font-weight:700">${a}</div><div style="font-size:22px;color:#9fe0bf;font-weight:800">${b}</div></div>`).join('')}
<div id="out2" style="opacity:0;border-top:2px solid rgba(255,255,255,.2);padding-top:12px;margin-top:6px"><div class="kick" style="color:#7fd4ff">Output · 30-minute priority route</div><div class="h2" style="font-size:38px">A → D → B → G</div><div class="lbl" style="color:#cfe6da">Computed in seconds. Reason beside every stop.</div></div>`,
  'left:1230px;top:150px;width:620px', at(3, 0.9), at(3, 6.5), 'right', 'glass');


/* ---------- ACT 2b: Field Node 3D (real CAD model, turntable + explode) ---------- */
shot('06_farm.jpg', S[4] - 0.2, S[5] + 0.4, [1.12, 0, 0], [1.2, 0, 0], 'brightness(.28) blur(8px) saturate(.7)');
const n3d = ov(`<img id="n3d" src="assets/node3d/f0000.png" style="width:1100px;height:800px;display:block">`, 'left:80px;top:140px', S[4] + 0.2, at(4, 7.4), 'fade', '', 'KokoShield Field Node CAD model (concept, not yet built)');
const N3D = Array.from({ length: 210 }, (_, i) => { const im = new Image(); im.src = `assets/node3d/f${String(i).padStart(4, '0')}.png`; return im; });
ov(`<div class="kick">Field Node · CAD concept</div><div class="h2" style="font-size:40px">Local sensor at block level</div>
${[['Ventilated hood', 'air temperature + humidity sensor', 1.8], ['Enclosure', '86 × 62 × 32 mm, 3D-printed', 2.6], ['Controller envelope', 'ESP32-class board', 3.4], ['Status', 'concept · not yet field-tested', 4.4]].map(([a, b, d], i) => `<div class="row" id="nc${i}" style="opacity:0"><div class="num" style="background:#1f6fb8">${i + 1}</div><div><div style="font-size:26px;font-weight:800">${a}</div><div style="font-size:21px;color:#cfe6da">${b}</div></div></div>`).join('')}`,
  'left:1230px;top:200px;width:620px', S[4] + 0.6, at(4, 7.4), 'right', 'glass');

/* ---------- ACT 3: the proof: two real scouts, same 30 minutes, the prototype's aerial map with GPS trails ---------- */
const NODE={gate:[42,336],w1:[46,250],w2:[48,200],m0:[52,148],ma:[120,152],m1:[190,158],mx:[222,146],mb:[255,149],m2:[297,158],me:[330,150],m3:[378,140],m4:[474,168],
 l1:[90,258],l2:[176,281],l3:[228,252],l4:[300,278],gh0:[280,284],gh:[280,300],l5:[402,256],l6:[556,286],vd:[215,200],vf:[392,200],s1:[281,348],s2:[400,346],s3:[547,345],
 eA:[128,134],eB:[300,136],eC:[474,148],eD:[115,174],eE:[300,180],eG:[190,292],eH:[405,280]};
const LINKS='gate-w1 w1-w2 w2-m0 m0-ma ma-m1 m1-mx mx-mb mb-m2 m2-me me-m3 m3-m4 w1-l1 l1-l2 l2-l3 l3-l4 l4-gh0 gh0-gh gh-s1 l4-l5 l5-l6 l6-s3 gate-s1 s1-s2 s2-s3 m1-vd vd-l3 m3-vf vf-l5 ma-eA ma-eD m2-eB m2-eE m4-eC l2-eG l5-eH';
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
    <div class="hhead" style="border-color:${col};top:262px"><div style="font-size:24px;font-weight:800">${title}</div><div style="font-size:19px;color:#cfe6da" id="${id}f">First find —</div></div>
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
ov(`<div class="kick">The find · Block A · minute 2</div><div class="h2" style="font-size:40px">Dark lesions on the lower pods.</div><div class="lbl" style="color:#cfe6da;margin-top:6px">Logged on the phone, offline, in three taps.</div>`, 'left:70px;top:150px;width:720px', at(6, 0.4), at(6, 8.2), 'left', 'glass');
ov(`<span class="chip" style="background:#2B654F;color:#fff;font-size:24px;box-shadow:0 8px 20px rgba(0,0,0,.3)">Adviser confirms · only the affected blocks are treated</span>`, 'left:600px;top:40px', at(6, 10.4), S[7] - 0.3, 'up');

/* ---------- ACT 4: vision and ask ---------- */
ov(`<div class="kick">Sustainable impact</div>${[['Fewer pods lost', 'to a climate-driven disease'], ['Higher smallholder income', 'and food systems that hold'], ['SDG 2.3 · 2.4 · 13.1', 'income, resilient farming, adaptation']].map(([a, b], i) => `<div class="row" id="vi${i}" style="opacity:0"><div class="num">✓</div><div><div style="font-size:30px;font-weight:800">${a}</div><div style="font-size:21px;color:#cfe6da">${b}</div></div></div>`).join('')}`,
  'left:70px;top:150px;width:760px', at(7, 2.6), at(7, 8.6), 'left', 'glass');
ov(`<div class="kick">Cross-crop</div><div class="h2" style="font-size:40px">Rice blast · China</div><div class="lbl" style="color:#cfe6da;margin-top:6px">Same route planner, new crop profile already in the prototype.</div>`, 'left:70px;top:150px;width:720px', at(7, 8.8), S[8] - 0.3, 'left', 'glass');
ov(`<div class="phone" style="width:300px;height:620px"><div class="scr"><img src="assets/rec/rice/f0000.jpg" alt="" style="width:100%;height:100%;object-fit:cover;object-position:50% 0"></div></div>`, 'right:140px;top:200px', at(7, 9.2), S[8] - 0.3, 'right');
ov(`<div style="text-align:center"><div class="kick" style="font-size:24px">The ask</div><div class="h1" style="font-size:78px;color:#fff">RM 1,200</div><div class="lbl" style="color:#cfe6da;font-size:28px;margin-top:8px">to complete the first single-farm pilot:<br>four paired post-rain rounds, one adviser, one Malaysian cocoa farm</div></div>`,
  'left:410px;top:230px;width:1100px', at(8, 0.6), at(8, 9.6), 'up', 'glass');
ov(`<div style="width:1920px;height:1080px;background:#0f2a20;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center">
  <svg width="130" height="146" viewBox="0 0 34 38"><path d="M17 2 31 7v11c0 9-6 15-14 18C9 33 3 27 3 18V7z" fill="#2B654F" stroke="#9fe0bf" stroke-width="1"/><path d="M17 11c-4 3-6 7-5 12 4 0 7-3 8-7 1 4 0 8-3 11" stroke="#9fe0bf" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>
  <div style="font-size:70px;font-weight:800;margin-top:18px">KokoShield</div><div style="font-size:30px;color:#9fe0bf;margin-top:6px">Find disease sooner after the rain.</div>
  <div style="font-size:22px;color:#cfe6da;margin-top:26px">Universiti Malaya · GSC 2026–27 · Food Resilience</div>
  <div style="font-size:16px;color:#a9c3b7;margin-top:40px;max-width:1300px;line-height:1.5">Footage: Nothing Ahead, Srinivas Kashyap, Zeal Creative Studios, Prodèép Nëpalënsis, Ucundinamarca Virtual, Serg Alesenko (Pexels License). Photos: Scot Nelson (CC0), Irene Scott/AusAID (CC BY 2.0), Isabell Schulz (CC BY-SA 2.0), GPhoto15 (CC BY 4.0), via Wikimedia Commons. App footage: KokoShield Field Desk prototype, demo data. Drone survey, routes and counts: demo simulation. Voice: AI-generated.</div></div>`,
  'left:0;top:0', at(8, 9.4), END + 5, 'fade');


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
rec({ name: 'walk', n: 180, kind: 'phone', tin: at(6, 3.2), tout: at(6, 8.3), map: t => t - at(6, 3.2), at: 'left:1330px;top:110px',
  cam: [[0, 1.0, 195, 422], [6, 1.0, 195, 422]] });
/* Act 3b: adviser confirms on the Scout log */
rec({ name: 'log', n: 144, kind: 'lap', tin: at(6, 8.7), tout: S[7] + 0.2, map: t => t - at(6, 8.5),
  cam: [[0, 1.0, 720, 450], [0.9, 1.45, 560, 300], [4.8, 1.45, 560, 300]] });

/* ---------- per-frame ---------- */
const rainAt = t => Math.max(0.4 * Math.min(ramp(t, 0, 1.0), 1 - ramp(t, S[1] + 0.2, S[1] + 2.2)), 0.35 * Math.min(ramp(t, S[1] + 2.0, S[1] + 3), 1 - ramp(t, S[2] - 1.2, S[2] - 0.3)));
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
  [0, 1, 2].forEach(i => { const d = [3.0, 5.5, 9.8][i], q = ramp(t, at(1, d), at(1, d + 0.4)); const e = $('#pb' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * -30}px)`; });
  /* act 2 */
  const mm2 = 48 * ramp(t, at(2, 0.4), at(2, 2.8)); $('#mm2').textContent = Math.round(mm2); $('#mmbar2').style.width = (560 * Math.min(mm2, 60) / 60) + 'px';
  $('#trig2').innerHTML = mm2 >= 30 ? '<b style="color:#ff8a66">TRIGGER REACHED · 30 mm</b>' : 'Trigger 30 mm';
  $('#act2').style.opacity = ramp(t, at(2, 5.0), at(2, 5.4)) * (0.7 + 0.3 * Math.sin(t * 8));
  const u = t - S[3]; const f1 = sm((u - 0.8) / 2.4);
  const [dx, dy, dang] = along(SWEEP, f1); $('#hd').setAttribute('transform', `translate(${dx} ${dy}) rotate(${dang * 180 / Math.PI + 90}) scale(1.5)`);
  document.querySelectorAll('#hd .blade').forEach((b, i) => b.setAttribute('transform', `rotate(${(t * 2200 + i * 45) % 360})`));
  $('#sw').setAttribute('stroke-dashoffset', sweepLen * (1 - f1));
  ['A', 'D', 'G'].forEach(k => { const a = clamp((f1 - (WATER2[k][0][1] - 20) / 330) * 5); $('#hw' + k).setAttribute('opacity', a * (0.7 + 0.3 * Math.sin(t * 6))); $('#hs' + k).setAttribute('opacity', a); });
  [0, 1, 2, 3].forEach(i => { const a = ramp(u, 1.1 + i * 0.6, 1.4 + i * 0.6); const e = $('#in' + i); e.style.opacity = a; e.style.transform = `translateX(${(1 - a) * 30}px)`; });
  $('#hr').setAttribute('stroke-dashoffset', 900 * (1 - ramp(u, 3.6, 5.0)));
  [1, 2, 3, 4].forEach(n => $('#hn' + n).setAttribute('opacity', ramp(u, 3.5 + n * 0.3, 3.8 + n * 0.3)));
  $('#out2').style.opacity = ramp(u, 4.9, 5.3);
  document.querySelectorAll('.holoframe,.holomap').forEach(h => { h.style.transform = `perspective(1600px) rotateY(${-6 + 3 * Math.sin(t * 0.7)}deg) rotateX(${2 * Math.sin(t * 0.5)}deg)`; });
  /* act 2b */
  { const u = t - S[4] - 0.2; const fi = Math.max(0, Math.min(209, Math.round(u * 30))); const im = N3D[fi]; if (im.complete) $('#n3d').src = im.src; }
  [0, 1, 2, 3].forEach(i => { const q = ramp(t, S[4] + [1.8, 2.6, 3.4, 4.4][i], S[4] + [1.8, 2.6, 3.4, 4.4][i] + 0.4); const e = $('#nc' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * 30}px)`; });
  updateRecs(t);
  /* act 3 */
  updateVids(t);
  { const m = raceMin(t); if (t > S[5] - 0.5 && t < at(5, 10.8)) { drawSide('hu', RU, m, '#9fb4c6'); drawSide('hr2', RR, m, '#3fe08f'); }
    $('#clk3').textContent = `${Math.floor(m)}:${String(Math.floor((m % 1) * 60)).padStart(2, '0')}`; }
  /* act 4 */
  [0, 1, 2].forEach(i => { const q = ramp(t, at(7, 3.0 + i * 0.9), at(7, 3.5 + i * 0.9)); const e = $('#vi' + i); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * -30}px)`; });
}
