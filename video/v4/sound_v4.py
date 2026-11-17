"""Soundtrack for the v4 (real-image) video: synthesised score, rain and SFX synced to on-screen events, ducked under the voice."""
import json, wave, subprocess
import numpy as np, imageio_ffmpeg
SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
S = json.load(open("timeline.json", encoding="utf-8"))["starts"]
END = S[-1]; N = int(END * SR)
rng = np.random.default_rng(11)
T = np.arange(N) / SR

def sm(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def ramp(t, a, b): return sm((t - a) / (b - a))
def bus(): return [np.zeros(N, np.float32), np.zeros(N, np.float32)]
MUS, SFX, RAIN = bus(), bus(), bus()

def add(b, t0, sig, gain=1.0, pan=0.0):
    i = int(round(t0 * SR)); sig = np.asarray(sig, np.float32)
    if i < 0: sig, i = sig[-i:], 0
    n = min(len(sig), N - i)
    if n <= 0: return
    gl, gr = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    b[0][i:i + n] += sig[:n] * gain * gl; b[1][i:i + n] += sig[:n] * gain * gr

def shaped(n, lo, hi, tilt=0.0):
    x = rng.standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    g = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    if tilt: g = g * (np.maximum(f, 20) / 1000.0) ** tilt
    y = np.fft.irfft(X * g, n); return y / (np.max(np.abs(y)) + 1e-9)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt(n): return np.arange(n) / SR

# ---------------- instruments ----------------
def pad(m, dur, att=0.8, rel=1.4):
    f = mtof(m); n = int((dur + rel) * SR); t = tt(n); y = np.zeros(n)
    for det in (-0.0035, 0.0035):
        for k in range(1, 7):
            if f * k > 5000: break
            y += np.sin(2 * np.pi * f * (1 + det) * k * t + k * 1.3) / k ** 1.6
    env = sm(t / att) * (1 - ramp(t, dur, dur + rel)); return y * env * 0.5
def pluck(m, dur=0.9):
    f = mtof(m); n = int(dur * SR); t = tt(n)
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.30) + 0.35 * np.sin(2 * np.pi * f * 3.99 * t) * np.exp(-t / 0.045)
         + 0.18 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / 0.12))
    return y * np.minimum(1, t / 0.003)
def bass(m, dur):
    f = mtof(m); n = int((dur + 0.4) * SR); t = tt(n)
    y = np.tanh(1.6 * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)))
    return y * np.minimum(1, t / 0.02) * np.exp(-t / 2.2) * (1 - ramp(t, dur, dur + 0.4))
def kick():
    n = int(0.4 * SR); t = tt(n); fr = 48 + 80 * np.exp(-t / 0.035)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.16)
def shaker():
    n = int(0.09 * SR); t = tt(n); return shaped(n, 5000, 14000) * np.exp(-t / 0.022)
def drone(m, dur):
    f = mtof(m); n = int(dur * SR); t = tt(n)
    y = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t) + 0.25 * np.sin(2 * np.pi * f * 2 * t)
    return y * (0.75 + 0.25 * np.sin(2 * np.pi * 0.12 * t)) * sm(t / 3) * (1 - ramp(t, dur - 3, dur))


