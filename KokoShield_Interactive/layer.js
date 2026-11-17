/* ================= KokoShield interactive player on the real-image story ================= */
(() => {
if (new URLSearchParams(location.search).get('mode') === 'video') { document.getElementById('start').hidden = true; document.getElementById('ctl').hidden = true; return; }
const el = id => document.getElementById(id);
const stage = el('stage'), wrap = document.createElement('div'); wrap.id = 'wrap'; stage.parentNode.insertBefore(wrap, stage); wrap.appendChild(stage);
['mode', 'cta'].forEach(id => stage.appendChild(el(id)));
function fit() { const k = Math.min((innerWidth - 32) / 1920, (innerHeight - 24) / 1080); stage.style.transform = `scale(${k})`; }
addEventListener('resize', fit); fit();
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const NAMES = K.names.map(n => n.replace(' and ', ' & '));
const audio = new Audio('assets/soundtrack.mp3'); audio.preload = 'auto';
const pp = el('pp'), seek = el('seek'), tm = el('tm'), exBtn = el('explore'), chBtn = el('challenge'), ctl = el('ctl');
const modeEl = el('mode'), chal = el('chal'), info = el('info'), toastEl = el('toast'), cta = el('cta');
const ICON_PLAY = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z" fill="currentColor"/></svg>';
const ICON_PAUSE = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg>';
let t = 0, playing = false, mode = 'story', last = performance.now(), lastSync = 0, lastMove = performance.now(), toastT = 0;
addEventListener('pointermove', () => { lastMove = performance.now(); }); addEventListener('keydown', () => { lastMove = performance.now(); });
const toast = msg => { toastEl.textContent = msg; toastEl.style.opacity = 1; toastT = performance.now(); };
const fmt = x => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, '0')}`;

/* ---------- map (the Field Desk app's own block map) ---------- */
WP.H = [400, 305];
const MIN = { A: 7, B: 8, C: 7, D: 8, E: 8, G: 7, H: 7 }, PODS = { A: 3, G: 2, D: 1, B: 1 }, PRIOR = new Set(['A', 'B']), WETB = new Set(['A', 'D', 'G']);
const NAME = { A: 'North terraces', B: 'East rows', C: 'Ridge rows', D: 'Lower grove', E: 'West rows', F: 'Stream edge (closed)', G: 'South rows', H: 'Packing lane' };
const PHOTO = { A: '13_black_pod.jpg', D: '12_black_pod.jpg', G: '11_black_pod.jpg', B: '02_hook_close.jpg', C: '06_farm.jpg', E: '06_farm.jpg', H: '01_hook_close.jpg', F: '06_farm.jpg' };
const chip = (id, x, y, txt, bg, fg = '#fff') => `<g id="${id}" opacity="0" style="pointer-events:none"><rect x="${x - txt.length * 3.4 - 8}" y="${y - 11}" width="${txt.length * 6.8 + 16}" height="22" rx="7" fill="${bg}"/><text x="${x}" y="${y + 4.5}" text-anchor="middle" font-size="12" font-weight="800" fill="${fg}">${txt}</text></g>`;
const extra = `<g>${Object.entries(WATER).map(([k, bl]) => `<g id="xw${k}" clip-path="url(#ch-c${k})" opacity="0" style="pointer-events:none">${bl.map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#3d8fd4" opacity=".62"/>`).join('')}<circle class="rp" cx="${bl[0][0]}" cy="${bl[0][1]}" r="6" fill="none" stroke="#bfe0ff" stroke-width="2"/></g>`).join('')}</g>
 <polyline id="xRY" style="pointer-events:none" points="" fill="none" stroke="#2f8fd8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
 <polyline id="xRR" style="pointer-events:none" points="${[WP.gate, ...PLAN_R.map(p => WP[p[0]])].map(p => p.join(',')).join(' ')}" fill="none" stroke="#1f8f5f" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>
 <g id="xMarks" style="pointer-events:none"></g>
 <g id="xNode" style="cursor:pointer"><rect x="212" y="139" width="22" height="16" rx="3" fill="#2B654F" stroke="#fff" stroke-width="2"/><rect x="236" y="142" width="9" height="11" rx="2" fill="#e8c9a0" stroke="#fff" stroke-width="1.5"/><text x="229" y="169" text-anchor="middle" font-size="10" font-weight="800" fill="#17201C" style="paint-order:stroke" stroke="#fff" stroke-width="3">Field Node</text></g>
 ${['A', 'D', 'G'].map(k => chip('xs' + k, WATER[k][0][0], WATER[k][0][1] - 26, 'Standing water', '#1f6fb8')).join('')}
 ${chip('xpA', 137, 50, 'Past case', '#D6A03E', '#1f1606')}${chip('xpB', 308, 50, 'Past case', '#D6A03E', '#1f1606')}
 <g id="xScout" opacity="0" style="pointer-events:none"><circle r="16" fill="#2f8fd8" opacity=".25"/><circle r="10" fill="#2f8fd8" stroke="#fff" stroke-width="3"/></g>
 <g id="xDrone" style="cursor:pointer">${DRONE}</g>`;
