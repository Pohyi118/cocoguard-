/* ---------------- photo shots (Ken Burns + grade) ---------------- */
const SHOTS = [];
function shot(file, t0, t1, from, to, grade = '', pos = '50% 50%', extra = '') {
  const el = document.createElement('div'); el.className = 'shot';
  el.innerHTML = `<img src="${PH}${file}" style="object-position:${pos};filter:${grade}">${extra}`; $('#bg').appendChild(el);
  SHOTS.push({ el, file, t0, t1, from, to, credit: CRED[file] || '' });
}
const pin = (x, y, text, col, dx, dy, side = 'right') => `<div class="pin" style="left:${x}px;top:${y}px"><div class="dot" style="background:${col}"></div><div class="lab" style="background:${col};${side === 'right' ? 'left' : 'right'}:${dx}px;top:${dy}px">${text}</div></div>`;
/* 1 hook */
shot('18_rain.jpg', -0.2, at(0, 3.9), [1.10, 0, 0], [1.24, -2, 1], 'saturate(.65) brightness(.68) contrast(1.12)');
shot('02_hook_close.jpg', at(0, 3.3), at(0, 7.1), [1.06, 2, 0], [1.2, -1, -2], 'saturate(.8) brightness(.74) contrast(1.08)');
shot('13_black_pod.jpg', at(0, 6.5), S[1] + 0.45, [1.0, 0, 0], [1.16, -5, -4], 'saturate(.95) brightness(.88)', '50% 43%',
  `<div class="hb">${pin(691, 386, 'Healthy pod', '#2f9a6a', 34, -70)}${pin(1306, 694, 'Black pod', '#B0452E', 34, -74)}</div>`);
/* 2 climate risk */
shot('11_black_pod.jpg', S[1] - 0.2, at(1, 6.9), [1.04, 0, 0], [1.16, 2, -2], 'brightness(.78) saturate(.9)');
shot('17_market.jpg', at(1, 6.4), at(1, 13.0), [1.04, 0, 0], [1.14, -2, 0], 'brightness(.8)');
shot('14_farmer.jpg', at(1, 12.5), S[2] + 0.4, [1.03, 0, 0], [1.14, -2, 1], 'brightness(.82)');
/* 3 market gap */
shot('16_farmer.jpg', S[2] - 0.2, S[3] + 0.4, [1.05, 0, 0], [1.12, 2, 0], 'brightness(.55) blur(3px)');
/* 4 drone (photo, then map and node scenes) */
shot('20_drone.jpg', S[3] - 0.2, at(3, 2.7), [1.04, 0, 0], [1.16, 3, 2], 'brightness(.88) saturate(1.05)', '50% 50%',
  `<div class="hb">${pin(595, 367, 'Camera drone', '#2B654F', 34, -74)}</div>`);
shot('06_farm.jpg', at(3, 7.6), S[4] + 0.3, [1.08, 0, 0], [1.14, 0, 0], 'brightness(.35) blur(6px) saturate(.8)');
/* 5 ranked route: blurred farm behind the laptop */
shot('02_hook_close.jpg', S[4] - 0.2, S[5] + 0.3, [1.15, 0, 0], [1.22, 0, 0], 'brightness(.35) blur(8px)');
/* 6 record and confirm */
shot('12_black_pod.jpg', S[5] - 0.2, at(5, 3.4), [1.0, 0, 0], [1.12, -2, 0], 'brightness(.85)', '50% 40%');
shot('19_rain.jpg', at(5, 3.0), S[6] + 0.3, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.35) blur(8px)');
/* 7 pilot: dark farm behind the map */
shot('06_farm.jpg', S[6] - 0.2, S[7] + 0.3, [1.1, 0, 0], [1.16, 0, 0], 'brightness(.3) blur(8px)');
/* 8 impact and market */
shot('01_hook_close.jpg', S[7] - 0.2, at(7, 5.8), [1.04, 0, 0], [1.14, -2, 0], 'brightness(.62)');
shot('15_farmer.jpg', at(7, 5.3), at(7, 10.9), [1.04, 0, 0], [1.12, 0, -2], 'brightness(.66)');
shot('10_pods.jpg', at(7, 10.4), S[8] + 0.4, [1.04, 0, 0], [1.12, 2, 0], 'brightness(.62)');
/* 9 close */
shot('02_hook_close.jpg', S[8] - 0.2, END + 1, [1.2, -2, -1], [1.04, 0, 0], 'sepia(.22) saturate(1.15) brightness(.8) contrast(1.05)');

/* ---------------- overlay system (cards, scenes) ---------------- */
const OV = [];
function ov(html, css, tin, tout, fx = 'up', cls = '', credit = '') {
  const el = document.createElement('div'); el.className = 'ov ' + cls; el.style.cssText = css; el.innerHTML = html; $('#ovl').appendChild(el);
  const o = { el, tin, tout, fx, credit }; OV.push(o); return o;
}
const brand = ov('<svg width="34" height="38" viewBox="0 0 34 38"><path d="M17 2 31 7v11c0 9-6 15-14 18C9 33 3 27 3 18V7z" fill="#2B654F"/><path d="M17 11c-4 3-6 7-5 12 4 0 7-3 8-7 1 4 0 8-3 11" stroke="#9fe0bf" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg><span>KokoShield <small>Weather-guided disease scouting</small></span>', '', 0.2, END - 2.2, 'fade');
brand.el.id = 'brand'; brand.el.dataset.d = 'flex';
const chap = ov('', '', 0.4, END - 2.4, 'fade'); chap.el.id = 'chap';
const cap = ov('', '', 0, END - 2.3, 'none'); cap.el.id = 'cap';
const credEl = document.createElement('div'); credEl.className = 'ov'; credEl.id = 'credit'; $('#ovl').appendChild(credEl);
const prog = document.createElement('div'); prog.className = 'ov'; prog.id = 'prog'; $('#ovl').appendChild(prog);