# ---------------- score: tense minor until the solution (scene 4), hopeful major after, outro on the close ----------------
BAR = 2.5
MINOR = [(47, [59, 62, 66]), (43, [55, 59, 62]), (40, [55, 59, 64]), (42, [54, 58, 61])]
MAJOR = [(38, [57, 62, 66]), (45, [57, 61, 64]), (47, [59, 62, 66]), (43, [55, 59, 62])]
OUTRO = [(38, [57, 62, 66]), (43, [55, 59, 62]), (45, [57, 61, 64]), (38, [57, 62, 66, 69])]
A_END = S[3]
add(MUS, 0.0, drone(35, A_END + 1.0), 0.10, 0.0)
for b in range(int(np.ceil(A_END / BAR))):
    t0 = b * BAR; root, ch = MINOR[(b // 2) % 4]
    if b % 2 == 0:
        dur = min(2 * BAR, A_END - t0)
        if dur > 0.5:
            for j, m in enumerate(ch): add(MUS, t0, pad(m, dur - 0.2), 0.050, (j - 1) * 0.35)
    for q, idx in enumerate([0, 2, 1, 2]):
        tq = t0 + q * BAR / 4
        if tq >= A_END - 0.1 or (b < 2 and q % 2): continue
        add(MUS, tq, pluck(ch[idx] + 12, 0.8), 0.045 + 0.02 * (t0 >= A_END - 10), 0.25 * (idx - 1))
    if t0 >= A_END - 4 * BAR:
        for s16 in range(16):
            ts = t0 + s16 * BAR / 16
            if ts < A_END - 0.05: add(MUS, ts, pluck(ch[s16 % 3] + 24, 0.25), 0.014, 0.4 * ((s16 % 3) - 1))
n = int(2.6 * SR); add(MUS, A_END - 2.6, shaped(n, 800, 9000) * ramp(tt(n), 0, 2.6) ** 2, 0.06)
n = int(2.2 * SR); add(MUS, A_END - 0.05, shaped(n, 300, 12000, -0.4) * np.exp(-tt(n) / 0.5), 0.07)
B_END = S[8]
for b in range(int(np.ceil((B_END - A_END) / BAR))):
    t0 = A_END + b * BAR; root, ch = MAJOR[b % 4]; d = min(BAR, B_END - t0)
    if d < 0.4: continue
    for j, m in enumerate(ch): add(MUS, t0, pad(m, d - 0.1, 0.4, 1.0), 0.045, (j - 1) * 0.35)
    add(MUS, t0, bass(root, d - 0.15), 0.11)
    for e, idx in enumerate([0, 1, 2, 1, 0, 2, 1, 2]):
        if e * BAR / 8 < d - 0.05: add(MUS, t0 + e * BAR / 8, pluck(ch[idx] + 12, 0.7), 0.05, 0.3 * (idx - 1))
    if t0 >= S[4] - 0.01:
        for beat in (0, 2):
            if beat * BAR / 4 < d: add(MUS, t0 + beat * BAR / 4, kick(), 0.16)
    if S[6] - 0.01 <= t0 < S[7]:
        for e in range(8):
            if e * BAR / 8 < d: add(MUS, t0 + e * BAR / 8, shaker(), 0.035 if e % 2 else 0.05, 0.3)
for k, (root, ch) in enumerate(OUTRO):
    t0 = B_END + k * BAR; last = k == 3; d = (END - t0) if last else BAR
    if d < 0.5: continue
    for j, m in enumerate(ch): add(MUS, t0, pad(m, d - 0.2, 0.5, 1.2 if not last else 0.6), 0.05, (j - 1.5) * 0.3)
    add(MUS, t0, bass(root, d - 0.3), 0.08)
    for e, idx in enumerate([0, 1, 2, 1] if not last else [0, 1, 2, 3]): add(MUS, t0 + e * BAR / 4, pluck(ch[idx] + 12, 1.2), 0.05, 0.3 * (idx - 1))
fade = (ramp(T, 0.0, 3.0) * (1 - ramp(T, END - 3.0, END - 0.1))).astype(np.float32)
MUS[0] *= fade; MUS[1] *= fade

# ---------------- ambience: rain (matches the on-screen rain) + thunder (after each lightning flash) ----------------
rain_env = np.maximum(np.minimum(ramp(T, 0, 1.2), 1 - ramp(T, S[1] + 1.5, S[1] + 4.5)),
                      0.55 * np.minimum(ramp(T, S[3] + 4.4, S[3] + 5.0), 1 - ramp(T, S[3] + 6.6, S[3] + 7.4))).astype(np.float32)
for c in (0, 1):
    hiss = shaped(N, 250, 7000, -0.6)
    drops = np.zeros(N); k = rng.random(N) < 45 / SR; drops[k] = rng.uniform(0.2, 1.0, k.sum())
    ker = np.sin(2 * np.pi * rng.uniform(2500, 4500) * tt(240)) * np.exp(-tt(240) / 0.0015)
    drops = np.fft.irfft(np.fft.rfft(drops, N + 240) * np.fft.rfft(ker, N + 240), N + 240)[:N]
    RAIN[c] += ((0.8 * hiss + 0.25 * drops / (np.max(np.abs(drops)) + 1e-9)) * rain_env).astype(np.float32)
def thunder(seed):
    n = int(3.6 * SR); t = tt(n)
    crack = shaped(n, 900, 9000) * np.exp(-t / 0.05)
    rumble = shaped(n, 25, 260, -1.0) * (np.exp(-t / 1.1) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.7 * t + seed) ** 2))
    return 0.35 * crack + rumble
