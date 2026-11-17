"""Apply the v3 motion + interaction upgrades to KokoShield_3D/index.html (idempotency guarded by a marker)."""
import pathlib, re, shutil
P = pathlib.Path("C:/Users/User/Documents/GSC/KokoShield_3D/index.html")
s = P.read_text(encoding="utf-8")
assert "KS_V3" not in s, "already patched"
shutil.copy(P, P.with_name("index_v2_backup.html"))

def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:80])
    s = s.replace(a, b)

# ---------- CSS ----------
rep("#ctl{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);display:flex;gap:8px;align-items:center;background:rgba(10,20,16,.86);color:#fff;border-radius:14px;padding:10px 14px;font-size:14px;z-index:5;transition:opacity .3s;flex-wrap:wrap;justify-content:center;max-width:96vw}\n#ctl button{background:#21352c;color:#fff;border:1px solid #3d5a4c;border-radius:9px;padding:7px 11px;font:600 13px 'Noto Sans','Segoe UI',sans-serif;cursor:pointer}\n#ctl button.on{background:#2B654F;border-color:#9fe0bf}\n#ctl input[type=range]{width:220px}\n#start{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:6;background:rgba(6,14,10,.55)}\n#start button{font:800 30px 'Noto Sans','Segoe UI',sans-serif;background:#2B654F;color:#fff;border:0;border-radius:18px;padding:22px 44px;cursor:pointer;box-shadow:0 18px 40px rgba(0,0,0,.4)}\n#start p{color:#dfeee6;font-size:17px;text-align:center;margin-top:14px}\nbody.video #ctl,body.video #start{display:none}",
"""/* KS_V3 */
.w{display:inline-block;will-change:transform,opacity}
.big,#mins,#mm,#farms,#cfound{font-variant-numeric:tabular-nums}
#flash{position:absolute;inset:0;background:#eef6ff;opacity:0;pointer-events:none}
#wipe{position:absolute;top:-220px;left:0;width:2600px;height:1520px;background:linear-gradient(90deg,#123527 0%,#2B654F 38%,#2B654F 62%,#123527 100%);display:none;align-items:center;justify-content:center;pointer-events:none;z-index:3}
#wipe svg{transform:skewX(16deg)}
.panel{position:absolute;right:40px;top:96px;width:620px;z-index:4;color:#fff;background:rgba(12,32,24,.9);border-radius:24px;padding:26px 30px;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.panel .lbl{color:#d6e9df;font-size:22px}
.panel button,#cta button,#start button{font:700 21px 'Noto Sans','Segoe UI',sans-serif;min-height:56px;padding:0 20px;border-radius:14px;border:2px solid #3d5a4c;background:#21352c;color:#fff;cursor:pointer}
.panel button.primary,#cta button.primary,#start button.primary{background:#2B654F;border-color:#9fe0bf}
.panel button:hover,#cta button:hover,#start button:hover{border-color:#9fe0bf}
button:focus-visible,input:focus-visible{outline:4px solid #9fe0bf;outline-offset:2px}
.blocks{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;margin:14px 0 10px}
.blocks button{padding:0;font-size:24px;font-weight:800}
.blocks button.sel{background:#2f8fd8;border-color:#bfe0ff}
.blocks button.closed{opacity:.5;text-decoration:line-through}
.budget{height:16px;background:rgba(255,255,255,.15);border-radius:8px;overflow:hidden;margin:6px 0 6px}
#cbar{height:100%;width:0;background:#2f8fd8;transition:width .25s}
#clist{margin:8px 0 12px;padding-left:30px;font-size:21px;line-height:1.5;min-height:34px}
.btns{display:flex;gap:10px;flex-wrap:wrap}
.tog{display:flex;align-items:center;gap:12px;font-size:21px;margin-top:12px;cursor:pointer}
.tog input{width:26px;height:26px;accent-color:#2f8fd8}
#cres{margin-top:12px;background:rgba(255,255,255,.08);border-radius:16px;padding:16px 18px;font-size:21px;line-height:1.45}
#toast{position:absolute;left:50%;bottom:150px;transform:translateX(-50%);background:rgba(8,16,12,.92);color:#fff;font-size:26px;font-weight:700;padding:14px 26px;border-radius:14px;opacity:0;transition:opacity .2s;z-index:6;pointer-events:none;white-space:nowrap}
#info .close{position:absolute;right:14px;top:12px;min-height:56px;min-width:56px;padding:0;font-size:32px;line-height:1}
#cta{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(6,14,10,.45);z-index:5}
#cta .box{background:rgba(12,32,24,.95);color:#fff;border-radius:26px;padding:40px 50px;text-align:center;max-width:980px}
#cta .btns,#start .btns{justify-content:center;margin-top:24px}
#ctl{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);display:flex;gap:8px;align-items:center;background:rgba(10,20,16,.9);color:#fff;border-radius:16px;padding:8px 12px;font-size:14px;z-index:7;transition:opacity .3s;flex-wrap:wrap;justify-content:center;max-width:96vw}
#ctl button{display:inline-flex;align-items:center;gap:8px;min-height:44px;min-width:44px;background:#21352c;color:#fff;border:1px solid #3d5a4c;border-radius:10px;padding:0 13px;font:700 14px 'Noto Sans','Segoe UI',sans-serif;cursor:pointer}
#ctl button[aria-pressed=true],#ctl button[aria-current=true]{background:#2B654F;border-color:#9fe0bf}
#ctl input[type=range]{width:200px;height:44px;accent-color:#9fe0bf}
#start{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:8;background:rgba(6,14,10,.6)}
#start button{font-size:26px;min-height:64px;padding:0 32px;margin:0 6px}
#start p{color:#dfeee6;font-size:17px;text-align:center;margin-top:16px}
[hidden]{display:none!important}
body.video #ctl,body.video #start,body.video #chal,body.video #info,body.video #toast,body.video #cta{display:none!important}""")