el('mapin').innerHTML = mapSVG('ch', 'neutral', extra);
const poly = k => el('ch-' + k);
function setFills(priority) { Object.keys(POLY).forEach(k => { poly(k).setAttribute('fill', priority ? PRI[k] : (k === 'F' ? 'url(#mclosed)' : '#C8D4BC'));
  const dark = priority && WETB.has(k), lab = el('ch-l' + k); lab.setAttribute('fill', dark ? '#fff' : (k === 'F' ? '#67716B' : '#17201C')); lab.setAttribute('stroke', dark ? '#B0452E' : '#EEF0EB'); }); }
const dronePlace = (x, y, ang, sc, spin) => { el('xDrone').setAttribute('transform', `translate(${x} ${y}) rotate(${ang}) scale(${sc})`); el('xDrone').querySelectorAll('.blade').forEach((b, i) => b.setAttribute('transform', `rotate(${(spin + i * 45) % 360})`)); };
const setWater = (k, a, now) => { el('xw' + k).setAttribute('opacity', a); el('xs' + k).setAttribute('opacity', a); const rp = el('xw' + k).querySelector('.rp'); const ph = (now / 1100) % 1; rp.setAttribute('r', 6 + ph * 26); rp.setAttribute('opacity', a * (1 - ph)); };
const rowOf = k => (WATER[k][0][1] - 20) / 330;