add(SFX, 2.35, thunder(0.3), 0.30, -0.3); add(SFX, 5.65, thunder(1.7), 0.26, 0.35)

# ---------------- SFX library ----------------
def tick():
    n = int(0.03 * SR); t = tt(n); return np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.006)
def pop(f=700):
    n = int(0.16 * SR); t = tt(n); fr = f * (1 + 0.6 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.05) * np.minimum(1, t / 0.002)
def whoosh(dur=0.8):
    n = int(dur * SR); t = tt(n); lo = shaped(n, 150, 1500); hi = shaped(n, 1200, 8000)
    k = ramp(t, 0, dur); env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return ((1 - k) * lo + k * hi) * env
def bell(f, dec=0.9):
    n = int((dec * 3) * SR); t = tt(n)
    y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (dec * d)) for r, a, d in ((1, 1, 1), (2.76, .45, .45), (5.4, .25, .22), (2.0, .3, .6)))
    return y * np.minimum(1, t / 0.002)
def thud():
    n = int(0.3 * SR); t = tt(n); fr = 95 + 60 * np.exp(-t / 0.03); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.09)
def buzz():
    n = int(0.22 * SR); t = tt(n); return np.tanh(3 * np.sin(2 * np.pi * 110 * t)) * np.exp(-t / 0.08) * np.minimum(1, t / 0.005)
def blip(f=880):
    n = int(0.7 * SR); t = tt(n); fr = f * (1 - 0.25 * ramp(t, 0, 0.5)); y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.16)
    return y + 0.4 * np.concatenate([np.zeros(int(0.18 * SR)), y[: n - int(0.18 * SR)]])
def sweep(dur, f0=300, f1=1100):
    n = int(dur * SR); t = tt(n); fr = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / dur) ** 2 * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
def clunk():
    n = int(0.25 * SR); t = tt(n); return 0.6 * shaped(n, 600, 5000) * np.exp(-t / 0.012) + thud()[:n] * 0.8
def chime(base=74):
    y = np.zeros(int(2.4 * SR))
    for k, m in enumerate([base, base + 4, base + 7, base + 12]):
        b = bell(mtof(m), 0.7); i = int(k * 0.09 * SR); y[i:i + len(b)] += b[: len(y) - i] * (0.8 - 0.1 * k)
    return y


def drone_hum(dur):
    n = int(dur * SR); t = tt(n); f = 205 + 6 * np.sin(2 * np.pi * 0.7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = 0.6 * np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3) + 0.2 * np.sin(3 * ph + 1.1) + 0.25 * shaped(n, 2500, 7000)
    return y * (0.75 + 0.25 * np.sin(2 * np.pi * 31 * t)) * np.minimum(sm(t / 0.4), 1 - sm((t - dur + 0.5) / 0.5))
def drip(f=1300):
    n = int(0.35 * SR); t = tt(n); fr = f * (1 + 0.8 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.07)
def click():
    n = int(0.06 * SR); t = tt(n)
    return 0.7 * shaped(n, 1500, 8000) * np.exp(-t / 0.004) + 0.5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.02)
def shutter():
    a = click(); y = np.zeros(int(0.25 * SR)); y[:len(a)] += a; i = int(0.09 * SR); y[i:i + len(a)] += 0.8 * a; return y