# ---------- markup ----------
rep("""<canvas id="gl" width="1920" height="1080"></canvas>
<div id="ovl"></div>
</div></div>
<div id="start"><div><button id="startBtn">▶ Play the KokoShield story</button><p>Narrated, about 2 minutes · Pause any time to explore the 3D farm</p></div></div>
<div id="ctl">
 <button id="pp">❚❚ Pause</button>
 <span id="chips"></span>
 <input id="seek" type="range" min="0" max="119.5" step="0.1" value="0">
 <span id="tm">0:00</span>
 <button id="explore">Explore 3D</button>
</div>""",
"""<canvas id="gl" width="1920" height="1080" aria-label="3D model of a demo cocoa farm"></canvas>
<div id="flash"></div>
<div id="ovl"></div>
<div id="wipe"><svg width="150" height="168" viewBox="0 0 34 38" aria-hidden="true"><path d="M17 2 31 7v11c0 9-6 15-14 18C9 33 3 27 3 18V7z" fill="#ffffff"/><path d="M17 11c-4 3-6 7-5 12 4 0 7-3 8-7 1 4 0 8-3 11" stroke="#2B654F" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg></div>
<div id="chal" class="panel" hidden role="region" aria-label="Your turn challenge">
 <div class="kick">Your turn</div>
 <div class="h2" style="font-size:38px">Plan the 30-minute round</div>
 <p class="lbl" style="margin:8px 0 0">48 mm of rain fell overnight. Pick blocks in the order you'd walk them, on the farm or with the buttons. Can you find the black pod?</p>
 <div id="cblocks" class="blocks" role="group" aria-label="Add a block to your route"></div>
 <div class="budget" aria-hidden="true"><div id="cbar"></div></div>
 <div id="cmin" class="lbl" aria-live="polite">0 of 30 min used</div>
 <ol id="clist"></ol>
 <div class="btns"><button id="cwalk" class="primary">Walk my route</button><button id="cks" class="primary" hidden>Watch KokoShield's route</button><button id="cundo">Undo</button><button id="creset">Try again</button><button id="cback">Back to story</button></div>
 <div id="clive" class="lbl" style="margin-top:10px" aria-live="polite" hidden>Walking… found <b id="cfound">0</b> of 7</div>
 <label class="tog"><input type="checkbox" id="chint"> Show KokoShield's signals</label>
 <div id="cres" hidden aria-live="polite"></div>
</div>
<div id="info" class="panel" hidden role="dialog" aria-label="Details"><button id="infoclose" class="close" aria-label="Close details">×</button><div id="infobody"></div></div>
<div id="toast" role="status" aria-live="polite"></div>
<div id="cta" hidden><div class="box"><div class="kick">That was KokoShield</div><div class="h2">Your turn: can you beat the ranked route?</div><div class="btns"><button id="ctaCh" class="primary">Try the challenge</button><button id="ctaEx">Explore the 3D farm</button><button id="ctaRe">Replay</button></div></div></div>
</div></div>
<div id="start"><div><div class="btns"><button id="startBtn" class="primary">Play the KokoShield story</button><button id="startCh">Try the challenge</button></div><p>Narrated with music, about 2 minutes. Explore 3D lets you orbit the farm and click blocks.</p></div></div>
<div id="ctl" role="toolbar" aria-label="Story controls">
 <button id="pp" aria-label="Play the story"></button>
 <span id="chips" role="group" aria-label="Chapters" style="display:flex;gap:6px;flex-wrap:wrap"></span>
 <input id="seek" type="range" min="0" max="119.5" step="0.1" value="0" aria-label="Story position">
 <span id="tm">0:00</span>
 <button id="explore" aria-pressed="false">Explore 3D</button>
 <button id="challenge" aria-pressed="false">Your turn</button>
</div>""")

