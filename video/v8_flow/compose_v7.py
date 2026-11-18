"""Compose the KokoShield v7 film frame by frame (1920x1080, 30 fps) from Flow clips, prototype recordings and overlays.
Every cut and overlay is keyed to a spoken word from timeline.json (voice_v6.py).
Outputs: work/film_clean.mp4 (no subtitles), work/film_subs.mp4 (burned subtitles), shots.json (for the sound mix).
Usage: python compose_v6.py [--from T] [--to T] [--sheet]   (--sheet writes only a contact sheet of key moments)"""
import json, math, pathlib, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS = 30; W, H = 1920, 1080
HERE = pathlib.Path(__file__).parent; FC = HERE.parent / "v5/flow_clips"; REC = HERE / "rec"; WORK = HERE / "work"; WORK.mkdir(exist_ok=True)
TL = json.load(open(HERE / "timeline.json")); SC = {s["id"]: s for s in TL["scenes"]}; END = TL["end"]
FONT = {k: str(HERE / f"fonts/Plex-{k}.ttf") for k in ("Regular", "Medium", "SemiBold")}
GREEN, INK, PAPER = (31, 90, 69), (20, 33, 28), (238, 243, 239)


def wt(sid, word, occ=1, end=False):
    """Absolute time of the occ-th occurrence of `word` in scene sid (start, or end with end=True)."""
    n = 0
    for a, b, w in SC[sid]["words"]:
        if w.lower().strip(".,;:!?") == word.lower():
            n += 1
            if n == occ: return SC[sid]["speech_at"] + (b if end else a)
    raise KeyError(f"S{sid}: {word} #{occ}")


S0 = lambda sid: SC[sid]["start"]; S1 = lambda sid: SC[sid]["end"]
ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))


# ---------------- sources ----------------
class Video:
    """Forward-reading clip source with frame blending for slowed footage."""
    def __init__(self, path):
        self.path = str(path); self.cap = cv2.VideoCapture(self.path); self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)); self.idx = -1; self.cur = None; self.prev = None

    def _read_to(self, i):
        i = min(max(i, 0), self.n - 1)
        if i == self.idx - 1 and self.prev is not None: return self.prev
        if i < self.idx: self.cap.release(); self.cap = cv2.VideoCapture(self.path); self.idx = -1; self.cur = None
        while self.idx < i:
            ok, f = self.cap.read()
            if not ok: break
            self.prev, self.cur, self.idx = self.cur, f, self.idx + 1
        return self.cur

    def at(self, t):
        x = max(0.0, t * self.fps); i = int(x); fr = x - i
        a = self._read_to(i)
        if fr < 0.05 or i + 1 >= self.n: return a
        a = a.copy(); b = self._read_to(i + 1)
        return cv2.addWeighted(a, 1 - fr, b, fr, 0)


class Still:
    def __init__(self, path): self.img = cv2.imread(str(path))
    def at(self, t): return self.img


def cover(src_w, src_h):
    s = max(W / src_w, H / src_h); return s, (W - src_w * s) / 2, (H - src_h * s) / 2


def warp(img, s, tx, ty, size=(W, H)):
    M = np.float32([[s, 0, tx], [0, s, ty]])
    return cv2.warpAffine(img, M, size, flags=cv2.INTER_CUBIC if s > 1.2 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def remap(keys):
    """Piecewise-linear out-time -> source-time map from [(out_t, src_t), ...]; holds outside the range."""
    def f(t):
        if t <= keys[0][0]: return keys[0][1]
        for (a, sa), (b, sb) in zip(keys, keys[1:]):
            if t <= b: return sa + (sb - sa) * (t - a) / (b - a)
        return keys[-1][1]
    return f


SHOTS = []  # dict(t0, t1, src, path, time=f(out_t)->src_t, xf=f(out_t)->(s,tx,ty) | None, fade=crossfade-in seconds, audio=bool, draw=f(frame,t))


def shot(t0, t1, path, time, xf=None, fade=0.0, audio=True, kind="video", post=None):
    src = Still(path) if kind == "still" else Video(path)
    SHOTS.append(dict(t0=t0, t1=t1, src=src, path=str(path), time=time, xf=xf, fade=fade, audio=audio and kind == "video", post=post))


def speed(t0, src0, rate=1.0): return lambda t: src0 + (t - t0) * rate


def fit_rate(t0, t1, src0, src1): return remap([(t0, src0), (t1, src1)])


def kenburns(s_from, s_to, t0, t1, cx=0.5, cy=0.5, src=(1280, 720)):
    base, bx, by = cover(*src)
    def f(t):
        k = s_from + (s_to - s_from) * ease((t - t0) / (t1 - t0)); s = base * k
        return s, W * cx - src[0] * s * cx, H * cy - src[1] * s * cy
    return f


# ---------------- overlays ----------------
def font(k, size): return ImageFont.truetype(FONT[k], size)


_cache = {}
def text_img(key, lines, pad=0, box=None, radius=0, center=False):
    """lines: [(text, font_key, size, rgba, gap_after)] -> RGBA numpy image (cached)."""
    if key in _cache: return _cache[key]
    fonts = [font(k, s) for _, k, s, _, _ in lines]
    widths = [f.getbbox(t)[2] for (t, *_), f in zip(lines, fonts)]
    heights = [f.getbbox("Ag")[3] for f in fonts]
    w = max(widths) + 2 * pad; h = sum(hh + g for hh, (*_, g) in zip(heights, lines)) + 2 * pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if box: d.rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=box)
    y = pad
    for (t, _, _, col, g), f, hh, ww in zip(lines, fonts, heights, widths):
        d.text(((w - ww) / 2 if center else pad, y), t, font=f, fill=col); y += hh + g
    _cache[key] = np.array(im); return _cache[key]


def paste(frame, rgba, x, y, alpha=1.0):
    h, w = rgba.shape[:2]; x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0 or alpha <= 0: return
    src = rgba[y0 - y: y1 - y, x0 - x: x1 - x].astype(np.float32)
    a = src[..., 3:4] / 255 * alpha; roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - a) + src[..., 2::-1] * a).astype(np.uint8)


def fade_env(t, t0, t1, fi=0.35, fo=0.35):
    if t < t0 or t > t1: return 0.0
    return min(1.0, (t - t0) / fi if fi else 1, (t1 - t) / fo if fo else 1)


TEXTS = []  # (t0, t1, img, x, y, fi, fo, rise)
def text(t0, t1, img, x, y, fi=0.4, fo=0.35, rise=14): TEXTS.append((t0, t1, img, W - 96 - img.shape[1] if x is None else x, y, fi, fo, rise))


