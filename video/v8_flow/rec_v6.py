"""Record the KokoShield prototype as full-screen clips (CDP screencast -> constant 30 fps MP4) with an event log.
Each clip: rec/<name>.mp4 and rec/<name>.json {"marks": {label: t}, "boxes": {label: [x, y, w, h]} in video pixels}.
Run: python rec_v6.py [clip ...]   (default: all clips)"""
import base64, json, pathlib, subprocess, sys, time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 30
HERE = pathlib.Path(__file__).parent; OUT = HERE / "rec"; OUT.mkdir(exist_ok=True)
URL = (HERE.parent.parent / "prototype/KokoShield_Prototype.html").resolve().as_uri()
DESK = dict(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
PHONE = dict(viewport={"width": 412, "height": 892}, device_scale_factor=2, is_mobile=True, has_touch=True)


class Rec:
    def __init__(self, pg, scale):
        self.pg, self.scale, self.frames, self.marks, self.boxes = pg, scale, [], {}, {}
        self.cdp = pg.context.new_cdp_session(pg)
        self.cdp.on("Page.screencastFrame", self._frame)
        vp = pg.viewport_size
        self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "everyNthFrame": 1,
                                                "maxWidth": vp["width"] * scale, "maxHeight": vp["height"] * scale})
        self.t0 = None

    def _frame(self, p):
        self.cdp.send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})
        ts = p["metadata"]["timestamp"]
        if self.t0 is None: self.t0 = ts
        self.frames.append((ts - self.t0, base64.b64decode(p["data"])))

    def now(self):
        return (time.time() - self.wall0) if self.t0 is None else time.time() - self.wall0

    def wait(self, s):
        self.pg.wait_for_timeout(int(s * 1000))

    def mark(self, label):
        self.marks[label] = round(time.time() - self.wall0, 3)

    def box(self, label, selector=None, text=None, nth=0):
        loc = self.pg.get_by_text(text, exact=True).nth(nth) if text else self.pg.locator(selector).nth(nth)
        b = loc.bounding_box()
        self.boxes[label] = [round(v * self.scale) for v in (b["x"], b["y"], b["width"], b["height"])]

    def stop(self, name):
        self.cdp.send("Page.stopScreencast")
        # Align wall clock with the first screencast frame: frame 0 is the page as it was when recording started.
        frames = self.frames; dur = time.time() - self.wall0
        enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "14", str(OUT / f"{name}.mp4")],
                               stdin=subprocess.PIPE)
        j = 0
        for i in range(int(dur * FPS)):
            t = i / FPS
            while j + 1 < len(frames) and frames[j + 1][0] <= t: j += 1
            enc.stdin.write(frames[j][1])
        enc.stdin.close(); enc.wait()
        json.dump({"marks": self.marks, "boxes": self.boxes, "duration": round(dur, 2), "size": None},
                  open(OUT / f"{name}.json", "w"), indent=1)
        print(f"{name}: {dur:.1f}s, {len(frames)} screencast frames, marks {self.marks}")


def session(p, kind, setup=None):
    b = p.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(**kind); pg = ctx.new_page()
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.goto(URL); pg.wait_for_timeout(1500)
    if setup: setup(pg); pg.wait_for_timeout(1200)
    pg.mouse.move(-10, -10)
    r = Rec(pg, kind["device_scale_factor"]); r.wall0 = time.time(); pg.wait_for_timeout(300)
    return b, pg, r


def set_scenario(v): return lambda pg: pg.select_option("select[data-set-select=scenario]", v)


# ---------------- clips ----------------
def plan_activate(p):  # routine -> wet spell: rain card flips, route redraws A D B G
    b, pg, r = session(p, DESK, set_scenario("normal"))
    r.wait(1.5); r.mark("switch"); pg.select_option("select[data-set-select=scenario]", "wet"); r.wait(4.0)
    r.boxes.update(boxes_plan(pg)); r.stop("plan_activate"); b.close()


def boxes_plan(pg):
    out = {}
    js = """() => { const R = e => { const b = e.getBoundingClientRect(); return [b.x, b.y, b.width, b.height].map(Math.round); };
      const aside = document.querySelector('aside, .side, .panel'); const res = {};
      const rows = [...document.querySelectorAll('li, .stop, [data-stop]')].filter(e => /min$/.test(e.innerText.trim()) && e.getBoundingClientRect().x > 1500);
      rows.slice(0, 4).forEach((e, i) => res['row' + (i + 1)] = R(e));
      const wc = [...document.querySelectorAll('div,section')].find(e => /rain in 24 h/.test(e.innerText) && e.getBoundingClientRect().height < 140 && e.getBoundingClientRect().x > 1500);
      if (wc) res.raincard = R(wc);
      const det = [...document.querySelectorAll('div,section')].find(e => /^Block A/.test(e.innerText.trim()) && e.getBoundingClientRect().y > 850 && e.getBoundingClientRect().height < 160);
      if (det) res.detail = R(det);
      const map = document.querySelector('svg.map'); if (map) res.map = R(map);
      const route = [...document.querySelectorAll('div,section')].find(e => /^Today.s route/.test(e.innerText.trim()) && e.getBoundingClientRect().x > 1500 && e.getBoundingClientRect().height < 420);
      if (route) res.route = R(route);
      return res; }"""
    out.update(pg.evaluate(js)); return out


