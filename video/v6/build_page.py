"""Assemble stage/real.html from the engine parts and the scene file."""
import pathlib
st = pathlib.Path(__file__).parent / "stage"
r = lambda f: (st / f).read_text(encoding="utf-8")
head, helpers, tail, scenes, css = r("_engine_head.html"), r("_engine_helpers.js"), r("_engine_tail.js"), r("scenes_v5.js"), r("extra.css")
h = helpers[: helpers.index("/* 1 hook */")] + helpers[helpers.index("/* ---------------- overlay system"):]
t = tail[: tail.index("const rainAt = t =>")] + tail[tail.index("/* cursor helper"): tail.index("/* ================= per-frame update")] + tail[tail.index("window.renderAt"):]
t = t.replace("window.renderAt = async t => { update(t); return true; };",
              "window.renderAt = async t => { PEND.length = 0; update(t); await Promise.all(PEND); return true; };")
assert "await Promise.all(PEND)" in t
page = head.replace("</style>", css + "</style>").replace("KokoShield Pitch v5 cinematic", "KokoShield Pitch v6 cinematic") + h + "\n" + scenes + "\n" + t
(st / "real.html").write_text(page, encoding="utf-8"); print("real.html", len(page))
