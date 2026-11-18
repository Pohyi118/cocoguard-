"""Soundtrack for v8: no music; CC0 sound effects (sfx/) + Flow clip ambience + birdsong, rain, thunder and a tropical bed, under the voice, mixed to -16 LUFS.
Reads timeline.json (voice) and shots.json (compose_v6.py). Writes work/music.wav, work/ambience.wav, work/mix.wav, work/mix_bed.wav (-25 LUFS, no voice)."""
import json, pathlib, subprocess, wave
import numpy as np, imageio_ffmpeg
from scipy.signal import butter, sosfilt, fftconvolve

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000; HERE = pathlib.Path(__file__).parent; WORK = HERE / "work"
TL = json.load(open(HERE / "timeline.json")); SC = {s["id"]: s for s in TL["scenes"]}; END = TL["end"]; N = int((END + 0.5) * SR)
rng = np.random.default_rng(7)


def wt(sid, word, occ=1):
    n = 0
    for a, b, w in SC[sid]["words"]:
        if w.lower().strip(".,;:") == word.lower():
            n += 1
            if n == occ: return SC[sid]["speech_at"] + a
    raise KeyError(word)


def read_wav(p):
    w = wave.open(str(p)); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; ch = w.getnchannels(); w.close()
    return x.reshape(-1, ch).mean(1) if ch > 1 else x


def write_wav(p, x):
    x = np.atleast_2d(x.T).T if x.ndim == 1 else x
    w = wave.open(str(p), "wb"); w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


lp = lambda x, f, o=2: sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f, o=2: sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
bp = lambda x, a, b, o=2: sosfilt(butter(o, [a, b], "band", fs=SR, output="sos"), x)
mus = np.zeros((N, 2))
def put(sig, t, g=1.0, pan=0.0):
    i = int(t * SR); sig = sig[: max(0, N - i)]
    if len(sig) == 0 or i >= N: return
    mus[i:i + len(sig), 0] += sig * g * np.sqrt(0.5 * (1 - pan)) * 1.414
    mus[i:i + len(sig), 1] += sig * g * np.sqrt(0.5 * (1 + pan)) * 1.414


