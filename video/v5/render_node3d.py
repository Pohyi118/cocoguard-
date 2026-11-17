"""Render the Field Node GLB turntable/explode beat to transparent PNG frames (7 s @ 30 fps) for compositing."""
import sys, time, socket, subprocess, pathlib
from playwright.sync_api import sync_playwright
ROOT = "C:/Users/User/Documents/GSC/video/v5"; OUT = pathlib.Path(ROOT) / "stage/assets/node3d"; OUT.mkdir(parents=True, exist_ok=True)
srv = None
if socket.socket().connect_ex(("127.0.0.1", 8769)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8769", "--bind", "127.0.0.1"], cwd="C:/Users/User/Documents/GSC", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
FPS, DUR = 30, 7.0
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1100, "height": 800}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:8769/video/v5/stage/node3d.html"); pg.wait_for_function("window.KS_READY !== undefined"); pg.evaluate("window.KS_READY")
    n = int(DUR * FPS); t0 = time.time()
    for i in range(n):
        pg.evaluate(f"window.renderAt({i / FPS})"); pg.screenshot(path=str(OUT / f"f{i:04d}.png"), omit_background=True)
    print(f"{n} frames in {time.time() - t0:.0f}s; errors: {errs[:3]}"); b.close()
if srv: srv.terminate()
