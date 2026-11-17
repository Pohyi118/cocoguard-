"""Record real interaction footage from prototype/KokoShield_Prototype.html, frame by frame at 30 fps.
Real mouse moves/clicks drive the app; a visible cursor (desktop) or touch dot (phone) is drawn on top.
The page clock is controlled, so timers, toasts and the walk countdown advance exactly 1/30 s per frame.
Usage: python record_proto.py [clip ...]   (clips: plan, sensor, compare, walk, log, rice)"""
import sys, pathlib, math
from playwright.sync_api import sync_playwright
URL = pathlib.Path("C:/Users/User/Documents/GSC/prototype/KokoShield_Prototype.html").as_uri()
OUT = pathlib.Path(__file__).parent / "stage/assets/rec"
FPS = 30
CURSOR_JS = r"""
(() => { if (window.__cur) return;
  const c = document.createElement('div'); c.id = '__cur';
  c.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;will-change:transform';
  c.innerHTML = window.__touch
    ? '<div style="width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(255,255,255,.45);border:2.5px solid rgba(23,32,28,.55);box-shadow:0 2px 10px rgba(0,0,0,.25)"></div>'
    : '<svg width="26" height="30" viewBox="0 0 26 30" style="filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))"><path d="M2 2v22l6-5.5 4 9 4-1.8-4-8.8h8.2z" fill="#fff" stroke="#17201C" stroke-width="1.8" stroke-linejoin="round"/></svg>';
  const r = document.createElement('div'); r.id = '__rip';
  r.style.cssText = 'position:fixed;z-index:2147483646;pointer-events:none;border-radius:50%;border:3px solid #2B654F;width:10px;height:10px;opacity:0';
  document.documentElement.append(r, c);
  window.__cur = (x, y, vis, ripAge, rx, ry) => {
    c.style.transform = `translate(${x}px,${y}px)`; c.style.opacity = vis;
    if (ripAge >= 0 && ripAge < 0.45) { const k = ripAge / 0.45, s = 10 + 46 * k;
      r.style.left = (rx - s / 2) + 'px'; r.style.top = (ry - s / 2) + 'px'; r.style.width = r.style.height = s + 'px'; r.style.opacity = (1 - k) * 0.9; }
    else r.style.opacity = 0;
  };
})();
"""
sm = lambda x: 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)

