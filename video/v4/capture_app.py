"""Capture real Field Desk prototype states (desktop 1440x900 @2x) for the v4 video."""
from playwright.sync_api import sync_playwright
URL = "file:///C:/Users/User/Documents/GSC/build/kit/KokoShield_Prototype.html"
OUT = "C:/Users/User/Documents/GSC/video/v4/stage/assets/"
PHOTO = "C:/Users/User/Documents/GSC/video/v4/photos/13_black_pod.jpg"
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2).new_page()
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.get_by_role("button", name="Routine", exact=True).click(); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT + "app_plan_routine.png")
    pg.get_by_role("button", name="Wet spell", exact=True).click(); pg.wait_for_timeout(400)
    pg.get_by_role("button", name="Generate route", exact=True).click(); pg.wait_for_timeout(700)
    pg.screenshot(path=OUT + "app_plan_route.png")
    pg.get_by_role("button", name="Scout log").first.click(); pg.wait_for_timeout(400)
    for blk, n, note, photo in [("A", 3, "Brown lesions on lower pods after rain; near drain.", True),
                                ("G", 2, "Two pods with spreading dark patch, east side.", False),
                                ("D", 1, "Small spot, possibly mechanical damage. Check again.", False)]:
        pg.locator("select[name=block]").select_option(index=["A", "B", "C", "D", "E", "G", "H"].index(blk))
        pg.locator("input[name=count]").fill(str(n)); pg.locator("textarea[name=note]").fill(note)
        if photo: pg.locator("#photoInput").set_input_files(PHOTO)
        pg.get_by_role("button", name="Save for review").click(); pg.wait_for_timeout(400)
    pg.get_by_role("button", name="All (3)").click(); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT + "app_log_pending.png")
    pg.get_by_role("button", name="Confirm", exact=True).last.click(); pg.wait_for_timeout(250)
    pg.get_by_role("button", name="Confirm", exact=True).last.click(); pg.wait_for_timeout(250)
    pg.get_by_role("button", name="Rule out", exact=True).first.click(); pg.wait_for_timeout(250)
    pg.get_by_role("button", name="All (3)").click(); pg.wait_for_timeout(2600)   # let the toast disappear
    pg.screenshot(path=OUT + "app_log_reviewed.png")
    # positions of the buttons we 'click' in the video (CSS px in the 1440x900 page)
    pg.get_by_role("button", name="Field plan").first.click(); pg.wait_for_timeout(400)
    pg.get_by_role("button", name="Routine", exact=True).click(); pg.wait_for_timeout(300)
    for name in ["Wet spell", "Generate route"]:
        bb = pg.get_by_role("button", name=name, exact=True).first.bounding_box(); print(name, {k: round(v) for k, v in bb.items()})
    b.close()
