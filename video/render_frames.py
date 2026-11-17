"""Render one 1920x1080 PNG per scene from scenes.py using headless Edge."""
import pathlib
from playwright.sync_api import sync_playwright
from scenes import SCENES

IMG = "file:///C:/Users/User/Documents/GSC/build/img/"
OUT = pathlib.Path("frames")

CSS = """
*{box-sizing:border-box;margin:0}
body{width:1920px;height:1080px;font-family:'Noto Sans','Segoe UI',sans-serif;color:#1f2421;background:#f6f8f6;overflow:hidden}
.wrap{position:relative;width:1920px;height:1080px;padding:96px 120px}
.kick{font-size:26px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#2B654F;margin-bottom:22px}
h1{font-size:64px;line-height:1.12;font-weight:700;margin-bottom:44px;max-width:1600px}
.brand{position:absolute;left:120px;bottom:46px;font-size:22px;color:#5f6b65;font-weight:600}
.brand b{color:#2B654F}
.num{position:absolute;right:120px;bottom:46px;font-size:22px;color:#5f6b65}
.bar{position:absolute;left:0;bottom:0;height:10px;background:#2B654F}
.hero{padding:0}
.hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,43,33,.92) 0%,rgba(17,43,33,.75) 50%,rgba(17,43,33,.15) 100%)}
.hero .txt{position:absolute;left:120px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;width:1180px;color:#fff}
.hero .kick{color:#9fd3b9}
.hero h1{font-size:76px;margin-bottom:28px}
.hero .sub{font-size:28px;color:#d9e8e0}
.hero .brand,.hero .num{color:#cfe0d7}.hero .brand b{color:#fff}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:40px}
.stat{background:#fff;border-top:12px solid #2B654F;padding:56px 48px;min-height:440px;box-shadow:0 2px 0 #dfe7e2}
.stat .v{white-space:nowrap;font-size:76px;font-weight:700;color:#2B654F;line-height:1.05;margin-bottom:20px}
.stat .l{font-size:34px;line-height:1.4;color:#33403a}
.fig{display:flex;justify-content:center}
.fig img{max-height:640px;max-width:1680px;border:2px solid #d7e0db;background:#fff}
.two{display:grid;grid-template-columns:330px 640px 1fr;gap:48px;align-items:start}
.two img{width:100%;border:2px solid #d7e0db;border-radius:14px;background:#fff}
.two img.tall{height:690px;object-fit:cover;object-position:top}
ul.b{list-style:none;padding:0}
ul.b li{font-size:34px;line-height:1.35;margin-bottom:28px;padding-left:44px;position:relative}
ul.b li:before{content:"";position:absolute;left:0;top:14px;width:20px;height:20px;background:#2B654F;border-radius:4px}
.split{display:grid;grid-template-columns:1000px 1fr;gap:60px;align-items:start}
.split img{width:100%;border:2px solid #d7e0db;background:#fff}
.split ul.b li{font-size:32px}
"""

def body(s):
    n = f'<div class="brand"><b>KokoShield</b> · Weather-guided disease scouting · Universiti Malaya</div><div class="num">{s["id"]} / {len(SCENES)}</div>'
    bar = f'<div class="bar" style="width:{1920*s["id"]/len(SCENES):.0f}px"></div>'
    L = s["layout"]
    if L == "hero":
        return (f'<div class="wrap hero"><img class="bg" src="{IMG}{s["img"]}"><div class="shade"></div>'
                f'<div class="txt"><div class="kick">{s["kicker"]}</div><h1>{s["head"]}</h1>'
                f'<div class="sub">{s.get("sub","")}</div></div>{n}{bar}</div>')
    top = f'<div class="kick">{s["kicker"]}</div><h1>{s["head"]}</h1>'
    if L == "stats":
        tiles = "".join(f'<div class="stat"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in s["stats"])
        mid = f'<div class="stats">{tiles}</div>'
    elif L == "figure":
        mid = f'<div class="fig"><img src="{IMG}{s["img"]}"></div>'
    elif L == "two":
        a, b = s["imgs"]
        lis = "".join(f"<li>{x}</li>" for x in s["bullets"])
        mid = f'<div class="two"><img class="tall" src="{IMG}{a}"><img class="tall" src="{IMG}{b}"><ul class="b" style="margin-top:20px">{lis}</ul></div>'
        top = f'<div class="kick">{s["kicker"]}</div><h1 style="margin-bottom:34px">{s["head"]}</h1>'
    elif L == "split":
        lis = "".join(f"<li>{x}</li>" for x in s["bullets"])
        mid = f'<div class="split"><img src="{IMG}{s["img"]}"><ul class="b">{lis}</ul></div>'
    return f'<div class="wrap">{top}{mid}{n}{bar}</div>'

OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for s in SCENES:
        html = ('<!doctype html><html><head><meta charset="utf-8">'
                '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">'
                f'<style>{CSS}</style></head><body>{body(s)}</body></html>')
        f = OUT / f"scene{s['id']}.html"; f.write_text(html, encoding="utf-8")
        pg.goto(f.resolve().as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"scene{s['id']}.png"))
    b.close()
print("done")
