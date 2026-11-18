"""Render node.html to transparent PNG frames + anchors.json. Usage: python render_node.py [--preview t1 t2 ...] (default: 8 s @ 30 fps)."""
import json, pathlib, socket, subprocess, sys, time
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent; OUT = HERE / "frames"; OUT.mkdir(exist_ok=True)
PORT = 8791; FPS, DUR = 30, 8.0
srv = None
if socket.socket().connect_ex(("127.0.0.1", PORT)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"], cwd=HERE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
preview = "--preview" in sys.argv
times = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]] if preview else [i / FPS for i in range(int(DUR * FPS))]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(f"http://127.0.0.1:{PORT}/node.html"); print("parts:", pg.evaluate("window.KS_READY"))
    anchors = []; t0 = time.time()
    for i, t in enumerate(times):
        a = pg.evaluate(f"window.renderAt({t})"); anchors.append(a)
        name = f"preview_{t:04.1f}.png" if preview else f"f{i:04d}.png"
        pg.locator("canvas").screenshot(path=str(OUT / name), omit_background=True)
    if not preview: json.dump(dict(fps=FPS, anchors=anchors), open(HERE / "anchors.json", "w"))
    print(f"{len(times)} frames in {time.time() - t0:.0f}s; errors: {errs[:3]}; last anchors {anchors[-1]}")
    b.close()
if srv: srv.terminate()