/* ---------- info cards (Explore) ---------- */
function showInfo(kind) {
  let h;
  if (kind === 'drone') h = `<img id="infophoto" src="photos/20_drone.jpg" alt="Illustrative camera drone flight"><div class="kick">Drone survey · concept</div><div class="h2" style="font-size:32px;padding-right:56px">Borrowed UM camera drone</div><p class="lbl">Flight 1 maps the blocks at setup. Flight 2, after heavy rain, shows where water is standing, so wet blocks are checked first. It cannot see black pod under the canopy and does not spray. Flown only with the grower's consent, under current CAAM rules, never in storms.</p><p class="lbl" style="font-size:15px;color:#9fb5aa">Photo: illustrative flight by another operator (Trusted user53, CC BY-SA 4.0)</p>`;
  else if (kind === 'node') h = `<img id="infophoto" src="assets/node_exploded.jpg" alt="Field Node CAD render" style="background:#fff;object-fit:contain"><div class="kick">Field Node · CAD concept</div><div class="h2" style="font-size:32px;padding-right:56px">Optional local sensor</div><p class="lbl">Ventilated hood for air temperature and humidity, 86 × 62 × 32 mm enclosure, ESP32-class controller envelope. Rainfall still comes from a gauge. Not yet built or field-tested.</p>`;
  else { const k = kind;
    h = `<img id="infophoto" src="photos/${PHOTO[k]}" alt=""><div class="kick">Block ${k}</div><div class="h2" style="font-size:32px;padding-right:56px">${NAME[k]}</div>` + (k === 'F' ? `<p class="lbl">Closed to scouts today, so KokoShield leaves it out of the route.</p>` :
      `<div class="btns" style="margin:10px 0">${WETB.has(k) ? '<span class="chip" style="background:#d8ecfb;color:#134b75">Standing water after rain</span>' : '<span class="chip" style="background:#e9f2ed;color:#2B654F">Drains normally</span>'}${PRIOR.has(k) ? '<span class="chip" style="background:#fbefd6;color:#8a5a0b">Past confirmed case</span>' : ''}</div>
       <p class="lbl">Scout time: <b>${MIN[k]} min</b> · KokoShield priority: <b>${WETB.has(k) ? 'Priority' : k === 'B' ? 'Watch' : 'Routine'}</b><br>Demo farm: <b>${PODS[k] || 0}</b> simulated infected pod${PODS[k] === 1 ? '' : 's'} after this storm.</p>`) +
      `<p class="lbl" style="font-size:15px;color:#9fb5aa">Photo: real cocoa photo from Wikimedia Commons (illustrative, not this block)</p>`; }
  el('infobody').innerHTML = h; info.hidden = false; el('infoclose').focus();
}
el('infoclose').onclick = () => { info.hidden = true; };
Object.keys(POLY).forEach(k => poly(k).addEventListener('click', () => { if (mode === 'explore') showInfo(k); else if (mode === 'challenge') addBlock(k); }));
el('xDrone').addEventListener('click', () => { if (mode === 'explore') showInfo('drone'); });
el('xNode').addEventListener('click', () => { if (mode === 'explore') showInfo('node'); });

/* ---------- challenge ---------- */
const C2 = { route: [], walking: false, done: false, ks: false, hint: false, walkT0: 0, ksT0: 0, dT0: 0 };
const bbtn = {};
Object.keys(POLY).forEach(k => { const b = document.createElement('button'); b.textContent = k; b.setAttribute('aria-label', k === 'F' ? 'Block F, closed today' : `Add block ${k}, ${NAME[k]}, ${MIN[k]} minutes`);
  if (k === 'F') b.classList.add('closed'); b.onclick = () => addBlock(k); el('cblocks').appendChild(b); bbtn[k] = b; });