def at(t, sig, g, pan=0.0): add(SFX, t, sig, g, pan)
def sc(i, x): return S[i] + x
for k in range(1, len(S) - 1): at(S[k] - 0.4, whoosh(0.8), 0.20, -0.2)          # brand wipe between scenes
# 1 hook: clock ticks, rain-gauge trigger chime, shot changes, pod labels
for k in range(8): at(1.0 + k * 0.25, tick(), 0.09, 0.2)
at(3.85, bell(988, 0.35), 0.10, 0.5); at(3.99, bell(1318, 0.35), 0.09, 0.5)
at(3.3, whoosh(0.5), 0.05); at(6.5, whoosh(0.5), 0.05)
at(sc(0, 7.2), pop(820), 0.09, -0.3); at(sc(0, 7.7), pop(560), 0.10, 0.3); at(sc(0, 7.72), thud(), 0.10, 0.3)
# 2 climate risk: three cards, count-ups, country chips
for c0 in (sc(1, 1.6), sc(1, 6.9), sc(1, 13.1)): at(c0, whoosh(0.45), 0.08, -0.4)
for k in range(10): at(sc(1, 1.85) + 1.5 * (k / 10) ** 0.8, tick(), 0.06, -0.4)
at(sc(1, 3.4), pop(820), 0.09, -0.4)
for k in range(3): at(sc(1, 7.3 + k * 0.5), pop(640 + 90 * k), 0.08, -0.3 + 0.2 * k)
for k in range(14): at(sc(1, 13.55) + 1.9 * (k / 14) ** 0.8, tick(), 0.06, -0.4)
at(sc(1, 15.5), pop(900), 0.09, -0.4)
# 3 market gap: axes, tool dots, empty corner, KokoShield lands
at(sc(2, 0.7), sweep(1.0, 400, 700), 0.05, 0.4)
for k, d in enumerate([2.0, 2.7, 3.4, 4.1, 4.8]): at(sc(2, d), pop(560 + 70 * k), 0.08, 0.5)
at(sc(2, 6.0), sweep(1.2, 900, 1600), 0.04, 0.6)
at(sc(2, 8.6), thud(), 0.16, 0.6); at(sc(2, 8.62), chime(74), 0.11, 0.6)
# 4 drone survey (two flights, standing water drips) + Field Node callouts
at(sc(3, 2.4), drone_hum(2.3), 0.10, -0.2); at(sc(3, 4.5), drone_hum(2.3), 0.10, 0.2)
at(sc(3, 4.5), bell(1175, 0.4), 0.07)
for d, f in ((5.33, 1500), (5.79, 1300), (6.22, 1150)): at(sc(3, d), drip(f), 0.12, -0.2)
at(sc(3, 6.65), chime(79), 0.06)
at(sc(3, 7.7), whoosh(0.5), 0.08)
for k in range(4): at(sc(3, 8.4 + 0.4 * k), pop(700 + 80 * k), 0.07, -0.3)
# 5 ranked route on the real app: two clicks, route changes, zoom, phone + print
at(sc(4, 0.2), whoosh(0.5), 0.08)
at(sc(4, 1.55), click(), 0.16); at(sc(4, 2.65), click(), 0.16); at(sc(4, 2.9), chime(76), 0.07)
at(sc(4, 3.7), whoosh(0.6), 0.06); at(sc(4, 7.0), whoosh(0.5), 0.08)
# 6 record and confirm: camera shutter, confirm dings, rule-out thud
at(sc(5, 0.4), whoosh(0.5), 0.08, 0.6); at(sc(5, 1.2), shutter(), 0.14, 0.6)
at(sc(5, 3.0), whoosh(0.5), 0.07)
at(sc(5, 4.6), click(), 0.12); at(sc(5, 4.62), bell(1318, 0.45), 0.10)
at(sc(5, 5.6), click(), 0.12); at(sc(5, 5.62), bell(1480, 0.45), 0.10)
at(sc(5, 6.6), click(), 0.12); at(sc(5, 6.62), thud(), 0.16)
at(sc(5, 7.4), chime(79), 0.06)
# 7 pilot race: start beeps, clock, finds, finish, misses, facts
r0, r1 = sc(6, 1.4), sc(6, 11.4)
at(r0 - 0.5, bell(660, 0.18), 0.08); at(r0, bell(880, 0.25), 0.09)
for k in range(15): at(r0 + k * (r1 - r0) / 15, tick(), 0.05, 0.6)
for m, pods in ((7, 3), (14, 2), (22, 1), (30, 1)):
    for p in range(pods): at(r0 + (r1 - r0) * m / 30 + p * 0.09, bell(1568 + 120 * p, 0.3), 0.08, -0.3)
