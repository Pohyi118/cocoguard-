/* ---------- drone survey (concept): model, flights, block outlines, standing water ---------- */
function makeDrone() {
  const g = new THREE.Group();
  const dark = new THREE.MeshStandardMaterial({ color: '#20262a', roughness: .5, metalness: .3 });
  const green = new THREE.MeshStandardMaterial({ color: '#2B654F', roughness: .45 });
  const body = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.28, 0.6), green); g.add(body);
  const top = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.12, 0.4), dark); top.position.y = 0.2; g.add(top);
  const rotors = [];
  for (const [x, z] of [[0.85, 0.85], [-0.85, 0.85], [0.85, -0.85], [-0.85, -0.85]]) {
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, Math.hypot(x, z), 8), dark);
    arm.position.set(x / 2, 0.05, z / 2); arm.rotation.set(0, -Math.atan2(z, x), Math.PI / 2, 'YXZ'); g.add(arm);
    const motor = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.16, 12), dark); motor.position.set(x, 0.12, z); g.add(motor);
    const disc = new THREE.Mesh(new THREE.CircleGeometry(0.55, 28), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: .16, side: THREE.DoubleSide, depthWrite: false }));
    disc.rotation.x = -Math.PI / 2; disc.position.set(x, 0.22, z); g.add(disc);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.02, 0.08), dark); blade.position.set(x, 0.23, z); g.add(blade); rotors.push(blade);
  }
  const cam = new THREE.Mesh(new THREE.SphereGeometry(0.13, 12, 10), dark); cam.position.set(0.45, -0.18, 0); g.add(cam);
  const led = new THREE.Mesh(new THREE.SphereGeometry(0.06, 8, 6), new THREE.MeshBasicMaterial({ color: '#3fe08f' })); led.position.set(-0.47, 0.05, 0); g.add(led);
  g.userData.rotors = rotors; g.scale.setScalar(1.35); g.traverse(o => { if (o.isMesh) o.castShadow = true; }); g.visible = false; scene.add(g); return g;
}
const drone = makeDrone();
const PAD = W(9, 79);
{ const pad = new THREE.Mesh(new THREE.CylinderGeometry(1.7, 1.7, 0.08, 32), new THREE.MeshStandardMaterial({ color: '#3a4a44', roughness: .9 })); pad.position.copy(PAD).setY(0.04); pad.receiveShadow = true; scene.add(pad);
  const ring = new THREE.Mesh(new THREE.RingGeometry(1.15, 1.32, 32), new THREE.MeshBasicMaterial({ color: '#e9f2ed', side: THREE.DoubleSide })); ring.rotation.x = -Math.PI / 2; ring.position.copy(PAD).setY(0.09); scene.add(ring); }
