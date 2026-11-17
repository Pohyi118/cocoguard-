import sys, time
from playwright.sync_api import sync_playwright
URL = "http://127.0.0.1:8765/index.html?mode=video"
OUT = "C:/Users/User/AppData/Local/Temp/claude/a460c5756f12cc2e/a113cf1f-c331-40e5-a923-a01e76f99174/scratchpad/"
times = [float(x) for x in sys.argv[1:]] or [1, 8, 16, 25, 38, 47, 53, 64, 76, 86, 96, 103, 115]
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    errs = []
    pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.goto(URL); pg.wait_for_function("window.KS_READY !== undefined", timeout=60000)
    pg.evaluate("window.KS_READY")
    print("GL:", pg.evaluate("(()=>{const g=document.getElementById('gl').getContext('webgl2');const d=g.getExtension('WEBGL_debug_renderer_info');return d?g.getParameter(d.UNMASKED_RENDERER_WEBGL):'n/a'})()"))
    for t in times:
        t0 = time.time(); pg.evaluate(f"window.renderAt({t})"); pg.screenshot(path=OUT + f"t3d_{t:06.1f}.jpg", type="jpeg", quality=80)
        print(f"t={t}: {time.time()-t0:.2f}s")
    print("\n".join(errs[:20]))
    b.close()