for m in (8, 30): at(r0 + (r1 - r0) * m / 30 + 0.05, bell(784, 0.25), 0.07, -0.3)
at(r1 + 0.05, bell(523, 1.1), 0.08)
at(r1 + 0.15, buzz(), 0.09, -0.4); at(r1 + 0.4, buzz(), 0.08, -0.4)
at(sc(6, 12.0), whoosh(0.5), 0.08, 0.6)
for k in range(5): at(sc(6, 12.45 + 0.6 * k), pop(700 + 50 * k), 0.07, 0.6)
# 8 impact and market
at(sc(7, 0.9), whoosh(0.5), 0.08); at(sc(7, 5.6), whoosh(0.5), 0.08)
for k in range(3): at(sc(7, 6.0 + 1.6 * k), blip(1320), 0.03, -0.3); at(sc(7, 6.7 + 1.6 * k), blip(1480), 0.03, 0.3)
at(sc(7, 10.7), whoosh(0.45), 0.07)
for k in range(20): at(sc(7, 11.2) + 1.6 * k / 20, tick(), 0.05, -0.2)
for k in range(20): at(sc(7, 13.2) + 1.8 * k / 20, tick(), 0.05, 0.2)
at(sc(7, 15.1), chime(76), 0.07)
# 9 close + end card
at(sc(8, 0.65), chime(74), 0.09, -0.3)
at(END - 2.2, chime(74), 0.08); at(END - 2.15, bell(587, 1.4), 0.06)

# ---------------- mix with ducking ----------------
w = wave.open("voice_track_v4.wav"); voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
def smooth(x, sec): k = max(1, int(sec * SR)); c = np.cumsum(np.insert(x, 0, 0)); y = (c[k:] - c[:-k]) / k; return np.pad(y, (k // 2, k - 1 - k // 2), mode="edge")
lvl = np.sqrt(smooth(voice ** 2, 0.08)); gate = np.clip(lvl / 0.05, 0, 1)
gate = np.maximum(gate, np.roll(smooth(gate, 0.45), int(0.2 * SR)))      # hold ~0.4 s after speech
duck = smooth(gate, 0.12)
music_gain = (0.42 * (1 - 0.60 * duck)).astype(np.float32)
rain_gain = (0.20 * (1 - 0.40 * duck)).astype(np.float32)
mixL = voice * 0.92 + MUS[0] * music_gain + RAIN[0] * rain_gain + SFX[0] * (1 - 0.25 * duck)
mixR = voice * 0.92 + MUS[1] * music_gain + RAIN[1] * rain_gain + SFX[1] * (1 - 0.25 * duck)
mix = np.stack([mixL, mixR], 1)
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
mix *= 0.89 / np.max(np.abs(mix))
for name, part in (("music", MUS[0] * music_gain), ("rain", RAIN[0] * rain_gain), ("sfx", SFX[0]), ("voice", voice)):
    print(f"{name:6s} peak {np.max(np.abs(part)):.2f}  rms {np.sqrt(np.mean(part ** 2)):.3f}")
np.savez_compressed("mixparts_v4.npz", music=(MUS[0] * music_gain)[::480], rain=(RAIN[0] * rain_gain)[::480], sfx=SFX[0][::480], voice=voice[::480])
w = wave.open("soundtrack_v4.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack_v4.wav", "-c:a", "aac", "-b:a", "192k", "soundtrack_v4.m4a"], check=True)
print("soundtrack:", f"{N / SR:.2f}s")
