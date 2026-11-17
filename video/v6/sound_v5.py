"""Soundtrack for the v5 cinematic video: four-act score, rain and SFX synced to on-screen events, ducked under the voice."""
import json, wave, subprocess
import numpy as np, imageio_ffmpeg
SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
_tl = json.load(open("timeline.json", encoding="utf-8")); S = _tl["starts"]; END = _tl["end"]; N = int(END * SR)
rng = np.random.default_rng(11); T = np.arange(N) / SR
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


# ---------------- score: act 1 ticking dread, act 2 electronic pulse, act 3 driving peak, act 4 hopeful resolve ----------------
BAR = 2.5
MINOR = [(47, [59, 62, 66]), (43, [55, 59, 62]), (40, [55, 59, 64]), (42, [54, 58, 61])]
MAJOR = [(38, [57, 62, 66]), (45, [57, 61, 64]), (47, [59, 62, 66]), (43, [55, 59, 62])]
OUTRO = [(38, [57, 62, 66]), (43, [55, 59, 62]), (45, [57, 61, 64]), (38, [57, 62, 66, 69])]
def arp_pulse(f, dur):
    n = int(dur * SR); t = tt(n); y = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 7)) * np.exp(-t / 0.12) * np.minimum(1, t / 0.004); return y * 0.5