# ---------------- no score: placed sound effects (Freesound, CC0) on the SFX bus ----------------
s3 = SC[5]["start"]; t_then = wt(2, "Then"); t_flash = wt(2, "comes") + SC[2]["words"][-1][1] - SC[2]["words"][-1][0] + 0.3
FX = {}
def fx(name, a=0.0, z=None, fade=0.05):
    """Load a CC0 effect from sfx/ (cached), trimmed to [a, z] seconds, mono, peak-normalised."""
    key = (name, a, z)
    if key not in FX:
        f = next((HERE / "sfx").glob(name + "_fs*.wav")); x = read_wav(f)[int(a * SR): int(z * SR) if z else None].copy()
        k = min(len(x) // 3, int(fade * SR)); x[-k:] *= np.linspace(1, 0, k) if k else 1
        FX[key] = x / (np.abs(x).max() + 1e-9)
    return FX[key]
def tick_bed(t0, t1, g):
    x = fx("clock_tick", 0.3, 5.2); n = int((t1 - t0) * SR); y = np.tile(x, n // len(x) + 1)[:n]
    k = int(0.25 * SR); y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k); put(y, t0, g)
wt_end = lambda sid, w: [SC[sid]["speech_at"] + b for a, b, x in SC[sid]["words"] if x.lower().strip(".,;:?!") == w.lower()][0]

# thunder: a real recording, its crack 0.35 s in, on the lightning flash after "Then the rain comes"
thunder = read_wav(HERE / "sfx/thunder_loganzsound_840628.wav")
put(thunder / np.abs(thunder).max() * 0.85, t_flash - 0.35)
# black pod photos land
for w in ("black", "splashes", "carry"): put(fx("whoosh_light", 0.2, 1.2), wt(3, w) - 0.1 - 0.25, 0.10, pan=0.2)
# the golden half-hour clock, and its return at "Two minutes in"
tick_bed(wt(4, "golden") - 0.1, SC[4]["end"] - 0.2, 0.10)
tick_bed(wt(9, "Two") - 0.1, wt(9, "He") - 0.35, 0.10)
# KokoShield logo: one soft bell, the film's only musical note
logo_t = SC[5]["start"] + 0.35
put(fx("bell_ambient", 0.2, 4.5, fade=1.5), logo_t - 0.4, 0.22)
# the app's rain alert
put(fx("notify_soft", 0, 1.2), wt(5, "millimetres") + 0.25, 0.16)
# Field Node labels slide out, then the four clues connect and every block gets a score
put(fx("whoosh_digital", 0, 1.0), wt(6, "damp") - 0.35, 0.12)
L0 = wt(6, "Add") + 0.6
for j, t in enumerate((L0 + 0.1, L0 + 0.25, max(wt(6, "rain"), L0 + 0.4), max(wt(6, "past"), L0 + 0.55))): put(fx("ui_blip"), t + 0.15, 0.10, pan=-0.3 if j % 2 == 0 else 0.3)
put(fx("kalimba_notify"), wt(6, "score") - 0.35, 0.14)
# the plan: one soft click per block as the route is drawn (A, D, B, G)
for w in ("A", "D", "B", "G"): put(fx("ui_click"), wt(7, w) - 0.2, 0.18)
# the phone slides in, the photo, the adviser's confirmation
put(fx("whoosh_digital", 0, 1.0), wt(8, "His") - 0.25 - 0.4, 0.10)
put(fx("camera_shutter"), wt_end(9, "photo") - 0.05, 0.22)
put(fx("success_melody", 0, 1.9, fade=0.4), wt(9, "confirms") + 0.15, 0.12)
# the race (times as in race/build_race2.py): ticking runs, a pop per pod found, the missed blocks, the rewind, the tally
C0 = SC[10]["start"]; T0 = wt(10, "routes") + 0.2; MISS = wt(11, "walks") - 0.1; K0 = wt(11, "KokoShield's") - 0.15; NONE = wt(11, "none") - 0.1
DU = MISS - 0.15 - T0; DK = NONE - K0; RW = K0 - 0.95
tick_bed(T0, T0 + DU, 0.07); tick_bed(K0, K0 + DK, 0.07)
for m in (4.0, 26.5): put(fx("pop_soft"), T0 + DU * m / 30 - 0.1, 0.20)
for m in (1.75, 3.5, 5.25, 9.67, 12.34, 19.0, 26.5): put(fx("pop_soft"), K0 + DK * m / 30 - 0.1, 0.20)
put(fx("ui_back"), MISS, 0.20)
put(fx("rewind_tape", 0.15, 1.15, fade=0.3), RW, 0.07)
put(fx("kalimba_notify"), NONE + 0.6, 0.12)
# the map pin, then the closing bell under the name
put(fx("pop_soft"), wt(12, "Sepat") - 0.1 + 0.35, 0.22)
brand_t = wt(12, "KokoShield") - 0.3
put(fx("bell_bowl", 0, 6.0, fade=2.5), brand_t + 0.1, 0.20)

# ---------------- ambience: the clips' own sound, levelled, plus rain ----------------
amb = np.zeros(N)
for s in json.load(open(HERE / "shots.json")):
    if not s["audio"]: continue
    d_out = s["t1"] - s["t0"]; d_src = max(0.2, s["src1"] - s["src0"])
    tmp = WORK / "seg.wav"; tempo = min(2.0, max(0.5, d_src / d_out))
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{s['src0']:.3f}", "-t", f"{d_src:.3f}", "-i", s["path"], "-vn", "-ac", "1", "-ar", str(SR),
                    "-af", f"atempo={tempo:.4f}", str(tmp)], check=False)
    if not tmp.exists() or tmp.stat().st_size < 1000: continue
    x = read_wav(tmp); tmp.unlink()
    if len(x) < 100: continue
    rms = np.sqrt(np.mean(x ** 2)) + 1e-6; x = x * min(8.0, 10 ** (-30 / 20) / rms)
    n = len(x); f = int(0.25 * SR); env = np.ones(n); env[:f] = np.linspace(0, 1, f) if n > 2 * f else 1; env[-f:] = np.linspace(1, 0, f) if n > 2 * f else 1
    i = int(s["t0"] * SR); amb[i:i + n] += (x * env)[: N - i]
