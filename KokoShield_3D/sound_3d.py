"""Soundtrack for the interactive 3D page on the v4 (9-scene) story: v4 voice + score, the v3 3D sound cues re-timed through
the same story map the page uses, plus drone-sequence cues. Writes assets/soundtrack3d.m4a and assets/soundtrack3d.mp3."""
import json, re, pathlib
import numpy as np

V = pathlib.Path("../video"); V4 = V / "v4"
src = (V / "sound.py").read_text(encoding="utf-8")
cut = lambda a, b: src[src.index(a): src.index(b)]
inst = cut("def sm(x)", "# ---------------- score ----------------")
sfxlib = cut("# ---------------- SFX library ----------------", "def at(t, sig, g, pan=0.0)")
cues3 = cut("def at(t, sig, g, pan=0.0)", "# ---------------- mix with ducking ----------------").split("\n", 1)[1]
mix = src[src.index("# ---------------- mix with ducking ----------------"):]
mix = (mix.replace('wave.open("voice_track.wav")', f'wave.open(r"{(V4 / "voice_track_v4.wav").resolve()}")')
          .replace('np.savez_compressed("mixparts.npz"', 'np.savez_compressed("mixparts3d.npz"')
          .replace('wave.open("soundtrack.wav", "wb")', 'wave.open("soundtrack3d.wav", "wb")')
          .replace('subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack.wav", "-c:a", "aac", "-b:a", "192k", str(ROOT / "KokoShield_3D/assets/soundtrack.m4a")], check=True)',
                   'subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack3d.wav", "-c:a", "aac", "-b:a", "192k", "assets/soundtrack3d.m4a"], check=True)\n'
                   'subprocess.run([FF, "-y", "-loglevel", "error", "-i", "soundtrack3d.wav", "-c:a", "libmp3lame", "-b:a", "160k", "assets/soundtrack3d.mp3"], check=True)'))
assert "soundtrack3d.mp3" in mix and "voice_track_v4" in mix

data = pathlib.Path("assets/data.js").read_text(encoding="utf-8")
S3 = json.loads(re.search(r"window\.KS_STARTS=(\[.*?\]);", data).group(1))
S4 = json.loads(re.search(r"window\.KS4_STARTS=(\[.*?\]);", data).group(1))
DR = 7.6
SEGS = [[S4[0], S4[1], S3[0], S3[1]], [S4[1], S4[2], S3[1], S3[2]], [S4[2], S4[3], S3[2], S3[3]], [S4[3], S4[3] + DR, None, None],
        [S4[3] + DR, S4[4], S3[3] + 0.4, S3[3] + 5.6], [S4[4], S4[5], S3[3] + 5.6, S3[4]], [S4[5], S4[6], S3[4], S3[5]], [S4[6], S4[7], S3[5], S3[6]],
        [S4[7], S4[8], S3[6], S3[7]], [S4[8], S4[9], S3[7], S3[8]]]
def inv(t3):
    for a, b, c, d in SEGS:
        if c is not None and c <= t3 < d: return a + (t3 - c) / (d - c) * (b - a)
    if S3[3] <= t3 < S3[3] + 0.4: return S4[3] + DR - 0.4 + (t3 - S3[3])
    return S4[9] + (t3 - S3[8]) if t3 >= S3[8] else 0.0

ns = {}
head = f"""
import json, wave, subprocess
import numpy as np, imageio_ffmpeg
SR = 48000; FF = imageio_ffmpeg.get_ffmpeg_exe()
S4 = {S4}; END = S4[-1]; N = int(END * SR); rng = np.random.default_rng(11); T = np.arange(N) / SR
"""
exec(head + inst, ns)
ns.update(inv=inv, SEGS=SEGS, S3=S3, DR=DR)
# music: the v4 score, timed on the v4 story
score = (V4 / "parts/score.py").read_text(encoding="utf-8")
music = score[: score.index("# ---------------- ambience")].replace("S[", "S4[")
exec(music, ns)
# ambience: rain that matches the 3D page (story-mapped) plus the drone's post-rain flight, thunder after each flash
exec("""
t3 = np.full(N, np.nan)
for a, b, c, d in SEGS:
    if c is None: continue
    m = (T >= a) & (T < b); t3[m] = c + (T[m] - a) / (b - a) * (d - c)
rain3 = np.nan_to_num(np.minimum(ramp(t3, 2.2, 5.0), 1 - ramp(t3, S3[2] + 2.5, S3[2] + 7)), nan=0.0)
u = T - S4[3]; rainD = 0.5 * np.minimum(ramp(u, 4.4, 5.0), 1 - ramp(u, 6.8, 7.4)); rainD[(u < 0) | (u > DR)] = 0
rain_env = np.maximum(rain3, rainD).astype(np.float32)
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
add(SFX, inv(4.95), thunder(0.3), 0.28, -0.3); add(SFX, inv(S3[1] + 5.85), thunder(1.7), 0.26, 0.35)
""", ns)
exec(sfxlib, ns)
exec((V4 / "parts/extra_sfx.py").read_text(encoding="utf-8"), ns)
# the 3D page's own cues (written against the v3 visual timeline), re-timed onto the story
exec("S = S3\ndef at(t, sig, g, pan=0.0): add(SFX, inv(t), sig, g, pan)\n" + cues3, ns)
# drone sequence (story time) and the extra scene boundary between the drone scene and the ranked route
exec("""
def atu(u, sig, g, pan=0.0): add(SFX, S4[3] + u, sig, g, pan)
atu(0.3, whoosh(0.6), 0.07); atu(0.3, drone_hum(6.7), 0.10, -0.1)
atu(4.6, bell(1175, 0.4), 0.07)
for uu, f in ((5.33, 1500), (5.83, 1300), (6.32, 1150)): atu(uu, drip(f), 0.12, -0.2)
atu(6.95, chime(79), 0.06)
add(SFX, S4[4] - 0.4, whoosh(0.8), 0.20, -0.2)
""", ns)
exec(mix, ns)
