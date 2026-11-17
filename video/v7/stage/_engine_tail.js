/* kinetic headlines */
function splitWords(root) { const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const ns = []; while (tw.nextNode()) ns.push(tw.currentNode); const out = [];
  ns.forEach(nd => { const fr = document.createDocumentFragment(); nd.textContent.split(/(\s+)/).forEach(p => { if (!p) return; if (/^\s+$/.test(p)) fr.appendChild(document.createTextNode(p)); else { const w = document.createElement('span'); w.className = 'w'; w.textContent = p; fr.appendChild(w); out.push(w); } }); nd.parentNode.replaceChild(fr, nd); }); return out; }
OV.forEach(o => { const hs = o.el.querySelectorAll('.h1,.h2'); if (!hs.length) return; o.words = []; hs.forEach(h => { const a = h.dataset.at ? +h.dataset.at : null; splitWords(h).forEach((w, j) => { w._at = a; w._j = j; o.words.push(w); }); }); });

/* rain + lightning */
const rc = $('#rain').getContext('2d'); const DROPS = Array.from({ length: 1000 }, () => [rnd() * 2200 - 140, rnd() * 1200, 1100 + rnd() * 700, 20 + rnd() * 30, 0.2 + rnd() * 0.5]);
function drawRain(t, k) { rc.clearRect(0, 0, 1920, 1080); if (k < 0.01) return; rc.strokeStyle = '#dbe8f1'; rc.lineWidth = 1.6;
  for (const [x0, y0, v, len, a] of DROPS) { const y = ((y0 + v * t) % 1200) - 60, x = x0 + y * 0.14; rc.globalAlpha = a * k; rc.beginPath(); rc.moveTo(x, y); rc.lineTo(x + len * 0.14, y + len); rc.stroke(); } rc.globalAlpha = 1; }
const rainAt = t => Math.max(Math.min(ramp(t, 0, 1.2), 1 - ramp(t, S[1] + 1.5, S[1] + 4.5)), 0.55 * Math.min(ramp(t, at(3, 4.4), at(3, 5.0)), 1 - ramp(t, at(3, 6.6), at(3, 7.4))));
const FLASHES = [2.0, 5.3];
const flashAt = t => { let v = 0; for (const f of FLASHES) { const d = t - f; v = Math.max(v, 0.85 * Math.exp(-((d / 0.045) ** 2)), 0.55 * Math.exp(-(((d - 0.17) / 0.05) ** 2)), 0.25 * Math.exp(-(((d - 0.32) / 0.08) ** 2))); } return v; };

/* cursor helper for the laptop scenes */
function cursor(id, t, keys) {   /* keys: [time, cssX, cssY, click?] */
  const cur = $('#' + id + 'cur'), rip = $('#' + id + 'rip'); let i = 0; while (i < keys.length - 1 && keys[i + 1][0] <= t) i++;
  const a = keys[i], b = keys[Math.min(i + 1, keys.length - 1)], k = b[0] > a[0] ? sm((t - a[0]) / (b[0] - a[0])) : 0;
  const x = lerp(a[1], b[1], k) * CSS, y = lerp(a[2], b[2], k) * CSS; cur.style.transform = `translate(${x}px,${y}px)`;
  let r = 0, rs = 1; for (const kk of keys) if (kk[3] && t >= kk[0] && t < kk[0] + 0.6) { const f = (t - kk[0]) / 0.6; r = 1 - f; rs = 0.4 + f * 1.4; }
  rip.style.opacity = r; rip.style.transform = `scale(${rs})`;
}