A1 = S[2]
add(MUS, 0.0, drone(35, A1 + 0.5), 0.12)
for b in range(int(np.ceil(A1 / BAR))):
    t0 = b * BAR; root, ch = MINOR[(b // 2) % 4]
    if b % 2 == 0:
        d = min(2 * BAR, A1 - t0)
        if d > 0.5:
            for j, m in enumerate(ch): add(MUS, t0, pad(m, d - 0.2), 0.055, (j - 1) * 0.35)
    for q in range(4):
        tq = t0 + q * BAR / 4
        if tq < A1 - 0.1: add(MUS, tq, pluck(ch[[0, 2, 1, 2][q]] + 12, 0.5), 0.03 + 0.03 * (tq / A1), 0.2 * ((q % 3) - 1))
    if t0 >= A1 - 4 * BAR:
        for s16 in range(16):
            ts = t0 + s16 * BAR / 16
            if ts < A1 - 0.05: add(MUS, ts, pluck(ch[s16 % 3] + 24, 0.25), 0.016, 0.4 * ((s16 % 3) - 1))
n = int(3.0 * SR); add(MUS, A1 - 3.0, shaped(n, 600, 9000) * ramp(tt(n), 0, 3.0) ** 2, 0.07)
A2 = S[2] + 5.0; A3 = S[5]; A4 = S[7]
BPM2 = 2.0
for b in range(int(np.ceil((A3 - A2) / BPM2))):
    t0 = A2 + b * BPM2; root, ch = MAJOR[b % 4]; d = min(BPM2, A3 - t0)
    if d < 0.3: continue
    add(MUS, t0, bass(root, d - 0.1), 0.10 + 0.03 * min(1, b / 6))
    for e in range(8):
        te = t0 + e * BPM2 / 8
        if te < A3 - 0.05: add(MUS, te, arp_pulse(mtof(ch[e % 3] + 12), 0.3), 0.045 + 0.015 * min(1, b / 6), 0.35 * ((e % 3) - 1))
    for beat in (0, 2):
        if beat * BPM2 / 4 < d: add(MUS, t0 + beat * BPM2 / 4, kick(), 0.14)
    for e in (1, 3, 5, 7):
        if e * BPM2 / 8 < d: add(MUS, t0 + e * BPM2 / 8, shaker(), 0.04, 0.3)
BPM3 = 1.8
for b in range(int(np.ceil((A4 - A3) / BPM3))):
    t0 = A3 + b * BPM3; root, ch = MAJOR[b % 4]; d = min(BPM3, A4 - t0)
    if d < 0.3: continue
    for j, m in enumerate(ch): add(MUS, t0, pad(m + 12, d - 0.1, 0.2, 0.8), 0.04, (j - 1) * 0.35)
    add(MUS, t0, bass(root, d - 0.1), 0.13)
    for e in range(8):
        te = t0 + e * BPM3 / 8
        if te < A4 - 0.05: add(MUS, te, arp_pulse(mtof(ch[e % 3] + 24), 0.25), 0.05, 0.35 * ((e % 3) - 1))
    for beat in range(4):
        if beat * BPM3 / 4 < d: add(MUS, t0 + beat * BPM3 / 4, kick(), 0.15 if beat % 2 == 0 else 0.09)
    for e in range(8):
        if e * BPM3 / 8 < d: add(MUS, t0 + e * BPM3 / 8, shaker(), 0.05 if e % 2 else 0.035, 0.3)
A5 = S[8] + 9.4
for b in range(int(np.ceil((A5 - A4) / BAR))):
    t0 = A4 + b * BAR; root, ch = (OUTRO if t0 >= S[8] else MAJOR)[b % 4]; d = min(BAR, A5 - t0)
    if d < 0.4: continue
    for j, m in enumerate(ch): add(MUS, t0, pad(m, d - 0.1, 0.5, 1.2), 0.06, (j - 1) * 0.35)
    add(MUS, t0, bass(root, d - 0.2), 0.10)
    for e, idx in enumerate([0, 1, 2, 1]): add(MUS, t0 + e * BAR / 4, pluck(ch[idx] + 12, 1.1), 0.05, 0.3 * (idx - 1))
    if t0 < S[8]:
        for beat in (0, 2): add(MUS, t0 + beat * BAR / 4, kick(), 0.1)
add(MUS, A5, pad(50, END - A5 - 0.3, 0.4, 0.8), 0.06); add(MUS, A5, pad(57, END - A5 - 0.3, 0.4, 0.8), 0.05); add(MUS, A5, bass(38, END - A5 - 0.5), 0.09)
fade = (ramp(T, 0.0, 2.5) * (1 - ramp(T, END - 2.5, END - 0.1))).astype(np.float32)
MUS[0] *= fade; MUS[1] *= fade

# ---------------- ambience: rain matching the on-screen rain ----------------
rain_env = np.maximum(np.minimum(ramp(T, 0, 1.0), 1 - ramp(T, S[1] + 0.2, S[1] + 2.2)), 0.35 * np.minimum(ramp(T, S[1] + 2.0, S[1] + 3), 1 - ramp(T, S[2] - 1.2, S[2] - 0.3))).astype(np.float32)
for c in (0, 1):
    hiss = shaped(N, 250, 7000, -0.6)
    drops = np.zeros(N); k = rng.random(N) < 45 / SR; drops[k] = rng.uniform(0.2, 1.0, k.sum())
    ker = np.sin(2 * np.pi * rng.uniform(2500, 4500) * tt(240)) * np.exp(-tt(240) / 0.0015)
    drops = np.fft.irfft(np.fft.rfft(drops, N + 240) * np.fft.rfft(ker, N + 240), N + 240)[:N]
    RAIN[c] += ((0.8 * hiss + 0.25 * drops / (np.max(np.abs(drops)) + 1e-9)) * rain_env * 1.3).astype(np.float32)
def thunder(seed):
    n = int(3.6 * SR); t = tt(n)
    crack = shaped(n, 900, 9000) * np.exp(-t / 0.05)
    rumble = shaped(n, 25, 260, -1.0) * (np.exp(-t / 1.1) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.7 * t + seed) ** 2))
    return 0.35 * crack + rumble

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
for k in (2, 5, 7): at(S[k] - 0.4, whoosh(0.8), 0.20, -0.2)           # act wipes
# ACT 1: thunder after each flash, loss count-up ticks, the 30-minute clock ticking, "?" pops
for f, seed, g in ((1.6, 0.3, 0.34), (3.4, 1.1, 0.26), (9.6, 1.9, 0.3)): at(f + 0.35, thunder(seed), g, -0.3 if f < 5 else 0.3)
for k in range(10): at(5.7 + 1.6 * (k / 10) ** 0.8, tick(), 0.06, -0.3)
at(7.4, pop(820), 0.08, -0.3)
for k in range(int(S[2] - S[1] - 1.0)): at(S[1] + 1.0 + k, tick(), 0.07 + 0.01 * (k % 2), 0.4)
for i in range(7): at(S[1] + 6.4 + i * 0.25, pop(500 + 50 * i), 0.07, -0.4 + 0.13 * i)
# ACT 2: cut to silence, a single ding, gauge count-up, activation hit, drone hum, drips, input checks, route draw, chime
at(S[2] + 0.05, bell(1760, 0.5), 0.10); at(S[2] + 0.2, sweep(2.6, 300, 1400), 0.05)
for k in range(12): at(S[2] + 0.5 + 2.2 * (k / 12) ** 0.9, tick(), 0.06, 0.3)
at(S[2] + 2.75, bell(1318, 0.4), 0.09, 0.4); at(S[2] + 2.9, bell(1760, 0.4), 0.08, 0.4)
at(S[2] + 5.0, thud(), 0.16); at(S[2] + 5.02, chime(74), 0.12)
at(S[3] + 0.8, drone_hum(2.6), 0.10, -0.1)
for uu, f in ((1.75, 1500), (2.3, 1300), (2.9, 1150)): at(S[3] + uu, drip(f), 0.11, -0.2)
for i in range(4): at(S[3] + 1.15 + 0.6 * i, pop(640 + 70 * i), 0.08, 0.5)
at(S[3] + 3.6, sweep(1.4, 400, 1300), 0.05, -0.2)
for n in range(1, 5): at(S[3] + 3.5 + n * 0.3, pop(700 + 80 * n), 0.07, -0.2)
at(S[3] + 4.95, chime(76), 0.08); at(S[3] + 6.0, whoosh(0.6), 0.08)
for rt in (10.2, 11.75, 12.9, 15.6): at(S[3] + 6.0 + rt - 6.5, click(), 0.12, 0.3)
at(S[3] + 6.0 + 11.8 - 6.5, sweep(0.5, 600, 1100), 0.04, 0.3); at(S[3] + 6.0 + 15.65 - 6.5, chime(76), 0.06)
# ACT 3: heartbeat under the race, lock-on finds, clock ticks, finish bell, phone shutter, lock sting
r0, r1 = sc(5, 1.0), sc(5, 9.6)
for k in range(int((r1 - r0) / 0.6)):
    at(r0 + k * 0.6, thud(), 0.07 + 0.02 * (k % 2), 0); at(r0 + k * 0.6 + 0.18, thud(), 0.045, 0)
