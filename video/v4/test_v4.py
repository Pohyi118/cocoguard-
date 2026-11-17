import sys, time, socket, subprocess
from playwright.sync_api import sync_playwright
SP = "C:/Users/User/AppData/Local/Temp/claude/a460c5756f12cc2e/a113cf1f-c331-40e5-a923-a01e76f99174/scratchpad/"
srv = None
if socket.socket().connect_ex(("127.0.0.1", 8766)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8766", "--bind", "127.0.0.1"], cwd="C:/Users/User/Documents/GSC/video/v4", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
times = [float(x) for x in sys.argv[1:]]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:8766/stage/real.html"); pg.wait_for_function("window.KS_READY !== undefined"); pg.evaluate("window.KS_READY")
    for t in times:
        t0 = time.time(); pg.evaluate(f"window.renderAt({t})"); pg.screenshot(path=SP + f"v4_{t:06.1f}.jpg", type="jpeg", quality=80)
    print("per frame ~", round((time.time() - t0), 2), "s; errors:", errs[:5]); b.close()
if srv: srv.terminate()