/* ================= per-frame update ================= */
function update(t) {
  for (const s of SHOTS) { const v = vis(t, s.t0, s.t1, 0.6, 0.6); if (v <= 0.001) { s.el.style.display = 'none'; continue; }
    s.el.style.display = 'block'; s.el.style.opacity = v; const k = sm((t - s.t0) / (s.t1 - s.t0));
    s.el.style.transform = `scale(${lerp(s.from[0], s.to[0], k)}) translate(${lerp(s.from[1], s.to[1], k)}%, ${lerp(s.from[2], s.to[2], k)}%)`; }
  drawRain(t, rainAt(t)); const fl = flashAt(t); $('#flash').style.opacity = (fl * 0.6).toFixed(3);
  /* overlays */
  let credit = '';
  for (const s of SHOTS) if (s.el.style.display === 'block' && +s.el.style.opacity > 0.5 && s.credit) credit = s.credit;
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
  chap.el.textContent = `${si + 1} / ${S.length - 1} · ${NAMES[si]}`;
  const c = CAPS.find(c => t >= c[0] - 0.05 && t < c[1] + 0.25); cap.el.style.display = c && t < END - 2.3 ? 'block' : 'none'; if (c && cap.el.textContent !== c[2]) cap.el.textContent = c[2];
  prog.style.width = (1920 * clamp(t / END)) + 'px';
  let wp = -1; for (let k = 1; k < S.length - 1; k++) if (Math.abs(t - S[k]) < 0.42) wp = (t - S[k] + 0.42) / 0.84;
  const wipe = $('#wipe'); if (wp >= 0) { wipe.style.display = 'flex'; wipe.style.transform = `translateX(${-3050 + wp * 5420}px) skewX(-16deg)`; } else wipe.style.display = 'none';

  /* scene 1 widgets */
  $('#clk1').style.strokeDashoffset = 276.5 * (1 - ramp(t, 1.0, 2.9));
  $('#which').style.opacity = ramp(t, 3.8, 4.5);
  const mm = 48 * ramp(t, 1.4, 5.6); $('#mm').textContent = Math.round(mm); $('#mmbar').style.width = (360 * Math.min(mm, 60) / 60) + 'px';
  $('#trigtxt').innerHTML = mm >= 30 ? '<b style="color:#B5462E">Trigger reached · 30 mm</b> → scout now' : 'Trigger: 30 mm';
  document.querySelectorAll('.hb .pin').forEach((p, i) => { const a = bo((t - at(0, 7.2) - i * 0.5) / 0.45); p.style.opacity = clamp(a); p.style.transform = `scale(${0.6 + 0.4 * a})`; });
  /* scene 2 */
  $('#st1').textContent = t < at(1, 3.4) ? Math.round(30 * ramp(t, at(1, 1.8), at(1, 3.4))) + '%' : '20–30%';
  ['#c1', '#c2', '#c3'].forEach((s, i) => { const a = ramp(t, at(1, 7.3 + i * 0.5), at(1, 7.8 + i * 0.5)); $(s).style.opacity = a; $(s).style.transform = `scale(${0.6 + 0.4 * bo(a)})`; });
  const d3 = ramp(t, at(1, 13.5), at(1, 15.5)); $('#st3').textContent = Math.round(86 * d3) + '%'; $('#donut').style.strokeDashoffset = 251.3 * (1 - 0.86 * d3);
  /* scene 3 */
  $('#ax1').style.strokeDashoffset = 790 * (1 - ramp(t, at(2, 0.7), at(2, 1.6))); $('#ax2').style.strokeDashoffset = 510 * (1 - ramp(t, at(2, 0.7), at(2, 1.6)));
  dots.forEach((d, i) => { const a = ramp(t, at(2, d[3]), at(2, d[3] + 0.4)); const g = $('#d' + i); g.setAttribute('opacity', a); const cx = X(d[1]), cy = Y(d[2]), z = 0.3 + 0.7 * bo(a); g.setAttribute('transform', `translate(${cx} ${cy}) scale(${z}) translate(${-cx} ${-cy})`); });
  const qa = ramp(t, at(2, 6.0), at(2, 6.8)); $('#quad').setAttribute('opacity', (0.10 + 0.06 * Math.sin(t * 5)) * qa); $('#qlab').setAttribute('opacity', qa);
  const ka = ramp(t, at(2, 8.6), at(2, 9.2)); $('#ks').setAttribute('opacity', ka); { const cx = X(8.6), cy = Y(8.2), z = 0.4 + 0.6 * bo(ka); $('#ks').setAttribute('transform', `translate(${cx} ${cy}) scale(${z}) translate(${-cx} ${-cy})`); }
  $('#ksring').setAttribute('r', 22 + 18 * ramp(t, at(2, 8.6), at(2, 10))); $('#ksring').setAttribute('opacity', 1 - ramp(t, at(2, 9), at(2, 10.2)));
  /* scene 4: drone mapping flight then post-rain flight */
  const f1 = ramp(t, at(3, 2.6), at(3, 4.5)), f2 = ramp(t, at(3, 4.7), at(3, 6.6)); const second = t >= at(3, 4.6);
  const [dx, dy, dang] = along(LAWN, second ? f2 : f1);
  $('#drone').setAttribute('transform', `translate(${dx} ${dy}) rotate(${dang * 180 / Math.PI + 90}) scale(1.7)`);
  document.querySelectorAll('#drone .blade').forEach((b, i) => b.setAttribute('transform', `rotate(${(t * 2200 + i * 45) % 360})`));
  $('#lawn').setAttribute('stroke-dashoffset', lawnLen * (1 - (second ? f2 : f1))); $('#lawn').setAttribute('stroke', second ? '#1f6fb8' : '#2B654F');
  Object.keys(POLY).forEach(k => { const cy = POLY[k].split(' ').map(p => +p.split(',')[1]).reduce((a, b) => a + b) / POLY[k].split(' ').length;
    const pass = (cy - 20) / 330; $('#o' + k).setAttribute('opacity', clamp((f1 - pass) * 6) * (1 - 0.6 * ramp(t, at(3, 4.6), at(3, 5.2)))); });
  ['A', 'D', 'G'].forEach(k => { const cy = WATER[k][0][1]; const a = second ? clamp((f2 - (cy - 20) / 330) * 5) : 0; const g = $('#w' + k); g.setAttribute('opacity', a);
    const rp = g.querySelector('.rip'); const ph = ((t * 0.9) % 1); rp.setAttribute('r', 6 + ph * 26); rp.setAttribute('opacity', a * (1 - ph)); });
  const chipTxt = t < at(3, 4.6) ? (f1 >= 1 ? '✓ Block map ready · 8 blocks' : 'Flight 1 · mapping the blocks') : (f2 >= 1 ? 'Wet blocks found: A, D, G → ranked first' : 'Flight 2 · after 48 mm of rain');
  const chipEl = $('#dmchip'); chipEl.textContent = chipTxt; chipEl.style.background = second ? '#1f6fb8' : '#2B654F'; chipEl.style.color = '#fff'; chipEl.style.fontSize = '24px';
  document.querySelectorAll('.callout').forEach((c, i) => c.setAttribute('opacity', ramp(t, at(3, 8.4 + i * 0.4), at(3, 8.8 + i * 0.4))));
  /* scene 5: real app, click Wet spell then Generate route, zoom on the route */
  cursor('lp1', t, [[at(4, 0.0), 900, 640], [at(4, 1.4), 198, 381], [at(4, 1.55), 198, 381, 1], [at(4, 2.5), 1311, 111], [at(4, 2.65), 1311, 111, 1], [at(4, 3.4), 1360, 160], [at(4, 9), 1360, 160]]);
  $('#lp1cur').style.opacity = 1 - ramp(t, at(4, 3.2), at(4, 3.6));
  $('#lp1i1').style.opacity = ramp(t, at(4, 2.75), at(4, 3.05));
  { const z = 1 + 0.55 * Math.min(ramp(t, at(4, 3.7), at(4, 4.7)), 1 - ramp(t, at(4, 6.6), at(4, 7.2))); const ox = 760 * CSS, oy = 900 * CSS; $('#lp1z').style.transform = `translate(${ox}px,${oy}px) scale(${z}) translate(${-ox}px,${-oy}px)`; }
  /* scene 6: review clicks on the real scout log */
  cursor('lp2', t, [[at(5, 3.2), 700, 600], [at(5, 4.4), 1242, 394], [at(5, 4.6), 1242, 394, 1], [at(5, 5.4), 1242, 328], [at(5, 5.6), 1242, 328, 1], [at(5, 6.4), 1319, 263], [at(5, 6.6), 1319, 263, 1], [at(5, 7.3), 1194, 172], [at(5, 9), 1194, 172]]);
  BADGES.forEach((b, i) => { const a = ramp(t, at(5, b[3]), at(5, b[3] + 0.15)); const e = $('#bdg' + i); e.style.opacity = a * (1 - ramp(t, at(5, 7.0), at(5, 7.2))); e.style.transform = `scale(${1 + 0.2 * (1 - ramp(t, at(5, b[3]), at(5, b[3] + 0.3)))})`; });
  $('#lp2i1').style.opacity = ramp(t, at(5, 7.0), at(5, 7.2));
  $('#confring').style.opacity = Math.min(ramp(t, at(5, 7.4), at(5, 7.7)), 1) * (0.6 + 0.4 * Math.sin(t * 6));
  /* scene 7: race */
  const m = raceMin(t), a = walk2(PLAN_R, m), b = walk2(PLAN_U, m);
  $('#scR').setAttribute('transform', `translate(${a.pos[0]} ${a.pos[1]})`); $('#scU').setAttribute('transform', `translate(${b.pos[0]} ${b.pos[1]})`);
  document.querySelectorAll('#scR .halo, #scU .halo').forEach(h => h.setAttribute('r', 14 + 4 * Math.sin(t * 6)));
  $('#trR').setAttribute('stroke-dashoffset', LR * (1 - a.trail)); $('#trU').setAttribute('stroke-dashoffset', LU * (1 - b.trail));
  finishAt(PLAN_R).filter(x => x[2]).forEach(([k, mm2], i) => { const tk = raceT0 + (raceT1 - raceT0) * mm2 / 30, f = (t - tk) / 1.2; const g = $('#bu' + i);
    g.setAttribute('opacity', f > 0 && f < 1 ? 1 - f : 0); g.querySelector('.br').setAttribute('r', 10 + 30 * clamp(f)); g.querySelector('.bt').setAttribute('y', WP[k][1] - 16 - 30 * clamp(f)); });
  document.querySelectorAll('.mis').forEach(g => g.setAttribute('opacity', ramp(t, raceT1 + 0.1, raceT1 + 0.5)));
  $('#mins').textContent = Math.floor(m) + ' min'; $('#clk').style.strokeDashoffset = 263.9 * (1 - m / 30);
  $('#srn').textContent = a.finds; $('#sun').textContent = b.finds;
  $('#srf').textContent = a.first ? `First find ${a.first} min · 0 affected blocks missed` : 'First find —';
  $('#suf').textContent = b.first ? `First find ${b.first} min` + (m >= 30 ? ' · 2 affected blocks missed' : '') : 'First find —';
  FACTS.forEach((f, i) => { const e = $('#fact' + i); const q = ramp(t, at(6, 12.4 + i * 0.6), at(6, 12.8 + i * 0.6)); e.style.opacity = q; e.style.transform = `translateX(${(1 - q) * 30}px)`; });
  /* scene 8 */
  [['#f1', at(7, 6.0)], ['#f2', at(7, 6.7)]].forEach(([s, t0]) => { const f = ((t - t0) % 1.6) / 1.6; $(s).setAttribute('cx', t > t0 ? 10 + 165 * f : 10); $(s).setAttribute('opacity', t > t0 ? 1 - f * 0.3 : 0); });
  const n = t < at(7, 13.2) ? 20 * ramp(t, at(7, 11.2), at(7, 12.8)) : 20 + 40 * ramp(t, at(7, 13.2), at(7, 15.0));
  for (let i = 0; i < 60; i++) $('#g' + i).style.background = i < Math.round(n) ? (i < 20 ? '#2B654F' : '#8CAE9E') : '#d9e3dd';
  $('#farms').textContent = Math.round(n);
}
window.renderAt = async t => { update(t); return true; };
window.KS_READY = Promise.all([document.fonts.ready, ...[...document.images].map(im => im.complete ? 1 : new Promise(r => { im.onload = im.onerror = r; }))]).then(() => { update(0); return true; });
</script>
</body>
</html>