/* ---------- app-style block map (exact geometry from the Field Desk prototype) ---------- */
const POLY = { A: '68,57 191,39 215,105 181,150 66,142', B: '209,38 362,34 367,133 286,151 232,125', C: '382,40 534,64 558,135 474,160 385,127',
  D: '64,159 181,169 217,236 173,272 80,248 51,216', E: '221,154 287,170 368,151 391,236 319,273 244,250', F: '390,145 474,176 562,152 595,221 550,273 416,255',
  G: '99,267 178,291 222,260 276,292 267,334 121,333', H: '283,290 322,286 405,263 547,291 503,333 291,335' };
const LBL = { A: [137, 73], B: [308, 73], C: [462, 98], D: [113, 205], E: [307, 205], F: [491, 214], G: [185, 320], H: [387, 308] };
const PRI = { A: '#B0452E', D: '#B0452E', G: '#B0452E', B: '#D6A03E', C: '#C8D4BC', E: '#C8D4BC', H: '#C8D4BC', F: 'url(#mclosed)' };
function mapSVG(id, mode, extra = '') {
  let grid = ''; for (let x = 25; x < 650; x += 25) grid += `M${x} 0V357`; for (let y = 25; y < 357; y += 25) grid += `M0 ${y}H650`;
  const blocks = Object.keys(POLY).map(k => {
    const fill = mode === 'priority' ? PRI[k] : (k === 'F' ? 'url(#mclosed)' : '#C8D4BC');
    const dark = mode === 'priority' && ['A', 'D', 'G'].includes(k);
    return `<polygon id="${id}-${k}" points="${POLY[k]}" fill="${fill}" stroke="#EEF0EB" stroke-width="3" stroke-linejoin="round"/>
      <text id="${id}-l${k}" x="${LBL[k][0]}" y="${LBL[k][1]}" text-anchor="middle" dominant-baseline="central" font-size="17" font-weight="800" fill="${dark ? '#fff' : (k === 'F' ? '#67716B' : '#17201C')}" style="paint-order:stroke" stroke="${dark ? '#B0452E' : '#EEF0EB'}" stroke-width="4">${k}</text>`; }).join('');
  return `<svg viewBox="0 0 650 357" style="display:block;width:100%;height:100%;font-family:'Noto Sans','Segoe UI',sans-serif">
  <defs><pattern id="mclosed" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#E3E4E0"/><path d="M0 0v6" stroke="#A9A69F" stroke-width="1.3"/></pattern>
  ${Object.keys(POLY).map(k => `<clipPath id="${id}-c${k}"><polygon points="${POLY[k]}"/></clipPath>`).join('')}</defs>
  <rect width="650" height="357" fill="#EEF0EB"/><path d="${grid}" stroke="#17201C" stroke-opacity=".05" stroke-width="1"/>
  <path d="M610 -8C617 56 565 99 597 141S611 230 627 271 617 326 648 362" stroke="#D3E0EA" stroke-width="10" fill="none"/>
  <path d="M611 -8C617 56 566 99 598 141S611 230 627 271 617 326 648 362" stroke="#7FA0B9" stroke-width="2" fill="none"/>
  <path d="M42 336L46 250 49 151 57 61M42 336L85 347 281 348 547 345M52 148L190 158 297 162 389 133 562 147" fill="none" stroke="#AFB6AA" stroke-width="1.4" stroke-dasharray="5 4"/>
  ${blocks}
  <rect x="36" y="330" width="12" height="12" rx="2" fill="#17201C" stroke="#fff" stroke-width="1.5"/><text x="14" y="321" font-size="12" fill="#56645d" font-weight="700">Gate</text>
  <path d="M621 58L621 30M614 40L621 30 628 40" fill="none" stroke="#17201C" stroke-width="1.6"/><text x="617" y="72" font-size="12" fill="#56645d" font-weight="700">N</text>
  ${extra}</svg>`;
}
const DRONE = `<g class="drone"><ellipse cx="6" cy="9" rx="17" ry="7" fill="#000" opacity=".18"/>
  <path d="M-11 -11L11 11M11 -11L-11 11" stroke="#17201C" stroke-width="3.2" stroke-linecap="round"/>
  ${[[-11, -11], [11, -11], [-11, 11], [11, 11]].map(([x, y]) => `<g transform="translate(${x} ${y})"><circle r="7.5" fill="rgba(255,255,255,.55)" stroke="#17201C" stroke-width="1.2"/><path class="blade" d="M-7 0H7" stroke="#17201C" stroke-width="1.6"/></g>`).join('')}
  <rect x="-5" y="-5" width="10" height="10" rx="2.5" fill="#2B654F" stroke="#fff" stroke-width="1.2"/></g>`;