def run(pw, name, *, mobile, dur, path, actions, setup=None, vis=None):
    """path: [(t, target)] where target is (x, y) or a CSS selector (centre of its box); actions: [(t, kind, arg...)]."""
    b = pw.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1440, "height": 900},
                        device_scale_factor=2 if mobile else 1.5, is_mobile=mobile, has_touch=mobile, locale="en-GB", timezone_id="Asia/Kuala_Lumpur")
    pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.clock.install(time="2026-11-17T08:05:00+08:00")
    pg.goto(URL); pg.clock.run_for(1500)
    if setup: setup(pg)
    pg.evaluate(f"window.__touch={'true' if mobile else 'false'}"); pg.evaluate(CURSOR_JS)
    def pos(target):
        if isinstance(target, str):
            bb = pg.locator(target).first.bounding_box(); return (bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
        return target
    d = OUT / name; d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("*.jpg"): f.unlink()
    acts = sorted(actions, key=lambda a: a[0]); done = set(); last_click = (-9, 0, 0)
    pts = []  # resolved lazily so selectors are measured when the cursor heads for them
    n = int(round(dur * FPS))
    for i in range(n):
        t = i / FPS
        # resolve path segment
        k = max(j for j in range(len(path)) if path[j][0] <= t) if t >= path[0][0] else 0
        if len(pts) <= k + 1:
            while len(pts) < min(len(path), k + 2): pts.append(pos(path[len(pts)][1]))
        if k + 1 < len(path):
            t0, t1 = path[k][0], path[k + 1][0]; a = sm((t - t0) / max(1e-6, t1 - t0)) if t >= t0 else 0
            # gentle arc so moves look hand-made
            x = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * a; y = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * a - math.sin(math.pi * a) * 18
        else: x, y = pts[k]
        if not mobile: pg.mouse.move(x, y)
        for j, act in enumerate(acts):
            if j in done or act[0] > t + 1e-6: continue
            done.add(j); kind = act[1]
            if kind == "click":
                if mobile: pg.locator(act[2]).first.tap() if len(act) > 2 else pg.touchscreen.tap(x, y)
                else: pg.mouse.click(x, y)
                last_click = (t, x, y)
            elif kind == "select": pg.locator(act[2]).first.select_option(act[3])
            elif kind == "scroll": pass
            elif kind == "advance": pg.clock.run_for(act[2])
        for act in acts:   # smooth scrolls: (t0, 'scroll', t1, y0, y1)
            if act[1] == "scroll" and act[0] <= t <= act[2] + 1 / FPS:
                yy = act[3] + (act[4] - act[3]) * sm((t - act[0]) / (act[2] - act[0])); pg.evaluate(f"window.scrollTo(0,{yy})")
        v = 1.0 if vis is None else vis(t)
        pg.evaluate(f"window.__cur({x:.1f},{y:.1f},{v},{t - last_click[0]:.3f},{last_click[1]:.1f},{last_click[2]:.1f})")
        pg.screenshot(path=str(d / f"f{i:04d}.jpg"), type="jpeg", quality=88)
        pg.clock.run_for(1000 // FPS)
    print(f"{name}: {n} frames, errors {errs[:2]}"); b.close()

def plan(pw):   # 17.4 s: rain card -> map blocks -> usual vs priority -> route list -> Start scouting
    run(pw, "plan", mobile=False, dur=17.4,
        path=[(0, (1500, 960)), (1.5, (1300, 205)), (6.6, (1300, 210)), (7.4, (240, 380)), (8.3, (232, 525)), (9.2, (310, 655)), (10.0, (245, 382)), (10.7, (245, 382)),
              (11.3, 'select[data-set-select="method"]'), (13.4, (1240, 370)), (14.2, (1240, 427)), (15.0, '[data-act="walk-start"]'), (17.4, '[data-act="walk-start"]')],
        actions=[(10.2, "click"), (11.75, "select", 'select[data-set-select="method"]', "usual"), (12.9, "select", 'select[data-set-select="method"]', "ranked"), (15.6, "click")])

def sensor(pw):   # 2.8 s: Sensor node page, toggle Exploded
    run(pw, "sensor", mobile=False, dur=2.8, setup=lambda pg: (pg.locator('[data-act="view-hardware"]').first.click(), pg.clock.run_for(600)),
        path=[(0, (760, 640)), (0.9, '[data-set="explode"][data-val="1"]'), (2.8, '[data-set="explode"][data-val="1"]')], actions=[(1.1, "click")])

def compare(pw):   # 5.4 s: Compare page, slow scroll to the measures table
    run(pw, "compare", mobile=False, dur=5.4, setup=lambda pg: (pg.locator('[data-act="view-compare"]').first.click(), pg.clock.run_for(600)),
        path=[(0, (1500, 700)), (1.0, (205, 598)), (2.4, (530, 598)), (5.4, (560, 600))], actions=[(2.6, "scroll", 5.2, 0, 330)])

def walk(pw):   # 6.0 s phone: Stop 1 Block A -> Found -> 3 pods -> Save -> Stop 2
    def setup(pg):
        pg.locator('[data-act="walk-start"]').first.tap(); pg.clock.run_for(2 * 60 * 1000 + 5000)
    run(pw, "walk", mobile=True, dur=6.0, setup=setup,
        path=[(0, (300, 700)), (0.8, '[data-act="walk-found"]'), (1.5, '[data-act="walk-found"]'), (1.7, '[data-step="1"]'), (2.6, '[data-step="1"]'),
              (2.9, '[data-act="walk-save"]'), (3.6, '[data-act="walk-save"]'), (4.4, (300, 760))],
        actions=[(1.0, "click", '[data-act="walk-found"]'), (1.95, "click", '[data-step="1"]'), (2.4, "click", '[data-step="1"]'), (3.25, "click", '[data-act="walk-save"]')],
        vis=lambda t: max(0.0, min(1.0, 1 - abs(t - 2.1) / 2.0 + 0.4)) if t < 4.2 else max(0.0, 1 - (t - 4.2) / 0.4))

def log(pw):   # 4.8 s: Scout log, confirm the two pending cases from today's round
    run(pw, "log", mobile=False, dur=4.8, setup=lambda pg: (pg.locator('[data-act="view-log"]').first.click(), pg.clock.run_for(600)),
        path=[(0, (700, 860)), (1.1, '[data-act^="confirm:"] >> nth=0'), (2.4, '[data-act^="confirm:"] >> nth=0'), (3.0, '[data-act^="confirm:"] >> nth=0'), (4.8, (900, 470))],
        actions=[(1.3, "click"), (3.15, "click")])

def rice(pw):   # still: phone Field plan with the rice blast profile (Hangzhou demo paddy)
    b = pw.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(800); pg.locator("#crop").select_option("rice"); pg.wait_for_timeout(3800)
    d = OUT / "rice"; d.mkdir(parents=True, exist_ok=True); pg.screenshot(path=str(d / "f0000.jpg"), type="jpeg", quality=90); print("rice: still"); b.close()

CLIPS = dict(plan=plan, sensor=sensor, compare=compare, walk=walk, log=log, rice=rice)
with sync_playwright() as pw:
    for nm in (sys.argv[1:] or CLIPS): CLIPS[nm](pw)