for k in range(15): at(r0 + k * (r1 - r0) / 15, tick(), 0.045, 0.6)
for i, m in enumerate((1.75, 3.5, 5.25, 9.67, 12.33, 19.0, 26.5)): at(r0 + (r1 - r0) * m / 30, blip(1760 + 60 * (i % 3)), 0.09, 0.35)
for m in (4.0, 26.5): at(r0 + (r1 - r0) * m / 30 + 0.05, bell(784, 0.25), 0.06, -0.35)
at(r1 + 0.05, bell(523, 1.1), 0.08)
at(sc(6, 3.2), whoosh(0.5), 0.08, 0.6)
for d in (1.0, 1.95, 2.4, 3.25): at(sc(6, 3.2 + d), click(), 0.12, 0.6)
at(sc(6, 3.2 + 1.05), blip(1480), 0.08, 0.6); at(sc(6, 3.2 + 3.3), chime(79), 0.06, 0.6)
at(sc(6, 8.6), whoosh(0.5), 0.07)
for d in (1.3, 3.15): at(sc(6, 8.5 + d), click(), 0.12, 0.2); at(sc(6, 8.5 + d + 0.08), pop(880), 0.06, 0.2)
at(sc(6, 10.4), chime(79), 0.07)
# ACT 4: gentle whooshes, check-ins, match-cut whoosh, ask hit, closing chime
at(sc(7, 2.6), whoosh(0.5), 0.07, -0.3)
for i in range(3): at(sc(7, 3.1 + 0.9 * i), pop(700 + 50 * i), 0.07, -0.3)
at(sc(7, 8.0), whoosh(0.9), 0.10)
at(sc(8, 0.6), thud(), 0.14); at(sc(8, 0.62), chime(74), 0.10)
at(sc(8, 9.4), chime(74), 0.08); at(sc(8, 9.45), bell(587, 1.4), 0.06)

