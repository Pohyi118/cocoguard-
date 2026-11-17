import sys, time, socket, subprocess
from playwright.sync_api import sync_playwright
SP = "C:/Users/User/AppData/Local/Temp/claude/a460c5756f12cc2e/a113cf1f-c331-40e5-a923-a01e76f99174/scratchpad/"
srv = None
if socket.socket().connect_ex(("127.0.0.1", 8767)) != 0:
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8767", "--bind", "127.0.0.1"], cwd="C:/Users/User/Documents/GSC/KokoShield_Interactive", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True, args=["--autoplay-policy=no-user-gesture-required"])
    pg = b.new_page(viewport={"width": 1600, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto("http://127.0.0.1:8767/index.html"); pg.wait_for_function("window.KS_READY !== undefined"); pg.evaluate("window.KS_READY")
    pg.screenshot(path=SP + "i0.jpg", type="jpeg", quality=75)
    pg.click("#startBtn"); pg.wait_for_timeout(2500); print("t:", pg.eval_on_selector("#seek", "e=>e.value"))
    pg.click("#chips button:nth-child(4)"); pg.wait_for_timeout(2500); print("after chapter 4:", pg.eval_on_selector("#seek", "e=>e.value"))
    pg.screenshot(path=SP + "i1.jpg", type="jpeg", quality=75)
    pg.click("#explore"); pg.wait_for_timeout(500)
    pg.locator("#ch-A").click(force=True); pg.wait_for_timeout(400); print("info A:", pg.inner_text("#infobody")[:80].replace("\n", " | "))
    pg.screenshot(path=SP + "i2.jpg", type="jpeg", quality=75)
    pg.locator("#xDrone").click(force=True); pg.wait_for_timeout(300); print("info drone:", pg.inner_text("#infobody")[:60].replace("\n", " | "))
    pg.click("#challenge"); pg.wait_for_timeout(400)
    pg.check("#chint"); pg.wait_for_timeout(2600); pg.screenshot(path=SP + "i3.jpg", type="jpeg", quality=75)
    for k in "GBH": pg.locator(f"#ch-{k}").click(force=True); pg.wait_for_timeout(120)
    pg.wait_for_timeout(2500); pg.click("#cwalk"); pg.wait_for_timeout(7000)
    print("result:", pg.inner_text("#cres")[:90].replace("\n", " | "))
    pg.screenshot(path=SP + "i4.jpg", type="jpeg", quality=75)
    pg.click("#cks"); pg.wait_for_timeout(7000); print("ks finds:", pg.inner_text("#cksn"))
    pg.screenshot(path=SP + "i5.jpg", type="jpeg", quality=75)
    print("errors:", errs[:6]); b.close()
if srv: srv.terminate()