# ---------- JS: helpers ----------
rep("if (VIDEO) document.body.classList.add('video');",
    "if (VIDEO) document.body.classList.add('video');\nconst REDUCED = !VIDEO && matchMedia('(prefers-reduced-motion: reduce)').matches;")
rep("const C = h => new THREE.Color(h);",
    "const C = h => new THREE.Color(h);\nconst eo = x => 1 - Math.pow(1 - clamp(x), 3);            /* decelerate: entering */\nconst ei = x => clamp(x) * clamp(x);                      /* accelerate: leaving */\nconst bo = x => { x = clamp(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };  /* spring-like overshoot */")
rep('<div id="which" class="h2" style="margin-top:18px;opacity:0">', '<div id="which" class="h2" data-at="5.4" style="margin-top:18px;opacity:0">')
rep('<div style="margin-top:10px;font-size:23px;color:#cfe6da">📍 Tanjung Sepat',
    '<div style="margin-top:10px;font-size:23px;color:#cfe6da"><svg width="18" height="22" viewBox="0 0 24 30" style="vertical-align:-4px;margin-right:8px" aria-hidden="true"><path d="M12 1C6 1 2 5.5 2 11c0 7.5 10 18 10 18s10-10.5 10-18C22 5.5 18 1 12 1z" fill="#9fe0bf"/><circle cx="12" cy="11" r="4" fill="#0c2018"/></svg>Tanjung Sepat')

# kinetic headlines, lightning, wipe (after the last overlay)
rep("/* ---------- interaction state ---------- */",
"""/* kinetic headlines: split into words, revealed with a short stagger */
function splitWords(root) {
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const nodes = []; while (tw.nextNode()) nodes.push(tw.currentNode);
  const out = [];
  nodes.forEach(nd => { const frag = document.createDocumentFragment();
    nd.textContent.split(/(\\s+)/).forEach(p => { if (!p) return; if (/^\\s+$/.test(p)) frag.appendChild(document.createTextNode(p)); else { const w = document.createElement('span'); w.className = 'w'; w.textContent = p; frag.appendChild(w); out.push(w); } });
    nd.parentNode.replaceChild(frag, nd); });
  return out;
}
OV.forEach(o => { const hs = o.el.querySelectorAll('.h1,.h2'); if (!hs.length) return; o.words = [];
  hs.forEach(h => { const at = h.dataset.at ? +h.dataset.at : null; splitWords(h).forEach((w, j) => { w._at = at; w._j = j; o.words.push(w); }); }); });
const flashEl = document.getElementById('flash'), wipeEl = document.getElementById('wipe');
const FLASHES = [4.6, S[1] + 5.5];
function flashAt(t) { if (REDUCED) return 0; let v = 0; for (const f of FLASHES) { const d = t - f; v = Math.max(v, 0.85 * Math.exp(-((d / 0.045) ** 2)), 0.55 * Math.exp(-(((d - 0.17) / 0.05) ** 2)), 0.25 * Math.exp(-(((d - 0.32) / 0.08) ** 2))); } return v; }

/* ---------- interaction state ---------- */""")