# ACT 2b: Field Node 3D beat: servo-like whir on the explode, clicks on reassembly, pops on callouts
at(S[4] + 0.2, whoosh(0.6), 0.07); at(S[4] + 1.8, sweep(1.6, 500, 1600), 0.05, 0.2)
for i, d in enumerate((1.8, 2.6, 3.4, 4.4)): at(S[4] + d, pop(700 + 70 * i), 0.07, 0.5)
at(S[4] + 5.6, click(), 0.12); at(S[4] + 6.1, click(), 0.12); at(S[4] + 6.3, chime(76), 0.06)
# v6: real-footage entries
at(S[2] + 6.0, whoosh(0.7), 0.09)                  # laptop arrives with the alert
at(S[4] + 7.0, whoosh(0.5), 0.07); at(S[4] + 8.1, click(), 0.12, 0.3)   # sensor node page, Exploded
at(S[5] + 10.0, whoosh(0.6), 0.08)                  # Compare screen
# ---------------- mix with ducking ----------------
w = wave.open("voice_track_v5.wav"); voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
def smooth(x, sec): k = max(1, int(sec * SR)); c = np.cumsum(np.insert(x, 0, 0)); y = (c[k:] - c[:-k]) / k; return np.pad(y, (k // 2, k - 1 - k // 2), mode="edge")
lvl = np.sqrt(smooth(voice ** 2, 0.08)); gate = np.clip(lvl / 0.05, 0, 1)
gate = np.maximum(gate, np.roll(smooth(gate, 0.45), int(0.2 * SR)))      # hold ~0.4 s after speech
duck = smooth(gate, 0.12)
music_gain = (0.48 * (1 - 0.58 * duck)).astype(np.float32)
rain_gain = (0.20 * (1 - 0.40 * duck)).astype(np.float32)
mixL = voice * 0.92 + MUS[0] * music_gain + RAIN[0] * rain_gain + SFX[0] * (1 - 0.25 * duck)
mixR = voice * 0.92 + MUS[1] * music_gain + RAIN[1] * rain_gain + SFX[1] * (1 - 0.25 * duck)
mix = np.stack([mixL, mixR], 1)
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
mix *= 0.89 / np.max(np.abs(mix))
for name, part in (("music", MUS[0] * music_gain), ("rain", RAIN[0] * rain_gain), ("sfx", SFX[0]), ("voice", voice)):
    print(f"{name:6s} peak {np.max(np.abs(part)):.2f}  rms {np.sqrt(np.mean(part ** 2)):.3f}")
np.savez_compressed("mixparts_v5.npz", music=(MUS[0] * music_gain)[::480], rain=(RAIN[0] * rain_gain)[::480], sfx=SFX[0][::480], voice=voice[::480])
w = wave.open("soundtrack_v5.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack_v5.wav", "-c:a", "aac", "-b:a", "192k", "soundtrack_v5.m4a"], check=True)
print("soundtrack:", f"{N / SR:.2f}s")