def rrect_mask(holes, feather=10):
    m = np.zeros((H // 2, W // 2), np.uint8)
    for x, y, w, h, *r in holes:
        r = (r[0] if r else 10) // 2
        cv2.rectangle(m, (x // 2 + r, y // 2), ((x + w) // 2 - r, (y + h) // 2), 255, -1)
        cv2.rectangle(m, (x // 2, y // 2 + r), ((x + w) // 2, (y + h) // 2 - r), 255, -1)
        for cx, cy in ((x // 2 + r, y // 2 + r), ((x + w) // 2 - r, y // 2 + r), (x // 2 + r, (y + h) // 2 - r), ((x + w) // 2 - r, (y + h) // 2 - r)):
            cv2.circle(m, (cx, cy), r, 255, -1)
    m = cv2.GaussianBlur(m, (0, 0), feather / 2)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)[..., None] / 255


HL = []  # (t0, t1, holes) ; consecutive entries cross-blend
def highlight(t0, t1, *holes): HL.append((t0, t1, [list(h) for h in holes], rrect_mask(holes)))


def dimmed(frame):
    small = cv2.resize(frame, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), 3)
    return (cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) * 0.38 + 6)


def apply_highlights(frame, t):
    act = [(t0, t1, m) for t0, t1, _, m in HL if t0 - 0.35 <= t <= t1 + 0.35]
    if not act: return frame
    a = 0.0; mask = np.zeros((H, W, 1), np.float32); wsum = 0.0
    for t0, t1, m in act:
        e = (t - (t0 - 0.35)) / 0.35 if t < t0 else (1.0 if t <= t1 else 1 - (t - t1) / 0.35)
        e = min(1.0, max(0.0, e)); mask += m * e; wsum += e; a = max(a, e)
    mask = mask / max(wsum, 1e-6)
    a = ease(a); f = frame.astype(np.float32); d = dimmed(frame)
    out = f * (1 - a) + (f * mask + d * (1 - mask)) * a
    return out.astype(np.uint8)


POPS = []  # (t0, t1, src_rect, center, scale)
def popout(t0, t1, rect, center, scale): POPS.append((t0, t1, rect, center, scale))


def apply_pops(frame, t, base):
    for t0, t1, (x, y, w, h), (cx, cy), sc in POPS:
        e = fade_env(t, t0, t1, 0.3, 0.25)
        if e <= 0: continue
        k = sc * (0.92 + 0.08 * ease(e)); crop = base[y:y + h, x:x + w]
        big = cv2.resize(crop, (int(w * k), int(h * k)), interpolation=cv2.INTER_CUBIC)
        bh, bw = big.shape[:2]; r = 14
        im = Image.new("RGBA", (bw + 60, bh + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([30, 36, 30 + bw, 36 + bh], r, fill=(0, 0, 0, 110)); im = im.filter(ImageFilter.GaussianBlur(14))
        sh = np.array(im); paste(frame, sh, cx - bw / 2 - 30, cy - bh / 2 - 30, e)
        mk = Image.new("L", (bw, bh), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, bw - 1, bh - 1], r, fill=255)
        rgba = np.dstack([big[..., ::-1], np.array(mk)]); paste(frame, rgba, cx - bw / 2, cy - bh / 2, e)
        ring = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); ImageDraw.Draw(ring).rounded_rectangle([0, 0, bw - 1, bh - 1], r, outline=(255, 255, 255, 230), width=3)
        paste(frame, np.array(ring), cx - bw / 2, cy - bh / 2, e)
    return frame


# ---------------- phone mockup ----------------
PH_H = 930; PH_S = PH_H / 892; PH_W = int(412 * PH_S)
def phone_layer():
    bez = 16; R = 62; w, h = PH_W + 2 * bez, PH_H + 2 * bez
    im = Image.new("RGBA", (w + 120, h + 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([60, 74, 60 + w, 74 + h], R, fill=(0, 0, 0, 150)); im = im.filter(ImageFilter.GaussianBlur(26))
    d = ImageDraw.Draw(im); d.rounded_rectangle([60, 60, 60 + w, 60 + h], R, fill=(18, 20, 19, 255), outline=(70, 74, 72, 255), width=2)
    scr = Image.new("L", (PH_W, PH_H), 0); ImageDraw.Draw(scr).rounded_rectangle([0, 0, PH_W - 1, PH_H - 1], R - bez, fill=255)
    return np.array(im), np.array(scr).astype(np.float32)[..., None] / 255, bez
PHONE_FRAME, PHONE_MASK, PHONE_BEZ = phone_layer()


def phone_post(rec, keys, px=1150, py=None, bgdim=0.42):
    """Post-processor: blur/dim the shot underneath and put the phone recording on top."""
    vid = Video(rec); tm = remap(keys); py = (H - (PH_H + 2 * PHONE_BEZ)) / 2 if py is None else py
    def post(frame, t, t0):
        e = ease(min(1, (t - t0) / 0.5))
        small = cv2.GaussianBlur(cv2.resize(frame, (W // 4, H // 4)), (0, 0), 4)
        bg = cv2.resize(small, (W, H)).astype(np.float32) * bgdim
        frame = (frame.astype(np.float32) * (1 - e) + bg * e).astype(np.uint8)
        scr = cv2.resize(vid.at(tm(t)), (PH_W, PH_H), interpolation=cv2.INTER_CUBIC)
        y = py + (1 - e) * 60
        paste(frame, PHONE_FRAME, px - 60, y - 60, e)
        rgba = np.dstack([scr[..., ::-1], (PHONE_MASK[..., 0] * 255).astype(np.uint8)])
        paste(frame, rgba, px + PHONE_BEZ, y + PHONE_BEZ, e)
        return frame
    return post


# =====================================================================================
#                              THE EDIT (v7, spliced into compose_v7.py)
# =====================================================================================
F = lambda n: FC / n
V7 = pathlib.Path("C:/Users/user/flow-mcp-out/KokoShield_v7")
BR = HERE / "brand"; PH = HERE.parent.parent / "KokoShield_Interactive/photos"


def rgba_img(path, w=None, h=None):
    im = Image.open(path).convert("RGBA")
    if w or h:
        r = (w / im.width) if w else (h / im.height); im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return im


def shadowed(im, radius=14, border=0, border_col=(255, 255, 255, 255), shadow=110, blur=22, offset=14):
    """Rounded card with optional border and a soft drop shadow, as an RGBA numpy array (image at offset 40,40)."""
    w, h = im.size; W2, H2 = w + 2 * border, h + 2 * border
    card = Image.new("RGBA", (W2, H2), border_col if border else (0, 0, 0, 0)); card.alpha_composite(im, (border, border))
    m = Image.new("L", (W2, H2), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, W2 - 1, H2 - 1], radius, fill=255); card.putalpha(Image.fromarray(np.minimum(np.array(card)[..., 3], np.array(m))))
    out = Image.new("RGBA", (W2 + 80, H2 + 80), (0, 0, 0, 0)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 40 + offset, 40 + W2, 40 + H2 + offset], radius, fill=(0, 0, 0, shadow)); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh); out.alpha_composite(card, (40, 40)); return np.array(out)


def rot(arr, deg):
    im = Image.fromarray(arr).rotate(deg, resample=Image.BICUBIC, expand=True); return np.array(im)


# ---------- rain streaks (code-drawn, for the storm) ----------
_rng = np.random.default_rng(3); RAIN = _rng.uniform(0, 1, (900, 3))
def rain_post(strength_fn):
    def post(frame, t, t0):
        s = strength_fn(t)
        if s <= 0: return frame
        lay = np.zeros_like(frame); n = int(len(RAIN) * min(1, s))
        for x, y, v in RAIN[:n]:
            px = (x * (W + 300) - 150 + t * 260) % (W + 300) - 150; py = (y * H + t * (1700 + 900 * v)) % (H + 200) - 100
            cv2.line(lay, (int(px), int(py)), (int(px - 16), int(py + 64)), (210, 220, 225), 1, cv2.LINE_AA)
        lay = cv2.GaussianBlur(lay, (0, 0), 0.8)
        f = frame.astype(np.float32) * (1 - 0.12 * s) + lay.astype(np.float32) * 0.55 * s
        return np.clip(f, 0, 255).astype(np.uint8)
    return post


# ---------- logo lockup ----------
SHIELD = rgba_img(BR / "shield.png")
def lockup(scale=1.0, tag="Weather-guided disease scouting", key="lock"):
    sh = SHIELD.resize((int(150 * scale), int(150 * scale)), Image.LANCZOS)
    word = Image.fromarray(text_img(key + "w", [("KokoShield", "SemiBold", int(112 * scale), (255, 255, 255, 255), int(6 * scale)),
                                                 (tag, "Medium", int(34 * scale), (225, 238, 230, 240), 0)]))
    w = sh.width + int(34 * scale) + word.width; h = max(sh.height, word.height)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); im.alpha_composite(sh, (0, (h - sh.height) // 2)); im.alpha_composite(word, (sh.width + int(34 * scale), (h - word.height) // 2 - 4))
    return im
LOCK = lockup(); LOCK_ARR = np.array(LOCK)


def logo_post(t_in, t_out, center=(W / 2, H / 2 - 30), vignette=0.55):
    def post(frame, t, t0):
        e = fade_env(t, t_in, t_out, 0.8, 0.6)
        if e <= 0: return frame
        k = ease(e); yy, xx = np.ogrid[:H, :W]
        vig = 1 - vignette * k * np.exp(-(((xx - center[0]) / 720.0) ** 2 + ((yy - center[1]) / 300.0) ** 2))[..., None]
        frame = (frame.astype(np.float32) * vig).astype(np.uint8)
        sc = 0.92 + 0.08 * ease(min(1, (t - t_in) / 1.2)); im = LOCK.resize((int(LOCK.width * sc), int(LOCK.height * sc)), Image.LANCZOS)
        paste(frame, np.array(im), center[0] - im.width / 2, center[1] - im.height / 2, k); return frame
    return post


# ================= S1 Harvest: the pod grows, then a healthy pod ==================
# Flow time-lapse (flower, cherelle, young pod, ripe pod) lands on the healthy pod's first frame as "harvest" ends;
# then the dry pod holds (the clip's first, rain-free second, slowed, no sound); on "Then the rain comes" the clip runs on and the drops start
t_then, t_cut = wt(2, "Then") - 0.1, wt(2, "comes", end=True) + 0.25
t_grow = wt(1, "harvest", end=True) + 0.15
shot(0.0, t_grow, F("growth_timelapse_smooth.mp4"), fit_rate(0.0, t_grow, 0.0, 4.966), audio=False)   # evenly paced, frame-blended
shot(t_grow, t_then, F("opening_healthy_pod_rain.mp4"), fit_rate(t_grow, t_then, 0.0, 0.95), kenburns(1.0, 1.05, t_grow, t_then), audio=False)
shot(t_then, t_cut, F("opening_healthy_pod_rain.mp4"), speed(t_then, 0.95), lambda t: kenburns(1.0, 1.05, t_grow, t_then)(t_then))
# ================= S2 The rain: the storm rolls over the farm ==================
t_flash = t_cut + 0.05
def storm_post(frame, t, t0):
    frame = rain_post(lambda t: 1.0)(frame, t, t0)
    fl = max(0.0, 1 - abs(t - t_flash) / 0.12) * 0.9 + max(0.0, 1 - abs(t - t_flash - 0.35) / 0.1) * 0.5
    if fl > 0: frame = np.clip(frame.astype(np.float32) * (1 + 0.9 * fl) + 25 * fl, 0, 255).astype(np.uint8)
    return frame
shot(t_cut, S1(2), F("opening_storm_over_farm.mp4"), fit_rate(t_cut, S1(2), 1.6, 3.95), post=(t_cut, storm_post))

# ================= S3 Black pod: real photos of the disease, then the loss figure ==================
c_end = wt(3, "Worldwide") - 0.25
def cards_post(frame, t, t0):
    a = ease((t - (wt(3, "black") - 0.4)) / 0.5) * (1 - ease((t - (c_end - 0.2)) / 0.5))
    if a > 0:
        small = cv2.GaussianBlur(cv2.resize(frame, (W // 4, H // 4)), (0, 0), 3)
        frame = (frame.astype(np.float32) * (1 - a) + cv2.resize(small, (W, H)).astype(np.float32) * 0.42 * a).astype(np.uint8)
    return frame
shot(S0(3), S1(3), F("shot3_stream_drainage.mp4"), fit_rate(S0(3), S1(3), 0.0, 7.9), kenburns(1.0, 1.08, S0(3), S1(3)), fade=0.25, post=(S0(3), cards_post))
CARDS = [("13_black_pod.jpg", wt(3, "black") - 0.1, 470, 455, -5), ("12_black_pod.jpg", wt(3, "splashes") - 0.1, 960, 430, 3),
         ("11_black_pod.jpg", wt(3, "carry") - 0.1, 1450, 465, -2)]
for f, t0, cx, cy, deg in CARDS:
    im = rgba_img(PH / f, h=430); im = im.crop(((im.width - min(im.width, 470)) // 2, 0, (im.width - min(im.width, 470)) // 2 + min(im.width, 470), im.height))
    arr = rot(shadowed(im, radius=10, border=10), deg)
    text(t0, c_end, arr, cx - arr.shape[1] / 2, cy - arr.shape[0] / 2, fi=0.35, fo=0.4, rise=30)
cap = text_img("bp_cap", [("Black pod (Phytophthora palmivora)", "SemiBold", 34, (255, 255, 255, 255), 6), ("Real photos: Scot Nelson, CC0", "Regular", 22, (255, 255, 255, 190), 0)], center=True)
text(wt(3, "black") + 0.2, c_end, cap, (W - cap.shape[1]) / 2, 790, rise=0)
text(wt(3, "twenty") - 0.15, S1(3) - 0.2,
     text_img("stat", [("20–30%", "SemiBold", 132, (255, 255, 255, 255), 6), ("of the world's cocoa lost to black pod each year", "Medium", 34, (255, 255, 255, 235), 14),
                       ("Estimate: Guest, 2007", "Regular", 24, (255, 255, 255, 190), 0)], pad=40, box=(12, 22, 18, 150), radius=18), None, 300)

# ================= S4 The farmer: who this is about, then the farm he has to choose from ==================
f_end = wt(4, "eight") - 0.45
shot(S0(4), f_end, F("farmer1_after_storm.mp4"), fit_rate(S0(4), f_end, 0.0, 7.7), fade=0.5)
text(wt(4, "most") - 0.1, wt(4, "After") - 0.2, text_img("sh86", [("86%", "SemiBold", 96, (255, 255, 255, 255), 4), ("of Malaysia's cocoa land is smallholdings", "Medium", 30, (255, 255, 255, 235), 10),
                                                           ("Malaysian Cocoa Board, 2025", "Regular", 22, (255, 255, 255, 190), 0)], pad=34, box=(12, 22, 18, 150), radius=16), 96, 560)
OBL = HERE.parent / "v5/flow_frames/shot1_first_oblique.jpeg"
shot(f_end, S1(4), OBL, lambda t: 0, kenburns(1.10, 1.0, f_end, S1(4), src=(1376, 768)), kind="still", fade=0.4)
for i, (w0, lab) in enumerate([("eight", "8 blocks"), ("where", "Where to start?")], 1):
    text(wt(4, w0) - 0.1, S1(4) - 0.2, text_img(f"chip{i}", [(lab, "SemiBold", 40, (255, 255, 255, 255), 0)], pad=22, box=(12, 22, 18, 165), radius=12), 120, 600 + i * 104, rise=10)


# ---------- the golden half-hour: a countdown that starts in S4 and comes back at "Two minutes in" (S9) ----------
AMBER = (255, 178, 84)
def clock_img(secs_left):
    w, h = 470, 150; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=(12, 22, 18, 170))
    cx, cy, r = 78, 75, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 60), width=8)
    frac = max(0.0, secs_left / 1800.0)
    if frac > 0: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=AMBER + (255,), width=8)
    m, s = divmod(int(math.ceil(secs_left)), 60)
    d.text((150, 22), f"{m:02d}:{s:02d}", font=font("SemiBold", 62), fill=(255, 255, 255, 255))
    d.text((153, 98), "Golden half-hour", font=font("Medium", 26), fill=AMBER + (240,))
    return np.array(im)
CLOCKS = [(wt(4, "golden") - 0.1, S1(4) - 0.2, 1800.0, 120, 470),            # 30:00 starts running
          (wt(9, "Two") - 0.1, wt(9, "He") - 0.35, 1680.0, 96, 96)]          # two minutes in: 28:00
CLOCK_RATE = 6.0   # clock seconds per film second
def clocks(frame, t):
    for t0, t1, start, x, y in CLOCKS:
        e = fade_env(t, t0, t1, 0.35, 0.3)
        if e > 0: paste(frame, clock_img(start - max(0.0, t - t0) * CLOCK_RATE), x, y + (1 - ease(e)) * 10, ease(e))
    return frame

# ================= S5 KokoShield: logo over the descent, which lands on the app's map ==================
D0 = S0(5); DL = D0 + 6.6
def descent_xf(t):
    k = ease((t - (D0 + 4.9)) / 1.7); return 1.5 + 0.15 * k, 0.0, -21.0 * k
shot(D0, DL, F("shot1_descent_to_aerial.mp4"), speed(D0, 0.0), descent_xf, post=(D0, logo_post(D0 + 0.35, DL - 0.75)))
ACT = json.load(open(REC / "plan_activate.json")); X = wt(5, "millimetres") - 0.1
shot(DL, S1(5), REC / "plan_activate.mp4", remap([(DL - 0.6, 0.3), (X, ACT["marks"]["switch"]), (S1(5), ACT["marks"]["switch"] + (S1(5) - X))]), fade=0.6, audio=False)
popout(X + 0.35, S1(5) - 0.3, (1561, 158, 335, 93), (1150, 220), 1.6)

# ================= S6 The clues: drone, sensor (product shot), then everything feeding the score ==================
a, b, c = S0(6), wt(6, "shows") - 0.1, wt(6, "A", 2) - 0.25
shot(a, b, F("drone_closeup_flyaway.mp4"), speed(a, 0.3), fade=0.35)
shot(b, c, F("drone_topdown_pass.mp4"), fit_rate(b, c, 1.0, 6.6))

NODE = json.load(open(HERE / "node/anchors.json"))["anchors"]; NF = HERE / "node/frames"
n_end = wt(6, "Add") + 0.6   # the Field Node and its labels hold 0.75 s into "Add the rain gauge"
node_u = remap([(c, 0.4), (wt(6, "damp"), 3.9), (n_end, 5.6)])
def studio():
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    spot = np.exp(-(((xx - 960) / 760) ** 2 + ((yy - 470) / 430) ** 2))
    floor = np.clip((yy - 780) / 300, 0, 1)
    base = np.array((22, 30, 26), np.float32)[None, None] + spot[..., None] * np.array((50, 62, 56), np.float32)[None, None]
    base = base * (1 - 0.35 * floor[..., None]) + floor[..., None] * np.array((10, 14, 12), np.float32)[None, None]
    hz = np.exp(-((yy - 780) / 22) ** 2)[..., None] * 9
    return np.clip(base + hz, 0, 255)[..., ::-1].astype(np.uint8)
STUDIO = studio()


class NodeShot:
    """Product showcase: studio sweep + soft spotlight + mirror reflection under the product, the rendered node on top."""
    def at(self, u):
        i = min(len(NODE) - 1, max(0, int(round(u * 30)))); fr = np.array(Image.open(NF / f"f{i:04d}.png"))
        out = STUDIO.copy()
        solid = np.nonzero((fr[..., 3] > 200).any(1))[0]
        if len(solid):
            yb = int(solid[-1]); h_ = min(H - yb, yb)
            ref = fr[yb - 1: yb - 1 - h_: -1].copy() if h_ > 0 else None
            if ref is not None and len(ref):
                fade = (0.18 * np.clip(1 - np.arange(len(ref)) / 260.0, 0, 1))[:, None]
                ref[..., 3] = (ref[..., 3].astype(np.float32) * fade).astype(np.uint8)
                full = np.zeros_like(fr); full[yb: yb + len(ref)] = cv2.GaussianBlur(ref, (0, 0), 2.5); paste(out, full, 0, 0)
        paste(out, fr, 0, 0); return out


NS_ = NodeShot()
SHOTS.append(dict(t0=c, t1=n_end + 0.6, src=type("S", (), {"at": lambda self, u: NS_.at(u)})(), path="node", time=node_u, xf=lambda t: (1.0, 0.0, 0.0), fade=0.35, audio=False, post=None))
CALL = [("hood", "Vented sensor hood", "air temperature and humidity", (1, 1)), ("lid", "Removable lid", "3.2 mm, 3D-printed", (1, -1)),
        ("base", "86 × 62 × 32 mm enclosure", "3D-printed", (-1, 1)), ("board", "ESP32-class controller", "size envelope", (-1, 1))]
def callouts(frame, t):
    if not (c <= t <= n_end + 0.6): return frame
    u = node_u(t); i = min(len(NODE) - 1, int(round(u * 30))); A = NODE[i]
    e = ease((u - 4.0) / 0.6) * (1 - ease((t - n_end) / 0.4))
    if e <= 0: return frame
    for k, (name, l1, l2, (dx, dy)) in enumerate(CALL):
        ax, ay = A[name]; e2 = ease((u - 4.0 - 0.2 * k) / 0.5) * (1 - ease((t - n_end) / 0.4))
        if e2 <= 0: continue
        lab = text_img("call" + name, [(l1, "SemiBold", 30, (255, 255, 255, 255), 4), (l2, "Regular", 24, (215, 228, 220, 255), 0)], center=False)
        ex = ax + dx * (230 if name != "board" else 330); ey = ay + dy * (120 if name != "board" else 170)
        ex = min(ex, W - 60 - lab.shape[1]) if dx > 0 else max(ex, 60 + lab.shape[1]); ey = min(max(ey, 150), H - 230)
        mx = ax + (ex - ax) * e2; my = ay + (ey - ay) * e2
        cv2.circle(frame, (int(ax), int(ay)), 6, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.line(frame, (int(ax), int(ay)), (int(mx), int(my)), (235, 240, 236), 2, cv2.LINE_AA)
        lx = ex + (14 if dx > 0 else -14 - lab.shape[1]); ly = ey - lab.shape[0] / 2
        paste(frame, lab, lx, ly, e2)
    tag = text_img("concept", [("KokoShield Field Node, concept prototype", "Medium", 26, (255, 255, 255, 230), 0)], pad=14, box=(0, 0, 0, 110), radius=8)
    paste(frame, tag, 48, 48, ease((u - 0.4) / 0.6) * (1 - ease((t - n_end) / 0.4)))
    return frame


# ---- the link: four clues flow into KokoShield, which turns into the ranked plan ----
L0, L1 = n_end, S1(6)
def card(path, title, sub, w=380):
    im = rgba_img(path, w=w)
    if im.height > 230: im = im.crop((0, (im.height - 230) // 2, im.width, (im.height - 230) // 2 + 230))
    body = Image.new("RGBA", (w + 28, im.height + 112), (24, 36, 30, 236)); body.alpha_composite(im, (14, 14))
    lab = Image.fromarray(text_img("lk" + title, [(title, "SemiBold", 28, (255, 255, 255, 255), 2), (sub, "Regular", 22, (200, 218, 208, 255), 0)]))
    body.alpha_composite(lab, (16, im.height + 24)); return shadowed(body, radius=14)
LINKS = [(card(BR / "card_drone.jpg", "Drone", "where water is standing"), (330, 280), L0 + 0.1),
         (card(BR / "card_node.jpg", "Field node", "air temperature and humidity"), (330, 800), L0 + 0.25),
         (card(BR / "card_rain.png", "Rain gauge", "48 mm in 24 hours", w=380), (1590, 280), max(wt(6, "rain"), L0 + 0.4)),
         (card(BR / "card_log.png", "Past outbreaks", "confirmed cases by block"), (1590, 800), max(wt(6, "past"), L0 + 0.55))]
CENTER = (960, 540)
def link_frame(t):
    fr = STUDIO.copy(); fr = (fr.astype(np.float32) * 0.8).astype(np.uint8)
    pulse_t0 = wt(6, "outbreaks")
    for arr, (cx, cy), t0 in LINKS:
        e = ease((t - t0) / 0.45)
        if e <= 0: continue
        ln = ease((t - t0 - 0.2) / 0.6)
        if ln > 0:
            x0, y0 = cx + (150 if cx < 960 else -150), cy; x1, y1 = CENTER[0] + (x0 - CENTER[0]) * 0.16, CENTER[1] + (y0 - CENTER[1]) * 0.16
            xe, ye = x0 + (x1 - x0) * ln, y0 + (y1 - y0) * ln
            cv2.line(fr, (int(x0), int(y0)), (int(xe), int(ye)), (120, 170, 140), 2, cv2.LINE_AA)
            if t > pulse_t0:
                for j in range(3):
                    q = ((t - pulse_t0) * 1.4 + j / 3) % 1; px, py = x0 + (x1 - x0) * q, y0 + (y1 - y0) * q
                    cv2.circle(fr, (int(px), int(py)), 7, (170, 240, 200), -1, cv2.LINE_AA)
        paste(fr, arr, cx - arr.shape[1] / 2, cy - arr.shape[0] / 2 + (1 - e) * 30, e)
    sc_t = wt(6, "score"); glow = ease((t - (sc_t - 0.4)) / 0.4)
    k = 0.85 + 0.15 * ease((t - L0) / 0.6) + 0.12 * glow
    sh = SHIELD.resize((int(190 * k), int(190 * k)), Image.LANCZOS)
    if glow > 0:
        g = Image.new("RGBA", (sh.width + 160, sh.height + 160), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([30, 30, g.width - 30, g.height - 30], fill=(95, 192, 149, int(150 * glow)))
        g = g.filter(ImageFilter.GaussianBlur(30)); paste(fr, np.array(g), CENTER[0] - g.width / 2, CENTER[1] - g.height / 2)
    paste(fr, np.array(sh), CENTER[0] - sh.width / 2, CENTER[1] - sh.height / 2, ease((t - L0) / 0.5))
    lbl = text_img("score_lbl", [("Every block gets a score", "SemiBold", 34, (255, 255, 255, 255), 0)], center=True)
    paste(fr, lbl, (W - lbl.shape[1]) / 2, CENTER[1] + 140, glow)
    return fr
SHOTS.append(dict(t0=L0, t1=L1, src=type("S", (), {"at": lambda self, t: link_frame(t)})(), path="link", time=lambda t: t, xf=lambda t: (1.0, 0.0, 0.0), fade=0.45, audio=False, post=None))

# ================= S7 The plan: route clicks re-timed to the spoken block letters ==================
ROUTE = json.load(open(REC / "plan_route.json")); RB = ROUTE["boxes"]; MK = ROUTE["marks"]
LIST = (1537, 330, 383, 245, 6); d = S0(7)
keys = [(d - 0.5, 0.4), (wt(7, "A") - 0.25, MK["stop1"] - 0.05), (wt(7, "D") - 0.2, MK["stop2"] - 0.05),
        (wt(7, "B") - 0.2, MK["stop3"] - 0.05), (wt(7, "G") - 0.2, MK["stop4"] - 0.05), (S1(7), MK["stop4"] + 1.2)]
shot(d, S1(7), REC / "plan_route.mp4", remap(keys), fade=0.5, audio=False)
highlight(d + 0.2, wt(7, "block") - 0.2, LIST, (1537, 251, 383, 75, 6))
for i, Lt in enumerate("ADBG", 1):
    t0 = wt(7, Lt) - 0.2; t1 = (wt(7, "ADBG"[i]) - 0.2) if i < 4 else S1(7) - 0.1
    r = RB[f"row{i}"]; highlight(t0, t1, (0, 55, 1536, 1025, 0), (r[0], r[1], r[2], r[3], 6))

# ================= S8 He heads out: walking into the farm, the phone screen ==================
g = wt(8, "His") - 0.25; WK = json.load(open(REC / "walk_phone.json"))["marks"]
shot(S0(8), S1(8), F("farmer2_he_goes.mp4"), speed(S0(8), 0.2), fade=0.3,
     post=(g, phone_post(REC / "walk_phone.mp4", [(g, WK["start"] + 0.7), (S1(8), WK["found"] - 0.25)], px=1180)))
text(g + 0.4, S1(8) - 0.1, text_img("walk", [("Scout's phone", "SemiBold", 40, (255, 255, 255, 255), 10), ("Each stop: why it is ranked,", "Regular", 30, (255, 255, 255, 225), 4),
                                         ("what to check, saved offline", "Regular", 30, (255, 255, 255, 225), 0)], pad=0), 330, 430)

# ================= S9 The find: the pod, the photo, the adviser's confirmation ==================
p1, p2 = wt(9, "He") - 0.2, wt(9, "and") - 0.15
shot(S0(9), p1, F("pod_black_pod_closeup.mp4"), fit_rate(S0(9), p1, 0.0, 3.95), fade=0.3)
shot(p1, p2, F("farmer3_find_photo.mp4"), speed(p1, 0.3))
LOG = json.load(open(REC / "log_confirm.json")); LM = LOG["marks"]
shot(p2, S1(9), REC / "log_confirm.mp4", remap([(p2, LM["confirm"] - 1.0), (wt(9, "confirms"), LM["confirm"] - 0.05), (S1(9), LM["confirm"] + 1.2)]), fade=0.3, audio=False)
highlight(p2 + 0.15, S1(9) - 0.35, (309, 318, 946, 72, 8))
text(p2 + 0.3, S1(9) - 0.6, text_img("adv", [("Adviser review", "SemiBold", 34, (255, 255, 255, 255), 0)], pad=16, box=(31, 90, 69, 235), radius=10), 1290, 330)

# ================= S10-S11 The race: real top-down view shrinks into the race map, then the race ==================
R0 = S0(10)
shot(R0, S1(11), REC / "race.mp4", lambda t: t - R0, audio=False)
# match move: shot1's final top-down frames, full screen, glide into the race's opening map (same image, same place)
M0, M1, M2 = R0, R0 + 0.45, wt(10, "help") + 0.15
BIG = (260, 196, 1400, 768)
def into_race(frame, t, t0):
    k = ease((t - M1) / (M2 - M1))
    s = 1.5 + (1.851 - 1.5) * k; tx = 173.85 * k; ty = -85.56 * k
    aer = warp(AER.at(7.0 + (t - M0) * 0.4), s, tx, ty)
    x0, y0, w0, h0 = 0 + (BIG[0]) * k, 0 + BIG[1] * k, W + (BIG[2] - W) * k, H + (BIG[3] - H) * k
    m = np.zeros((H, W), np.uint8); r = int(14 * k)
    cv2.rectangle(m, (int(x0) + r, int(y0)), (int(x0 + w0) - r, int(y0 + h0)), 255, -1); cv2.rectangle(m, (int(x0), int(y0) + r), (int(x0 + w0), int(y0 + h0) - r), 255, -1)
    for cx_, cy_ in ((x0 + r, y0 + r), (x0 + w0 - r, y0 + r), (x0 + r, y0 + h0 - r), (x0 + w0 - r, y0 + h0 - r)): cv2.circle(m, (int(cx_), int(cy_)), r, 255, -1, cv2.LINE_AA)
    a = (m.astype(np.float32) / 255)[..., None] * (1 - ease((t - M2) / 0.35))
    return (frame.astype(np.float32) * (1 - a) + aer.astype(np.float32) * a).astype(np.uint8)
AER = Video(F("shot1_descent_to_aerial.mp4"))
SHOTS[-1]["post"] = (R0 - 0.45, into_race)
SHOTS[-1]["fade"] = 0.4

# ================= S12 The pilot: the nod, the pull-back, his face, the map of Malaysia, the name ==================
q0, q1, q2 = wt(12, "That") - 0.25, wt(12, "and") - 0.25, wt(12, "We're") - 0.3
q4 = wt(12, "KokoShield") - 0.3; q3 = q4
shot(S0(12), q0, F("farmer3_find_photo.mp4"), fit_rate(S0(12), q0, 4.4, 8.0), fade=0.4)
shot(q0, q1, HERE / "work/shot1_reversed.mp4", fit_rate(q0, q1, 1.4, 4.6), lambda t: cover(1280, 720), fade=0.4)
shot(q1, q2, F("farmer1_after_storm.mp4"), fit_rate(q1, q2, 5.0, 8.0), fade=0.4)

# ---- impact card over the pull-back and his face: two spoken outcomes, then the SDG targets (Proposal v3, page 12) ----
i0 = wt(12, "spreads") - 0.2; i1 = q2 - 0.3; PX, PY = 96, 230
def panel(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(12, 22, 18, 175)); return np.array(im)
text(i0, i1, panel(700, 222), PX, PY, rise=0)
text(wt(12, "less") - 0.2, i1, panel(700, 160), PX, PY + 222, rise=0)
text(i0 + 0.15, i1, text_img("imp_k", [("Sustainable impact", "Medium", 26, (170, 236, 200, 255), 0)]), PX + 40, PY + 34, rise=8)
SDG = [np.array(rgba_img(HERE / f"brand/sdg/sdg_{n}_tile.png", w=128)) for n in ("02", "13")]
s_t = i0 + 0.4
for j, tile in enumerate(SDG): text(s_t + 0.12 * j, i1, tile, PX + 40 + j * 146, PY + 82, rise=10)
text(s_t + 0.3, i1, text_img("imp_sdg", [("SDG targets", "Medium", 26, (215, 228, 220, 255), 6), ("2.3, 2.4 and 13.1", "SemiBold", 34, (255, 255, 255, 255), 0)]), PX + 340, PY + 110, rise=8)
text(wt(12, "less") - 0.1, i1, text_img("imp_1", [("Fewer pods lost", "SemiBold", 44, (255, 255, 255, 255), 0)]), PX + 40, PY + 242, rise=10)
text(wt(12, "steadier") - 0.1, i1, text_img("imp_2", [("Steadier smallholder income", "SemiBold", 44, (255, 255, 255, 255), 0)]), PX + 40, PY + 306, rise=10)

GEO = json.load(open(HERE / "geo_malaysia.json"))
def rings(geom):
    cs = geom["coordinates"]; polys = cs if geom["type"] == "MultiPolygon" else [cs]
    return [np.array(p[0], np.float64) for p in polys]
LAND = [(f["properties"]["ADM0_A3"], r) for f in GEO["countries"] for r in rings(f["geometry"]) if 94 < r[:, 0].mean() < 125 and -3 < r[:, 1].mean() < 10]
STATES = [(f["properties"]["name"], r) for f in GEO["my_states"] for r in rings(f["geometry"])]
PIN = (101.565, 2.66); KL = (101.69, 3.14)
V_START = (109.6, 4.3, 24.0); V_END = (101.55, 2.95, 2.3)   # centre lon, centre lat, view width in degrees
z0, z1 = q2 + 0.2, wt(12, "Tanjung") + 0.2
def map_frame(t):
    k = ease((t - z0) / (z1 - z0)); kc = ease(min(1.0, (t - z0) / (z1 - z0) * 1.7)); cx = V_START[0] + (V_END[0] - V_START[0]) * kc; cy = V_START[1] + (V_END[1] - V_START[1]) * kc
    wdeg = math.exp(math.log(V_START[2]) + (math.log(V_END[2]) - math.log(V_START[2])) * k); s = W / wdeg
    P = lambda r: np.stack([(r[:, 0] - cx) * s + W / 2, -(r[:, 1] - cy) * s + H / 2], 1).astype(np.int32)
    yy, xx = np.mgrid[:H, :W]; fr = np.empty((H, W, 3), np.uint8); fr[:] = (40, 30, 18)  # deep sea, BGR
    fr = (fr.astype(np.float32) + (np.exp(-(((xx - 960) / 900) ** 2 + ((yy - 540) / 600) ** 2)) * 18)[..., None]).astype(np.uint8)
    for iso, r in LAND:
        col = (60, 82, 68) if iso == "MYS" else (44, 56, 49)
        cv2.fillPoly(fr, [P(r)], col, cv2.LINE_AA)
    sel_a = ease((t - (z1 - 1.0)) / 0.8)
    for name, r in STATES:
        pts = P(r)
        if name == "Selangor" and sel_a > 0:
            ov = fr.copy(); cv2.fillPoly(ov, [pts], (120, 170, 95), cv2.LINE_AA); fr = cv2.addWeighted(fr, 1 - 0.75 * sel_a, ov, 0.75 * sel_a, 0)
        cv2.polylines(fr, [pts], True, (110, 130, 118), 1, cv2.LINE_AA)
    for iso, r in LAND:
        if iso == "MYS": cv2.polylines(fr, [P(r)], True, (200, 220, 208), 1, cv2.LINE_AA)
    lab = lambda key, txt, size, col: text_img(key, [(txt, "SemiBold", size, col, 0)])
    paste(fr, lab("mys", "MALAYSIA", 40, (255, 255, 255, 200)), *(P(np.array([[102.4, 4.6]]))[0] - [110, 20]), 1 - ease(k * 1.6))
    kl = P(np.array([KL]))[0]
    if k > 0.6:
        cv2.circle(fr, tuple(int(v) for v in kl), 6, (235, 240, 236), -1, cv2.LINE_AA)
        paste(fr, lab("kl", "Kuala Lumpur", 28, (235, 240, 236, 230)), kl[0] + 14, kl[1] - 20, ease((k - 0.6) / 0.3))
    if sel_a > 0:
        sp = P(np.array([[101.45, 3.35]]))[0]; paste(fr, lab("sel", "SELANGOR", 34, (255, 255, 255, 220)), sp[0] - 260, sp[1] - 18, sel_a)
    pin_t = wt(12, "Sepat") - 0.1; e = ease((t - pin_t) / 0.45)
    if e > 0:
        px, py = P(np.array([PIN]))[0]
        for j in range(2):
            q = ((t - pin_t) * 0.8 + j * 0.5) % 1; cv2.circle(fr, (int(px), int(py)), int(14 + 70 * q), (120, 200, 150), 2, cv2.LINE_AA) if q > 0.02 else None
        cv2.circle(fr, (int(px), int(py - (1 - e) * 60)), 13, (70, 90, 230), -1, cv2.LINE_AA); cv2.circle(fr, (int(px), int(py - (1 - e) * 60)), 13, (255, 255, 255), 3, cv2.LINE_AA)
        lines = [("Tanjung Sepat, Selangor", "SemiBold", 40, (255, 255, 255, 255), 6), ("First pilot: a cocoa farm, in talks", "Medium", 28, (220, 236, 226, 255), 0)]
        if t > wt(12, "budget") - 0.2:
            lines[-1] = ("First pilot: a cocoa farm, in talks", "Medium", 28, (220, 236, 226, 255), 18)
            lines += [("Pilot plan: RM1,200", "SemiBold", 34, (170, 236, 200, 255), 8),
                      ("4 post-rain scouting rounds over about 6 weeks", "Regular", 24, (220, 236, 226, 235), 4),
                      ("Adviser reviews, travel, supplies, contingency", "Regular", 24, (220, 236, 226, 235), 0)]
        crd = text_img("pin" + str(len(lines)), lines, pad=26, box=(14, 26, 20, 225), radius=14)
        paste(fr, crd, px + 70, py - crd.shape[0] / 2, e)
    return fr
SHOTS.append(dict(t0=q2, t1=q3, src=type("S", (), {"at": lambda self, t: map_frame(t)})(), path="map", time=lambda t: t, xf=lambda t: (1.0, 0.0, 0.0), fade=0.5, audio=False, post=None))
text(q2 + 0.3, q3 - 0.2, text_img("mapsrc", [("Map: Natural Earth", "Regular", 20, (255, 255, 255, 150), 0)]), 48, H - 60, rise=0)



def endcard(frame, t, t0):
    e = ease((t - t0) / 0.6)
    small = cv2.GaussianBlur(cv2.resize(frame, (W // 8, H // 8)), (0, 0), 3); blur = cv2.resize(small, (W, H)).astype(np.float32)
    base = (blur * 0.30 + np.array((24, 40, 30), np.float32) * 0.70)
    return (frame.astype(np.float32) * (1 - e) + base * e).astype(np.uint8)
shot(q4, END, HERE / "work/shot1_reversed.mp4", lambda t: 7.9, lambda t: cover(1280, 720), fade=0.6, audio=False, post=(q4 - 0.6, endcard))
END_LOCK = np.array(lockup(1.0, "Find disease sooner, after the rain.", "endlock"))
text(q4 + 0.2, END + 1, END_LOCK, (W - END_LOCK.shape[1]) / 2, 400, fi=0.7, fo=0.0, rise=18)
# the team (Proposal v3 cover, same order) and the Universiti Malaya logo (um.edu.my, shown near its native size as a rounded badge)
team = text_img("team", [("Leow Shen En, Chong Pohyi, Choong Zhuo Lin, Lee Jia Shern, Teoh Xi Xian", "SemiBold", 34, (255, 255, 255, 240), 0)], center=True)
text(q4 + 0.6, END + 1, team, (W - team.shape[1]) / 2, 650, fi=0.6, fo=0.0, rise=10)
um = rgba_img(BR / "um_logo_site.png", h=68); badge = Image.new("RGBA", (um.width + 36, um.height + 20), (0, 0, 0, 0))
ImageDraw.Draw(badge).rounded_rectangle([0, 0, badge.width - 1, badge.height - 1], 12, fill=(255, 255, 255, 245)); badge.alpha_composite(um, (18, 10))
UM = np.array(badge)
text(q4 + 0.8, END + 1, UM, (W - UM.shape[1]) / 2, 728, fi=0.6, fo=0.0, rise=10)
credit = text_img("credit", [("Farm, farmer, drone and time-lapse footage: AI-generated with Google Flow. Disease photos: Scot Nelson, CC0. Voice: Microsoft neural TTS.", "Regular", 24, (255, 255, 255, 210), 8),
                             ("App: KokoShield Field Desk prototype with demo data. Map: Natural Earth. Sources: Guest (2007); Malaysian Cocoa Board (2025).", "Regular", 24, (255, 255, 255, 210), 8),
                             ("Thunder: loganzsound (Freesound), CC0. SDG icons: United Nations.", "Regular", 24, (255, 255, 255, 210), 0)], center=True)
text(q4 + 1.0, END + 1, credit, (W - credit.shape[1]) / 2, 930, fi=0.6, fo=0.0, rise=0)


# ---------------- subtitles ----------------
WEAK = {"a", "an", "the", "in", "to", "of", "for", "on", "and", "his", "he", "at", "twenty"}


def captions():
    from scenes_v6 import SCENES
    out = []
    for s in TL["scenes"]:
        words = [(s["speech_at"] + a, s["speech_at"] + b) for a, b, _ in s["words"]]
        toks = next(x for x in SCENES if x["id"] == s["id"])["text"].split(); assert len(toks) == len(words), (s["id"], len(toks), len(words))
        sent = []
        for i, tok in enumerate(toks):
            sent.append(i)
            if tok[-1] in ".;:?!" or i == len(toks) - 1:
                chunks = [sent]
                while any(len(" ".join(toks[j] for j in c)) > 46 for c in chunks):
                    c = max(chunks, key=lambda c: len(" ".join(toks[j] for j in c))); k = chunks.index(c)
                    L = len(" ".join(toks[j] for j in c)); best, acc = 1, 0
                    for m in range(1, len(c)):
                        acc = len(" ".join(toks[j] for j in c[:m])); end = toks[c[m - 1]]
                        score = abs(acc - L / 2) - (22 if end[-1] in ",:" else 0) + (60 if end.lower() in WEAK else 0) + (60 if max(acc, L - acc - 1) > 46 else 0)
                        if m == 1 or score < bscore: best, bscore = m, score
                    chunks[k:k + 1] = [c[:best], c[best:]]
                for c in chunks: out.append([words[c[0]][0], words[c[-1]][1], " ".join(toks[j] for j in c)])
                sent = []
    for x, y in zip(out, out[1:]): x[1] = min(y[0] - 0.04, x[1] + 0.5)
    q4 = wt(12, "KokoShield") - 0.3
    return [c for c in out if c[0] < q4 - 0.1]


CAPS = captions()
def draw_sub(frame, t):
    for a, b, line in CAPS:
        if a <= t <= b:
            img = text_img("sub:" + line, [(line, "Medium", 40, (255, 255, 255, 255), 0)], pad=16, box=(0, 0, 0, 165), radius=10)
            paste(frame, img, (W - img.shape[1]) / 2, H - 70 - img.shape[0]); return


# ---------------- render ----------------
def render_frame(t):
    frame = None
    for s in sorted([s for s in SHOTS if s["t0"] - s["fade"] <= t < s["t1"]], key=lambda s: s["t0"]):
        src = s["src"].at(s["time"](t)); h, w = src.shape[:2]
        sc, tx, ty = s["xf"](t) if s["xf"] else cover(w, h)
        img = src.copy() if (w, h) == (W, H) and (sc, tx, ty) == (1.0, 0.0, 0.0) else warp(src, sc, tx, ty)
        if s["post"] and t >= s["post"][0]: img = s["post"][1](img, t, s["post"][0])
        if frame is not None and t < s["t0"]:
            a = ease((t - (s["t0"] - s["fade"])) / s["fade"]); frame = cv2.addWeighted(frame, 1 - a, img, a, 0)
        else:
            frame = img
    if frame is None: frame = np.zeros((H, W, 3), np.uint8)
    base = frame.copy()
    frame = apply_highlights(frame, t)
    frame = apply_pops(frame, t, base)
    frame = callouts(frame, t)
    frame = clocks(frame, t)
    for t0, t1, img, x, y, fi, fo, rise in TEXTS:
        e = fade_env(t, t0, t1, fi, fo)
        if e > 0: paste(frame, img, x, y + (1 - ease(e)) * rise, ease(e))
    if t < 0.8: frame = (frame.astype(np.float32) * ease(t / 0.8)).astype(np.uint8)
    return frame


def encoder(path):
    return subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                             "-color_primaries", "bt709", "-color_trc", "bt709", str(path)], stdin=subprocess.PIPE)


if __name__ == "__main__":
    args = sys.argv[1:]
    json.dump([dict(t0=s["t0"], t1=s["t1"], path=s["path"], audio=s["audio"], src0=s["time"](s["t0"]), src1=s["time"](s["t1"] - 1 / FPS)) for s in SHOTS],
              open(HERE / "shots.json", "w"), indent=1)
    json.dump(CAPS, open(HERE / "captions.json", "w"), indent=1)
    if "--sheet" in args:
        ts = [float(x) for x in args[args.index("--sheet") + 1:]]
        for t in ts:
            f = render_frame(t); draw_sub(f, t); cv2.imwrite(str(WORK / f"sheet_{t:06.2f}.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 85])
        sys.exit()
    n = int(END * FPS); clean, subs = encoder(WORK / "film_clean.mp4"), encoder(WORK / "film_subs.mp4")
    import time; t0 = time.time()
    for i in range(n):
        t = i / FPS; f = render_frame(t); clean.stdin.write(f.tobytes()); draw_sub(f, t); subs.stdin.write(f.tobytes())
        if i % 300 == 0: print(f"{i}/{n} {time.time() - t0:.0f}s", flush=True)
    for e in (clean, subs): e.stdin.close(); e.wait()
    print("done", f"{time.time() - t0:.0f}s")
