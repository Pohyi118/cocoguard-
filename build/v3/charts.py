"""Inline SVG charts in the Field Desk visual language (brand green, IBM Plex via CSS)."""
BR, BRD, TINT, INK, INK2, INK3, LINE, HI, MID, LO, RAIN = "#1E5A43", "#15432F", "#E9F1EC", "#17201C", "#4A554F", "#67716B", "#DADFD8", "#B0452E", "#D6A03E", "#C8D4BC", "#2D5F86"
SOFT = "#8DB09E"

def _t(x, y, s, size=11, fill=INK2, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'

def hbars(rows, fmt, w=520, label_w=150, bar_h=22, gap=12, maxv=None, axis=None):
    """rows: [(label, value, strong)]"""
    maxv = maxv or max(v for _, v, _ in rows) * 1.18
    plot = w - label_w - 70; h = len(rows) * (bar_h + gap) + 26
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for i, (lab, v, strong) in enumerate(rows):
        y = 6 + i * (bar_h + gap); bw = plot * v / maxv
        out.append(_t(label_w - 10, y + bar_h * .68, lab, 11, INK2, "end"))
        out.append(f'<rect x="{label_w}" y="{y}" width="{bw:.1f}" height="{bar_h}" rx="3" fill="{BR if strong else SOFT}"/>')
        out.append(_t(label_w + bw + 7, y + bar_h * .68, fmt(v), 11, INK, "start", 700))
    out.append(f'<line x1="{label_w}" y1="2" x2="{label_w}" y2="{h - 22}" stroke="{LINE}"/>')
    if axis: out.append(_t(label_w + plot / 2, h - 4, axis, 10, INK3, "middle"))
    return "".join(out) + "</svg>"

def vbars(rows, fmt, w=330, h=176, axis=None):
    maxv = max(v for _, v, _ in rows) * 1.2; n = len(rows); left, bottom = 10, 36; pw = w - left * 2; ph = h - bottom - 18
    bw = pw / n * .62; out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for i, (lab, v, strong) in enumerate(rows):
        cx = left + pw / n * (i + .5); bh = ph * v / maxv; y = 18 + ph - bh
        out.append(f'<rect x="{cx - bw / 2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{BR if strong else SOFT}"/>')
        out.append(_t(cx, y - 5, fmt(v), 11, INK, "middle", 700)); out.append(_t(cx, 18 + ph + 15, lab, 10.5, INK2, "middle"))
    out.append(f'<line x1="{left}" y1="{18 + ph}" x2="{w - left}" y2="{18 + ph}" stroke="{LINE}"/>')
    if axis: out.append(_t(w / 2, h - 2, axis, 9.5, INK3, "middle"))
    return "".join(out) + "</svg>"

def contribution(w=330, h=190):
    rows = [(10, -150), (14, 30), (20, 300), (30, 750)]; lo, hi = -200, 860; left, bottom, top = 10, 38, 16
    ph = h - bottom - top; y0 = top + ph * hi / (hi - lo); pw = w - 2 * left; bw = pw / 4 * .58
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for i, (n, v) in enumerate(rows):
        cx = left + pw / 4 * (i + .5); bh = ph * abs(v) / (hi - lo); y = y0 - bh if v >= 0 else y0
        out.append(f'<rect x="{cx - bw / 2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh, 1.5):.1f}" rx="2" fill="{HI if v < 0 else (SOFT if v < 100 else BR)}"/>')
        lab = ("-RM" if v < 0 else "+RM") + f"{abs(v)}"
        out.append(_t(cx, (y - 5) if v >= 0 else (y0 - 5), lab, 11, HI if v < 0 else INK, "middle", 700))
        out.append(_t(cx, top + ph + 16, f"{n} farms", 10.5, INK2, "middle"))
    out.append(f'<line x1="{left}" y1="{y0:.1f}" x2="{w - left}" y2="{y0:.1f}" stroke="{INK3}"/>')
    out.append(_t(w / 2, h - 2, "Active farms per cluster", 9.5, INK3, "middle"))
    return "".join(out) + "</svg>"

def heat(w=330, h=150):
    fees = [60, 75, 90]; farms = [10, 14, 20, 30]
    val = lambda f, n: (f - 30) * n - 600
    left, top, cw, chh = 52, 6, (w - 56) / 4, 34
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for r, f in enumerate(fees):
        out.append(_t(left - 8, top + r * chh + chh * .62, f"RM{f}", 10.5, INK2, "end"))
        for c, n in enumerate(farms):
            v = val(f, n); col = HI if v < 0 else ("#EEF0EB" if v < 100 else (SOFT if v < 600 else BR))
            ink = "#fff" if (v < 0 or v >= 600) else INK
            out.append(f'<rect x="{left + c * cw + 1:.1f}" y="{top + r * chh + 1}" width="{cw - 2:.1f}" height="{chh - 2}" rx="3" fill="{col}" fill-opacity="{.85 if v < 0 else 1}"/>')
            out.append(_t(left + c * cw + cw / 2, top + r * chh + chh * .62, ("-" if v < 0 else "") + f"{abs(v):,}", 11, ink, "middle", 700))
    for c, n in enumerate(farms): out.append(_t(left + c * cw + cw / 2, top + 3 * chh + 15, f"{n}", 10.5, INK2, "middle"))
    out.append(_t(left + 2 * cw, h - 4, "Active farms per cluster (rows: fee per farm)", 9.5, INK3, "middle"))
    return "".join(out) + "</svg>"

def gantt(w=520, h=170):
    tasks = [("Site and grower agreement", .5, 1.5, True), ("Farm map and route setup", .5, 2.5, False), ("Dry run and revisions", 1.5, 2.5, True),
             ("Timed field rounds", 2.5, 8.5, False), ("Analysis and demo", 6.5, 8.5, True)]
    left = 170; pw = w - left - 10; bh = 18; gap = 9
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" role="img">']
    for i, (lab, a, b, s) in enumerate(tasks):
        y = 4 + i * (bh + gap)
        out.append(_t(left - 8, y + bh * .7, lab, 10.5, INK2, "end"))
        out.append(f'<rect x="{left + pw * (a - .5) / 8:.1f}" y="{y}" width="{pw * (b - a) / 8:.1f}" height="{bh}" rx="3" fill="{BR if s else SOFT}"/>')
    yb = 4 + 5 * (bh + gap)
    out.append(f'<line x1="{left}" y1="{yb}" x2="{left + pw}" y2="{yb}" stroke="{LINE}"/>')
    for k in range(1, 9): out.append(_t(left + pw * (k - .5 + .5) / 8 - pw / 16, yb + 14, str(k), 10, INK3, "middle"))
    out.append(_t(left + pw / 2, h - 2, "Build week", 9.5, INK3, "middle"))
    return "".join(out) + "</svg>"
