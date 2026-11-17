
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

