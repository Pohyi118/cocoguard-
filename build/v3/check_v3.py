"""Report pages whose content overflows, and render page previews."""
import sys, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True); pg = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=1)
    pg.goto((HERE / "proposal_v3.html").as_uri()); pg.emulate_media(media="print"); pg.wait_for_timeout(1500)
    over = pg.evaluate("""[...document.querySelectorAll('.page')].map((s,i)=>{const c=s.querySelector('.content');return [i+1, c.scrollHeight - c.clientHeight]})""")
    print("overflow (px):", [o for o in over if o[1] > 1])
    if len(sys.argv) > 1:
        out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
        for i, el in enumerate(pg.query_selector_all(".page"), 1): el.screenshot(path=str(out / f"p{i:02d}.png"))
    b.close()
