
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