const used = () => C2.route.reduce((a, k) => a + MIN[k], 0);
const planOf = r => r.map(k => [k, MIN[k], PODS[k] || 0]);
function addBlock(k) {
  if (C2.walking || C2.done || C2.ks) { toast('Press Try again to plan a new route'); return; }
  if (k === 'F') { toast('Block F is closed to scouts today'); return; }
  if (C2.route.includes(k)) { toast(`Block ${k} is already in your route`); return; }
  if (used() + MIN[k] > 30) { toast(`Only ${30 - used()} min left: block ${k} needs ${MIN[k]} min`); return; }
  C2.route.push(k); renderChallenge();
}
function renderChallenge() {
  const u = used(); el('cbar').style.width = (100 * u / 30) + '%'; el('cmin').textContent = `${u} of 30 min used`;
  el('clist').innerHTML = C2.route.length ? C2.route.map(k => `<li>Block ${k} · ${NAME[k]} · ${MIN[k]} min</li>`).join('') : '<li style="list-style:none;margin-left:-30px;color:#9fb5aa">No blocks yet. Click a block on the map or a letter above.</li>';
  Object.entries(bbtn).forEach(([k, b]) => { b.classList.toggle('sel', C2.route.includes(k)); if (k !== 'F') b.setAttribute('aria-pressed', String(C2.route.includes(k))); });
  const pts = [WP.gate, ...C2.route.map(k => WP[k])]; el('xRY').setAttribute('points', C2.route.length ? pts.map(p => p.join(',')).join(' ') : '');
  el('xMarks').innerHTML = C2.route.map((k, i) => `<g><circle cx="${WP[k][0]}" cy="${WP[k][1]}" r="11" fill="#2f8fd8" stroke="#fff" stroke-width="2.5"/><text x="${WP[k][0]}" y="${WP[k][1] + 4.5}" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">${i + 1}</text></g>`).join('') + '<g id="xRings"></g>';
}
function resetChallenge() { Object.assign(C2, { route: [], walking: false, done: false, ks: false }); el('cres').hidden = true; el('clive').hidden = true; el('clist').hidden = false; el('cwalk').hidden = false; el('cks').hidden = true; renderChallenge(); }
function showResult() {
  const found = C2.route.reduce((a, k) => a + (PODS[k] || 0), 0), missedB = Object.keys(PODS).filter(k => !C2.route.includes(k));
  el('cres').innerHTML = `<div style="font-size:28px;font-weight:800">You found ${found} of 7 diseased pods</div><div style="margin-top:6px">${missedB.length ? `Missed: block${missedB.length > 1 ? 's' : ''} ${missedB.join(', ')} (red rings).` : 'You found every infected pod. Great scouting!'}</div>
    <div style="margin-top:10px;color:#cfe6da">KokoShield ranks blocks by two signals you can't see from the gate: standing water after heavy rain and past confirmed cases. Its route A → G → D → B finds <b id="cksn">7</b> of 7 on this demo farm.</div>`;
  el('cres').hidden = false; el('clist').hidden = true; el('cwalk').hidden = true; el('cks').hidden = false; el('cks').focus();
}
el('cwalk').onclick = () => { if (!C2.route.length) { toast('Pick at least one block first'); return; } C2.walking = true; C2.walkT0 = performance.now(); el('clive').hidden = false; };
el('cks').onclick = () => { C2.ks = true; C2.ksT0 = performance.now(); el('cks').hidden = true; };
el('cundo').onclick = () => { if (C2.walking || C2.done || C2.ks) return; C2.route.pop(); renderChallenge(); };
el('creset').onclick = resetChallenge;
el('chint').onchange = e => { C2.hint = e.target.checked; if (C2.hint) C2.dT0 = performance.now(); };
function rings(doneB, ksMode, showMissed) {
  el('xRings').innerHTML = Object.keys(PODS).map(k => { const f = doneB.has(k), m = showMissed && !f; if (!f && !m) return '';
    const col = f ? '#1f8f5f' : '#B0452E', txt = f ? `+${PODS[k]} found` : `${PODS[k]} missed`;
    return `<circle cx="${WP[k][0]}" cy="${WP[k][1]}" r="20" fill="none" stroke="${col}" stroke-width="4"/><text x="${WP[k][0]}" y="${WP[k][1] + 38}" text-anchor="middle" font-size="13" font-weight="800" fill="${col}" style="paint-order:stroke" stroke="#fff" stroke-width="4">${txt}</text>`; }).join('');
}
function tickMap(now) {
  /* drone: survey flight in the challenge, hovering in Explore */
  if (mode === 'challenge' && C2.hint) {
    const f = clamp((now - C2.dT0) / 4500); const [x, y, a] = along(LAWN, f); dronePlace(x, y, a * 180 / Math.PI + 90, 1.4, now * 2);
    ['A', 'D', 'G'].forEach(k => { setWater(k, clamp((f - rowOf(k)) * 5), now); if (C2.walking || C2.done || C2.ks) el('xs' + k).setAttribute('opacity', 0); });
    const pc = ramp(f, 0.92, 1); el('xpA').setAttribute('opacity', pc); el('xpB').setAttribute('opacity', pc);
  } else if (mode === 'explore') {
    dronePlace(520, 28 + 3 * Math.sin(now / 500), 0, 1.4, now * 2); ['A', 'D', 'G'].forEach(k => setWater(k, 1, now));
    el('xpA').setAttribute('opacity', 1); el('xpB').setAttribute('opacity', 1);
  } else {
    dronePlace(72, 312, 0, 1.2, 0); ['A', 'D', 'G'].forEach(k => setWater(k, 0, now)); el('xpA').setAttribute('opacity', 0); el('xpB').setAttribute('opacity', 0);
  }
  if (mode !== 'challenge') { el('xScout').setAttribute('opacity', 0); el('xRR').setAttribute('opacity', 0); return; }
  const plan = planOf(C2.route), dur = 6; let doneB = new Set(), showMissed = false;
  if (C2.ks) {
    const m = Math.min(30, (now - C2.ksT0) / 1000 / dur * 30), w = walk2(PLAN_R, m);
    el('xScout').setAttribute('opacity', 1); el('xScout').setAttribute('transform', `translate(${w.pos[0]} ${w.pos[1]})`); el('xScout').querySelectorAll('circle').forEach(c => c.setAttribute('fill', '#1f8f5f'));
    const L = plen([WP.gate, ...PLAN_R.map(p => WP[p[0]])]); el('xRR').setAttribute('opacity', 1); el('xRR').setAttribute('stroke-dasharray', L); el('xRR').setAttribute('stroke-dashoffset', L * (1 - w.trail));
    el('xRY').setAttribute('opacity', 0.25); let acc = 0; PLAN_R.forEach(([k, mm]) => { acc += mm; if (m >= acc) doneB.add(k); }); const n = el('cksn'); if (n) n.textContent = w.finds;
  } else if (C2.walking || C2.done) {
    const m = Math.min(30, (now - C2.walkT0) / 1000 / dur * 30), w = walk2(plan, m);
    el('xScout').setAttribute('opacity', 1); el('xScout').setAttribute('transform', `translate(${w.pos[0]} ${w.pos[1]})`); el('xScout').querySelectorAll('circle').forEach(c => c.setAttribute('fill', '#2f8fd8'));
    el('xRR').setAttribute('opacity', 0); el('xRY').setAttribute('opacity', 1); el('cfound').textContent = w.finds;
    let acc = 0; plan.forEach(([k, mm]) => { acc += mm; if (m >= acc) doneB.add(k); });
    if (C2.walking && m >= plan.reduce((a, p) => a + p[1], 0)) { C2.walking = false; C2.done = true; showResult(); }
    showMissed = C2.done;
  } else { el('xScout').setAttribute('opacity', 0); el('xRR').setAttribute('opacity', 0); el('xRY').setAttribute('opacity', 1); }
  if (el('xRings')) rings(doneB, C2.ks, showMissed);
}

