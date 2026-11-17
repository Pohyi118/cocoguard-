"""Synthesised soundtrack for the KokoShield 3D video: music score + rain/thunder ambience + SFX synced to
on-screen events, ducked under the voice. Everything is generated here (no samples, no external services).
Inputs : voice_track.wav (from voice.py), KS_STARTS from data.js
Outputs: soundtrack.wav and KokoShield_3D/assets/soundtrack.m4a"""
import json, re, wave, subprocess, pathlib
import numpy as np, imageio_ffmpeg

SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("C:/Users/User/Documents/GSC")
S = json.loads(re.search(r"KS_STARTS=(\[.*?\]);", (ROOT / "KokoShield_3D/assets/data.js").read_text(encoding="utf-8")).group(1))
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

# ---------------- score ----------------
BAR = 2.5                                   # 96 bpm, 4/4
MINOR = [(47, [59, 62, 66]), (43, [55, 59, 62]), (40, [55, 59, 64]), (42, [54, 58, 61])]     # Bm G Em F#
MAJOR = [(38, [57, 62, 66]), (45, [57, 61, 64]), (47, [59, 62, 66]), (43, [55, 59, 62])]     # D A Bm G
OUTRO = [(38, [57, 62, 66]), (43, [55, 59, 62]), (45, [57, 61, 64]), (38, [57, 62, 66, 69])]  # D G A D
# section A: 0-45 s, minor, 2 bars per chord, sparse quarter plucks, low drone
add(MUS, 0.0, drone(35, 46.0), 0.10, 0.0)
for b in range(18):
    root, ch = MINOR[(b // 2) % 4]
    if b % 2 == 0:
        for j, m in enumerate(ch): add(MUS, b * BAR, pad(m, 2 * BAR - 0.2), 0.050, (j - 1) * 0.35)
    for q, idx in enumerate([0, 2, 1, 2]):
        if b < 2 and q % 2: continue
        add(MUS, b * BAR + q * BAR / 4, pluck(ch[idx] + 12, 0.8), 0.045 + 0.02 * (b >= 12), 0.25 * (idx - 1))
    if b >= 14:                                                  # build: 16th arps in the last 4 bars before the reveal
        for s16 in range(16): add(MUS, b * BAR + s16 * BAR / 16, pluck(ch[s16 % 3] + 24, 0.25), 0.012 + 0.006 * (b - 14), 0.4 * ((s16 % 3) - 1))
# riser into the solution reveal + soft impact at 45 s
n = int(2.6 * SR); add(MUS, 42.5, shaped(n, 800, 9000) * ramp(tt(n), 0, 2.6) ** 2, 0.06)
n = int(2.2 * SR); add(MUS, S[3] - 0.05, shaped(n, 300, 12000, -0.4) * np.exp(-tt(n) / 0.5), 0.07)
# section B: 45-107.5 s, major, 1 bar per chord, 8th-note marimba arps, bass, kick from 60 s, shaker 70-107 s
for b in range(18, 43):
    root, ch = MAJOR[(b - 18) % 4]; t0 = b * BAR
    for j, m in enumerate(ch): add(MUS, t0, pad(m, BAR - 0.1, 0.4, 1.0), 0.045, (j - 1) * 0.35)
    add(MUS, t0, bass(root, BAR - 0.15), 0.11)
    for e, idx in enumerate([0, 1, 2, 1, 0, 2, 1, 2]): add(MUS, t0 + e * BAR / 8, pluck(ch[idx] + 12, 0.7), 0.05, 0.3 * (idx - 1))
    if t0 >= 60:
        for beat in (0, 2): add(MUS, t0 + beat * BAR / 4, kick(), 0.16)
    if 70 <= t0 < 107.5:
        for e in range(8): add(MUS, t0 + e * BAR / 8, shaker(), 0.035 if e % 2 else 0.05, 0.3)
# outro: 107.5 s to end, gentle resolve and fade
for k, (root, ch) in enumerate(OUTRO):
    t0 = 107.5 + k * BAR * (1 if k < 3 else 1); last = k == 3; d = (END - t0) if last else BAR
    for j, m in enumerate(ch): add(MUS, t0, pad(m, d - 0.2, 0.5, 1.2 if not last else 0.6), 0.05, (j - 1.5) * 0.3)
    add(MUS, t0, bass(root, d - 0.3), 0.08)
    for e, idx in enumerate([0, 1, 2, 1] if not last else [0, 1, 2, 3]): add(MUS, t0 + e * BAR / 4, pluck(ch[idx] + 12, 1.2), 0.05, 0.3 * (idx - 1))
fade = (ramp(T, 0.0, 4.0) * (1 - ramp(T, END - 3.0, END - 0.1))).astype(np.float32)
MUS[0] *= fade; MUS[1] *= fade

# ---------------- ambience: rain + thunder ----------------
rain_env = np.minimum(ramp(T, 2.2, 5.0), 1 - ramp(T, S[2] + 2.5, S[2] + 7)).astype(np.float32)
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
add(SFX, 4.95, thunder(0.3), 0.28, -0.3); add(SFX, S[1] + 5.85, thunder(1.7), 0.28, 0.35)

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

def at(t, sig, g, pan=0.0): add(SFX, t, sig, g, pan)
# scene wipes (whoosh peaks at each boundary)
for k in range(1, 8): at(S[k] - 0.4, whoosh(0.8), 0.20, -0.2)
# 1 hook: clock ticks, ? markers, trigger alert
for k in range(9): at(1.25 + k * 0.25, tick(), 0.09, 0.2)
for k, f in enumerate([620, 760, 900, 700]): at(5.62 + k * 0.11, pop(f), 0.07, -0.5 + k * 0.33)
at(7.38, bell(988, 0.35), 0.10, 0.5); at(7.52, bell(1318, 0.35), 0.09, 0.5)
at(2.6, whoosh(0.45), 0.07, 0.6)
# 2 climate risk: stat cards, count-ups, country chips, pods turning
at(S[1] + 3.0, sweep(2.0, 220, 140), 0.06)
for c0 in (S[1] + 2.4, S[1] + 8.0, S[1] + 12.5): at(c0, whoosh(0.45), 0.08, -0.4)
for k in range(12): at(S[1] + 2.65 + 1.7 * (k / 12) ** 0.8, tick(), 0.06, -0.4)
at(S[1] + 4.4, pop(820), 0.09, -0.4)
for k in range(3): at(S[1] + 8.4 + k * 0.5, pop(640 + 90 * k), 0.08, 0.1 * k)
for k in range(14): at(S[1] + 12.95 + 2.0 * (k / 14) ** 0.8, tick(), 0.06, 0.4)
at(S[1] + 15.0, pop(900), 0.09, 0.4)
# 3 market gap: axes draw, competitor dots, empty corner, KokoShield lands
at(S[2] + 0.8, sweep(1.0, 400, 700), 0.05, 0.4)
for k, d in enumerate([2.4, 3.2, 4.0, 4.8, 5.6]): at(S[2] + d, pop(560 + 70 * k), 0.08, 0.5)
at(S[2] + 7.2, sweep(1.2, 900, 1600), 0.04, 0.6)
at(S[2] + 9.6, thud(), 0.16, 0.6); at(S[2] + 9.62, chime(74), 0.11, 0.6)
# 4 solution: Field Node explodes, data pulses, blocks recolour, stops + route, phone
at(S[3] + 1.0, clunk(), 0.14); at(S[3] + 1.05, whoosh(0.5), 0.07)
at(S[3] + 2.2, blip(880), 0.10); at(S[3] + 3.8, blip(988), 0.09); at(S[3] + 4.95, clunk(), 0.10)
at(S[3] + 5.6, sweep(1.2, 500, 1500), 0.05)
for k in range(4): at(S[3] + 6.62 + k * 0.7, pop(660 + 110 * k), 0.09, -0.3 + 0.2 * k)
at(S[3] + 6.5, sweep(3.3, 300, 900), 0.035, 0.0)
at(S[3] + 10.0, bell(1175, 0.4), 0.07, -0.5); at(S[3] + 9.6, whoosh(0.5), 0.08, 0.7)
# 5 record and confirm: phone, taps, status flips
at(S[4] + 1.0, whoosh(0.5), 0.08, 0.7); at(S[4] + 1.6, whoosh(0.45), 0.06, -0.6)
for k in range(3): at(S[4] + 4.2 + 1.4 * k, tick(), 0.08, 0.6)
at(S[4] + 4.6, bell(1318, 0.45), 0.10, -0.4); at(S[4] + 6.0, bell(1480, 0.45), 0.10, -0.4); at(S[4] + 7.4, thud(), 0.16, -0.4)
at(S[4] + 8.2, chime(79), 0.06, -0.4)
# 6 pilot race: start beeps, clock, finds, end bell, missed buzz, fact check-ins
r0 = S[5] + 1.2
at(r0 - 0.5, bell(660, 0.18), 0.08); at(r0, bell(880, 0.25), 0.09)
for k in range(15): at(r0 + k * 0.8, tick(), 0.05, 0.6)
for m, pods in ((7, 3), (14, 2), (22, 1), (30, 1)):
    for p in range(pods): at(r0 + 12 * m / 30 + p * 0.09, bell(1568 + 120 * p, 0.3), 0.08, 0.5)
for m in (8, 30): at(r0 + 12 * m / 30 + 0.05, bell(784, 0.25), 0.07, 0.5)
at(r0 + 12.05, bell(523, 1.1), 0.08)
at(S[5] + 13.3, buzz(), 0.09, -0.3); at(S[5] + 13.55, buzz(), 0.08, -0.3)
at(S[5] + 14.4, whoosh(0.5), 0.08, 0.6)
for k in range(6): at(S[5] + 14.85 + k * 0.75, pop(700 + 50 * k), 0.07, 0.6)
# 7 impact and market: cards, money flow, farm dots
at(S[6] + 0.9, whoosh(0.5), 0.08)
at(S[6] + 6.8, whoosh(0.5), 0.08)
for k in range(5): at(S[6] + 7.2 + k * 1.6, blip(1320), 0.03, -0.3); at(S[6] + 7.9 + k * 1.6, blip(1480), 0.03, 0.3)
at(S[6] + 9.6, whoosh(0.45), 0.07)
for k in range(20): at(S[6] + 10.4 + 2.0 * k / 20, tick(), 0.05, -0.2)
for k in range(20): at(S[6] + 13.2 + 2.0 * k / 20, tick(), 0.05, 0.2)
at(S[6] + 15.25, chime(76), 0.07)
# 8 close: title chime and final sting
at(S[7] + 0.85, chime(74), 0.09, -0.3)
at(END - 2.6, bell(587, 1.4), 0.07); at(END - 2.55, bell(880, 1.4), 0.05)

# ---------------- mix with ducking ----------------
w = wave.open("voice_track.wav"); voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
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
np.savez_compressed("mixparts.npz", music=(MUS[0] * music_gain)[::480], rain=(RAIN[0] * rain_gain)[::480], sfx=SFX[0][::480], voice=voice[::480])
w = wave.open("soundtrack.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack.wav", "-c:a", "aac", "-b:a", "192k", str(ROOT / "KokoShield_3D/assets/soundtrack.m4a")], check=True)
print("soundtrack:", f"{N / SR:.2f}s")