# birdsong under the time-lapse and the dry pod (the growth clips' own sound, at real speed), gone as the rain starts
birds = np.zeros(int(14 * SR)); pos = 0
for clip, a, z in (("growth_1a_flower_to_cherelle.mp4", 0.25, 2.1), ("growth_1b_cherelle_to_young.mp4", 0.25, 3.6), ("growth_2_young_to_ripe.mp4", 0.5, 4.0)):
    tmp = WORK / "seg.wav"   # only the part of each clip that has sound, levelled on its own, overlapped by 0.3 s
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(a), "-t", str(z - a), "-i", str(HERE.parent / "v5/flow_clips" / clip), "-vn", "-ac", "1", "-ar", str(SR), str(tmp)], check=False)
    if tmp.exists() and tmp.stat().st_size > 1000:
        x = read_wav(tmp); x = x / (np.sqrt(np.mean(x ** 2)) + 1e-6)
        k = int(0.3 * SR); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k)
        birds[pos:pos + len(x)] += x; pos += len(x) - k
    tmp.unlink(missing_ok=True)
if pos:
    b = birds[:pos]; b = b * 10 ** (-32 / 20) / (np.sqrt(np.mean(b ** 2)) + 1e-6)
    n = min(len(b), int((t_then + 0.8) * SR)); b = b[:n] * np.interp(np.arange(n) / SR, [0, 0.8, t_then - 0.2, t_then + 0.8], [0, 1, 1, 0])
    amb[:n] += b
# a quiet tropical bed (birds, frogs, insects) from the black pod scene on, so the app scenes never go silent
trop = read_wav(next((HERE / "sfx").glob("amb_tropical_fs*.wav"))); trop = trop / (np.sqrt(np.mean(trop ** 2)) + 1e-6)
reps = np.tile(trop, N // len(trop) + 1)[:N]
amb += reps * np.interp(np.arange(N) / SR, [0, SC[3]["start"] + 1.0, SC[3]["start"] + 3.0, END - 1.5, END], [0, 0, 1, 1, 0]) * 10 ** (-41 / 20)
rain_n = rng.standard_normal(N); rain = bp(rain_n, 900, 9000) * 0.5 + lp(rain_n, 500) * 0.2
drops = np.zeros(N); idx = rng.integers(0, N, int(END * 18)); drops[idx] = rng.uniform(0.2, 1, len(idx)); rain += hp(fftconvolve(drops, np.exp(-np.arange(400) / 60))[:N], 1500) * 0.4
tt = np.arange(N) / SR
rain_env = np.interp(tt, [0, t_then - 0.1, t_then + 0.6, t_flash, SC[3]["end"], SC[4]["end"], s3 + 2.0, END], [0, 0, 0.45, 1.0, 0.8, 0.45, 0.0, 0.0])
amb += rain * rain_env * 10 ** (-33 / 20) / np.sqrt(np.mean(rain ** 2))

# ---------------- mix ----------------
voice = np.zeros(N); v = read_wav(HERE / "voice_v6.wav"); voice[: len(v)] = v[:N]
from scipy.ndimage import uniform_filter1d
env = uniform_filter1d(uniform_filter1d(np.abs(voice), int(0.3 * SR)), int(0.3 * SR))
duck = np.clip(env / (env.max() * 0.08), 0, 1)
music_g = (0.9 * (1 - 0.35 * duck))[:, None]; amb_g = 0.9 * (1 - 0.45 * duck)   # mus now carries the sound effects
mix = mus * music_g + (amb * amb_g)[:, None] + voice[:, None] * 0.95
bed = mus * 0.62 + (amb * 0.9)[:, None]
write_wav(WORK / "music.wav", mus); write_wav(WORK / "ambience.wav", amb); write_wav(WORK / "voice_stem.wav", voice)
for name, x, lufs in (("mix", mix, -16), ("mix_bed", bed, -25)):
    write_wav(WORK / f"{name}_raw.wav", x / max(1e-6, np.abs(x).max()) * 0.8)
    r = subprocess.run([FF, "-hide_banner", "-i", str(WORK / f"{name}_raw.wav"), "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"): r.rindex("}") + 1])
    af = (f"loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(WORK / f"{name}_raw.wav"), "-af", af, "-ar", str(SR), str(WORK / f"{name}.wav")], check=True)
    print(name, "measured", m["input_i"], "->", lufs)