def plan_route(p):  # wet spell: click stops 1..4 so the map and the detail card show each stop's reason
    b, pg, r = session(p, DESK)
    r.boxes.update(boxes_plan(pg)); r.wait(1.0)
    for i, blk in enumerate("ADBG", 1):
        r.mark(f"stop{i}"); pg.mouse.click(*center(r.boxes[f"row{i}"])); r.wait(1.6)
    pg.mouse.move(-10, -10); r.wait(0.8)
    r.stop("plan_route"); b.close()


def center(bx): return bx[0] + bx[2] / 2, bx[1] + bx[3] / 2


def walk_phone(p):  # phone: Field plan -> Start scouting -> walk screen -> Found black pod -> 1 pod -> Save
    b, pg, r = session(p, PHONE)
    r.wait(0.6); r.mark("start"); pg.get_by_text("Start scouting", exact=True).first.click(); r.wait(2.5)
    r.box("check", text="What to check"); r.box("offline", text="Saved offline")
    r.mark("found"); pg.get_by_text("Found black pod", exact=True).first.click(); r.wait(1.4)
    r.mark("plus"); pg.get_by_text("+", exact=True).first.click(); r.wait(1.0)
    r.mark("save"); pg.get_by_text("Save", exact=True).first.click(); r.wait(2.0)
    r.stop("walk_phone"); b.close()


def log_confirm(p):  # scout log: confirm the block A case
    b, pg, r = session(p, DESK, lambda pg: pg.get_by_text("Scout log", exact=True).first.click())
    row = pg.locator("tr, [role=row], li, div").filter(has_text="Brown lesions on lower pods").last
    bb = row.bounding_box(); r.boxes["rowA"] = [round(v) for v in (bb["x"], bb["y"], bb["width"], bb["height"])]
    btn = pg.get_by_text("Confirm", exact=True).first; bb = btn.bounding_box()
    r.boxes["confirmA"] = [round(v) for v in (bb["x"], bb["y"], bb["width"], bb["height"])]
    r.wait(1.5); pg.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2, steps=20); r.wait(0.5)
    r.mark("confirm"); btn.click(); r.wait(3.0)
    r.stop("log_confirm"); b.close()


def compare(p):
    b, pg, r = session(p, DESK, lambda pg: pg.get_by_text("Compare", exact=True).first.click())
    js = """() => { const R = e => { const b = e.getBoundingClientRect(); return [b.x, b.y, b.width, b.height].map(Math.round); };
      const find = (re, maxH) => [...document.querySelectorAll('div,section,table,tr,p')].filter(e => re.test(e.innerText.trim()) && e.getBoundingClientRect().height < maxH).pop();
      const res = {}; const pr = find(/^Priority route/, 600), us = find(/^Usual round/, 600);
      if (pr) res.priority = R(pr); if (us) res.usual = R(us);
      const t = document.querySelector('table'); if (t) res.table = R(t);
      [...document.querySelectorAll('tr')].forEach(tr => { const k = tr.innerText.trim().split('\\n')[0].split('\\t')[0];
        if (/Pods found/.test(k)) res.row_found = R(tr); if (/Blocks with disease/.test(k)) res.row_missed = R(tr); });
      const n = find(/^The pilot measures/, 60); if (n) res.note = R(n); return res; }"""
    r.boxes.update(pg.evaluate(js)); r.wait(12.0); r.stop("compare"); b.close()


def rice(p):  # wet spell on cocoa, then switch the crop profile to rice
    b, pg, r = session(p, DESK)
    r.wait(1.2); r.mark("switch"); pg.select_option("#crop", "rice"); r.wait(4.0)
    r.boxes.update(boxes_plan(pg)); r.box("crop", "#crop"); r.stop("rice"); b.close()


CLIPS = dict(plan_activate=plan_activate, plan_route=plan_route, walk_phone=walk_phone, log_confirm=log_confirm, compare=compare, rice=rice)
if __name__ == "__main__":
    with sync_playwright() as p:
        for n in (sys.argv[1:] or CLIPS):
            CLIPS[n](p)
