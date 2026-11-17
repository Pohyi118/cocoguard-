"""Assemble the interactive page from the v4 real-image composition + the interactive layer.
Writes index.html (local) and artifact.html (for publishing; no document wrapper)."""
import pathlib, re
real = pathlib.Path("../video/v4/stage/real.html").read_text(encoding="utf-8")
layer = pathlib.Path("layer.html").read_text(encoding="utf-8")
js = pathlib.Path("layer.js").read_text(encoding="utf-8")
s = real
for a, b in [("<title>KokoShield Pitch v4</title>", "<title>KokoShield Farm Story</title>"),
             ("const PH = '../photos/';", "const PH = 'photos/';"),
             (":root{--g:#2B654F;", ":root{color-scheme:dark;--g:#2B654F;")]:
    assert s.count(a) == 1, a; s = s.replace(a, b)
s, n = re.subn(r"(app_[a-z_]+|node_exploded)\.png", r"\1.jpg", s); print("png refs ->", n)
s = s.replace("</body>", layer + "\n<script>\n" + js + "\n</script>\n</body>")
pathlib.Path("index.html").write_text(s, encoding="utf-8")
a = s
for x, y in [('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n', ''), ("</head>\n<body>\n", "\n"), ("</body>\n</html>", "")]:
    assert a.count(x) == 1, x[:30]; a = a.replace(x, y)
assert "<html" not in a and "<body" not in a and "<head" not in a
pathlib.Path("artifact.html").write_text(a, encoding="utf-8")
print("index.html", len(s), "artifact.html", len(a))