# ---------- JS: update() ----------
rep("  hemi.intensity = lerp(0.95, 0.65, rainL);",
    "  hemi.intensity = lerp(0.95, 0.65, rainL);\n  const fl = flashAt(t); hemi.intensity += fl * 1.6; skyU.top.value.lerp(C('#e8f0ff'), fl * 0.6); skyU.bot.value.lerp(C('#ffffff'), fl * 0.5); flashEl.style.opacity = (fl * 0.55).toFixed(3);")
rep("const z = 2.6 * (0.6 + 0.4 * sm(a)); s.scale.set(z, z, 1);", "const z = 2.6 * (0.5 + 0.5 * bo(a)); s.scale.set(z, z, 1);")
rep("const bob = Math.abs(Math.sin(t * 9)) * 0.12;", "const bob = REDUCED ? 0 : Math.abs(Math.sin(t * 9)) * 0.12;")
rep("    let vis = o.fx === 'none' ? 1 : win(t, o.tin, o.tout, 0.55);",
    "    let vis = o.fx === 'none' ? 1 : Math.min(eo((t - o.tin) / 0.55), 1 - ei((t - o.tout + 0.35) / 0.35));")
rep("    const k = 1 - sm(vis); let tr = '';", "    const k = 1 - vis; let tr = '';")
rep("    if (o === cap) tr = 'translateX(-50%)';\n    o.el.style.transform = tr;\n  }",
    "    if (o === cap) tr = 'translateX(-50%)';\n    o.el.style.transform = tr;\n    if (o.words) o.words.forEach(w => { const a = REDUCED ? 1 : eo((t - (w._at ?? o.tin) - 0.12 - w._j * 0.05) / 0.4); w.style.opacity = a; w.style.transform = a >= 1 ? '' : `translateY(${(1 - a) * 22}px)`; });\n  }\n  /* brand wipe between scenes */\n  let wp = -1; for (let k = 1; k < 8; k++) if (Math.abs(t - S[k]) < 0.42) wp = (t - S[k] + 0.42) / 0.84;\n  if (wp >= 0 && !REDUCED) { wipeEl.style.display = 'flex'; wipeEl.style.transform = `translateX(${-3050 + wp * 5420}px) skewX(-16deg)`; } else wipeEl.style.display = 'none';")
rep("$(s).style.transform = `scale(${0.7 + 0.3 * a})`;", "$(s).style.transform = `scale(${0.6 + 0.4 * bo(a)})`;")
rep("const g = $('#d' + i); g.setAttribute('opacity', a); });",
    "const g = $('#d' + i); g.setAttribute('opacity', a); const cx = X(d[1]), cy = Y(d[2]), z = 0.3 + 0.7 * bo(a); g.setAttribute('transform', `translate(${cx} ${cy}) scale(${z}) translate(${-cx} ${-cy})`); });")
rep("$('#ks').setAttribute('opacity', ka);",
    "$('#ks').setAttribute('opacity', ka); { const cx = X(8.6), cy = Y(8.2), z = 0.4 + 0.6 * bo(ka); $('#ks').setAttribute('transform', `translate(${cx} ${cy}) scale(${z}) translate(${-cx} ${-cy})`); }")

# ---------- JS: frame hook ----------
rep("function frame(tt) { update(tt); if (exploring) controls.update(); renderer.render(scene, camera); }",
    "let postUpdate = null;\nfunction frame(tt) { update(tt); if (postUpdate) postUpdate(); if (exploring) controls.update(); renderer.render(scene, camera); }")

# ---------- JS: interactive block (player, explore hotspots, challenge) ----------
i0 = s.index("if (!VIDEO) {\n  const audio = new Audio('assets/narration.m4a');")
i1 = s.index("</script>\n</body>")
s = s[:i0] + pathlib.Path("C:/Users/User/Documents/GSC/video/interactive_v3.js").read_text(encoding="utf-8") + "\n" + s[i1:]
P.write_text(s, encoding="utf-8")
print("patched", len(s), "chars")
