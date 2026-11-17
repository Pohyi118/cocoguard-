/* ================= interactive mode: story player, Explore hotspots, "Your turn" challenge ================= */
if (!VIDEO) {
  const audio = new Audio('assets/soundtrack.m4a'); audio.preload = 'auto';
  const el = id => document.getElementById(id);
  const pp = el('pp'), seek = el('seek'), tm = el('tm'), exBtn = el('explore'), chBtn = el('challenge'), ctl = el('ctl');
  const ovlEl = el('ovl'), chal = el('chal'), info = el('info'), toastEl = el('toast'), cta = el('cta');
  const ICON_PLAY = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z" fill="currentColor"/></svg>';
  const ICON_PAUSE = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg>';
  let mode = 'story', lastMove = performance.now(), toastT = 0;
  addEventListener('pointermove', () => { lastMove = performance.now(); });
  addEventListener('keydown', () => { lastMove = performance.now(); });
  const toast = msg => { toastEl.textContent = msg; toastEl.style.opacity = 1; toastT = performance.now(); };
  const fmt = x => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, '0')}`;

  /* ---------- player ---------- */
  const chipBtns = NAMES.map((n, i) => { const b = document.createElement('button'); b.textContent = `${i + 1} ${n}`; b.setAttribute('aria-label', `Chapter ${i + 1}: ${n}`);
    b.onclick = () => { setMode('story'); go(S[i] + 0.05); }; el('chips').appendChild(b); return b; });
  function setPlay(p) {
    playing = p; pp.innerHTML = (p ? ICON_PAUSE : ICON_PLAY) + `<span>${p ? 'Pause' : 'Play'}</span>`; pp.setAttribute('aria-label', p ? 'Pause the story' : 'Play the story');
    if (p) { if (mode !== 'story') setMode('story'); cta.hidden = true; if (t >= END - 0.05) t = 0; try { audio.currentTime = t; } catch (e) {} audio.play().catch(() => {}); }
    else audio.pause();
  }
  function go(x) { t = clamp(x, 0, END); try { audio.currentTime = t; } catch (e) {} cta.hidden = true; if (!playing) frame(t); }
  function setMode(m) {
    if (m !== 'story' && playing) setPlay(false);
    if (mode === 'challenge' && m !== 'challenge') leaveChallenge();
    mode = m; exploring = m === 'explore'; controls.enabled = exploring;
    exBtn.setAttribute('aria-pressed', String(m === 'explore')); chBtn.setAttribute('aria-pressed', String(m === 'challenge'));
    chal.hidden = m !== 'challenge'; ovlEl.style.display = m === 'story' ? '' : 'none'; info.hidden = true; cta.hidden = true;
    postUpdate = m === 'challenge' ? applyChallenge : null;
    if (m === 'challenge') resetChallenge();
    if (m === 'explore') toast('Drag to orbit · scroll to zoom · click a block or the Field Node');
    canvas.style.cursor = m === 'explore' ? 'grab' : 'default';
    if (!playing) frame(mode === 'challenge' ? CH_T : t);
  }
  pp.onclick = () => setPlay(!playing);
  seek.oninput = () => { if (mode !== 'story') setMode('story'); go(+seek.value); };
  exBtn.onclick = () => setMode(mode === 'explore' ? 'story' : 'explore');
  chBtn.onclick = () => setMode(mode === 'challenge' ? 'story' : 'challenge');
  el('startBtn').onclick = () => { el('start').hidden = true; setPlay(true); };
  el('startCh').onclick = () => { el('start').hidden = true; setMode('challenge'); };
  el('ctaCh').onclick = () => setMode('challenge');
  el('ctaEx').onclick = () => setMode('explore');
  el('ctaRe').onclick = () => { go(0); setPlay(true); };
  addEventListener('keydown', e => {
    const tag = e.target.tagName;
    if (tag === 'INPUT' && e.target.type === 'range' && e.code.startsWith('Arrow')) return;
    if (e.code === 'Space' && tag !== 'BUTTON' && tag !== 'INPUT') { e.preventDefault(); setPlay(!playing); }
    else if (e.code === 'ArrowRight') { setMode('story'); go(t + 5); }
    else if (e.code === 'ArrowLeft') { setMode('story'); go(t - 5); }
    else if (/^Digit[1-8]$/.test(e.code)) { setMode('story'); go(S[+e.code.slice(5) - 1] + 0.05); }
    else if (e.key === 'e' || e.key === 'E') exBtn.click();
    else if (e.key === 'c' || e.key === 'C') chBtn.click();
    else if (e.code === 'Escape') { if (!info.hidden) info.hidden = true; else if (mode !== 'story') setMode('story'); }
  });

  /* ---------- picking (raycast) ---------- */
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  const blockMeshes = Object.keys(blocks).map(k => { blocks[k].mesh.userData.block = k; return blocks[k].mesh; });
  function pick(e) {
    const r = canvas.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hb = ray.intersectObjects(blockMeshes, false)[0];
    const hn = mode === 'explore' ? ray.intersectObjects([nodeSpin, post], true)[0] : null;
    if (hn && (!hb || hn.distance < hb.distance + 2)) return { node: true };
    return hb ? { block: hb.object.userData.block } : null;
  }
  let down = null;
  canvas.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
  canvas.addEventListener('pointermove', e => { if (mode === 'story') return; const h = pick(e); canvas.style.cursor = h ? 'pointer' : (mode === 'explore' ? 'grab' : 'default'); });
  canvas.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 6) { down = null; return; }   /* a drag, not a click */
    down = null; const h = pick(e); if (!h) return;
    if (mode === 'challenge' && h.block) addBlock(h.block);
    else if (mode === 'explore') showInfo(h);
  });

  /* ---------- Explore: info cards ---------- */
  const INFO = { A: ['North terraces', 7], B: ['East rows', 8], C: ['Ridge rows', 7], D: ['Lower grove', 8], E: ['West rows', 8], F: ['Closed block', 0], G: ['South rows', 7], H: ['Packing lane', 7] };
  const PRIOR = new Set(['A', 'B']), PODS = { A: 3, G: 2, D: 1, B: 1 };
  const PRI_LABEL = k => k === 'F' ? 'Closed' : WET.has(k) ? 'Priority' : k === 'B' ? 'Watch' : 'Routine';
  function showInfo(h) {
    let html;
    if (h.node) html = `<div class="kick">Field Node · CAD concept</div><div class="h2" style="font-size:34px;padding-right:60px">Optional local sensor</div>
      <p class="lbl">Ventilated hood for an air temperature and humidity sensor, 86 × 62 × 32 mm enclosure and an ESP32-class controller envelope. Rainfall and leaf wetness need a separate gauge or a field record. Not yet built or field-tested.</p>`;
    else {
      const k = h.block, [name, min] = INFO[k];
      html = `<div class="kick">Block ${k}</div><div class="h2" style="font-size:36px;padding-right:60px">${name}</div>` + (k === 'F'
        ? `<p class="lbl">Closed to scouts today, so KokoShield leaves it out of the route.</p>`
        : `<div class="btns" style="margin:12px 0">${WET.has(k) ? '<span class="chip" style="background:#d8ecfb;color:#134b75">Slow drainage</span>' : '<span class="chip" style="background:#e9f2ed;color:#2B654F">Normal drainage</span>'}${PRIOR.has(k) ? '<span class="chip" style="background:#fbefd6;color:#8a5a0b">Past confirmed case</span>' : ''}</div>
           <p class="lbl">Scout time: <b>${min} min</b> · KokoShield priority: <b>${PRI_LABEL(k)}</b><br>Demo farm: <b>${PODS[k] || 0}</b> simulated infected pod${PODS[k] === 1 ? '' : 's'} after this storm.</p>`);
    }
    el('infobody').innerHTML = html; info.hidden = false; el('infoclose').focus();
  }
  el('infoclose').onclick = () => { info.hidden = true; };

  /* ---------- "Your turn" challenge ---------- */
  const MIN = { A: 7, B: 8, C: 7, D: 8, E: 8, G: 7, H: 7 };
  const CH_T = S[3] + 5.0;                                  /* after the storm, before KokoShield's colours appear */
  const C2 = { route: [], walking: false, done: false, ks: false, hint: false, walkT0: 0, ksT0: 0 };
  const scoutY = scout('#2f8fd8');
  const ynums = Array.from({ length: 7 }, (_, i) => sprite(labelTex(String(i + 1), '#2f8fd8', '#fff', 128, 128, 76, 64), 2.6, 2.6));
  const hintS = [
    ...['A', 'D', 'G'].map(k => { const s = sprite(labelTex('Wet · slow drainage', 'rgba(47,143,216,.95)', '#fff', 640, 110, 46, 40), 7.6, 1.3); s.position.copy(blocks[k].cen).setY(8.4); return s; }),
    ...['A', 'B'].map(k => { const s = sprite(labelTex('Past confirmed case', 'rgba(217,162,58,.95)', '#1f1606', 640, 110, 46, 40), 7.6, 1.3); s.position.copy(blocks[k].cen).setY(k === 'A' ? 10.0 : 8.4); return s; })];
  let yMesh = null;
  const bbtn = {};
  Object.keys(MAP).forEach(k => { const b = document.createElement('button'); b.textContent = k;
    b.setAttribute('aria-label', k === 'F' ? 'Block F, closed today' : `Add block ${k}, ${INFO[k][0]}, ${MIN[k]} minutes`); if (k === 'F') b.classList.add('closed');
    b.onclick = () => addBlock(k); el('cblocks').appendChild(b); bbtn[k] = b; });
  const used = () => C2.route.reduce((a, k) => a + MIN[k], 0);
  const planOf = route => route.map(k => [k, MIN[k], PODS[k] || 0]);
  function addBlock(k) {
    if (C2.walking || C2.done || C2.ks) { toast('Press Try again to plan a new route'); return; }
    if (k === 'F') { toast('Block F is closed to scouts today'); return; }
    if (C2.route.includes(k)) { toast(`Block ${k} is already in your route`); return; }
    if (used() + MIN[k] > 30) { toast(`Only ${30 - used()} min left: block ${k} needs ${MIN[k]} min`); return; }
    C2.route.push(k); renderChallenge();
  }
  function rebuildRoute() {
    if (yMesh) { scene.remove(yMesh); yMesh.geometry.dispose(); yMesh = null; }
    if (C2.route.length) { yMesh = new THREE.Mesh(new THREE.TubeGeometry(routeCurve(C2.route), 400, 0.3, 8, false), new THREE.MeshStandardMaterial({ color: '#2f8fd8', emissive: '#2f8fd8', emissiveIntensity: 0.35 })); scene.add(yMesh); }
  }
  function renderChallenge() {
    const u = used(); el('cbar').style.width = (100 * u / 30) + '%'; el('cmin').textContent = `${u} of 30 min used`;
    el('clist').innerHTML = C2.route.length ? C2.route.map(k => `<li>Block ${k} · ${INFO[k][0]} · ${MIN[k]} min</li>`).join('')
      : '<li style="list-style:none;margin-left:-30px;color:#9fb5aa">No blocks yet. Click a block on the farm or a letter above.</li>';
    Object.entries(bbtn).forEach(([k, b]) => { b.classList.toggle('sel', C2.route.includes(k)); if (k !== 'F') b.setAttribute('aria-pressed', String(C2.route.includes(k))); });
    rebuildRoute();
  }
  function resetChallenge() {
    Object.assign(C2, { route: [], walking: false, done: false, ks: false });
    el('cres').hidden = true; el('clive').hidden = true; el('clist').hidden = false; el('cwalk').hidden = false; el('cks').hidden = true; renderChallenge();
  }
  function leaveChallenge() { scoutY.visible = false; if (yMesh) yMesh.visible = false; ynums.forEach(s => s.material.opacity = 0); hintS.forEach(s => s.material.opacity = 0); }
  function showResult() {
    const found = C2.route.reduce((a, k) => a + (PODS[k] || 0), 0);
    const missedB = Object.keys(PODS).filter(k => !C2.route.includes(k));
    el('cres').innerHTML = `<div style="font-size:30px;font-weight:800">You found ${found} of 7 diseased pods</div>
      <div style="margin-top:6px">${missedB.length ? `Missed: block${missedB.length > 1 ? 's' : ''} ${missedB.join(', ')} (red rings on the farm).` : 'You found every infected pod. Great scouting!'}</div>
      <div style="margin-top:10px;color:#cfe6da">KokoShield ranks blocks with two signals you can't see from the gate: slow drainage after heavy rain and past confirmed cases. Its route A → G → D → B finds <b id="cksn">7</b> of 7 on this demo farm.</div>`;
    el('cres').hidden = false; el('clist').hidden = true; el('cwalk').hidden = true; el('cks').hidden = false; el('cks').focus();
  }
  el('cwalk').onclick = () => { if (!C2.route.length) { toast('Pick at least one block first'); return; } C2.walking = true; C2.done = false; C2.walkT0 = performance.now(); el('clive').hidden = false; el('cfound').textContent = '0'; };
  el('cks').onclick = () => { C2.ks = true; C2.ksT0 = performance.now(); el('cks').hidden = true; const n = el('cksn'); if (n) n.textContent = '0'; };
  el('cundo').onclick = () => { if (C2.walking || C2.done || C2.ks) return; C2.route.pop(); renderChallenge(); };
  el('creset').onclick = resetChallenge;
  el('cback').onclick = () => setMode('story');
  el('chint').onchange = e => { C2.hint = e.target.checked; };
  function applyChallenge() {
    const now = performance.now(), dur = 6;                         /* 30 scouting minutes walked in 6 seconds */
    camera.setViewOffset(1920, 1080, 330, 0, 1920, 1080); camera.position.set(0, 60, 36); camera.lookAt(0, 0, 1);
    for (const k in letters) letters[k].material.opacity = 1;
    for (const k in qmarks) qmarks[k].material.opacity = 0;
    nums.forEach(s => s.material.opacity = 0); missed.forEach(s => s.material.opacity = 0);
    closedLbl.material.opacity = 1; pulse.visible = false; gauge.visible = false; uMesh.visible = false; scoutU.visible = false;
    hintS.forEach(s => s.material.opacity = C2.hint ? 1 : 0);
    ynums.forEach((s, i) => { const k = C2.route[i]; s.material.opacity = k && !C2.ks ? 1 : 0; if (k) s.position.copy(blocks[k].cen).setY(6.4); });
    const plan = planOf(C2.route); let m = 0, w = null;
    if (C2.walking || C2.done) {
      m = Math.min(30, (now - C2.walkT0) / 1000 / dur * 30); w = walk(plan, m);
      el('cfound').textContent = w.finds;
      if (C2.walking && m >= plan.reduce((a, p) => a + p[1], 0)) { C2.walking = false; C2.done = true; showResult(); }
    }
    scoutY.visible = !!w && !C2.ks;
    if (w) { scoutY.position.copy(w.pos).setY(0.3 + (REDUCED ? 0 : Math.abs(Math.sin(now / 110)) * 0.12)); const nx = walk(plan, m + 0.15).pos; scoutY.rotation.y = Math.atan2(nx.x - w.pos.x, nx.z - w.pos.z); }
    if (yMesh) { yMesh.visible = !C2.ks; setReveal(yMesh, w ? w.trail : 1); }
    let km = -1;
    if (C2.ks) {
      km = Math.min(30, (now - C2.ksT0) / 1000 / dur * 30); const a = walk(PLAN_R, km);
      scoutR.visible = true; scoutR.position.copy(a.pos).setY(0.3); scoutR.children[0].rotation.x = 0;
      const nx = walk(PLAN_R, km + 0.15).pos; scoutR.rotation.y = Math.atan2(nx.x - a.pos.x, nx.z - a.pos.z);
      rMesh.visible = true; setReveal(rMesh, a.trail); const n = el('cksn'); if (n) n.textContent = a.finds;
    } else { scoutR.visible = false; rMesh.visible = false; }
    const doneB = new Set(); if (w) { let acc = 0; for (const [k, mm] of plan) { acc += mm; if (m >= acc) doneB.add(k); } }
    const ksB = new Set(); if (km >= 0) { let acc = 0; for (const [k, mm] of PLAN_R) { acc += mm; if (km >= acc) ksB.add(k); } }
    infected.forEach((p, i) => {
      const puls = 0.85 + 0.25 * Math.sin(now / 160 + i); let op = 0, tex = T_GRN;
      if (C2.ks) { if (ksB.has(p.block)) op = 1; }
      else if (doneB.has(p.block)) op = 1;
      else if (C2.done) { op = 1; tex = T_RED; }
      p.halo.material.map = tex; p.halo.material.opacity = op; p.halo.scale.set(1.3 * puls, 1.3 * puls, 1);
    });
  }

  /* ---------- main loop ---------- */
  window.KS_READY.then(() => {
    renderChallenge(); setPlay(false);
    last = performance.now();
    const loop = now => {
      const dt = (now - last) / 1000; last = now;
      if (playing) {
        t += Math.min(dt, 0.1);
        if (t >= END) { t = END; setPlay(false); cta.hidden = false; el('ctaCh').focus(); }
        if (audio.readyState >= 2 && Math.abs(audio.currentTime - t) > 0.35 && now - lastSync > 1000) { lastSync = now; try { audio.currentTime = t; } catch (e) {} }
      }
      ctl.style.opacity = (!playing || ctl.contains(document.activeElement) || now - lastMove < 2500) ? 1 : 0;
      if (toastT && now - toastT > 2200) { toastEl.style.opacity = 0; toastT = 0; }
      seek.value = t; tm.textContent = fmt(t);
      const si = Math.max(0, S.findIndex((s, i) => i < 8 && t >= s && t < S[i + 1]));
      chipBtns.forEach((b, i) => b.setAttribute('aria-current', String(i === si && mode === 'story')));
      frame(mode === 'challenge' ? CH_T : t);
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  });
}