/* ---------- modes and player ---------- */
const chipBtns = NAMES.map((n, i) => { const b = document.createElement('button'); b.textContent = `${i + 1} ${n}`; b.setAttribute('aria-label', `Chapter ${i + 1}: ${n}`);
  b.onclick = () => { setMode('story'); go(S[i] + 0.05); }; el('chips').appendChild(b); return b; });
function setPlay(p) {
  playing = p; pp.innerHTML = (p ? ICON_PAUSE : ICON_PLAY) + `<span>${p ? 'Pause' : 'Play'}</span>`; pp.setAttribute('aria-label', p ? 'Pause the story' : 'Play the story');
  if (p) { if (mode !== 'story') setMode('story'); cta.hidden = true; if (t >= END - 0.05) t = 0; try { audio.currentTime = t; } catch (e) {} audio.play().catch(() => {}); } else audio.pause();
}
function go(x) { t = clamp(x, 0, END); try { audio.currentTime = t; } catch (e) {} cta.hidden = true; if (!playing) update(t); }
function setMode(m) {
  if (m !== 'story' && playing) setPlay(false);
  mode = m; modeEl.hidden = m === 'story'; chal.hidden = m !== 'challenge'; info.hidden = true; cta.hidden = true;
  exBtn.setAttribute('aria-pressed', String(m === 'explore')); chBtn.setAttribute('aria-pressed', String(m === 'challenge'));
  [el('chips'), seek, tm].forEach(x => { x.hidden = m !== 'story'; });
  setFills(m === 'explore');
  el('modetitle').innerHTML = m === 'explore' ? 'Explore the farm map<small>The Field Desk map of the demo farm after 48 mm of rain · click a block, the drone or the Field Node</small>'
    : 'Your turn<small>Plan a 30-minute scouting round on the Field Desk map of the demo farm</small>';
  el('legend').innerHTML = m === 'explore' ? '<span><i style="background:#B0452E"></i>Priority</span><span><i style="background:#D6A03E"></i>Watch</span><span><i style="background:#C8D4BC"></i>Routine</span><span><i style="background:#3d8fd4"></i>Standing water (drone survey)</span><span><i style="background:#D6A03E;border-radius:50%"></i>Past case</span>'
    : '<span><i style="background:#2f8fd8"></i>Your route</span><span><i style="background:#1f8f5f"></i>KokoShield route</span><span><i style="background:#3d8fd4"></i>Standing water</span><span style="color:#cfe6da">Demo farm, simulated pods</span>';
  if (m === 'challenge') resetChallenge();
  if (m === 'story') update(t);
}
pp.onclick = () => setPlay(!playing);
seek.oninput = () => { if (mode !== 'story') setMode('story'); go(+seek.value); };
exBtn.onclick = () => setMode(mode === 'explore' ? 'story' : 'explore');
chBtn.onclick = () => setMode(mode === 'challenge' ? 'story' : 'challenge');
el('startBtn').onclick = () => { el('start').hidden = true; setPlay(true); };
el('startCh').onclick = () => { el('start').hidden = true; setMode('challenge'); };
el('ctaCh').onclick = () => setMode('challenge'); el('ctaEx').onclick = () => setMode('explore'); el('ctaRe').onclick = () => { go(0); setPlay(true); };
addEventListener('keydown', e => {
  const tag = e.target.tagName; if (tag === 'INPUT' && e.target.type === 'range' && e.code.startsWith('Arrow')) return;
  if (e.code === 'Space' && tag !== 'BUTTON' && tag !== 'INPUT') { e.preventDefault(); setPlay(!playing); }
  else if (e.code === 'ArrowRight') { setMode('story'); go(t + 5); } else if (e.code === 'ArrowLeft') { setMode('story'); go(t - 5); }
  else if (/^Digit[1-9]$/.test(e.code)) { setMode('story'); go(S[+e.code.slice(5) - 1] + 0.05); }
  else if (e.key === 'e' || e.key === 'E') exBtn.click(); else if (e.key === 'c' || e.key === 'C') chBtn.click();
  else if (e.code === 'Escape') { if (!info.hidden) info.hidden = true; else if (mode !== 'story') setMode('story'); }
});
window.KS_READY.then(() => {
  seek.max = END.toFixed(1); renderChallenge(); setPlay(false); setFills(false); update(0);
  const loop = now => {
    const dt = (now - last) / 1000; last = now;
    if (playing) { t += Math.min(dt, 0.1); if (t >= END) { t = END; setPlay(false); cta.hidden = false; el('ctaCh').focus(); }
      if (audio.readyState >= 2 && Math.abs(audio.currentTime - t) > 0.35 && now - lastSync > 1000) { lastSync = now; try { audio.currentTime = t; } catch (e) {} } }
    ctl.style.opacity = (!playing || ctl.contains(document.activeElement) || now - lastMove < 2500) ? 1 : 0;
    if (toastT && now - toastT > 2200) { toastEl.style.opacity = 0; toastT = 0; }
    seek.value = t; tm.textContent = fmt(t);
    let si = 0; for (let i = 0; i < S.length - 1; i++) if (t >= S[i]) si = i;
    chipBtns.forEach((b, i) => b.setAttribute('aria-current', String(i === si && mode === 'story')));
    if (mode === 'story') { if (playing) update(t); } else tickMap(now);
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
});
})();