const LAWN3 = []; [18, 9, 0, -9, -18].forEach((z, r) => { LAWN3.push(new THREE.Vector3(r % 2 ? 30 : -30, 9, z), new THREE.Vector3(r % 2 ? -30 : 30, 9, z)); });
function alongPath(pts, f) {
  const segs = pts.slice(1).map((p, i) => p.distanceTo(pts[i])); const L = segs.reduce((a, b) => a + b, 0); let d = clamp(f) * L;
  for (let i = 0; i < segs.length; i++) { if (d <= segs[i]) { const k = segs[i] ? d / segs[i] : 0; const a = pts[i], b = pts[i + 1]; return { pos: a.clone().lerp(b, k), yaw: Math.atan2(-(b.z - a.z), b.x - a.x) }; } d -= segs[i]; }
  const a = pts[pts.length - 2], b = pts[pts.length - 1]; return { pos: b.clone(), yaw: Math.atan2(-(b.z - a.z), b.x - a.x) };
}
const rowFrac = k => clamp((21 - blocks[k].cen.z) / 42);
const outlines = {}, ripples = {}, waterLbl = {};
for (const k of Object.keys(blocks)) {
  const g = new THREE.BufferGeometry().setFromPoints(blocks[k].pts.map(p => p.clone().setY(0.42)));
  const l = new THREE.LineLoop(g, new THREE.LineBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0, depthTest: false })); l.renderOrder = 6; scene.add(l); outlines[k] = l;
}
for (const k of ['A', 'D', 'G']) {
  ripples[k] = [0, 1].map(() => { const r = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.85, 40), new THREE.MeshBasicMaterial({ color: '#bfe0ff', transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
    r.rotation.x = -Math.PI / 2; r.position.copy(blocks[k].cen).setY(0.4); r.renderOrder = 6; scene.add(r); return r; });
  waterLbl[k] = sprite(labelTex('Standing water', 'rgba(31,111,184,.95)', '#fff', 560, 110, 46, 40), 6.4, 1.26); waterLbl[k].position.copy(blocks[k].cen).setY(7.0);
}
function setWater(k, a, tt) {   /* highlight standing water on a wet block: brighter puddle, ripples, label */
  const b = blocks[k]; if (a > 0.001) { b.pud.material.opacity = Math.max(b.pud.material.opacity, 0.78 * a); b.pud.material.color.set('#3d8fd4'); }
  ripples[k].forEach((r, i) => { const ph = ((tt * 0.8 + i * 0.5) % 1); r.visible = a > 0.01; r.scale.setScalar(1 + ph * 6); r.material.opacity = a * 0.8 * (1 - ph); });
  waterLbl[k].material.opacity = a;
}
function setRain(level, tt) {
  rain.visible = level > 0.01; rain.material.opacity = 0.55 * level; if (!rain.visible) return;
  for (let i = 0; i < N; i++) { const [x, y0, z, sp] = seeds[i]; const y = ((y0 - sp * tt) % 34 + 34) % 34; rp.set([x, y, z, x + 0.25, y + 1.1, z + 0.08], i * 6); }
  rg.attributes.position.needsUpdate = true;
}
function placeDrone(pos, yaw, pitch, spinAngle) {
  drone.visible = true; drone.position.copy(pos); drone.rotation.set(0, yaw, pitch, 'YXZ'); drone.userData.rotors.forEach((r, i) => r.rotation.y = spinAngle + i * 0.7);
}
/* drone chips (HTML), shown only during the drone part of scene 4 */
const dTitle = document.createElement('div'); dTitle.className = 'ov glass'; dTitle.style.cssText = 'left:70px;top:130px;width:800px';
dTitle.innerHTML = '<div class="kick">New · Drone survey (concept)</div><div class="h2" style="font-size:36px">A borrowed university camera drone maps the blocks, then checks for standing water after heavy rain</div>';
const dChip = document.createElement('div'); dChip.className = 'ov chip'; dChip.style.cssText = 'right:60px;top:130px;color:#fff;font-size:24px;box-shadow:0 10px 24px rgba(0,0,0,.3)';
ovl.appendChild(dTitle); ovl.appendChild(dChip);
const DCAM = [[0.0, PAD.clone().add(new THREE.Vector3(-8, 4, 10)), PAD.clone().add(new THREE.Vector3(0, 1.5, 0))],
  [1.9, PAD.clone().add(new THREE.Vector3(-13, 11, 15)), PAD.clone().add(new THREE.Vector3(0, 8, -3))],
  [2.7, new THREE.Vector3(0, 66, 34), new THREE.Vector3(0, 0, 2)], [4.5, new THREE.Vector3(0, 66, 34), new THREE.Vector3(0, 0, 2)],
  [5.2, new THREE.Vector3(-30, 36, 40), new THREE.Vector3(-10, 0, 2)], [6.9, new THREE.Vector3(-34, 32, 30), new THREE.Vector3(-12, 0, 0)],
  [7.6, new THREE.Vector3(NODE.x + 4.6, 4.3, NODE.z + 5.6), new THREE.Vector3(NODE.x, 2.6, NODE.z)]];
function droneUpdate(t4, fixed) {
  for (const k in blocks) blocks[k].pud.material.color.set('#5b86a6');
  for (const k in outlines) outlines[k].material.opacity = 0;
  for (const k of ['A', 'D', 'G']) setWater(k, 0, 0);
  dTitle.style.display = 'none'; dChip.style.display = 'none';
  /* default: parked on its pad once the drone has been introduced (or always in Explore / Your turn) */
  drone.visible = t4 >= S4[3] - 0.5 || exploring || fixed;
  if (drone.visible) placeDrone(PAD.clone().setY(0.45), 0.6, 0, 0);
  if (DRONE_SEG) {
    const u = t4 - S4[3];
    /* flight path: take off, mapping flight, post-rain flight, hover */
    let p, yaw = 0.6, pitch = 0;
    if (u < 2.0) p = { pos: PAD.clone().setY(0.45 + 8.55 * sm((u - 0.3) / 1.7)), yaw: 0.6 };
    else if (u < 2.6) p = { pos: PAD.clone().setY(9).lerp(LAWN3[0], sm((u - 2.0) / 0.6)), yaw: Math.atan2(-(LAWN3[0].z - PAD.z), LAWN3[0].x - PAD.x) };
    else if (u < 4.6) p = alongPath(LAWN3, sm((u - 2.6) / 2.0));
    else if (u < 6.9) p = alongPath(LAWN3, sm((u - 4.7) / 2.2));
    else p = { pos: LAWN3[LAWN3.length - 1].clone().setY(9 + 2 * sm((u - 6.9) / 0.7)), yaw: 0 };
    const moving = u > 2.0 && u < 6.9; pitch = moving ? -0.14 : 0;
    placeDrone(p.pos, p.yaw, pitch, t4 * 60);
    /* block outlines and letters appear as flight 1 passes over them */
    const f1 = sm((u - 2.6) / 2.0), f2 = u >= 4.7 ? sm((u - 4.7) / 2.2) : 0, fade = 1 - ramp(u, 7.0, 7.6);
    for (const k in outlines) { const a = clamp((f1 - rowFrac(k)) * 6) * fade; outlines[k].material.opacity = a; letters[k].material.opacity = a; }
    /* light rain and the second flight finds standing water in A, D and G */
    setRain(0.5 * Math.min(ramp(u, 4.4, 5.0), 1 - ramp(u, 6.8, 7.4)), t4);
    for (const k of ['A', 'D', 'G']) setWater(k, clamp((f2 - rowFrac(k)) * 5) * fade, t4);
    /* camera */
    if (!exploring) { let i = 0; while (i < DCAM.length - 1 && DCAM[i + 1][0] <= u) i++; const a = DCAM[i], b = DCAM[Math.min(i + 1, DCAM.length - 1)];
      const k = b[0] > a[0] ? sm((u - a[0]) / (b[0] - a[0])) : 0; camera.position.copy(a[1]).lerp(b[1], k); camera.lookAt(a[2].clone().lerp(b[2], k)); camera.setViewOffset(1920, 1080, 0, 0, 1920, 1080); }
    /* chips */
    const tv = Math.min(eo((u - 0.3) / 0.5), 1 - ei((u - 4.0) / 0.4));
    if (tv > 0.001) { dTitle.style.display = 'block'; dTitle.style.opacity = tv; dTitle.style.transform = `translateX(${-(1 - tv) * 80}px)`; }
    const cv = Math.min(eo((u - 0.4) / 0.5), 1 - ei((u - 7.2) / 0.4));
    if (cv > 0.001) {
      dChip.style.display = 'inline-flex'; dChip.style.opacity = cv;
      dChip.textContent = u < 2.6 ? 'Borrowed UM camera drone · concept' : u < 4.7 ? (f1 >= 1 ? '✓ Block map ready · 8 blocks' : 'Flight 1 · mapping the blocks') : (f2 >= 1 ? 'Wet blocks found: A, D, G → ranked first' : 'Flight 2 · after 48 mm of rain');
      dChip.style.background = u < 4.7 ? '#2B654F' : '#1f6fb8';
    }
  } else if (exploring && !fixed) {
    const now = performance.now() / 1000; placeDrone(new THREE.Vector3(2, 11 + 0.4 * Math.sin(now * 1.6), 4), now * 0.3, 0, now * 40);
  }
}
