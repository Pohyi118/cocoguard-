"""Capture real screenshots of prototype/KokoShield_Prototype.html for the v3 proposal (desktop @2x, phone @3x)."""
import pathlib
from playwright.sync_api import sync_playwright
URL = pathlib.Path("C:/Users/User/Documents/GSC/prototype/KokoShield_Prototype.html").as_uri()
OUT = pathlib.Path(__file__).parent / "shots"; OUT.mkdir(exist_ok=True)

def page(pw, mobile):
    b = pw.chromium.launch(channel="msedge", headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844} if mobile else {"width": 1440, "height": 900},
                        device_scale_factor=3 if mobile else 2, is_mobile=mobile, has_touch=mobile, locale="en-GB", timezone_id="Asia/Kuala_Lumpur")
    pg = ctx.new_page(); pg.clock.install(time="2026-11-17T08:05:00+08:00"); pg.goto(URL); pg.clock.run_for(1500)
    return b, pg

def snap(pg, name, full=False):
    pg.clock.run_for(4000)   # let any toast clear
    pg.screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=90, full_page=full); print(name)

with sync_playwright() as pw:
    b, pg = page(pw, False)
    snap(pg, "desk_plan")
    pg.locator('[data-act="view-log"]').first.click(); snap(pg, "desk_log")
    pg.locator('[data-act="view-compare"]').first.click(); snap(pg, "desk_compare", full=True)
    pg.locator('[data-act="view-hardware"]').first.click(); pg.locator('[data-set="explode"][data-val="1"]').first.click(); snap(pg, "desk_sensor")
    b.close()
    b, pg = page(pw, True)
    snap(pg, "phone_plan")
    pg.locator('[data-act="walk-start"]').first.tap(); pg.clock.run_for(2 * 60 * 1000 + 5000); snap(pg, "phone_walk")
    pg.locator('[data-act="walk-found"]').first.tap(); pg.locator('[data-step="1"]').first.tap(); pg.locator('[data-step="1"]').first.tap(); snap(pg, "phone_count")
    pg.locator('[data-act="walk-save"]').first.tap(); snap(pg, "phone_next")
    b.close()
    b, pg = page(pw, True)
    pg.locator("#crop").select_option("rice"); snap(pg, "phone_rice")
    b.close()
